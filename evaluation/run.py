"""Run configurations on the benchmark and save predictions (architecture §11.2, REQ-DAT-018).

  uv run python -m evaluation.run run --config A --split dev [--cases DEV-01,DEV-02]
  uv run python -m evaluation.run check <run_id>          # completeness + contract + label join
  uv run python -m evaluation.run sheet <run_id> [...]     # blinded scoring sheet (metric_spec §3)
  uv run python -m evaluation.run verify <B_run_id>          # D from B's saved outputs
  uv run python -m evaluation.run diagnostics <run_id> [...]  # structural diagnostics + retrieval

The generation process sees `CaseInput` only (as_of, situation_text, question); labels are
loaded only by `check` and `sheet`, after generation, and only for dev. The held-out split
runs only with `--final` (the final evaluation), from label-free `test_inputs.jsonl`
(D-064). Every case is written, including failures (metric_spec §7).
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from bto_buddy import llm, pipeline
from bto_buddy.generation import GENERATE_PROMPT, SCHEMA_NAME, load_prompt, strict_json_schema
from bto_buddy.pipeline import ConfigId, render_answer
from bto_buddy.schemas import FinalGuidance, GenerationOutput, UserRequest
from evaluation.benchmark import CaseInput, load_dev, load_test_inputs

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "evaluation" / "results"
SHEET_SEED = 20261029  # fixed so the blinded order is reproducible


def to_request(case: CaseInput) -> UserRequest:
    # Only the input fields cross into the pipeline; labels never do.
    return UserRequest(
        request_id=case.case_id,
        situation_text=case.situation_text,
        question=case.question,
        as_of=case.as_of,
    )


def _git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        )
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True
        ).stdout.strip()
        return out.stdout.strip() + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return None


def _client() -> llm.OpenAICompatibleClient:
    """Live runs need a key; fail before creating a results directory, without a traceback."""
    try:
        return llm.OpenAICompatibleClient.from_env(ROOT / ".env")
    except llm.LLMError:
        raise SystemExit(
            "No LLM API key: set BTO_BUDDY_LLM_API_KEY in .env (cp .env.example .env) or the "
            "environment. Offline commands (check, sheet, diagnostics, evaluation.metrics) "
            "need no key."
        ) from None


def run(config: ConfigId, split: str, case_ids: list[str] | None, final: bool) -> Path:
    if config not in ("A", "B", "D"):
        raise SystemExit(f"configuration {config} is not built (D-069)")
    if split == "test" and not final:
        raise SystemExit("the held-out split runs only in the final evaluation (--final)")
    cases = [i for i, _ in load_dev()] if split == "dev" else load_test_inputs()
    if case_ids:
        cases = [c for c in cases if c.case_id in case_ids]
    client = _client()
    run_id = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{config}-{split}"
    out_dir = RESULTS / run_id
    out_dir.mkdir(parents=True)
    prompt = load_prompt()
    meta: dict[str, Any] = {
        "run_id": run_id,
        "config_id": config,
        "split": split,
        "case_ids": [c.case_id for c in cases],
        "model_id": client.model_id,
        "base_url": client.base_url,
        "settings": {
            "temperature": client.temperature,
            "reasoning_effort": client.reasoning_effort,
            "max_completion_tokens": client.max_completion_tokens,
            "timeout_s": client.timeout_s,
            "max_transport_retries": client.max_retries,
            "response_format": "json_schema strict",
            "validation_retries": 1,
        },
        "prompt_versions": {"generate": GENERATE_PROMPT},
        "prompt_sha256": {"generate": hashlib.sha256(prompt.encode()).hexdigest()},
        "schema_name": SCHEMA_NAME,
        "schema_sha256": hashlib.sha256(
            json.dumps(strict_json_schema(GenerationOutput), sort_keys=True).encode()
        ).hexdigest(),
        "prices_usd_per_m": llm.PRICES.get(client.model_id),
        "kb_version": pipeline.get_index().kb_version if config == "B" else None,
        "retrieval_k": pipeline.retrieval.DEFAULT_K if config == "B" else None,
        "rules_version": None,
        "git_commit": _git_commit(),
        "started_at": datetime.now(UTC).isoformat(),
    }
    n_failed = 0
    with (out_dir / "predictions.jsonl").open("w") as f:
        for case in cases:
            g, attempts = _run_case(case, client, config)
            n_failed += g.run.status == "failed"
            row = {
                "case_id": case.case_id,
                "final_guidance": g.model_dump(mode="json"),
                "visible_answer": render_answer(g),
                "attempts": attempts,
            }
            f.write(json.dumps(row) + "\n")
            f.flush()
            r = g.run
            print(
                f"{case.case_id} {r.status} calls={r.llm_calls} ms={r.latency_ms} "
                f"in={r.input_tokens} out={r.output_tokens} cost=${r.estimated_cost_usd or 0:.5f}"
                + (f" error={r.error[:120]}" if r.error else ""),
                flush=True,
            )
    meta["finished_at"] = datetime.now(UTC).isoformat()
    meta["n_cases"] = len(cases)
    meta["n_failed"] = n_failed
    (out_dir / "run_metadata.json").write_text(json.dumps(meta, indent=1))
    print(f"saved {out_dir.relative_to(ROOT)} ({len(cases)} cases, {n_failed} failed)")
    return out_dir


def _run_case(
    case: CaseInput, client: llm.LLMClient, config: ConfigId
) -> tuple[FinalGuidance, list[dict[str, Any]]]:
    """Wrap the client so every attempt's raw response is kept alongside the prediction."""
    recorder = _RecordingClient(client)
    g = pipeline.run(to_request(case), config, recorder)
    return g, recorder.records


class _RecordingClient:
    def __init__(self, inner: llm.LLMClient) -> None:
        self.inner = inner
        self.model_id = inner.model_id
        self.temperature = inner.temperature
        self.reasoning_effort = inner.reasoning_effort
        self.records: list[dict[str, Any]] = []

    def complete(
        self, messages: list[dict[str, str]], schema_name: str, schema: dict[str, Any]
    ) -> llm.LLMResponse:
        at = datetime.now(UTC).isoformat()
        try:
            resp = self.inner.complete(messages, schema_name, schema)
        except llm.LLMError as e:
            self.records.append({"at": at, "error_kind": e.kind, "error": e.detail, "raw": e.raw})
            raise
        self.records.append(
            {
                "at": at,
                "latency_ms": resp.latency_ms,
                "input_tokens": resp.input_tokens,
                "output_tokens": resp.output_tokens,
                "reasoning_tokens": resp.reasoning_tokens,
                "raw": resp.raw,
            }
        )
        return resp


def verify_run(b_run_id: str) -> Path:
    """Configuration D from a saved B run: B's exact pre-verification outputs are reloaded
    (no new generation) and only the verifier calls the model, so B vs D isolates
    verification (REQ-EVL-012). Failed B cases stay failed in D."""
    from bto_buddy.verification import VERIFY_PROMPT, apply_verification, record_json

    b_meta = json.loads((RESULTS / b_run_id / "run_metadata.json").read_text())
    if b_meta["config_id"] != "B":
        raise SystemExit("verify takes a configuration-B run")
    index = pipeline.get_index()
    if index.kb_version != b_meta["kb_version"]:
        raise SystemExit("KB version differs from the B run; bundles would not match")
    # Label-free inputs for either split; the held-out labels are never loaded here.
    cases = [c for c, _ in load_dev()] if b_meta["split"] == "dev" else load_test_inputs()
    inputs = {c.case_id: c for c in cases}
    client = _client()
    run_id = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-D-{b_meta['split']}"
    out_dir = RESULTS / run_id
    out_dir.mkdir(parents=True)
    meta = {
        **{k: v for k, v in b_meta.items() if k not in ("run_id", "started_at", "finished_at")},
        "run_id": run_id,
        "config_id": "D",
        "pre_verification_run": b_run_id,
        "prompt_versions": {**b_meta["prompt_versions"], "verify": VERIFY_PROMPT},
        "verify_prompt_sha256": hashlib.sha256(
            (ROOT / "src/bto_buddy/prompts/verify_v1.md").read_bytes()
        ).hexdigest(),
        "judge_model_id": client.model_id,
        "judge_settings": {
            "temperature": client.temperature,
            "reasoning_effort": client.reasoning_effort,
            "max_completion_tokens": client.max_completion_tokens,
        },
        "git_commit": _git_commit(),
        "started_at": datetime.now(UTC).isoformat(),
    }
    n_failed = 0
    with (out_dir / "predictions.jsonl").open("w") as f:
        for p in load_predictions(b_run_id):
            pre = FinalGuidance.model_validate(p["final_guidance"])
            req = to_request(inputs[p["case_id"]])
            g, rec = apply_verification(pre, req, pipeline.retrieve_for(req), client)
            n_failed += g.run.status == "failed"
            row = {
                "case_id": p["case_id"],
                "final_guidance": g.model_dump(mode="json"),
                "visible_answer": render_answer(g),
                "pre_verification_sha256": hashlib.sha256(
                    json.dumps(p["final_guidance"], sort_keys=True).encode()
                ).hexdigest(),
                "verifier": record_json(rec),
            }
            f.write(json.dumps(row) + "\n")
            f.flush()
            outcomes = [r.outcome[:4] for r in rec.results]
            print(
                f"{p['case_id']} {g.run.status} verdicts={outcomes} judge_ms={rec.latency_ms}"
                + (f" judge_error={rec.judge_error[:100]}" if rec.judge_error else ""),
                flush=True,
            )
    meta["finished_at"] = datetime.now(UTC).isoformat()
    meta["n_failed"] = n_failed
    (out_dir / "run_metadata.json").write_text(json.dumps(meta, indent=1))
    print(f"saved {out_dir.relative_to(ROOT)}")
    return out_dir


def load_predictions(run_id: str) -> list[dict[str, Any]]:
    path = RESULTS / run_id / "predictions.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def check(run_id: str) -> dict[str, Any]:
    """Confirms a run can be scored: one prediction per case, each a valid FinalGuidance,
    and (dev only) every case joins to an approved label. Prints counts only."""
    meta = json.loads((RESULTS / run_id / "run_metadata.json").read_text())
    preds = load_predictions(run_id)
    ids = [p["case_id"] for p in preds]
    for p in preds:
        FinalGuidance.model_validate(p["final_guidance"])
    report: dict[str, Any] = {
        "run_id": run_id,
        "n_predictions": len(preds),
        "missing_cases": sorted(set(meta["case_ids"]) - set(ids)),
        "duplicate_cases": sorted({i for i in ids if ids.count(i) > 1}),
        "failed": sum(p["final_guidance"]["run"]["status"] == "failed" for p in preds),
        "retried": sum(p["final_guidance"]["run"]["llm_calls"] > 1 for p in preds),
    }
    if meta["split"] == "dev":
        labels = {lab.case_id: lab for _, lab in load_dev()}
        report["unlabelled"] = sorted(set(ids) - set(labels))
        report["labels_approved"] = all(labels[i].review.status == "approved" for i in ids)
    report["ok"] = not (
        report["missing_cases"] or report["duplicate_cases"] or report.get("unlabelled")
    )
    print(json.dumps(report, indent=1))
    return report


def sheet(run_ids: list[str]) -> Path:
    """Blinded scoring sheet: answers under random IDs in a seeded order, configuration
    hidden; the key goes to a separate file (metric_spec §3)."""
    rows, key = [], {}
    rng = random.Random(SHEET_SEED)
    for run_id in run_ids:
        for p in load_predictions(run_id):
            answer_id = f"ANS-{rng.getrandbits(32):08x}"
            key[answer_id] = {"run_id": run_id, "case_id": p["case_id"]}
            rows.append(
                {"answer_id": answer_id, "case_id": p["case_id"], "answer": p["visible_answer"]}
            )
    rng.shuffle(rows)
    rows.sort(key=lambda r: r["case_id"])  # group by case; order within a case stays random
    name = "sheet-" + hashlib.sha256("|".join(sorted(run_ids)).encode()).hexdigest()[:10]
    out_dir = RESULTS / "scoring" / name
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "answers.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["answer_id", "case_id", "answer"])
        w.writeheader()
        w.writerows(rows)
    (out_dir / "key.json").write_text(json.dumps(key, indent=1))
    print(
        f"wrote {out_dir.relative_to(ROOT)}/answers.csv ({len(rows)} answers); key.json kept apart"
    )
    return out_dir


def retrieval_recall(ks: tuple[int, ...] = (3, 5, 8, 12)) -> dict[str, Any]:
    """Diagnostic D3 on dev: gold = label evidence_fact_ids; query = question + situation (as
    in B). Micro recall, plus recall normalised by min(k, |gold|) because several cases have
    more gold facts than k."""
    from bto_buddy import retrieval

    index = pipeline.get_index()
    out: dict[str, Any] = {"kb_version": index.kb_version, "query": "question + situation"}
    for k in ks:
        hit = tot = ceil = 0
        misses: dict[str, list[str]] = {}
        for inp, lab in load_dev():
            gold = set(lab.evidence_fact_ids)
            if not gold:
                continue
            got = {
                f.fact_id
                for f, _ in retrieval.search(index, f"{inp.question} {inp.situation_text}", k)
            }
            hit += len(gold & got)
            tot += len(gold)
            ceil += min(k, len(gold))
            if gold - got:
                misses[inp.case_id] = sorted(gold - got)
        out[f"@{k}"] = {
            "hits": hit,
            "gold": tot,
            "recall": round(hit / tot, 3),
            "ceiling_normalised": round(hit / ceil, 3),
            "misses": misses,
        }
    return out


def diagnostics(run_ids: list[str]) -> dict[str, Any]:
    """Automated structural diagnostics on dev runs. NOT the primary metrics (those are the
    developer's blind judgements, metric_spec §3-4): these count what the structured output
    contains, never whether the content is correct."""
    labels = {lab.case_id: lab for _, lab in load_dev()}
    report: dict[str, Any] = {"note": diagnostics.__doc__, "runs": {}}
    for run_id in run_ids:
        preds = load_predictions(run_id)
        r: dict[str, Any] = {"n": len(preds)}
        g = [p["final_guidance"] for p in preds]
        lab = [labels[p["case_id"]] for p in preds]
        r["failed"] = sum(x["run"]["status"] == "failed" for x in g)
        # A generation retry, not the verifier's judge call (D adds one call per case).
        judge = [int("verify" in x["run"]["prompt_versions"] and bool(x["claims"])) for x in g]
        r["retried"] = sum(x["run"]["llm_calls"] - j > 1 for x, j in zip(g, judge, strict=True))
        pairs = list(zip(g, lab, strict=True))
        req = [(f, x) for x, lb in pairs for f in lb.required_missing_fields]
        listed = sum(f in {m["field"] for m in x["missing_profile_fields"]} for f, x in req)
        r["missing_fields_listed"] = f"{listed}/{len(req)}"
        conf = [(c, x) for x, lb in pairs for c in lb.expected_conflicts]
        flagged = sum(
            bool(set(c.fields) & {f for pc in x["profile_conflicts"] for f in pc["fields"]})
            for c, x in conf
        )
        r["conflicts_flagged"] = f"{flagged}/{len(conf)}"
        no = [x for x, lb in pairs if lb.answerable == "no"]
        r["out_of_scope_flagged"] = f"{sum(bool(x['out_of_scope_reasons']) for x in no)}/{len(no)}"
        yes = [x for x, lb in pairs if lb.answerable == "yes"]
        whole = sum(x["coverage"]["status"] == "out_of_scope" for x in yes)
        r["whole_answer_out_of_scope_on_answerable"] = f"{whole}/{len(yes)}"
        pol = [c for x in g for c in x["claims"] if c["claim"]["kind"] == "policy_fact"]
        r["policy_claims"] = len(pol)
        r["policy_claims_with_official_source"] = sum(bool(c["sources"]) for c in pol)
        cited = {f for c in pol for f in c["claim"]["cited_fact_ids"]}
        n_cites = n_gold = 0
        for x, lb in pairs:
            for c in x["claims"]:
                n_cites += len(c["claim"]["cited_fact_ids"])
                n_gold += len(set(c["claim"]["cited_fact_ids"]) & set(lb.evidence_fact_ids))
        r["cited_fact_ids_in_case_gold"] = f"{n_gold}/{n_cites}"
        r["distinct_facts_cited"] = len(cited)
        ver = [c["verification"] for x in g for c in x["claims"] if c["verification"]]
        if ver:
            r["verified_claims"] = len(ver)
            r["verdicts"] = {
                o: sum(v["outcome"] == o for v in ver)
                for o in ("supported", "contradicted", "insufficient_evidence")
            }
            r["claims_withheld"] = r["verdicts"]["contradicted"]

        # Answer-coverage proxy for every run: in-scope cases showing at least one non-caveat
        # claim that was not withheld or left unconfirmed by the verifier.
        def substantive(x: dict[str, Any]) -> bool:
            return any(
                c["claim"]["kind"] != "caveat"
                and (c["verification"] is None or c["verification"]["outcome"] == "supported")
                for c in x["claims"]
            )

        ok = [x for x, lb in pairs if lb.answerable != "no" and x["run"]["status"] == "ok"]
        in_scope = sum(lb.answerable != "no" for lb in lab)
        r["answer_coverage_proxy"] = f"{sum(substantive(x) for x in ok)}/{in_scope}"
        lat = sorted(x["run"]["latency_ms"] for x in g)
        r["latency_ms_median"] = lat[len(lat) // 2]
        r["cost_usd_total"] = round(sum(x["run"]["estimated_cost_usd"] or 0 for x in g), 5)
        r["tokens_in_mean"] = round(sum(x["run"]["input_tokens"] for x in g) / len(g))
        r["tokens_out_mean"] = round(sum(x["run"]["output_tokens"] for x in g) / len(g))
        report["runs"][run_id] = r
    report["retrieval"] = retrieval_recall()
    out = RESULTS / "diagnostics_dev.json"
    out.write_text(json.dumps(report, indent=1))
    print(json.dumps({k: v for k, v in report["runs"].items()}, indent=1))
    print(
        {
            k: {kk: vv for kk, vv in v.items() if kk != "misses"}
            for k, v in report["retrieval"].items()
            if k.startswith("@")
        }
    )
    return report


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["run"]:
        config = args[args.index("--config") + 1] if "--config" in args else "A"
        split = args[args.index("--split") + 1] if "--split" in args else "dev"
        cases = args[args.index("--cases") + 1].split(",") if "--cases" in args else None
        run(config, split, cases, "--final" in args)  # type: ignore[arg-type]
    elif args[:1] == ["check"] and len(args) == 2:
        sys.exit(0 if check(args[1])["ok"] else 1)
    elif args[:1] == ["verify"] and len(args) == 2:
        verify_run(args[1])
    elif args[:1] == ["diagnostics"] and len(args) >= 2:
        diagnostics(args[1:])
    elif args[:1] == ["sheet"] and len(args) >= 2:
        sheet(args[1:])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
