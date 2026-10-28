"""Offline corpus tooling (scripts/corpus.py) on independently authored HTML fixtures.

The fixture mimics the captured page layout (content column, accordions, nested tables,
same-page anchors) with invented text, so no HDB content is needed to run the tests.
"""

import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))  # stdlib-only tooling
import corpus

PAGE = """<html><body><main>
<nav class="PSidebar"><a href="/elsewhere">Sidebar link</a></nav>
<h1>Widget Permits</h1>
<div class="DestinationLayout_DestinationPageLayout__Cont__x">
 <div class="BodyContent_BodyContent__a"><h2>Overview</h2>
  <p>Permits are issued to <a href="/widgets/apply">applicants</a> who register first.</p>
  <img src="/-/media/widgets/overview.png" alt="Overview chart"></div>
 <div class="PAccordion">
  <div class="accordion-item">
   <div class="accordion-header"><button class="accordion-button collapsed" aria-expanded="false">
    <div class="PAccordion__header-text"><div class="h5" role="heading">Blue widgets</div>
    <div class="PAccordion__header-description"><p>Rules for blue widgets.</p></div></div>
   </button></div>
   <div class="accordion-collapse"><div class="accordion-body"><div>
    <a id="blue"></a>
    <h2>Conditions</h2>
    <table><thead><tr><th>Criterion</th><th>Owners</th><th>Renters</th></tr></thead>
     <tbody><tr><td>Age</td><td colspan="2">At least 30</td></tr>
     <tr><td>Storage</td><td>Indoor only<table><tr><th>Room</th><th>Limit</th></tr>
       <tr><td>Garage</td><td>Two units</td></tr></table></td><td>None</td></tr></tbody></table>
    <p class="Footnote">[1] Footnote applies to renters only.</p>
    <h2>Exceptions</h2>
    <ul><li>Holders under 30 may be listed as helpers.<ul><li>Helpers cannot sign.</li></ul></li>
     <li>Joint holders count as one.</li></ul>
    <p>See <a href="#blue">blue rules</a> or <a href="https://example.org/x.pdf">the guide</a>.</p>
   </div></div></div>
  </div>
  <div class="accordion-item">
   <div class="accordion-header"><button class="accordion-button collapsed" aria-expanded="false">
    <div class="PAccordion__header-text"><div class="h5" role="heading">Red widgets</div></div>
   </button></div>
   <div class="accordion-collapse"><div class="accordion-body"><div>
    <h2>Conditions</h2><p>Red widgets need the same storage as blue widgets do today.</p>
    <h2>Videos</h2><iframe src="https://www.youtube.com/embed/abc?si=x"></iframe>
   </div></div></div>
  </div>
 </div>
 <div class="Cards_Cards__Card"><a href="/other">Card link text</a></div>
</div>
<footer class="PFooterV">Footer text</footer>
</main></body></html>"""

SOURCE = {
    "source_id": "S99",
    "title": "Widget Permits",
    "canonical_url": "https://www.example.gov.sg/widgets",
    "page_last_updated": "2026-01-01",
    "effective_date": None,
    "acquisition": {"retrieved_at": "2026-10-28T00:00:00Z", "raw_sha256": "x", "private_path": "p"},
}


@pytest.fixture(scope="module")
def record() -> dict:
    return corpus.build_record(SOURCE, PAGE)


def _section(record: dict, title: str, parent: str | None = None) -> dict:
    hits = [
        s
        for s in record["sections"]
        if s["title"] == title and (parent is None or s["parent"] == parent)
    ]
    assert len(hits) == 1, (title, hits)
    return hits[0]


def test_accordions_become_lettered_sections_with_nested_headings(record: dict) -> None:
    blue = _section(record, "Blue widgets")
    red = _section(record, "Red widgets")
    assert (blue["section_id"], red["section_id"]) == ("S99.a", "S99.b")
    # The same sub-heading under two accordions stays attached to its own parent, so a
    # condition is never attributed to the wrong group (REQ-SRC-003).
    blue_cond = _section(record, "Conditions", "S99.a")
    red_cond = _section(record, "Conditions", "S99.b")
    assert blue_cond["path"] == ["Widget Permits", "Blue widgets", "Conditions"]
    assert red_cond["section_id"] != blue_cond["section_id"]
    assert "blue" in blue["anchors"]


def test_site_chrome_is_excluded(record: dict) -> None:
    text = " ".join(b["text"] for b in record["blocks"])
    assert "Sidebar link" not in text
    assert "Card link text" not in text
    assert "Footer text" not in text


def test_tables_keep_structure_spans_and_nesting(record: dict) -> None:
    tables = [b for b in record["blocks"] if b["kind"] == "table"]
    outer, inner = tables
    assert outer["header_rows"] == 1
    assert outer["rows"][1] == ["Age", "At least 30"]
    assert outer["spans"][1][1] == [2, 1]  # merged cell recorded for manual checking
    assert "[nested table]" in outer["rows"][2][1]
    assert "Two units" not in outer["text"]  # nested rows are not duplicated in the parent
    assert inner["nested_in"] == outer["block_id"]
    assert inner["rows"] == [["Room", "Limit"], ["Garage", "Two units"]]


def test_lists_keep_depth_and_footnotes_stay_with_their_section(record: dict) -> None:
    lst = next(b for b in record["blocks"] if b["kind"] == "list")
    assert [(i["depth"], i["text"]) for i in lst["items"]] == [
        (0, "Holders under 30 may be listed as helpers."),
        (1, "Helpers cannot sign."),
        (0, "Joint holders count as one."),
    ]
    foot = next(b for b in record["blocks"] if b["kind"] == "footnote")
    assert foot["section_id"] == _section(record, "Conditions", "S99.a")["section_id"]


def test_links_are_classified_and_media_recorded(record: dict) -> None:
    links = {link["href"]: link["kind"] for b in record["blocks"] for link in b.get("links", [])}
    assert links["#blue"] == "same_page"
    assert links["/widgets/apply"] == "internal"
    assert links["https://example.org/x.pdf"] == "pdf"
    media = [b for b in record["blocks"] if b["kind"] == "media"]
    assert {m["text"] for m in media} == {"image", "video"}


def test_passages_are_per_section_with_provenance(record: dict) -> None:
    ids = [p["passage_id"] for p in record["passages"]]
    assert len(ids) == len(set(ids))
    p = next(p for p in record["passages"] if p["section_id"] == "S99.a.1")
    assert p["source_url"] == "https://www.example.gov.sg/widgets?anchor=blue"  # inherited
    assert p["retrieved_at"] == "2026-10-28T00:00:00Z"
    assert p["text_sha256"] == hashlib.sha256(corpus.norm(p["text"]).encode()).hexdigest()
    assert "table" in p["block_kinds"] and "footnote" in p["block_kinds"]


def _validate(record: dict, spec: list[dict]) -> dict:
    summary, _ = corpus.validate_source(
        record, PAGE, spec, {"S99": SOURCE | {"mvp_class": "essential"}}, 1
    )
    return summary


SPEC = [
    {"label": "Overview", "match": "^overview$", "scope": "authored"},
    {"label": "Blue", "match": "^blue widgets", "scope": "authored"},
    {"label": "Red", "match": "^red widgets", "scope": "authored"},
]


def test_validation_reports_counts_spans_and_single_snapshot_limitation(record: dict) -> None:
    s = _validate(record, SPEC)
    assert s["counts"]["accordions_extracted"] == s["counts"]["accordion_toggles_raw"] == 2
    assert s["counts"]["tables"] == s["counts"]["raw_tables"] == 2
    kinds = {i["kind"] for i in s["issues"]}
    assert {"manual_check", "limitation", "temporal_gap"} <= kinds
    assert "missing_section" not in kinds and "unexpected_section" not in kinds


def test_validation_flags_missing_and_unexpected_sections(record: dict) -> None:
    spec = [*SPEC[:2], {"label": "Green", "match": "^green widgets$", "scope": "authored"}]
    issues = _validate(record, spec)["issues"]
    assert any(i["kind"] == "missing_section" and "Green" in i["detail"] for i in issues)
    assert any(i["kind"] == "unexpected_section" for i in issues)  # red widgets


def test_validation_detects_duplicate_blocks() -> None:
    para = "<p>This identical paragraph is repeated under two different headings here.</p>"
    page = PAGE.replace("<h2>Exceptions</h2>", f"{para}<h2>Exceptions</h2>").replace(
        "<h2>Videos</h2>", f"{para}<h2>Videos</h2>"
    )
    rec = corpus.build_record(SOURCE, page)
    s, _ = corpus.validate_source(rec, page, SPEC, {}, 1)
    assert any(len(group) == 2 for group in s["duplicates"]["blocks"])


def test_overlap_check_finds_longest_shared_run() -> None:
    a = corpus.words("Holders under thirty may only be helpers in the application")
    b = corpus.words("Rules say holders under thirty may only be helpers in the application form")
    n, run = corpus.longest_shared_run(a, b)
    assert n == 10 and run.startswith("holders under thirty")
    assert corpus.longest_shared_run(corpus.words("entirely new wording"), b)[0] == 0


def _fact(**over: object) -> dict:
    base = {
        "fact_id": "HH-TEST-001",
        "statement": "Authored statement about widgets.",
        "topic": "household_composition",
        "scope_tier": "core",
        "applies_to": {},
        "exceptions": [],
        "critical": False,
        "kb_version": "kb-test",
        "retrieved_at": "2026-10-28",
        "validation": {"status": "snapshot_checked"},
        "rights_review": {"status": "pending"},
        "private_passage_ids": ["S99.a.1.p1"],
        "source": {
            "source_id": "S99",
            "section_id": "S99.a.1",
            "url": "https://www.example.gov.sg/widgets?anchor=blue",
        },
    }
    base.update(over)
    return base


def test_fact_integrity_resolves_sources_sections_and_passages(record: dict) -> None:
    sources = {"S99": SOURCE | {"mvp_class": "essential", "content_format": ["html_text"]}}
    rows, errors = corpus.check_facts([_fact()], sources, {"S99": record})
    assert errors == [] and rows[0]["max_shared_run_words"] < corpus.OVERLAP_WORDS

    bad = [
        _fact(
            fact_id="HH-TEST-002",
            source={
                "source_id": "S99",
                "section_id": "S99.z",
                "url": "https://www.example.gov.sg/widgets",
            },
        ),
        _fact(
            fact_id="HH-TEST-003",
            source={"source_id": "S98", "section_id": "S98.a", "url": "https://x"},
        ),
        _fact(
            fact_id="HH-TEST-004",
            private_passage_ids=["S99.q.p1"],
            exceptions=[{"description": "d", "fact_id": "NOPE-001"}],
        ),
        _fact(fact_id="HH-TEST-004"),
    ]
    _, errors = corpus.check_facts(bad, sources, {"S99": record})
    joined = " | ".join(errors)
    assert "section_id S99.z not in L1" in joined
    assert "S98 not in manifest" in joined
    assert "passage S99.q.p1 not in L1" in joined
    assert "unknown fact NOPE-001" in joined
    assert "duplicate fact_id HH-TEST-004" in joined


def test_copied_wording_is_flagged(record: dict) -> None:
    copied = _fact(statement="Holders under 30 may be listed as helpers. Helpers cannot sign.")
    sources = {"S99": SOURCE | {"mvp_class": "essential", "content_format": ["html_text"]}}
    rows, _ = corpus.check_facts([copied], sources, {"S99": record})
    assert rows[0]["overlap_flag"] is True


@pytest.mark.parametrize("cmd", ["extract", "validate", "facts", "verify", "freeze"])
def test_corpus_commands_refuse_without_snapshots(
    cmd: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A clean clone has no private corpus; the commands must not rewrite tracked outputs.
    import snapshots

    for module in (corpus, snapshots):
        monkeypatch.setattr(module, "RAW", tmp_path / "data" / "private_corpus" / "raw")
        monkeypatch.setattr(module, "ROOT", tmp_path)
    for module, command in ((corpus, cmd), (snapshots, "register"), (snapshots, "audit")):
        monkeypatch.setattr(sys, "argv", ["x", command])
        with pytest.raises(SystemExit, match="no source snapshots"):
            module.main()
