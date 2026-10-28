# BTO Buddy — Project Context Index

This is a structured, traceable knowledge base built from the project's two private planning
sources:
- the **assessment brief** (`[ASM p.N]`);
- the **project-approach document** (`[APP p.N]`).

Both PDFs are kept locally and are Git-ignored. This documentation is independently
authored: it paraphrases requirements and policy content rather than reproducing them.

**Status (2026-10-29):** Phases 0, 1, 2a and 2b are complete. **D-044 to D-062 are all
APPROVED** (D-054 and D-058 as revised).
- **Phase 2b output:** 89 authored facts (`kb-2026-10-28.1`), of which 51 are `verified`,
  including all 47 critical ones.
- **Rules:** a 24-rule registry (`rules-2026-10-29.1`).
- **Supporting data:** a coverage matrix and visual resources.
- **Scope:** approved (D-061). The HFE FAQs are excluded because robots.txt disallows them
  (D-060).
- **Details:** [../data_sources.md](../data_sources.md) §12–§19, with scope boundaries and
  evidence gaps in §17.

**Phase 3a (benchmark design, 2026-10-29):**
- A candidate benchmark of 48 cases (18 dev / 30 sealed held-out), with its rubric and claim
  protocol: [../evaluation_benchmark.md](../evaluation_benchmark.md).
- Metric specification (architecture-neutral primary metrics, diagnostics, failure handling):
  [../../evaluation/metric_spec.md](../../evaluation/metric_spec.md).
- D-063 to D-066 are PROPOSED.
- Dev labels approved; the developer reports the held-out review complete (2026-10-29).
- The benchmark is **not frozen** until the developer confirms and approves the freeze.

**Phase 3 carried to-dos:**
1. live-page drift check;
2. rights clearance;
3. README data section with the D-054/D-057 disclosures.

**What exists:**
- the uv project and lockfile, Docker image and Streamlit shell;
- `src/bto_buddy/schemas.py` (KB and rule contracts) and `policy.py` (KB loader, rule
  interpreter, validators);
- `data/`: `sources_manifest.json`, `policy_facts.jsonl`, `policy_rules.yaml`,
  `source_coverage.csv`, `visual_resources.json`, and `corpus/` (checklist, reports,
  verification, version);
- `scripts/snapshots.py` and `scripts/corpus.py`;
- `evaluation/`: benchmark loader and validator, dev cases, held-out inputs, manifest,
  claim template (held-out labels in Git-ignored `evaluation/heldout/`);
- tests: smoke, corpus tooling, KB, rules, benchmark.

**Phase 3b (2026-10-29):** model chosen (D-067: `openai/gpt-oss-120b` on Groq; Gemini gave no
output, and the pre-registered acceptance thresholds were not met in direct generation).
Configuration A (direct LLM) is built: `llm.py`, `generation.py`, `pipeline.py`,
`prompts/generate_v1.md`, `evaluation/run.py`; dev run `20261028T203350Z-A-dev`. Contract
additions are D-068 (PROPOSED). **Config B (BM25 RAG) is built (D-069, D-070); C and D are
deferred.** The README holds the results and limitations; the dev runs are A
`20261028T203350Z-A-dev` and B `20261028T205255Z-B-dev`.

## Files

| File | Covers |
|---|---|
| [01_problem_and_scope.md](01_problem_and_scope.md) | Final idea, problem statement, research question, problem validation, **MVP scope**, HFE/income boundaries, supported-question draft, missing-information categories, demo archetypes |
| [02_policy_sources.md](02_policy_sources.md) | Seed sources, discovery method, **complete source-discovery matrix**, infographic/video registry candidates, **media-handling decisions**, policy nuances to verify |
| [03_data_and_licensing.md](03_data_and_licensing.md) | Datasets A/B/C, private vs reviewer-facing corpora, manifest, schemas, completeness checks, licensing/robots/copyright, privacy, reproducibility, limitations |
| [04_architecture.md](04_architecture.md) | Pipeline, coverage gate, missing-information contract, representation principles, verifier behaviour, proposed stack, provider comparison, model scorecard |
| [05_evaluation.md](05_evaluation.md) | Configurations A–D, **benchmark structure**, label protocol, proposed split, **metric definitions**, severity rubric, retrieval and verifier evaluation, statistics, failure taxonomy |
| [06_submission_requirements.md](06_submission_requirements.md) | Mandatory deliverables, scoring dimensions, non-compliance indicators, resources, AI-log rules, README requirements |
| [requirements_register.md](requirements_register.md) | **All requirement IDs** with source pages, components and acceptance evidence; contradictions; open questions; completeness audit |
| [../decisions.md](../decisions.md) | Decision log (D-001 onward, BD-00…BD-09) and the instruction priority |
| [../architecture.md](../architecture.md) | **Approved implementation design** (D-030 to D-040): pipeline, contracts, retrieval choice, dependencies, tests |
| [../data_sources.md](../data_sources.md) | **Dataset A sources (current state):** source IDs and classes, matrix reconciliation, relationships, dependencies, coverage, rights checks, manual acquisition and audit, corpus layers, manifest schema, reproducibility, open gaps |
| [../development_log.md](../development_log.md) | Progress per phase, verified commands, failures, next steps |
| [../../CLAUDE.md](../../CLAUDE.md) | Working instructions for coding agents (scope, invariants, Git workflow, commands) |

## Legend

**Status**

| Tag | Meaning |
|---|---|
| `MANDATORY` | Explicit requirement in the assessment brief |
| `APPROVED` | Final project decision (in the project approach as final, or ratified/added in [decisions.md](../decisions.md)) |
| `PROPOSED` | Technical alternative or implementation detail not yet approved |
| `OPEN` | Cannot be resolved from the sources or decisions; needs a developer answer |
| `HISTORICAL` / `SUPERSEDED` | Earlier idea or decision replaced by an approved one. Kept for traceability, **not** an active requirement |

**Provenance**

| Tag | Meaning |
|---|---|
| `COPIED-SOURCE` | The project-approach PDF quoted HDB text verbatim at this point. The quotation is **not** reproduced in tracked files |
| `AUTHORED-FACT (unverified)` | Independently paraphrased policy statement. It must be verified against a frozen source before it enters `data/policy_facts.jsonl` |
| `PROJECT-DECISION` | Design choice by the developer (the default for non-policy content) |
| *Author observation* | Point raised while building this knowledge base, not stated in either source |

## Instruction priority (D-001)
1. Mandatory assessment requirements.
2. The developer's latest explicit instructions and approved decisions.
3. Finalised scope, architecture, data strategy and evaluation methodology.
4. The current approved implementation task.
5. Proposed alternatives and open questions.
6. Historical or superseded brainstorming.

## Where to look for a task
| Task | Read |
|---|---|
| Any task | `CLAUDE.md`, then this index |
| Scope questions | 01, plus D-008 / D-013 / D-033 in [decisions](../decisions.md) |
| Source capture, extraction, facts | [data_sources](../data_sources.md) first, then 02, 03, [architecture §5](../architecture.md) |
| Pipeline code | [architecture.md](../architecture.md) (§3 stages, §5 contracts, §11 modules, §12 tests), 04 |
| Benchmark and evaluation | 05, register (REQ-EVL-*) |
| README and submission | 06, register (REQ-SUB-*, REQ-DOC-*) |
| History and current state | [development_log.md](../development_log.md) |

## Current open items
- **Contradictions open:**
  - C-14 (URL mismatch in the matrix, Q-24);
  - C-15 and C-16 (metric gaps, Q-16 and Q-15);
  - C-17 (privacy missing from the scorecard, Q-13).
- **Questions open:**

  | Needed by | Questions |
  |---|---|
  | Phase 2 | Q-06, Q-07, Q-08, Q-09, Q-11, Q-22, Q-24 |
  | Model selection | Q-13 |
  | Before evaluation | Q-14, Q-15, Q-16, Q-17 |
  | Before dataset creation | Q-20, Q-21 |
  | Pre-submission | Q-19 |

- **Resolved:** Q-05, Q-10, Q-12, Q-18, Q-23.
- **Awaiting confirmation:** the `llm.py` addition in D-041.
- **Execution risk:** C-09 / Q-19 (log anonymity vs completeness).

Details are in [requirements_register.md §2–3](requirements_register.md#2-contradictions). The
consolidated list with owners and deadlines is in the
[development log](../development_log.md#unresolved-issues-carried-forward).
