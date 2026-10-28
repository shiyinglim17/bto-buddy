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
