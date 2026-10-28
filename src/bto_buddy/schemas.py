"""Typed contracts (architecture §5). This module imports nothing from the package.

Contracts are added when their stages are built, so nothing here is an unused stub. So far:
knowledge base, rules, and the request/generation/report contracts used by configuration A
(direct LLM). Extraction, evidence and verification-input contracts come with B-D.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class Tier(StrEnum):
    CORE = "core"
    LIMITED = "limited"
    CONTEXT = "context"
    EXCLUDED = "excluded"


class Topic(StrEnum):
    # in scope (tier fixed by D-008)
    HOUSEHOLD_COMPOSITION = "household_composition"
    APPLICATION_REQUIREMENTS = "application_requirements"
    HFE_PROCESS = "hfe_process"
    HFE_DOCUMENTS = "hfe_documents"
    PRIORITY_CONSIDERATIONS = "priority_considerations"
    NON_SELECTION = "non_selection"
    HFE_GRANT_LOAN_CONTEXT = "hfe_grant_loan_context"
    # excluded (D-008): handled by the coverage gate, never by facts
    GRANT_LOAN_CALCULATION = "grant_loan_calculation"
    FINANCING_AFFORDABILITY = "financing_affordability"
    BALLOT_ODDS = "ballot_odds"
    POST_PURCHASE = "post_purchase"
    ELIGIBILITY_DETERMINATION = "eligibility_determination"
    OTHER_HOUSING = "other_housing"
    UNRELATED = "unrelated"


# Single source of truth for the coverage gate and for fact tiers (D-008, REQ-SCP-012).
TOPIC_TIER: dict[Topic, Tier] = {
    Topic.HOUSEHOLD_COMPOSITION: Tier.CORE,
    Topic.APPLICATION_REQUIREMENTS: Tier.CORE,
    Topic.HFE_PROCESS: Tier.CORE,
    Topic.HFE_DOCUMENTS: Tier.CORE,
    Topic.PRIORITY_CONSIDERATIONS: Tier.LIMITED,
    Topic.NON_SELECTION: Tier.LIMITED,
    Topic.HFE_GRANT_LOAN_CONTEXT: Tier.CONTEXT,
    Topic.GRANT_LOAN_CALCULATION: Tier.EXCLUDED,
    Topic.FINANCING_AFFORDABILITY: Tier.EXCLUDED,
    Topic.BALLOT_ODDS: Tier.EXCLUDED,
    Topic.POST_PURCHASE: Tier.EXCLUDED,
    Topic.ELIGIBILITY_DETERMINATION: Tier.EXCLUDED,
    Topic.OTHER_HOUSING: Tier.EXCLUDED,
    Topic.UNRELATED: Tier.EXCLUDED,
}

FACT_ID_PATTERN = re.compile(r"^[A-Z]{2,4}-[A-Z0-9]+(-[A-Z0-9]+)*-\d{3}$")


class _Frozen(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SourceRef(_Frozen):
    """Where a fact comes from. Resolves through data/sources_manifest.json (D-006)."""

    source_id: str
    section_id: str  # L1 section ID, e.g. "S01.a.2"; stable while the snapshot hash holds
    section: str  # human-readable heading path on the official page
    url: HttpUrl  # official page (with ?anchor= where HDB provides one)
    locator: str | None = None  # e.g. table row or PDF page; authored, not quoted


class FactException(_Frozen):
    description: str
    fact_id: str | None = None  # the fact that states the exception in full, if any


class Validation(_Frozen):
    # draft -> snapshot_checked (agent, against the captured source) -> verified (developer,
    # against the live official page). Rejected facts are kept for audit, never used.
    status: Literal["draft", "snapshot_checked", "verified", "rejected"]
    method: str
    validated_at: date | None = None
    notes: str = ""


class RightsReview(_Frozen):
    # overlap_checked = local 8-word overlap check passed and read by the author (D-054);
    # cleared = developer's manual rights read before submission (REQ-LIC-015).
    status: Literal["pending", "overlap_checked", "cleared", "rejected"]
    max_shared_run_words: int | None = None
    notes: str = ""


class PolicyFact(_Frozen):
    """One independently authored, source-attributed policy fact (03 §2.5, D-023, D-031)."""

    fact_id: str
    statement: str = Field(min_length=20)
    topic: Topic
    scope_tier: Tier
    aliases: list[str] = []
    applies_to: dict[str, list[str]] = {}
    exceptions: list[FactException] = []
    source: SourceRef
    private_passage_ids: list[str] = []  # provenance only; never needed at runtime (D-006)
    retrieved_at: date
    page_last_updated: date | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    effective_date_note: str = ""
    critical: bool  # policy-critical: needs developer verification before use (D-058)
    validation: Validation
    rights_review: RightsReview
    kb_version: str

    @field_validator("fact_id")
    @classmethod
    def _fact_id_format(cls, v: str) -> str:
        if not FACT_ID_PATTERN.match(v):
            raise ValueError(f"fact_id {v!r} does not match {FACT_ID_PATTERN.pattern}")
        return v

    @field_validator("scope_tier")
    @classmethod
    def _not_excluded(cls, v: Tier) -> Tier:
        if v is Tier.EXCLUDED:
            raise ValueError("excluded topics are redirected by the gate, never stored as facts")
        return v

    def tier_matches_topic(self) -> bool:
        return TOPIC_TIER[self.topic] is self.scope_tier

    def usable(self) -> bool:
        """Runtime eligibility of the fact (D-058, PROPOSED).

        Critical facts must be developer-verified; others may be used once checked against the
        captured snapshot. Rights review must at least have passed the overlap check.
        """
        if self.validation.status == "rejected" or self.rights_review.status in (
            "pending",
            "rejected",
        ):
            return False
        if self.validation.status == "verified":
            return True
        return self.validation.status == "snapshot_checked" and not self.critical


class ManifestSource(BaseModel):
    """The subset of a data/sources_manifest.json record the runtime needs."""

    model_config = ConfigDict(extra="ignore", frozen=True)

    source_id: str
    title: str
    canonical_url: HttpUrl | None
    mvp_class: Literal["essential", "supporting", "context_only", "outside_mvp", "pending"]
    page_last_updated: date | None = None


class VisualResource(_Frozen):
    """An official infographic or video, shown as a link only (REQ-SRC-010/011, D-049)."""

    resource_id: str  # manifest media ID, e.g. "M03"
    kind: Literal["infographic", "video"]
    title: str
    url: HttpUrl  # official page or video; media files are never downloaded or embedded
    media_url: HttpUrl | None = None  # image location seen in the capture (provenance only)
    host_page_source_id: str
    topics: list[Topic] = Field(min_length=1)
    stages: list[str] = Field(min_length=1)
    display_when: str  # authored display condition, applied by the report stage
    evidence: Literal[False] = False  # never policy evidence


class RuleResult(_Frozen):
    """Outcome of one rule for one profile (architecture §5). Never an eligibility verdict."""

    rule_id: str
    rule_version: int
    status: Literal["applies", "not_applicable", "cannot_determine"]
    kind: Literal["preparation", "caution", "evidence_gap"]
    preparation_step: str | None  # only when status == "applies"
    source_fact_ids: list[str] = Field(min_length=1)
    missing_fields: list[str] = []  # required (non-empty) when cannot_determine
    requires_human_review: bool
    notes: list[str] = []  # triggered exception notes and interpretation caveats


# ---- request, generation and report (architecture §5; configuration A first) -------------
class ProfileField(StrEnum):
    """Addressable profile fields for missing/conflict reporting. Values match the benchmark's
    reference-profile keys, so missing-information recall needs no mapping."""

    RELATIONSHIP = "relationship"
    A1_AGE = "applicant_1.age"
    A2_AGE = "applicant_2.age"
    A1_CITIZENSHIP = "applicant_1.citizenship"
    A2_CITIZENSHIP = "applicant_2.citizenship"
    A1_PRIOR_HOUSING = "applicant_1.prior_flat_or_subsidy"
    A2_PRIOR_HOUSING = "applicant_2.prior_flat_or_subsidy"
    A1_EMPLOYMENT = "applicant_1.employment"
    A2_EMPLOYMENT = "applicant_2.employment"
    A1_JOB_COUNT = "applicant_1.job_count"  # D-062 (I-11)
    A2_JOB_COUNT = "applicant_2.job_count"
    HFE_STATUS = "hfe_status"
    HFE_ISSUE_DATE = "hfe_issue_date"
    PRIVATE_PROPERTY = "private_property_interest"
    HOUSING_LOAN_INTENT = "housing_loan_intent"
    CHILDREN = "children_or_expecting"


class UserRequest(_Frozen):
    request_id: str
    situation_text: str = Field(min_length=1)  # free text; fictional profiles only
    question: str = Field(min_length=1)
    # Reference date for date-dependent guidance (benchmark cases fix it; the app uses today).
    as_of: date


class MissingProfileField(_Frozen):
    field: ProfileField
    needed_for: list[str]  # topic values and/or rule IDs
    follow_up_question: str


class ProfileConflict(_Frozen):
    fields: list[ProfileField] = Field(min_length=1)
    kind: Literal["stated_contradiction", "logical_inconsistency"]
    detail: str
    quotes: list[str]
    clarification_question: str


class EvidenceGap(_Frozen):
    topic: Topic | None
    claim_id: str | None = None
    kind: Literal[
        "no_evidence_for_topic", "claim_uncited", "claim_unsupported", "fact_temporally_uncertain"
    ]
    detail: str
    official_source_url: HttpUrl | None = None


class OutOfScopeReason(_Frozen):
    code: Literal["excluded_topic", "unsupported_household_type", "unrecognised_question"]
    topic: Topic | None = None
    detail: str
    redirect_url: HttpUrl | None = None  # official service or page


class CoverageDecision(_Frozen):
    status: Literal["in_scope", "partially_in_scope", "out_of_scope"]
    supported_topics: list[Topic]
    out_of_scope_reasons: list[OutOfScopeReason]


class GeneratedClaim(_Frozen):
    claim_id: str
    text: str = Field(min_length=1)
    kind: Literal["policy_fact", "preparation_step", "caveat"]  # caveat = not checkable
    cited_fact_ids: list[str]


class GenerationOutput(_Frozen):
    """LLM #2 output. In A and B the model also fills the three signal lists, with the same
    enums that C and D fill deterministically (architecture §3.2, A6)."""

    summary: str
    claims: list[GeneratedClaim]
    missing_profile_fields: list[MissingProfileField] = []
    profile_conflicts: list[ProfileConflict] = []
    out_of_scope_reasons: list[OutOfScopeReason] = []


class VerificationResult(_Frozen):
    claim_id: str
    outcome: Literal["supported", "contradicted", "insufficient_evidence"]
    method: Literal["deterministic", "llm_judge"]
    checked_fact_ids: list[str]
    rationale: str
    display_action: Literal["show_with_source", "withhold_and_flag", "state_as_unconfirmed"]


class DisplayedClaim(_Frozen):
    claim: GeneratedClaim
    verification: VerificationResult | None  # None in A-C (no verifier)
    sources: list[HttpUrl]


class RunMetadata(_Frozen):
    config_id: Literal["A", "B", "C", "D"]
    model_id: str
    prompt_versions: dict[str, str]
    temperature: float
    reasoning_effort: str | None
    kb_version: str | None  # None when no KB is used (A)
    rules_version: str | None  # None when no rules are used (A, B)
    started_at: datetime
    llm_calls: int  # logical calls, including the one bounded validation retry
    input_tokens: int
    output_tokens: int  # includes reasoning tokens
    reasoning_tokens: int
    latency_ms: int
    cache_hits: int
    estimated_cost_usd: float | None  # list price at run time; None if the price is unknown
    # Failed runs are kept, never dropped or substituted (metric_spec §7).
    status: Literal["ok", "failed"]
    error: str | None = None


class FinalGuidance(_Frozen):
    """The one output contract for every configuration (D-035)."""

    request_id: str
    coverage: CoverageDecision
    summary: str
    claims: list[DisplayedClaim]
    preparation_steps: list[RuleResult]  # applies-only, C/D
    missing_profile_fields: list[MissingProfileField]
    profile_conflicts: list[ProfileConflict]
    evidence_gaps: list[EvidenceGap]
    out_of_scope_reasons: list[OutOfScopeReason]
    visual_resources: list[VisualResource]  # display-only links
    policy_period: str  # D-021
    disclaimer: str  # not an official eligibility assessment
    run: RunMetadata
