"""BM25 retrieval over the tracked KB and configuration B (no network: fake client)."""

from __future__ import annotations

import json
from datetime import date

from bto_buddy import pipeline, retrieval
from bto_buddy.policy import load_kb
from bto_buddy.schemas import UserRequest
from test_baseline import VALID, FakeClient

INDEX = retrieval.build_index(load_kb())


def ids(query: str, k: int = 5) -> list[str]:
    return [f.fact_id for f, _ in retrieval.search(INDEX, query, k)]


def test_index_uses_only_usable_tracked_facts() -> None:
    assert INDEX.facts and all(f.usable() for f in INDEX.facts)


def test_exact_policy_terminology() -> None:
    assert "HFE-VALID-001" in ids("How long is the HFE letter valid?")


def test_paraphrased_query() -> None:
    # "fiancée" with an accent, no "HFE" or "family nucleus" wording.
    assert "HH-COUPLE-001" in ids("Can my fiancée and I buy a new flat together?", 8)


def test_multiple_conditions_query_returns_several_relevant_facts() -> None:
    got = ids("engaged couple HFE letter validity and marriage registration", 8)
    assert {"HFE-VALID-001", "HH-MARRY-001"} <= set(got)


def test_no_relevant_evidence_gives_gap_not_facts() -> None:
    bundle = retrieval.retrieve(INDEX, "zxqv blorp")
    assert bundle.items == [] and bundle.evidence_gaps[0].kind == "no_evidence_for_topic"
    assert "official confirmation" in retrieval.evidence_block(bundle)


def test_ranking_is_deterministic() -> None:
    q = "What documents do we need for the HFE application?"
    assert ids(q, 12) == ids(q, 12)


REQ = UserRequest(
    request_id="T-B",
    situation_text="We are an engaged Singapore Citizen couple, both first-timers.",
    question="How long is the HFE letter valid?",
    as_of=date(2026, 11, 1),
)


def test_rag_cites_bundle_facts_and_maps_to_official_sources() -> None:
    bundle = retrieval.retrieve(INDEX, f"{REQ.question} {REQ.situation_text}")
    fid = bundle.items[0].fact_id
    out = {
        **VALID,
        "claims": [{"claim_id": "c1", "text": "x", "kind": "policy_fact", "cited_fact_ids": [fid]}],
    }
    client = FakeClient(json.dumps(out))
    g = pipeline.run_rag(REQ, client)
    assert g.run.status == "ok" and g.run.config_id == "B" and g.run.kb_version
    fact = next(f for f in INDEX.facts if f.fact_id == fid)
    assert g.claims[0].sources == [fact.source.url]
    assert f"[{fid}]" in client.calls[0][0]["content"]  # evidence in the prompt


def test_rag_rejects_citation_outside_bundle_then_fails_closed() -> None:
    out = {
        **VALID,
        "claims": [
            {
                "claim_id": "c1",
                "text": "x",
                "kind": "policy_fact",
                "cited_fact_ids": ["ZZ-NOPE-001"],
            }
        ],
    }
    g = pipeline.run_rag(REQ, FakeClient(json.dumps(out), json.dumps(out)))
    assert g.run.status == "failed" and g.claims == []


def test_uncited_policy_claim_becomes_evidence_gap() -> None:
    out = {
        **VALID,
        "claims": [
            {"claim_id": "c1", "text": "Uncited rule.", "kind": "policy_fact", "cited_fact_ids": []}
        ],
    }
    g = pipeline.run_rag(REQ, FakeClient(json.dumps(out)))
    gaps = [e for e in g.evidence_gaps if e.kind == "claim_uncited"]
    assert gaps and gaps[0].claim_id == "c1"


def test_hfe_question_shows_learning_resources_only_as_links() -> None:
    g = pipeline.run_rag(REQ, FakeClient(json.dumps(VALID)))
    assert g.visual_resources and all(v.evidence is False for v in g.visual_resources)
