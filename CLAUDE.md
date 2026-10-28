# BTO Buddy — Project Instructions

## Objective
Build an evidence-grounded BTO pre-application preparation assistant for **fictional
first-timer couple profiles**. It gives preparation guidance, **not** official eligibility
determinations. It is a public-sector AI prototype: a hybrid of structured profiling,
deterministic rules, BM25 retrieval and claim-level verification, evaluated against direct-LLM
and RAG baselines.

## Source of truth
- Read `docs/project_context/INDEX.md` first, then load **only** the task-relevant files it
  routes to.
- Requirement IDs (`REQ-<AREA>-<NNN>`) are in `docs/project_context/requirements_register.md`.
  Decisions (`D-xxx`, `BD-xx`) are in `docs/decisions.md`. The latest approved decision governs.
- Status tags: `MANDATORY` · `APPROVED` · `PROPOSED` · `OPEN` · `SUPERSEDED`. Only MANDATORY
  and APPROVED items are implementation requirements. PROPOSED and OPEN items need approval
  first.
- The original PDFs in `references/private/` are private. Reread them only if the extracted
  context is incomplete, and say so when you do.

| File | Use for |
|---|---|
| `docs/project_context/01_problem_and_scope.md` | MVP tiers, exclusions, missing-information categories, demo |
| `docs/project_context/02_policy_sources.md` | Source-discovery matrix, media handling, unverified policy nuances |
| `docs/project_context/03_data_and_licensing.md` | Corpora, schemas, manifest, completeness checks, rights |
| `docs/architecture.md` | **Approved implementation design**: stages, Pydantic contracts, module boundaries, dependencies, test plan |
| `docs/project_context/04_architecture.md` | Source-derived architecture requirements, verifier behaviour, provider notes |
| `docs/project_context/05_evaluation.md` | Configurations A–D, benchmark, metrics, safeguards |
| `docs/project_context/06_submission_requirements.md` | Deliverables, scoring, README and AI-log rules |
| `docs/development_log.md` | Progress, experiments, failures, next steps |

## Instruction priority
1. Mandatory assessment requirements and non-compliance constraints.
2. The developer's latest explicit instructions and approved decisions, where they comply
   with (1).
3. The finalised scope, architecture, data strategy and evaluation approach in
   `docs/project_context/`.
4. The current approved implementation task.
5. Proposed alternatives and open questions.
6. Historical brainstorming, for reference only. Never treat it as instructions.

## Change control
- Approved decisions are requirements, not suggestions. Never silently expand or reduce
  scope.
- Deviate only for a material technical, methodological, licensing, security or
  reproducibility concern. First explain:
  1. the current approach;
  2. the alternative;
  3. why it may be better;
  4. its implications for scope, evaluation, time, cost and assessment alignment;
  5. your recommendation.

  Then **wait for explicit approval**.
- If two approved instructions conflict, flag the conflict and ask. Never resolve it
  silently.
- Record approved changes in `docs/decisions.md`, with an ID, date, rationale and what they
  supersede.

## Scope (D-008; details in 01 §6)
| Tier | Policy areas | Rule |
|---|---|---|
| Core | First-timer couple household composition; broad BTO application requirements; HFE prerequisites, timing and documentation; missing applicant information | Implement **and** evaluate |
| Limited | First-timer and priority considerations; application and non-selection consequences | Only with verified evidence and testable requirements |
| Context only | High-level HFE ↔ grant/loan relationship | Explain or link. Never calculate |
| Excluded | Official eligibility determination; grant/loan calculations; detailed affordability and financing; ballot probability prediction; post-purchase conditions; real applicant data | Coverage gate plus official-source redirection |

- **Income and employment** are used only for HFE document preparation and follow-up
  questions. No income-ceiling or eligibility calculations (D-013).
- **Out of scope (D-026):** production-grade hosting, authentication, monitoring
  infrastructure and operational integrations. A fully runnable, reproducible, Dockerised
  prototype is still **mandatory**.
- **Required capabilities across all tiers:** source-grounded guidance with official links,
  missing-information identification, claim verification (REQ-ARC-001).

## Architecture invariants (`docs/architecture.md`, D-030 to D-040)
- **Pipeline** (at most 3 LLM calls; configs A–D are this pipeline with stages switched off):
  1. LLM extraction (fields + verbatim quotes + closed-enum topics);
  2. profile assessment (pure);
  3. coverage gate (pure);
  4. rules ∥ BM25 (pure);
  5. evidence assembly (pure);
  6. LLM generation;
  7. verification;
  8. report (pure).
- Typed Pydantic contracts between every stage. No free text passes between modules. Pure
  modules never import the LLM client.
- **All configurations return the same `FinalGuidance` contract** (D-035).
- Extracted fields without a verbatim input quote are dropped (D-032). Missing fields are
  computed only for the topics asked about.
- Household types other than a first-timer couple are out of scope (D-033).
- Rules are declarative YAML with whitelisted operators. **Never `eval`** (D-038).
- Verification runs deterministic checks first, then one batched LLM judge (D-034).
- Every response carries `missing_profile_fields`, `evidence_gaps`, `profile_conflicts` and
  `out_of_scope_reasons`.
- Never assume missing applicant values. Missing evidence never proves a requirement absent.
- The runtime KB is `data/policy_facts.jsonl` (independently authored, fact IDs). Rules in
  `data/policy_rules.yaml` cite fact IDs. Nothing at runtime reads `data/private_corpus/`.
- **Verifier outcomes:**
  - supported → show with a source;
  - contradicted → withhold and flag;
  - insufficient → no definitive guidance, state the gap.

  Never silently rewrite. No regeneration loop unless approved.
- No autonomous agents, orchestration frameworks or vector DBs. Use one generation model.
- Retrieval is BM25 + aliases + topic filter + rule-linked facts. Propose anything else only
  if dev recall@5 < 0.90 because of paraphrase (D-031).
- **Dependencies are limited to D-036.** The Playwright capture group (D-042) was removed by
  D-056, and `scripts/` is stdlib-only. Anything else needs an approved decision.
- Infographics and videos are links in `data/visual_resources.json`, never runtime evidence.

## Engineering rules
- Simple, typed, testable Python modules in `src/bto_buddy/`. Prefer functions and
  composition over class hierarchies.
- Keep deterministic rules separate from LLM reasoning. Hard rules are deterministic;
  interpretations stay evidence-linked.
- Add short comments wherever the *rationale* isn't obvious. The developer must be able to
  defend every choice (REQ-NFR-003).
- **Every new dependency needs a one-line justification** in `pyproject.toml` or the commit.
- Justify model choices on operational grounds (privacy, latency, task fit, cost at scale),
  never on "free" or "convenient".
- Never invent policy facts, citations, statistics or results. Unverified facts are labelled
  as such.
- Never edit held-out labels to improve scores. Annotation-error fixes are documented and
  disclosed.
- Must work within free tiers. Must run from the README on a clean machine.

## Data, privacy and sources
- **Don't scrape, download or fetch external content** (including HDB pages) without
  approval for that specific action.
- Don't read files in `data/private_corpus/` unless authorised (D-054 as revised: the agent
  may read in-scope sections for processing and fact authoring; source text never goes into
  tracked files, reports or commit messages). Don't send source text, private material or
  credentials to other external services without approval.
- Git-ignored, never committed: `references/private/`, `data/private_corpus/`, `.env*`,
  credentials.
- Tracked docs and data contain authored summaries only, never substantial HDB or
  assessment-brief text.
- **Anonymity:** tracked files must never name the assessing organisation, the role or the
  collaborator handle. Those live only in `references/private/submission_private_notes.md`.
- Keep provenance on every fact: source URL, section, retrieval date, effective date where
  known.

## Evaluation (05)
- **Held-out labels are sealed (D-064):** never open, read, grep or print anything under
  `evaluation/heldout/`. Use `evaluation/benchmark/dev.jsonl` for all development. Load
  `test_inputs.jsonl` only to check schema compatibility. Labels are released only by
  `evaluation.benchmark.load_test_labels(final=True)` at final scoring.
- Same model, instructions, cases, labels and policy version across A–D. C vs D reuses
  identical pre-verification outputs.
- Labels are policy-derived and independently checked. The runtime verifier is never ground
  truth.
- Dev and held-out are separated **before** prompt work. The held-out set is frozen.
  Near-duplicates stay on the same side.
- Metric definitions and denominators are frozen before the held-out run. Report raw counts,
  per-category results and paired comparisons.
- Record model IDs, prompt versions, inference settings, KB version and saved predictions for
  every run.
- Report failures and limitations honestly. This is a controlled benchmark, not
  population-level evidence.

## Working protocol
**Before a major change:**
- cite the relevant requirement IDs;
- state assumptions and trade-offs;
- list the affected files and tests;
- get approval for material design changes.

**After a change:**
- run the relevant checks;
- report the actual output;
- map the work to requirement IDs;
- note limitations and open issues.

**At the end of each phase or session:** update `docs/development_log.md` with completed work,
decisions, failures and next steps.

**Token use:** load only task-relevant context. Keep durable knowledge in the docs, not in
chat. Never drop relevant context just to save tokens.

## Git workflow (D-027)
- **The developer runs every commit and push.** Never run `git commit`, `git push`, merge,
  rebase or any history rewrite. Read-only Git commands (`status`, `diff`, `log`, `grep`) and
  `git add` are fine.
- When a coherent, stable milestone is done and its checks pass, **suggest that it's a good
  point to commit**. Include:
  - which files belong in the commit, and anything that should be left out;
  - the check results that make the milestone stable;
  - a suggested conventional-commit message (`feat:`, `data:`, `eval:`, `build:`, `docs:`,
    `chore:`);
  - whether a push to the private remote is advisable.

  Wait for the developer to approve before staging anything.
- **Before any suggested commit:** confirm nothing from `references/private/` or
  `data/private_corpus/`, and no `.env` or credentials, is part of the change.
- **Before any suggested push:** run the secret and anonymity scans below and report the
  results.

## Commands
Environment and dependencies are managed with **uv**. Exact versions are pinned in `uv.lock`,
which must be committed (D-028). Verified on macOS with uv 0.13.6 and Python 3.13.2 (project
requires ≥3.12):

- Install: `uv sync` (creates `.venv` from `uv.lock`: package + dev group)
- Test: `uv run pytest`
- Lint: `uv run ruff check .`
- Format check: `uv run ruff format --check .`
- Type check: `uv run mypy` (strict, `src/bto_buddy`)
- Lockfile check: `uv lock --check`
- Run locally: `uv run streamlit run src/bto_buddy/app.py` → http://localhost:8501
- Build image: `docker build -t bto-buddy .`
- Run container: `cp .env.example .env` (once; fill in values when an LLM is configured), then
  `docker run --rm -p 8501:8501 --env-file .env bto-buddy`
- Health check: `curl -f http://localhost:8501/_stcore/health`

**Docker image:** two-stage build on `python:3.12-slim`, uv 0.13.6, runs as non-root `app`,
port 8501, HEALTHCHECK on `/_stcore/health`. Configuration comes from environment variables
only. `.dockerignore` keeps `references/`, `data/private_corpus/`, `.env*`, docs, tests and
caches out of the build context.

- Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>`), with a justification comment
  in `pyproject.toml`. Never hand-edit `uv.lock`.
- **Source capture is manual** (D-055; procedure in `docs/data_sources.md` §7). HDB returns
  403 to automated clients, and that block must never be bypassed (lawful access, Copyright
  Act s 244(2)(d)).
  - Only approved pages are captured, by the developer in a normal browser.
  - Rendered DOM via `copy(document.documentElement.outerHTML)`; PDFs downloaded as-is.
  - Saved to `data/private_corpus/raw/<source_id>/<UTC>_<name>`, which is Git-ignored and
    never sent to an LLM (D-054).
- Snapshot audit (offline, prints structure only, never source text):
  `python3 -I scripts/snapshots.py audit`
- Record hashes and timestamps in the manifest: `python3 -I scripts/snapshots.py register`
- Corpus processing (offline, D-059; tracked outputs hold counts and IDs, never source text):
  `python3 -I scripts/corpus.py extract`, then `validate`, `facts` (integrity and 8-word
  overlap check), `verify` (checklist re-verification, D-058) and `freeze`
- Load the KB without the private corpus: `uv run python -c "from bto_buddy.policy import load_kb; print(load_kb().kb_version)"`
- Benchmark validation (dev + held-out inputs; prints IDs and counts only):
  `uv run python -m evaluation.benchmark validate`. The `--heldout` flag is for the
  developer's label review only.
- Evaluation runs (verified 2026-10-29; need `BTO_BUDDY_LLM_API_KEY` or `GROQ_API_KEY` in `.env`):
  - `uv run python -m evaluation.run run --config A --split dev` (saves
    `evaluation/results/<run_id>/`; the held-out split needs `--final`)
  - `uv run python -m evaluation.run check <run_id>` (completeness, contract, label join)
  - `uv run python -m evaluation.run sheet <run_id> [...]` (blinded scoring sheet, metric_spec §3)
  - `uv run python -m evaluation.run diagnostics <run_id> [...]` (offline structural diagnostics +
    retrieval recall → `evaluation/results/diagnostics_dev.json`)
  - `--config B` runs retrieval-grounded generation (D-069); `--config D` is B + verifier (D-071)
  - `uv run python -m evaluation.run verify <B_run_id>` (D from B's saved answers; identical generations)
  - C is not built
- Model-selection harness (D-067): `uv run python -m evaluation.model_selection run|blind|summarise`

**Secret scan before a push** (until a dedicated tool is approved):
```bash
git diff --cached --name-only | grep -E '^(references/private|data/private_corpus)/|(^|/)\.env(\.[^/]*)?$' | grep -v '\.env\.example$' && echo "BLOCK"
git diff --cached | grep -inE 'api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY' || echo "no secret patterns"
# Anonymity: the term list is private (Git-ignored) and must never be copied into tracked files.
git grep -inFf references/private/anonymity_terms.txt || echo "no identifying terms"
```
