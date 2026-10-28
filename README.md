<div align="center">

<h1>BTO Buddy</h1>

<p><b>An evidence-grounded preparation assistant for first-time BTO flat applicants</b><br/>
Public-sector AI prototype · fictional applicant profiles only · not an official eligibility assessment</p>

<p>
<a href="#1-quick-start-docker">Run it</a> ·
<a href="#4-how-it-works">Architecture</a> ·
<a href="#5-data-provenance-licensing-and-privacy">Data</a> ·
<a href="#6-model-selection">Model</a> ·
<a href="#7-evaluation">Evaluation</a> ·
<a href="#8-results-development-set">Results</a> ·
<a href="#10-limitations">Limitations</a> ·
<a href="#13-ai-coding-agent-usage">AI usage</a>
</p>

<p><b>Demo video (3–5 min):</b> <i>link to be added before submission</i></p>

</div>

---

## 1. Quick start (Docker)

Prerequisites: Docker, and a GroqCloud API key (free account at console.groq.com).

```bash
git clone <this repository> && cd bto-buddy
cp .env.example .env          # then set BTO_BUDDY_LLM_API_KEY=<your Groq key>
docker build -t bto-buddy .
docker run --rm -p 8501:8501 --env-file .env bto-buddy
# open http://localhost:8501   ·   health: curl -f http://localhost:8501/_stcore/health
```

- The image contains only the tracked, reviewer-facing data (`data/policy_facts.jsonl`,
  `policy_rules.yaml`, `sources_manifest.json`, `visual_resources.json`). It never needs the
  private source snapshots (`data/private_corpus/`), the held-out labels or any local file
  other than `.env`.
- The only credential is `BTO_BUDDY_LLM_API_KEY` (or `GROQ_API_KEY`). Base URL and model
  default to Groq and `openai/gpt-oss-120b` when left blank. Write the key unquoted.
- Without a key the app still starts, passes the health check and shows "No LLM API key is
  configured" at the top of the page. No answer can be generated until a key is set.

**Local development** (uv 0.13.6, Python ≥ 3.12):

```bash
uv sync                                   # exact versions from uv.lock
uv run pytest                             # 145 offline tests, no API key (1 skips without held-out labels)
uv run ruff check . && uv run mypy        # lint + strict typing
uv run streamlit run src/bto_buddy/app.py # reads ./.env, like the evaluation runner
```

### Offline (deterministic) vs live (API, non-deterministic)

| Kind | Commands | Needs | Reproduces |
|---|---|---|---|
| **Offline, deterministic** | `pytest`, `ruff`, `mypy`, KB load, BM25 retrieval, `evaluation.run check / sheet / diagnostics`, `evaluation.metrics` on the saved runs | Nothing beyond `uv sync` | **Exactly**: `diagnostics_dev.json` and `metrics_dev.json` are recomputed byte-for-byte from the saved predictions |
| **Live, non-deterministic** | the app, `evaluation.run run`, `evaluation.run verify` | API key, network, Groq availability | **Not exactly.** Provider-side variation remains even at temperature 0, so a re-run is a *new experiment*, saved under a new run ID; it never overwrites the saved record |

The saved predictions in `evaluation/results/` are the reproducible record of the reported
results:

```bash
# Offline: recompute the reported diagnostics and metrics from the saved runs (no key)
uv run python -m evaluation.run diagnostics 20261028T203350Z-A-dev 20261028T205255Z-B-dev 20261028T211724Z-D-dev
uv run python -m evaluation.metrics 20261028T203350Z-A-dev 20261028T205255Z-B-dev 20261028T211724Z-D-dev
git diff --exit-code evaluation/results/   # no diff = reproduced

# Live: new runs (key needed; results vary)
uv run python -m evaluation.run run --config A --split dev
uv run python -m evaluation.run verify 20261028T205255Z-B-dev   # D re-judged on B's saved answers
```

`evaluation.metrics` on a **new** D run needs claim labels (`claim_annotations.jsonl`) to be
written for that run first. They are hand labels, not generated.

**Live re-run variance (measured 2026-10-29 from a clean clone).** `verify` on the saved B
answers reused identical pre-verification outputs (18/18 hashes) and reproduced the saved
verifier verdicts on **46 of 49 claims**. In the three that changed, the judge moved from
"insufficient" to "supported" (2) or to "contradicted" (1). Re-running A gave 18/18
successful cases, with the same counts of missing fields, conflicts and out-of-scope
reasons in 17/18 cases, but identical summary text in only 5/18. The reported numbers come
from the saved runs, not from these re-runs.

### What a reviewer cannot reproduce from the repository

- **Source snapshots and fact authoring (L0/L1 → L2).** `scripts/corpus.py` and
  `scripts/snapshots.py` need `data/private_corpus/`. These HDB snapshots are not
  redistributed, because rights to redistribute are not established (§5). A reviewer can
  recapture the same pages by hand in a browser (`docs/data_sources.md` §7), but the live
  pages may have changed, so the hashes in `data/sources_manifest.json` may not match. The
  tracked `policy_facts.jsonl` is the reproducible starting point. Without snapshots, both
  scripts stop with a message and change nothing.
- **Held-out scoring.** The labels are sealed (D-064); only their hash is tracked.

### Clean-machine smoke test

Run from a fresh `git clone`, with no `.env`, no `data/private_corpus/` and no
`references/`:

1. `uv lock --check && uv sync`: resolves 61 packages from `uv.lock`.
2. `uv run pytest`: 144 passed, 1 skipped (held-out labels absent).
3. `uv run ruff check . && uv run ruff format --check . && uv run mypy`: clean.
4. `uv run python -c "from bto_buddy.policy import load_kb; print(load_kb().kb_version)"` prints `kb-2026-10-28.1`.
5. Offline evaluation recomputation (above) leaves `git diff` empty.
6. `cp .env.example .env && docker build -t bto-buddy . && docker run --rm -p 8501:8501 --env-file .env bto-buddy`.
7. `curl -f http://localhost:8501/_stcore/health` returns `ok`; the page shows the "No LLM API key" error.
8. Put the key in `.env`, restart the container, choose a preset and click **Get preparation
   guidance**. A summary, sourced requirements, and a footer with the model, latency and
   token count appear.

Verified on 2026-10-29 (macOS, Docker 29.9.2, uv 0.13.6). The image was built with
`--no-cache` from a fresh clone of commit `8947d7e` (plus the reproducibility fixes listed
in `docs/development_log.md`). Steps 1–8 passed. Live answers ran inside the container for
configurations A and D.

## 2. Problem and objective

Couples applying for their first Build-To-Order (BTO) flat in Singapore must first get an HDB
Flat Eligibility (HFE) letter. The rules on household composition, timing and documents are
spread across several official pages and PDFs. Small misunderstandings, such as "the HFE
letter lasts a year" or "we must marry before applying", lead to wasted applications.

**BTO Buddy** turns a free-text description of a (fictional) couple and a question into
**preparation guidance**:
- what the published requirements say;
- what to prepare;
- what information is missing;
- which details contradict each other;
- what our sources cannot confirm.

Every policy statement links to the official HDB page it comes from. It **never** decides
eligibility, calculates grants or estimates ballot chances. Those are redirected to official
services.

**Research question:** does grounding a single LLM in a small, verified, source-attributed
knowledge base (and, in the full design, deterministic rules and claim verification) reduce
critical errors compared with the same model answering from its own knowledge?

**Scope** (D-008):
- **Core:** first-timer couple household composition; broad application requirements; HFE
  prerequisites, timing and documents; missing applicant information.
- **Limited:** priority schemes; non-selection consequences.
- **Context only:** how the HFE letter relates to grants and loans.
- **Excluded:** eligibility decisions, grant and loan calculations, financing, ballot odds,
  post-purchase conditions, real applicant data.

## 3. What is implemented (and what is not)

| Component | Status | Where |
|---|---|---|
| Authored knowledge base: 89 facts, each with source URL, section, retrieval date and validation status | ✅ | `data/policy_facts.jsonl`, `src/bto_buddy/policy.py` |
| Declarative rule registry: 24 rules, three-valued logic, no `eval` | ✅ built and unit-tested; **not yet wired into the answer pipeline** | `data/policy_rules.yaml`, `policy.py`, `tests/test_rules.py` |
| **Configuration A**, direct LLM (baseline) | ✅ | `pipeline.run_direct` |
| **Configuration B**, BM25 retrieval plus grounded generation with citations restricted to retrieved facts | ✅ | `retrieval.py`, `pipeline.run_rag` |
| Configuration C (LLM profile extraction, coverage gate, rules wired in) | ❌ designed, not built | `docs/architecture.md` §3 |
| **Configuration D**, claim-level verifier (deterministic checks + one batched LLM judge), **applied to B** | ✅ built on B, not C (D-071) | `verification.py`, `pipeline.run_verified` |
| Streamlit app (A/B/D toggle, 3 live presets, verified/unconfirmed/withheld display, source links, learning resources) | ✅ | `src/bto_buddy/app.py` |
| Benchmark: 48 fictional cases (18 dev / 30 sealed held-out) | ✅ (candidate, not frozen) | `evaluation/benchmark/`, `docs/evaluation_benchmark.md` |
| Evaluation runner, blinded scoring sheet, diagnostics | ✅ | `evaluation/run.py`, `evaluation/metric_spec.md` |

C was dropped for time (D-069). D was then built **on B instead of C** (D-071). The
verifier re-checks B's *saved* answers, so **B vs D is a clean verification ablation**:
identical generated answers, and only verification differs. The held-out set was never opened
or run, so a full A–D evaluation can still be done without leakage.

## 4. How it works

```
free text + question
   ├─ A: ─────────────────────────────────────────────► LLM (generate_v1, no evidence) ─► FinalGuidance
   ├─ B: BM25 over 89 authored facts (top 12) ─► evidence block ─► LLM (generate_v1) ─► citation check ─► FinalGuidance
   └─ D: B's output ─► deterministic checks (no citation / citation not retrieved → insufficient)
                   ─► ONE batched LLM judge (verify_v1, cited facts + applicant situation only)
                   ─► supported: show with source · contradicted: withhold + flag · insufficient: "unconfirmed", no source
   (approved C design, not built: LLM extraction → quote guard → deterministic gate → rules ∥ BM25 → generation)
```

- **One output contract** (`FinalGuidance`, Pydantic) for every configuration. It always
  carries:
  - `missing_profile_fields`, `profile_conflicts`, `evidence_gaps` and
    `out_of_scope_reasons` as separate lists;
  - claims tagged `policy_fact` / `preparation_step` / `caveat`;
  - run metadata: model, prompt version, tokens, latency, cost, status.
- **One prompt** (`src/bto_buddy/prompts/generate_v1.md`) with an evidence slot. A gets
  "no sources provided"; B gets the retrieved facts with their IDs and exceptions. Task
  instructions are otherwise identical, so A vs B isolates retrieval.
- **Structured output:** strict JSON schema derived from the Pydantic models. On a
  validation failure, one retry carries the error; after that the request **fails closed**
  and the failure is kept in the results.
- **Citation integrity (B):** a claim may cite only facts that were actually retrieved. Each
  cited fact maps to its official URL through the source manifest. A policy claim with no
  citation is shown as "not confirmed by our sources" (an `evidence_gap`), never as
  established. Missing evidence is never presented as proof that a requirement does not
  exist.
- **Verification (D):** checks every `policy_fact` claim and any cited preparation step;
  caveats and uncited procedural steps are not policy assertions. The judge must find that the
  cited facts **substantively** state the claim, including numbers, conditions and who it
  applies to; a fact on the same topic is not enough. Claims are never rewritten and nothing
  is regenerated. If the judge fails or returns no verdict, the claim is shown only as
  unconfirmed (fail closed). The judge uses the same model as generation (A5), so they can
  share a misunderstanding; the results below show this happening.
- **Retrieval:** one authored fact is one passage. Facts are atomic, so splitting would
  separate conditions from qualifiers and merging would blur citations. The index text is
  the statement, aliases, topic, section heading and exceptions. Tokenisation is
  deterministic, with accent folding and a small reviewable synonym map. No vector database
  (D-031).

## 5. Data provenance, licensing and privacy

| Dataset | What | Provenance | In Git? |
|---|---|---|---|
| Source snapshots (L0/L1) | 5 HDB pages (S01–S05) and 2 HDB PDFs (S07, S08), captured manually in a browser on 2026-10-28; other sources are link-only | `data/sources_manifest.json` (URL, hash, timestamp, rights record per source) | **No**, private and Git-ignored |
| Policy facts (L2) | 89 **independently authored** paraphrases. 53 `verified` (all critical facts) and 36 `snapshot_checked`; all passed an automated 8-word-overlap check | `data/policy_facts.jsonl`; method in `docs/data_sources.md` | Yes |
| Rules (L3) | 24 declarative rules citing verified facts only | `data/policy_rules.yaml` | Yes |
| Learning resources | 2 official HFE infographics and 2 videos, **links only**, never evidence | `data/visual_resources.json` | Yes |
| Benchmark | 48 **synthetic** couple profiles with labels citing facts and rules | `evaluation/benchmark/` | Dev yes; held-out labels sealed |

- **Lawful access:**
  - HDB returns HTTP 403 to automated clients. That block was respected: pages were captured
    by hand, with no scraping or spoofing (D-055).
  - The HFE FAQ pages are excluded because robots.txt disallows them (D-060).
- **Copyright:**
  - Snapshots are kept for computational analysis only (Copyright Act 2021 s 244).
  - Only authored paraphrases are tracked; no source text is.
  - HDB's Terms of Use ask for permission before linking or reuse. This prototype is private
    and locally run. Public deployment would need HDB's permission (D-057; residual risk,
    disclosed).
  - Facts carry `rights_review: overlap_checked`. The developer's final rights read
    (`cleared`) is pending.
- **Privacy:**
  - Only fictional profiles are used, and the UI warns against entering real data.
  - User text is not logged.
  - Runtime calls send the fictional profile and the authored facts to Groq, never raw source
    text (D-054).
- **Why synthetic profiles:**
  - Real applicant data would be personal data under the PDPA and isn't needed.
  - Hand-built profiles can target specific failure modes (missing fields, contradictions,
    exceptions, misconceptions, out-of-scope requests) that real logs would rarely contain
    in a small sample.
  - Each label cites the facts and rules it rests on.

## 6. Model selection

**Selected:** `openai/gpt-oss-120b` on GroqCloud (D-067). One model is used for every
configuration, at temperature 0, reasoning effort `low`, and strict `json_schema` output.

- **Method:** a protocol registered before any output was produced
  (`evaluation/model_selection/protocol.md`). It used 12 dev cases, one prompt, one schema,
  the scorecard (accuracy 35, structured output 25, uncertainty 20, latency 10, cost 10) and
  minimum acceptance thresholds.
- **Gemini 3.8 Flash** could not be evaluated: one-word probes took 25–104 s and one call
  returned HTTP 503. It was stopped for time, so **there was no head-to-head comparison**.
- **gpt-oss-120b, direct generation:**
  - schema-valid 11/12 on the first attempt and 12/12 after one retry;
  - median latency 1.9 s; about US$0.0005 per call;
  - but policy accuracy 0.20, with critical errors in 7/12 cases. It **failed** the
    pre-registered accuracy and critical-error thresholds. This is disclosed rather than
    hidden.
  - Raw outputs and scores: `evaluation/model_selection/runs/20261028T201952Z/`.
- **Operational justification:**
  - **Latency:** about 2 s per call suits a multi-call pipeline.
  - **Cost:** the lowest cost at scale of the candidates.
  - **Reproducibility and portability:** open weights (Apache-2.0) can be pinned, re-hosted
    or served locally.
  - **Data handling:** Groq keeps no inference data by default and offers zero data
    retention.
  - **Task fit:** the threshold failure shows the model's own HDB knowledge is unreliable.
    That is the case for grounding it in verified facts, not for trusting it directly.
- **Rejected options:**
  - **Fine-tuning:** no rights-cleared training data, and policy changes over time.
  - **Local inference:** fictional data needs no on-premise processing, and laptop
    performance varies across reviewers. Revisit for real applicant data.

## 7. Evaluation

**Design** (`docs/project_context/05_evaluation.md`, `evaluation/metric_spec.md`): an
ablation of one pipeline. A (direct LLM) → B (+ retrieval) → C (+ profiling and rules) →
D (+ verification), all with the same model, instructions, cases and output contract.

- **Benchmark:** 48 synthetic cases in 6 categories × 8: standard, missing information,
  policy exception, misconception, conflicting details, out of scope. The split is group-aware
  (18 dev / 30 held-out), with near-duplicate families kept on one side. Held-out labels are
  Git-ignored and hash-committed, released only by a guarded loader (D-064). **No model or
  agent has seen them.**
- **Primary metrics** (D-066, architecture-neutral; judged blind on the visible answer only):
  - critical-error rate (severity rubric: critical / major);
  - required-information coverage;
  - claim-level factual correctness and unsupported-claim rate;
  - missing-information recall and conflict identification;
  - appropriate abstention and over-abstention;
  - answer coverage and actionability.

  Factual correctness is scored separately from citation, so A is not penalised just for
  having no citation mechanism.
- **Diagnostics** (never used to rank): structured-signal counts, citation traceability,
  retrieval recall@k, and verifier accuracy on labelled claims (false approvals, false alarms,
  contradiction recall, insufficient-evidence detection).
- **Ablation as built:** A vs B (retrieval) and **B vs D (verification, identical generated
  answers)**. B vs C and C vs D need C, so they are omitted.
- **Automated metrics** (`evaluation/metrics.py`):
  - missing-information recall;
  - conflict identification;
  - appropriate abstention and over-abstention (proxies of metric_spec §4.5);
  - answer-coverage proxy;
  - citation traceability, and citation precision against the gold facts;
  - unsupported-claim rate (B and D, from claim labels).

  Statistics are exact McNemar plus paired and case-cluster bootstraps, tested against
  hand-computed values. Required-rule recall is not applicable because no built
  configuration applies rules.
- **Scorer:** the developer, blind. `evaluation.run sheet` exports answers under random IDs
  with the configuration hidden. **This scoring has not been done yet**, so no primary metric
  is reported below.
- **Statistics planned:** exact McNemar and a paired bootstrap on paired cases, with
  failures kept in every denominator.
- **Retrieval metric:** recall@3 suits single-answer retrieval. Here, dev cases carry 1–7
  gold facts, so recall@3 is capped below 1 for many cases. The informative measure is recall
  at the k actually passed to generation (12), also reported normalised by
  min(k, number of gold facts).

## 8. Results (development set)

> **Development set only:** 18 cases, one run per configuration. **No held-out run** (the
> benchmark isn't frozen and the labels stay sealed), and **no human-judged primary metrics
> yet**: critical-error rate, key-point coverage and actionability await the developer's
> blind scoring. Case-level tests on 18 cases have almost no power. Claim-level labels were
> made by the coding agent after the run. **No configuration is claimed to be better
> overall.**

Full report with definitions, the per-category table and the failure analysis:
**[evaluation/results/evaluation_report.md](evaluation/results/evaluation_report.md)**.
Machine-readable: `evaluation/results/metrics_dev.json`, computed offline by
`uv run python -m evaluation.metrics <A_run> <B_run> <D_run>`.

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
| Median latency per case (includes rate-limit waits) | 4.3 s | 15.7 s | 21.5 s |
| Total cost, 18 cases (list price) | US$0.0095 | US$0.0127 | US$0.0182 |

**Paired comparisons** (same cases; failures included):

| Paired comparison | Discordant cases or claims | Test |
|---|---|---|
| A vs B: all required missing fields listed (4 cases) | A only 0, B only 1 | exact McNemar p = 1.0 |
| A vs B: answer covered (15 cases) | A only 1, B only 0 | p = 1.0 (B's one loss is the DEV-12 API failure) |
| A vs B: per-case missing-info recall | mean diff +0.25 | bootstrap 95% CI [0.00, 0.75] |
| B vs D: answer covered / missing fields | 0 discordant | identical (same generated answers) |
| **B vs D: claims shown as established that are not gold-supported (49 claims)** | B 22/49 → D 6/33; B only 16, D only 0 | McNemar p = 3.1e-05 *if claims were independent (they are not)*; **case-cluster bootstrap: -0.94 per case, 95% CI [-1.41, -0.47]** |
| B vs D: contradicted claims shown as established | B 8 → D 4 (and D labels those 4 "verified") | — |
| B vs D: correct claims lost | D 0 | — |


**Verifier evaluation (B vs D, the same 49 checked claims).** Each claim was labelled against
its cited facts and the applicant's situation. Labels and rationales are in
`evaluation/results/20261028T211724Z-D-dev/claim_annotations.jsonl`; metrics are in
`verifier_eval.json`. **The coding agent annotated these after the run. They are not
developer-blind and are not the planned D-065 claim set**, so treat them as indicative.

| Gold \ verifier | supported | contradicted | insufficient |
|---|---|---|---|
| supported (27) | **27** | 0 | 0 |
| contradicted (8) | **4** | 1 | 3 |
| insufficient (14) | **2** | 0 | 12 |

- **False alarms: 0/27.** No correct claim was withheld or downgraded, so there is no
  usefulness loss on the answer-coverage proxy (14/15 in both B and D).
- **False approvals: 6/22**, including **4 of the 8 contradicted claims**, which D then
  displays as verified with an official source.
- **Contradiction recall: 1/8.** 4/8 contradicted claims are no longer shown as established
  (1 withheld, 3 unconfirmed). In B, all 8 were shown as established, 7 with a source link.
- **Insufficient-evidence detection: 12/14.**
- **Cost:** about 5.9 s median and US$0.0003 per case for one extra call.

**Retrieval (dev, 52 gold facts over 18 cases):** recall@3 0.23 · @5 0.33 · @8 0.42 ·
**@12 0.52**. This is well below the 0.90 target in D-031. Misses per case are listed in
`diagnostics_dev.json`.

**Observed behaviour** (observations, not scores):
- **A states wrong policy confidently:**
  - HFE validity given as "one year" (DEV-10) or "6 months" (DEV-13), against 9 months in
    `HFE-VALID-001`;
  - "wait until he turns 21" instead of the under-21 core-occupier route (DEV-07);
  - an invented meaning of FT(PMC) (model selection, DEV-14).
- **B gets the 9-month validity and the core-occupier route right, citing the facts.** It
  introduces a new error: it over-generalises the KB's "unconfirmed for engaged couples" note,
  which is about FT(PMC) priority, into "eligibility for engaged couples is unconfirmed"
  (DEV-07, DEV-10, DEV-13).
- **Neither configuration flags contradictions** (0/3), and both sometimes assume missing
  values (DEV-05). That is exactly what C's deterministic profile checks are designed for.
- **Out-of-scope requests** (grant amounts, ballot odds, singles) are declined by all
  configurations.
- **D's main weakness is applicant-category applicability.** 4 of the 6 false approvals cite
  the FT(PMC) fact for claims about all first-timer couples, e.g. telling an engaged couple
  "first-timer couples must be married" (DEV-01 c2, DEV-13 c1). The other two: "first-timer
  families receive three ballot chances", when the fact gives 2, or 3 only with FT(PMC)
  (DEV-17 c2); and an assumed citizenship (DEV-05 c1). The generator and the judge appear to
  share this misreading.

## 9. Error analysis (dev, confirmed vs hypothesised)

| Failure category | Cases | Observed | Expected | Likely cause | Remediation |
|---|---|---|---|---|---|
| Pretrained-knowledge error (A) | DEV-07, 10, 13 | Wrong validity period; wrong under-21 route | 9 months; core occupier | No evidence (confirmed) | Retrieval (B fixes these cases) |
| Retrieval miss | 9/18 cases miss ≥1 gold fact at k=12 | Generation lacks some facts | Gold facts present | Lexical gap between colloquial questions and fact text; multi-fact questions (confirmed by recall) | Rule-linked facts (C, by design); more aliases from dev misses only |
| Evidence over-generalisation (B) | DEV-07, 10, 13 | "Engaged couples unconfirmed" | Unconfirmed only for FT(PMC) | Gap note retrieved out of context (hypothesis) | Retrieve gap notes only on matching topics (C's topic filter); verifier (D) |
| Conflict not detected | DEV-13, 14, 15 | No conflict listed (A and B) | Neutral clarification | The LLM is not asked to compare statements systematically (hypothesis) | Deterministic conflict checks on the extracted profile (C) |
| Verifier false approval: wrong applicant category | DEV-01 c2, DEV-13 c1, DEV-13 c3, DEV-17 c2 | Shown as verified | Contradicted | Fact names a sub-group (FT(PMC)) and the claim generalises it; the same model generates and judges (hypothesis) | Pass `applies_to` metadata to the judge and check it deterministically; a different judge model family (A5) |
| Verifier missed contradiction ("both must be SC") | DEV-01 c3, DEV-07 c3, DEV-16 c3 | Unconfirmed, not withheld | Contradicted | The judge treats "stricter than the fact" as "not stated" (confirmed by rationales) | Prompt example for stricter/looser conditions; rule-based citizenship check (C) |
| True correction shown as unconfirmed | DEV-11 c1 | "Engaged couples can apply without marrying" unconfirmed | Supported by HH-COUPLE-001 | Generator did not cite the fact (deterministic rule: no citation → insufficient) | Rule-linked facts and a citation prompt (C); not a verifier error |
| Rate-limit configuration | DEV-12 (B) | HTTP 413 "request too large" | An answer | `max_completion_tokens` 6000 + prompt exceeded the 8K tokens/min plan (confirmed) | Cap lowered to 4096 for future runs; saved run unchanged |

## 10. Limitations

- **C is not built**, and **D runs on B rather than C** (D-071). The rule engine exists and is
  unit-tested but does not influence answers, so the "deterministic rules" half of the hybrid
  hypothesis is untested.
- **The verifier evaluation uses agent annotations made after the run**, on 49 claims from
  one run. Counts this small (e.g. 4/8) have very wide uncertainty and are not statistically
  significant. The verifier shares the generator's model, so the errors are not independent.
- **No blind primary scoring and no held-out run.** Results are dev diagnostics from one run
  per configuration on 18 synthetic cases, with no statistical power. The benchmark is still
  a candidate (not frozen).
- **Model:** failed its own pre-registered direct-generation thresholds. The alternative was
  unavailable during the session.
- **Retrieval recall is low** (0.52 at k=12).
- **Temporal fairness:** A relies on older pretrained knowledge, while B reads an October
  2026 snapshot. B's advantage on facts partly reflects recency, not better reasoning.
- **Policy currency:** facts reflect the 2026-10-28 snapshot. A live-page drift check (G-15)
  and the final rights clearance are pending.
- **Structured output:** strict mode is not airtight on the provider (one invalid enum was
  observed and recovered by the retry). Latency includes waits for the free-plan rate limit.

## 11. Deployment considerations

*(Described, not implemented.)* **Target users and environment:** first-time couples
preparing for a BTO application, using a web assistant run by a public agency. It sits
beside the official HDB Flat Portal, not inside it, and never collects NRIC or Singpass
data. **Cost at scale:** configuration B used about 2,650 input and 520 output tokens per
query, about US$0.0007 at gpt-oss-120b list prices; the verifier adds about US$0.0003. That
is roughly US$100 a month for 100,000 verified queries. C's extraction call would add about
another US$0.0005. Retrieval and rules run on the CPU at negligible cost. **Monitoring:**
weekly blind audits of sampled answers for critical-error rate; the share of policy claims
with a valid citation; evidence-gap and out-of-scope rates by topic (a rise signals coverage
holes); schema-failure and API-error rates; p95 latency and cost per query; and user
"was this helpful" feedback. **Key risk: policy drift.** HDB changes a rule, for example the
HFE validity period, while the knowledge base still holds the old fact, so the assistant
confidently cites an official page that no longer says what it claims. Mitigation: monthly
re-capture of source pages, with automated hash comparison flagging changed sections; facts
from changed sections are suspended until re-verified; and every answer shows the
"sources retrieved" date.

## 12. Development narrative

- **Phase 0–1:** turned the brief and my own planning approach document into a requirements register
  and a decision log (`docs/decisions.md`, D-001 onward). Scaffolded with uv, Docker and
  Streamlit.
- **Phase 2:**
  - Automated capture (Playwright) was **dropped** after HDB returned 403. Bypassing the
    block would have undermined the "lawful access" defence, so capture became manual
    (D-055, D-056).
  - A PDF-parsing dependency was rejected in favour of manual review of 6 pages (D-052).
  - The HFE FAQs were dropped for robots.txt (D-060).
  - Facts were authored and verified against hash-pinned snapshots (D-058). The rules were
    kept as declarative YAML rather than code (D-038, D-062).
- **Phase 3a:** benchmark and rubric written **before** any prompt work. Held-out labels
  were sealed with a hash commitment (D-063, D-064). Rule-ID recall was replaced by
  architecture-neutral content key points, so the A–D comparison stays fair (D-066).
- **Phase 3b:**
  - **Model selection:** pre-registered; Gemini unavailable; Groq chosen despite failing its
    thresholds, with that disclosed (D-067).
  - **Baseline A:** built with fail-closed handling and 25 failure-mode tests.
  - **Time-boxing:** with about 1.5 h left, C and D were deferred in favour of B, a working
    Docker build and this documentation (D-069). With one hour left, D was chosen over C
    because it needed one module rather than five, and could re-verify B's saved answers for
    a clean ablation (D-071). Every failed attempt (an aborted harness
    run, Cloudflare and 413 errors) is recorded in `docs/development_log.md`.
- **Tooling:** uv (reproducible lockfile); Pydantic (typed contracts); `openai` client
  (provider-agnostic); `rank-bm25` (deterministic, explainable retrieval); stdlib for
  evaluation.

## 13. AI coding agent usage

- **Tool:** Claude Code (Anthropic), used throughout for requirements extraction, design
  drafting, code, tests and documentation.
- **Developer's role:** every decision was approved by the developer and recorded with an ID
  in `docs/decisions.md`. The agent never committed or pushed.
- **Constraints the agent worked under:**
  - It read private source snapshots only for fact authoring (D-054, with model training
    turned off for the account).
  - It never opened held-out labels (D-064).
  - It flagged rather than hid failures, such as the model's threshold failure.
- **Session logs:** exported to `ai_logs/` *(to be added by the developer before submission;
  any redactions of private source text or identifying details will be listed in
  `ai_logs/REDACTIONS.md`)*.
