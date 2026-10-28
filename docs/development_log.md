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
3. **Capture run:** Playwright (`--group capture`), approved pages only. No crawling,
   link-following or transactional pages. Output goes to `data/private_corpus/raw/`
   (Git-ignored), with SHA-256 and timestamps in `data/sources_manifest.json`.
4. **Extraction and completeness audit:** 8 checks (03 §2.7), output to
   `data/private_corpus/processed/`, plus `data/source_coverage.csv`.
5. **Authoring:** `data/policy_facts.jsonl` (independently authored, verified, rights-reviewed,
   with `aliases`) and `data/policy_rules.yaml` (declarative, D-038). Finalise Q-22.

**Can proceed in parallel, with no dependence on real facts:**
- `schemas.py` and `policy.py` (loaders, rule interpreter, gate, profile assessment), with
  unit tests against a clearly fictional fixture KB in `tests/fixtures/`.
