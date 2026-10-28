"""Dataset C: benchmark schema, access-controlled loaders and validation.

Design and rubric: docs/evaluation_benchmark.md.

Files:
  evaluation/benchmark/dev.jsonl          development cases: inputs and labels (tracked)
  evaluation/benchmark/test_inputs.jsonl  held-out inputs only, no labels (tracked)
  evaluation/heldout/test_labels.jsonl    held-out labels (Git-ignored until final scoring)
  evaluation/benchmark/manifest.json      counts, split, families and the SHA-256 commitment
                                          of the held-out labels (tracked)

Held-out labels are released only by `load_test_labels(final=True)` with
BTO_BUDDY_FINAL_EVAL=1, a frozen manifest and a matching hash (D-064). Prompt tuning and model
selection use dev cases only (REQ-EVL-022).

Usage:
  python -m evaluation.benchmark validate             # dev labels + test inputs
  python -m evaluation.benchmark validate --heldout   # authoring/review only; prints IDs/counts
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from bto_buddy import policy
from bto_buddy.schemas import TOPIC_TIER, Topic

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "evaluation" / "benchmark"
HELDOUT = ROOT / "evaluation" / "heldout"
DEV_PATH = BENCH / "dev.jsonl"
TEST_INPUTS_PATH = BENCH / "test_inputs.jsonl"
TEST_LABELS_PATH = HELDOUT / "test_labels.jsonl"
MANIFEST_PATH = BENCH / "manifest.json"
FINAL_ENV = "BTO_BUDDY_FINAL_EVAL"

Category = Literal[
    "standard",
    "missing_information",
    "policy_exception",
    "misconception",
    "conflicting",
    "out_of_scope",
]
Behaviour = Literal[
    "provide_guidance",  # give the applicable preparation steps with sources
    "ask_follow_up",  # ask for the named missing fields; guidance stays conditional
    "flag_conflict",  # point out the contradiction and ask; no guidance relying on it
    "correct_misconception",  # correct the user's wrong assumption with the source fact
    "state_unconfirmed",  # say the point is not established by the sources (U-xx); redirect
    "abstain_and_redirect",  # decline the excluded request; point to the official source
    "partial_answer_and_redirect",  # answer the in-scope part; redirect the excluded part
]
UNRESOLVED = {
    "U-01",
    "U-02",
    "U-03",
    "U-04",
    "G-17",
    "I-01",
    "I-02",
    "I-03",
    "I-05",
    "I-08",
    "I-09",
}
SEVERITY = Literal["critical", "major"]
NEAR_DUP_JACCARD = 0.6  # token-set similarity above which two cases count as near-duplicates


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class CaseInput(_Model):
    """What a system under test sees. Nothing here reveals the label."""

    case_id: str = Field(pattern=r"^(DEV|TST)-\d{2}$")
    split: Literal["dev", "test"]
    as_of: date  # fixed evaluation date for date-dependent guidance
    situation_text: str = Field(min_length=20)  # fictional profile only
    question: str = Field(min_length=10)


class Prohibited(_Model):
    id: str
    text: str
    severity: SEVERITY
    basis: list[str] = Field(min_length=1)  # fact IDs, rule IDs or decision IDs


class Conflict(_Model):
    fields: list[str] = Field(min_length=1)
    kind: Literal["stated_contradiction", "logical_inconsistency"]
    material: bool  # does the answer to the question depend on it?


class OutOfScope(_Model):
    code: Literal["excluded_topic", "unsupported_household_type", "unrecognised_question"]
    topic: Topic | None
    redirect_source_id: str | None


class Review(_Model):
    status: Literal["candidate", "approved", "edited", "rejected"]
    requires_source_check: bool  # the developer must verify against the source before freeze
    reasons: list[str] = []
    reviewer_notes: str = ""


class CaseLabel(_Model):
    case_id: str
    category: Category
    family_id: str  # near-duplicate group; a family never spans dev and test
    reference_profile: dict[str, Any]  # expected extraction; None = not stated / conflicting
    question_topics: list[Topic] = Field(min_length=1)
    answerable: Literal["yes", "partial", "no"]
    required_rule_ids: list[str]  # must be reflected in the answer (required-rule recall)
    conditional_rule_ids: list[str] = []  # depend on missing information; raise conditionally
    optional_rule_ids: list[str] = []  # relevant but not required; never penalised
    required_missing_fields: list[str] = []  # essential follow-ups (missing-info recall)
    acceptable_follow_ups: list[str] = []  # reasonable to ask, not required
    expected_conflicts: list[Conflict] = []
    out_of_scope: list[OutOfScope] = []
    expected_behaviour: list[Behaviour] = Field(min_length=1)
    key_points: list[str] = Field(min_length=1)  # authored content the answer must convey
    prohibited_conclusions: list[Prohibited] = Field(min_length=1)
    evidence_fact_ids: list[str]
    unresolved_refs: list[str] = []  # U-/I-/G- items: no definitive label on these points
    review: Review


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return data


def load_dev() -> list[tuple[CaseInput, CaseLabel]]:
    rows = read_jsonl(DEV_PATH)
    return [
        (CaseInput.model_validate(r["input"]), CaseLabel.model_validate(r["label"])) for r in rows
    ]


def load_test_inputs() -> list[CaseInput]:
    """Held-out inputs only: allowed for schema-compatibility checks and the final run."""
    return [CaseInput.model_validate(r) for r in read_jsonl(TEST_INPUTS_PATH)]


class HeldOutLocked(PermissionError):
    """Held-out labels requested outside final scoring."""


def load_test_labels(*, final: bool = False, review: bool = False) -> list[CaseLabel]:
    """Release held-out labels only for final scoring (or the developer's label review).

    Final scoring needs final=True, BTO_BUDDY_FINAL_EVAL=1, a frozen manifest and a file whose
    SHA-256 matches the committed value, so labels cannot be changed after predictions.
    """
    manifest = load_manifest()
    committed = manifest["heldout_labels_sha256"]
    if final:
        if os.environ.get(FINAL_ENV) != "1":
            raise HeldOutLocked(f"set {FINAL_ENV}=1 for final scoring only")
        if manifest["status"] != "frozen":
            raise HeldOutLocked("benchmark is not frozen; labels are not approved yet")
    elif not review:
        raise HeldOutLocked("held-out labels are only available for final scoring")
    if not TEST_LABELS_PATH.exists():
        raise FileNotFoundError(TEST_LABELS_PATH)
    if sha256(TEST_LABELS_PATH) != committed and final:
        raise HeldOutLocked("held-out labels differ from the committed hash")
    return [CaseLabel.model_validate(r) for r in read_jsonl(TEST_LABELS_PATH)]


# ---------------------------------------------------------------- validation --------------
def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard(a: str, b: str) -> float:
    x, y = tokens(a), tokens(b)
    return len(x & y) / len(x | y) if x | y else 0.0


def near_duplicates(
    inputs: list[CaseInput], threshold: float = NEAR_DUP_JACCARD
) -> list[tuple[str, str, float]]:
    pairs = []
    for i, a in enumerate(inputs):
        for b in inputs[i + 1 :]:
            s = jaccard(a.situation_text + " " + a.question, b.situation_text + " " + b.question)
            if s >= threshold:
                pairs.append((a.case_id, b.case_id, round(s, 2)))
    return pairs


def validate_label(
    label: CaseLabel, case: CaseInput, kb: policy.KnowledgeBase, reg: policy.Registry
) -> list[str]:
    """Traceability of one label to approved rules and verified facts (REQ-EVL-020)."""
    e: list[str] = []
    cid = label.case_id
    if cid != case.case_id:
        e.append(f"{cid}: label/input mismatch")
    rule_ids = {r["rule_id"] for r in reg.rules}
    facts = {f.fact_id: f for f in kb.facts}
    for rid in label.required_rule_ids + label.conditional_rule_ids + label.optional_rule_ids:
        if rid not in rule_ids:
            e.append(f"{cid}: unknown rule {rid}")
    for fid in label.evidence_fact_ids:
        if fid not in facts:
            e.append(f"{cid}: unknown fact {fid}")
        elif facts[fid].validation.status != "verified":
            e.append(f"{cid}: fact {fid} is not verified")
    known_fields = set(reg.fields)
    for f in [
        *label.required_missing_fields,
        *label.acceptable_follow_ups,
        *[x for c in label.expected_conflicts for x in c.fields],
        *label.reference_profile,
    ]:
        if f not in known_fields:
            e.append(f"{cid}: unknown profile field {f}")
    for f in label.required_missing_fields:
        if label.reference_profile.get(f) is not None:
            e.append(f"{cid}: {f} is labelled missing but present in the reference profile")
    for c in label.expected_conflicts:
        for f in c.fields:
            if label.reference_profile.get(f) is not None:
                e.append(f"{cid}: conflicting field {f} must be None in the reference profile")
    for p in label.prohibited_conclusions:
        for b in p.basis:
            if not (b in facts or b in rule_ids or re.match(r"^(D|REQ)-", b) or b in UNRESOLVED):
                e.append(f"{cid}: prohibited conclusion {p.id} basis {b} is not traceable")
    for u in label.unresolved_refs:
        if u not in UNRESOLVED:
            e.append(f"{cid}: unknown unresolved reference {u}")
    if (
        label.unresolved_refs
        and "state_unconfirmed" not in label.expected_behaviour
        and not (
            set(label.unresolved_refs) <= {"G-17", "I-02", "I-03", "I-05", "I-08", "I-09", "I-01"}
        )
    ):
        e.append(f"{cid}: unresolved U-items need the state_unconfirmed behaviour")
    excluded = [t for t in label.question_topics if TOPIC_TIER[t].value == "excluded"]
    if excluded and not label.out_of_scope:
        e.append(f"{cid}: excluded topic without an out_of_scope label")
    if (
        label.answerable == "no"
        and "abstain_and_redirect" not in label.expected_behaviour
        and ("state_unconfirmed" not in label.expected_behaviour)
    ):
        e.append(f"{cid}: unanswerable case must abstain or state unconfirmed")
    if label.expected_conflicts and "flag_conflict" not in label.expected_behaviour:
        e.append(f"{cid}: conflicts require the flag_conflict behaviour")
    if label.required_missing_fields and "ask_follow_up" not in label.expected_behaviour:
        e.append(f"{cid}: missing fields require the ask_follow_up behaviour")
    return e


def engine_crosscheck(
    label: CaseLabel, case: CaseInput, reg: policy.Registry
) -> dict[str, list[str]]:
    """Compare the authored label with the deterministic rules (annotation QA only).

    Disagreements are reported for human review and never used to rewrite labels.
    """
    profile = {
        k: (date.fromisoformat(v) if k == "hfe_issue_date" and v else v)
        for k, v in label.reference_profile.items()
    }
    results = policy.evaluate_rules(
        reg, profile, case.as_of, topics={t.value for t in label.question_topics}
    )
    applies = {r.rule_id for r in results if r.status == "applies"}
    cannot = {r.rule_id for r in results if r.status == "cannot_determine"}
    labelled_applies = set(label.required_rule_ids) | set(label.optional_rule_ids)
    return {
        "label_required_but_engine_not_applies": sorted(set(label.required_rule_ids) - applies),
        "engine_applies_but_unlabelled": sorted(applies - labelled_applies),
        "label_conditional_but_engine_determined": sorted(set(label.conditional_rule_ids) - cannot),
    }


def engine_undetermined_unlabelled(
    label: CaseLabel, case: CaseInput, reg: policy.Registry
) -> list[str]:
    """Rules the engine cannot determine that the label does not list anywhere.

    Report-only warning for manual triage: many are legitimately omitted because the question
    does not need them (e.g. a missing property field on an HFE-timing question), so they are
    never errors. Added after DEV-13's missing conditional R-HH-001 slipped through.
    """
    profile = {
        k: (date.fromisoformat(v) if k == "hfe_issue_date" and v else v)
        for k, v in label.reference_profile.items()
    }
    results = policy.evaluate_rules(
        reg, profile, case.as_of, topics={t.value for t in label.question_topics}
    )
    labelled = {
        *label.required_rule_ids,
        *label.conditional_rule_ids,
        *label.optional_rule_ids,
    }
    return sorted({r.rule_id for r in results if r.status == "cannot_determine"} - labelled)


def validate(include_heldout: bool = False) -> dict[str, Any]:
    kb = policy.load_kb()
    reg = policy.load_rules()
    manifest = load_manifest()
    dev = load_dev()
    test_inputs = load_test_inputs()
    errors: list[str] = []
    for case, label in dev:
        errors += validate_label(label, case, kb, reg)
    if any(c.split != "dev" for c, _ in dev) or any(c.split != "test" for c in test_inputs):
        errors.append("a case is in the wrong split file")
    ids = [c.case_id for c, _ in dev] + [c.case_id for c in test_inputs]
    if len(ids) != len(set(ids)):
        errors.append("duplicate case IDs")
    fam = manifest["families"]
    dev_fams = {fam[c.case_id] for c, _ in dev}
    test_fams = {fam[c.case_id] for c in test_inputs}
    if dev_fams & test_fams:
        errors.append(f"families span both splits: {sorted(dev_fams & test_fams)}")
    for c, lab in dev:
        if fam[c.case_id] != lab.family_id:
            errors.append(f"{c.case_id}: family differs from the manifest")
    cross = near_duplicates([c for c, _ in dev] + test_inputs)
    leaks = [(a, b, s) for a, b, s in cross if a[:3] != b[:3]]
    out: dict[str, Any] = {
        "dev_cases": len(dev),
        "test_inputs": len(test_inputs),
        "cross_split_near_duplicates": leaks,
        "errors": errors,
    }
    crosscheck = {c.case_id: engine_crosscheck(lab, c, reg) for c, lab in dev}
    undetermined = {c.case_id: engine_undetermined_unlabelled(lab, c, reg) for c, lab in dev}
    if include_heldout:
        labels = load_test_labels(review=True)
        by_id = {c.case_id: c for c in test_inputs}
        for lab in labels:
            errors += validate_label(lab, by_id[lab.case_id], kb, reg)
            if fam[lab.case_id] != lab.family_id:
                errors.append(f"{lab.case_id}: family differs from the manifest")
            crosscheck[lab.case_id] = engine_crosscheck(lab, by_id[lab.case_id], reg)
            undetermined[lab.case_id] = engine_undetermined_unlabelled(lab, by_id[lab.case_id], reg)
        if sha256(TEST_LABELS_PATH) != manifest["heldout_labels_sha256"]:
            errors.append("held-out labels differ from the committed hash")
    out["engine_disagreements"] = {k: v for k, v in crosscheck.items() if any(v.values())}
    out["warnings_undetermined_unlabelled"] = {k: v for k, v in undetermined.items() if v}
    return out


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] != "validate":
        sys.exit(__doc__)
    report = validate(include_heldout="--heldout" in sys.argv)
    # IDs and counts only: no label content is printed (held-out labels stay unread).
    print(
        f"dev={report['dev_cases']} test_inputs={report['test_inputs']} "
        f"errors={len(report['errors'])} cross_split_near_dups="
        f"{len(report['cross_split_near_duplicates'])} "
        f"engine_disagreements={sorted(report['engine_disagreements'])}"
    )
    for e in report["errors"]:
        print("  ERROR", e)
    # Rule IDs only (registry content, not label content); report-only, never fails the run.
    for cid, rules in sorted(report["warnings_undetermined_unlabelled"].items()):
        print("  WARN undetermined-but-unlabelled", cid, ", ".join(rules))
    if report["errors"] or report["cross_split_near_duplicates"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
