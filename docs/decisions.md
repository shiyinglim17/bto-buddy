# Decision Log

This is the authoritative record of project decisions. When two sources conflict, the latest
decision approved here governs, provided it complies with the mandatory assessment
requirements (D-001, D-012).

**Status values:** `APPROVED`, `PROPOSED`, `SUPERSEDED`, `OPEN`.
**Source tags:** `[ASM p.N]` = assessment brief, page N; `[APP p.N]` = project-approach
document, page N; `[DEV 2026-10-28]` = developer clarification given on that date.

Both source PDFs are private (Git-ignored). The requirements they contain are catalogued in
[project_context/requirements_register.md](project_context/requirements_register.md).

---

## Instruction priority (D-001)

1. Mandatory assessment requirements.
2. The developer's latest explicit instructions and approved decisions, where compatible with the assessment.
3. The finalised project scope, architecture, data strategy and evaluation methodology.
4. The current approved implementation task.
5. Proposed alternatives and unresolved questions.
6. Historical or superseded brainstorming.

Any material improvement or conflict found later must be raised with:
- the current approach;
- the alternative;
- the trade-offs;
- the assessment implications.

The developer must approve it before any deviation.

This replaces the hierarchy in [APP p.1], which is recorded as superseded in BD-00.

---

## Decisions approved 2026-10-28

| ID | Decision | Status | Resolves | Rationale | Supersedes |
|---|---|---|---|---|---|
| D-001 | Status taxonomy: MANDATORY, APPROVED, PROPOSED, OPEN, HISTORICAL/SUPERSEDED. The instruction priority above applies. Approved areas: final MVP scope, canonical reviewer-facing KB, hybrid architecture, evaluation safeguards, source-handling restrictions. Decided later by evidence-based selection: LLM provider/model, retrieval improvements beyond BM25, verifier model, statistical tests, implementation optimisations | APPROVED | Proposal Q1 | Makes approval status explicit for every item | APP p.1 hierarchy (BD-00) |
| D-002 | Canonical name **BTO Buddy**. Repo/distribution `bto-buddy`; Python package `bto_buddy`; application name "BTO Buddy". "BTOPath" is a superseded working name | APPROVED | C-01 | One consistent name across code and docs | "BTOPath" [APP p.3, 21, 24, 25] |
| D-003 | Four system configurations: A Direct LLM (profile + question, no retrieval, no rules); B RAG (same model + retrieved evidence); C Hybrid (structured profiling + deterministic rules + RAG); D Hybrid + runtime factual verification. All use the same generation model, equivalent task instructions and the same benchmark cases wherever applicable. C vs D reuses identical pre-verification outputs. If time is short, run A, C and D and document why B was omitted | APPROVED | C-02 | Ablation isolates the effect of each component | 3-configuration design [APP p.3] |
| D-004 | **Primary metrics:** critical-error rate, required-rule recall, missing-information recall, unsupported-claim rate, appropriate abstention. **Supporting metrics:** citation precision, factual correctness, answer coverage, latency, inference cost. **Component evaluations:** retrieval recall@k on labelled queries; runtime verifier on independently labelled supported/contradicted/insufficient claims. All metrics are defined operationally, with denominators, before evaluation. The critical/major/minor severity rubric is kept | APPROVED | C-03 | Puts safety first and makes each component measurable | Primary/secondary list [APP p.24]; table [APP p.26] (definitions kept) |
| D-005 | `data/policy_facts.jsonl` is the canonical runtime, retrieval and primary-evaluation KB. HTML snapshots and source-derived passages live under `data/private_corpus/`, for local auditing, extraction and completeness validation only. Running the app and the reviewer evaluation must not depend on the private corpus | APPROVED | C-04 | Reproducible on a clean machine and rights-compliant | Tech-table row "Knowledge base: curated official HTML/text passages" [APP p.21] |
| D-006 | The rule registry references stable, reviewer-accessible **fact IDs**. These resolve to official URLs and sections through the source manifest. Private passage IDs may be kept for provenance but are never needed at runtime | APPROVED | C-05 | Reviewers can resolve every rule citation | `source_passage_id` in the rule example [APP p.15] |
| D-007 | The four HDB pages are **seed sources**, not necessarily the complete corpus. The minimum MVP source set will be decided in Phase 2. Nothing is included just because it appears in the source-discovery matrix. Don't claim a four-page corpus until coverage validation confirms it | APPROVED | C-06 | Coverage is decided by evidence | "four official HDB webpages" wording [APP p.14] |
| D-008 | The MVP scope table is authoritative. Core: first-timer couple household composition, broad BTO application requirements, HFE prerequisites/timing/documentation, missing applicant information. Limited, source-verified: relevant first-timer/priority considerations; application/non-selection consequences. Context only: high-level relationship between HFE, grants and loans. **Excluded:** grant/loan eligibility calculations, detailed financing, **ballot probability prediction**, post-purchase conditions, **comprehensive official eligibility determination**. The supported-question inventory must reflect these tiers | APPROVED | C-07 | One authoritative scope. Ballot prediction and comprehensive determination are added to the exclusions | Supported-question list [APP p.5] |
| D-009 | Upload the **complete project-specific coding-agent session and chat logs**, not selected sessions. Replace every reference to "essential logs". Disclosing ChatGPT planning use is not required. Full non-coding brainstorming transcripts are not included automatically | APPROVED | C-08 | The brief requires all coding-agent logs [ASM p.4] | "Essential coding agent sessions and chat logs" [APP p.30]; ChatGPT paragraph in the draft disclosure [APP p.31] (now removed) |
| D-010 | Keep the complete coding-agent history, including Phase 0. Before submission, audit logs for identifying information, credentials, sensitive local paths and restricted source material. Redact only what genuinely needs protection, keep the structure and substance, and document every redaction in `ai_logs/redactions.md`. Never remove failed sessions or rewrite prompts. If completeness and anonymity can't both be met with confidence, escalate to the developer | APPROVED | C-09 | Balances two mandatory requirements | — |
| D-011 | Verifier outcome handling. **Supported:** show the claim with a verified source reference. **Contradicted:** withhold the unqualified claim and flag the contradiction. **Insufficient evidence:** give no definitive guidance; state the evidence gap or the need for official confirmation. Never silently rewrite. One controlled regeneration is an optional improvement and needs approval before it is implemented | APPROVED | C-10 | Errors are never shown without a flag | "remove / label / regenerate once" options [APP p.22] |
| D-012 | Keep this decision log. The latest explicitly approved decision governs, provided it complies with the assessment | APPROVED | C-11 | Lets decision recency be determined | — |
| D-013 | Income/employment information is used only where needed for HFE preparation, document identification and follow-up questions. No comprehensive income-eligibility calculation, income-ceiling determination or financing calculation. Income exceptions enter the benchmark only if they are within preparation scope and backed by verified policy evidence | APPROVED | C-12 | Prevents scope creep into eligibility determination | — |
| D-014 | The sketch-count discrepancy in the brief's Annex A is a minor source inconsistency with no impact on implementation. No further effort | APPROVED | C-13 | — | — |
| D-015 | "PolicyProof" was an earlier brainstorming concept for evidence-grounded factual verification. It was never an implemented project. BTO Buddy is a new implementation that borrows its verification principles | APPROVED | Proposal Q2 | Confirms the fresh-project requirement [ASM p.4] | "PolicyProof-inspired" [APP p.21] → HISTORICAL |
| D-016 | Commit `docs/project_context/` after reviewing it for anonymity, copied source content and restricted information. Use independently authored summaries, never substantial copyrighted text | APPROVED | Proposal Q3 | Transparent planning record | — |
| D-017 | Organisation-specific assessment details, collaborator handles and private submission instructions stay in `references/private/` (Git-ignored). Submission-facing docs describe the project as a public-sector AI prototype | APPROVED | Proposal Q4 | Anonymity requirement [ASM p.2] | — |
| D-018 | Supabase stays listed as a possible demo-video annotation tool | APPROVED | Proposal Q7 | Developer's tool choice | — |
| D-019 | Benchmark: target **48 fictional scenarios in total** across six categories, with a dev/held-out split that preserves category coverage. The exact split (and whether K-fold suits better) must be proposed before the dataset is created. Don't assume all 48 are held-out | APPROVED (split OPEN) | Proposal Q8 | — | — |
| D-020 | Propose an appropriately sized, independently labelled verifier claim set (dev + eval). No fabricated labels | APPROVED (size OPEN) | Proposal Q8 | — | — |
| D-021 | Record source retrieval dates and known effective dates. The supported policy snapshot period is set after source acquisition and validation | APPROVED (period OPEN) | Proposal Q8 | — | — |
| D-022 | Data paths: `data/policy_facts.jsonl`, `data/policy_rules.yaml`, `data/visual_resources.json`, `data/sources_manifest.json`, `data/source_coverage.csv`, `data/private_corpus/raw/`, `data/private_corpus/processed/` | APPROVED | Proposal Q8 | — | — |
| D-023 | Propose a minimal typed `policy_facts` schema: stable fact IDs, factual statements, applicability conditions, exceptions, source references, temporal metadata, validation status. Finalise it during architecture and corpus design | APPROVED (schema PROPOSED) | Proposal Q8 | — | — |
| D-024 | HDB Terms of Use, robots.txt and Copyright Act 2021 ss 243–244 are **preliminary findings** to verify in Phase 2. Never claim HDB granted general redistribution permission | APPROVED | Proposal Q8 | — | — |
| D-025 | The problem-validation research questions are optional evidence-gathering tasks. No invented statistics about confusion, hotline volumes or operational benefit | APPROVED | Proposal Q8 | — | — |
| D-026 | Out of scope: production-grade hosting, authentication, monitoring infrastructure and operational integrations. A fully runnable, reproducible Dockerised prototype stays mandatory | APPROVED | Phase 1 CLAUDE.md template | Effort goes to the evaluated prototype. Monitoring is *described* in the 150–250-word section only (REQ-DOC-002) | — |
| D-027 | Git workflow: **the developer executes all commits and pushes**. The coding agent suggests when a coherent, stable milestone (checks passing) is ready to commit, with the file list, check results, a suggested conventional-commit message and push advice. It runs secret and identifying-term scans before a suggested push and waits for approval. No fixed milestone list | APPROVED (revised 2026-10-28) | Phase 1 instructions | Developer keeps control of history; protects anonymity and private material | Earlier draft with a fixed milestone/message table and agent-executed commits |
| D-028 | Tooling: Python ≥3.12, setuptools `src/` layout, Pydantic v2 (runtime); pytest, ruff, mypy `--strict` as a PEP 735 `dev` dependency group. **uv** manages the environment, with a committed **`uv.lock`** | APPROVED (uv + lockfile, 2026-10-28) | Phase 1 setup | A cross-platform lockfile gives exact, reproducible installs for the clean-machine and Docker requirements (REQ-NFR-001). Preferred over a `pip freeze` lock, which is platform-specific and mixes in transitive noise | pip + venv without a lockfile |
| D-029 | **Architecture decisions on hold** pending the developer's architecture review: stack (Q-23), gate design (Q-12), file paths (Q-10), facts schema/contracts (Q-22). The draft is held as an **uncommitted** file, `docs/proposals/architecture_layout_draft.md`, and kept out of the Phase 1 scaffold commit | APPROVED (hold) | Phase 1 instructions | Review before any contracts code | Earlier "04 §7" placement |

---

## Baseline decisions from the project approach (ratified by D-001 on 2026-10-28)

The project-approach document has no dates. The items below were already stated there as
final, or as firm constraints, and D-001 confirms them as approved.

| ID | Decision | Source |
|---|---|---|
| BD-00 | Original instruction hierarchy | [APP p.1] — **SUPERSEDED by D-001** |
| BD-01 | BTO Buddy is the selected project; final revised idea is a pre-application preparation layer | [APP p.1] |
| BD-02 | Source-discovery matrix does not automatically expand the MVP | [APP p.1, 4, 17] |
| BD-03 | Do not commit complete HDB HTML; store under `data/private_corpus/` (Git-ignored) | [APP p.13] |
| BD-04 | Hybrid architecture: structured profile → rule engine + BM25 retrieval → grounded generation → claim-level verification → preparation report | [APP p.17, 21] |
| BD-05 | Explicit coverage gate before generation | [APP p.21] |
| BD-06 | Structured missing-information contract (four fields) | [APP p.20] |
| BD-07 | Infographics and videos are contextual resources, not runtime evidence | [APP p.12, 18] |
| BD-08 | Evaluation annotation protocol, scoring rules and safeguards | [APP p.16, 24–25] |
| BD-09 | Avoid autonomous agents, complex orchestration frameworks and unnecessary vector databases | [APP p.17] |

## Superseded / historical items (kept for traceability)

| Item | Status | Replaced by |
|---|---|---|
| Working name "BTOPath" | SUPERSEDED | D-002 |
| Three-configuration comparison (A baseline / B RAG / C BTOPath) | SUPERSEDED | D-003 |
| Primary/secondary metric list [APP p.24] and metric table [APP p.26] as the metric hierarchy | SUPERSEDED (definitions reused) | D-004 |
| KB = "curated official HTML/text passages" [APP p.21] | SUPERSEDED | D-005 |
| `source_passage_id` as the rule reference [APP p.15] | SUPERSEDED | D-006 |
| "four official HDB webpages" as the corpus description [APP p.14] | SUPERSEDED | D-007 |
| Supported-question list [APP p.5] | SUPERSEDED | D-008 |
| "Essential" coding-agent logs [APP p.30] | SUPERSEDED | D-009 |
| ChatGPT paragraph in the draft AI disclosure [APP p.31] | Optional (not required) | D-009 |
| "PolicyProof-inspired verification layer" [APP p.21] | HISTORICAL | D-015 |
