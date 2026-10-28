"""Run configurations on the benchmark and save predictions (architecture §11.2, REQ-DAT-018).

  uv run python -m evaluation.run run --config A --split dev [--cases DEV-01,DEV-02]
  uv run python -m evaluation.run check <run_id>          # completeness + contract + label join
  uv run python -m evaluation.run sheet <run_id> [...]     # blinded scoring sheet (metric_spec §3)

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

from bto_buddy import llm
from bto_buddy.generation import GENERATE_PROMPT, SCHEMA_NAME, load_prompt, strict_json_schema
from bto_buddy.pipeline import ConfigId, render_answer, run_direct
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


def run(config: ConfigId, split: str, case_ids: list[str] | None, final: bool) -> Path:
    if config != "A":
        raise SystemExit(f"configuration {config} is not built yet")
    if split == "test" and not final:
        raise SystemExit("the held-out split runs only in the final evaluation (--final)")
    cases = [i for i, _ in load_dev()] if split == "dev" else load_test_inputs()
    if case_ids:
        cases = [c for c in cases if c.case_id in case_ids]
    client = llm.OpenAICompatibleClient.from_env(ROOT / ".env")
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
        "kb_version": None,
        "rules_version": None,
        "git_commit": _git_commit(),
        "started_at": datetime.now(UTC).isoformat(),
    }
    n_failed = 0
    with (out_dir / "predictions.jsonl").open("w") as f:
        for case in cases:
            g, attempts = _run_case(case, client)
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


def _run_case(case: CaseInput, client: llm.LLMClient) -> tuple[FinalGuidance, list[dict[str, Any]]]:
    """Wrap the client so every attempt's raw response is kept alongside the prediction."""
    recorder = _RecordingClient(client)
    g = run_direct(to_request(case), recorder)
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


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["run"]:
        config = args[args.index("--config") + 1] if "--config" in args else "A"
        split = args[args.index("--split") + 1] if "--split" in args else "dev"
        cases = args[args.index("--cases") + 1].split(",") if "--cases" in args else None
        run(config, split, cases, "--final" in args)  # type: ignore[arg-type]
    elif args[:1] == ["check"] and len(args) == 2:
        sys.exit(0 if check(args[1])["ok"] else 1)
    elif args[:1] == ["sheet"] and len(args) >= 2:
        sheet(args[1:])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
