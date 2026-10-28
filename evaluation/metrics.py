"""Automated evaluation metrics and paired ablation statistics (05 §4, metric_spec §4-§8).

  uv run python -m evaluation.metrics <A_run> <B_run> <D_run>   # dev runs -> metrics_dev.json
  BTO_BUDDY_FINAL_EVAL=1 uv run python -m evaluation.metrics <A> <B> <D>  # -> metrics_test.json

The split comes from the runs' metadata. Held-out labels are released only through
`load_test_labels(final=True)` (D-064); the metric definitions are identical for both splits.

Scope and honesty rules:
- Only metrics that can be computed WITHOUT human judgement are computed here. The primary
  human-judged metrics (critical-error rate, required-information coverage, claim
  correctness for A, actionability) need the developer's blind scoring (metric_spec §3) and
  are reported as "pending", never estimated.
- Every case stays in every denominator, including failed calls (metric_spec §7).
- Paired comparisons use the same cases: exact McNemar on binary case outcomes, and a paired
  bootstrap (10,000 resamples, fixed seed) for differences in rates.
- Claim-level rates for B and D use the agent's post-hoc claim annotations
  (`claim_annotations.jsonl` in the D run), disclosed as such.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from evaluation.benchmark import CaseLabel, load_dev, load_test_labels
from evaluation.run import RESULTS, load_predictions

SEED = 20261029
N_BOOT = 10_000
CATEGORIES = [
    "standard",
    "missing_information",
    "policy_exception",
    "misconception",
    "conflicting",
    "out_of_scope",
]


# ---- statistics (stdlib) ------------------------------------------------------------------
def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value from the discordant counts b and c (binomial, p=0.5)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n
    return min(1.0, p)


def paired_bootstrap(x: list[float], y: list[float], seed: int = SEED) -> dict[str, float]:
    """95% percentile CI for mean(y) - mean(x) over paired units."""
    assert len(x) == len(y)
    n = len(x)
    if n == 0:
        return {"diff": 0.0, "ci_low": 0.0, "ci_high": 0.0}
    rng = random.Random(seed)
    diffs = []
    for _ in range(N_BOOT):
        idx = [rng.randrange(n) for _ in range(n)]
        diffs.append(sum(y[i] - x[i] for i in idx) / n)
    diffs.sort()
    return {
        "diff": round(sum(y) / n - sum(x) / n, 4),
        "ci_low": round(diffs[int(0.025 * N_BOOT)], 4),
        "ci_high": round(diffs[int(0.975 * N_BOOT) - 1], 4),
    }


def ratio(num: int, den: int) -> dict[str, Any]:
    return {"num": num, "den": den, "rate": round(num / den, 3) if den else None}


# ---- per-case outcomes ------------------------------------------------------------------
def case_outcomes(g: dict[str, Any], lab: CaseLabel) -> dict[str, Any]:
    """Binary/count outcomes for one case, from the visible structured output only."""
    failed = g["run"]["status"] == "failed"
    listed = {m["field"] for m in g["missing_profile_fields"]}
    conflict_fields = {f for c in g["profile_conflicts"] for f in c["fields"]}
    shown = [
        c
        for c in g["claims"]
        if c["verification"] is None or c["verification"]["outcome"] != "contradicted"
    ]
    substantive = [
        c
        for c in shown
        if c["claim"]["kind"] != "caveat"
        and (c["verification"] is None or c["verification"]["outcome"] == "supported")
    ]
    policy = [c for c in shown if c["claim"]["kind"] == "policy_fact"]
    cited = [f for c in g["claims"] for f in c["claim"]["cited_fact_ids"]]
    return {
        "failed": failed,
        "missing_hits": sum(f in listed for f in lab.required_missing_fields),
        "missing_den": len(lab.required_missing_fields),
        "conflict_hits": sum(bool(set(c.fields) & conflict_fields) for c in lab.expected_conflicts),
        "conflict_den": len(lab.expected_conflicts),
        # Appropriate abstention, automated proxy of metric_spec §4.5: (1) declines via
        # out_of_scope_reasons and (2) gives an official redirect (redirect_url, or HDB named
        # in the decline or a caveat). "No calculation or verdict in the text" needs the human
        # scorer. A failed call is not a redirect.
        "abstained_ok": (not failed)
        and bool(g["out_of_scope_reasons"])
        and (
            any(o["redirect_url"] for o in g["out_of_scope_reasons"])
            or "hdb" in " ".join(o["detail"] for o in g["out_of_scope_reasons"]).lower()
            or any(
                c["claim"]["kind"] == "caveat" and "hdb" in c["claim"]["text"].lower()
                for c in g["claims"]
            )
        ),
        # Over-abstention (answerable = yes): whole answer declined, or no substantive claim.
        "over_abstained": (not failed) and not substantive,
        "covered": bool(substantive),  # answer-coverage proxy (in-scope cases)
        "policy_shown": len(policy),
        "policy_with_source": sum(bool(c["sources"]) for c in policy),
        "cited": len(cited),
        "cited_in_gold": sum(f in set(lab.evidence_fact_ids) for f in cited),
    }


def aggregate(outs: list[dict[str, Any]], labs: list[CaseLabel]) -> dict[str, Any]:
    no = [o for o, lb in zip(outs, labs, strict=True) if lb.answerable == "no"]
    yes = [o for o, lb in zip(outs, labs, strict=True) if lb.answerable == "yes"]
    in_scope = [o for o, lb in zip(outs, labs, strict=True) if lb.answerable != "no"]
    return {
        "cases": len(outs),
        "failed": sum(o["failed"] for o in outs),
        "missing_information_recall": ratio(
            sum(o["missing_hits"] for o in outs), sum(o["missing_den"] for o in outs)
        ),
        "conflict_identification": ratio(
            sum(o["conflict_hits"] for o in outs), sum(o["conflict_den"] for o in outs)
        ),
        "appropriate_abstention": ratio(sum(o["abstained_ok"] for o in no), len(no)),
        "over_abstention": ratio(sum(o["over_abstained"] for o in yes), len(yes)),
        "answer_coverage_proxy": ratio(sum(o["covered"] for o in in_scope), len(in_scope)),
        "citation_traceability": ratio(
            sum(o["policy_with_source"] for o in outs), sum(o["policy_shown"] for o in outs)
        ),
        "citation_precision_vs_gold_facts": ratio(
            sum(o["cited_in_gold"] for o in outs), sum(o["cited"] for o in outs)
        ),
    }


# ---- claim-level (B vs D) -----------------------------------------------------------------
def claim_level(d_run: str, split: str = "dev") -> dict[str, Any]:
    """Unsupported-claim rate as exposed to the user, B vs D, on the same annotated claims.
    B shows every claim as stated; D withholds contradicted and labels insufficient ones as
    unconfirmed, so only D's 'supported' claims count as presented-as-established."""
    path = RESULTS / d_run / "claim_annotations.jsonl"
    if not path.exists() and split == "test":
        # Held-out claims are not hand-labelled: report the verifier's outcomes only, with no
        # accuracy claim (label-free, descriptive).
        outcomes: dict[str, int] = defaultdict(int)
        for p in load_predictions(d_run):
            for r in (p["verifier"] or {}).get("results", []):
                outcomes[r["outcome"]] += 1
        return {"annotated": False, "verifier_outcomes": dict(outcomes)}
    if not path.exists():
        # Gold claim labels are written by hand after a D run; a fresh live D run has none.
        raise SystemExit(
            f"{d_run} has no claim_annotations.jsonl: label its checked claims first "
            "(template: evaluation/claims/claim_template.jsonl), or pass the saved D run."
        )
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    b_est = rows  # B: all checked claims are presented as established
    d_est = [r for r in rows if r["verifier"] == "supported"]

    def unsupported(rs: list[dict[str, Any]]) -> dict[str, Any]:
        return ratio(sum(r["gold"] != "supported" for r in rs), len(rs))

    def contradicted(rs: list[dict[str, Any]]) -> int:
        return sum(r["gold"] == "contradicted" for r in rs)

    # Paired per claim: exposed-as-established AND not gold-supported (1) vs not (0).
    b_bad = [int(r["gold"] != "supported") for r in rows]
    d_bad = [int(r["gold"] != "supported" and r["verifier"] == "supported") for r in rows]
    disc_b = sum(1 for x, y in zip(b_bad, d_bad, strict=True) if x and not y)
    disc_d = sum(1 for x, y in zip(b_bad, d_bad, strict=True) if y and not x)
    return {
        "annotator": "coding agent, post hoc (not developer-blind; not the D-065 claim set)",
        "checked_claims": len(rows),
        "B_unsupported_among_established": unsupported(b_est),
        "D_unsupported_among_established": unsupported(d_est),
        "B_contradicted_shown_as_established": contradicted(b_est),
        "D_contradicted_shown_as_established": contradicted(d_est),
        "D_true_claims_lost": sum(
            r["gold"] == "supported" and r["verifier"] != "supported" for r in rows
        ),
        "paired_exposed_unsupported": {
            "B_only": disc_b,
            "D_only": disc_d,
            # Claims are clustered within cases, so this p-value overstates the evidence.
            "mcnemar_exact_p_claims_assumed_independent": f"{mcnemar_exact(disc_b, disc_d):.1e}",
            "bootstrap_D_minus_B": paired_bootstrap(
                [float(v) for v in b_bad], [float(v) for v in d_bad]
            ),
            # Respects clustering: resample cases, compare exposed unsupported claims per case.
            "case_cluster_bootstrap_D_minus_B_per_case": paired_bootstrap(
                *_per_case(rows, b_bad, d_bad)
            ),
        },
    }


def _per_case(
    rows: list[dict[str, Any]], b_bad: list[int], d_bad: list[int]
) -> tuple[list[float], list[float]]:
    xb: dict[str, float] = defaultdict(float)
    yd: dict[str, float] = defaultdict(float)
    for r, x, y in zip(rows, b_bad, d_bad, strict=True):
        xb[r["case_id"]] += x
        yd[r["case_id"]] += y
    cases = sorted(xb)
    return [xb[c] for c in cases], [yd[c] for c in cases]


# ---- main ------------------------------------------------------------------------------
def run_split(runs: dict[str, str]) -> str:
    splits = {
        json.loads((RESULTS / r / "run_metadata.json").read_text())["split"] for r in runs.values()
    }
    if len(splits) != 1:
        raise SystemExit(f"runs mix splits: {sorted(splits)}")
    return splits.pop()


def evaluate(runs: dict[str, str]) -> dict[str, Any]:
    split = run_split(runs)
    gold = [lb for _, lb in load_dev()] if split == "dev" else load_test_labels(final=True)
    labels = {lb.case_id: lb for lb in gold}
    per_cfg: dict[str, dict[str, dict[str, Any]]] = {}
    for cfg, run_id in runs.items():
        per_cfg[cfg] = {
            p["case_id"]: case_outcomes(p["final_guidance"], labels[p["case_id"]])
            for p in load_predictions(run_id)
        }
    case_ids = sorted(set.intersection(*(set(v) for v in per_cfg.values())))
    labs = [labels[c] for c in case_ids]
    report: dict[str, Any] = {
        "split": split,
        "runs": runs,
        "n_paired_cases": len(case_ids),
        "pending_human_metrics": [
            "critical-error rate (labelled + unlabelled critical errors)",
            "required-information coverage (content key points)",
            "claim-level factual correctness for A",
            "actionability",
        ],
        "not_applicable": {
            "required_rule_recall": "C is not built; no configuration applies rules "
            "(diagnostic D1 needs C)",
        },
        "overall": {},
        "by_category": defaultdict(dict),
        "paired": {},
    }
    for cfg in runs:
        outs = [per_cfg[cfg][c] for c in case_ids]
        report["overall"][cfg] = aggregate(outs, labs)
        for cat in CATEGORIES:
            sel = [i for i, lb in enumerate(labs) if lb.category == cat]
            report["by_category"][cat][cfg] = aggregate(
                [outs[i] for i in sel], [labs[i] for i in sel]
            )

    def paired(x_cfg: str, y_cfg: str) -> dict[str, Any]:
        out: dict[str, Any] = {}
        # Case-level binary outcome: all required missing fields listed (cases that have any).
        sel = [i for i, lb in enumerate(labs) if lb.required_missing_fields]
        xs = [per_cfg[x_cfg][case_ids[i]] for i in sel]
        ys = [per_cfg[y_cfg][case_ids[i]] for i in sel]
        xb = [int(o["missing_hits"] == o["missing_den"]) for o in xs]
        yb = [int(o["missing_hits"] == o["missing_den"]) for o in ys]
        b = sum(1 for p, q in zip(xb, yb, strict=True) if p and not q)
        c = sum(1 for p, q in zip(xb, yb, strict=True) if q and not p)
        out["all_missing_fields_listed"] = {
            "cases": len(sel),
            f"{x_cfg}_only": b,
            f"{y_cfg}_only": c,
            "mcnemar_exact_p": round(mcnemar_exact(b, c), 4),
        }
        # Case-level: answer covered (in-scope cases).
        sel = [i for i, lb in enumerate(labs) if lb.answerable != "no"]
        xb = [int(per_cfg[x_cfg][case_ids[i]]["covered"]) for i in sel]
        yb = [int(per_cfg[y_cfg][case_ids[i]]["covered"]) for i in sel]
        b = sum(1 for p, q in zip(xb, yb, strict=True) if p and not q)
        c = sum(1 for p, q in zip(xb, yb, strict=True) if q and not p)
        out["answer_covered"] = {
            "cases": len(sel),
            f"{x_cfg}_only": b,
            f"{y_cfg}_only": c,
            "mcnemar_exact_p": round(mcnemar_exact(b, c), 4),
        }
        # Per-case missing-information recall, paired bootstrap.
        sel = [i for i, lb in enumerate(labs) if lb.required_missing_fields]

        def recall(cfg: str, i: int) -> float:
            o = per_cfg[cfg][case_ids[i]]
            return float(o["missing_hits"] / o["missing_den"])

        out["missing_information_recall_bootstrap"] = paired_bootstrap(
            [recall(x_cfg, i) for i in sel], [recall(y_cfg, i) for i in sel]
        )
        return out

    cfgs = list(runs)
    for x_cfg, y_cfg in itertools.pairwise(cfgs):
        report["paired"][f"{x_cfg}_vs_{y_cfg}"] = paired(x_cfg, y_cfg)
    if "D" in runs:
        report["claim_level_B_vs_D"] = claim_level(runs["D"], split)
    report["by_category"] = dict(report["by_category"])
    return report


def main() -> None:
    args = sys.argv[1:]
    if len(args) != 3:
        raise SystemExit(__doc__)
    report = evaluate(dict(zip(["A", "B", "D"], args, strict=True)))
    out = RESULTS / f"metrics_{report['split']}.json"
    out.write_text(json.dumps(report, indent=1))
    print(json.dumps({k: report[k] for k in ("overall", "paired", "claim_level_B_vs_D")}, indent=1))
    print(f"wrote {out.relative_to(Path(__file__).resolve().parents[1])}")


if __name__ == "__main__":
    main()
