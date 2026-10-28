# Requirements Register

Stable IDs: `REQ-<AREA>-<NNN>`. IDs are never renumbered or reused. Superseded items keep
their ID and are marked as superseded. Decisions are in [../decisions.md](../decisions.md).

**Status values:** `MANDATORY` (assessment brief) · `APPROVED` · `PROPOSED` · `OPEN` ·
`SUPERSEDED`.
**Source tags:** `[ASM p.N]` assessment brief · `[APP p.N]` project approach · `D-xxx` / `BD-xx`
decisions. Page numbers are physical PDF pages.

**Areas:**

| Code | Area | Code | Area |
|---|---|---|---|
| PRB | problem | ARC | architecture |
| SCP | scope | VER | verifier |
| SRC | sources | EVL | evaluation |
| DAT | data | MOD | model selection |
| LIC | licensing | DOC | documentation |
| PRIV | privacy | SUB | submission |
| NFR | non-functional | | |

**Planned components** (traceability only; nothing is implemented):

| Group | Components |
|---|---|
| Data pipeline | `source_acquisition` · `source_manifest` · `coverage_audit` · `policy_facts_kb` · `rule_registry` · `visual_resource_registry` |
| Runtime | `profile_extractor` · `coverage_gate` · `rule_engine` · `retriever` · `generator` · `verifier` · `report_ui` |
| Evaluation | `eval_harness` · `benchmark_dataset` · `verifier_claim_set` · `retrieval_qrels` |
| Delivery | `docker` · `README` · `ai_logs` · `repo_hygiene` |

## 1. Register

### Problem (PRB)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-PRB-001 | Problem relevant to SG public-sector stakeholders (agency/ministry/citizen group) | MANDATORY | [ASM p.1][APP p.29] | 01 §1 | README | README names the stakeholder (citizen group: BTO applicants) |
| REQ-PRB-002 | AI in core functionality; significant AI integration, not just an API call in a web app | MANDATORY | [ASM p.1, 2][APP p.29] | 04 §1 | profile_extractor, generator, verifier | Architecture section + A–D ablation showing component contribution |
| REQ-PRB-003 | Fresh project; no recycled past project | MANDATORY | [ASM p.4] | 06 §5; D-015 | repo_hygiene | Git history starts fresh; PolicyProof recorded as brainstorm only |
| REQ-PRB-010 | BTO Buddy = pre-application preparation layer; transparency & preparation, not replacing authoritative assessment | APPROVED | [APP p.1–2]; BD-01 | 01 §2 | report_ui, README | UI/README disclaimers; no determinations made |
| REQ-PRB-011 | Problem statement | APPROVED | [APP p.3] | 01 §3 | README | README problem section matches |
| REQ-PRB-012 | Research question (hybrid vs conventional LLM reliability) | APPROVED | [APP p.3] | 01 §4 | eval_harness | Results answer it via A vs C/D comparisons |
| REQ-PRB-013 | Substantiate complexity from official docs; never invent statistics on confusion/hotline/benefit | APPROVED | [APP p.3]; D-025 | 01 §5 | README | Every statistic in README cites a source; manual review |
| REQ-PRB-014 | Own-research questions are optional evidence tasks | APPROVED (tasks OPEN) | [APP p.3, 29–30]; D-025 | 01 §5 | README | Included only with citations, else omitted |
| REQ-PRB-015 | Downstream admin-workload reduction is a hypothesis requiring future user testing | APPROVED | [APP p.2] | 01 §2.2 | README | Phrased as hypothesis/future work |

### Scope (SCP)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-SCP-001 | MVP scope table is authoritative (Core/Limited/Context/Excluded incl. ballot prediction & comprehensive determination) | APPROVED | [APP p.17–18]; D-008 | 01 §6 | coverage_gate, policy_facts_kb | Gate config and fact `scope_tier` values match table; out-of-scope benchmark category |
| REQ-SCP-002 | Core capabilities implemented and evaluated | APPROVED | [APP p.17] | 01 §6.1 | all runtime; eval_harness | Each Core area has facts, rules (where explicit) and benchmark cases |
| REQ-SCP-003 | Limited only where authoritative evidence and testable requirements exist | APPROVED | [APP p.17] | 01 §6.1 | policy_facts_kb | Coverage matrix shows verified source per Limited fact |
| REQ-SCP-004 | Context-only topics never trigger eligibility calculations | APPROVED | [APP p.17] | 01 §6.1 | rule_engine, generator | No calculation rules; benchmark prohibited-conclusion checks |
| REQ-SCP-005 | Excluded capabilities handled by coverage gate + official redirection | APPROVED | [APP p.17] | 01 §6.1, 04 §2 | coverage_gate | Out-of-scope category abstention results; gate unit tests |
| REQ-SCP-006 | Scope expansion requires explicit approval + evaluation-plan update | APPROVED | [APP p.17] | 01 §6.1 | — | decisions.md entry precedes any expansion |
| REQ-SCP-007 | Source-discovery matrix/ideas do not expand MVP | APPROVED | [APP p.1, 4, 17]; BD-02 | 02 §3 | policy_facts_kb | Every fact maps to an MVP tier |
| REQ-SCP-008 | HFE boundary: explain HFE↔purchase/grants/loans; no grant/loan/financing determination; redirect | APPROVED | [APP p.18] | 01 §6.2 | coverage_gate, generator | Benchmark cases with prohibited conclusions on amounts |
| REQ-SCP-009 | Videos excluded from core corpus; optional contextual links for Step 1/Step 2 HFE topics | APPROVED | [APP p.12, 18] | 02 §4 | visual_resource_registry | Videos absent from policy_facts; registry entries with display conditions |
| REQ-SCP-010 | Income/employment only for HFE preparation, documents, follow-ups; no income-ceiling/eligibility/financing calc | APPROVED | D-013 | 01 §6.3 | rule_engine, profile_extractor | No income-calculation code; benchmark checks |
| REQ-SCP-011 | No claim of comprehensive current/historical policy coverage | APPROVED | [APP p.28] | 01 §9 | README, report_ui | README/UI state supported period & scope |
| REQ-SCP-012 | Scope discipline: ~4–5 policy areas handled accurately | APPROVED | [APP p.28] | 01 §9 | — | Final area count reported |
| REQ-SCP-013 | Separate missing applicant info (A) vs missing corpus evidence (B) in architecture, benchmark, docs | APPROVED | [APP p.18–19] | 01 §7 | profile_extractor, verifier, eval_harness | Distinct response fields; distinct benchmark labels |
| REQ-SCP-014 | Demo: 3 archetypes (straightforward, missing info, misconception); representative, not cherry-picked | APPROVED (archetypes refinable) | [APP p.20–21] | 01 §8 | README (video) | Video shows the three; README notes known failure modes |

### Sources (SRC)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-SRC-001 | Four HDB seed pages | APPROVED (as seeds) | [APP p.4]; D-007 | 02 §1 | source_manifest | Manifest contains seeds |
| REQ-SRC-002 | Manifest: URL, title, access timestamp, section, extraction method, SHA-256, policy scope | APPROVED | [APP p.4, 14] | 03 §2.3 | source_manifest | `data/sources_manifest.json` schema-validated |
| REQ-SRC-003 | Passages keep enough context (condition stays with its applicant-group heading) | APPROVED | [APP p.4] | 03 §2.4 | source_acquisition | Spot-check in coverage audit **Phase 2b:** one passage per section, sub-headings keep their accordion parent; fixture test (data_sources §12). |
| REQ-SRC-004 | Frozen, versioned corpus for evaluation | APPROVED | [APP p.5] | 02 §2 | policy_facts_kb | `kb_version` recorded in every run |
| REQ-SRC-005 | Discovery path seeds→anchors→linked→PDFs/visuals; manual mapping | APPROVED | [APP p.5] | 02 §2 | — | Matrix in 02 §3 (done) |
| REQ-SRC-006 | Capture only approved pages (manual rendered-DOM or controlled automation, permissions documented); expand info sections; no auto link-following; no transactional services; no crawling | APPROVED | [APP p.11, 14] | 03 §2.6 | source_acquisition | Manual capture of approved pages only (D-055); `acquisition.method` and hashes in `data/sources_manifest.json`; procedure in data_sources §7 |
| REQ-SRC-007 | Normalise headings, paragraphs, tables, lists, links, metadata | APPROVED | [APP p.11] | 03 §2.6 | source_acquisition | Processed passages retain structure **Phase 2b:** `scripts/corpus.py extract` (stdlib, D-059 approved); tables keep spans and nesting. |
| REQ-SRC-008 | Media only when unique & essential; simplest method | APPROVED | [APP p.11] | 02 §4 | source_acquisition | Media decision recorded per resource |
| REQ-SRC-009 | PDFs: HTML-equivalent check first; PyMuPDF + manual validation; keep title/URL/page/pub date/section; OCR only if needed | APPROVED | [APP p.11–12] | 02 §4 | source_acquisition | Manifest entries for PDFs with page refs **Phase 2b:** S07/S08 reviewed manually page by page, page refs in `source.locator`; D-052 approved (manual review, no parser). |
| REQ-SRC-010 | Infographics: contextual registry (title, URL, topic, stage, display conditions); no runtime image interpretation; embed only with rights + reference | APPROVED | [APP p.12] | 02 §4 | visual_resource_registry | `data/visual_resources.json`; no vision calls in code **Phase 2b:** `data/visual_resources.json` (M00, M01, M03, M04), links only, `evidence: false`. |
| REQ-SRC-011 | Videos: registry only; never policy evidence unless independently validated | APPROVED | [APP p.12] | 02 §4 | visual_resource_registry | As REQ-SCP-009 |
| REQ-SRC-012 | Extraction-completeness checks (8: accordion, section, link, table, exception, traceability, temporal, duplicates) | APPROVED | [APP p.12–13] | 03 §2.7 | coverage_audit | Audit report per source **Phase 2b:** `data/corpus/extraction_report.json`; single-snapshot limitation recorded per source. |
| REQ-SRC-013 | Policy coverage matrix: each supported rule ≥1 verified source; exceptions checked | APPROVED | [APP p.13] | 03 §2.7 | coverage_audit | `data/source_coverage.csv` **Phase 2b:** `data/source_coverage.csv` (36 rows); G-17 per-status document gap; U-01 to U-03 unconfirmed (D-061). |
| REQ-SRC-014 | Minimum MVP source set decided in Phase 2; no auto-inclusion; no "four pages" claim until validated | APPROVED | D-007 | 02 §1 | — | Phase 2 decision entry |
| REQ-SRC-015 | Record URL, retrieval date, effective date, scope; app states supported policy period | APPROVED (period OPEN) | [APP p.28]; D-021 | 03 §2.8 | policy_facts_kb, report_ui | Fields populated; UI/README show period **Phase 2b:** Period: "HDB sources retrieved 28 Oct 2026"; no stated effective dates (data_sources §13). |

### Data (DAT)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-DAT-001 | Document provenance, processing, licensing, privacy for all data | MANDATORY | [ASM p.2][APP p.29] | 03 | README | README data section covers every dataset |
| REQ-DAT-002 | Synthetic data meaningful/high-fidelity, with defence | MANDATORY | [ASM p.2] | 03 §4 | README | Defence paragraph |
| REQ-DAT-003 | Representativeness; what data does/doesn't cover | MANDATORY | [ASM p.3] | 03 §9 | README | Coverage statement |
| REQ-DAT-010 | `data/policy_facts.jsonl` canonical KB: independently authored, source-attributed, validated, rights-reviewed | APPROVED | [APP p.4]; D-005 | 03 §2.1 | policy_facts_kb | All facts `validation.status=verified`, `rights_review=cleared` **Phase 2b:** 89 facts; all 47 critical + 4 rule-cited facts `verified` against the snapshot (D-058 revised, approved); rights `overlap_checked`, `cleared` pending. |
| REQ-DAT-011 | App, BM25 index, Docker and primary eval use the same reviewer corpus | APPROVED | [APP p.4] | 03 §2.1 | retriever, eval_harness, docker | Config points to one file; run metadata **Phase 2b:** `bto_buddy.policy.load_kb()` is the single loader. |
| REQ-DAT-012 | Private corpus not required for execution or reviewer evaluation | APPROVED | [APP p.4, 13]; D-005 | 03 §2.1 | docker | Clean-machine run with `data/private_corpus/` absent **Phase 2b:** `tests/test_policy_kb.py` loads and resolves the KB from tracked files only; Docker copies only L2/L3. |
| REQ-DAT-013 | Same retrieval interface for both corpora; document coverage differences; no cross-corpus result claims | APPROVED | [APP p.13] | 03 §2.2 | retriever | Interface accepts either corpus; README statement |
| REQ-DAT-014 | Rule registry encodes only explicit, reliable rules; no binary forcing of discretionary decisions | APPROVED | [APP p.15] | 03 §3 | rule_registry, rule_engine | Rule review checklist; unit tests **Phase 2b:** `data/policy_rules.yaml` (24 rules, D-062 approved); discretionary cases → human review or a redirect (data_sources §19). |
| REQ-DAT-015 | Rules reference reviewer-accessible fact IDs (private passage IDs optional provenance) | APPROVED | D-006 | 03 §3 | rule_registry | Every `source_fact_id` resolves in policy_facts |
| REQ-DAT-016 | Dataset C separate from KB and runtime verifier | APPROVED | [APP p.15] | 03 §4 | benchmark_dataset | Separate files; no label derived from verifier |
| REQ-DAT-017 | Fictional profiles, synthetic names; never real records | APPROVED | [APP p.16] | 03 §4 | benchmark_dataset | Dataset review |
| REQ-DAT-018 | Record model IDs, prompt versions, inference settings, corpus versions, saved predictions; offline scoring distinct from live inference | APPROVED | [APP p.15] | 03 §7 | eval_harness | Run metadata files; rescoring from saved predictions works offline |
| REQ-DAT-019 | Data paths per D-022 | APPROVED | D-022 | 03 §1 | repo_hygiene | Files at those paths |
| REQ-DAT-020 | Minimal typed policy-facts schema | APPROVED | D-023, D-059 | 03 §2.5 | policy_facts_kb | Pydantic model + validation test **Phase 2b:** `bto_buddy.schemas.PolicyFact` + tests (D-059 approved). |
| REQ-DAT-021 | Reviewers build index and run Docker without downloading HDB pages | APPROVED | [APP p.14] | 03 §7 | docker, retriever | Offline clean-machine test |
| REQ-DAT-022 | Capture/extraction scripts optional, not startup/eval dependencies | APPROVED | [APP p.14] | 03 §7 | source_acquisition | Docker image doesn't invoke them |

### Licensing (LIC)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-LIC-001 | Comply with source licensing and robots.txt | MANDATORY | [ASM p.2][APP p.29] | 03 §5 | source_acquisition | Rights review record per host |
| REQ-LIC-010 | Never commit complete HDB HTML; store in `data/private_corpus/` (Git-ignored) | APPROVED | [APP p.13]; BD-03 | 03 §5.2 | repo_hygiene | `.gitignore` entry (done); `git ls-files` check |
| REQ-LIC-011 | Substantial-text passages and derived indexes Git-ignored unless permission | APPROVED | [APP p.14] | 03 §5.2 | repo_hygiene | `git ls-files` check before submission |
| REQ-LIC-012 | Never claim HDB granted redistribution licence | APPROVED | [APP p.14]; D-024 | 03 §5.1 | README | Wording review |
| REQ-LIC-013 | Terms of Use and Copyright Act 2021 ss 243–244 recorded as preliminary; verify in Phase 2 | APPROVED (ToU read 2026-10-28; statute via a secondary source; see data_sources §6, D-057) | [APP p.14]; D-024 | 03 §5.1 | — | Phase 2 rights note |
| REQ-LIC-014 | robots.txt check for each host | APPROVED (www.hdb.gov.sg done 2026-10-28; file.go.gov.sg and mynicehome not checked, no automated access used) | [ASM p.2]; D-024 | 03 §5.1 | source_acquisition | Recorded robots.txt snapshot/date |
| REQ-LIC-015 | Review all tracked data for copyright/privacy/credentials before submission | APPROVED | [APP p.14] | 03 §5.2 | repo_hygiene | Pre-submission checklist **Phase 2b:** Fact overlap check done (max 7 shared words); developer clearance outstanding. |
| REQ-LIC-016 | Re-download ≠ reconstruct frozen snapshot; hashes and capture dates recorded | APPROVED | [APP p.13] | 03 §5.1 | source_manifest | SHA-256 + timestamp per source |
| REQ-LIC-017 | Project-context docs contain authored summaries, not substantial copied text | APPROVED | D-016 | 02 note | repo_hygiene | Phase 0 audit (§4 below) |

### Privacy (PRIV)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-PRIV-001 | Address ethics/handling if personal data | MANDATORY | [ASM p.2][APP p.29] | 03 §6 | README | Synthetic-only statement |
| REQ-PRIV-010 | Free-tier API data terms unsuitable for real PII — stated as limitation & deployment consideration | APPROVED | [APP p.28] | 03 §6 | README | Limitation present |

### Architecture (ARC)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-ARC-001 | Three essential capabilities (retrieve, generate profile-specific guidance incl. missing info, verify & flag) | APPROVED | [APP p.17] | 04 §1 | retriever, generator, verifier | Each present and tested |
| REQ-ARC-002 | Deterministic Python validation for structured fields; no autonomous agents / complex frameworks / unnecessary vector DB | APPROVED | [APP p.17]; BD-09 | 04 §1 | all runtime | Dependency list review |
| REQ-ARC-003 | 5-stage pipeline (extract/validate → rules ∥ BM25 → grounded generation → claim verification → report) | APPROVED | [APP p.17]; BD-04 | 04 §2 | all runtime | Module structure; integration test |
| REQ-ARC-004 | Coverage gate before generation | APPROVED | [APP p.21]; BD-05 | 04 §2 | coverage_gate | Unit tests; out-of-scope results |
| REQ-ARC-005 | Missing-information contract: `missing_profile_fields`, `evidence_gaps`, `profile_conflicts`, `out_of_scope_reasons` | APPROVED | [APP p.20]; BD-06 | 04 §3 | profile_extractor, generator | Pydantic response model |
| REQ-ARC-006 | Policies as structured conditions/exceptions/dates/sources | APPROVED | [APP p.22] | 04 §4 | policy_facts_kb, rule_registry | Schema fields populated |
| REQ-ARC-007 | Typed objects between all modules | APPROVED | [APP p.28] | 04 §4 | all runtime | Type-checked interfaces |
| REQ-ARC-008 | Hard rules deterministic; complex interpretations evidence-linked + official confirmation; justify which is which | APPROVED | [APP p.28] | 04 §4 | rule_engine | Rule table with justification column **Phase 2b:** each rule has `basis` (source_established / interpretation); interpretations always require human review; `tests/test_rules.py`. |
| REQ-ARC-009 | Answers link to actual HDB webpages | APPROVED | [APP p.13] | 04 §4 | report_ui | Every supported claim shows a URL |
| REQ-ARC-010 | BM25 only (+ aliases, topic filter, rule-linked facts); dense/hybrid/rerank only if dev recall@5 < 0.90 because of paraphrase | APPROVED | [APP p.17, 21]; D-031 | architecture §4.2 | retriever | Recall@k table; escalation decision only on the trigger |
| REQ-ARC-011 | One generation model; no unnecessary orchestration | APPROVED | [APP p.21] | 04 §6.1 | generator | Config |
| REQ-ARC-012 | Dependencies limited to pydantic, pyyaml, rank-bm25, openai (compatible client), streamlit; dev pytest/ruff/mypy/types-PyYAML; stdlib statistics; `scripts/` stdlib-only (Playwright group removed) | APPROVED | [APP p.21]; D-036; D-042 superseded by D-056 | architecture §11.1 | all | `pyproject.toml` / `uv.lock` match the list |
| REQ-ARC-013 | Never assume missing applicant values | APPROVED | [APP p.19] | 04 §3 | profile_extractor | Missing-info benchmark category |
| REQ-ARC-014 | Missing evidence ≠ requirement absent | APPROVED | [APP p.20] | 04 §3 | generator, verifier | Prohibited-conclusion labels |
| REQ-ARC-015 | Linear 8-stage pipeline, ≤3 LLM calls; A–D from one pipeline; pure modules don't import the LLM client | APPROVED | D-030 | architecture §3, §11.2 | pipeline | Integration tests per config; import-boundary test |
| REQ-ARC-016 | Extracted fields need verbatim input quotes (quote guard); missing fields scoped to the topics asked; template follow-ups | APPROVED | D-032 | architecture §3.1, §6 | profile_extractor | Unit tests: quote guard, topic-scoped missing fields |
| REQ-ARC-017 | Closed-enum topic tags → deterministic tier map; partial scope; non-couple households out of scope | APPROVED | D-033 | architecture §3.1, §5 | coverage_gate | Every topic mapped; gate unit tests; out-of-scope category |
| REQ-ARC-018 | Rules as declarative YAML with whitelisted operators; no `eval` | APPROVED | D-038 | architecture §7 | rule_registry, rule_engine | Interpreter unit tests; unknown operator rejected |
| REQ-ARC-019 | Single-turn interaction; follow-ups are outputs; no stored user text | APPROVED | D-037 | architecture §3.2 | pipeline, report_ui | No session state in code |
| REQ-VER-008 | Verifier: deterministic checks first, then one batched LLM judge (model decided at selection) | APPROVED | D-034 | architecture §3.1 | verifier | Unit tests (deterministic layer); verifier claim-set results |

### Verifier (VER)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-VER-001 | Three outcomes: supported / contradicted / insufficient evidence | APPROVED | [APP p.17, 27] | 04 §5 | verifier | Enum in schema |
| REQ-VER-002 | Display handling per outcome (D-011) | APPROVED | D-011 | 04 §5 | verifier, report_ui | UI tests per outcome |
| REQ-VER-003 | No silent rewrite; no unlimited loops | APPROVED | [APP p.22, 27] | 04 §5 | verifier | Code review; bounded calls |
| REQ-VER-004 | Single controlled regeneration optional; requires approval | PROPOSED | D-011 | 04 §5 | verifier | Decision entry if adopted |
| REQ-VER-005 | Distinguish contradicted vs not established | APPROVED | [APP p.28] | 04 §5 | verifier | Separate labels and metrics |
| REQ-VER-006 | Justify second LLM verification call against incremental detection, cost, latency | APPROVED | [APP p.21, 26] | 04 §5 | verifier, eval_harness | C vs D cost/latency table |
| REQ-VER-007 | To claim reduced exposed errors, verifier must withhold/correct/flag; else measure detection separately | APPROVED | [APP p.26] | 04 §5 | verifier | D-011 behaviour + verifier eval |

### Evaluation (EVL)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-EVL-001 | Choose & justify evaluation method; rationale in README; soundness over magnitude | MANDATORY | [ASM p.2][APP p.29] | 05 intro | README | README evaluation rationale |
| REQ-EVL-002 | Honest about limitations | MANDATORY | [ASM p.3] | 05 | README | Limitations section |
| REQ-EVL-010 | Four configurations A–D | APPROVED | D-003 [APP p.25] | 05 §1 | eval_harness | Results table A–D |
| REQ-EVL-011 | Same model, equivalent instructions, same cases, same labels and policy version | APPROVED | [APP p.3, 25]; D-003 | 05 §1 | eval_harness | Run metadata identical except config |
| REQ-EVL-012 | C vs D reuse identical pre-verification outputs | APPROVED | D-003 | 05 §1 | eval_harness | D computed from saved C outputs |
| REQ-EVL-013 | If constrained: A, C, D; document omission of B | APPROVED | [APP p.26]; D-003 | 05 §1 | README | Statement if B omitted |
| REQ-EVL-014 | 48 fictional cases, 6 categories × 8 (total) | APPROVED | [APP p.15–16]; D-019 | 05 §3.1 | benchmark_dataset | Dataset counts |
| REQ-EVL-015 | Dev/held-out split preserving categories; exact split proposed before creation | APPROVED (split PROPOSED 18/30) | [APP p.16]; D-019 | 05 §3.3 | benchmark_dataset | Approved split recorded; split file |
| REQ-EVL-016 | Label protocol: rule inventory → templates → fictional profiles → manual outcomes → independent review → freeze | APPROVED | [APP p.16] | 05 §3.2 | benchmark_dataset | Label provenance notes |
| REQ-EVL-017 | Policy-derived scenarios; no LLM-invented eligibility labels | APPROVED | [APP p.16] | 05 §3.2 | benchmark_dataset | Each label cites fact IDs |
| REQ-EVL-018 | Second reviewer sample or disclosed author-validated source audit | APPROVED | [APP p.16] | 05 §3.2 | README | Disclosure statement |
| REQ-EVL-019 | Freeze held-out; edits only for documented annotation errors | APPROVED | [APP p.16] | 05 §3.2 | benchmark_dataset | Hash of frozen set; change log |
| REQ-EVL-020 | Reference label fields (rule IDs, missing fields, expected behaviour, prohibited conclusions, sources, answerable flag) | APPROVED | [APP p.24] | 05 §4.4 | benchmark_dataset | Schema-validated labels |
| REQ-EVL-021 | Scoring rules (recall vs reference sets, claim-level unsupported rate, substantive citation support, rubric, abstention only where required) | APPROVED | [APP p.24] | 05 §4.4 | eval_harness | Scoring code mirrors rules |
| REQ-EVL-022 | Safeguards (separate before optimisation; near-duplicates same side; verifier not sole truth; ambiguous labels reviewed; raw counts; disclose post-hoc changes) | APPROVED | [APP p.24–25]; BD-08 | 05 §4.5 | eval_harness, README | Checklist in results doc |
| REQ-EVL-023 | Critical/major/minor rubric; critical primary, major separate | APPROVED | [APP p.25]; D-004 | 05 §4.3 | eval_harness | Rubric in annotation guide |
| REQ-EVL-024 | Primary metrics: critical-error rate, required-rule recall, missing-info recall, unsupported-claim rate, appropriate abstention | APPROVED | D-004 | 05 §4.1 | eval_harness | Results table |
| REQ-EVL-025 | Supporting: citation precision, factual correctness, answer coverage, latency, cost | APPROVED (answer coverage definition OPEN) | D-004 | 05 §4.2 | eval_harness | Results table |
| REQ-EVL-026 | Operational definitions with denominators frozen before evaluation | APPROVED | D-004 | 05 §4 | eval_harness | Frozen metric spec committed before held-out run |
| REQ-EVL-027 | Retrieval recall@k on labelled queries | APPROVED (k, query set PROPOSED) | [APP p.20]; D-004 | 05 §5 | retrieval_qrels, eval_harness | Recall@k table |
| REQ-EVL-028 | Independent verifier evaluation (precision/recall per class, false-alarm, false-approval, latency/cost) | APPROVED (set size PROPOSED 60) | [APP p.27]; D-004, D-020 | 05 §6 | verifier_claim_set, eval_harness | Verifier metrics table |
| REQ-EVL-029 | Runtime verifier never ground truth; offline labels independent | APPROVED | [APP p.25, 27] | 05 §2 | eval_harness | Label provenance |
| REQ-EVL-030 | Raw counts + percentages; paired comparisons; bootstrap / exact McNemar as options | APPROVED (tests PROPOSED) | [APP p.27]; D-001 | 05 §7 | eval_harness | Stats in results |
| REQ-EVL-031 | README: controlled benchmark, not population-level evidence | APPROVED | [APP p.27] | 05 §7 | README | Statement present |
| REQ-EVL-032 | Expand demo archetypes into many cases; include conflicting & out-of-scope | APPROVED | [APP p.27] | 05 §3.1 | benchmark_dataset | Category counts |
| REQ-EVL-033 | Category-B failure taxonomy for root-cause analysis | APPROVED | [APP p.19–20] | 05 §8 | eval_harness | Error analysis by type |
| REQ-EVL-034 | Benchmark tests verified policy exceptions (HFE validity, income within D-013, household, non-selection) | APPROVED (facts unverified) | [APP p.21–22]; D-013 | 05 §9 | benchmark_dataset | Exception cases cite verified fact IDs |
| REQ-EVL-035 | Report performance by category; balance categories | APPROVED | [APP p.16] | 05 §3.2 | eval_harness | Per-category table |
| REQ-EVL-036 | All configurations emit the same structured `FinalGuidance`; A/B fill the four signals themselves; README states A is a structured-output baseline | APPROVED | D-035 | architecture §3.2 | pipeline, eval_harness, README | Same schema validated for A–D; README statement |
| REQ-EVL-037 | Optional extraction diagnostic against gold profiles, time permitting | APPROVED (optional) | D-040 | architecture §10 | eval_harness | Field-level P/R table, if done |

### Model selection (MOD)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-MOD-001 | Justify model on operational grounds (privacy, latency, task fit, fine-tuning, cost at scale), not free/cool/available | MANDATORY | [ASM p.4][APP p.30] | 04 §6.3 | README | Model justification section |
| REQ-MOD-010 | Provider comparison labelled preliminary | APPROVED | [APP p.22] | 04 §6.2 | README | Wording |
| REQ-MOD-011 | Scorecard weights 35/25/20/10/10 | PROPOSED | [APP p.22–23] | 04 §6.3 | eval_harness | Approval; scorecard results |
| REQ-MOD-012 | Model selected by evidence later, not in Phase 0 | APPROVED | D-001 | 04 §6 | — | Decision entry at selection |

### Documentation (DOC)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-DOC-001 | Primary artifact: objectives, rationale, implementation, results, execution, limitations | MANDATORY | [ASM p.2][APP p.29] | 06 §2 | README | Section checklist |
| REQ-DOC-002 | 150–250-word section: user & environment, cost/compute at scale, monitoring metrics, one deployment risk (not implemented) | MANDATORY | [ASM p.2][APP p.30] | 06 §2 | README | Word count in range |
| REQ-DOC-003 | Development narrative (iterations, discarded strategies, tools, decisions) | MANDATORY | [ASM p.2][APP p.30] | 06 §2 | README | Section present; consistent with decisions.md |
| REQ-DOC-004 | Write-up matches code; no overclaiming | MANDATORY | [ASM p.3, 4] | 06 §5 | README | Pre-submission README↔code audit |
| REQ-DOC-005 | State technical limitations and enhancements if constraints removed | MANDATORY | [ASM p.4] | 06 §6 | README | Section present |
| REQ-DOC-010 | README formatted with HTML; diagrams where useful | APPROVED | [APP p.30] | 06 §8 | README | Renders on GitHub |
| REQ-DOC-011 | Core story in README (11 listed items) | APPROVED | [APP p.30] | 06 §8 | README | Checklist |
| REQ-DOC-012 | Separate files only for supporting detail | APPROVED | [APP p.30] | 06 §8 | README | Review |
| REQ-DOC-013 | `ai_logs/` layout with README and redactions.md | APPROVED | [APP p.30–31] | 06 §7 | ai_logs | Directory present |
| REQ-DOC-014 | AI-usage disclosure (Claude Code; ChatGPT optional) | APPROVED (wording PROPOSED) | [APP p.31]; D-009 | 06 §7 | README | Section at README end |
| REQ-DOC-015 | Optional `docs/project_selection.md` | PROPOSED (optional) | [APP p.31] | 06 §8 | — | — |
| REQ-DOC-016 | Short rationale comments in code | APPROVED | [APP p.31] | 06 §8 | all code | Code review |
| REQ-DOC-017 | Limitations list (snapshot currency, no live retrieval/maintenance, synthetic profiles, free-tier PII terms, not official assessment) | APPROVED | [APP p.15, 28] | 03 §9 | README | Section present |
| REQ-DOC-019 | Demo tools: Loom / screen recording / Supabase | APPROVED | [APP p.30]; D-018 | 06 §8 | — | — |
| REQ-DOC-020 | README data-section draft (revise "four pages") | PROPOSED | [APP p.14–15]; D-007 | 03 §8 | README | Revised text |
| REQ-DOC-021 | Maintain `docs/decisions.md` | APPROVED | D-012 | decisions.md | — | File exists (done) |

### Submission (SUB)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-SUB-001 | Full deployment/execution instructions | MANDATORY | [ASM p.2][APP p.29] | 06 §2 | README | Clean-machine run log |
| REQ-SUB-002 | Dockerised solution | MANDATORY | [ASM p.1] | 06 §1 | docker | `docker build` + run on clean machine |
| REQ-SUB-003 | 3–5 min demo video; URL in README | MANDATORY | [ASM p.2][APP p.30] | 06 §2 | README | Link present; duration check |
| REQ-SUB-004 | Private GitHub repo; collaborator invited (handle private) | MANDATORY | [ASM p.2] | 06 §3 | repo_hygiene | Private notes checklist |
| REQ-SUB-005 | Repo anonymous re organisation and role | MANDATORY | [ASM p.2]; D-017 | 06 §3 | repo_hygiene | Grep audit of tracked files and logs |
| REQ-SUB-006 | Repo unchanged during evaluation | MANDATORY | [ASM p.2] | 06 §3 | repo_hygiene | No pushes after submission |
| REQ-SUB-007 | Submit via designated channel (private) | MANDATORY | [ASM p.2] | 06 §3 | — | — |
| REQ-SUB-008 | Deadline 5 days from receipt; 12–16 h estimate | MANDATORY | [ASM p.2] | 06 §3 | — | Receipt date recorded privately (Q-18) |
| REQ-SUB-009 | Coding-agent usage section at end of README | MANDATORY | [ASM p.4][APP p.30] | 06 §6 | README | Section position |
| REQ-SUB-010 | Upload all coding-agent session & chat logs; location in README | MANDATORY | [ASM p.4]; D-009 | 06 §7 | ai_logs | Log inventory vs local session list |
| REQ-SUB-020 | Pre-submission log audit; minimal documented redaction; escalate if conflict | APPROVED | D-010 | 06 §7 | ai_logs | `ai_logs/redactions.md` |
| REQ-SUB-021 | Private submission details only in `references/private/` | APPROVED | [APP p.31]; D-017 | 06 §3 | repo_hygiene | File exists, Git-ignored (done) |

### Non-functional (NFR)
| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |
|---|---|---|---|---|---|---|
| REQ-NFR-001 | Runs from README on a clean machine (clean-machine Docker test) | MANDATORY | [ASM p.3, 4][APP p.13] | 06 §5 | docker | Documented clean-machine test |
| REQ-NFR-002 | Professional code quality & maintainability | MANDATORY | [ASM p.3, 4][APP p.31] | 06 §5 | all code | Lint/type/test CI or local checks |
| REQ-NFR-003 | Developer can articulate technical rationale | MANDATORY | [ASM p.4][APP p.31] | 06 §5 | all code, decisions.md | Rationale comments; decisions log |
| REQ-NFR-004 | Works within free-tier limits; paid production needs noted | MANDATORY | [ASM p.4][APP p.31] | 06 §6 | generator, README | Rate-limit handling; README note |

### Superseded items (kept for traceability)
| Item | Source | Replaced by |
|---|---|---|
| Name "BTOPath" | [APP p.3, 21, 24, 25] | D-002 |
| 3-configuration comparison | [APP p.3] | D-003 / REQ-EVL-010 |
| Metric hierarchy of [APP p.24]/[APP p.26] | [APP p.24, 26] | D-004 / REQ-EVL-024..025 |
| KB = curated HTML/text passages | [APP p.21] | D-005 / REQ-DAT-010 |
| `source_passage_id` rule reference | [APP p.15] | D-006 / REQ-DAT-015 |
| "four official HDB webpages" | [APP p.14] | D-007 / REQ-SRC-014 |
| Supported-question list | [APP p.5] | D-008 / 01 §6.4 |
| "Essential" logs | [APP p.30] | D-009 / REQ-SUB-010 |
| Instruction hierarchy | [APP p.1] | D-001 |
| "PolicyProof-inspired" | [APP p.21] | D-015 (HISTORICAL) |

## 2. Contradictions

| ID | Conflict | Pages | Status |
|---|---|---|---|
| C-01 | BTOPath vs BTO Buddy | APP p.3, 21, 24, 25 vs p.1, 17 | Resolved D-002 |
| C-02 | 3 vs 4 configurations | APP p.3 vs p.25–26 | Resolved D-003 |
| C-03 | Differing primary metric sets | APP p.24 vs p.26, p.25 | Resolved D-004 |
| C-04 | KB = HTML passages vs authored facts | APP p.21 vs p.4, 13–14 | Resolved D-005 |
| C-05 | Rules cite private passage IDs | APP p.4–5, 15 | Resolved D-006 |
| C-06 | "Four pages" vs wider matrix/Limited scope | APP p.4, 14 vs p.6–11, 18 | Resolved D-007 |
| C-07 | Supported-question lists differ | APP p.5 vs p.17–18, 28 | Resolved D-008 |
| C-08 | All vs essential logs; ChatGPT disclosure | ASM p.4 vs APP p.30–31 | Resolved D-009 |
| C-09 | Complete logs vs anonymity | ASM p.2 vs p.4 | Policy set D-010; **execution risk remains** (Q-19) |
| C-10 | Verifier failure handling variants | APP p.22 vs p.27 | Resolved D-011 |
| C-11 | No dates to establish recency | APP p.1 | Resolved D-012 |
| C-12 | Income exceptions vs no calculations | APP p.22 vs p.17–18 | Resolved D-013 |
| C-13 | Annex A "around 21" vs 15 sketches | ASM p.4–5 | Recorded D-014 (no impact) |
| **C-14** | **Matrix row "High-level overview of BTO application process" names the "Application for a New Flat" page but gives the HFE page URL (`…/application-for-an-hdb-flat-eligibility-hfe-letter#how-to-apply`), not SEED-4** | APP p.10–11 vs p.4 | **OPEN — new** |
| **C-15** | **"Human-review burden created by verification flags" is a secondary metric in APP p.24 but absent from D-004** | APP p.24 vs D-004 | **OPEN — new** (Q-16) |
| **C-16** | **D-004 introduces "answer coverage" without a definition in either source** | D-004 | **OPEN — new** (Q-15) |
| **C-17** | **Model scorecard omits data privacy, though the brief lists privacy as a primary valid justification ground** | APP p.22–23 vs ASM p.4 | **OPEN — new** (Q-13) |

## 3. Open questions

| ID | Question | Raised from | Needed by |
|---|---|---|---|
| ~~Q-05~~ | ~~Non-couple household types~~ → **resolved D-033**: out of scope, redirected | 01 §6.4, 02 Row 1 | Done |
| Q-06 | SC + SPR household premium / Citizen Top-Up: Excluded (financing) or Limited (first-timer consideration)? *Proposed: D-046* | 02 Row 1 | Phase 2 |
| Q-07 | Resale levy: Excluded (post-purchase) or Limited? *Proposed: D-046* | 02 Row 1 | Phase 2 |
| ~~Q-08~~ | Which of the HFE FAQ page's 5 sub-links, and which "Exceptions and waivers" source, are needed? → **resolved:** waivers are in S04 (D-048); the FAQs are excluded because robots.txt disallows them (D-060) | 02 Rows 2, 5 | Phase 2 |
| Q-09 | Strip `si=` tracking parameters from video URLs? (minor) *Proposed: D-049* | 02 Row 2 | Phase 2 |
| ~~Q-10~~ | ~~Evaluation and run paths~~ → **resolved D-039** | 03 §1 | Done |
| Q-11 | Is any experiment planned on the private corpus (affects REQ-DAT-013)? *Proposed: D-050* | 03 §2.2 | Phase 2 |
| ~~Q-12~~ | ~~Coverage gate placement~~ → **resolved D-033** (after extraction, before rules/retrieval) | 04 §2 | Done |
| Q-13 | Add a data-privacy criterion to the model scorecard? (C-17) | 04 §6.3 | Model selection |
| Q-14 | Claim segmentation / "checkable claim" annotation guide | 05 §4.1 | Before eval |
| Q-15 | Definition of "answer coverage" (C-16) | 05 §4.2 | Before eval |
| Q-16 | Keep "human-review burden" as a supporting metric? (C-15) | 05 §4.2 | Before eval |
| Q-17 | Who/what scores claim-level judgements: manual, validated LLM-as-judge, or hybrid? | 05 §4.4 | Before eval |
| ~~Q-18~~ | ~~Brief receipt date~~ → developer-set completion target 2026-10-29 07:00 (private notes, development log) | 06 §3 | Done |
| Q-19 | Log redaction of organisation name: does redacting it in this Phase 0 session satisfy D-010, or escalate? | 06 §7 | Pre-submission |
| Q-20 | Approve proposed benchmark split 18/30 (stratified, group-aware; K-fold not recommended) | 05 §3.3 | Before dataset creation |
| Q-21 | Approve proposed verifier claim set 60 (15 dev / 45 eval, balanced) or fallback 36 | 05 §6.1 | Before claim creation |
| Q-22 | Finalise `policy_facts` schema field details (shape + `aliases` approved: D-031, architecture §5). *Proposed: D-059 / `bto_buddy.schemas.PolicyFact`* | 03 §2.5 | Phase 2 |
| ~~Q-23~~ | ~~Stack~~ → **resolved D-036** | 04 §6.1 | Done |
| Q-24 | Fix C-14: which URL is intended for the BTO-process row? *Proposed: D-045* | 02 Row 4 | Phase 2 |
| ~~Q-25~~ | REQ-SRC-009 names PyMuPDF, but D-036/D-042 exclude it: which PDF method? → **resolved: D-052 approved, option (a)** (manual page review, no parser dependency) | data_sources §7 | Before any PDF extraction |
| ~~Q-26~~ | May the coding agent read processed source text? → **resolved: D-054 approved as revised** (yes, in-scope sections, training off, no source text in tracked files) | Phase 2a plan §9.4 | Before fact authoring |

## 4. Source-to-Markdown completeness audit (Phase 0, 2026-10-28)

Method: every physical page of both PDFs was read. Text was extracted with pdfplumber. Every
embedded image (11 in APP, none in ASM) was cropped at 300 dpi and read visually. Non-default
text colours were checked to locate verbatim HDB quotations (APP p.7) and highlights
(APP p.3).

### 4.1 Assessment brief (6 pages, no embedded images)
| Page | Content | Captured in |
|---|---|---|
| 1 | Overview, rationale, 4 themes, acceptable methods, Annex A pointer | 06 §1; REQ-PRB-001/002, REQ-SUB-002 |
| 2 | 8 submission requirements; timeline; submission protocol | 06 §2–3; REQ-SUB-001..008, REQ-EVL-001, REQ-DAT-001/002, REQ-LIC-001, REQ-PRIV-001, REQ-DOC-001..003; private notes |
| 3 | Scoring table (5 dimensions, weights) | 06 §4; REQ-NFR-001/002, REQ-DOC-004, REQ-EVL-002, REQ-DAT-003 |
| 4 | 6 non-compliance indicators; 5 methods/resources bullets; supplemental guidance | 06 §5–6; REQ-NFR-001..004, REQ-MOD-001, REQ-PRB-003, REQ-DOC-005, REQ-SUB-009/010 |
| 5 | Annex A sketches 1–9 | 01 §10 (adjacency only; sketches intentionally not reproduced) |
| 6 | Annex A sketches 10–15; Annex B link | 01 §10; link in private notes only; C-13 |

### 4.2 Project approach (31 pages, 11 images)
| Page | Content (incl. images) | Captured in |
|---|---|---|
| 1 | Document status, hierarchy, final idea, chatbot example intro | decisions D-001/BD-00/BD-01; 01 §2 |
| 2 | **Image:** chatbot screenshot; site-structure critique; differentiation; downstream benefit | 01 §2.1–2.2 (vendor branding omitted) |
| 3 | Problem statement, research question (highlighted), narrative, validation, own-research list (highlighted); **image:** 3-config table | 01 §3–5; 05 §1 (superseded design) |
| 4 | Dataset A bullets; seed-source table; manifest note; passage-context rule | 02 §1; 03 §2.1–2.4 |
| 5 | Passage schema; source-discovery intro; supported questions; frozen corpus; discovery path; matrix start | 03 §2.4; 02 §2–3; 01 §6.4 |
| 6–7 | Matrix row 1 cont.: priority schemes, user groups, **verbatim HDB quotes** (SC/SPR, fiancé <21, application validity, unwed parent), MOP, resale levy, subsidies | 02 Row 1 (paraphrased; COPIED-SOURCE flagged) |
| 8 | Income-ceiling PDF; matrix row 2 HFE (what-is infographic text, IPA, when/how to apply, guide, videos) | 02 Rows 1–2 |
| 9 | **Images:** HFE application infographic; flat-buying-journey infographic | 02 Row 2 VR-1, VR-2 (structure summarised, not transcribed) |
| 10 | HFE FAQs, validity/next-steps sections, integrated loan, Singpass portal; matrix row 3 income | 02 Rows 2–3 |
| 11 | Matrix row 4 BTO process (URL anomaly), row 5 non-selection; content-extraction & media rules start | 02 Rows 4–5, §4; 03 §2.6; C-14 |
| 12 | PDF/infographic/video handling; completeness validation; checks table start | 02 §4; 03 §2.7 |
| 13 | Checks table end; coverage matrix; reviewer reproducibility; no-HTML rule; HDB links | 03 §2.2, 2.7, 5, 7; REQ-ARC-009 |
| 14 | README data-section draft (sources, acquisition, provenance, licensing, handling, reproducibility) | 03 §5, 7, 8 |
| 15 | Reproducibility cont.; limitations; Dataset B rule example; Dataset C table start | 03 §3, 7, 9; 05 §3.1 |
| 16 | Dataset C table end; label protocol; **image:** steps 3–6 + dev/held-out note | 05 §3 |
| 17 | Capabilities; constraints; **image:** pipeline diagram; MVP scope intro | 04 §1–2; 01 §6 |
| 18 | MVP table; HFE boundary; missing-info intro | 01 §6, 6.2, 7 |
| 19–20 | Missing info A/B; failure-type table; missing-info contract; demo intro | 01 §7; 05 §8; 04 §3 |
| 21 | **Images:** demo scenarios A–C; tech-stack table + BM25/verifier notes; coverage gate; exceptions start | 01 §8; 04 §2, 6.1; 02 §5 |
| 22 | Exceptions cont.; architecture implication; no-silent-rewrite; provider table; scorecard start | 02 §5; 04 §4–6 |
| 23 | Scorecard weights | 04 §6.3 |
| 24 | **Image:** primary/secondary metrics + ablation note; label & scoring protocol; safeguards start | 05 §1, 4 |
| 25 | Safeguards end; severity rubric; **images:** A–D table, controlled-variables table | 05 §1, 4.3, 4.5 |
| 26 | Prioritise A/C/D; verification ablation notes; resources; metric table; priority note | 05 §1, 4; 04 §6.2 |
| 27 | Verifier evaluation; stats; expansion of archetypes; evaluation risk; **image:** runtime vs offline table | 05 §2, 6, 7, 10 |
| 28 | Temporal validity; scope discipline; hard vs soft; typed outputs; contradicted vs not established; impressive signals; limitations | 01 §9; 03 §2.8, 9; 04 §4–5; 05 §10 |
| 29 | Project requirements checklist (stakeholder, themes, resources, README items) | 01 §1; 06 §2, 8 |
| 30 | Problem-validation via hackathon projects; model-justification; considerations; narrative; demo; AI usage; README preferences; repo contents | 01 §5; 06 §7–8 |
| 31 | ai_logs tree; draft disclosure; optional project_selection; rules; private-notes instruction | 06 §7–8; private notes |

### 4.3 Deliberate omissions (not gaps)
- The verbatim HDB quotations (APP p.7, p.8 "What is HFE" infographic text) and the full
  infographic transcriptions (APP p.9) are replaced by paraphrased, unverified facts
  (D-016, REQ-LIC-017).
- Annex A sketch texts (ASM p.5–6) are not reproduced; only the adjacent sketches are named.
- Organisation, role, collaborator handle, hackathon gallery link and chatbot vendor are
  moved to `references/private/submission_private_notes.md` (D-017).
- The chatbot screenshot itself is not reproduced; it is described in text.

### 4.4 Content in the sources with no actionable requirement
- APP p.29's ticked checklist duplicates ASM requirements. It is mapped to existing IDs and
  adds the stakeholder choice (citizen group) and theme choice (retrieval & knowledge).
