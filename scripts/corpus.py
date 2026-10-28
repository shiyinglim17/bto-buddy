"""Offline corpus processing for the manually captured HDB snapshots (docs/data_sources.md §12).

  extract   L0 raw HTML -> L1 structured sections, blocks and passages under
            data/private_corpus/processed/<source_id>.json (private, Git-ignored)
  validate  extraction-completeness checks -> data/corpus/extraction_report.json (tracked,
            counts and IDs only) plus a private detail file
  facts     integrity of data/policy_facts.jsonl against the manifest, and the local overlap
            check (8+ consecutive shared words with L1) for the rights review (D-054)
  freeze    write data/corpus/corpus_version.json (hashes, counts, versions)

snapshots.py owns capture registration and the raw structural audit; this script owns
everything downstream of the raw files. Stdlib only (D-036). Never imported by src/ or used
by Docker (REQ-DAT-022). Terminal output is counts, IDs and short labels, never passages.

Usage: python -I scripts/corpus.py {extract|validate|facts|verify|freeze}
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # sibling import under python -I
from snapshots import (
    MANIFEST,
    RAW,
    ROOT,
    STAMP,
    Snapshot,
    json_strings,
    norm,
    short,
)

EXTRACTOR_VERSION = "1.0.0"
PROCESSED = ROOT / "data" / "private_corpus" / "processed"
CORPUS_META = ROOT / "data" / "corpus"
FACTS = ROOT / "data" / "policy_facts.jsonl"
VISUALS = ROOT / "data" / "visual_resources.json"
COVERAGE = ROOT / "data" / "source_coverage.csv"
RULES = ROOT / "data" / "policy_rules.yaml"
OVERLAP_WORDS = 8  # D-054: runs of this many shared words are flagged for rewording

VOID = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}
SKIP = {
    "script",
    "style",
    "noscript",
    "svg",
    "template",
    "button",
    "form",
    "nav",
    "header",
    "footer",
    "iframe",
    "select",
}
INLINE = {
    "a",
    "span",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "sup",
    "sub",
    "small",
    "br",
    "abbr",
    "mark",
    "label",
    "time",
    "img",
}
HEADINGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
# Site chrome inside the content column: link cards to other pages and hidden menus. Their
# links are kept as relationships, but they are not page content (data_sources §2.2, S02.h).
CHROME_CLASSES = ("PSidebar", "Cards_Cards", "PCard", "breadcrumb", "d-none", "PFooter")


# ---------------------------------------------------------------- minimal DOM -------------
@dataclass
class Node:
    tag: str
    attrs: dict[str, str]
    children: list[Node | str] = field(default_factory=list)

    @property
    def cls(self) -> str:
        return self.attrs.get("class", "")

    def text(self) -> str:
        out: list[str] = []
        for c in self.children:
            if isinstance(c, str):
                out.append(c)
            elif c.tag not in SKIP - {"button"}:
                out.append(c.text())
                if c.tag not in INLINE or c.tag == "br":
                    out.append(" ")  # block boundaries separate words (e.g. th|td cells)
        return " ".join("".join(out).split())

    def find_all(self, pred: object) -> list[Node]:
        found: list[Node] = []
        for c in self.children:
            if isinstance(c, Node):
                if pred(c):  # type: ignore[operator]
                    found.append(c)
                found += c.find_all(pred)
        return found


class TreeBuilder(HTMLParser):
    """Tolerant tree builder: void tags never nest, unmatched end tags are ignored."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {})
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {k: v or "" for k, v in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.stack[-1].children.append(Node(tag, {k: v or "" for k, v in attrs}))

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID or all(n.tag != tag for n in self.stack[1:]):
            return
        while self.stack[-1].tag != tag:
            self.stack.pop()
        self.stack.pop()

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data.replace("\xa0", " "))


def parse(html: str) -> Node:
    b = TreeBuilder()
    b.feed(html)
    return b.root


# ---------------------------------------------------------------- block extraction --------
@dataclass
class Link:
    href: str
    text: str
    kind: str  # same_page | internal | external | pdf | mailto | tel


@dataclass
class Block:
    kind: str  # heading | paragraph | list | table | footnote | accordion_summary
    text: str
    level: int = 0
    items: list[dict[str, object]] = field(default_factory=list)  # list items with depth
    rows: list[list[str]] = field(default_factory=list)  # table cells, row-major
    header_rows: int = 0
    nested_in: str | None = None  # parent table block id for nested tables
    spans: list[list[list[int]]] = field(default_factory=list)  # [colspan, rowspan] per cell
    anchors: list[str] = field(default_factory=list)  # same-page ids defined here
    links: list[Link] = field(default_factory=list)
    accordion: bool = False
    block_id: str = ""


def link_kind(href: str) -> str:
    h = href.strip().lower()
    if h.startswith("#") or ("?anchor=" in h and not h.startswith("http")):
        return "same_page"
    if h.startswith("mailto:"):
        return "mailto"
    if h.startswith("tel:"):
        return "tel"
    if ".pdf" in h or "file.go.gov.sg" in h or "go.gov.sg/" in h:
        return "pdf"
    if h.startswith("/") or "hdb.gov.sg" in h:
        return "internal"
    return "external"


def collect_links(n: Node) -> list[Link]:
    return [
        Link(a.attrs["href"], a.text(), link_kind(a.attrs["href"]))
        for a in ([n] if n.tag == "a" else []) + n.find_all(lambda x: x.tag == "a")
        if a.attrs.get("href")
    ]


def collect_anchors(n: Node) -> list[str]:
    nodes = [n, *n.find_all(lambda x: bool(x.attrs.get("id")))]
    return list(dict.fromkeys(x.attrs["id"] for x in nodes if x.attrs.get("id") and x.tag == "a"))


def is_chrome(n: Node) -> bool:
    return any(c in n.cls for c in CHROME_CLASSES) or n.tag in SKIP


class Walker:
    """Turns a content subtree into an ordered list of blocks, keeping heading levels."""

    def __init__(self) -> None:
        self.blocks: list[Block] = []
        self._inline: list[Node | str] = []

    def flush(self) -> None:
        if not self._inline:
            return
        holder = Node("p", {}, list(self._inline))
        self._inline = []
        txt = holder.text()
        if txt:
            self.blocks.append(
                Block(
                    "paragraph", txt, links=collect_links(holder), anchors=collect_anchors(holder)
                )
            )

    def walk(self, n: Node) -> None:
        for c in n.children:
            if isinstance(c, str):
                if c.strip():
                    self._inline.append(c)
                continue
            if c.tag == "iframe" or (c.tag == "img" and "/-/media/" in c.attrs.get("src", "")):
                # Videos and infographics: recorded so media-only sections are explainable,
                # never treated as text evidence (REQ-SRC-010, REQ-SRC-011).
                self.flush()
                src = c.attrs.get("src", "")
                kind = "video" if c.tag == "iframe" else "image"
                self.blocks.append(
                    Block("media", kind, links=[Link(src, c.attrs.get("alt", ""), kind)])
                )
                continue
            if is_chrome(c):
                continue
            if c.tag in INLINE:
                # An anchor with an id and no text marks a same-page target, e.g. <a id="fpps">.
                if c.tag == "a" and c.attrs.get("id") and not c.text():
                    self.flush()
                    self.blocks.append(Block("anchor", "", anchors=[c.attrs["id"]]))
                    continue
                self._inline.append(c)
                continue
            self.flush()
            self.block(c)
        self.flush()

    def block(self, n: Node) -> None:
        if "accordion-item" in n.cls:
            self.accordion(n)
        elif n.tag in HEADINGS or n.attrs.get("role") == "heading":
            level = HEADINGS.get(n.tag, 0) or int(n.attrs.get("aria-level", "0") or 0) or 3
            txt = n.text()
            if txt:
                self.blocks.append(Block("heading", txt, level=level, anchors=collect_anchors(n)))
        elif n.tag == "p":
            for img in n.find_all(
                lambda x: x.tag == "img" and "/-/media/" in x.attrs.get("src", "")
            ):
                self.blocks.append(
                    Block(
                        "media",
                        "image",
                        links=[Link(img.attrs["src"], img.attrs.get("alt", ""), "image")],
                    )
                )
            txt = n.text()
            if txt:
                kind = "footnote" if "Footnote" in n.cls else "paragraph"
                self.blocks.append(
                    Block(kind, txt, links=collect_links(n), anchors=collect_anchors(n))
                )
        elif n.tag in ("ul", "ol"):
            items: list[dict[str, object]] = []
            in_list: list[Node] = []
            self.list_items(n, 0, items, in_list)
            if items:
                self.blocks.append(
                    Block(
                        "list",
                        " ".join(str(i["text"]) for i in items),
                        items=items,
                        links=collect_links(n),
                    )
                )
            for t in in_list:
                self.table(t, None)
        elif n.tag == "table":
            self.table(n, None)
        else:
            self.walk(n)

    def accordion(self, n: Node) -> None:
        heading = n.find_all(lambda x: x.attrs.get("role") == "heading")
        desc = n.find_all(lambda x: "PAccordion__header-description" in x.cls)
        title = heading[0].text() if heading else "(untitled accordion)"
        self.blocks.append(
            Block("heading", title, level=0, accordion=True, anchors=collect_anchors(n))
        )
        if desc and desc[0].text():
            self.blocks.append(Block("accordion_summary", desc[0].text()))
        for body in n.find_all(lambda x: "accordion-body" in x.cls):
            self.walk(body)
        self.blocks.append(Block("accordion_end", ""))

    def list_items(
        self, n: Node, depth: int, out: list[dict[str, object]], tables: list[Node]
    ) -> None:
        for li in (c for c in n.children if isinstance(c, Node) and c.tag == "li"):
            out.append({"depth": depth, "text": without(li, {"ul", "ol", "table"}).text()})
            for sub in outermost(li, {"ul", "ol", "table"}):
                if sub.tag == "table":
                    tables.append(sub)  # emitted as its own block after the list
                else:
                    self.list_items(sub, depth + 1, out, tables)

    def table(self, n: Node, parent: str | None) -> None:
        idx = len(self.blocks)
        rows: list[list[str]] = []
        header_rows = 0
        row_spans: list[list[list[int]]] = []
        nested: list[Node] = []
        for tr in n.find_all(lambda x: x.tag == "tr"):
            if self._owner_table(n, tr) is not n:
                continue  # rows of a nested table belong to that table's block
            cells = []
            spans: list[list[int]] = []
            for td in (c for c in tr.children if isinstance(c, Node) and c.tag in ("td", "th")):
                inner = td.find_all(lambda x: x.tag == "table")
                nested += [t for t in inner if self._owner_table(td, t) is td]
                cells.append(self._cell_text(td))
                spans.append([int(td.attrs.get("colspan") or 1), int(td.attrs.get("rowspan") or 1)])
            if cells and all(
                isinstance(c, Node) and c.tag == "th" for c in tr.children if isinstance(c, Node)
            ):
                header_rows += 1
            rows.append(cells)
            row_spans.append(spans)
        text = " | ".join(" ; ".join(r) for r in rows)
        self.blocks.append(
            Block(
                "table",
                text,
                rows=rows,
                header_rows=header_rows,
                links=collect_links(n),
                nested_in=parent,
                spans=row_spans,
            )
        )
        for t in nested:
            self.table(t, f"#{idx}")  # resolved to a block id after numbering

    @staticmethod
    def _owner_table(scope: Node, target: Node) -> Node | None:
        """Nearest enclosing <table> (or the given cell scope) of target within scope."""

        def search(n: Node, owner: Node | None) -> Node | None:
            for c in n.children:
                if not isinstance(c, Node):
                    continue
                if c is target:
                    return owner
                r = search(c, c if c.tag == "table" or c is scope else owner)
                if r is not None:
                    return r
            return None

        return search(scope, scope)

    @staticmethod
    def _cell_text(td: Node) -> str:
        def strip(n: Node) -> Node:
            return Node(
                n.tag,
                n.attrs,
                [
                    c if isinstance(c, str) else strip(c)
                    for c in n.children
                    if isinstance(c, str) or c.tag != "table"
                ],
            )

        txt = strip(td).text()
        has_nested = bool(td.find_all(lambda x: x.tag == "table"))
        return f"{txt} [nested table]" if has_nested else txt


def without(n: Node, tags: set[str]) -> Node:
    """Copy of n with every descendant in tags removed (their text belongs elsewhere)."""
    return Node(
        n.tag,
        n.attrs,
        [
            c if isinstance(c, str) else without(c, tags)
            for c in n.children
            if isinstance(c, str) or c.tag not in tags
        ],
    )


def outermost(n: Node, tags: set[str]) -> list[Node]:
    """Descendants with a tag in tags that are not inside another such descendant."""
    found: list[Node] = []
    for c in n.children:
        if isinstance(c, Node):
            found += [c] if c.tag in tags else outermost(c, tags)
    return found


def content_root(doc: Node) -> Node:
    cols = doc.find_all(lambda x: "DestinationLayout_DestinationPageLayout__Cont" in x.cls)
    if cols:
        return cols[0]
    mains = doc.find_all(lambda x: x.tag == "main")
    return mains[0] if mains else doc


# ---------------------------------------------------------------- sections and passages ---
def letters(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(97 + r) + s
    return s


def build_record(source: dict[str, object], html: str) -> dict[str, object]:
    sid = str(source["source_id"])
    doc = parse(html)
    h1 = doc.find_all(lambda x: x.tag == "h1")
    page_title = h1[0].text() if h1 else str(source["title"])
    w = Walker()
    w.walk(content_root(doc))
    blocks = [b for b in w.blocks]

    # Number blocks, then resolve nested-table parents.
    for i, b in enumerate(blocks):
        b.block_id = f"{sid}.b{i:03d}"
    for b in blocks:
        if b.nested_in and b.nested_in.startswith("#"):
            b.nested_in = blocks[int(b.nested_in[1:])].block_id

    # Sections: accordion items get letters (S01.a ...); headings outside accordions get
    # h-numbers; headings inside an accordion get dotted numbers under it.
    sections: list[dict[str, object]] = [
        {
            "section_id": f"{sid}.0",
            "title": page_title,
            "path": [page_title],
            "level": 1,
            "kind": "page",
            "anchors": [],
            "parent": None,
        }
    ]
    acc_i = top_h = 0
    current_acc: dict[str, object] | None = None
    sub_i = 0
    stack: list[tuple[int, dict[str, object]]] = []  # (level, section) within current scope
    block_section: dict[str, str] = {}
    for b in blocks:
        if b.kind == "heading" and b.accordion:
            current_acc = {
                "section_id": f"{sid}.{letters(acc_i)}",
                "title": b.text,
                "path": [page_title, b.text],
                "level": 2,
                "kind": "accordion",
                "anchors": list(dict.fromkeys(b.anchors)),
                "parent": f"{sid}.0",
            }
            acc_i += 1
            sub_i = 0
            stack = []
            sections.append(current_acc)
        elif b.kind == "accordion_end":
            current_acc = None
            stack = []
        elif b.kind == "heading":
            while stack and stack[-1][0] >= b.level:
                stack.pop()
            parent = stack[-1][1] if stack else (current_acc or sections[0])
            if current_acc is not None:
                sub_i += 1
                sec_id = f"{current_acc['section_id']}.{sub_i}"
            else:
                top_h += 1
                sec_id = f"{sid}.h{top_h}"
            sec = {
                "section_id": sec_id,
                "title": b.text,
                "path": [*parent["path"], b.text],  # type: ignore[misc]
                "level": b.level,
                "kind": "heading",
                "anchors": list(b.anchors),
                "parent": parent["section_id"],
            }
            sections.append(sec)
            stack.append((b.level, sec))
        if b.kind == "anchor":
            target = stack[-1][1] if stack else (current_acc or sections[0])
            if b.anchors[0] not in target["anchors"]:  # type: ignore[operator]
                target["anchors"].append(b.anchors[0])  # type: ignore[union-attr]
        sec_now = stack[-1][1] if stack else (current_acc or sections[0])
        block_section[b.block_id] = str(sec_now["section_id"])

    content = [b for b in blocks if b.kind not in ("anchor", "accordion_end")]
    canonical = str(source["canonical_url"])
    acq = source["acquisition"]
    assert isinstance(acq, dict)

    # Passages: one per section, holding all its non-heading blocks in order, so a condition
    # always travels with the heading that names its applicant group (REQ-SRC-003). Tables
    # are not split; a long table stays whole rather than losing its row/column context.
    passages: list[dict[str, object]] = []
    by_sec: dict[str, list[Block]] = {}
    for b in content:
        if b.kind != "heading":
            by_sec.setdefault(block_section[b.block_id], []).append(b)
    sec_index = {str(s["section_id"]): s for s in sections}
    for sec in sections:
        bl = by_sec.get(str(sec["section_id"]), [])
        if not bl:
            continue
        text = "\n".join(b.text for b in bl)
        anchor = nearest_anchor(sec, sec_index)
        url = canonical + (f"?anchor={anchor}" if anchor else "")
        passages.append(
            {
                "passage_id": f"{sec['section_id']}.p1",
                "source_id": sid,
                "section_id": sec["section_id"],
                "heading_path": sec["path"],
                "block_ids": [b.block_id for b in bl],
                "block_kinds": sorted({b.kind for b in bl}),
                "source_url": url,
                "content_type": "html",
                "retrieved_at": acq.get("retrieved_at"),
                "page_last_updated": source.get("page_last_updated"),
                "policy_effective_date": source.get("effective_date"),
                "text": text,
                "text_sha256": hashlib.sha256(norm(text).encode()).hexdigest(),
                "review_status": "pending",
            }
        )

    return {
        "source_id": sid,
        "extractor_version": EXTRACTOR_VERSION,
        "raw_sha256": acq.get("raw_sha256"),
        "private_path": acq.get("private_path"),
        "page_title": page_title,
        "sections": sections,
        "blocks": [block_dict(b, block_section[b.block_id]) for b in content],
        "passages": passages,
    }


def nearest_anchor(sec: dict[str, object], index: dict[str, dict[str, object]]) -> str | None:
    """Same-page anchor of the section or its nearest ancestor (HDB uses ?anchor=<id>)."""
    cur: dict[str, object] | None = sec
    while cur is not None:
        anchors = cur["anchors"]
        assert isinstance(anchors, list)
        if anchors:
            return str(anchors[0])
        parent = cur["parent"]
        cur = index.get(str(parent)) if parent else None
    return None


def block_dict(b: Block, section_id: str) -> dict[str, object]:
    d: dict[str, object] = {
        "block_id": b.block_id,
        "section_id": section_id,
        "kind": b.kind,
        "text": b.text,
    }
    if b.kind == "heading":
        d["level"] = b.level
        d["accordion"] = b.accordion
    if b.items:
        d["items"] = b.items
    if b.rows:
        d["rows"] = b.rows
        d["header_rows"] = b.header_rows
        d["nested_in"] = b.nested_in
        d["spans"] = b.spans
    if b.links:
        d["links"] = [vars(x) for x in b.links]
    if b.anchors:
        d["anchors"] = b.anchors
    return d


# ---------------------------------------------------------------- commands ----------------
def manifest_sources() -> dict[str, dict[str, object]]:
    m = json.loads(MANIFEST.read_text())
    return {str(s["source_id"]): s for s in m["sources"]}


def newest(folder: Path, suffix: str) -> Path | None:
    files = sorted(f for f in folder.glob(f"*{suffix}") if STAMP.match(f.name))
    return files[-1] if files else None


def run_extract() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    sources = manifest_sources()
    for folder in sorted(p for p in RAW.glob("S*") if p.is_dir()):
        sid = folder.name
        f = newest(folder, ".html")
        if f is None or sid not in sources:
            continue
        data = f.read_bytes()
        if hashlib.sha256(data).hexdigest() != sources[sid]["acquisition"]["raw_sha256"]:  # type: ignore[index]
            sys.exit(
                f"{sid}: raw hash differs from the manifest; run snapshots.py register "
                "only if the new capture is intended"
            )
        rec = build_record(sources[sid], data.decode("utf-8", errors="replace"))
        out = PROCESSED / f"{sid}.json"
        out.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
        kinds: dict[str, int] = {}
        for b in rec["blocks"]:  # type: ignore[attr-defined]
            kinds[b["kind"]] = kinds.get(b["kind"], 0) + 1
        print(
            f"{sid}: sections={len(rec['sections'])} passages={len(rec['passages'])} "  # type: ignore[arg-type]
            f"blocks={kinds}"
        )


# ---------------------------------------------------------------- validate ----------------
EXPECTED_SECTIONS = CORPUS_META / "expected_sections.json"
SENTENCE_MIN = 30


def canon(text: str) -> str:
    """norm() plus link-join repair ("service ." -> "service.") for robust matching."""
    return re.sub(r"\s+([.,;:!?)])", r"\1", norm(text).replace("( ", "("))


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?:;])\s+", canon(text)) if len(s) >= SENTENCE_MIN]


def html_segments(fragment: str) -> list[str]:
    """Text of an HTML fragment split at block boundaries, so a heading never fuses with
    the paragraph after it."""
    tree = parse(fragment)
    out: list[str] = []

    def visit(n: Node) -> None:
        inline_only = all(isinstance(c, str) or c.tag in INLINE for c in n.children)
        if inline_only and n.tag != "#root":
            out.append(n.text())
            return
        buf: list[Node | str] = []
        for c in n.children:
            if isinstance(c, str) or c.tag in INLINE:
                buf.append(c)
                continue
            if buf:
                out.append(Node("p", {}, buf).text())
                buf = []
            visit(c)
        if buf:
            out.append(Node("p", {}, buf).text())

    visit(tree)
    return [x for x in out if x.strip()]


def chrome_text(doc: Node) -> str:
    return canon(
        " ".join(
            n.text()
            for n in doc.find_all(
                lambda x: (
                    any(c in x.cls for c in CHROME_CLASSES) or x.tag in ("nav", "footer", "header")
                )
            )
        )
    )


def match_expected(spec: list[dict[str, str]], title: str) -> dict[str, str] | None:
    for item in spec:
        if re.search(item["match"], norm(title)):
            return item
    return None


def resolve_link(href: str, page_url: str, sources: dict[str, dict[str, object]]) -> str | None:
    """Manifest source ID a link points to, by canonical-URL prefix (anchors ignored)."""
    h = href.split("#")[0].split("?")[0].rstrip("/")
    if h.startswith("/"):
        h = "https://www.hdb.gov.sg" + h
    if not h:
        return None
    best: tuple[int, str] | None = None
    for sid, s in sources.items():
        for key in ("canonical_url", "original_url"):
            u = str(s.get(key) or "").split("?")[0].rstrip("/")
            if (
                u
                and (h == u or h.endswith(u.split("://", 1)[-1]))
                and (best is None or len(u) > best[0])
            ):
                best = (len(u), sid)
        acq = s.get("acquisition")
        if isinstance(acq, dict):
            for key in ("requested_url", "final_url"):
                u = str(acq.get(key) or "").rstrip("/")
                if u and h == u:
                    best = (len(u), sid)
    _ = page_url
    return best[1] if best else None


def validate_source(
    rec: dict[str, object],
    raw_html: str,
    spec: list[dict[str, str]],
    sources: dict[str, dict[str, object]],
    snapshot_count: int,
    spec_links: list[dict[str, str]] | None = None,
) -> tuple[dict[str, object], dict[str, object]]:
    """Return (tracked summary with counts/IDs only, private detail with text fragments)."""
    sid = str(rec["source_id"])
    sections = rec["sections"]
    blocks = rec["blocks"]
    passages = rec["passages"]
    assert isinstance(sections, list) and isinstance(blocks, list) and isinstance(passages, list)
    passage_text = canon(" ".join([str(rec["page_title"]), *(str(b["text"]) for b in blocks)]))
    by_section: dict[str, list[dict[str, object]]] = {}
    for b in blocks:
        by_section.setdefault(str(b["section_id"]), []).append(b)
    detail: dict[str, object] = {"source_id": sid}
    issues: list[dict[str, str]] = []

    # 1. Accordions: toggles counted on the raw HTML, independently of the tree walker.
    raw_toggles = len(re.findall(r'class="accordion-button[^"]*"', raw_html))
    acc = [s for s in sections if s["kind"] == "accordion"]
    acc_rows = []
    for s in acc:
        own = [
            s["section_id"],
            *[
                x["section_id"]
                for x in sections
                if str(x["section_id"]).startswith(f"{s['section_id']}.")
            ],
        ]
        kinds = sorted(
            {
                str(b["kind"])
                for sec in own
                for b in by_section.get(str(sec), [])
                if b["kind"] not in ("heading", "accordion_summary")
            }
        )
        acc_rows.append(
            {
                "section_id": s["section_id"],
                "title": short(str(s["title"])),
                "body_block_kinds": kinds,
            }
        )
        if not kinds:
            issues.append(
                {
                    "kind": "extraction_failure",
                    "where": str(s["section_id"]),
                    "detail": "accordion body has no extracted content",
                }
            )
    collapsed = len(re.findall(r'aria-expanded="false"[^>]*>\s*<div class="PAccordion', raw_html))

    # 2. Expected sections from the matrix / data_sources §2.2 versus extracted headings.
    expected_rows = []
    seen_items: set[str] = set()
    for s in sections:
        if s["kind"] == "page":
            continue
        item = match_expected(spec, " > ".join(str(t) for t in s["path"][1:]))  # type: ignore[index]
        own_kinds = sorted(
            {
                str(b["kind"])
                for b in by_section.get(str(s["section_id"]), [])
                if b["kind"] != "heading"
            }
        )
        row = {
            "section_id": s["section_id"],
            "title": short(str(s["title"])),
            "scope": item["scope"] if item else "unexpected",
            "content": own_kinds,
        }
        if item:
            seen_items.add(item["match"])
        else:
            issues.append(
                {
                    "kind": "unexpected_section",
                    "where": str(s["section_id"]),
                    "detail": "heading not in the expected-section checklist",
                }
            )
        expected_rows.append(row)
    for item in spec:
        if item["match"] not in seen_items:
            issues.append(
                {
                    "kind": "missing_section",
                    "where": sid,
                    "detail": f"expected '{item.get('label', item['match'])}' not found",
                }
            )

    chrome_all = chrome_text(parse(raw_html))
    # 3. Independent heading check with the snapshots.py parser (whole page, incl. chrome).
    snap = Snapshot()
    snap.feed(raw_html)
    extracted_titles = {norm(str(s["title"])) for s in sections}
    page_headings = [h for _, h in snap.headings if h]
    unmatched_all = sorted({h for h in page_headings if h not in extracted_titles})
    in_cells = [h for h in unmatched_all if canon(h) in passage_text]
    unmatched = [h for h in unmatched_all if h not in in_cells and canon(h) not in chrome_all]

    # 4. Text coverage: page-data sentences (Sitecore __NEXT_DATA__) found in the passages.
    missing_sents: list[str] = []
    total = found = 0
    if snap.next_data.strip():
        for path, s_ in json_strings(json.loads(snap.next_data)):
            if len(s_) < 40 or s_.startswith(("http", "/", "{")) or ".fields.meta" in path:
                continue
            for seg in html_segments(s_) if "<" in s_ else [s_]:
                for sent in sentences(seg):
                    total += 1
                    if sent in passage_text:
                        found += 1
                    else:
                        missing_sents.append(sent)
    dom_text = canon(" ".join(snap.text))
    chrome = chrome_all
    in_dom = [x for x in missing_sents if x in dom_text]
    in_chrome = [x for x in in_dom if x in chrome]
    in_dom_not_l1 = [x for x in in_dom if x not in chrome]
    not_rendered = [x for x in missing_sents if x not in dom_text]
    if in_dom_not_l1:
        issues.append(
            {
                "kind": "extraction_gap",
                "where": sid,
                "detail": f"{len(in_dom_not_l1)} rendered content sentence(s) not in "
                "extracted blocks (see private detail)",
            }
        )
    detail["rendered_but_not_extracted"] = in_dom_not_l1
    detail["chrome_only"] = in_chrome
    detail["not_rendered"] = not_rendered

    # 5. Tables: count on raw HTML vs extracted; spans flagged for manual check.
    root_html = raw_html.split("DestinationLayout_DestinationPageLayout__Cont", 1)[-1]
    raw_tables = len(re.findall(r"<table\b", root_html.split("<footer", 1)[0]))
    tables = [b for b in blocks if b["kind"] == "table"]
    table_rows = []
    for t in tables:
        rows = t["rows"]
        spans = t.get("spans") or []
        assert isinstance(rows, list) and isinstance(spans, list)
        merged = sum(1 for r in spans for c in r if c != [1, 1])
        empty = sum(1 for r in rows for c in r if not str(c).strip())
        table_rows.append(
            {
                "block_id": t["block_id"],
                "section_id": t["section_id"],
                "rows": len(rows),
                "cells": sum(len(r) for r in rows),
                "header_rows": t.get("header_rows"),
                "merged_cells": merged,
                "empty_cells": empty,
                "nested_in": t.get("nested_in"),
            }
        )
        if merged:
            issues.append(
                {
                    "kind": "manual_check",
                    "where": str(t["block_id"]),
                    "detail": f"{merged} merged cell(s): confirm which rows a value "
                    "applies to against the rendered page",
                }
            )
    if raw_tables != len(tables):
        issues.append(
            {
                "kind": "extraction_failure",
                "where": sid,
                "detail": f"raw <table> count {raw_tables} != extracted {len(tables)}",
            }
        )

    # 6. Links: classified and resolved against the manifest.
    link_rows: dict[str, dict[str, object]] = {}
    for b in blocks:
        for ln in b.get("links", []) or []:  # type: ignore[union-attr]
            href = str(ln["href"])
            if ln["kind"] in ("image", "video"):
                continue
            target = resolve_link(href, "", sources)
            key = href.split("?si=")[0]
            row = link_rows.setdefault(
                key,
                {
                    "href": key[:160],
                    "kind": ln["kind"],
                    "target_source_id": target,
                    "count": 0,
                    "sections": [],
                },
            )
            row["count"] = int(row["count"]) + 1  # type: ignore[call-overload]
            secs = row["sections"]
            assert isinstance(secs, list)
            if b["section_id"] not in secs:
                secs.append(b["section_id"])
    deps = spec_links or []
    for row in link_rows.values():
        t = row["target_source_id"]
        row["status"] = (
            "same_page"
            if row["kind"] == "same_page" and t in (None, sid)
            else f"manifest:{sources[str(t)]['mvp_class']}"
            if t
            else "transactional_or_service"
            if re.search(r"services2|homes\.hdb|iam\.hdb|singpass", str(row["href"]))
            else "unmapped"
        )
        if row["status"] == "unmapped":
            for d in deps:
                if re.search(d["match"], str(row["href"])):
                    row["status"] = f"dependency:{d['class']}"
                    row["note"] = d["note"]
                    break
        if row["status"] == "unmapped":
            issues.append(
                {"kind": "unresolved_link", "where": sid, "detail": short(str(row["href"]))}
            )

    # 7. Duplicates and malformed passages.
    hashes: dict[str, list[str]] = {}
    for p in passages:
        hashes.setdefault(str(p["text_sha256"]), []).append(str(p["passage_id"]))
    dup_blocks: dict[str, list[str]] = {}
    for b in blocks:
        if b["kind"] in ("paragraph", "list", "table", "footnote") and len(str(b["text"])) > 60:
            dup_blocks.setdefault(
                hashlib.sha256(norm(str(b["text"])).encode()).hexdigest(), []
            ).append(str(b["block_id"]))
    empty_sections = [
        s["section_id"]
        for s in sections
        if not [b for b in by_section.get(str(s["section_id"]), []) if b["kind"] != "heading"]
    ]
    ids = [p["passage_id"] for p in passages]

    # 8. Temporal metadata.
    temporal = {
        "retrieved_at": sorted({str(p["retrieved_at"]) for p in passages}),
        "page_last_updated": sorted({str(p["page_last_updated"]) for p in passages}),
        "effective_date_known": any(p["policy_effective_date"] for p in passages),
    }
    if not temporal["effective_date_known"]:
        issues.append(
            {
                "kind": "temporal_gap",
                "where": sid,
                "detail": "no stated effective date; page 'last updated' date only",
            }
        )
    if snapshot_count < 2:
        issues.append(
            {
                "kind": "limitation",
                "where": sid,
                "detail": "single default-state snapshot: no default-vs-expanded diff. "
                "Mitigation: collapsed panels present in DOM + page-data check",
            }
        )

    summary = {
        "source_id": sid,
        "raw_sha256": rec["raw_sha256"],
        "extractor_version": rec["extractor_version"],
        "snapshots": snapshot_count,
        "counts": {
            "sections": len(sections),
            "passages": len(passages),
            "blocks": len(blocks),
            "tables": len(tables),
            "raw_tables": raw_tables,
            "accordions_extracted": len(acc),
            "accordion_toggles_raw": raw_toggles,
            "accordions_collapsed_at_capture": collapsed,
        },
        "accordions": acc_rows,
        "sections": expected_rows,
        "headings": {
            "page_total": len(page_headings),
            "as_sections": len([h for h in page_headings if h in extracted_titles]),
            "inside_table_or_list_text": [short(h) for h in in_cells],
            "site_chrome": len(unmatched_all) - len(in_cells) - len(unmatched),
            "not_extracted": [short(h) for h in unmatched],
        },
        "page_data_coverage": {
            "sentences": total,
            "in_extracted_blocks": found,
            "site_chrome_excluded": len(in_chrome),
            "not_rendered_metadata": len(not_rendered),
            "rendered_but_not_extracted": len(in_dom_not_l1),
        },
        "tables": table_rows,
        "links": sorted(link_rows.values(), key=lambda r: str(r["href"])),
        "duplicates": {
            "passages": [v for v in hashes.values() if len(v) > 1],
            "blocks": [v for v in dup_blocks.values() if len(v) > 1],
        },
        "empty_sections": empty_sections,
        "passage_ids_unique": len(ids) == len(set(ids)),
        "temporal": temporal,
        "issues": issues,
    }
    return summary, detail


def run_validate() -> None:
    spec_all = json.loads(EXPECTED_SECTIONS.read_text())
    sources = manifest_sources()
    reports, details = [], []
    for sid in sorted(spec_all["html"]):
        rec_path = PROCESSED / f"{sid}.json"
        if not rec_path.exists():
            print(f"{sid}: not extracted; run extract first")
            continue
        rec = json.loads(rec_path.read_text())
        f = newest(RAW / sid, ".html")
        assert f is not None
        count = len([x for x in (RAW / sid).glob("*.html") if STAMP.match(x.name)])
        s, d = validate_source(
            rec,
            f.read_text(encoding="utf-8", errors="replace"),
            spec_all["html"][sid],
            sources,
            count,
            spec_all.get("link_dependencies"),
        )
        reports.append(s)
        details.append(d)
        kinds: dict[str, int] = {}
        for i in s["issues"]:  # type: ignore[attr-defined]
            kinds[i["kind"]] = kinds.get(i["kind"], 0) + 1
        cov = s["page_data_coverage"]
        print(
            f"{sid}: passages={s['counts']['passages']} "  # type: ignore[index]
            f"page-data {cov['in_extracted_blocks']}/{cov['sentences']} "  # type: ignore[index]
            f"chrome={cov['site_chrome_excluded']} meta={cov['not_rendered_metadata']} "  # type: ignore[index]
            f"rendered-not-extracted={cov['rendered_but_not_extracted']} issues={kinds}"
        )  # type: ignore[index]
    pdfs = []
    for sid, item in sorted(spec_all["pdf"].items()):
        acq = sources[sid]["acquisition"]
        assert isinstance(acq, dict)
        pdfs.append(
            {
                "source_id": sid,
                "raw_sha256": acq.get("raw_sha256"),
                "method": "manual page review (D-052); no text extraction",
                **item,
            }
        )
    report = {
        "report_version": EXTRACTOR_VERSION,
        "generated_from": "data/private_corpus (local only)",
        "note": "Counts, IDs and short heading labels only; no source passages (D-054).",
        "html_sources": reports,
        "pdf_sources": pdfs,
    }
    CORPUS_META.mkdir(parents=True, exist_ok=True)
    (CORPUS_META / "extraction_report.json").write_text(
        json.dumps(report, indent=1, ensure_ascii=False) + "\n"
    )
    (PROCESSED / "validation_detail.json").write_text(
        json.dumps(details, indent=1, ensure_ascii=False) + "\n"
    )
    print("wrote data/corpus/extraction_report.json (+ private validation_detail.json)")


# ---------------------------------------------------------------- facts -------------------
FACT_ID = re.compile(r"^[A-Z]{2,4}-[A-Z0-9]+(-[A-Z0-9]+)*-\d{3}$")
REQUIRED = (
    "fact_id",
    "statement",
    "topic",
    "scope_tier",
    "applies_to",
    "exceptions",
    "source",
    "retrieved_at",
    "validation",
    "rights_review",
    "kb_version",
    "critical",
)
WORD = re.compile(r"[a-z0-9$%]+(?:[.'\u2019][a-z0-9]+)*")


def words(text: str) -> list[str]:
    return WORD.findall(norm(text))


def longest_shared_run(a: list[str], b: list[str]) -> tuple[int, str]:
    """Longest run of consecutive identical words shared by a and b (dynamic programming)."""
    best, end = 0, 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, end = cur[j], i
        prev = cur
    return best, " ".join(a[end - best : end])


def load_facts(path: Path = FACTS) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def check_facts(
    facts: list[dict[str, object]],
    sources: dict[str, dict[str, object]],
    l1: dict[str, dict[str, object]],
) -> tuple[list[dict[str, object]], list[str]]:
    """Integrity and overlap checks. Returns (per-fact rows, errors). Rows hold no source text."""
    errors: list[str] = []
    ids = [str(f.get("fact_id")) for f in facts]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"duplicate fact_id {dup}")
    known = set(ids)
    rows = []
    for f in facts:
        fid = str(f.get("fact_id"))
        for key in REQUIRED:
            if key not in f:
                errors.append(f"{fid}: missing field {key}")
        if not FACT_ID.match(fid):
            errors.append(f"{fid}: fact_id format")
        src = f.get("source")
        if not isinstance(src, dict):
            errors.append(f"{fid}: source must be an object")
            continue
        sid = str(src.get("source_id"))
        man = sources.get(sid)
        if man is None:
            errors.append(f"{fid}: source_id {sid} not in manifest")
            continue
        if man.get("mvp_class") in ("outside_mvp", "pending"):
            errors.append(f"{fid}: cites {sid}, classed {man.get('mvp_class')}")
        url = str(src.get("url", ""))
        if not url.startswith(str(man.get("canonical_url"))):
            errors.append(f"{fid}: url does not start with the manifest canonical_url of {sid}")
        if not url.startswith("https://"):
            errors.append(f"{fid}: url must be an absolute https official URL")
        for ex in f.get("exceptions", []) or []:  # type: ignore[union-attr]
            ref = ex.get("fact_id") if isinstance(ex, dict) else None
            if ref and ref not in known:
                errors.append(f"{fid}: exception references unknown fact {ref}")
        # Section and passage provenance resolve against L1 when it is present locally.
        rec = l1.get(sid)
        source_words: list[str] = []
        passage_words: list[str] = []
        if rec is not None:
            secs = {str(s["section_id"]) for s in rec["sections"]}  # type: ignore[attr-defined]
            pids = {str(p["passage_id"]): p for p in rec["passages"]}  # type: ignore[attr-defined]
            if src.get("section_id") not in secs:
                errors.append(f"{fid}: section_id {src.get('section_id')} not in L1 {sid}")
            for pid in f.get("private_passage_ids", []) or []:  # type: ignore[union-attr]
                if pid not in pids:
                    errors.append(f"{fid}: passage {pid} not in L1 {sid}")
                else:
                    passage_words += words(str(pids[pid]["text"]))
            source_words = words(" ".join(str(p["text"]) for p in pids.values()))
        elif "pdf" not in str(man.get("content_format")):
            errors.append(f"{fid}: no L1 record for {sid}; run extract")
        authored = " ".join(
            [
                str(f.get("statement", "")),
                *[
                    str(e.get("description", ""))
                    for e in f.get("exceptions", []) or []  # type: ignore[union-attr]
                    if isinstance(e, dict)
                ],
            ]
        )
        run, _ = longest_shared_run(words(authored), source_words) if source_words else (0, "")
        rows.append(
            {
                "fact_id": fid,
                "source_id": sid,
                "section_id": src.get("section_id"),
                "topic": f.get("topic"),
                "scope_tier": f.get("scope_tier"),
                "critical": f.get("critical"),
                "validation_status": (f.get("validation") or {}).get("status"),  # type: ignore[union-attr]
                "rights_status": (f.get("rights_review") or {}).get("status"),  # type: ignore[union-attr]
                "max_shared_run_words": run,
                "overlap_flag": run >= OVERLAP_WORDS,
                "overlap_checked_against": "L1 passages" if source_words else "manual (PDF, D-052)",
            }
        )
    return rows, errors


def load_l1() -> dict[str, dict[str, object]]:
    return {p.stem: json.loads(p.read_text()) for p in sorted(PROCESSED.glob("S*.json"))}


def run_facts() -> None:
    facts = load_facts()
    rows, errors = check_facts(facts, manifest_sources(), load_l1())
    flagged = [r for r in rows if r["overlap_flag"]]
    CORPUS_META.mkdir(parents=True, exist_ok=True)
    (CORPUS_META / "fact_check_report.json").write_text(
        json.dumps(
            {"overlap_threshold_words": OVERLAP_WORDS, "facts": rows, "errors": errors},
            indent=1,
            ensure_ascii=False,
        )
        + "\n"
    )
    print(f"facts={len(facts)} errors={len(errors)} overlap_flags={len(flagged)}")
    for e in errors:
        print("  ERROR", e)
    for r in flagged:
        print(f"  OVERLAP {r['fact_id']}: {r['max_shared_run_words']} shared words (reword)")
    if errors:
        sys.exit(1)


# ---------------------------------------------------------------- verify ------------------
REVIEW = CORPUS_META / "critical_fact_review.json"
NUMBER = re.compile(r"(?<![A-Za-z0-9])\$?\d[\d,]*\d%?|(?<![A-Za-z0-9])\$?\d%?")  # not IDs like S01
ANCHOR_MAX_WORDS = 6  # anchors are short phrases, far below the 8-word overlap threshold


def verify_fact(
    fact: dict[str, object], item: dict[str, object], l1: dict[str, dict[str, object]]
) -> dict[str, object]:
    """Deterministic part of the checklist review: every number in the statement and every
    authored term anchor must occur in the fact's cited L1 section. PDF facts have no L1
    text and rely on the recorded manual page check (D-052)."""
    src = fact["source"]
    assert isinstance(src, dict)
    sid, sec = str(src["source_id"]), str(src["section_id"])
    anchors = [str(a) for a in item.get("term_anchors", [])]  # type: ignore[union-attr]
    too_long = [a for a in anchors if len(a.split()) > ANCHOR_MAX_WORDS]
    numbers = sorted({n.rstrip(",") for n in NUMBER.findall(str(fact["statement"]))})
    rec = l1.get(sid)
    if rec is None:
        return {
            "fact_id": fact["fact_id"],
            "checklist": item["checklist"],
            "method": "manual_pdf_page_check",
            "numbers": numbers,
            "missing": [],
            "anchor_too_long": too_long,
            "result": "pass" if not too_long else "fail",
        }
    # The cited section's own heading path counts: conditions are often stated in headings.
    text = canon(
        " ".join(
            " ".join([*map(str, p["heading_path"]), str(p["text"])])
            for p in rec["passages"]  # type: ignore[attr-defined]
            if p["section_id"] == sec
        )
    )
    missing = [n for n in numbers if n.lower() not in text] + [
        a for a in anchors if canon(a) not in text
    ]
    return {
        "fact_id": fact["fact_id"],
        "checklist": item["checklist"],
        "method": "anchor_check_on_cited_section+agent_reading",
        "numbers": numbers,
        "anchors_checked": len(anchors),
        "missing": missing,
        "anchor_too_long": too_long,
        "result": "pass" if not missing and not too_long else "fail",
    }


def run_verify() -> None:
    review = json.loads(REVIEW.read_text())
    items = {str(i["fact_id"]): i for i in review["items"]}
    facts = load_facts()
    l1 = load_l1()
    sources = manifest_sources()
    rows, _ = check_facts(facts, sources, l1)
    runs = {str(r["fact_id"]): r["max_shared_run_words"] for r in rows}
    unreviewed_critical = [
        f["fact_id"] for f in facts if f["critical"] and f["fact_id"] not in items
    ]
    results = []
    for f in facts:
        fid = str(f["fact_id"])
        rr = f["rights_review"]
        assert isinstance(rr, dict)
        if fid in runs and f["source"]["source_id"] in l1:  # type: ignore[index]
            rr["max_shared_run_words"] = runs[fid]  # refresh after any rewording
        if fid not in items:
            continue
        res = verify_fact(f, items[fid], l1)
        results.append(res)
        if res["result"] == "pass":
            f["validation"] = {
                "status": "verified",
                "method": f"checklist {items[fid]['checklist']}: {res['method']} against the "
                "hash-pinned 2026-10-28 snapshot (D-058 as revised); no live-page check",
                "validated_at": review["reviewed_at"],
                "notes": str(items[fid]["notes"]),
            }
    FACTS.write_text("".join(json.dumps(f, ensure_ascii=False) + "\n" for f in facts))
    failed = [r for r in results if r["result"] != "pass"]
    (CORPUS_META / "fact_verification.json").write_text(
        json.dumps(
            {
                "reviewed_at": review["reviewed_at"],
                "results": results,
                "unreviewed_critical": unreviewed_critical,
            },
            indent=1,
            ensure_ascii=False,
        )
        + "\n"
    )
    print(
        f"reviewed={len(results)} passed={len(results) - len(failed)} failed={len(failed)} "
        f"unreviewed_critical={len(unreviewed_critical)}"
    )
    for r in failed:
        print(f"  FAIL {r['fact_id']}: missing={r['missing']} too_long={r['anchor_too_long']}")
    if failed or unreviewed_critical:
        sys.exit(1)


# ---------------------------------------------------------------- freeze ------------------
KB_VERSION = "kb-2026-10-28.1"


def sha_file(p: Path) -> str | None:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def rules_version() -> str | None:
    m = re.search(r"^rules_version: (\S+)$", RULES.read_text(), re.M) if RULES.exists() else None
    return m.group(1) if m else None


def run_freeze() -> None:
    facts = load_facts()
    sources = manifest_sources()
    by: dict[str, dict[str, int]] = {"topic": {}, "scope_tier": {}, "validation": {}, "rights": {}}
    for f in facts:
        for key, val in (
            ("topic", f["topic"]),
            ("scope_tier", f["scope_tier"]),
            ("validation", f["validation"]["status"]),  # type: ignore[index]
            ("rights", f["rights_review"]["status"]),
        ):  # type: ignore[index]
            by[key][str(val)] = by[key].get(str(val), 0) + 1
    versions = {str(f["kb_version"]) for f in facts}
    if versions != {KB_VERSION}:
        sys.exit(f"kb_version mismatch in facts: {sorted(versions)}")
    cited = sorted({str(f["source"]["source_id"]) for f in facts})  # type: ignore[index]
    l1 = load_l1()
    frozen = {
        "kb_version": KB_VERSION,
        "policy_period": "HDB sources retrieved 28 Oct 2026 (UTC); no stated effective dates",
        "extractor_version": EXTRACTOR_VERSION,
        "sources": [
            {
                "source_id": sid,
                "retrieved_at": sources[sid]["acquisition"]["retrieved_at"],  # type: ignore[index]
                "raw_sha256": sources[sid]["acquisition"]["raw_sha256"],  # type: ignore[index]
                "text_sha256": sources[sid]["acquisition"]["text_sha256"],  # type: ignore[index]
                "page_last_updated": sources[sid].get("page_last_updated"),
                "effective_date": sources[sid].get("effective_date"),
                "effective_date_status": sources[sid].get("effective_date_status"),
                "l1_passages": len(l1[sid]["passages"]) if sid in l1 else None,  # type: ignore[arg-type]
                "facts": sum(1 for f in facts if f["source"]["source_id"] == sid),
            }  # type: ignore[index]
            for sid in cited
        ],
        "fact_count": len(facts),
        "rules_version": rules_version(),
        "fact_counts": by,
        "files_sha256": {
            str(p.relative_to(ROOT)): sha_file(p)
            for p in (
                FACTS,
                VISUALS,
                COVERAGE,
                MANIFEST,
                EXPECTED_SECTIONS,
                RULES,
                REVIEW,
                CORPUS_META / "fact_verification.json",
                CORPUS_META / "extraction_report.json",
                CORPUS_META / "fact_check_report.json",
            )
        },
        "freeze_status": "frozen: scope (D-061), verification (D-058) and rules (D-062) approved",
    }
    (CORPUS_META / "corpus_version.json").write_text(
        json.dumps(frozen, indent=1, ensure_ascii=False) + "\n"
    )
    print(f"frozen {KB_VERSION}: {len(facts)} facts from {len(cited)} sources")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    commands = {
        "extract": run_extract,
        "validate": run_validate,
        "facts": run_facts,
        "verify": run_verify,
        "freeze": run_freeze,
    }
    if cmd not in commands:
        sys.exit("usage: python -I scripts/corpus.py {extract|validate|facts|verify|freeze}")
    commands[cmd]()


if __name__ == "__main__":
    main()
