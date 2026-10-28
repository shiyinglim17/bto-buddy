"""The reviewer-facing KB loads from tracked files only and every fact resolves (REQ-DAT-012)."""

import json
from pathlib import Path

import pytest

from bto_buddy import policy
from bto_buddy.schemas import TOPIC_TIER, PolicyFact, Tier, Topic

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def kb() -> policy.KnowledgeBase:
    return policy.load_kb()


def test_every_topic_has_a_tier() -> None:
    assert set(TOPIC_TIER) == set(Topic)
    in_scope = {t for t, tier in TOPIC_TIER.items() if tier is not Tier.EXCLUDED}
    assert len(in_scope) == 7  # 4 Core, 2 Limited, 1 Context (REQ-SCP-012)


def test_kb_loads_and_resolves_without_private_corpus(kb: policy.KnowledgeBase) -> None:
    assert kb.facts and kb.kb_version.startswith("kb-")
    assert policy.check_integrity(list(kb.facts), kb.sources) == []
    for f in kb.facts:
        src = kb.sources[f.source.source_id]
        assert src.mvp_class in policy.CITABLE
        assert str(f.source.url).startswith(("https://www.hdb.gov.sg/", "https://file.go.gov.sg/"))


def test_tracked_kb_files_hold_no_private_paths() -> None:
    for name in ("policy_facts.jsonl", "visual_resources.json", "source_coverage.csv"):
        text = (DATA / name).read_text(encoding="utf-8")
        assert "private_corpus" not in text and "/Users/" not in text, name


def test_kb_covers_every_in_scope_topic(kb: policy.KnowledgeBase) -> None:
    covered = {f.topic for f in kb.facts}
    assert covered == {t for t, tier in TOPIC_TIER.items() if tier is not Tier.EXCLUDED}


def test_usable_rule_holds_back_unverified_critical_facts(kb: policy.KnowledgeBase) -> None:
    for f in kb.facts:
        if f.critical and f.validation.status != "verified":
            assert not f.usable()
    sample = next(f for f in kb.facts if not f.critical)
    pending = sample.model_copy(
        update={"rights_review": sample.rights_review.model_copy(update={"status": "pending"})}
    )
    assert not pending.usable()


def test_fact_schema_rejects_excluded_tier_and_bad_ids() -> None:
    line = (DATA / "policy_facts.jsonl").read_text(encoding="utf-8").splitlines()[0]
    raw = json.loads(line)
    with pytest.raises(ValueError):
        PolicyFact.model_validate(raw | {"scope_tier": "excluded"})
    with pytest.raises(ValueError):
        PolicyFact.model_validate(raw | {"fact_id": "bad id"})
    with pytest.raises(ValueError):
        PolicyFact.model_validate(raw | {"unknown_field": 1})


def test_integrity_catches_broken_references(kb: policy.KnowledgeBase) -> None:
    f = kb.facts[0]
    broken = [
        f.model_copy(update={"source": f.source.model_copy(update={"source_id": "S99"})}),
        f.model_copy(update={"fact_id": "HH-DUP-001"}),
        f.model_copy(update={"fact_id": "HH-DUP-001"}),
    ]
    errors = policy.check_integrity(broken, kb.sources)
    assert any("unknown source S99" in e for e in errors)
    assert any("duplicate fact_id HH-DUP-001" in e for e in errors)


def test_visual_resources_are_links_never_evidence(kb: policy.KnowledgeBase) -> None:
    items = policy.load_visual_resources(sources=kb.sources)
    assert {i.resource_id for i in items} == {"M00", "M01", "M03", "M04"}
    assert all(i.evidence is False for i in items)
    assert all("si=" not in str(i.url) for i in items)  # share tracking stripped (D-049)


def test_excluded_sources_are_never_cited(kb: policy.KnowledgeBase) -> None:
    raw = json.loads((DATA / "sources_manifest.json").read_text(encoding="utf-8"))
    excluded = {s["source_id"] for s in raw["excluded_sources"]}
    assert "S10" in excluded and not excluded & set(kb.sources)  # D-060
    for f in kb.facts:
        assert f.source.source_id not in excluded
        assert "/hdb-flat-portal" not in str(f.source.url)
    for r in policy.load_visual_resources(sources=kb.sources):
        assert "/hdb-flat-portal" not in str(r.url)


def test_one_frozen_kb_for_app_rules_retrieval_and_benchmark() -> None:
    # The app, BM25 index and evaluation all load data/policy_facts.jsonl through load_kb();
    # this pins that file (and the rules) to the hashes recorded at the corpus freeze.
    import hashlib

    from bto_buddy import pipeline

    root = Path(__file__).resolve().parents[1]
    frozen = json.loads((root / "data/corpus/corpus_version.json").read_text())
    for rel in ("data/policy_facts.jsonl", "data/policy_rules.yaml"):
        digest = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        assert digest == frozen["files_sha256"][rel], rel
    kb, reg = policy.load_kb(), policy.load_rules()
    bench = json.loads((root / "evaluation/benchmark/manifest.json").read_text())
    versions = {kb.kb_version, reg.kb_version, bench["kb_version"], frozen["kb_version"]}
    assert versions == {pipeline.get_index().kb_version}
    assert policy.validate_registry(reg, kb) == []
