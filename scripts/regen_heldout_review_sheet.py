"""Regenerate evaluation/heldout/test_review_sheet.csv from the held-out labels (developer only).

Run by the developer, never by an agent (D-064): it reads `evaluation/heldout/`. It prints
counts and hash checks only, never label content.

- Read-only on every benchmark file: labels, inputs and manifest are opened for reading, and
  their SHA-256 is compared before and after, so labels, hashes, splits and status cannot
  change.
- Columns: the header already in the sheet is reused exactly. If the header is missing, the
  original 20-column layout is used. Cell formats mirror
  `evaluation/benchmark/dev_review_sheet.csv`.
- REVIEW_* columns start empty, as in the original sheet. Review entries lost in the
  truncation cannot be recovered from the labels.
- Atomic: writes a temp file in the same directory, fsyncs it, then os.replace().
- Refuses to overwrite a sheet that still has data rows unless --force is given.

Usage (from the repo root):  python3 -I scripts/regen_heldout_review_sheet.py [--force]
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LABELS = ROOT / "evaluation/heldout/test_labels.jsonl"
SHEET = ROOT / "evaluation/heldout/test_review_sheet.csv"
INPUTS = ROOT / "evaluation/benchmark/test_inputs.jsonl"
MANIFEST = ROOT / "evaluation/benchmark/manifest.json"

# The original layout, the same as the dev sheet before review batch 1 added key_points.
ORIGINAL_COLUMNS = [
    "case_id",
    "category",
    "family_id",
    "question",
    "answerable",
    "expected_behaviour",
    "required_rule_ids",
    "conditional_rule_ids",
    "optional_rule_ids",
    "required_missing_fields",
    "expected_conflicts",
    "out_of_scope",
    "prohibited_conclusions",
    "evidence_fact_ids",
    "unresolved_refs",
    "requires_source_check",
    "check_reasons",
    "REVIEW_decision (approve/edit/reject)",
    "REVIEW_source_checked (yes/no)",
    "REVIEW_notes",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def join(items: list[str]) -> str:
    return "; ".join(items)


def conflict(c: dict[str, Any]) -> str:
    # Dev format: "<field> (<kind>, material=<bool>)"; multiple fields are joined with " + ".
    return f"{' + '.join(c['fields'])} ({c['kind']}, material={c['material']})"


def out_of_scope(o: dict[str, Any]) -> str:
    return f"{o['code']}:{o['topic']}" if o.get("topic") else o["code"]


def row_for(label: dict[str, Any], question: str) -> dict[str, str]:
    review = label["review"]
    return {
        "case_id": label["case_id"],
        "category": label["category"],
        "family_id": label["family_id"],
        "question": question,
        "answerable": label["answerable"],
        "expected_behaviour": join(label["expected_behaviour"]),
        "required_rule_ids": join(label["required_rule_ids"]),
        "conditional_rule_ids": join(label["conditional_rule_ids"]),
        "optional_rule_ids": join(label["optional_rule_ids"]),
        "required_missing_fields": join(label["required_missing_fields"]),
        "expected_conflicts": join([conflict(c) for c in label["expected_conflicts"]]),
        "out_of_scope": join([out_of_scope(o) for o in label["out_of_scope"]]),
        "key_points": " | ".join(label["key_points"]),
        "prohibited_conclusions": " | ".join(
            f"{p['id']} [{p['severity']}] {p['text']}" for p in label["prohibited_conclusions"]
        ),
        "evidence_fact_ids": join(label["evidence_fact_ids"]),
        "unresolved_refs": join(label["unresolved_refs"]),
        "requires_source_check": "yes" if review["requires_source_check"] else "no",
        "check_reasons": join(review.get("reasons", [])),
        "REVIEW_decision (approve/edit/reject)": "",
        "REVIEW_source_checked (yes/no)": "",
        "REVIEW_notes": "",
    }


def existing_sheet() -> tuple[list[str] | None, int]:
    """Return the sheet's current header (if any) and its number of data rows."""
    if not SHEET.exists() or not SHEET.read_text(encoding="utf-8").strip():
        return None, 0
    with SHEET.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        return header, sum(1 for r in reader if any(cell.strip() for cell in r))


def main() -> None:
    force = "--force" in sys.argv[1:]
    for p in (LABELS, INPUTS, MANIFEST):
        if not p.exists():
            sys.exit(f"missing: {p.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    before = {p: sha256(p) for p in (LABELS, INPUTS, MANIFEST)}
    committed = manifest["heldout_labels_sha256"]
    match = "match" if before[LABELS] == committed else "MISMATCH"
    print(f"labels hash vs manifest commitment: {match}")

    header, data_rows = existing_sheet()
    if data_rows and not force:
        sys.exit(f"sheet still has {data_rows} data rows; refusing to overwrite (use --force)")
    columns = header or ORIGINAL_COLUMNS
    known = set(row_for({"case_id": "", **_EMPTY_LABEL}, "").keys())
    unknown = [c for c in columns if c not in known]
    if unknown:
        sys.exit(f"sheet header has columns this script cannot fill: {unknown}")

    labels = read_jsonl(LABELS)
    questions = {r["case_id"]: r["question"] for r in read_jsonl(INPUTS)}
    if {lab["case_id"] for lab in labels} != set(questions):
        sys.exit("case IDs in the labels and test_inputs.jsonl differ; nothing written")
    order = list(questions)  # test_inputs order, as in the original sheet
    by_id = {lab["case_id"]: lab for lab in labels}

    fd, tmp = tempfile.mkstemp(dir=SHEET.parent, prefix=".test_review_sheet.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
            w.writeheader()
            for cid in order:
                w.writerow(row_for(by_id[cid], questions[cid]))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, SHEET)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise

    after = {p: sha256(p) for p in before}
    if after != before:
        sys.exit("ERROR: a benchmark file changed during regeneration; investigate")
    print(f"wrote {len(order)} rows x {len(columns)} columns to {SHEET.relative_to(ROOT)}")
    print("labels, inputs and manifest unchanged (SHA-256 before == after)")


# A minimal label used only to list the columns row_for() can fill.
_EMPTY_LABEL: dict[str, Any] = {
    "category": "",
    "family_id": "",
    "answerable": "",
    "expected_behaviour": [],
    "required_rule_ids": [],
    "conditional_rule_ids": [],
    "optional_rule_ids": [],
    "required_missing_fields": [],
    "expected_conflicts": [],
    "out_of_scope": [],
    "key_points": [],
    "prohibited_conclusions": [],
    "evidence_fact_ids": [],
    "unresolved_refs": [],
    "review": {"requires_source_check": False},
}

if __name__ == "__main__":
    main()
