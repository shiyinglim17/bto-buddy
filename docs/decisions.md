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
| D-029 | **Architecture decisions on hold** pending the developer's architecture review: stack (Q-23), gate design (Q-12), file paths (Q-10), facts schema/contracts (Q-22). The draft was kept out of the Phase 1 scaffold commit | SUPERSEDED (hold lifted by D-030 to D-040) | Phase 1 instructions | Review before any contracts code | Earlier "04 §7" placement |

---

## Architecture decisions approved 2026-10-28 (from the architecture review)

Specification: [architecture.md](architecture.md). Each decision was checked against the
approved scope (D-008, D-013, D-026) and against the hard constraints:
- no agents, frameworks or vector DB (REQ-ARC-002);
- free tier (REQ-NFR-004);
- reproducible on a clean machine (REQ-NFR-001).

| ID | Decision | Resolves | Justification | Scope alignment | Supersedes |
|---|---|---|---|---|---|
| D-030 | **Linear typed pipeline:** ① LLM extraction → ② profile assessment → ③ coverage gate → ④ rules ∥ BM25 → ⑤ evidence assembly → ⑥ LLM generation → ⑦ verification → ⑧ report. At most 3 LLM calls per request. Configurations A–D are the same pipeline with stages switched off | Review A1; REQ-ARC-003 | The steps are fixed and known, so a linear pipeline is the simplest design that implements BD-04. Typed boundaries make each stage independently testable and scorable (REQ-ARC-007), and bound latency and cost | Exactly the approved capabilities (REQ-ARC-001). Adds no features beyond the MVP | — |
| D-031 | **Retrieval is BM25 only** (`rank-bm25`), over fact `statement` + `aliases`, filtered to gate-approved topics. Facts cited by applicable rules are always added to the evidence. Dense, hybrid or reranking retrieval is proposed **only if** dev retrieval recall@5 < 0.90 *and* error analysis attributes the misses to paraphrase. Facts schema gains an `aliases: list[str]` field | Review A2; REQ-ARC-010; part of Q-22 | ~100 acronym-heavy authored facts suit exact lexical matching, which is explainable, deterministic and dependency-light. Aliases fix BM25's synonym weakness cheaply. Rule-linked facts make required-rule evidence independent of ranking. Embeddings would add torch (≈2 GB image) or another data-sharing API with no demonstrated gain | Retrieval covers only in-scope topics; excluded topics are never searched | "BM25 or lightweight embeddings" open choice [APP p.21] |
| D-032 | **Quote-grounded extraction.** Each extracted field must carry a verbatim quote, and a deterministic guard drops any field whose quote isn't in the input. Missing fields are computed **only for the topics asked about** (plus rules returning `cannot_determine`). Follow-up questions come from static templates | Review A3; REQ-ARC-013, REQ-SCP-013 | Turns LLM extraction into an auditable step and blocks hallucinated applicant facts, the main risk in a consequential domain. Topic scoping avoids interrogating users with irrelevant questions. Templates make follow-ups deterministic and testable | Uses only fields needed by Core/Limited topics. Income/employment fields are limited to HFE documentation (D-013) | — |
| D-033 | **Coverage gate.** The extraction call tags the question with topics from a closed enum. A deterministic `TOPIC_TIER` map applies D-008. Mixed questions are partially answered, with `out_of_scope_reasons` for the rest. **Household types other than a first-timer couple (married or engaged) are out of scope** and redirected to official sources | Review A4; Q-12; Q-05 (default) | Keeps scope enforcement deterministic and unit-testable, using the LLM only for language understanding. Partial answering avoids needless refusals, and over-abstention is measured | Directly enforces the MVP tiers. Matches the Core definition "first-timer **couple** household composition". Non-couple groups were never Core | Q-05 left open in 01 §6.4 |
| D-034 | **Verifier structure.** Deterministic checks first: uncited claim or citation outside the evidence → insufficient; contradicting a rule result → contradicted. Then **one batched LLM entailment judgement** for the remaining checkable claims. The judge model may differ from the generation model; that is decided at model selection with evidence. No regeneration loop (D-011) | Review A5; REQ-VER-001..007 | Cheap, certain checks shouldn't spend an LLM call. Batching bounds cost (+1 call). A different model family reduces correlated errors [APP p.27]. Its value is proved, not assumed, through C vs D and the verifier claim set (REQ-VER-006) | Implements the approved verification capability only | — |
| D-035 | **Same output contract for all configurations.** A–D all return a structured `FinalGuidance`. In A and B, the LLM itself fills `missing_profile_fields`, `profile_conflicts` and `out_of_scope_reasons`, using the same enums that C and D fill deterministically. The README must state that baseline A is a *structured-output* direct LLM | Review A6; D-003, REQ-EVL-011 | Makes every primary metric score identically and automatically across configurations, and is the strictest reading of "equivalent task instructions" (D-003). The comparison measures architecture, not output format. A structured baseline is a *stronger*, fairer comparator, which makes any hybrid gain more credible. Free-text baselines would need manual mapping per case: slower, less reproducible, more annotator bias | Evaluation design only. No user-facing feature added | — |
| D-036 | **Dependencies.** Runtime: `pydantic`, `pyyaml`, `rank-bm25`, `openai` (used only as an OpenAI-compatible client, so provider and model stay configurable), `streamlit`. Dev: `pytest`, `ruff`, `mypy`, `types-PyYAML`. **No** pandas, scikit-learn, pydantic-settings, LangChain/LlamaIndex, vector stores or torch. Statistics are implemented with the stdlib. Each package is added only when first needed, with a justification comment | Review A7; Q-23; REQ-ARC-012 | Smallest set covering the approved stack. Counts, ratios, bootstrap and exact McNemar don't justify pandas or scikit-learn. One OpenAI-compatible client covers the free-tier providers and local Ollama, keeping model choice an evidence-based configuration decision (REQ-MOD-001) | Streamlit is a demo UI, not production hosting (D-026) | Stack row "Python, Pandas, scikit-learn" [APP p.21] |
| D-037 | **Single-turn interaction.** Follow-up questions are outputs; the user resubmits with more detail. No conversation memory | Review A8 | Matches single-turn benchmark cases, avoids session-state complexity, and stores no user text | Within the MVP; multi-turn dialogue was never in scope | — |
| D-038 | **Rules as declarative YAML** in `data/policy_rules.yaml`. Conditions use whitelisted operators (`eq`, `ne`, `lt`, `gte`, `in`, `is_null`, `all`, `any`), read by a small interpreter. **No `eval`, no executable code in data** | Review A9; D-022, REQ-DAT-014 | Keeps policy as reviewable data separate from code, and safe to load. The interpreter is small enough to test exhaustively | Only explicit, reliably established rules are encoded; no discretionary or calculation rules (REQ-SCP-004, D-013) | — |
| D-039 | ~~**Paths**~~ (SUPERSEDED by D-041) **Paths** (in addition to D-022): `data/eval/{scenarios,retrieval_queries,verifier_claims}.jsonl`, `data/eval/split.json`, `eval/metric_spec.md`, `results/runs/<run_id>/{run_metadata.json,predictions.jsonl,scores.json}` (tracked), `.cache/llm/` (Git-ignored) | Review A10; Q-10 | Committed predictions allow offline re-scoring without an API key (REQ-DAT-018). The raw cache stays local | — | — |
| D-040 | **Optional extraction diagnostic.** Score field-level extraction against a gold profile per scenario, **only if time allows**. A diagnostic, not a primary metric | Review A11 | Cheap to label alongside scenarios, and helps attribute end-to-end errors | Evaluation only; adds no feature | — |
| D-041 | **Repository layout** follows the developer's recommended structure, simplified: `src/bto_buddy/{app,schemas,policy,retrieval,llm,generation,verification,pipeline}.py` + `prompts/`; `evaluation/{run,metrics}.py`, `metric_spec.md`, `results/`; `scripts/` for Phase 2 tooling. Benchmark as `data/benchmark_{dev,test}.jsonl`; verifier claims as `data/verifier_claims_{dev,test}.jsonl`; run outputs in `evaluation/results/<run_id>/`. `llm.py` added; `evaluation/baselines.py` and a separate retrieval-query file dropped (reasons in architecture §11.2). Files are created only when they hold real content | APPROVED (developer instruction 2026-10-28; `llm.py` addition flagged for confirmation) | Repository and tooling setup | Developer's latest instruction. Separate dev/test files make held-out separation physical (REQ-EVL-022). Merging small modules reduces indirection without changing stage boundaries or contracts | No change to scope or pipeline stages (D-030 unchanged in behaviour) | Module list in D-030 layout and paths in D-039 |

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
| Stack row "Evaluation: Python, Pandas, scikit-learn" [APP p.21] | SUPERSEDED | D-036 |
| "BM25 or lightweight embeddings" as an open choice [APP p.21] | SUPERSEDED | D-031 |
| Held architecture draft (D-029) | SUPERSEDED | D-030 to D-040, [architecture.md](architecture.md) |
