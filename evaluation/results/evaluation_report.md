# Evaluation report: ablation on the development set (2026-10-29)

**Status: development-set results only.** The benchmark is still a candidate (not frozen),
held-out labels are sealed and unused (D-064), and the human-judged primary metrics
(metric_spec §3) are not scored yet. Nothing here is a held-out result, and no
configuration is claimed to be better overall.

## 1. What was compared

| Config | Description | Run (saved predictions + metadata) |
|---|---|---|
| A | Direct LLM: profile + question, no evidence, no rules | `20261028T203350Z-A-dev` |
| B | A + BM25 retrieval over 89 authored facts (k=12), citations restricted to retrieved facts | `20261028T205255Z-B-dev` |
| D | B's **saved** answers + claim verifier (deterministic checks + 1 batched LLM judge) | `20261028T211724Z-D-dev` |
| C | Profiling + rules + retrieval | **Not built** (D-069). B vs C and C vs D are omitted |

- **Fairness controls:**
  - same model (`openai/gpt-oss-120b`, temperature 0, reasoning `low`) for all three;
  - same prompt (`generate_v1`) apart from its evidence slot;
  - same 18 cases, same `FinalGuidance` schema;
  - D reuses B's exact generations, with a SHA-256 of each pre-verification output stored;
  - failures kept in every denominator (B and D: DEV-12, HTTP 413).
- **Factual correctness vs citation:** citation traceability and citation precision are
  reported separately from claim correctness. The claim-correctness labels below judge what
  each claim says, whether or not it is cited.
- **Temporal fairness:** A's knowledge is older pretraining; B and D read an October 2026
  snapshot. B's factual gains partly reflect recency, not better reasoning.

Reproduce from saved outputs (offline, no API key):
`uv run python -m evaluation.metrics 20261028T203350Z-A-dev 20261028T205255Z-B-dev 20261028T211724Z-D-dev`
→ `evaluation/results/metrics_dev.json`.

## 2. Automated metrics (raw counts and denominators)

| Metric (dev, 18 paired cases) | A | B | D |
|---|---|---|---|
| Failed cases (kept in denominators) | 0 | 1 | 1 |
| Missing-information recall (instances) | 2/6 (0.33) | 3/6 (0.50) | 3/6 (0.50) |
| Conflict identification (instances) | 0/3 (0.00) | 0/3 (0.00) | 0/3 (0.00) |
| Appropriate abstention (automated proxy) | 3/3 (1.00) | 3/3 (1.00) | 3/3 (1.00) |
| Over-abstention (answerable = yes) | 0/9 (0.00) | 0/9 (0.00) | 0/9 (0.00) |
| Answer coverage proxy (in-scope) | 15/15 (1.00) | 14/15 (0.93) | 14/15 (0.93) |
| Citation traceability (shown policy claims with official source) | 0/34 (0.00) | 33/35 (0.94) | 28/34 (0.82) |
| Citation precision vs case gold facts | 0/0 | 19/50 (0.38) | 19/50 (0.38) |

| Category | Missing-info recall A/B/D | Answer coverage A/B/D | Source-linked policy claims A/B/D |
|---|---|---|---|
| standard | 0/0 · 0/0 · 0/0 | 3/3 · 3/3 · 3/3 | 0/4 · 8/8 · 7/8 |
| missing_information | 2/5 · 2/5 · 2/5 | 3/3 · 3/3 · 3/3 | 0/9 · 8/8 · 6/8 |
| policy_exception | 0/0 · 0/0 · 0/0 | 3/3 · 3/3 · 3/3 | 0/3 · 6/6 · 5/6 |
| misconception | 0/0 · 0/0 · 0/0 | 3/3 · 2/3 · 2/3 | 0/5 · 2/3 · 2/3 |
| conflicting | 0/1 · 1/1 · 1/1 | 3/3 · 3/3 · 3/3 | 0/8 · 6/6 · 5/5 |
| out_of_scope | 0/0 · 0/0 · 0/0 | 0/0 · 0/0 · 0/0 | 0/5 · 3/4 · 3/4 |

| Paired comparison | Discordant cases or claims | Test |
|---|---|---|
| A vs B: all required missing fields listed (4 cases) | A only 0, B only 1 | exact McNemar p = 1.0 |
| A vs B: answer covered (15 cases) | A only 1, B only 0 | p = 1.0 (B's one loss is the DEV-12 API failure) |
| A vs B: per-case missing-info recall | mean diff +0.25 | bootstrap 95% CI [0.00, 0.75] |
| B vs D: answer covered / missing fields | 0 discordant | identical (same generated answers) |
| **B vs D: claims shown as established that are not gold-supported (49 claims)** | B 22/49 → D 6/33; B only 16, D only 0 | McNemar p = 3.1e-05 *if claims were independent (they are not)*; **case-cluster bootstrap: -0.94 per case, 95% CI [-1.41, -0.47]** |
| B vs D: contradicted claims shown as established | B 8 → D 4 (and D labels those 4 "verified") | — |
| B vs D: correct claims lost | D 0 | — |

**Notes on definitions** (all computed from the visible structured output; implementation in
`evaluation/metrics.py`):
- **Missing-information recall:** the labelled required field appears in
  `missing_profile_fields`. A follow-up question written only in free text isn't counted, so
  this is a lower bound.
- **Appropriate abstention:** an automated proxy of metric_spec §4.5: declines via
  `out_of_scope_reasons` and gives an official redirect. "No calculation or verdict in the
  text" needs the human scorer.
- **Answer coverage proxy:** an in-scope case with at least one non-caveat claim that wasn't
  withheld or left unconfirmed. Actionability needs the human scorer.
- **Citation precision vs gold facts:** a cited fact is among the case's labelled evidence
  facts. This is strict, because a correct but unlabelled fact counts as imprecise.
- **Claim-level rates (B vs D):** the coding agent annotated all 49 checked claims after the
  run, against the cited facts and the applicant's situation
  (`20261028T211724Z-D-dev/claim_annotations.jsonl`). These labels are **not developer-blind
  and not the planned D-065 claim set.**
- **Statistics:** exact McNemar on discordant pairs; paired bootstrap with 10,000 resamples
  and seed 20261029; for claims, a case-cluster bootstrap, because claims within a case are
  not independent. With 18 cases, case-level tests have almost no power: p = 1.0 means "no
  evidence either way", not "no difference".

## 3. Verifier (D) against the claim labels

| Gold \ verifier | supported | contradicted | insufficient |
|---|---|---|---|
| supported (27) | 27 | 0 | 0 |
| contradicted (8) | 4 | 1 | 3 |
| insufficient (14) | 2 | 0 | 12 |

- **False alarms:** 0/27.
- **False approvals:** 6/22, including 4/8 contradicted claims.
- **Contradiction recall:** 1/8.
- **Insufficient detection:** 12/14.
- **Cost of verification:** +1 call per case; +43% cost over B (US$0.0182 vs US$0.0127 for
  18 cases); median latency 21.5 s vs 15.7 s (both include rate-limit waits).
- **Quality–coverage trade-off:** D removed or downgraded 16 claims that weren't supported,
  lost no correct claim, and answer coverage was unchanged (14/15). The cost is a worse kind
  of error on 4 claims: they are now shown as "verified".

## 4. Failure analysis (component-separated)

| Component | Failure | Cases | Observed → expected | Root cause | Status | Remediation |
|---|---|---|---|---|---|---|
| Generation (A) | Pretrained-knowledge errors | DEV-07, DEV-10, DEV-13 | "wait until 21", HFE "one year"/"6 months" → core occupier, 9 months | No evidence | Confirmed | Retrieval (fixed in B for these cases) |
| Retrieval | Gold facts not retrieved | 9/18 cases at k=12; recall@12 0.52 | Missing facts in the prompt | Colloquial vs authored wording; multi-fact questions | Confirmed (recall) | Rule-linked facts (C); aliases from dev misses only; denser retrieval only if D-031 approved |
| Generation (B) | Sub-group fact generalised | DEV-01, DEV-07, DEV-10, DEV-13 | FT(PMC)/U-02 note applied to all engaged couples | Fact applicability not visible to the model | Hypothesis | Pass `applies_to`; topic filter (C) |
| Profile signals (A, B) | Conflicts never flagged | DEV-13, DEV-14, DEV-15 | 0/3 → neutral clarification | The model is not asked to compare statements systematically | Confirmed (0/3) | Deterministic conflict checks (C) |
| Profile signals (A, B) | Missing fields assumed | DEV-04, DEV-05 | e.g. assumes the spouse is SC → ask | Same as above | Confirmed | Topic-scoped missing-field computation (C) |
| Verifier | False approval: wrong applicant category | DEV-01 c2, DEV-13 c1/c3, DEV-17 c2 | Shown as verified → contradicted | Same model generates and judges; no applicability metadata | Hypothesis (pattern confirmed) | Deterministic `applies_to` check; different judge model family (A5) |
| Verifier | Stricter-than-source condition missed | DEV-01 c3, DEV-07 c3, DEV-16 c3 | Unconfirmed → withheld | Judge reads "stricter" as "not stated" | Confirmed (rationales) | Prompt example; citizenship rule (C) |
| Citation | True correction left uncited | DEV-11 c1 | Unconfirmed → supported (HH-COUPLE-001) | Generator didn't cite | Confirmed | Rule-linked facts (C) |
| Infrastructure | HTTP 413 | DEV-12 (B, D) | Failure → answer | Output cap 6000 counted against the 8K tokens/min plan | Confirmed | Cap 4096 (D-070) |

## 5. Task-13 requirements: status

| Requirement | Status |
|---|---|
| Same model, instructions, scenarios and schema across configurations | ✅ (A, B, D) |
| C vs D reuses identical pre-verification outputs | ✅ as **B vs D** (C not built) |
| Held-out evaluation with frozen labels, rubric and metrics | ❌ Not run: freeze not approved; labels sealed and untouched |
| Retrieval evaluated separately (recall@k, k justified) | ✅ dev recall@3/5/8/12 with ceiling normalisation; k = 12 justified by the retrieval budget |
| Retrieval at rule level; indexing conditions, exceptions and topic | ✅ index includes aliases, topic, section, exceptions; ❌ rule-level retrieval (no C) |
| Required-rule recall | ❌ Not applicable (no configuration applies rules) |
| Missing-information recall | ✅ automated (lower bound) |
| Unsupported-claim rate | ✅ B and D (agent claim labels); ❌ A (needs human) |
| Citation precision | ✅ vs gold facts; traceability separately |
| Appropriate abstention | ✅ automated proxy |
| Critical-error rate | ❌ Pending developer blind scoring (sheet `scoring/sheet-de54b20a64/`) |
| Signals evaluated separately | ✅ missing fields, conflicts, evidence gaps (in output), out-of-scope |
| Severity rubric | ✅ defined (metric_spec); applied only in human scoring (pending) |
| Verifier evaluated on labelled claims | ✅ (agent labels, post hoc) |
| Raw predictions, model IDs, prompt and corpus versions, latency, tokens, cost recorded | ✅ `predictions.jsonl`, `run_metadata.json` |
| Raw counts, per-category, paired differences, CIs | ✅ dev |
| Failures not excluded | ✅ |
| No optimisation on held-out data | ✅ never opened |
| Answer coverage / quality–coverage trade-off | ✅ proxy |

## 6. How to complete the held-out evaluation (developer)

1. Approve D-063 to D-066 and freeze the benchmark (manifest `status: frozen`).
2. `uv run python -m evaluation.run run --config A --split test --final`, then the same with
   `--config B`, then `uv run python -m evaluation.run verify <B_test_run>`.
3. Score blind with `evaluation.run sheet <A_run> <B_run> <D_run>`. Release the labels only
   through `load_test_labels(final=True)` with `BTO_BUDDY_FINAL_EVAL=1`.
4. Extend `evaluation.metrics` to the test split. It currently loads dev labels only, by
   design.
