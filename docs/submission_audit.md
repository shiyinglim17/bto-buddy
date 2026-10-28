# Pre-submission audit (2026-10-29)

Requirement-by-requirement check of the 30 MANDATORY items in
[project_context/requirements_register.md](project_context/requirements_register.md), plus
the data-rights, anonymity, secrets and reproducibility checks. Status: ✅ met · ⚠️ partly
met or met with a disclosed gap · ❌ not met. The agent wrote this audit; the developer
reviews it.

## 1. Mandatory requirements

| ID | Requirement (short) | Where | Acceptance evidence | Status |
|---|---|---|---|---|
| REQ-PRB-001 | Problem relevant to SG public-sector stakeholders | README §3 | Names the citizen group (first-time BTO couples) and the answering agency | ✅ |
| REQ-PRB-002 | AI in the core, not just an API call | README §4, §8; `src/bto_buddy/` | Retrieval, grounded generation and claim verification; A vs B and B vs D ablation results | ✅ |
| REQ-PRB-003 | Fresh project | Git history; D-015 | History starts with this project | ✅ |
| REQ-DAT-001 | Provenance, processing, licensing, privacy for all data | README §5; `data/sources_manifest.json`; `docs/data_sources.md` | Every dataset has a row with provenance and Git status | ✅ |
| REQ-DAT-002 | Defend synthetic data | README §5 "Synthetic-data methodology and defence" | Why, how, leakage controls, fidelity limits | ✅ |
| REQ-DAT-003 | Representativeness | README §5 "Representativeness" | States covered and excluded households, tiers and policy date | ✅ |
| REQ-LIC-001 | Source licensing and robots.txt | README §5; D-055, D-057, D-060; manifest rights records | 403 respected, FAQs excluded for robots.txt; final manual rights read (`cleared`) **pending** | ⚠️ |
| REQ-PRIV-001 | Personal data ethics | README §5 "Privacy" | Synthetic-only; UI warning; no logging | ✅ |
| REQ-EVL-001 | Justified evaluation method | README §7 "Why this method" | Ablation rationale; blind human scoring planned | ✅ |
| REQ-EVL-002 | Honest limitations | README §8 (warnings), §10 | Disclosure of incomplete held-out, unscored primary metrics, model threshold failure | ✅ |
| REQ-MOD-001 | Operational model justification | README §6 | Latency, cost, portability, data handling, task fit; rejected options | ✅ (no head-to-head; disclosed) |
| REQ-DOC-001 | Objectives, rationale, implementation, results, execution, limitations | README §1–§13 | All sections present | ✅ |
| REQ-DOC-002 | 150–250-word deployment section | README §12 | 210 words (`awk` + `wc -w`) | ✅ |
| REQ-DOC-003 | Development narrative | README §13 | Consistent with `docs/decisions.md` D-052 to D-073 | ✅ |
| REQ-DOC-004 | Write-up matches code; no overclaiming | README §2 built-vs-designed table; §3 below | Every number traced to a saved output (§3) | ✅ |
| REQ-DOC-005 | Limitations and enhancements if constraints removed | README §10, §11 | Both present | ✅ |
| REQ-SUB-001 | Full deployment/execution instructions | README §1 | Step-by-step Docker guide, troubleshooting, clean-clone smoke test | ✅ |
| REQ-SUB-002 | Dockerised | `Dockerfile`; README §1 | `--no-cache` build from a fresh clone; health `ok`; live answers in the container (2026-10-29) | ✅ |
| REQ-SUB-003 | 3–5 min demo video, URL in README | README header | **Placeholder only** | ❌ |
| REQ-SUB-004 | Private repo, collaborator invited | Private notes | Not verifiable from the repo | ⚠️ developer |
| REQ-SUB-005 | Anonymous re organisation and role | Whole repo | `git grep -iFf references/private/anonymity_terms.txt` over tracked and new files: no matches | ✅ for the repo · ❌ risk for logs (§4) |
| REQ-SUB-006 | Repo unchanged during evaluation | Process | Developer's responsibility after submission | ⚠️ developer |
| REQ-SUB-007 | Submit via designated channel | Private | Not verifiable from the repo | ⚠️ developer |
| REQ-SUB-008 | Deadline | Private | Not verifiable from the repo | ⚠️ developer |
| REQ-SUB-009 | Coding-agent section at end of README | README §15 (last section) | Position checked | ✅ |
| REQ-SUB-010 | All coding-agent session logs uploaded; location in README | README §15 names `ai_logs/` | **`ai_logs/` does not exist.** 5 local session files (about 26 MB) need redaction first (§4) | ❌ |
| REQ-NFR-001 | Runs from README on a clean machine | README §1 smoke test | 8/8 steps passed from a fresh clone (macOS); Linux/Windows untested | ✅ (macOS) |
| REQ-NFR-002 | Code quality | `pyproject.toml`, `tests/` | `uv run pytest`, `ruff check`, `ruff format --check`, `mypy --strict`: all pass | ✅ |
| REQ-NFR-003 | Developer can explain the rationale | Code comments; `docs/decisions.md` | Rationale comments at non-obvious choices; 73 decisions with reasons | ✅ |
| REQ-NFR-004 | Works within free tier; paid needs noted | README §1 troubleshooting, §10, §12 | The app works on the free tier; **the full evaluation does not fit one day's free quota** (held-out B/D 7/30), disclosed; paid tier noted for production | ⚠️ |

**Approved (non-mandatory) items worth noting:**
- **REQ-EVL-010 and REQ-EVL-013:** 4 configurations, or A/C/D if constrained. Built A/B/D
  instead, under the approved D-069 and D-071 deviations; C's omission is documented.
- **REQ-EVL-019:** held-out set frozen (D-073), labels unchanged (SHA-256 check in
  `load_test_labels`).
- **REQ-DOC-017** (limitations list) and **REQ-PRIV-010** (free-tier data terms) are in
  README §10.
- **REQ-SCP-014:** the demo presets cover the 3 archetypes.

## 2. One frozen policy-facts version

| Consumer | How it loads the KB | Evidence |
|---|---|---|
| Streamlit app (local and Docker) | `pipeline.get_index()` → `policy.load_kb()` → `data/policy_facts.jsonl` (`BTO_BUDDY_DATA_DIR=/app/data` in the image, copied from the same file) | Dockerfile `COPY data/policy_facts.jsonl …` |
| BM25 index | `retrieval.build_index(policy.load_kb())` | `kb_version` stored in every evidence bundle and B/D run record |
| Rule registry | `policy.load_rules()`; `validate_registry` requires `reg.kb_version == kb.kb_version` and every cited fact to exist | 0 errors |
| Evaluation (dev and held-out) | Same pipeline; benchmark manifest `kb_version: kb-2026-10-28.1` | B/D `run_metadata.json` record `kb-2026-10-28.1` |

- `sha256(data/policy_facts.jsonl)` = `30b73603…` equals the freeze record in
  `data/corpus/corpus_version.json`. The same holds for `policy_rules.yaml`.
- The Git blob of both files is identical in every commit used for the saved runs
  (`ea94cbf` to `8369092`). The last change was `1235c67`, before the benchmark was created.
- Enforced by `tests/test_policy_kb.py::test_one_frozen_kb_for_app_rules_retrieval_and_benchmark`.
- **Caveat:** the run metadata records `kb_version` and the Git commit, not the file hash. The
  dev runs were made on dirty trees (`-dirty`), so file identity at run time rests on the
  unchanged blob history, not on a recorded hash.

## 3. Claims traced to code or saved outputs

| README claim | Source | Check |
|---|---|---|
| 89 facts, 53 verified / 36 snapshot_checked | `data/corpus/corpus_version.json` | ✅ |
| 24 rules | `data/policy_rules.yaml` | ✅ |
| 48 cases, 6 × 8, 18/30, 0 cross-split near-duplicates | `evaluation/benchmark/manifest.json`; `evaluation.benchmark validate` | ✅ |
| Dev metrics table, paired tests, claim-level B vs D | `evaluation/results/metrics_dev.json` (byte-reproducible) | ✅ |
| Dev latency and cost | `evaluation/results/diagnostics_dev.json` | ✅ |
| Retrieval recall@k | `diagnostics_dev.json` | ✅ |
| Verifier confusion matrix | `20261028T211724Z-D-dev/claim_annotations.jsonl`, `verifier_eval.json` | ✅ (agent labels, disclosed) |
| Held-out table, 23 failures, judge 25/25 insufficient | `evaluation/results/metrics_test.json`; run predictions | ✅ |
| 7-case exploratory subset | Computed from saved held-out predictions with `evaluation.metrics` functions; not saved as a file | ⚠️ recomputable, not persisted |
| Model selection figures | `evaluation/model_selection/runs/20261028T201952Z/scorecard.json` | ✅ |
| Live re-run variance (46/49; 17/18; 5/18) | Clean-clone re-runs, **not kept** (development_log 2026-10-29 audit entry) | ⚠️ not persisted |
| Deployment cost (2,650 / 520 tokens, US$0.0007) | Dev B run metadata | ✅ |

**No unsupported feature claims remain:** C, rules-in-answers and human scoring are all
marked as not built or not done.

## 4. Restricted content, secrets and anonymity

- **Private files tracked:** none (`references/`, `data/private_corpus/`,
  `evaluation/heldout/`, `.env`).
- **Secrets:** no key-like strings in tracked or new files. The only regex hit is the scan
  command in `CLAUDE.md`.
- **Anonymity:** no identifying terms in tracked or new files.
- **Account identifier:** the Groq organisation ID (`org_…`) appears inside saved HTTP 429/413
  error messages: dev B/D 1 line each, held-out B 23, held-out D 30. It is not a credential.
  Redacting it would change the pre-verification hashes that D records, so it is left as is
  and flagged.
- **Source-text overlap** (8-word shingles shared with the private corpus, URLs removed;
  counts only, no text printed):
  - Almost all overlap in `policy_facts.jsonl` (73 facts) and `policy_rules.yaml` is the
    `source.section` field, which holds verbatim section headings used as citation
    locators. That is short, factual and needed for provenance.
  - **One fact statement, `HH-CIT-001`, shares one 8-word run with its source.** The
    project's own `corpus.py facts` check (different normalisation) passed it. It is not
    reworded now, because the KB is frozen and every saved run depends on its hash.
    Developer review recommended.
  - Saved predictions and the scoring sheet share 2–8 runs per file (model paraphrases of
    the authored facts). `docs/project_context/02_policy_sources.md` shares 24 (mostly
    section names). Low risk; no passage-level reproduction found.
- **Coding-agent logs (not in repo):** 5 local session files. Counts only: two sessions
  contain lines matching the private anonymity terms (5 and 9 lines); all contain local
  paths with the developer's username (28 to 2,334 lines); none contains a Groq-key-like
  string. Sessions that authored facts also contain private HDB source text, which must be
  redacted (REQ-SUB-020; escalation case C-09).

## 5. Prioritised blockers and improvements

**Blockers (mandatory, must fix before submission):**
1. **REQ-SUB-010: add `ai_logs/`.** Export all 5 sessions, then redact (a) identifying terms,
   (b) private HDB source text from fact-authoring sessions, and (c) optionally local paths.
   List every redaction in `ai_logs/REDACTIONS.md`. Do not drop failed sessions. The agent
   can prepare a redaction script on request; the developer decides what to redact.
2. **REQ-SUB-003: record the 3–5 min demo and put the URL in the README header.** Use the 3
   presets with D, and show one ⚠️ unconfirmed and, if it occurs, one withheld claim.
3. **REQ-SUB-004/006/007/008:** private-repo invite, submission channel and freezing the repo
   after submission (developer actions).

**High-value improvements (if time allows):**
4. **Complete the held-out run** after the Groq daily quota recovers (about 24 h) or on a paid
   tier: B on the 23 failed cases (`--cases`), then `verify`, then `metrics`. Keep the first
   attempt and disclose both. Without this, held-out B/D numbers mostly measure quota
   failures.
5. **Blind human scoring** with `evaluation.run sheet` (critical errors, coverage,
   actionability). These are the pre-registered primary metrics and are currently unreported.
6. **Final rights read** (`rights_review: cleared`), and a check of `HH-CIT-001`'s wording.
7. **Record the KB file hash in run metadata** for future runs, so file identity no longer
   rests on Git history.

**Lower priority:**
8. Persist the 7-case exploratory subset and the live re-run variance as files, if they are
   to be cited as results.
9. Test the Docker steps on Linux and Windows hosts.
