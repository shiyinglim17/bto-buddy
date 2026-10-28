"""Composes configurations into one `FinalGuidance` contract (D-030, D-035).

Only configuration A (direct LLM) exists so far. B-D reuse `generation.generate` with their
evidence block and add the pure stages; this module is the only place that knows about
configurations (architecture §11.2).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from bto_buddy import policy, retrieval
from bto_buddy.generation import GENERATE_PROMPT, NO_EVIDENCE, GenerationResult, generate
from bto_buddy.llm import LLMClient, estimate_cost_usd
from bto_buddy.schemas import (
    CoverageDecision,
    DisplayedClaim,
    EvidenceBundle,
    EvidenceGap,
    FinalGuidance,
    GenerationOutput,
    RunMetadata,
    UserRequest,
    VisualResource,
)

ConfigId = Literal["A", "B", "C", "D"]

DISCLAIMER = (
    "BTO Buddy gives preparation guidance for fictional first-timer couple profiles. It is "
    "not an official HDB eligibility assessment. Confirm everything on the HDB website or "
    "the HDB Flat Portal before acting."
)
# D-021: A uses no policy sources, so the period is the model's own knowledge.
POLICY_PERIOD_A = "No policy sources used: the model's pretrained knowledge only (unverified)."
FAILURE_SUMMARY = (
    "BTO Buddy could not produce guidance for this request because of a technical error. "
    "Please try again later, or check https://www.hdb.gov.sg directly."
)


def run(request: UserRequest, config_id: ConfigId, client: LLMClient) -> FinalGuidance:
    if config_id == "A":
        return run_direct(request, client)
    if config_id == "B":
        return run_rag(request, client)
    if config_id == "D":
        return run_verified(request, client)
    raise NotImplementedError(f"configuration {config_id} is not built (D-069)")


def retrieve_for(request: UserRequest, k: int = retrieval.DEFAULT_K) -> EvidenceBundle:
    """B's retrieval step; deterministic, so D can rebuild B's exact bundle."""
    return retrieval.retrieve(get_index(), f"{request.question} {request.situation_text}", k)


def run_verified(request: UserRequest, client: LLMClient) -> FinalGuidance:
    """Configuration D as built (D-071): B's output plus claim verification. The approved
    design runs the verifier on C; C is not built, so D here isolates verification on B."""
    from bto_buddy.verification import apply_verification

    pre = run_rag(request, client)
    return apply_verification(pre, request, retrieve_for(request), client)[0]


_INDEX: retrieval.Index | None = None


def get_index() -> retrieval.Index:
    """Built once per process from the tracked KB; deterministic."""
    global _INDEX
    if _INDEX is None:
        _INDEX = retrieval.build_index(policy.load_kb())
    return _INDEX


def run_rag(request: UserRequest, client: LLMClient, k: int = retrieval.DEFAULT_K) -> FinalGuidance:
    """Configuration B: BM25 over the authored KB (question + situation), the retrieved facts
    in the shared prompt's evidence slot, citations restricted to the bundle."""
    started = datetime.now(UTC)
    bundle = retrieve_for(request, k)
    allowed = frozenset(e.fact_id for e in bundle.items)
    result = generate(
        request, client, evidence=retrieval.evidence_block(bundle), allowed_fact_ids=allowed
    )
    out = result.output or GenerationOutput(summary=FAILURE_SUMMARY, claims=[])
    by_id = {e.fact_id: e for e in bundle.items}
    claims = [
        DisplayedClaim(
            claim=c,
            verification=None,
            sources=sorted({by_id[f].source_url for f in c.cited_fact_ids}, key=str),
        )
        for c in out.claims
    ]
    return FinalGuidance(
        request_id=request.request_id,
        coverage=_coverage_from_model(out),
        summary=out.summary,
        claims=claims,
        preparation_steps=[],
        missing_profile_fields=out.missing_profile_fields,
        profile_conflicts=out.profile_conflicts,
        evidence_gaps=[*bundle.evidence_gaps, *_uncited_gaps(out, bundle)],
        out_of_scope_reasons=out.out_of_scope_reasons,
        visual_resources=visual_resources_for(request),
        policy_period=f"Sources retrieved 2026-10-28 ({bundle.kb_version})",
        disclaimer=DISCLAIMER,
        run=_metadata("B", client, result, started, kb_version=bundle.kb_version),
    )


def _uncited_gaps(out: GenerationOutput, bundle: EvidenceBundle) -> list[EvidenceGap]:
    """A policy claim with no citation is not shown as established (REQ-ARC-014). This is a
    report rule, not verification: it never judges whether a cited fact supports the claim."""
    return [
        EvidenceGap(
            topic=None,
            claim_id=c.claim_id,
            kind="claim_uncited",
            detail=f"Not confirmed by our sources: {c.text}",
            official_source_url="https://www.hdb.gov.sg",
        )
        for c in out.claims
        if c.kind == "policy_fact" and not c.cited_fact_ids
    ]


# Learning resources (links only, never evidence). Shown when the question mentions the HFE;
# a keyword match keeps this deterministic until C's topic tags exist.
def visual_resources_for(request: UserRequest) -> list[VisualResource]:
    text = f"{request.question} {request.situation_text}".lower()
    if "hfe" not in text and "eligibility letter" not in text:
        return []
    return [v for v in policy.load_visual_resources() if v.kind in ("infographic", "video")]


def run_direct(request: UserRequest, client: LLMClient) -> FinalGuidance:
    """Configuration A: the profile and question go straight to the model. No extraction,
    gate, rules, retrieval or verification; the model fills the signal lists itself (A6)."""
    started = datetime.now(UTC)
    result = generate(request, client, evidence=NO_EVIDENCE, allowed_fact_ids=frozenset())
    out = result.output
    if out is None:
        # Fail closed: keep the failed case with empty content (metric_spec §7).
        out = GenerationOutput(summary=FAILURE_SUMMARY, claims=[])
    return FinalGuidance(
        request_id=request.request_id,
        coverage=_coverage_from_model(out),
        summary=out.summary,
        claims=[DisplayedClaim(claim=c, verification=None, sources=[]) for c in out.claims],
        preparation_steps=[],
        missing_profile_fields=out.missing_profile_fields,
        profile_conflicts=out.profile_conflicts,
        evidence_gaps=[],
        out_of_scope_reasons=out.out_of_scope_reasons,
        visual_resources=visual_resources_for(request),  # display-only links
        policy_period=POLICY_PERIOD_A,
        disclaimer=DISCLAIMER,
        run=_metadata("A", client, result, started),
    )


def _coverage_from_model(out: GenerationOutput) -> CoverageDecision:
    """A has no gate, so coverage only restates the model's own out-of-scope reasons.
    supported_topics stays empty because A does not tag topics."""
    substantive = any(c.kind != "caveat" for c in out.claims)
    if not out.out_of_scope_reasons:
        status: Literal["in_scope", "partially_in_scope", "out_of_scope"] = "in_scope"
    else:
        status = "partially_in_scope" if substantive else "out_of_scope"
    return CoverageDecision(
        status=status, supported_topics=[], out_of_scope_reasons=out.out_of_scope_reasons
    )


def _metadata(
    config_id: ConfigId,
    client: LLMClient,
    result: GenerationResult,
    started: datetime,
    kb_version: str | None = None,
) -> RunMetadata:
    a = result.attempts
    tokens_in = sum(x.input_tokens for x in a)
    tokens_out = sum(x.output_tokens for x in a)
    return RunMetadata(
        config_id=config_id,
        model_id=client.model_id,
        prompt_versions={"generate": GENERATE_PROMPT},
        temperature=client.temperature,
        reasoning_effort=client.reasoning_effort,
        kb_version=kb_version,
        rules_version=None,
        started_at=started,
        llm_calls=len(a),
        input_tokens=tokens_in,
        output_tokens=tokens_out,
        reasoning_tokens=sum(x.reasoning_tokens for x in a),
        latency_ms=sum(x.latency_ms for x in a),
        cache_hits=0,  # no response cache yet; saved predictions are the reproducible record
        estimated_cost_usd=estimate_cost_usd(client.model_id, tokens_in, tokens_out),
        status="ok" if result.output is not None else "failed",
        error=result.error,
    )


def render_answer(g: FinalGuidance) -> str:
    """The user-visible answer as plain text: one template for every configuration, so blind
    scoring (metric_spec §3) sees no structural difference except D's withheld notices."""
    lines = [g.summary, ""]
    shown = [
        d
        for d in g.claims
        if d.verification is None or d.verification.display_action != "withhold_and_flag"
    ]
    if shown:
        lines.append("Guidance:")
        for d in shown:
            unconfirmed = (
                d.verification is not None
                and d.verification.display_action == "state_as_unconfirmed"
            )
            prefix = "Note: " if d.claim.kind == "caveat" else ""
            suffix = " (Unconfirmed by our sources.)" if unconfirmed else ""
            src = f" [Source: {', '.join(str(u) for u in d.sources)}]" if d.sources else ""
            lines.append(f"- {prefix}{d.claim.text}{suffix}{src}")
        lines.append("")
    withheld = len(g.claims) - len(shown)
    if withheld:
        lines += [f"{withheld} statement(s) were withheld because our sources contradict them.", ""]
    if g.missing_profile_fields:
        lines.append("We need a bit more information:")
        lines += [f"- {m.follow_up_question}" for m in g.missing_profile_fields]
        lines.append("")
    if g.profile_conflicts:
        lines.append("Please clarify:")
        lines += [f"- {c.clarification_question}" for c in g.profile_conflicts]
        lines.append("")
    if g.out_of_scope_reasons:
        lines.append("Outside what BTO Buddy covers:")
        for o in g.out_of_scope_reasons:
            url = f" See {o.redirect_url}" if o.redirect_url else ""
            lines.append(f"- {o.detail}{url}")
        lines.append("")
    if g.evidence_gaps:
        lines.append("We could not confirm from our sources:")
        for e in g.evidence_gaps:
            url = f" Check {e.official_source_url}" if e.official_source_url else ""
            lines.append(f"- {e.detail}{url}")
        lines.append("")
    lines.append(g.disclaimer)
    return "\n".join(lines).strip() + "\n"
