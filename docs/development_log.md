# Development Log

Chronological record of completed work, decisions, failures and next steps. Decisions
themselves live in [decisions.md](decisions.md). Requirement IDs are in
[project_context/requirements_register.md](project_context/requirements_register.md).

---

## Phase 0 — Context building (2026-10-27 → 2026-10-28) — complete

**Done:**
- Reviewed both private planning PDFs page by page, including all 11 embedded images.
- Built the `docs/project_context/` knowledge base: 150 requirement IDs, a source-discovery
  matrix, the evaluation design, and a completeness audit (register §4).
- The developer resolved contradictions C-01 to C-13 (D-001 to D-025).
- Created `.gitignore` (private PDFs, private corpus, secrets) and private submission notes.
- Commit `c49555f docs: establish project context and requirements`.
- Context-extraction method (for re-audits): text via pdfplumber; every embedded image cropped
  at 300 dpi and read visually; non-default text colours checked to locate verbatim HDB quotes.

**Found:**
- New contradictions C-14 to C-17.
- Open questions Q-05 to Q-24.
- All policy facts quoted in the approach document are **unverified** until Phase 2.

## Phase 1 — Project setup and architecture (2026-10-28) — complete

### Chronology
| Step | Outcome | Decisions | Commit (by developer) |
|---|---|---|---|
| Scaffold and agent instructions | `CLAUDE.md`, `pyproject.toml` (src layout), package, smoke test, placeholder README | D-026 (production infra out of scope), D-027 (developer runs all commits/pushes; agent suggests) | `e163bdd chore: initialise project and tooling` |
| Lockfile and tooling | uv with committed `uv.lock`; dev tools in a PEP 735 `dev` group | D-028 | (in `e163bdd`) |
| Docker | Agent install failed (needs `sudo`); developer installed Docker Desktop. Docker 29.9.2 verified | — | — |
| Architecture review | Held draft (D-029) replaced by a full review; A1–A11 approved → [architecture.md](architecture.md) | D-030 to D-040; Q-05, Q-10, Q-12, Q-23 resolved | `0cca98b docs: approve architecture and record design decisions` |
| Schedule | Target 2026-10-29 07:00; effort estimate is reference only; all of A–D planned | D-043 | (in `0cca98b`, as notes) |
| Repository and tooling setup | Developer's structure adopted, simplified; Streamlit entry point, `Dockerfile`, `.dockerignore`, `.env.example`, `.streamlit/config.toml` (telemetry off), merged `.gitignore`; Ruff excludes `docs/` (it formats Python blocks inside Markdown) | D-041 | `36531ae chore: add Streamlit entry point, Docker and environment tooling` |
| Capture tooling | Playwright in opt-in `capture` group; Chromium headless shell in user cache; offline launch test only | D-042 | `910eb78 chore: add opt-in Playwright capture dependency group` |

### Final verified state (re-run 2026-10-28, macOS, Python 3.13.2, uv 0.13.6, Docker 29.9.2)
| Check | Result |
|---|---|
| `uv sync` / `uv lock --check` | OK. 54 packages locked (49 in the default env; Playwright only with `--group capture`) |
| `uv run ruff check .` / `uv run ruff format --check .` | All checks passed / 5 files formatted |
| `uv run mypy` (strict) | No issues in 2 source files |
| `uv run pytest` | **1 passed** (`tests/test_smoke.py`: app renders, title, version, disclaimer) |
| `docker build -t bto-buddy .` | OK (image ≈ 820 MB; Streamlit brings numpy, pandas, pyarrow) |
| `docker run -p 8501:8501 --env-file .env.example bto-buddy` | Docker HEALTHCHECK `healthy` in ~8 s; `/_stcore/health` returns `ok` |
| Image contents (checked at setup) | Non-root `app`; `/app` = `.venv`, `.streamlit`, `app.py`; no PDFs, `.env`, `references/`, `private_corpus` |
| Git hygiene | Working tree clean; no private or secret files tracked; `git check-ignore` covers `.env`, private corpus, `references/private/`, caches, `tmp/`, logs, Streamlit secrets; anonymity scan clean |

**What exists in code:** only `src/bto_buddy/__init__.py` and `app.py` (a shell with a disclaimer
and privacy notice; it says the pipeline isn't available yet), plus one smoke test. No pipeline
modules, data files, prompts, model choice or datasets exist yet.

### Unresolved issues carried forward
| Item | Needed by | Where |
|---|---|---|
| D-041: confirm the `llm.py` addition | Before pipeline code | [decisions.md](decisions.md) |
| C-14 / Q-24: the matrix's BTO-process row cites the HFE page URL | Phase 2 | register §2–3; 02 Row 4 |
| Q-06, Q-07: SC+SPR premium and resale-levy tiers | Phase 2 | 02 Row 1 |
| Q-08: HFE FAQ sub-links and the "exceptions and waivers" source | Phase 2 | 02 Rows 2, 5 |
| Q-09: strip `si=` from video URLs (minor) | Phase 2 | 02 Row 2 |
| Q-11: any experiment on the private corpus? (register still says "Phase 1"; carried to Phase 2) | Phase 2 | 03 §2.2 |
| Q-22: `policy_facts` field-level schema | Phase 2 | 03 §2.5; architecture §5 |
| robots.txt and Terms of Use checks; Copyright Act ss 243–244 verification (D-024) | Before any capture | 03 §5.1 |
| Supported policy period (D-021) | After capture | 03 §2.8 |
| Q-13 / C-17: privacy criterion in model scorecard; model and judge-model selection | Model selection | 04 §6.3 |
| Q-14, Q-15/C-16, Q-16/C-15, Q-17: claim annotation guide, "answer coverage", human-review burden, scorer | Before evaluation | 05 §4 |
| Q-20, Q-21: benchmark split (proposed 18/30) and verifier claim set (proposed 60) | Before dataset creation | 05 §3.3, §6.1 |
| Q-19 / C-09: log anonymity vs completeness | Pre-submission | 06 §7 |
| All policy facts in the context docs remain **AUTHORED-FACT (unverified)** | Phase 2 | 02 §5 |

## Phase 2 — Policy sources (handoff)

**Goal (D-007):** determine the **minimum source set** for the MVP and turn verified content
into the reviewer-facing knowledge base. Nothing is included just because it appears in the
matrix.

**Read first:**
1. [CLAUDE.md](../CLAUDE.md);
2. [INDEX.md](project_context/INDEX.md);
3. [02_policy_sources.md](project_context/02_policy_sources.md) (matrix, media handling,
   facts to verify);
4. [03_data_and_licensing.md](project_context/03_data_and_licensing.md) (corpora, manifest,
   completeness checks, rights);
5. [architecture.md §5](architecture.md) (contracts, `PolicyFact`).

**Gates the developer must approve, in order:**
1. **Page list for capture.** Seeds plus any linked sources justified by the MVP tiers, with
   C-14 and Q-06 to Q-08 resolved.
2. **Rights check before fetching:** robots.txt and Terms of Use for each host. Never claim a
   redistribution licence.
3. **Capture run** *(superseded: capture became manual, D-055/D-056; see Phase 2a)*:
   Playwright (`--group capture`), approved pages only. No crawling,
   link-following or transactional pages. Output goes to `data/private_corpus/raw/`
   (Git-ignored), with SHA-256 and timestamps in `data/sources_manifest.json`.
4. **Extraction and completeness audit:** 8 checks (03 §2.7), output to
   `data/private_corpus/processed/`, plus `data/source_coverage.csv`.
5. **Authoring:** `data/policy_facts.jsonl` (independently authored, verified, rights-reviewed,
   with `aliases`) and `data/policy_rules.yaml` (declarative, D-038). Finalise Q-22.

**Can proceed in parallel, with no dependence on real facts:**
- `schemas.py` and `policy.py` (loaders, rule interpreter, gate, profile assessment), with
  unit tests against a clearly fictional fixture KB in `tests/fixtures/`.

## Phase 2a — Source discovery, MVP mapping and rights review (2026-10-28) — awaiting approval

**Done:**
- Reconciled every matrix row and linked resource against the approved scope. The result is
  [source_acquisition_plan.md, since consolidated into data_sources.md](data_sources.md):
  - stable IDs: 17 documents (S01–S17), about 30 sections, 5 media items;
  - a five-way classification with reasons;
  - a relationship tree and link-type inventory;
  - a policy-dependency table;
  - an MVP coverage matrix;
  - a rights table per host;
  - the manifest schema;
  - the corpus layers L0–L3;
  - an extraction method per source;
  - a reviewer-reproducibility strategy;
  - gaps G-01 to G-14 and gates R, C and P.
- Reread APP p.4–12 of the private approach PDF (text and link annotations only) to confirm
  the matrix's original references. The Phase 0 extraction was complete. C-14 is present in
  the original.
- Proposed D-044 to D-055. Added Q-25 (the PyMuPDF vs D-036 conflict) and Q-26 (agent access
  to processed source text) to the register.

**Update (same day):**
- The developer asked to reconsider D-047. It was revised so that an SC + non-resident
  spouse or fiancé(e) is an in-scope couple. The first draft would have silently reduced Core
  scope.
- **Gate R** (approved):
  - HDB robots.txt allows S01–S06 and disallows `/hdb-flat-portal` (S10).
  - HDB's bot protection returns **403** to curl and to headless Chromium with an honest
    user agent. Both error pages are saved privately with hashes.
  - The HDB Terms of Use couldn't be read automatically and stay **unresolved**.
  - Copyright Act ss 244 and 187 were read from a secondary source (SSO returned 403).
- D-055 revised: **manual rendered-DOM capture** is primary. No bot-protection evasion.

**P1 capture (developer, manual rendered DOM, 2026-10-28 09:18–09:38Z):**
- S01–S04 saved in their default state; all panels were already in the DOM. The agent
  renamed the files with UTC creation-time prefixes and gave the two rights-check 403 pages
  descriptive names.
- Added `scripts/audit_snapshots.py` (offline, stdlib, structure-only output).
- Results are in [data_sources.md §7](data_sources.md):
  - capture is complete against the embedded page data (only metadata unrendered);
  - gaps G-01, G-02 and G-03 resolved;
  - **FT(PMC)/FPPS are no longer on S01**, so S05 is needed for the Limited priority area;
  - S03 lacks per-employment document lists, so the P3 PDFs are needed;
  - S02 was updated on 28 Oct 2026 (G-15).

**Second capture batch (developer, 2026-10-28 10:29–10:30Z):**
- S05 Priority Schemes, manual rendered DOM. It is now Essential, because FT(PMC) and FPPS
  moved there.
- S07 and S08 HFE PDF guides, manual browser download. The final URL comes from the
  download metadata.
- The agent added UTC prefixes; they match Chrome's download timestamps to within 2 s.
- The S05 audit shows 9/9 concepts. The PDFs have a text layer, with metadata dated
  19 Dec 2025.
- Created `data/sources_manifest.json`: 22 records, 4 rights records, hashes for 7 acquired
  files.
- Added `scripts/register_snapshots.py`. Both scripts pass ruff and run with `python3 -I`.

**Repository cleanup (2026-10-28):**
- `docs/source_acquisition_plan.md`, which was pre-capture and partly superseded, was
  replaced by the current-state [data_sources.md](data_sources.md). Superseded
  automated-capture text and duplicated decision lists were removed. Decisions stay in this
  file and in decisions.md.
- `scripts/audit_snapshots.py` and `register_snapshots.py` were merged into
  `scripts/snapshots.py {audit|register}`. The merged script reproduces the manifest
  byte-for-byte.
- Local artefacts (`.DS_Store`, `src/*.egg-info`, tool caches) were deleted. All are
  Git-ignored and regenerated on demand.
- **D-056 (approved by the developer, done):** removed the Playwright `capture` group,
  because no current or planned step needs a browser driver.
  - `uv remove --group capture playwright`; the lockfile went from 54 to 51 packages.
  - D-042 is superseded.
  - Architecture §11, CLAUDE.md, 03 and the register are updated.
  - `data_sources.md` §6.3 maps the manual acquisition approach to the provenance and
    licensing requirements and to the Copyright Act s 244 conditions.
  - The Chromium cache (~587 MB, outside the repo) is left for the developer to delete.

**HDB Terms of Use (2026-10-28 13:44Z):**
- The developer captured them manually, over the earlier 403 block-page file. The agent
  renamed the file to `raw/rights/2026-10-28T134435Z_hdb_terms_of_use.html`, using the
  modification time, since the creation time belonged to the overwritten file.
- `snapshots.py register` now records the terms hash and check time in the manifest.
- The agent read them in full under the approved rights check (R4) and wrote an authored
  summary.
- Findings:
  - copying or reuse needs written permission, with no research carve-out, so local copies
    rest on s 244/s 187;
  - linking, caching or framing needs written permission, which conflicts with REQ-ARC-009
    → proposed **D-057**;
  - no robots, scraping or AI clauses;
  - the reliance disclaimer matches the app's.

**Not done (by design):** no automated fetch, download or extraction beyond the Gate R checks
and the audits above. No facts have been authored. robots.txt, the Terms of
Use and Copyright Act ss 243–244 are **unchecked**. Every permission is UNRESOLVED.

**Next:**
1. Developer review of D-044 to D-055.
2. Gate R fetches (plan §14.3).
3. Gate C: capture P1 (S01–S04).
4. Completeness audit and P3/P4 decisions.
5. Fact authoring.

---

## 2026-10-28: Phase 2b, offline processing, completeness validation and KB (to approval checkpoint)

**Decisions:**
- The developer approved D-044 to D-047, D-049 to D-051, D-053, D-055 and D-057.
- D-054 was approved **as revised**: the agent may read in-scope L0/L1 text, because model
  training is turned off; no source text goes into tracked files.
- D-048 and D-052 are held for explanation.
- New proposals: D-058 (fact statuses and runtime use) and D-059 (processing tooling and KB
  schema).

**Done:**
- **`scripts/corpus.py`** (stdlib): `extract` produced 80 private passages from S01–S05,
  keeping sections, nested tables with spans, lists, footnotes, anchors, links and media.
  `validate`, `facts` and `freeze` were added. Two full runs gave byte-identical outputs.
- **Completeness:** the counts for accordions, tables, expected sections and headings all
  match. Rendered page-data sentences missing from L1: **0 on every page**. Merged cells
  are flagged for a manual check. The single-snapshot limitation is recorded for each
  source.
- **PDFs:** S07 and S08 were reviewed manually. **Finding G-17:** no approved source lists
  documents per employment status.
- **KB:**
  - `data/policy_facts.jsonl` holds 89 facts (21 household, 11 application, 14 HFE
    process, 15 HFE documents, 15 priority, 8 non-selection, 5 context). 47 are critical.
  - All are `snapshot_checked` and `overlap_checked`. The first draft had 12 facts flagged
    at 8+ shared words; they were reworded, and the maximum shared run is now 7.
  - `src/bto_buddy/schemas.py` and `policy.py` load and resolve the KB from tracked files
    only.
  - Docker now copies the L2/L3 files (`BTO_BUDDY_DATA_DIR`).
- **Coverage and media:** `data/source_coverage.csv` (33 rows at the time; 36 after the 2026-10-29 update) and
  `data/visual_resources.json` (M00, M01, M03, M04, as links).
- **Tests:** `tests/test_corpus.py` and `tests/test_policy_kb.py`, using invented fixtures.

**Failures and fixes along the way:**
- The first page-data check reported many false gaps: headings fused with paragraphs, link
  spacing, and card text. Fixed with block-aware segmentation and chrome classification.
- A list-embedded table on S05 was flattened. It is now emitted as its own block.
- Infographics inside `<p>` were missed. They are now recorded as media.
- One authored exception ("marriage after approval is a marital-status change") was an
  inference. It was removed and logged as U-01.

**Open for the developer:**
1. Approve or adjust the corpus and the supported scope (data_sources §16).
2. Decide D-048, D-052, D-058 and D-059.
3. Verify the 47 critical facts with checklist C-01 to C-16.
4. Clear rights (REQ-LIC-015).
5. Decide U-01 to U-03.
6. Approve filling the manifest URLs for M00–M02 (M-01).
7. Confirm R-dates.

**Next (after approval):** the policy-rule registry (Dataset B), then the benchmark.

## 2026-10-29: Phase 2b follow-up, scope approved and HFE FAQs excluded

**Decisions:**
- Developer approved:
  - the recommended scope, with unconfirmed items kept outside the KB (D-061);
  - D-048: the waiver condition is met, and the S10 part is replaced by D-060;
  - D-052, option (a): manual PDF page review, no parser dependency, as the quickest
    compliant approach.
- Developer confirmed that S01 and S05 were not edited after pasting (R-dates closed).
- New, approved: **D-060** removes the HFE FAQs (S10) from the source list, because
  robots.txt disallows `/hdb-flat-portal`.

**Done:**
- **Manifest:** S10 moved to `excluded_sources`, with the reason and its effect. S01 and S05
  review status set to `confirmed`.
- **Link classification:** links to the FAQs are now `excluded_by_policy`.
- **Coverage matrix:** now 36 rows. New explicit `unconfirmed` rows for U-01 to U-03; the S10
  row is `excluded_by_policy`.
- **Facts:**
  - PRI-FTPMC-001 now says U-02 is unconfirmed.
  - The 9 PDF facts got a second-pass page check.
- **data_sources §17** documents everything outside the KB:
  - content excluded for data-policy reasons, and what is lost;
  - evidence gaps inside the scope;
  - content excluded by scope.

**Effect:** G-17 and U-01 cannot be closed from the approved sources. They are reported to
users as evidence gaps with redirects.

**Next:**
1. Developer verifies the 47 critical facts (C-01 to C-16).
2. Decide D-058 and D-059.
3. Rights clearance (REQ-LIC-015).
4. Then the policy-rule registry (Dataset B), which must emit the §17 gaps.

## 2026-10-29: Critical-fact verification and the policy rule registry

**Request:** verify the 47 critical facts using checklist C-01 to C-16 through a rule
registry, and build that registry using verified facts only.

**Done:**
- **`scripts/corpus.py verify`:** a deterministic number and term-anchor check on each
  fact's cited section, plus recorded review notes (`data/corpus/critical_fact_review.json`).
  Results: 51/51 pass (all 47 critical facts plus 4 cited by rules).
- **3 facts corrected first**, because their wording went beyond the source:
  - HH-SUBSIDY-002 (how subsidies are counted);
  - HH-COUPLE-002 (the childless-couple reading);
  - HFE-APPLY-001 (the wrong section was cited).
- **D-058 revised:** `verified` now means this structured snapshot re-verification, not a
  live-page check. Still PROPOSED.
- **`data/policy_rules.yaml`:** 24 rules. The interpreter and validator are in
  `bto_buddy.policy`, and the `RuleResult` contract is in `schemas.py`. `pyyaml` and
  `types-PyYAML` were added (already listed in D-036). The Docker image now copies the rule
  file.
- **Proposed in D-062:**
  - three-valued logic: missing data gives `cannot_determine`;
  - verdict wording rejected;
  - interpretations and evidence gaps always require human review.
- **Issues recorded:**
  - incomplete source information I-01 to I-05, I-08 and I-09, plus U-04 (FPPS for engaged
    couples);
  - design inconsistencies I-10 (employment values) and I-11 (`job_count`);
  - no direct contradictions found between sources.
- **Tests:** 83 pass, 62 of them new rule tests. ruff, mypy and the lockfile check pass.

**Open for the developer:**
1. Approve D-058 (revised), D-059 and D-062, including the I-10 and I-11 profile changes.
2. Spot-check the live pages for drift.
3. Rights clearance.

**Next (after approval):** the benchmark (Dataset C).

## 2026-10-29: D-058, D-059 and D-062 approved; Phase 2b closed

- The developer approved:
  - **D-058 (revised):** "verified" means the recorded snapshot re-check, not a live-page
    check;
  - **D-059:** stdlib processing and the `PolicyFact` schema;
  - **D-062:** the rule registry, with the S07 employment statuses and `job_count` added to
    the profile.
- Approval note and alignment rationale: decisions.md.
- Contracts updated to match:
  - architecture §5 (`employment`, `job_count`, `RuleResult.kind`/`notes`, `usable()`);
  - REQ-DAT-020 is now APPROVED.
- **Phase 2b summary (4a to now):**
  - sources acquired manually (D-055);
  - HFE FAQs excluded per robots.txt (D-060);
  - L1 extraction with 0 rendered-content gaps;
  - 89 facts, rights overlap-checked (max 7 shared words);
  - 47 critical facts plus 4 rule-cited facts verified, with 3 corrected;
  - 24 rules;
  - the out-of-scope and evidence-gap register (data_sources §17).
- **Standing to-dos before submission:**
  - live-page spot-check for drift (G-15);
  - developer rights clearance (REQ-LIC-015);
  - README data section (03 §8), including the D-054 and D-057 disclosures.

## 2026-10-29: Phase 3a, evaluation benchmark design (candidate, not frozen)

**Carried over from Phase 2b:**
1. live-page drift check;
2. rights clearance;
3. README data section (evaluation_benchmark §10).

**Done:**
- **Two context facts verified** (CTX-HFE-001, CTX-GRANT-001; 53 verified in total), because
  out-of-scope redirect labels need them.
- **Rubric and claim protocol:** `docs/evaluation_benchmark.md`, with the rubric written
  before the cases, the claim-level protocol, sampling, split, leakage, QA, the
  manual-validation list and limitations.
- **`evaluation/benchmark.py`:** the `CaseInput`/`CaseLabel` schema, locked held-out loader,
  validator (traceability, split, family and hash checks) and engine cross-check.
- **48 candidate cases:**
  - 18 dev cases in `dev.jsonl`;
  - 30 held-out inputs in `test_inputs.jsonl`;
  - held-out labels in Git-ignored `evaluation/heldout/test_labels.jsonl`, with the SHA-256
    in `manifest.json`;
  - review sheets for both.
  - 20 cases are flagged for source checking (dev 4, held-out 16).
  - 34 families; 0 cross-split near-duplicates (maximum Jaccard 0.49).
  - 22 of 24 rules are exercised.
- **Engine cross-check:** found 1 label error (DEV-05), corrected against HH-CIT-001. R-APP-002
  was added as optional to 3 cases.
- **Claim template:** 4 dev claims. Tests: `tests/test_benchmark.py`. 92 tests pass.
- **Access rule:** CLAUDE.md now forbids agents from reading `evaluation/heldout/`. The
  authoring script, which contained the held-out labels, was deleted after generation.

**Open for the developer:**
1. Review and approve the labels using the two review sheets.
2. Decide D-063 to D-065.
3. Back up `evaluation/heldout/`.
4. Then freeze (evaluation_benchmark §8) and write `metric_spec.md` before any prompt work.

## 2026-10-29: Dev label review, batch 1 (DEV-03, DEV-08, DEV-09, DEV-14)

The developer gave review notes on four dev cases; the agent checked each against the cited
sections (S01, S02, S05; authored summaries only) and applied the agreed edits to `dev.jsonl`.
- **DEV-03 (edited):** the 30-day date is now approximate (inclusive counting not stated;
  new major PC-X3). **Label error found:** the old key point advised doing Step 2 in October,
  but the case date is 1 November; replaced with "details must be updated" (new major PC-X4).
- **DEV-08 (edited):** key point reworded as meeting one published condition, not overall
  eligibility. I-05 removed from `unresolved_refs`: he is already 21, so the assessment date
  cannot change the result, and keeping it contradicted rubric §2.6.
- **DEV-09 (approved unchanged):** both constraints are explicit in HFE-STEPS-001; 21 days
  apart is inside the window under any counting convention.
- **DEV-14 (edited):** S01 does list a flat bought from HDB as a subsidy, so the inference holds
  for this profile; the FT(PMC) ownership/sale criterion is now a separate conditional point;
  added the mixed first-/second-timer point (PRI-FT-001), PC-VERDICT (was missing) and major
  PC-X2.
- **Rubric:** §2.7 gains a key-point coverage row so fact-only cases are scored; its definition
  is deferred to `metric_spec.md`.
- **Review sheet:** `dev_review_sheet.csv` gains a `key_points` column. The held-out sheet was
  not regenerated (D-064), so it still lacks that column.
- Checks: benchmark validate errors=0, engine disagreements none; `tests/test_benchmark.py` 9 pass.

## 2026-10-29: Dev label review, batch 2 (DEV-13) and snapshot assumption A-01

- **DEV-13 (edited):** "engaged in May" vs "my wife" may be informal wording or a marriage
  since May. The key points now require a neutral clarifying question allowing both readings.
  R-HH-001 is added as conditional (the engine returns `cannot_determine` on `relationship`;
  the label had omitted it), HH-MARRY-001 is added to evidence, and major PC-X1 prohibits
  settling either side or telling the user they are wrong.
- **Rubric §2.6:** conflict labels never presume user error (generalises DEV-13).
- **A-01 (snapshot assumption):** the 2026-10-28 snapshot is assumed to still apply on the
  2026-11-01 `as_of`. Recorded in evaluation_benchmark §4 (with the date-sensitive
  facts/rules), §9, D-063 (still PROPOSED) and `manifest.json` (`policy_snapshot_assumption`).
  It is unverified until the G-15 drift check.
- **QA gap noted:** `engine_crosscheck` does not flag engine `cannot_determine` rules missing
  from `conditional_rule_ids`, which is how DEV-13's omission slipped through.

## 2026-10-29: Undetermined-rule warning added; dev labels approved

- **New QA warning:** `validate` now also lists rules the engine returns `cannot_determine` for
  that the label omits entirely (`engine_undetermined_unlabelled`). It is report-only and
  prints rule IDs only. Regression test added in `tests/test_benchmark.py`.
- **Dev triage, 13 warnings in 10 cases:**
  - 10 legitimate omissions: R-HH-006 in 9 cases (field never asked); R-APP-003/R-HFE-004
    in DEV-04/13 (downstream of the missing `hfe_status`).
  - 3 real omissions fixed: DEV-13 R-APP-002 as optional; DEV-14 R-HH-007 and R-PRI-002 as
    conditional.
  - Recorded in evaluation_benchmark §6.
- **Dev labels approved:** all 18 dev labels are `approved` on the developer's instruction,
  and the review sheet records the decisions. The triage fixes were applied immediately
  before approval.
- **Held-out labels:** still `candidate`. Developer review is pending, and the warning
  applies there too via `validate --heldout` (developer only).

## 2026-10-29: Held-out review sheet regeneration script

- The developer reported that `evaluation/heldout/test_review_sheet.csv` had been truncated
  to its header by a CSV-editing script. No generator existed in the repo, because the
  original authoring script was deleted (it held the labels).
- Added `scripts/regen_heldout_review_sheet.py` (stdlib only, **developer-run**, D-064):
  - reads the labels, inputs and manifest read-only, and compares their SHA-256 before and
    after the run;
  - reuses the sheet's existing header exactly;
  - writes atomically (temp file, fsync, `os.replace`);
  - refuses to overwrite a non-empty sheet without `--force`;
  - prints counts only.
- Tested by the agent only on a mock tree built from dev data, never on `evaluation/heldout/`.
  The output matched `dev_review_sheet.csv` cell for cell (20 columns, 0 mismatches).
- Review entries already typed into the truncated sheet cannot be recovered from the labels.

## 2026-10-29: Metric specification (D-066, PROPOSED)

- The developer reports the held-out label review complete and approved (done privately; the
  agent did not access `evaluation/heldout/`). They asked that the `undetermined-but-unlabelled`
  warnings **not** become labels, since only question-relevant requirements are scored.
- **Wrote `evaluation/metric_spec.md` from dev cases only:**
  - **Primary metrics, judged blind on the visible answer** (architecture-neutral): critical
    errors, required-information coverage (content key points), claim-level factual
    correctness and unsupported rate, missing-information and conflict identification,
    abstention and over-abstention, answer coverage, actionability.
  - **Diagnostics:** rule triggering, citations, retrieval recall@k, verifier.
  - **Failure, withheld-answer and rerun rules;** statistics.
  - **Dev denominators:** 18 cases; 33 content and 11 interaction key points; 6 missing-field
    instances; 3 conflicts; 3 abstention cases; 15 yes/partial cases; 9 yes cases; 52 gold
    facts; 17 required-rule instances.
- **Finding behind the coverage unit:** required-rule actions are broader than the question in
  some cases (e.g. R-HH-001 marriage registration in DEV-15, which asks about applicant
  roles). Key points are therefore the coverage unit; rule IDs move to diagnostic D1.
- Cross-references updated: INDEX, 05 §4, the register (Q-14 to Q-17), evaluation_benchmark §8.
- **Not done:** no freeze; no change to held-out files, labels or hashes.

## 2026-10-29: Model selection (D-067) and configuration A baseline

**Model selection**
- Protocol pre-registered before any output (`evaluation/model_selection/protocol.md`). It
  covers 12 dev cases (two per category, fixed rule), prompt `ms-1`, one strict schema, the
  35/25/20/10/10 scorecard and minimum acceptance criteria. Provider facts were checked on
  the official pages on 2026-10-29.
- Harness: `evaluation/model_selection.py` (stdlib HTTP).
- **Failures and fixes before any output was seen** (protocol §9):
  - Gemini returned an HTTP 503 whose error body is a list, which crashed the harness;
  - Groq's CDN rejected urllib's default agent (Cloudflare 1010), so the harness now sends an
    honest User-Agent;
  - the timeout was raised to 240 s.
- **Gemini 3.8 Flash** took 25–104 s for one-word probes and finished no case in about
  5 minutes. The developer stopped it and chose Groq.
- **Groq `gpt-oss-120b`, direct generation:**
  - schema-valid 11/12 on the first attempt (one provider-side `json_validate_failed`, so
    strict mode did not constrain decoding) and 12/12 after the retry;
  - accuracy 0.20; critical errors in 7/12 cases; uncertainty handling 0.25;
  - median latency 1.9 s; about US$0.0005 per call;
  - fails acceptance criteria 2 and 3. Recorded in D-067 as the developer's choice, with the
    failure disclosed. Scoring was by the agent and not blind (one system).

**Configuration A (direct LLM)**
- Added the `openai` client (D-036). New modules:
  - `llm.py`: client protocol, OpenAI-compatible client, typed failures, cost;
  - `generation.py`: strict schema from Pydantic, one bounded retry, fail closed;
  - `pipeline.py`: A → `FinalGuidance`, plus a shared answer renderer for blind scoring;
  - `prompts/generate_v1.md`: one prompt, with an evidence slot for B–D.
- Contracts: architecture §5 generation and report contracts added to `schemas.py`.
  Additions are proposed as D-068.
- `evaluation/run.py`: `run`, `check`, `sheet`. Every attempt's raw response is kept; failures
  stay in the output; the held-out split needs `--final`.
- `tests/test_baseline.py` (25 tests): parsing, schema validation (wrong type, missing field,
  bad enum, extra field), retry, fail-closed, invented citations, every transport-failure
  kind, the provider's schema rejection, and the real client against an httpx mock
  transport.
- Checks: `ruff check`, `ruff format --check`, strict `mypy` and `uv lock --check` are clean;
  118 tests pass.

**Dev run `20261028T203350Z-A-dev`:**
- 18/18 ok, no retries, no failures. US$0.0095 in total. Median latency 4.3 s, which includes
  waits on 429 throttling under the 8K tokens-per-minute limit.
- `check` passes. Blinded sheet: `evaluation/results/scoring/sheet-a2ab6598fd/`.
- **Structural diagnostics only, not primary metrics:**
  - required missing fields reported in the structured list: 2/6;
  - conflicts flagged: 0/3;
  - out-of-scope flagged: 3/3;
  - no whole-answer refusals on answerable cases.
- **Representative errors:**
  - DEV-07 says to wait until 21;
  - DEV-10 endorses one-year HFE validity;
  - DEV-13 gives 6-month validity and ignores the engaged / "wife" conflict.
- The run started before a typing-only refactor of `llm.py` (kwargs dict, test seam); its
  behaviour is identical.

**Next:**
- developer review of D-067 and D-068;
- developer blind scoring per metric_spec (D-066 is still PROPOSED);
- configurations B–D (retrieval, extraction, gate, rules wiring, verifier);
- benchmark freeze before any held-out run.

## 2026-10-29: Recommended path to submission (D-069, PROPOSED)

- **Situation:** about 1.5 h remain.
  - The selected model fails the direct-generation thresholds (D-067).
  - The README is a stub and the app does not call the pipeline.
  - C and D are not built.
- **Recommendation (D-069):** keep the model; build config B (BM25 RAG); wire the app to A/B;
  run A and B on dev only, reporting structural diagnostics with no comparative claim; write
  the README; check Docker; record the demo.
  - C and D are disclosed as designed but not built. The rule engine and its tests are the
    built evidence for the deterministic layer.
  - The held-out set stays sealed for a later full run.
- **Findings so far, for the README:**
  - **Direct generation without evidence** makes critical policy errors, e.g. HFE validity
    given as 6 or 12 months instead of 9, "wait until 21" instead of the core-occupier route,
    and an invented FT(PMC) meaning.
  - **It under-reports applicant-information signals:** 2/6 required missing fields and 0/3
    conflicts in the dev run.
  - **It handles explicit out-of-scope requests well:** 3/3 declined.
  - **The provider's strict schema mode** still produced one invalid enum value, which the
    bounded retry recovered.
  - **Gemini 3.8 Flash was unusable during the session:** 25–104 s for one-word probes, and
    HTTP 503.
  - **Groq's 8K tokens-per-minute limit** throttles runs but caused no failures.
- **Q-13 / C-17:** privacy was handled qualitatively in model selection (register updated).

## 2026-10-29: Configuration B, app, Docker and README (D-069 approved, D-070)

**Retrieval** (`retrieval.py`)
- BM25 over 89 usable facts, with one fact as one passage.
- Dev recall at k = 3 / 5 / 8 / 12: 0.23 / 0.33 / 0.42 / 0.52 (52 gold facts). 9/18 cases
  miss at least one gold fact at k = 12.
- Query variants tried: question only, and no synonyms. Neither helped materially.
- D-031's trigger for an alternative retrieval method is met, but there was no time to act
  on it. Disclosed.

**Configuration B** (`pipeline.run_rag`)
- Evidence goes into the shared prompt's slot. Citations are restricted to the bundle and
  mapped to official URLs. An uncited policy claim becomes an `evidence_gap`.

**Dev run `20261028T205255Z-B-dev`**
- 17/18 ok. DEV-12 failed with HTTP 413: `max_completion_tokens` 6000 plus the prompt went
  over the 8K tokens-per-minute limit, so the cap is now 4096 (D-070). DEV-09 needed one
  retry.
- 33/35 policy claims have an official source.
- Missing fields 3/6, conflicts 0/3, out-of-scope 3/3.
- Median latency 15.7 s (includes rate-limit waits). Cost US$0.0127.
- **Observations, not scores:**
  - B correctly gives the 9-month validity and the core-occupier route;
  - B over-generalises an FT(PMC) "unconfirmed" note into "eligibility for engaged couples is
    unconfirmed" (DEV-07, DEV-10, DEV-13);
  - neither A nor B flags conflicts.
- Combined blinded sheet: `evaluation/results/scoring/sheet-c286058da9/`. The A-only sheet
  was replaced.
- Diagnostics: `evaluation/results/diagnostics_dev.json` (`evaluation.run diagnostics`).

**App** (`app.py`)
- Live pipeline with an A/B toggle and three presets (dev cases DEV-01, DEV-04, DEV-10) that
  only fill the inputs.
- Signals are shown in separate sections. Source links per claim. Learning resources as
  links. A clear message when the API key is missing.
- New smoke test for that message.

**Docker**
- The image builds, the health check returns 200, a live B inference ran inside the
  container (9-month validity, citing `HFE-VALID-001`), the missing-key error is correct,
  and there is no `private_corpus` in the image.
- Rebuilt after the token-cap change.

**README**
- Full rewrite: run instructions, scope, what is and isn't built, architecture, data and
  licensing, model selection, evaluation design, dev diagnostics, error analysis,
  limitations, a 211-word deployment section, narrative and AI usage.

**Checks:** 129 tests pass; ruff, format, strict mypy and `uv lock --check` are clean.

**Still open:**
1. developer blind scoring (no primary metrics yet);
2. demo video link;
3. AI session log export to `ai_logs/` with redactions;
4. final rights clearance and the G-15 drift check;
5. benchmark freeze, held-out run, and configurations C and D (deferred).
