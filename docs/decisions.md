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

**Status of this block (updated 2026-10-29):** **APPROVED** by the developer: D-044 to
D-053 (D-048 with the S10 condition later replaced by D-060), D-054 as revised, D-055 to
D-057 and D-058 (revised) to D-062. Nothing in this block is still PROPOSED. **Alignment:** each decision stays inside the approved approach: authored-facts-only runtime (D-005, D-006), declarative rules with no `eval` (D-038), the D-036 dependency list, the income-for-documents-only rule (D-013), the first-timer-couple scope (D-033), and preparation guidance rather than eligibility decisions (REQ-SCP-008). The
current-state analysis is in [data_sources.md](data_sources.md).

| ID | Proposal | Resolves | Rationale | Supersedes |
|---|---|---|---|---|
| D-044 | **APPROVED (developer, 2026-10-28).** **Source classification and acquisition scope** (plan §2, §13). P1 Essential: S01–S04 (seeds) **and S05 Priority Schemes** (revised after the P1 audit: FT(PMC)/FPPS are no longer on S01, so S05 is the only source for the approved Limited priority area. FT(PMC), FPPS and Family Care Scheme sections are authored; other schemes are Outside). P2 Supporting: S06 (BTO section). P3: S07/S08 PDFs, needed because S03 lacks per-employment document lists (audit 2026-10-28). P4 pending: S10, S11, S04.b if it is a separate page. Link only: M00–M04, S12–S16. Never: S17 (portal), S09 (income ceilings) | REQ-SRC-014; D-007 | Smallest set covering all Core areas; the Limited areas degrade gracefully | — |
| D-045 | **APPROVED (developer, 2026-10-28).** Matrix Row 4's main source is **S04** (Application for a New Flat). The HFE `#how-to-apply` URL is a recording slip in the original | C-14, Q-24 | The row names S04; S02 is already Essential | — |
| D-046 | **APPROVED (developer, 2026-10-28).** SC + SPR premium and Citizen Top-Up (S13) → **Outside MVP**, link only. Resale levy (S15) → **Outside MVP**, link only. SC/SPR *eligibility* stays Core via S01.b | Q-06, Q-07 | Both are financing or post-purchase matters (D-008 Excluded) | — |
| D-047 | **APPROVED (developer, 2026-10-28).** **(Revised 2026-10-28 after developer query.)** An SC with a non-resident spouse or fiancé(e) is a **first-timer couple, in scope** (Core household composition). Facts are authored only from the couple rows of the "families with non-residents" section (S01.e) and only for explicit conditions. If those conditions turn out discretionary or too detailed to verify, the topic falls back to identify-and-redirect with an evidence gap. Non-couple non-resident households (parents, children) stay out of scope (D-033). Citizenship combinations with no matching section in the captured sources produce an evidence gap, never a determination | Follows D-033; corrects the first draft | D-033 scopes "first-timer couple (married or engaged)" and doesn't exclude a couple by citizenship. The first draft would have silently reduced Core scope. Citizenship combination is itself a household-composition rule the assistant must explain. Same snapshot (S01), so no extra acquisition | First draft of D-047 (non-resident partner → out of scope) |
| D-048 | **APPROVED (developer, 2026-10-29).** HFE FAQ sub-links: the developer inspects their titles in a browser before any capture. Non-selection consequences are implemented only if "exceptions and waivers" is located and verified. Otherwise the topic is identify-and-link plus an evidence gap. *Outcome:* the waiver content was located and verified in S04 (G-03), so non-selection is implemented (Limited). The S10 part was approved as "link-only unless its titles show per-status document lists", then **replaced by D-060** (S10 excluded entirely) | Q-08 | 03 §2.7b: a non-selection case isn't covered without its exceptions | — |
| D-049 | **APPROVED (developer, 2026-10-28).** Video URLs: canonical `youtube.com/watch?v=<id>` without `si=`. The original URL is kept in the manifest | Q-09 | Removes share tracking; keeps provenance | — |
| D-050 | **APPROVED (developer, 2026-10-28).** No experiment on the private corpus. REQ-DAT-013's same-interface requirement holds structurally only | Q-11 | No evaluation claim depends on it | — |
| D-051 | **APPROVED (developer, 2026-10-28).** Policy details found only in infographics are an **evidence gap** unless a text equivalent exists in an approved text source. *Alternative (b):* a manually authored fact citing the infographic | — | (a) follows REQ-SRC-010 and gives a real Category-B test case. (b) would expand the media rule | — |
| D-052 | **APPROVED (developer, 2026-10-29), option (a).** **Resolves a conflict:** REQ-SRC-009 names PyMuPDF, but D-036 excludes it (and it is AGPL). The developer asked for the quickest approach that is compliant and gives acceptable quality, so: **no PDF parser dependency**. S07 (2 pages) and S08 (4 pages) are reviewed manually, page by page. Facts cite pages in `source.locator`. A second-pass page check was done on 2026-10-29. Limitation: the 9 PDF facts get a manual wording comparison rather than the automated 8-word check. Adding `pypdf` would need a new decision | Conflict REQ-SRC-009 vs D-036; Q-25 | Two short PDFs; manual review is fastest, adds no dependency or licence question, and every condition is checked by eye | REQ-SRC-009's tool choice (method otherwise kept) |
| D-053 | **APPROVED (developer, 2026-10-28).** Manifest schema with host `rights_records` ([data_sources.md §8.3](data_sources.md)). Canonical-URL rules. Two hashes per artefact (`raw_sha256`, `text_sha256`). Full-page screenshots off by default. *(The tracked capture allowlist in the first draft was dropped, because capture is manual under D-055.)* Implemented in `data/sources_manifest.json`, with `scripts/snapshots.py register` | REQ-SRC-002, Q-22 (manifest part) | Makes rights, provenance and drift checking explicit without storing text | — |
| D-054 | **APPROVED as revised (developer, 2026-10-28).** **Data flow:** (1) at **runtime**, only authored facts, rules and fictional profiles go to LLM providers; raw (L0) and processed (L1) source text never does. (2) The **coding agent may read L0/L1 source text** to extract, validate and author facts, on the developer's instruction, because the developer has turned off model training ("Help improve Claude") for the account. Reading is limited to the approved in-scope sections; source text is never written to tracked files, reports or commit messages, and tracked reports carry counts, IDs and short heading labels only. (3) Rights review includes a local check that flags runs of 8+ shared words between a fact and the source (`scripts/corpus.py facts`). *Assessment:* PDPA is not engaged (the HDB pages hold no personal data; profiles are fictional). Under Copyright Act s 244 the copies are made for computational analysis; sending excerpts to a model provider acting as the developer's processing tool, with training off, is treated as part of that analysis rather than supply to others (s 244(2)(c)). This is the project's reading, not legal advice, and is disclosed in the README | Q-26 | The original option (a), developer drafts every fact, was not feasible before the deadline; training-off plus minimisation keeps the analysis use defensible | First draft of D-054 (agent never reads L1) |
| D-055 | **APPROVED (developer, 2026-10-28).** **(Revised 2026-10-28 after Gate R.)** **Manual rendered-DOM capture is the primary method.** The developer opens each approved page in a normal browser, expands every accordion, and copies the live DOM (`document.documentElement.outerHTML`) into `data/private_corpus/raw/<source_id>/`. No images are saved. A local, offline, stdlib-only script (`scripts/snapshots.py`) then audits and registers the file. Automated network capture is **not used**, because HDB's bot protection returns HTTP 403 to both curl and headless Chromium with an honest user agent. Spoofing a browser to get past it is ruled out: it is ethically wrong and would undermine "lawful access" (s 244(2)(d)). Linked PDFs are downloaded manually in the browser. The final URL is taken from the download record. Files are never opened and re-saved. *Applied 2026-10-28 to S01–S05, S07, S08* | REQ-SRC-006, REQ-LIC-001 | REQ-SRC-006 allows manual rendered-DOM extraction. Provenance (hash, timestamp, accordion counts) is kept by the local script | First draft of D-055 (Playwright primary, manual fallback) |
| D-056 | **APPROVED (developer, 2026-10-28) and done.** **Remove the unused Playwright `capture` dependency group** from `pyproject.toml` and `uv.lock` (51 packages locked, down from 54). Drop the planned `scripts/capture_sources.py` from architecture §11. No current or planned step needs a browser driver: capture is manual (D-055); the audit, register and later passage extraction parse saved files with the stdlib; PDFs are validated manually (D-052); drift checks are a manual re-capture plus `snapshots.py register`. The per-machine Chromium cache (~/Library/Caches/ms-playwright) is outside the repo and the developer's to delete | Follows D-055 | D-042's only purpose was automated capture, which HDB's bot protection rules out. The stdlib audit replaced it. An unused dependency group adds review surface and a lockfile entry nobody can justify (REQ-ARC-012, REQ-NFR-003). Re-adding it later is one `uv add --group capture` | D-042 |
| D-057 | **APPROVED (developer, 2026-10-28).** The HDB Terms of Use require prior written permission for linking, caching or framing, and for any reuse of Materials. Proposal: (1) keep the official source links that REQ-ARC-009 requires, in the **private, locally run** prototype only (no public hosting, D-026); (2) the local snapshots rest on Copyright Act s 244, with s 187 voiding the contractual copying ban to that extent; (3) disclose both clauses in the README as residual contractual risk, and as a precondition for any public deployment (HDB permission); (4) *optional, developer's call:* send HDB a written permission request (identity, content, intent, manner, time frame, as the terms ask). This is outward-facing, and a reply is unlikely before the deadline | Terms of Use read 2026-10-28 (data_sources §6.2) | The assessment requires official links and provenance, but the terms ask for permission. Disclosing the gap honestly, keeping the prototype private and pinning the terms version is the defensible middle ground. Dropping links would break REQ-ARC-009 and verifiability | — |
| D-058 | **APPROVED (developer, 2026-10-29), as revised at the developer's request to verify via the rule registry.** **Fact status and runtime use.** `validation.status`: `draft` → `snapshot_checked` (agent, at authoring) → `verified` → or `rejected`. **`verified` means a second, structured check against the hash-pinned 2026-10-28 snapshot**: (a) `scripts/corpus.py verify` confirms every number in the statement and every authored term anchor (≤6 words) occurs in the fact's cited section; (b) the agent re-reads the section for conditions, applicant group and exceptions, and the notes are recorded in `data/corpus/critical_fact_review.json`. It is **not** a live-page check (HDB blocks automated access). The developer should spot-check the live pages before submission for drift (G-15). `rights_review.status`: `pending` → `overlap_checked` → `cleared` (developer, REQ-LIC-015). **Runtime use:** rights at least `overlap_checked`, and `verified`, or `snapshot_checked` and not `critical`. **Deterministic rules may cite only `verified` facts** (D-062). Result on 2026-10-29: all 47 critical facts plus 4 rule-cited facts are verified; 3 facts were corrected first | REQ-DAT-010, REQ-SRC-012/013 | A repeatable, evidence-recorded check is better than an unrecorded read, and it is honest about not being a live check | Architecture §5 `validation_status: Literal["verified"]`; the first draft of D-058 (developer-only verification) |
| D-059 | **APPROVED (developer, 2026-10-29).** **Offline processing and KB schema.** (1) `scripts/corpus.py` (stdlib `html.parser`, **no BeautifulSoup**: D-036 allows no new dependency and the snapshots share one Sitecore layout) does `extract` (L0 → L1 sections, blocks, passages), `validate` (completeness report), `facts` (integrity and overlap) and `freeze`. `snapshots.py` keeps capture registration and the raw audit. (2) Section IDs: accordion items `Sxx.a…`, headings outside accordions `Sxx.hN`, sub-headings `Sxx.a.N`; one passage per section (`…p1`), tables never split. IDs are stable while the snapshot hash holds. (3) The `policy_facts.jsonl` schema is finalised as `bto_buddy.schemas.PolicyFact` (03 §2.5 plus `critical`, nested `source`, `applies_to` as lists). (4) The Docker image ships only L2/L3 (`policy_facts.jsonl`, `sources_manifest.json`, `visual_resources.json`) and reads them from `BTO_BUDDY_DATA_DIR` | D-023 (schema), Q-22, REQ-SRC-007, REQ-SRC-012 | Reuses the parser approach already in `snapshots.py`; deterministic (two runs byte-identical); typed loader lets reviewers load the KB without the private corpus | D-023's "schema PROPOSED" (finalised here once approved) |
| D-060 | **APPROVED (developer, 2026-10-29).** **Exclude the HFE FAQs (S10, `/hdb-flat-portal/hfe/get-help` and its sub-pages) from the source list**, because HDB's robots.txt disallows `/hdb-flat-portal`. No capture, no manual title inspection, no facts, no evidence. The record moves to `excluded_sources` in the manifest (the ID is never reused). Links to it on S02–S04 are recorded as `excluded_by_policy` and never followed. Consequences, stated openly: any HFE exceptions or per-status document lists on those pages are **not represented**, so G-17 and U-01 stay evidence gaps | Q-08 (S10 part); G-04 | Respecting the site's stated access preference is part of the lawful-access and good-faith position (REQ-LIC-014, s 244(2)(d)). Being honest about the content lost matters more than coverage | D-048's S10 condition; D-044's "P4 pending: S10" |
| D-061 | **APPROVED (developer, 2026-10-29).** **Supported scope:** the recommended scope in data_sources §16. Unconfirmed items (U-01 engaged couple marrying after HFE approval; U-02 FT(PMC) for engaged couples; U-03 engaged SC with a non-resident partner) and the per-status document lists (G-17) are **outside the knowledge base**. No facts assert them. The app reports them as unconfirmed or as evidence gaps with an official redirect, and never decides them. The full boundary list is in data_sources §17 | REQ-SCP-007, REQ-SRC-013 | Only verified source content is supported; the gaps are stated rather than filled | — |
| D-062 | **APPROVED (developer, 2026-10-29).** **Policy rule registry (Dataset B).** `data/policy_rules.yaml` (`rules-2026-10-29.1`, 24 rules) is read with `yaml.safe_load` and interpreted by `bto_buddy.policy` (D-038 operators only, no `eval`). (1) **Three-valued logic:** a missing field makes a condition unknown, which gives `cannot_determine` with the missing fields; an exception that cannot be checked also gives `cannot_determine`. (2) Each rule has `kind` (`preparation`, `caution`, `evidence_gap`), `basis` (`source_established` or `interpretation`), `requires_human_review`, `exceptions` (`suppress` or `human_review`), `interpretations`, `limitations`, `effective` scope, `source_fact_ids` (**verified facts only**) and `sources` (official URL per cited fact). (3) Rules never output eligibility decisions; the validator rejects verdict wording. (4) One derived field: `hfe_days_to_expiry` (issue date + 9 calendar months, clamped to month end: interpretation I-02). (5) Proposed profile changes: `employment` takes the six S07 statuses instead of architecture §5's four (I-10), and a new `job_count` (I-11). (6) `RuleResult` gains `kind` and `notes`. (7) `pyyaml` and `types-PyYAML` added, as already listed in D-036 | REQ-DAT-014, REQ-ARC-008, D-006, D-038 | Policy logic stays reviewable data. Every rule traces to verified facts and official URLs without the private corpus. Interpretations are visible and always routed to human review | Architecture §5 `Person.employment` values; `RuleResult` fields |

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
| Playwright `capture` group (D-042) | SUPERSEDED | D-055 (manual capture), D-056 (removed) |

### Approval note, 2026-10-29 (D-058, D-059, D-062)

The developer approved all three after reviewing the Phase 2b evidence (data_sources §12–§19):

- **D-058.** "Verified" is now a recorded, repeatable check:
  - a deterministic number and term-anchor test on the cited section;
  - plus the agent's documented reading.

  It is not claimed to be a live-page check. A live-page spot-check before submission is a
  standing to-do (G-15). This keeps REQ-DAT-010's "manually validated" requirement
  auditable.
- **D-059.** Stdlib processing keeps D-036 intact. The typed `PolicyFact` schema resolves
  D-023/Q-22 and REQ-DAT-020. Only L2/L3 files reach Docker (REQ-DAT-012).
- **D-062.**
  - The registry meets REQ-DAT-014 and REQ-ARC-008. Rules encode only explicit conditions;
    interpretations are labelled and always reviewed; missing data gives `cannot_determine`
    (REQ-ARC-013).
  - Rules cite verified fact IDs only (D-006).
  - The profile changes resolve architecture §5's "Phase 2 aligns with the HFE guide" note:
    `employment` takes the six S07 statuses, and `job_count` is added.

**Supersedes:**
- architecture §5's four-value `employment` field and its `RuleResult` field list;
- the strict `validation_status: Literal["verified"]` runtime filter, now replaced by
  `PolicyFact.usable()`.

