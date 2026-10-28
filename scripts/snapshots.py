"""Offline tooling for the manually captured HDB sources (docs/data_sources.md §7).

  audit     completeness audit of data/private_corpus/raw/<source_id>/ snapshots: headings,
            accordion labels, expected-concept presence, embedded page-data coverage, PDF
            page/date/text-layer facts and hashes
  register  write retrieved_at, hashes, size and private path into data/sources_manifest.json

Both print **structure only**, never passages of source text. Under D-054, source text must
not reach an external LLM, so this output is safe to share with the coding agent.
Stdlib only (D-036). Not used by the app or Docker (REQ-DAT-022).

Usage: python -I scripts/snapshots.py {audit|register}
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "private_corpus" / "raw"
MANIFEST = ROOT / "data" / "sources_manifest.json"
STAMP = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{6}Z)_")  # UTC capture-time filename prefix
RIGHTS_FILES = {"hdb_terms_of_use": "R-HDB-WWW"}  # raw/rights/<UTC>_<suffix>.html -> record

SKIP_TAGS = {"script", "style", "noscript", "svg", "template"}
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
LABEL_MAX = 70  # truncate labels so no passage-length text is ever printed

# Expected MVP concepts per source (plan §2, §5). Regexes over lower-cased page text. A hit
# shows the concept is present in the capture; it does not verify any policy content.
EXPECTED: dict[str, dict[str, str]] = {
    "S01": {
        "fiance_section": r"fianc[ée] and fianc[ée]e",
        "married_couples_section": r"married couples?",
        "non_resident_section": r"families with non-residents?|non-resident spouse",
        "ft_pmc": r"first-timer \(parents ?& ?married couples\)|ft\(pmc\)",
        "fpps": r"family and parenthood priority scheme|\bfpps\b",
        "under_21_note": r"below 21|under 21|younger than 21",
        "core_occupier": r"core occupier",
        "application_validity_note": (
            r"no changes? to the persons|changes? to the (persons|applicants|household)"
        ),
        "first_timer_term": r"first-timer|first timer",
        "private_property": r"private property|private residential property",
        "citizenship_sc_spr": r"singapore permanent resident|\bspr\b",
        "citizen_top_up_link": r"citizen top-up",
        "income_ceiling_present_excluded": r"income ceiling",
    },
    "S02": {
        "what_is_hfe": r"what is the hdb flat eligibility|what is the hfe",
        "when_to_apply": r"when to apply",
        "how_to_apply": r"how to apply",
        "validity_review": r"validity",
        "next_steps": r"next steps",
        "income_guidelines_section": r"income guidelines",
        "validity_9_months": r"\b9 months\b|nine months",
        "step_window_30_days": r"30 (calendar )?days",
        "processing_time": r"\b1 month\b|one month|processing time|working days",
        "preliminary_hfe": r"preliminary",
        "singpass": r"singpass",
        "ipa": r"in-principle approval|\bipa\b",
        "private_property_declaration": r"private property",
        "review_of_letter": r"review",
    },
    "S03": {
        "supporting_documents": r"supporting documents?",
        "assessment_period": r"assessment period|12 months|preceding",
        "employed": r"\bemployed\b",
        "self_employed": r"self-employed",
        "not_working": r"not working|unemployed",
        "payslip_or_cpf": r"payslip|cpf contribution|cpf statement",
        "employment_status_guide_link": r"employment status guide",
        "income_declaration_guide_link": r"income declaration guide",
    },
    "S04": {
        "cancellation_section": r"cancel",
        "non_selection": r"non-selection|not (to )?select|do not book|did not book|not book a flat",
        "waiver": r"waive",
        "exception": r"exception",
        "first_timer_term": r"first-timer|first timer",
        "valid_hfe_required": r"hfe letter",
        "sales_launch": r"sales launch|sales exercise",
        "ballot": r"ballot",
        "application_fee": r"application fee|administrative fee|\$10\b",
        "priority_schemes_link": r"priority scheme",
    },
    "S05": {
        "ft_pmc": r"first-timer \(parents ?& ?married couples\)|ft\(pmc\)",
        "fpps": r"family and parenthood priority scheme|\bfpps\b",
        "fcs_proximity": r"family care scheme (\(fcs\) )?\(proximity\)",
        "fcs_joint_balloting": r"family care scheme (\(fcs\) )?\(joint balloting\)",
        "first_timer_term": r"first-timer|first timer",
        "flat_supply_share": r"% of|per ?cent|quota|allocat",
        "tcps_outside": r"third child priority scheme",
        "sps_outside": r"senior priority scheme",
        "tps_outside": r"tenants['\u2019]? priority scheme",
    },
}
LINK_PATTERNS = {
    "file.go.gov.sg PDFs": r"file\.go\.gov\.sg",
    "mynicehome guide": r"mynicehome",
    "youtube": r"youtu\.?be",
    "hfe get-help (robots-disallowed)": r"hdb-flat-portal/hfe/get-help",
    "income-guidelines page": r"income-guidelines-and-documents",
    "priority-schemes page": r"priority-schemes",
    "citizen-topup": r"citizen-topup",
}
UPDATED_RE = re.compile(r"(last updated|updated on|last reviewed)[^0-9a-z]{0,5}([0-9a-z ,]{4,25})")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip().lower()


class Snapshot(HTMLParser):
    """Collects visible-DOM text, headings, toggles, links, images and __NEXT_DATA__."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.headings: list[tuple[str, str]] = []
        self.toggles: list[tuple[str, str]] = []
        self.links: list[str] = []
        self.images: list[tuple[str, str]] = []
        self.next_data = ""
        self.title = ""
        self._skip = 0
        self._in_next = False
        self._in_title = False
        self._label_stack: list[tuple[str, str, list[str]]] = []  # (kind, tag, parts)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: v or "" for k, v in attrs}
        if tag == "script" and a.get("id") == "__NEXT_DATA__":
            self._in_next = True
        if tag in SKIP_TAGS:
            self._skip += 1
            return
        if tag == "title":
            self._in_title = True
        if tag in HEADING_TAGS:
            self._label_stack.append(("h", tag, []))
        elif "aria-expanded" in a:
            self._label_stack.append(("t", tag, [a.get("aria-expanded", "")]))
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.images.append((a.get("src", ""), a.get("alt", "")))

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._in_next = False
        if tag in SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
            return
        if tag == "title":
            self._in_title = False
        if self._label_stack and self._label_stack[-1][1] == tag:
            kind, t, parts = self._label_stack.pop()
            if kind == "h":
                self.headings.append((t, norm(" ".join(parts))))
            else:
                self.toggles.append((parts[0], norm(" ".join(parts[1:]))))

    def handle_data(self, data: str) -> None:
        if self._in_next:
            self.next_data += data
            return
        if self._skip:
            return
        if self._in_title:
            self.title += data
        self.text.append(data)
        for _, _, parts in self._label_stack:
            parts.append(data)


class _Strip(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def strip_html(s: str) -> str:
    p = _Strip()
    p.feed(s)
    return " ".join(p.parts)


def json_strings(node: object, path: str = "$") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for k, v in node.items():
            out += json_strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += json_strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        out.append((path, node))
    return out


def next_data_coverage(raw: str, dom: str) -> tuple[int, int, list[tuple[str, int]]]:
    """Share of content sentences in __NEXT_DATA__ that also appear in the DOM text.

    A sentence missing from the DOM means content that exists in page data but was not
    rendered at capture (e.g. unmounted panels). Returns (total, found, missing paths)."""
    if not raw.strip():
        return 0, 0, []
    total = found = 0
    missing: dict[str, int] = {}
    for path, s in json_strings(json.loads(raw)):
        if len(s) < 40 or s.startswith(("http", "/", "{")):
            continue
        txt = norm(strip_html(s) if "<" in s else s)
        for sent in re.split(r"(?<=[.!?:;])\s+", txt):
            if len(sent) < 30:
                continue
            total += 1
            if sent in dom:
                found += 1
            else:
                missing[path] = missing.get(path, 0) + 1
    return total, found, sorted(missing.items(), key=lambda x: -x[1])


def short(s: str) -> str:
    return s if len(s) <= LABEL_MAX else s[: LABEL_MAX - 1] + "…"


def audit(path: Path, source_id: str) -> None:
    data = path.read_bytes()
    snap = Snapshot()
    snap.feed(data.decode("utf-8", errors="replace"))
    dom = norm(" ".join(snap.text))
    print(f"\n=== {source_id}: {path.name}")
    print(f"bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}")
    print(f"text_sha256={hashlib.sha256(dom.encode()).hexdigest()} dom_text_chars={len(dom)}")
    print(f"title: {short(norm(snap.title))}")
    m = UPDATED_RE.search(dom)
    print(f"last-updated marker: {m.group(0) if m else 'none found'}")

    print(f"headings ({len(snap.headings)}):")
    for tag, h in snap.headings:
        if h:
            print(f"  {tag}: {short(h)}")
    print(f"toggles with aria-expanded ({len(snap.toggles)}):")
    for state, label in snap.toggles:
        print(f"  [{state}] {short(label) or '(no text label)'}")

    print("expected concepts:")
    hits = 0
    for name, rx in EXPECTED.get(source_id, {}).items():
        n = len(re.findall(rx, dom))
        hits += n > 0
        print(f"  {'OK ' if n else 'MISSING'} {name} (matches={n})")
    print(f"  -> {hits}/{len(EXPECTED.get(source_id, {}))} present")

    print("links of interest:")
    for name, rx in LINK_PATTERNS.items():
        n = sum(bool(re.search(rx, h)) for h in snap.links)
        if n:
            print(f"  {name}: {n}")
    content_imgs = [
        (s, a) for s, a in snap.images if "/-/media/" in s or "infographic" in s.lower()
    ]
    print(f"content images ({len(content_imgs)}):")
    for src, alt in content_imgs:
        print(f"  {short(src.split('?')[0].rsplit('/', 1)[-1])} | alt_chars={len(alt)}")

    total, found, missing = next_data_coverage(snap.next_data, dom)
    print(f"__NEXT_DATA__ sentences rendered in DOM: {found}/{total}")
    for p, n in missing[:15]:
        print(f"  not in DOM: {n} sentence(s) at {short(p)}")


def audit_pdf(path: Path, source_id: str) -> None:
    """Byte-level PDF facts only: no parser dependency (D-052) and no text output (D-054).

    Counts and Info-dictionary dates are read with regexes over the raw bytes. They are
    indicative: compressed object streams can hide them, in which case 'not found' is shown.
    """
    data = path.read_bytes()
    print(f"\n=== {source_id}: {path.name}")
    print(f"bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}")
    print(f"pdf header: {data[:8].decode('latin-1', 'replace')!r}")
    pages = len(re.findall(rb"/Type\s*/Page(?!s)", data))
    print(f"page objects (indicative): {pages or 'not found (object streams)'}")
    for key in (b"CreationDate", b"ModDate"):
        m = re.search(rb"/" + key + rb"\s*\(D:(\d{8,14})", data)
        print(f"{key.decode()}: {m.group(1).decode() if m else 'not found'}")
    print(f"font resources present (text layer likely): {bool(re.search(rb'/Font', data))}")


def run_audit() -> None:
    for sid in sorted(EXPECTED):
        for f in sorted((RAW / sid).glob("*.html")):
            audit(f, sid)
    for f in sorted(RAW.glob("S*/*.pdf")):
        audit_pdf(f, f.parent.name)


def run_register() -> None:
    """Fill acquisition provenance in the manifest from the newest stamped capture per source.

    retrieved_at comes from the UTC filename prefix (the file's creation time at save).
    text_sha256 hashes the normalised DOM text, so a later re-capture can tell real content
    drift from page noise without storing text (REQ-LIC-016). Only metadata is written.
    """
    manifest = json.loads(MANIFEST.read_text())
    by_id = {s["source_id"]: s for s in manifest["sources"]}
    for folder in sorted(p for p in RAW.glob("S*") if p.is_dir()):
        files = sorted(f for f in folder.iterdir() if STAMP.match(f.name))
        if not files or folder.name not in by_id:
            print(f"skip {folder.name}: no stamped file or no manifest entry")
            continue
        f = files[-1]
        data = f.read_bytes()
        stamp = STAMP.match(f.name).group(1)  # type: ignore[union-attr]
        retrieved = datetime.strptime(stamp, "%Y-%m-%dT%H%M%SZ").replace(tzinfo=UTC)
        text_sha = None
        if f.suffix == ".html":
            snap = Snapshot()
            snap.feed(data.decode("utf-8", errors="replace"))
            text_sha = hashlib.sha256(norm(" ".join(snap.text)).encode()).hexdigest()
        acq = by_id[folder.name]["acquisition"]
        acq.update(
            {
                "retrieved_at": retrieved.isoformat().replace("+00:00", "Z"),
                "retrieved_at_basis": "file creation time at save (UTC filename prefix)",
                "raw_sha256": hashlib.sha256(data).hexdigest(),
                "text_sha256": text_sha,
                "byte_size": len(data),
                "private_path": str(f.relative_to(ROOT)),
            }
        )
        print(f"{folder.name}: {acq['retrieved_at']} sha256={acq['raw_sha256'][:12]} ({f.name})")
    # Terms-of-use copies in raw/rights/ update their host's rights record (hash + check time).
    rights = {r["rights_id"]: r for r in manifest["rights_records"]}
    for suffix, rights_id in RIGHTS_FILES.items():
        files = sorted(f for f in (RAW / "rights").glob(f"*_{suffix}.html") if STAMP.match(f.name))
        if not files or rights_id not in rights:
            continue
        f = files[-1]
        stamp = STAMP.match(f.name).group(1)  # type: ignore[union-attr]
        checked = datetime.strptime(stamp, "%Y-%m-%dT%H%M%SZ").replace(tzinfo=UTC)
        rights[rights_id]["terms_checked_at"] = checked.isoformat().replace("+00:00", "Z")
        rights[rights_id]["terms_sha256"] = hashlib.sha256(f.read_bytes()).hexdigest()
        rights[rights_id]["terms_private_path"] = str(f.relative_to(ROOT))
        print(f"{rights_id}: terms {rights[rights_id]['terms_checked_at']} ({f.name})")
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    # Without snapshots, `register` would rewrite the tracked manifest's hashes from nothing.
    if command in ("audit", "register") and not any(RAW.glob("*/*")):
        sys.exit(
            f"no source snapshots in {RAW.relative_to(ROOT)}: the private corpus is not "
            "redistributed (docs/data_sources.md §7). Nothing was changed."
        )
    if command == "audit":
        run_audit()
    elif command == "register":
        run_register()
    else:
        sys.exit("usage: python -I scripts/snapshots.py {audit|register}")


if __name__ == "__main__":
    main()
