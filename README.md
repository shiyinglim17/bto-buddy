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
  private source snapshots.
- Without an API key the app starts and shows a clear "No LLM API key is configured" message.
- Verified on 2026-10-29 (macOS, Docker): the build succeeded, the health endpoint returned
  200, and a live configuration-B answer ran inside the container.

**Local development** (uv 0.13.6, Python ≥ 3.12):

```bash
uv sync                                   # exact versions from uv.lock
uv run pytest                             # 135 offline tests, no API key needed
uv run ruff check . && uv run mypy        # lint + strict typing
uv run streamlit run src/bto_buddy/app.py
```

**Offline vs live.** `pytest`, lint, typing, the KB loader and retrieval are deterministic
and offline. Anything that calls the model (the app, `evaluation.run run`) is a **live,
potentially non-deterministic API experiment**, even at temperature 0. Saved predictions in
`evaluation/results/` are the reproducible record, and the diagnostics can be recomputed from
them without an API key:

```bash
uv run python -m evaluation.run diagnostics 20261028T203350Z-A-dev 20261028T205255Z-B-dev 20261028T211724Z-D-dev
uv run python -m evaluation.run run --config B --split dev     # live re-run (needs a key)
uv run python -m evaluation.run verify <B_run_id>              # D from B's saved answers (needs a key)
```

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
  answers)**. B vs C and C vs D need C.
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

> **Preliminary and diagnostic only.** 18 dev cases, one run per configuration, and no blind
> primary scoring yet. These numbers describe **what the structured output contains**, not
> whether it is correct, except for the verifier table, which is claim-level. **No claim is
> made that B or D is better overall.** Source: `evaluation/results/diagnostics_dev.json`.

| Diagnostic (dev, n = 18) | A: direct | B: retrieval | D: B + verifier |
|---|---|---|---|
| Failed cases (kept in all counts) | 0 | 1 (DEV-12: HTTP 413) | 1 (inherited from B) |
| Generation retries | 0 | 1 | 1 (same answers as B) |
| Required missing fields listed in `missing_profile_fields` | 2/6 | 3/6 | 3/6 |
| Expected conflicts flagged in `profile_conflicts` | 0/3 | 0/3 | 0/3 |
| Out-of-scope requests flagged | 3/3 | 3/3 | 3/3 |
| Whole answer refused on answerable cases | 0/9 | 0/9 | 0/9 |
| Policy claims shown with an official source link | 0/34 | 33/35 | 28/35 (verified only) |
| Claims withheld / shown as unconfirmed | n/a | n/a | 1 / 15 of 49 checked |
| Answer coverage proxy (in-scope cases with ≥1 substantive claim not withheld or unconfirmed) | 15/15 | 14/15 | 14/15 |
| Median latency per case (includes rate-limit waits) | 4.3 s | 15.7 s | 21.5 s |
| Total cost, 18 cases (list price) | US$0.0095 | US$0.0127 | US$0.0182 (+43% over B) |

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

**Observed behaviour** (developer review pending; observations, not scores):
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

- **Phase 0–1:** turned the brief and the approach document into a requirements register
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
