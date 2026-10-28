# BTO Buddy — Project Context Index

This is a structured, traceable knowledge base built from the project's two private planning
sources:
- the **assessment brief** (`[ASM p.N]`);
- the **project-approach document** (`[APP p.N]`).

Both PDFs are kept locally and are Git-ignored. This documentation is independently
authored: it paraphrases requirements and policy content rather than reproducing them.

**Phase:** 0 (context building).
**Created:** 2026-10-28.
**Code, models or datasets:** none have been implemented, selected or created.

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
| [../decisions.md](../decisions.md) | Decision log (D-001…D-025, BD-00…BD-09) and the instruction priority |

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

## Current open items
- **Contradictions still open:** C-14 (URL mismatch in the matrix), C-15 to C-17 (metric
  and scorecard gaps).
- **Questions:** Q-05 to Q-24.
- **Execution risk:** C-09 / Q-19 (log anonymity).

All are listed in [requirements_register.md §2–3](requirements_register.md#2-contradictions).
