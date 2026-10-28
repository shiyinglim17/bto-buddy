"""Configuration D plumbing (no network). The judge's semantic accuracy (negation, numbers,
exceptions, applicability) needs a real model and is evaluated on dev claims instead
(evaluation/results/*-D-dev/verifier_eval.json); here canned verdicts test that every
outcome is handled and displayed as D-011 requires."""

from __future__ import annotations

import json
from datetime import date
from typing import Any

from bto_buddy import pipeline, verification
from bto_buddy.llm import LLMError
from bto_buddy.schemas import UserRequest
from test_baseline import VALID, FakeClient

REQ = UserRequest(
    request_id="T-D",
    situation_text="We are an engaged Singapore Citizen couple, both first-timers.",
    question="How long is the HFE letter valid?",
    as_of=date(2026, 11, 1),
)
BUNDLE = pipeline.retrieve_for(REQ)
F1, F2 = BUNDLE.items[0].fact_id, BUNDLE.items[1].fact_id


def claim(cid: str, kind: str, cited: list[str], text: str = "x") -> dict[str, Any]:
    return {"claim_id": cid, "text": text, "kind": kind, "cited_fact_ids": cited}


GEN = {
    **VALID,
    "claims": [
        claim("c1", "policy_fact", [F1], "Valid for 9 months."),
        claim("c2", "policy_fact", [F2], "Valid for 12 months."),  # judge: contradicted
        claim("c3", "policy_fact", [F1], "Also covers resale."),  # judge: insufficient
        claim("c4", "policy_fact", [], "Uncited rule."),  # deterministic: insufficient
        claim("c5", "caveat", [], "Check hdb.gov.sg."),  # not checked
        claim("c6", "preparation_step", [], "Gather documents."),  # uncited step: not checked
    ],
}


def verdicts(**outcomes: str) -> str:
    return json.dumps(
        {"verdicts": [{"claim_id": c, "outcome": o, "rationale": "r"} for c, o in outcomes.items()]}
    )


def run_d(*judge: str | LLMError) -> Any:
    client = FakeClient(json.dumps(GEN), *judge)
    return pipeline.run_verified(REQ, client), client


def test_outcomes_map_to_display_actions_and_render() -> None:
    g, client = run_d(verdicts(c1="supported", c2="contradicted", c3="insufficient_evidence"))
    by = {d.claim.claim_id: d for d in g.claims}
    assert by["c1"].verification.display_action == "show_with_source" and by["c1"].sources
    assert by["c2"].verification.display_action == "withhold_and_flag" and not by["c2"].sources
    assert by["c3"].verification.display_action == "state_as_unconfirmed" and not by["c3"].sources
    assert by["c4"].verification.method == "deterministic"
    assert by["c5"].verification is None and by["c6"].verification is None
    text = pipeline.render_answer(g)
    assert "Valid for 12 months." not in text  # withheld claim never shown (REQ-VER-007)
    assert "withheld" in text and "Also covers resale. (Unconfirmed" in text
    assert g.run.config_id == "D" and g.run.llm_calls == 2
    assert g.run.prompt_versions["verify"] == verification.VERIFY_PROMPT
    # Only judge-bound claims (cited, in bundle) are sent to the judge.
    judge_user = client.calls[1][1]["content"]
    assert "c1 (cites" in judge_user and "c4" not in judge_user and "c5" not in judge_user


def test_original_claims_are_never_rewritten() -> None:
    g, _ = run_d(verdicts(c1="supported", c2="contradicted", c3="insufficient_evidence"))
    assert [d.claim.text for d in g.claims] == [c["text"] for c in GEN["claims"]]


def test_judge_failure_fails_closed_to_unconfirmed() -> None:
    g, _ = run_d(LLMError("timeout", "slow"))
    checked = [d for d in g.claims if d.verification is not None]
    assert all(d.verification.outcome == "insufficient_evidence" for d in checked)
    assert all(not d.sources for d in checked)
    assert g.run.error and g.run.error.startswith("verifier:")


def test_missing_verdict_is_insufficient() -> None:
    g, _ = run_d(verdicts(c1="supported"))
    by = {d.claim.claim_id: d for d in g.claims}
    assert by["c2"].verification.outcome == "insufficient_evidence"
    assert by["c3"].verification.rationale == "Judge returned no verdict."


def test_failed_generation_stays_failed_without_judge_call() -> None:
    client = FakeClient("bad", "bad")
    g = pipeline.run_verified(REQ, client)
    assert g.run.status == "failed" and g.run.config_id == "D" and len(client.calls) == 2


def test_citation_outside_bundle_is_insufficient_deterministically() -> None:
    from bto_buddy.schemas import GeneratedClaim

    c = GeneratedClaim(claim_id="x", text="t", kind="policy_fact", cited_fact_ids=["ZZ-NO-001"])
    r = verification.deterministic_check(c, BUNDLE)
    assert r is not None and r.outcome == "insufficient_evidence"
