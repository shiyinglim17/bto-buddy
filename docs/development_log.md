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

**Failures / blocked:**
- **Docker Desktop install failed:** `brew install --cask docker-desktop` needs `sudo` for
  its CLI symlinks, and the agent session can't enter a password. Homebrew rolled back
  cleanly. **The developer needs to run the install in their own terminal.** Docker commands
  stay unverified until then (REQ-SUB-002, REQ-NFR-001).

**On hold (D-029), pending the architecture review:**
- Q-23 (stack);
- Q-12 (gate design);
- Q-10 (paths);
- Q-22 (facts schema / contracts).

**Next:**
1. The developer commits the scaffold.
2. Architecture review.
3. Then `contracts.py` and the facts/rules loaders, with unit tests and no LLM calls.
4. Then Phase 2: source verification and the policy-facts corpus.
