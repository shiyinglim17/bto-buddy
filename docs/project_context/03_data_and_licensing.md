# 03 — Data, Licensing and Privacy

The legend is in [INDEX.md](INDEX.md#legend).

## 1. Data assets overview

| Asset | Path (D-022) | Git | Role | Status |
|---|---|---|---|---|
| Raw HDB HTML snapshots, PDFs | `data/private_corpus/raw/` | **Ignored** | Local provenance, extraction, completeness validation | APPROVED (BD-03, D-005) |
| Extracted source-derived passages; any index built from them | `data/private_corpus/processed/` | **Ignored** | Local auditing only | APPROVED |
| Source manifest | `data/sources_manifest.json` | Tracked | URLs, titles, timestamps, hashes, extraction method | APPROVED |
| Source coverage matrix | `data/source_coverage.csv` | Tracked | Policy/extraction coverage evidence | APPROVED (path); format PROPOSED |
| **Policy facts KB (canonical)** | `data/policy_facts.jsonl` | Tracked | Runtime, BM25 retrieval, primary evaluation | APPROVED (D-005); schema PROPOSED (D-023) |
| Structured rule registry | `data/policy_rules.yaml` | Tracked | Deterministic checks | APPROVED (path); content after Phase 2 |
| Visual-resource registry | `data/visual_resources.json` | Tracked | Infographic/video links and display conditions | APPROVED (path) |
| Evaluation scenarios (Dataset C) | `data/benchmark_dev.jsonl`, `data/benchmark_test.jsonl` (D-041) | Tracked | Benchmark | APPROVED (design); not yet created |
| Verifier claim set | `data/verifier_claims_{dev,test}.jsonl` (D-041) | Tracked | Verifier evaluation | APPROVED (D-020); size PROPOSED |
| Saved predictions and run metadata | `evaluation/results/<run_id>/` (D-041) | Tracked | Reproducible offline scoring | APPROVED (REQ-DAT-018) |

## 2. Dataset A — source acquisition and reviewer-facing KB [APP p.4–5, 11–14]

### 2.1 Two corpora (APPROVED, D-005)
- **Private source corpus:**
  - the original HDB HTML pages and approved linked resources;
  - kept locally for provenance, extraction and policy-completeness validation;
  - full snapshots and extracted copied-text passages are **excluded from Git**
    (REQ-LIC-010, REQ-LIC-011).
- **Reviewer-facing canonical KB:** `data/policy_facts.jsonl`, which holds
  **independently authored, source-attributed factual policy representations**. Each has
  passed manual validation and rights review (REQ-DAT-010).
- The application, BM25 index, Docker deployment and primary evaluation **all use the
  reviewer-facing corpus** (REQ-DAT-011).
- The private corpus is **not** needed for normal execution or reviewer evaluation
  (REQ-DAT-012).
- The matrix, snapshots and extraction reports support building and auditing the authored
  facts. They don't expand the MVP (REQ-SCP-007).

### 2.2 Same interface, no transfer of claims (APPROVED) [APP p.13], REQ-DAT-013
- Both corpora should be usable through the **same retrieval interface**.
- Document any coverage differences between them.
- **Never claim that results on one corpus apply to the other.**
- **OPEN (Q-11):** is any experiment planned on the private corpus? If not, the
  same-interface requirement only needs to hold structurally.

### 2.3 Source manifest — REQ-SRC-002 (APPROVED) [APP p.4, 14]
Required fields per source:
- URL;
- document title;
- access timestamp;
- source section;
- extraction method;
- **SHA-256 hash** of the snapshot, to show it didn't change between experiments;
- relevant policy scope [APP p.14].

### 2.4 Private passage record (APPROVED structure, private corpus only) [APP p.4–5]
- **REQ-SRC-003:** each passage keeps enough context to avoid misreading an exception. For
  example, a condition must not be separated from the heading that names its applicant group.
- Example fields from the source document:

  ```json
  {
    "passage_id": "HFE_001",
    "source_id": "HFE_APPLICATION",
    "section": "Application Requirements",
    "source_url": "https://www.hdb.gov.sg/...",
    "anchor": "#application-requirements",
    "content_type": "html",
    "retrieved_at": "2026-10-26",
    "policy_effective_date": null,
    "text": "Locally extracted source content",
    "review_status": "pending"
  }
  ```

- `text` holds copied source content, so these records live only under
  `data/private_corpus/processed/`.

### 2.5 `policy_facts.jsonl` schema — PROPOSED (D-023; finalise in architecture/corpus design)

One JSON object per line. Typed with Pydantic in code.

| Field | Type | Purpose |
|---|---|---|
| `fact_id` | str, stable, e.g. `HFE-VALIDITY-001` | Referenced by rules, labels and citations. Never reused |
| `statement` | str | **Independently authored** factual paraphrase. No substantial copied text |
| `topic` | enum (e.g. `household`, `hfe`, `income_docs`, `application`, `non_selection`, `priority`) | Retrieval facets and coverage gate |
| `scope_tier` | enum `core` / `limited` / `context` | Links to the MVP tier |
| `applies_to` | object of conditions (e.g. `{"household_type": "first_timer_couple"}`) | Applicability |
| `exceptions` | list of `{description, fact_id?}` | Keeps exceptions attached |
| `source` | `{source_id, url, section, anchor}` | Resolves through `sources_manifest.json` |
| `private_passage_ids` | list[str] (optional) | Provenance only; never needed at runtime (D-006) |
| `retrieved_at` | date | Temporal metadata |
| `effective_from` / `effective_to` | date or null; plus `effective_date_note` | Known effective dates and ambiguity |
| `validation` | `{status: draft/verified/rejected, method, validated_at, notes}` | Manual validation |
| `rights_review` | `{status: pending/cleared, notes}` | Rights review before it is tracked |
| `kb_version` | str | Corpus versioning |
| `aliases` | list[str] | Synonyms and acronyms indexed with the statement for BM25 (e.g. "HFE letter", "fiancé"). **APPROVED addition (D-031)** |

### 2.6 Extraction (APPROVED) [APP p.11]
- **REQ-SRC-006:**
  - capture **only explicitly approved webpages**, by manual rendered-DOM extraction or
    controlled browser automation, subject to documented access and usage permissions;
  - preserve expanded informational sections;
  - **never** follow links automatically or interact with transactional services;
  - no automated discovery or unrestricted crawling [APP p.14].
- **REQ-SRC-007:** extract and normalise headings, paragraphs, tables, lists, links and
  document metadata.
- **As implemented (2026-10-28; D-055, D-056):** HDB's bot protection returns HTTP 403 to
  automated clients, so capture is **manual**. The "controlled browser automation" option
  isn't used, and its tooling (Playwright) was removed.
  - HTML pages: the developer saves the rendered DOM from a normal browser. All accordion
    panels were already in the DOM, so a single default-state copy per page sufficed.
  - PDFs: downloaded manually in the browser.
  - Files go to `data/private_corpus/raw/<source_id>/<UTC>_<name>`.
  - Offline scripts: `scripts/snapshots.py audit` (completeness, structure-only output) and
    `scripts/snapshots.py register` (hashes and timestamps into
    `data/sources_manifest.json`).
  - Acquired so far: S01–S05 (HTML) and S07–S08 (PDF). See
    [data_sources.md §7](../data_sources.md).
- Media rules are in [02 §4](02_policy_sources.md#4-media-handling-decisions-approved-app-p1112-18).

### 2.7 Validate completeness and freeze — REQ-SRC-012, REQ-SRC-013 (APPROVED) [APP p.12–13]

Freezing involves a coverage matrix, missing exceptions, source hashes and manual review.

**(a) Extraction completeness.** Did the pipeline capture what the approved sources display?

| Check | Method |
|---|---|
| Accordion coverage | Compare discovered controls with successfully expanded controls |
| Section coverage | Compare visible page headings with extracted headings |
| Link coverage | Classify relevant links as included, excluded or pending review |
| Table preservation | Check row/column values against the rendered source |
| Policy exception coverage | Manually inspect exceptions and conditional wording |
| Source traceability | Verify that passage IDs map to real URLs and sections |
| Temporal validity | Record known effective dates and unresolved date ambiguity |
| Duplicate passages | Detect duplicates without discarding distinct exceptions |

**(b) Policy coverage completeness.** Does the captured information contain the
requirements and exceptions the supported scenarios need?
- Every supported rule has **at least one verified authoritative source**.
- Every important exception has been checked.
- Example: a "declining flat selection" case is **not** covered just because the corpus has
  a general first-timer paragraph. The relevant exceptions must be represented too.
- Stored in `data/source_coverage.csv`.

### 2.8 Temporal validity — REQ-SRC-015 (APPROVED) [APP p.28], D-021
- Every reference document records:
  - source URL;
  - retrieval date;
  - effective date where available;
  - applicable scope.
- The application **states the policy period it supports**. That period is set after
  acquisition and validation (OPEN until Phase 2).

## 3. Dataset B — structured policy rule registry [APP p.15], REQ-DAT-014, D-006

- A small machine-readable registry, so policy logic isn't buried in prompts.
- **Encode only rules whose conditions are explicit and reliably established.** Discretionary
  decisions are never forced into binary rules (for example, unwed-parent cases are assessed
  holistically).
- **Benefits:**
  - deterministic, unit-testable checks;
  - clear separation of policy facts from model explanations;
  - a defensible architecture for a consequential public-service domain.
- **Example** (original APP p.15, updated per D-006):

  ```yaml
  rule_id: HFE_REQUIRED
  scope: new_flat_application
  condition:
    requires_valid_hfe: true
  outcome:
    preparation_step: "Obtain a valid HFE letter"
  source_fact_id: HFE-REQUIRED-001     # D-006: reviewer-accessible fact ID
  # source_passage_id: hfe_application_001   # SUPERSEDED (private passage ID; may be kept as provenance)
  requires_human_review: false
  ```

## 4. Dataset C — independently labelled evaluation scenarios [APP p.15–16]

The full design is in [05_evaluation.md §3](05_evaluation.md).

- **REQ-DAT-016:** Dataset C is kept **separate from the knowledge corpus and from the
  runtime verifier**.
- **REQ-DAT-017:** profiles are fictional and use synthetic names. **Real applicant records
  are never used.**
  - Reason: real records are sensitive and hard to access.
  - Synthetic profiles suit controlled rule testing and edge-case coverage.
- **Defence of synthetic data** (needed by REQ-DAT-002):
  - scenarios are *policy-derived* from verified rules and vary one or two factors at a
    time, including boundary conditions;
  - labels are assigned manually against official rules, never invented by an LLM.

## 5. Licensing, access and permissions

### 5.1 Preliminary findings — to verify in Phase 2 (D-024)
- **REQ-LIC-013:** HDB website materials are subject to HDB's published **Terms of Use** and
  copyright.
  - Singapore's **Copyright Act 2021, ss 243–244**, gives a conditional exception for
    *computational data analysis*, covering certain copying and retention, subject to
    lawful-access, purpose and sharing restrictions.
  - This is a *preliminary* reading. The statutory text and the Terms of Use must be checked.
- **REQ-LIC-014:** **robots.txt** compliance [ASM p.2] for every host:
  - `www.hdb.gov.sg`;
  - `file.go.gov.sg`;
  - `www.mynicehome.gov.sg`;
  - (YouTube: links only).

  Status (2026-10-28, Gate R):
  - `www.hdb.gov.sg`: checked. Planned `/buying-a-flat/` paths are allowed;
    `/hdb-flat-portal` is disallowed.
  - `file.go.gov.sg`, `www.mynicehome.gov.sg`: not checked (PDFs were downloaded manually,
    not by a bot).
  - HDB Terms of Use: **unread** (403 or JavaScript-only).
  - Copyright Act ss 244 and 187: read from a secondary source.

  Details: [data_sources.md §6](../data_sources.md).
- **REQ-LIC-012:** **never claim HDB has granted a general redistribution licence.**
- **REQ-LIC-016:** a script may support lawful acquisition. Re-downloading current pages
  can't rebuild a historical frozen snapshot, so hashes and capture dates must be recorded.

### 5.2 Redistribution rules (APPROVED) [APP p.13–14]
- **Git-ignored:**
  - full HDB HTML files;
  - extracted passages containing substantial original text;
  - source-derived indexes containing such text.

  These stay ignored unless redistribution permission is established.
- **May be tracked, subject to content and rights review:**
  - independently authored factual representations;
  - source URLs and metadata;
  - rule definitions and evaluation labels;
  - processing scripts.
- The three-way distinction to document:
  1. A private source snapshot, for local extraction and analysis.
  2. A reviewer-accessible, independently authored policy KB.
  3. A frozen evaluation dataset of fictional scenarios with independently checked labels.
- **REQ-LIC-015:** before submission, review **all tracked data** for copyright, privacy
  and credential exposure.
- **REQ-LIC-017 (D-016):** project-context docs use authored summaries, never substantial
  copyrighted text.

## 6. Privacy — REQ-PRIV-001, REQ-PRIV-010
- **No real personal data:** all profiles are fictional [APP p.16].
- **Deployment limitation [APP p.28]:** free-tier API data-handling terms may not suit
  personal information in a real deployment that ingests applicant data. This feeds the
  model-selection justification (REQ-MOD-001) and the deployment-risk section (REQ-DOC-002).
- **The app never touches transactional services** such as Singpass or the HDB Flat Portal
  (REQ-SRC-006).

## 7. Reproducibility — REQ-DAT-018, REQ-DAT-021, REQ-DAT-022 (APPROVED) [APP p.13–15]
- **Reviewer path:**
  - The repo includes the rights-reviewed `policy_facts.jsonl`, the rules, the source
    metadata and the evaluation datasets.
  - Reviewers build the retrieval index and run the Dockerised app **without downloading HDB
    pages or rebuilding the private corpus**.
- **Developer scripts:** source-capture and extraction scripts are optional and documented.
  They are **not** dependencies of startup or of primary evaluation.
- **Clean-machine test:** a clean-machine Docker test must prove the reviewer-facing
  configuration works (REQ-NFR-001).
- **Live API runs vary,** so each run records:
  - model identifiers;
  - prompt versions;
  - inference settings;
  - corpus versions;
  - **saved predictions**.

  Reproducible offline scoring is reported separately from new live inference.

## 8. README data-section draft (PROPOSED wording, APP p.14–15)

The draft paragraphs in the source cover: data sources, data acquisition (hybrid,
scope-controlled, manual approval, optional browser automation for expandable sections, no
crawling), source provenance (manifest), licensing and access, data handling and
redistribution, reproducibility and limitations.

The draft must be revised before use:
- "Optional browser automation" is **not used**. Acquisition was manual browser capture,
  because HDB blocks automated clients (D-055, D-056). Describe it as in
  [data_sources.md §6–7](../data_sources.md).
- It says the prototype uses **"four official HDB webpages"**. That is SUPERSEDED by D-007;
  report the final source count after Phase 2.
- It must reflect D-005 (canonical KB) and D-024 (preliminary rights findings).

## 9. Data limitations (APPROVED, for README) [APP p.15, 28]
- Policy content reflects the retrieved versions and may miss later changes.
- No live retrieval. The static KB and rule registry need **manual updates after each policy
  change**, which makes maintenance effort high.
- Synthetic profiles support controlled testing. They **can't establish** how often real
  applicants misunderstand rules, or how the assistant performs on real enquiries.
- The prototype gives informational preparation guidance. It doesn't replace the official
  eligibility assessment.
- **Representativeness (REQ-DAT-003):** state what the data covers and doesn't cover. That
  means the MVP tiers, the household types and the policy period.
