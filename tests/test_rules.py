"""Rule registry: interpreter semantics, boundary cases and consistency with the KB."""

import copy
from datetime import date
from typing import Any

import pytest

from bto_buddy import policy
from bto_buddy.schemas import RuleResult

AS_OF = date(2026, 11, 1)


@pytest.fixture(scope="module")
def reg() -> policy.Registry:
    return policy.load_rules()


@pytest.fixture(scope="module")
def kb() -> policy.KnowledgeBase:
    return policy.load_kb()


def couple(**over: Any) -> dict[str, Any]:
    """A fully specified fictional engaged SC/SC first-timer couple."""
    base: dict[str, Any] = {
        "relationship": "engaged",
        "applicant_1.age": 28,
        "applicant_2.age": 27,
        "applicant_1.citizenship": "SC",
        "applicant_2.citizenship": "SC",
        "applicant_1.prior_flat_or_subsidy": False,
        "applicant_2.prior_flat_or_subsidy": False,
        "applicant_1.employment": "employed_with_cpf",
        "applicant_2.employment": "self_employed",
        "applicant_1.job_count": 1,
        "applicant_2.job_count": 1,
        "hfe_status": "not_started",
        "hfe_issue_date": None,
        "private_property_interest": False,
        "children_or_expecting": False,
    }
    base.update(over)
    return base


def run(
    reg: policy.Registry, rule_id: str, values: dict[str, Any], as_of: date = AS_OF
) -> RuleResult:
    (result,) = [
        policy.evaluate_rule(r, policy.derive(values, as_of), reg)
        for r in reg.rules
        if r["rule_id"] == rule_id
    ]
    return result


# ---------------------------------------------------------------- interpreter ------------
@pytest.mark.parametrize(
    ("cond", "values", "expected"),
    [
        ({"field": "x", "eq": 1}, {"x": 1}, True),
        ({"field": "x", "ne": 1}, {"x": 1}, False),
        ({"field": "x", "lt": 21}, {"x": 20}, True),
        ({"field": "x", "lt": 21}, {"x": 21}, False),
        ({"field": "x", "gte": 21}, {"x": 21}, True),
        ({"field": "x", "in": ["a", "b"]}, {"x": "c"}, False),
        ({"field": "x", "is_null": True}, {}, True),
        ({"field": "x", "is_null": False}, {}, False),
        ({"field": "x", "eq": 1}, {}, None),
        ({"all": [{"field": "x", "eq": 1}, {"field": "y", "eq": 1}]}, {"x": 0}, False),
        ({"all": [{"field": "x", "eq": 1}, {"field": "y", "eq": 1}]}, {"x": 1}, None),
        ({"any": [{"field": "x", "eq": 1}, {"field": "y", "eq": 1}]}, {"x": 1}, True),
        ({"any": [{"field": "x", "eq": 1}, {"field": "y", "eq": 1}]}, {"x": 0}, None),
        ({"any": [{"field": "x", "eq": 1}, {"field": "y", "eq": 1}]}, {"x": 0, "y": 0}, False),
    ],
)
def test_three_valued_logic(cond: dict, values: dict, expected: bool | None) -> None:
    assert policy.evaluate(cond, values)[0] is expected


def test_unknown_reports_the_missing_fields_only() -> None:
    cond = {
        "all": [
            {"field": "x", "eq": 1},
            {"any": [{"field": "y", "eq": 1}, {"field": "z", "eq": 1}]},
        ]
    }
    assert policy.evaluate(cond, {"x": 1, "y": 0}) == (None, {"z"})


@pytest.mark.parametrize(
    "bad", [{"field": "x", "eval": "1"}, {"field": "x", "eq": 1, "lt": 2}, {"field": "x"}]
)
def test_non_whitelisted_conditions_are_rejected(bad: dict) -> None:
    with pytest.raises(ValueError):
        policy.evaluate(bad, {"x": 1})


def test_add_months_clamps_to_month_end() -> None:
    assert policy.add_months(date(2026, 5, 31), 9) == date(2027, 2, 28)
    assert policy.add_months(date(2027, 5, 31), 9) == date(2028, 2, 29)
    assert policy.add_months(date(2026, 1, 15), 9) == date(2026, 10, 15)


# ---------------------------------------------------------------- boundary cases ---------
@pytest.mark.parametrize(("age", "status"), [(20, "applies"), (21, "not_applicable")])
def test_engaged_under_21_boundary(reg: policy.Registry, age: int, status: str) -> None:
    assert run(reg, "R-HH-002", couple(**{"applicant_2.age": age})).status == status


def test_missing_age_is_never_assumed(reg: policy.Registry) -> None:
    r = run(reg, "R-HH-002", couple(**{"applicant_2.age": None}))
    assert r.status == "cannot_determine" and r.missing_fields == ["applicant_2.age"]
    assert r.preparation_step is None


def test_one_known_under_21_partner_is_enough(reg: policy.Registry) -> None:
    r = run(reg, "R-HH-002", couple(**{"applicant_1.age": 19, "applicant_2.age": None}))
    assert r.status == "applies"


def test_married_under_21_is_flagged_not_decided(reg: policy.Registry) -> None:
    r = run(reg, "R-HH-003", couple(relationship="married", **{"applicant_1.age": 20}))
    assert r.status == "applies" and r.requires_human_review and r.kind == "caution"
    assert (
        run(reg, "R-HH-002", couple(relationship="married", **{"applicant_1.age": 20})).status
        == "not_applicable"
    )


ISSUE = date(2026, 3, 10)  # expiry under the I-02 convention: 2026-12-10


@pytest.mark.parametrize(
    ("as_of", "near", "expired"),
    [
        (date(2026, 11, 9), "not_applicable", "not_applicable"),  # 31 days left
        (date(2026, 11, 10), "applies", "not_applicable"),  # 30 days left
        (date(2026, 12, 10), "applies", "not_applicable"),  # expiry day
        (date(2026, 12, 11), "not_applicable", "applies"),  # 1 day after
    ],
)
def test_hfe_expiry_boundaries(reg: policy.Registry, as_of: date, near: str, expired: str) -> None:
    values = couple(hfe_status="issued", hfe_issue_date=ISSUE)
    assert run(reg, "R-HFE-003", values, as_of).status == near
    assert run(reg, "R-HFE-004", values, as_of).status == expired


def test_expiry_needs_the_issue_date(reg: policy.Registry) -> None:
    r = run(reg, "R-HFE-003", couple(hfe_status="issued"))
    assert r.status == "cannot_determine" and r.missing_fields == ["hfe_issue_date"]
    assert run(reg, "R-HFE-003", couple(hfe_status="not_started")).status == "not_applicable"


def test_expiry_rules_carry_their_interpretation(reg: policy.Registry) -> None:
    r = run(reg, "R-HFE-003", couple(hfe_status="issued", hfe_issue_date=ISSUE), date(2026, 12, 1))
    assert r.requires_human_review and any(n.startswith("I-02") for n in r.notes)


def test_hfe_letter_required_until_issued(reg: policy.Registry) -> None:
    assert run(reg, "R-APP-001", couple(hfe_status="applied")).status == "applies"
    assert run(reg, "R-APP-001", couple(hfe_status="issued")).status == "not_applicable"
    assert run(reg, "R-APP-001", couple(hfe_status=None)).missing_fields == ["hfe_status"]


@pytest.mark.parametrize(("age", "flagged"), [(34, True), (35, False)])
def test_non_resident_spouse_age_exception(reg: policy.Registry, age: int, flagged: bool) -> None:
    values = couple(
        relationship="married",
        **{"applicant_1.age": age, "applicant_2.citizenship": "non_resident"},
    )
    r = run(reg, "R-HH-005", values)
    assert r.status == "applies"
    assert any(n.startswith("X-NR-AGE") for n in r.notes) is flagged
    assert r.requires_human_review is flagged


def test_unknown_exception_input_asks_instead_of_assuming(reg: policy.Registry) -> None:
    values = couple(
        relationship="married",
        children_or_expecting=None,
        **{"applicant_2.citizenship": "non_resident"},
    )
    r = run(reg, "R-HH-005", values)
    assert r.status == "cannot_determine" and r.missing_fields == ["children_or_expecting"]


def test_engaged_non_resident_partner_is_an_evidence_gap(reg: policy.Registry) -> None:
    values = couple(**{"applicant_1.citizenship": "non_resident"})
    gap = run(reg, "R-GAP-U03", values)
    assert gap.status == "applies" and gap.kind == "evidence_gap" and gap.requires_human_review
    assert run(reg, "R-HH-005", values).status == "not_applicable"  # spouse route not inferred


@pytest.mark.parametrize(("age", "flag"), [(40, False), (41, True)])
def test_ftpmc_age_boundary_and_interpretation(reg: policy.Registry, age: int, flag: bool) -> None:
    r = run(reg, "R-PRI-002", couple(relationship="married", **{"applicant_1.age": age}))
    assert r.status == "applies" and r.requires_human_review  # I-01/I-08 always reviewed
    assert any(n.startswith("X-I01") for n in r.notes) is flag


def test_ftpmc_not_suggested_when_a_partner_is_second_timer(reg: policy.Registry) -> None:
    values = couple(relationship="married", **{"applicant_2.prior_flat_or_subsidy": True})
    assert run(reg, "R-PRI-002", values).status == "not_applicable"
    assert run(reg, "R-HH-007", values).status == "applies"
    assert run(reg, "R-NS-001", values).status == "applies"  # still a first-timer family


def test_engaged_couple_priority_is_unconfirmed(reg: policy.Registry) -> None:
    assert run(reg, "R-PRI-002", couple()).status == "not_applicable"
    assert run(reg, "R-PRI-003", couple(children_or_expecting=True)).status == "not_applicable"
    assert run(reg, "R-GAP-U02", couple()).kind == "evidence_gap"


def test_engaged_couple_household_change_flags_u01(reg: policy.Registry) -> None:
    r = run(reg, "R-HFE-005", couple(hfe_status="issued"))
    assert r.requires_human_review and any(n.startswith("X-U01") for n in r.notes)
    married = run(reg, "R-HFE-005", couple(relationship="married", hfe_status="issued"))
    assert not married.requires_human_review


@pytest.mark.parametrize(("jobs", "status"), [(1, "not_applicable"), (2, "applies")])
def test_multiple_jobs_boundary(reg: policy.Registry, jobs: int, status: str) -> None:
    assert run(reg, "R-DOC-002", couple(**{"applicant_2.job_count": jobs})).status == status


def test_unrecognised_employment_status_is_not_guessed(reg: policy.Registry) -> None:
    r = run(reg, "R-DOC-001", couple(**{"applicant_1.employment": None}))
    assert r.status == "cannot_determine" and r.missing_fields == ["applicant_1.employment"]


# ---------------------------------------------------------------- whole registry ---------
PROFILES = [
    couple(),
    couple(
        relationship="married",
        children_or_expecting=True,
        hfe_status="issued",
        hfe_issue_date=date(2026, 2, 1),
    ),
    couple(**{k: None for k in couple()}),
    couple(
        relationship="married",
        **{"applicant_1.citizenship": "SPR", "applicant_2.citizenship": "SPR"},
    ),
]


@pytest.mark.parametrize("values", PROFILES)
def test_result_contract_invariants(reg: policy.Registry, values: dict[str, Any]) -> None:
    for r in policy.evaluate_rules(reg, values, AS_OF):
        if r.status == "applies":
            assert r.preparation_step
        else:
            assert r.preparation_step is None
        if r.status == "cannot_determine":
            assert r.missing_fields
        assert r.source_fact_ids


def test_empty_profile_never_applies_a_rule(reg: policy.Registry) -> None:
    results = policy.evaluate_rules(reg, {}, AS_OF)
    assert {r.status for r in results} == {"cannot_determine"}


def test_topic_filter(reg: policy.Registry) -> None:
    results = policy.evaluate_rules(reg, couple(), AS_OF, topics={"non_selection"})
    assert {r.rule_id for r in results} == {"R-NS-001", "R-NS-002"}


def test_registry_is_consistent_with_the_kb(reg: policy.Registry, kb: policy.KnowledgeBase) -> None:
    assert policy.validate_registry(reg, kb) == []
    core_limited = {
        "household_composition",
        "application_requirements",
        "hfe_process",
        "hfe_documents",
        "priority_considerations",
        "non_selection",
    }
    assert core_limited <= {t for r in reg.rules for t in r["topics"]}


def _mutated(reg: policy.Registry, **changes: Any) -> policy.Registry:
    rules = copy.deepcopy(list(reg.rules))
    rules[0].update(changes)
    return policy.Registry(reg.rules_version, reg.kb_version, reg.fields, reg.derived, tuple(rules))


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"source_fact_ids": ["NOPE-X-001"]}, "unknown fact"),
        ({"source_fact_ids": ["HH-PROP-002"]}, "not verified"),
        ({"when": {"field": "salary", "gte": 1}}, "unknown field"),
        ({"when": {"field": "hfe_status", "eq": "lost"}}, "not in"),
        ({"when": {"field": "hfe_status", "matches": "x"}}, "operator"),
        ({"action": "You are eligible for a flat."}, "verdict"),
        ({"basis": "interpretation", "requires_human_review": False}, "human review"),
        ({"topics": ["ballot_odds"]}, "not in scope"),
        ({"sources": []}, "official URL"),
        ({"effective": {"from": "2026-01-01", "to": None}}, "effective dates"),
    ],
)
def test_validator_catches_inconsistencies(
    reg: policy.Registry, kb: policy.KnowledgeBase, changes: dict, message: str
) -> None:
    errors = policy.validate_registry(_mutated(reg, **changes), kb)
    assert any(message in e for e in errors), errors


def test_rules_reference_only_reviewer_accessible_metadata(reg: policy.Registry) -> None:
    for r in reg.rules:
        for s in r["sources"]:
            assert s["url"].startswith(("https://www.hdb.gov.sg/", "https://file.go.gov.sg/"))
        assert "private_corpus" not in str(r) and "passage" not in str(r)
