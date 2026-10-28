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

**Found:**
- New contradictions C-14 to C-17.
- Open questions Q-05 to Q-24.
- All policy facts quoted in the approach document are **unverified** until Phase 2.

## Phase 1 — Project setup and architecture (2026-10-28) — in progress

**Done:**
- `CLAUDE.md`: project instructions, scope, architecture invariants, Git workflow (D-027: the
  developer runs commits and pushes; the agent suggests them), verified commands.
- Scaffold:
  - `pyproject.toml` (src layout; Pydantic runtime; pytest/ruff/mypy in the `dev`
    dependency group);
  - `uv.lock` (18 packages pinned);
  - `src/bto_buddy/__init__.py`;
  - `tests/test_package.py`;
  - placeholder `README.md`.
- Decisions:
  - D-026: production infrastructure out of scope;
  - D-027: Git workflow, revised;
  - D-028: tooling, with uv and `uv.lock` approved;
  - D-029: architecture decisions on hold.
- Private anonymity term list (`references/private/anonymity_terms.txt`) for pre-push scans.
- The architecture layout proposal (modules, contracts, paths, gate design) was moved out of
  `04_architecture.md` into the **uncommitted** held draft
  `docs/proposals/architecture_layout_draft.md`, pending the developer's architecture
  review (D-029).

**Verified (macOS, uv 0.13.6, Python 3.13.2):**

| Command | Result |
|---|---|
| `uv lock` / `uv lock --check` | 18 packages resolved; lock up to date |
| `uv sync` | OK. pydantic 2.14.1, pytest 9.2.0, ruff 0.17.3, mypy 2.4.0 |
| `uv run pytest` | 1 passed |
| `uv run ruff check .` | All checks passed |
| `uv run ruff format --check .` | Already formatted |
| `uv run mypy` (strict) | No issues |

**Failures / resolved:**
- Docker Desktop: the agent couldn't install it (needs `sudo`). The developer installed it.
  Verified on 2026-10-28: Docker 29.9.2, engine started, `docker run --rm hello-world` OK.
  Project Docker commands are added at the deployment milestone.
- Commit `e163bdd chore: initialise project and tooling`, made by the developer.

**Architecture review (2026-10-28) — approved:**
- The developer approved review items A1–A11, recorded as **D-030 to D-040**. Each has a
  justification and a scope-alignment check.
- The review became the approved spec [architecture.md](architecture.md).
- Propagated to:
  - 01 (Q-05 resolved);
  - 03 (`aliases` field);
  - 04 (stack statuses);
  - the register (REQ-ARC-010/012 revised; REQ-ARC-015..019, REQ-VER-008, REQ-EVL-036/037
    added; Q-05/10/12/23 resolved);
  - CLAUDE.md (invariants, routing);
  - INDEX;
  - `.gitignore` (`.cache/`).

**Schedule (developer, 2026-10-28):**
- Target: complete and fully compliant by **2026-10-29 07:00**.
- The brief's 12–16-hour estimate is a reference only.
- All configurations A–D are planned; dropping B needs developer agreement.

**Still open before or during Phase 2:**
- Q-22 (facts schema field details);
- Q-06/Q-07 (premium, resale levy tiers);
- Q-08, Q-09, Q-11, Q-13–Q-21, Q-24;
- model selection;
- judge model.

**Repository and tooling setup (2026-10-28):**
- **Layout:** D-041 adopts the developer's recommended structure, simplified:
  - `llm.py` added;
  - `evaluation/baselines.py` and a separate retrieval-query file dropped;
  - benchmark and verifier claims split into physical dev/test files.
- **Files:**
  - `src/bto_buddy/app.py`: single Streamlit entry point; an honest shell with disclaimer and
    privacy notice, no pipeline yet;
  - `tests/test_smoke.py`: replaces `test_package.py`; uses Streamlit `AppTest`;
  - `Dockerfile`, `.dockerignore`, `.env.example`, `.streamlit/config.toml` (telemetry off);
  - `.gitignore`: merged with the developer's list, plus caches and temporary outputs.
- **Dependency:** Streamlit 1.66.1 via `uv add`; `uv.lock` now pins 51 packages.
- **Ruff:** ruff 0.17 formats Python blocks inside Markdown, so `docs/` is excluded (design
  sketches, not code).

**Verified (macOS, uv 0.13.6, Docker 29.9.2):**

| Check | Result |
|---|---|
| `uv sync` / `uv lock --check` | OK; 51 packages, lock up to date |
| `uv run ruff check .` / `ruff format --check .` | All passed / 5 files formatted |
| `uv run mypy` (strict) | No issues in 2 source files |
| `uv run pytest` | 1 passed (smoke: app renders, disclaimer visible) |
| `docker build -t bto-buddy .` | OK; image 820 MB (Streamlit brings numpy, pandas, pyarrow) |
| `docker run -p 8501:8501 --env-file .env.example bto-buddy` | `/_stcore/health` OK in ~4 s; Docker HEALTHCHECK `healthy` in ~8 s |
| Image contents | Runs as `app` (non-root); `/app` = `.venv`, `.streamlit`, `app.py`; no PDFs, `.env`, `references/` or `private_corpus` |
| `git check-ignore` | `.env`, private corpus raw/processed, `references/private/*`, `.cache/`, `tmp/`, `*.log`, Streamlit secrets, `.venv`, tool caches, `.DS_Store` all ignored; `.env.example` trackable |

**Noted:**
- **Playwright approved (D-042, option 2).** Added as the opt-in `capture` group (1.64.1);
  `uv.lock` now has 54 packages. Verified:
  - absent from the default `uv sync` env and the Docker (`--no-dev`) install set;
  - Chromium headless shell 156 installed to the user cache, outside the repo;
  - offline launch expanded a local `<details>` accordion. No external site was accessed.

**Next:**
1. Implement the pure core: `schemas.py` and `policy.py` (facts/rules loading, rule
   interpreter, gate, profile assessment), with unit tests against a synthetic fixture KB.
   No LLM calls.
2. Then Phase 2: source verification and authoring `policy_facts.jsonl`.
