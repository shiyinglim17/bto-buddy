"""BM25 retrieval over the authored KB (stage 4b, D-031). Pure: never imports the LLM client.

Segmentation: one authored fact = one passage. Facts are already atomic and short (one
condition each, ~20-40 words), so splitting would break a condition from its qualifier and
merging would blur citations. Each indexed document is the fact's statement plus its
aliases, topic words, section heading and exception descriptions, so exact policy terms
("HFE", "core occupier") and the authored paraphrases both match. Built deterministically
from data/policy_facts.jsonl; nothing reads the private corpus.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from rank_bm25 import BM25Okapi

from bto_buddy.policy import KnowledgeBase
from bto_buddy.schemas import Evidence, EvidenceBundle, EvidenceGap, PolicyFact

# Passed to generation. Dev recall rose from 0.42 (k=8) to 0.52 (k=12); 12 x ~50 tokens still
# fits the 8K tokens-per-minute plan.
DEFAULT_K = 12
_STOP_WORDS = (
    "a an the and or of to in on for with is are be we our us i my me you your can do "
    "does what how when which who will would should if it this that at as by from have has"
)
_STOP = frozenset(_STOP_WORDS.split())
# Colloquial -> KB vocabulary. Small and reviewable; extended only on dev retrieval misses.
_SYNONYMS = {
    "wife": ["spouse", "married"],
    "husband": ["spouse", "married"],
    "bto": ["flat", "new"],
    "letter": ["hfe"],
    "pr": ["spr", "permanent", "resident"],
    "citizen": ["sc"],
}


def tokenize(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    out: list[str] = []
    for tok in re.findall(r"[a-z0-9]+", text):
        if tok in _STOP:
            continue
        if len(tok) > 3 and tok.endswith("s") and not tok.endswith("ss"):
            tok = tok[:-1]  # crude plural folding: "applicants" -> "applicant"
        out.append(tok)
        out.extend(_SYNONYMS.get(tok, []))
    return out


def document_text(f: PolicyFact) -> str:
    return " ".join(
        [
            f.statement,
            " ".join(f.aliases),
            f.topic.value.replace("_", " "),
            f.source.section,
            " ".join(e.description for e in f.exceptions),
        ]
    )


@dataclass(frozen=True)
class Index:
    facts: tuple[PolicyFact, ...]
    bm25: BM25Okapi
    kb_version: str


def build_index(kb: KnowledgeBase) -> Index:
    facts = tuple(f for f in kb.facts if f.usable())  # runtime filter (D-058)
    return Index(facts, BM25Okapi([tokenize(document_text(f)) for f in facts]), kb.kb_version)


def search(index: Index, query: str, k: int = DEFAULT_K) -> list[tuple[PolicyFact, float]]:
    scores = index.bm25.get_scores(tokenize(query))
    # Deterministic ties: score descending, then fact ID.
    ranked = sorted(zip(index.facts, scores, strict=True), key=lambda p: (-p[1], p[0].fact_id))
    return [(f, float(s)) for f, s in ranked[:k] if s > 0]


def retrieve(index: Index, query: str, k: int = DEFAULT_K) -> EvidenceBundle:
    hits = search(index, query, k)
    items = [
        Evidence(
            fact_id=f.fact_id,
            statement=f.statement,
            exceptions=[e.description for e in f.exceptions],
            source_url=f.source.url,
            section=f.source.section,
            origin="bm25",
            bm25_score=round(s, 4),
            rank=i + 1,
        )
        for i, (f, s) in enumerate(hits)
    ]
    gaps = (
        []
        if items
        else [
            EvidenceGap(
                topic=None,
                kind="no_evidence_for_topic",
                detail="No matching policy facts were found for this question.",
                official_source_url="https://www.hdb.gov.sg",
            )
        ]
    )
    return EvidenceBundle(
        items=items, query=query, k=k, kb_version=index.kb_version, evidence_gaps=gaps
    )


def evidence_block(bundle: EvidenceBundle) -> str:
    """The policy-sources section of generate_v1 for B (and later C/D)."""
    if not bundle.items:
        return (
            "No matching facts were found. Do not state policy facts as established; say the "
            "point needs official confirmation. cited_fact_ids must be an empty list."
        )
    lines = [
        "Use ONLY these verified facts for policy statements, and cite their IDs in "
        "cited_fact_ids. If they do not cover a point, say it needs official confirmation "
        "(a caveat); absence of a fact here does not mean the requirement does not exist."
    ]
    for e in bundle.items:
        exc = f" Exceptions: {'; '.join(e.exceptions)}" if e.exceptions else ""
        lines.append(f"[{e.fact_id}] {e.statement}{exc}")
    return "\n".join(lines)
