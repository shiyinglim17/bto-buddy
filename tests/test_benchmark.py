"""Dataset C: schema, traceability, split hygiene and held-out access control (D-063, D-064)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation import benchmark as bm

from bto_buddy import policy


@pytest.fixture(scope="module")
def manifest() -> dict:
    return bm.load_manifest()


def test_dev_labels_are_traceable_and_valid() -> None:
    kb, reg = policy.load_kb(), policy.load_rules()
    for case, label in bm.load_dev():
        assert bm.validate_label(label, case, kb, reg) == []


def test_test_inputs_carry_no_labels() -> None:
    label_keys = set(bm.CaseLabel.model_fields) - {"case_id"}
    for row in bm.read_jsonl(bm.TEST_INPUTS_PATH):
        assert not label_keys & set(row), row["case_id"]
    assert all(c.split == "test" for c in bm.load_test_inputs())


def test_split_sizes_and_category_balance(manifest: dict) -> None:
    assert len(bm.load_dev()) == 18 and len(bm.load_test_inputs()) == 30
    for counts in manifest["counts"].values():
        assert counts == {"dev": 3, "test": 5}


def test_families_never_span_splits(manifest: dict) -> None:
    fam = manifest["families"]
    dev = {fam[c.case_id] for c, _ in bm.load_dev()}
    test = {fam[c.case_id] for c in bm.load_test_inputs()}
    assert not dev & test


def test_no_cross_split_near_duplicates() -> None:
    inputs = [c for c, _ in bm.load_dev()] + bm.load_test_inputs()
    assert [p for p in bm.near_duplicates(inputs) if p[0][:3] != p[1][:3]] == []


def test_heldout_labels_are_locked_outside_final_scoring(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(bm.FINAL_ENV, raising=False)
    with pytest.raises(bm.HeldOutLocked):
        bm.load_test_labels()
    with pytest.raises(bm.HeldOutLocked):
        bm.load_test_labels(final=True)  # env flag missing
    monkeypatch.setenv(bm.FINAL_ENV, "1")
    if bm.load_manifest()["status"] != "frozen":
        with pytest.raises(bm.HeldOutLocked):
            bm.load_test_labels(final=True)  # not frozen yet


def test_heldout_label_file_matches_commitment(manifest: dict) -> None:
    # Hashes the bytes only; the labels are not parsed or read here.
    if not bm.TEST_LABELS_PATH.exists():
        pytest.skip("held-out labels not present on this machine")
    assert bm.sha256(bm.TEST_LABELS_PATH) == manifest["heldout_labels_sha256"]


def test_validator_rejects_untraceable_labels() -> None:
    kb, reg = policy.load_kb(), policy.load_rules()
    case, label = bm.load_dev()[0]
    bad = label.model_copy(
        update={
            "required_rule_ids": ["R-NOPE-001"],
            "evidence_fact_ids": ["HH-PROP-002"],  # exists but not verified
            "required_missing_fields": ["salary"],
        }
    )
    errors = " | ".join(bm.validate_label(bad, case, kb, reg))
    assert (
        "unknown rule" in errors and "not verified" in errors and "unknown profile field" in errors
    )


def test_undetermined_rules_missing_from_label_are_warned() -> None:
    # Regression for DEV-13: a rule the engine cannot decide must not vanish from the label
    # unnoticed. Dropping the conditional R-HH-001 has to surface as a warning.
    reg = policy.load_rules()
    case, label = next((c, lab) for c, lab in bm.load_dev() if c.case_id == "DEV-13")
    assert "R-HH-001" not in bm.engine_undetermined_unlabelled(label, case, reg)
    dropped = label.model_copy(
        update={"conditional_rule_ids": [r for r in label.conditional_rule_ids if r != "R-HH-001"]}
    )
    assert "R-HH-001" in bm.engine_undetermined_unlabelled(dropped, case, reg)


def test_claim_template_follows_the_protocol() -> None:
    kb = policy.load_kb()
    verified = {f.fact_id for f in kb.facts if f.validation.status == "verified"}
    path = Path(__file__).resolve().parents[1] / "evaluation" / "claims" / "claim_template.jsonl"
    rows = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
    assert {r["gold_label"] for r in rows} == {"supported", "contradicted", "insufficient_evidence"}
    for r in rows:
        assert set(r["evidence_fact_ids"]) <= verified and r["split"] == "dev"
