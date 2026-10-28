"""Claim-level verification (stage 7, D-034): deterministic checks first, then ONE batched
LLM judge for the remaining claims. Display policy (D-011):
  supported            -> show with its official source
  contradicted         -> withhold the claim and flag that something was withheld
  insufficient_evidence -> show only as "unconfirmed", without a source, plus an evidence gap
Claims are never rewritten and there is no regeneration. The original claims, the verdicts
and the judge's raw response are all kept.

Which claims are checked (D-065): every `policy_fact`, and any `preparation_step` that cites
a fact. Caveats and uncited procedural steps are not factual assertions about policy, so
they pass through unverified.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from pydantic import ValidationError

from bto_buddy.generation import PROMPT_DIR, strict_json_schema
from bto_buddy.llm import LLMClient, LLMError, estimate_cost_usd
from bto_buddy.schemas import (
    DisplayedClaim,
    EvidenceBundle,
    EvidenceGap,
    FinalGuidance,
    GeneratedClaim,
    JudgeOutput,
    UserRequest,
    VerificationResult,
)

VERIFY_PROMPT = "verify_v1"
_ACTION = {
    "supported": "show_with_source",
    "contradicted": "withhold_and_flag",
    "insufficient_evidence": "state_as_unconfirmed",
}


@dataclass
class VerifierRecord:
    """What the verifier did, for the prediction file (raw judge output kept)."""

    results: list[VerificationResult] = field(default_factory=list)
    judge_raw: dict[str, Any] | None = None
    judge_error: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    latency_ms: int = 0
    llm_calls: int = 0


def checkable(c: GeneratedClaim) -> bool:
    return c.kind == "policy_fact" or (c.kind == "preparation_step" and bool(c.cited_fact_ids))


def _result(c: GeneratedClaim, outcome: str, method: str, why: str) -> VerificationResult:
    return VerificationResult(
        claim_id=c.claim_id,
        outcome=outcome,
        method=method,
        checked_fact_ids=list(c.cited_fact_ids),
        rationale=why,
        display_action=_ACTION[outcome],
    )


def deterministic_check(c: GeneratedClaim, bundle: EvidenceBundle) -> VerificationResult | None:
    """A hit decides the outcome without the LLM; None means 'send to the judge'."""
    if not c.cited_fact_ids:
        return _result(c, "insufficient_evidence", "deterministic", "No fact cited.")
    known = {e.fact_id for e in bundle.items}
    outside = [f for f in c.cited_fact_ids if f not in known]
    if outside:
        return _result(
            c, "insufficient_evidence", "deterministic", f"Cites facts not retrieved: {outside}"
        )
    return None


def judge_messages(
    request: UserRequest, claims: list[GeneratedClaim], bundle: EvidenceBundle
) -> list[dict[str, str]]:
    by_id = {e.fact_id: e for e in bundle.items}
    facts = sorted({f for c in claims for f in c.cited_fact_ids})
    fact_lines = []
    for f in facts:
        e = by_id[f]
        exc = f" Exceptions: {'; '.join(e.exceptions)}" if e.exceptions else ""
        fact_lines.append(f"[{f}] {e.statement}{exc}")
    claim_lines = [f"{c.claim_id} (cites {', '.join(c.cited_fact_ids)}): {c.text}" for c in claims]
    user = (
        f"<applicant_situation>\n{request.situation_text}\n</applicant_situation>\n\n"
        "<facts>\n" + "\n".join(fact_lines) + "\n</facts>\n\n"
        "<claims>\n" + "\n".join(claim_lines) + "\n</claims>"
    )
    system = (PROMPT_DIR / f"{VERIFY_PROMPT}.md").read_text()
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def verify(
    request: UserRequest, claims: list[GeneratedClaim], bundle: EvidenceBundle, client: LLMClient
) -> VerifierRecord:
    rec = VerifierRecord()
    pending: list[GeneratedClaim] = []
    decided: dict[str, VerificationResult] = {}
    for c in claims:
        if not checkable(c):
            continue
        hit = deterministic_check(c, bundle)
        if hit is not None:
            decided[c.claim_id] = hit
        else:
            pending.append(c)
    if pending:
        rec.llm_calls = 1
        try:
            resp = client.complete(
                judge_messages(request, pending, bundle),
                "claim_verdicts",
                strict_json_schema(JudgeOutput),
            )
            rec.judge_raw = resp.raw
            rec.input_tokens, rec.output_tokens = resp.input_tokens, resp.output_tokens
            rec.reasoning_tokens, rec.latency_ms = resp.reasoning_tokens, resp.latency_ms
            verdicts = {
                v.claim_id: v for v in JudgeOutput.model_validate_json(resp.content).verdicts
            }
        except (LLMError, ValidationError) as e:
            # Fail closed: an unverifiable claim is shown only as unconfirmed.
            rec.judge_error = f"{type(e).__name__}: {str(e)[:500]}"
            if isinstance(e, LLMError):
                rec.judge_raw = e.raw
            verdicts = {}
        for c in pending:
            v = verdicts.get(c.claim_id)
            if v is None:
                why = "Judge returned no verdict." if rec.judge_error is None else rec.judge_error
                decided[c.claim_id] = _result(c, "insufficient_evidence", "llm_judge", why)
            else:
                decided[c.claim_id] = _result(c, v.outcome, "llm_judge", v.rationale)
    rec.results = [decided[c.claim_id] for c in claims if c.claim_id in decided]
    return rec


def apply_verification(
    pre: FinalGuidance, request: UserRequest, bundle: EvidenceBundle, client: LLMClient
) -> tuple[FinalGuidance, VerifierRecord]:
    """D = the given pre-verification guidance + verification. Takes B's output unchanged, so a
    B-vs-D comparison isolates verification (no new generation)."""
    if pre.run.status == "failed":
        rec = VerifierRecord()
        return pre.model_copy(update={"run": pre.run.model_copy(update={"config_id": "D"})}), rec
    claims = [d.claim for d in pre.claims]
    rec = verify(request, claims, bundle, client)
    by_claim = {r.claim_id: r for r in rec.results}
    displayed, gaps = [], [g for g in pre.evidence_gaps if g.kind != "claim_uncited"]
    for d in pre.claims:
        r = by_claim.get(d.claim.claim_id)
        sources = d.sources if r is None or r.outcome == "supported" else []
        displayed.append(DisplayedClaim(claim=d.claim, verification=r, sources=sources))
        if r is not None and r.outcome != "supported":
            withheld = r.outcome == "contradicted"
            gaps.append(
                EvidenceGap(
                    topic=None,
                    claim_id=d.claim.claim_id,
                    kind="claim_uncited" if not d.claim.cited_fact_ids else "claim_unsupported",
                    detail=(
                        "A statement was withheld because our sources contradict it."
                        if withheld
                        else f"Not confirmed by our sources: {d.claim.text}"
                    ),
                    official_source_url="https://www.hdb.gov.sg",
                )
            )
    run = pre.run
    tokens_in, tokens_out = (
        run.input_tokens + rec.input_tokens,
        run.output_tokens + rec.output_tokens,
    )
    new_run = run.model_copy(
        update={
            "config_id": "D",
            "prompt_versions": {**run.prompt_versions, "verify": VERIFY_PROMPT},
            "llm_calls": run.llm_calls + rec.llm_calls,
            "input_tokens": tokens_in,
            "output_tokens": tokens_out,
            "reasoning_tokens": run.reasoning_tokens + rec.reasoning_tokens,
            "latency_ms": run.latency_ms + rec.latency_ms,
            "estimated_cost_usd": estimate_cost_usd(run.model_id, tokens_in, tokens_out),
            "error": f"verifier: {rec.judge_error}" if rec.judge_error else run.error,
        }
    )
    return pre.model_copy(update={"claims": displayed, "evidence_gaps": gaps, "run": new_run}), rec


def record_json(rec: VerifierRecord) -> dict[str, Any]:
    out: dict[str, Any] = json.loads(
        json.dumps(
            {
                "results": [r.model_dump(mode="json") for r in rec.results],
                "judge_raw": rec.judge_raw,
                "judge_error": rec.judge_error,
                "input_tokens": rec.input_tokens,
                "output_tokens": rec.output_tokens,
                "latency_ms": rec.latency_ms,
                "llm_calls": rec.llm_calls,
            }
        )
    )
    return out
