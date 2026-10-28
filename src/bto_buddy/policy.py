"""Pure policy domain: load and validate the reviewer-facing KB (architecture §11).

Reads only tracked files under data/ (L2/L3). Never reads data/private_corpus/ (D-005,
REQ-DAT-011/012) and never imports the LLM client.
"""

from __future__ import annotations

import calendar
import json
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from bto_buddy.schemas import (
    TOPIC_TIER,
    ManifestSource,
    PolicyFact,
    RuleResult,
    Tier,
    VisualResource,
)

# Repository data/ in development; the Docker image sets BTO_BUDDY_DATA_DIR=/app/data.
DATA = Path(os.environ.get("BTO_BUDDY_DATA_DIR") or Path(__file__).resolve().parents[2] / "data")
FACTS_PATH = DATA / "policy_facts.jsonl"
MANIFEST_PATH = DATA / "sources_manifest.json"
VISUALS_PATH = DATA / "visual_resources.json"
RULES_PATH = DATA / "policy_rules.yaml"
CITABLE = {"essential", "supporting", "context_only"}


class KBError(ValueError):
    """The knowledge base is inconsistent; the app must not start on it."""


@dataclass(frozen=True)
class KnowledgeBase:
    facts: tuple[PolicyFact, ...]
    sources: dict[str, ManifestSource]
    kb_version: str

    def usable_facts(self) -> tuple[PolicyFact, ...]:
        return tuple(f for f in self.facts if f.usable())

    def get(self, fact_id: str) -> PolicyFact:
        for f in self.facts:
            if f.fact_id == fact_id:
                return f
        raise KeyError(fact_id)


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, ManifestSource]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {s["source_id"]: ManifestSource.model_validate(s) for s in raw["sources"]}


def load_facts(path: Path = FACTS_PATH) -> list[PolicyFact]:
    facts = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            try:
                facts.append(PolicyFact.model_validate_json(line))
            except ValueError as e:  # pydantic.ValidationError subclasses ValueError
                raise KBError(f"{path.name}:{n}: {e}") from e
    return facts


def check_integrity(facts: list[PolicyFact], sources: dict[str, ManifestSource]) -> list[str]:
    """Reference integrity without the private corpus: every fact resolves to a citable
    manifest source and its official URL (REQ-SRC-002, REQ-DAT-012)."""
    errors: list[str] = []
    ids = [f.fact_id for f in facts]
    known = set(ids)
    errors += [f"duplicate fact_id {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    versions = {f.kb_version for f in facts}
    if len(versions) > 1:
        errors.append(f"mixed kb_version values: {sorted(versions)}")
    for f in facts:
        src = sources.get(f.source.source_id)
        if src is None:
            errors.append(f"{f.fact_id}: unknown source {f.source.source_id}")
            continue
        if src.mvp_class not in CITABLE:
            errors.append(f"{f.fact_id}: cites {src.source_id}, classed {src.mvp_class}")
        if src.canonical_url is None or not str(f.source.url).startswith(
            str(src.canonical_url).rstrip("/")
        ):
            errors.append(f"{f.fact_id}: url is not under {src.source_id}'s canonical URL")
        if not f.source.section_id.startswith(f"{src.source_id}."):
            errors.append(f"{f.fact_id}: section_id {f.source.section_id} not in {src.source_id}")
        if not f.tier_matches_topic():
            errors.append(f"{f.fact_id}: scope_tier {f.scope_tier} != tier of {f.topic}")
        for ex in f.exceptions:
            if ex.fact_id is not None and ex.fact_id not in known:
                errors.append(f"{f.fact_id}: exception cites unknown fact {ex.fact_id}")
    return errors


def load_kb(facts_path: Path = FACTS_PATH, manifest_path: Path = MANIFEST_PATH) -> KnowledgeBase:
    facts = load_facts(facts_path)
    sources = load_manifest(manifest_path)
    errors = check_integrity(facts, sources)
    if errors:
        raise KBError("; ".join(errors))
    version = facts[0].kb_version if facts else "empty"
    return KnowledgeBase(tuple(facts), sources, version)


def load_visual_resources(
    path: Path = VISUALS_PATH, sources: dict[str, ManifestSource] | None = None
) -> list[VisualResource]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = [VisualResource.model_validate(r) for r in raw["resources"]]
    if sources is not None:
        for r in items:
            if r.resource_id not in sources or r.host_page_source_id not in sources:
                raise KBError(f"{r.resource_id}: not resolvable in the manifest")
    return items


# ---------------------------------------------------------------- rule registry -----------
# Declarative conditions with whitelisted operators, no eval (D-038). Three-valued logic:
# a condition is True, False or None (unknown because a field it needs is missing). Unknown
# never becomes a guess: the rule returns cannot_determine with the missing fields.

LEAF_OPS = {"eq", "ne", "lt", "gte", "in", "is_null"}
GROUP_OPS = {"all", "any"}
RULE_ID = re.compile(r"^R-[A-Z0-9]+-[A-Z0-9]+$")
# Rules prepare and caution; they never decide (REQ-SCP-008, REQ-ARC-008).
VERDICT = re.compile(
    r"\b(you are (not )?eligible|you qualify|you do not qualify|you will (get|be allocated)|"
    r"guaranteed|approved for)\b",
    re.IGNORECASE,
)
Tri = bool | None


@dataclass(frozen=True)
class Registry:
    rules_version: str
    kb_version: str
    fields: dict[str, dict[str, Any]]
    derived: dict[str, dict[str, Any]]
    rules: tuple[dict[str, Any], ...]


def load_rules(path: Path = RULES_PATH) -> Registry:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Registry(
        raw["rules_version"],
        raw["kb_version"],
        raw["fields"],
        raw.get("derived", {}),
        tuple(raw["rules"]),
    )


def add_months(d: date, months: int) -> date:
    """Calendar-month addition, clamping the day to the month's end (I-02 convention)."""
    m = d.month - 1 + months
    year, month = d.year + m // 12, m % 12 + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1]))


def derive(values: Mapping[str, Any], as_of: date) -> dict[str, Any]:
    out = dict(values)
    issue = values.get("hfe_issue_date")
    out["derived.hfe_days_to_expiry"] = (
        (add_months(issue, 9) - as_of).days if isinstance(issue, date) else None
    )
    return out


def condition_fields(cond: Mapping[str, Any]) -> set[str]:
    for op in GROUP_OPS:
        if op in cond:
            return set().union(*(condition_fields(c) for c in cond[op]))
    return {str(cond["field"])}


def evaluate(cond: Mapping[str, Any], values: Mapping[str, Any]) -> tuple[Tri, set[str]]:
    """Returns (truth value, fields whose absence made the result unknown)."""
    if "all" in cond or "any" in cond:
        is_all = "all" in cond
        results = [evaluate(c, values) for c in cond["all" if is_all else "any"]]
        decisive = not is_all  # all: one False decides; any: one True decides
        if any(v is decisive for v, _ in results):
            return decisive, set()
        unknown = [m for v, m in results if v is None]
        if unknown:
            return None, set().union(*unknown)
        return not decisive, set()
    ops = (set(cond) - {"field"}) & LEAF_OPS
    if len(ops) != 1 or set(cond) - {"field"} - LEAF_OPS:
        raise ValueError(f"condition must have exactly one whitelisted operator: {dict(cond)}")
    op = ops.pop()
    field, target = str(cond["field"]), cond[op]
    value = values.get(field)
    if op == "is_null":
        return (value is None) is bool(target), set()
    if value is None:
        return None, {field}
    if op == "eq":
        result = value == target
    elif op == "ne":
        result = value != target
    elif op == "lt":
        result = value < target
    elif op == "gte":
        result = value >= target
    else:  # "in"
        result = value in target
    return bool(result), set()


def missing_inputs(fields: set[str], reg: Registry) -> list[str]:
    """Map derived fields back to the profile fields they are computed from."""
    out: set[str] = set()
    for f in fields:
        out |= set(reg.derived[f]["inputs"]) if f in reg.derived else {f}
    return sorted(out)


def evaluate_rule(rule: Mapping[str, Any], values: Mapping[str, Any], reg: Registry) -> RuleResult:
    base = {
        "rule_id": rule["rule_id"],
        "rule_version": rule["version"],
        "kind": rule["kind"],
        "source_fact_ids": list(rule["source_fact_ids"]),
    }
    review = bool(rule["requires_human_review"])
    truth, missing = evaluate(rule["when"], values)
    if truth is None:
        return RuleResult(
            **base,
            status="cannot_determine",
            preparation_step=None,
            missing_fields=missing_inputs(missing, reg),
            requires_human_review=review,
        )
    if truth is False:
        return RuleResult(
            **base, status="not_applicable", preparation_step=None, requires_human_review=False
        )
    notes = [f"{i['id']}: {i['note']}" for i in rule.get("interpretations", [])]
    notes += [f"Limitation: {x}" for x in rule.get("limitations", [])]
    exc_missing: set[str] = set()
    for exc in rule.get("exceptions", []):
        hit, m = evaluate(exc["when"], values)
        if hit is None:
            exc_missing |= m
        elif hit:
            if exc["effect"] == "suppress":
                return RuleResult(
                    **base,
                    status="not_applicable",
                    preparation_step=None,
                    requires_human_review=False,
                    notes=[f"{exc['id']}: {exc['note']}"],
                )
            review = True
            notes.append(f"{exc['id']}: {exc['note']}")
    if exc_missing:
        # An exception might apply but cannot be checked: ask rather than assume.
        return RuleResult(
            **base,
            status="cannot_determine",
            preparation_step=None,
            missing_fields=missing_inputs(exc_missing, reg),
            requires_human_review=review,
            notes=notes,
        )
    return RuleResult(
        **base,
        status="applies",
        preparation_step=str(rule["action"]),
        requires_human_review=review,
        notes=notes,
    )


def evaluate_rules(
    reg: Registry,
    profile_values: Mapping[str, Any],
    as_of: date,
    topics: set[str] | None = None,
) -> list[RuleResult]:
    """Evaluate every rule (optionally only those tagged with an asked topic)."""
    values = derive(profile_values, as_of)
    return [
        evaluate_rule(r, values, reg)
        for r in reg.rules
        if topics is None or topics & set(r["topics"])
    ]


def validate_registry(reg: Registry, kb: KnowledgeBase) -> list[str]:
    """Consistency of the registry with itself and with the reviewer-facing KB (D-006)."""
    errors: list[str] = []
    known_fields = set(reg.fields) | set(reg.derived)
    facts = {f.fact_id: f for f in kb.facts}
    if reg.kb_version != kb.kb_version:
        errors.append(f"rules cite {reg.kb_version}, KB is {kb.kb_version}")
    ids = [str(r.get("rule_id")) for r in reg.rules]
    errors += [f"duplicate rule_id {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    in_scope = {t.value for t, tier in TOPIC_TIER.items() if tier is not Tier.EXCLUDED}

    def check_condition(rid: str, cond: Any) -> None:
        if not isinstance(cond, dict):
            errors.append(f"{rid}: condition is not a mapping")
            return
        groups = set(cond) & GROUP_OPS
        if groups:
            if len(cond) != 1 or not isinstance(cond[groups.pop()], list):
                errors.append(f"{rid}: malformed all/any group")
                return
            for c in next(iter(cond.values())):
                check_condition(rid, c)
            return
        ops = set(cond) - {"field"}
        if "field" not in cond or len(ops) != 1 or not ops <= LEAF_OPS:
            errors.append(f"{rid}: unknown or extra operator in {sorted(cond)}")
            return
        field, op = cond["field"], ops.pop()
        if field not in known_fields:
            errors.append(f"{rid}: unknown field {field}")
            return
        spec = reg.fields.get(field) or reg.derived[field]
        allowed = spec.get("values")
        if allowed and op in ("eq", "ne") and cond[op] not in allowed:
            errors.append(f"{rid}: {field} value {cond[op]!r} not in {allowed}")
        if allowed and op == "in" and not set(cond[op]) <= set(allowed):
            errors.append(f"{rid}: {field} values {cond[op]} not all in {allowed}")
        if op in ("lt", "gte") and spec["type"] != "int":
            errors.append(f"{rid}: {op} used on non-numeric field {field}")

    for r in reg.rules:
        rid = str(r.get("rule_id"))
        if not RULE_ID.match(rid):
            errors.append(f"{rid}: rule_id format")
        for key in (
            "when",
            "action",
            "source_fact_ids",
            "sources",
            "topics",
            "effective",
            "basis",
            "kind",
            "requires_human_review",
        ):
            if key not in r:
                errors.append(f"{rid}: missing {key}")
        if any(e.startswith(f"{rid}: missing") for e in errors):
            continue
        check_condition(rid, r["when"])
        for exc in r.get("exceptions", []):
            check_condition(rid, exc.get("when"))
            if exc.get("effect") not in ("suppress", "human_review"):
                errors.append(f"{rid}: exception {exc.get('id')} has an unknown effect")
            for fid in exc.get("fact_ids", []):
                if fid not in r["source_fact_ids"]:
                    errors.append(f"{rid}: exception cites {fid}, which the rule does not cite")
        if not r["source_fact_ids"]:
            errors.append(f"{rid}: cites no facts")
        cited_topics: set[str] = set()
        for fid in r["source_fact_ids"]:
            fact = facts.get(fid)
            if fact is None:
                errors.append(f"{rid}: unknown fact {fid}")
                continue
            # Only manually verified facts may ground a deterministic rule.
            if fact.validation.status != "verified" or not fact.usable():
                errors.append(f"{rid}: fact {fid} is not verified/usable")
            cited_topics.add(fact.topic.value)
            ref = {"source_id": fact.source.source_id, "url": str(fact.source.url)}
            if not any(
                s.get("source_id") == ref["source_id"] and s.get("url") == ref["url"]
                for s in r["sources"]
            ):
                errors.append(f"{rid}: sources do not list {fid}'s official URL")
        for s in r["sources"]:
            if s.get("source_id") not in kb.sources:
                errors.append(f"{rid}: source {s.get('source_id')} not in the manifest")
        for t in r["topics"]:
            if t not in in_scope:
                errors.append(f"{rid}: topic {t} is not in scope")
            elif t not in cited_topics:
                errors.append(f"{rid}: topic {t} has no cited fact")
        if r["basis"] not in ("source_established", "interpretation"):
            errors.append(f"{rid}: basis must be source_established or interpretation")
        needs_review = (
            r["basis"] == "interpretation" or r["interpretations"] or r["kind"] == "evidence_gap"
        )
        if needs_review and not r["requires_human_review"]:
            errors.append(f"{rid}: interpretation/evidence gap must require human review")
        if r["kind"] == "evidence_gap" and r["basis"] != "interpretation":
            errors.append(f"{rid}: an evidence gap is identified by interpretation")
        if VERDICT.search(str(r["action"])):
            errors.append(f"{rid}: action reads as an eligibility verdict")
        eff = r["effective"]
        if eff.get("from") or eff.get("to"):
            dated = [facts[f].effective_from for f in r["source_fact_ids"] if f in facts]
            if not any(dated):
                errors.append(f"{rid}: claims effective dates its facts do not state")
    return errors
