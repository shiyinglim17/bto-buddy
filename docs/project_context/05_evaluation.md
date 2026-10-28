# 05 — Evaluation

The legend is in [INDEX.md](INDEX.md#legend).

**MANDATORY context [ASM p.2–3]:**
- Select and justify a specific evaluation methodology, with the rationale in the README.
- **Soundness outranks the size of the results.**
- Evaluation and effectiveness carry the largest scoring weight (30%).
- Novelty counts only together with effectiveness.
- Be honest about limitations (REQ-EVL-001, REQ-EVL-002).

**Chosen methodology (APPROVED):** a **controlled benchmark with an ablation-style
comparison** of system configurations. The runtime verifier and the retriever are also
evaluated as separate components.

## 1. System configurations — REQ-EVL-010 (APPROVED, D-003) [APP p.25–26]

| System | What it includes | Question answered |
|---|---|---|
| A — Direct LLM | Applicant profile + question → model response. No retrieval, no deterministic rules | How well does a simple assistant perform? |
| B — RAG | Retrieved policy evidence → model response (same model) | Does grounding improve reliability? |
| C — Hybrid | Structured profiling + deterministic rules + RAG | Do structured checks improve guidance? |
| D — Hybrid + verifier | Full BTO Buddy pipeline | Does verification reduce exposed errors? |

### Controlled variables [APP p.25, image 2]

| Dimension | A | B | C | D |
|---|---|---|---|---|
| Same generation model | Yes | Yes | Yes | Yes |
| Same applicant input | Yes | Yes | Yes | Yes |
| Same supported policy scope | Yes | Yes | Yes | Yes |
| Pretrained knowledge | Yes | Yes | Yes | Yes |
| Retrieved policy facts | No | Yes | Yes | Yes |
| Structured profile extraction | No separate module | No separate module | Yes | Yes |
| Deterministic policy rules | No | No | Yes | Yes |
| Claim verification | No | No | No | Yes |

- **REQ-EVL-011:** use the same generation model, equivalent task instructions and the same
  benchmark cases. All configurations are scored against **the same authoritative reference
  labels and the same policy version**.
- **REQ-EVL-012 (D-003):** C vs D **reuses identical pre-verification outputs**, so the
  difference isolates the verifier.
- **REQ-EVL-013:** if time is short, run **A, C and D** and document why B was omitted. That
  still gives a baseline, the core intervention and the verification ablation.
- **Purpose:** show *why* the added engineering complexity is justified, rather than assuming
  a more elaborate architecture is better [APP p.3].
- **Verification ablation [APP p.24, 26]:** enabled vs disabled on identical cases. This
  tests measurable value and also exposes false alarms, latency and cost.
- **SUPERSEDED [APP p.3]:** the three-configuration design (A baseline, B RAG,
  C "BTOPath" = profile + retrieval + verification). Its evaluated aspects were factual
  correctness, required-rule coverage, unsupported-claim rate, missing-information
  detection, abstention and latency. All of these are carried into §4.

## 2. Two separate evaluation activities (APPROVED) [APP p.27, image]

| Evaluation type | Purpose |
|---|---|
| Runtime verification | Checks generated claims against retrieved evidence before they are shown |
| Independent offline evaluation | Measures whether the application **and its verifier** are actually correct |

**REQ-EVL-029:** the offline benchmark has independently reviewed labels. **The runtime
verifier's judgements are never ground truth** [APP p.25, 27].

## 3. Benchmark (Dataset C) — REQ-EVL-014 (APPROVED, D-019) [APP p.15–16]

### 3.1 Structure: 48 fictional cases in total, 6 categories × 8

| Category | Cases | What it tests |
|---|---|---|
| Standard preparation | 8 | Correct applicable requirements |
| Missing information | 8 | Appropriate follow-up questions |
| Policy exceptions | 8 | Handling nuanced conditions |
| Misconceptions | 8 | Correcting inaccurate assumptions |
| Conflicting information | 8 | Detecting contradictory profile details |
| Out-of-scope | 8 | Abstaining appropriately |

- **REQ-EVL-032 [APP p.27]:** expand the three demo archetypes into many independently
  labelled cases covering different profiles, rules and edge conditions.
- Include conflicting-information and out-of-scope cases even if the video doesn't show them.

### 3.2 Label-creation protocol — REQ-EVL-016..019 (APPROVED) [APP p.16]
1. **Extract policy requirements first.** Build a rule inventory with source references.
2. **Design scenario templates.** Vary one or two meaningful factors at a time, including
   boundary conditions.
   - Use **policy-derived scenarios**. Never ask an LLM to invent eligibility labels.
   - Independently check the expected guidance against official rules (REQ-EVL-017).
3. **Write fictional profiles** with synthetic names. Never use real records.
4. **Assign expected outcomes manually.** Record:
   - applicable rules;
   - required follow-up information;
   - prohibited conclusions;
   - supporting passages (now fact IDs, D-006).
5. **Review labels independently of the model** (REQ-EVL-018).
   - Ideally a second reviewer checks a sample.
   - If no second reviewer is available, run a separate source-based audit and **disclose
     that the labels were author-validated**.
6. **Freeze the held-out set** (REQ-EVL-019). Its labels never change after final
   predictions are inspected, except to correct documented annotation errors.

**From the same page [APP p.16, image]:**
- Use development cases for prompt and architecture refinement.
- Keep a separate held-out set for the final comparisons.
- Balance cases across categories where possible.
- **Report performance by category** (REQ-EVL-035).

### 3.3 Dev/held-out split — PROPOSED (needs approval before dataset creation, D-019)

**Recommendation: a fixed, stratified, group-aware split. 18 development / 30 held-out.**

| Category | Dev | Held-out |
|---|---|---|
| Each of the 6 categories | 3 | 5 |
| **Total** | **18** | **30** |

- **Group-aware:** cases from the same scenario template or near-duplicate family all go to
  the *same* side, as REQ-EVL-022 requires. If grouping makes 3/5 impossible in a category,
  the split moves by at most one case and the change is documented.
- **Why not K-fold:**
  1. K-fold suits estimating a *trained* model's variance. No model is trained here. The
     "fitting" is manual prompt and architecture iteration, which can't be repeated
     independently per fold without leaking every case into development.
  2. The approved safeguards require dev and held-out cases to be **separated before prompt
     optimisation**, and the held-out set to be **frozen and untouched**. K-fold conflicts
     with both.
  3. Each run costs live API calls under free-tier limits.
- **Uncertainty with 30 held-out cases:** handle it with paired per-case comparisons and
  bootstrap intervals (§7), not with folds.
- **Trade-off:** 30 held-out cases give wide intervals. That is acceptable for a controlled
  benchmark if it's reported honestly (REQ-EVL-031).
- **Alternative (not recommended):** 24/24. This gives more test power but leaves only 4 dev
  cases per category, which is too few to iterate on prompts per category.

## 4. Metrics — REQ-EVL-024..026 (APPROVED hierarchy, D-004)

All definitions must be **operational, with denominators, and frozen before evaluation**
(REQ-EVL-026). The definitions below come from [APP p.24, 26]. Where the source is silent,
the operationalisation is marked PROPOSED.

### 4.1 Primary metrics

| # | Metric | Definition | Denominator / unit | Source |
|---|---|---|---|---|
| 1 | **Critical-error rate** | Cases with ≥1 *critical* error (severity rubric §4.3) ÷ evaluated cases. Major errors reported separately | Cases | [APP p.25–26] |
| 2 | **Required-rule recall** | Correct required rules identified ÷ all applicable reference rules | Rule instances, pooled over cases (PROPOSED: also report per-case macro mean) | [APP p.24, 26] |
| 3 | **Missing-information recall** | Correctly identified essential missing fields ÷ all reference missing fields | Field instances, pooled (PROPOSED: macro too) | [APP p.24, 26] |
| 4 | **Unsupported-claim rate** | Unsupported factual claims ÷ all *checkable* factual claims, measured at claim level | Claims. **PROPOSED:** claim segmentation and the "checkable" criterion need a written annotation guide (Q-14) | [APP p.24, 26] |
| 5 | **Appropriate abstention** | Correct abstentions ÷ cases whose reference label requires abstention or official confirmation. Scored **only** on such cases | Cases requiring abstention. **PROPOSED:** also report the *over-abstention* rate on answerable cases, so abstaining everywhere can't game the metric | [APP p.24, 26] |

**Priority [APP p.26]:** critical-error rate and required-rule recall matter most. A concise
but incomplete answer can be less dangerous than one that confidently tells an ineligible
applicant to proceed.

### 4.2 Supporting metrics

| Metric | Definition | Source |
|---|---|---|
| Citation precision | Correctly supported cited claims ÷ all claims with citations. "Supported" means the cited evidence **substantively** supports the claim | [APP p.24, 26] |
| Factual correctness | Proportion of independently labelled factual claims answered correctly | [APP p.24] ("factual accuracy") |
| Answer coverage | **Not defined in the sources → OPEN (Q-15).** PROPOSED: answerable cases given substantive (non-abstaining) guidance ÷ answerable cases | D-004 |
| Latency | **PROPOSED:** median and p95 end-to-end seconds per configuration | [APP p.3, 24] |
| Inference cost | **PROPOSED:** recorded tokens × published price, per case and per configuration (or $0 plus a compute note for local) | [APP p.24] |
| Human-review burden (verification flags) | Listed as secondary in [APP p.24] but **not in D-004 → OPEN (Q-16)** | [APP p.24] |

### 4.3 Critical-error severity rubric — REQ-EVL-023 (APPROVED) [APP p.25]

| Severity | Definition | Example |
|---|---|---|
| **Critical** | A materially misleading preparation or eligibility conclusion | Stating eligibility definitively without sufficient evidence |
| **Major** | Missing an important applicable requirement | Omitting an essential HFE prerequisite |
| **Minor** | Non-consequential incompleteness or a presentation issue | Repeating a preparation step |

The primary safety metric counts **critical** errors. **Major** errors are reported separately.

### 4.4 Reference labels and scoring rules (APPROVED, define and freeze before final evaluation) [APP p.24]

**Reference labels — REQ-EVL-020.** Each case records:
- applicable policy rule IDs;
- required missing applicant fields;
- expected response behaviour;
- prohibited or materially misleading conclusions;
- supporting authoritative source references (fact IDs);
- whether the scenario is answerable within the supported corpus.

**Scoring rules — REQ-EVL-021:**
- Required-rule recall is measured against the reference applicable-rule set.
- Missing-information recall is measured against the reference missing fields.
- The unsupported-claim rate is measured at the factual-claim level.
- Citation correctness requires the cited evidence to substantively support the claim.
- Critical errors follow the predefined severity rubric.
- Abstention is scored only where the label requires abstention or official confirmation.

**Scorer — OPEN (Q-17).** Neither source document says whether claim-level judgements
(supported, critical) are made by the author manually, by an LLM-as-judge validated against
manual labels, or both.

### 4.5 Evaluation safeguards — REQ-EVL-022 (APPROVED) [APP p.24–25]
- Separate development and held-out cases **before** prompt optimisation.
- Never split near-duplicate scenarios across dev and test.
- The runtime verifier is never the sole source of ground truth.
- Independently review and document ambiguous labels.
- Report final test results with **raw counts and denominators**.
- Disclose any change made after inspecting held-out results. The affected test set must
  not then be presented as untouched.

## 5. Retrieval evaluation — REQ-EVL-027 (APPROVED, D-004) [APP p.20]
- Measure **recall@k** on labelled queries, where each query has its gold fact IDs. This
  isolates *retrieval failure* (category B).
- The value of k and the labelled-query set are PROPOSED for Phase 2/3. A natural source is
  the benchmark cases' supporting fact IDs.
- The same metric decides whether embeddings are added (REQ-ARC-010).

## 6. Verifier evaluation — REQ-EVL-028 (APPROVED, D-004, D-020) [APP p.27]

**Measures:**
- precision and recall for detecting **contradicted** claims;
- precision and recall for detecting **insufficient-evidence** claims;
- **false-alarm rate** on supported claims;
- **false-approval rate**: how often the verifier wrongly approves a claim;
- added latency and inference cost.
- *Only if relevant:* macro-F1, contradiction recall, false-alarm rate and evidence-retrieval
  accuracy.

**Rationale:** don't assume a verifier is accurate just because it produces classifications.

### 6.1 Claim set — PROPOSED size (needs approval; labels never fabricated, D-020)

| Split | Supported | Contradicted | Insufficient | Total |
|---|---|---|---|---|
| Development | 5 | 5 | 5 | 15 |
| Evaluation | 15 | 15 | 15 | 45 |
| **Total** | 20 | 20 | 20 | **60** |

**Construction** (author-labelled against verified facts; disclosed as author-validated):

| Label | How the claims are built |
|---|---|
| Supported | Faithful paraphrases of verified facts |
| Contradicted | Single-attribute perturbations of verified facts: a changed number, period, applicant group, or a dropped exception. The "dropped exception" case targets the risk in [APP p.27] |
| Insufficient | Plausible claims on topics the KB deliberately doesn't cover, or claims that go beyond what the evidence states |

- Each claim is paired with the evidence passed to the verifier.
- **Balanced classes** keep the per-class precision and recall interpretable.
- **Fallback if time is short:** 36 claims (6 dev / 30 eval, i.e. 2/2/2 and 10/10/10). Report
  that intervals will be wide.

## 7. Statistical reporting (APPROVED principle; tests PROPOSED per D-001) [APP p.27]
- With about 48 cases (30 held-out under §3.3), **don't over-interpret small percentage
  differences**.
- Report raw counts alongside percentages, and use paired comparisons (REQ-EVL-030).
- **Options:**
  - paired bootstrap confidence intervals on system differences;
  - McNemar's test for binary case-level success, with an **exact** method for small samples.
- **REQ-EVL-031:** the README states this is a **controlled benchmark, not evidence of
  population-level effectiveness**.

## 8. Failure-type taxonomy (category B root cause) — REQ-EVL-033 (APPROVED) [APP p.19–20]

| Failure type | Meaning | How to test |
|---|---|---|
| Source coverage gap | Relevant document never included | Manual source coverage matrix |
| Extraction gap | Content exists in the source but wasn't extracted | HTML/visual completeness audit |
| Retrieval failure | Content is in the index but wasn't retrieved | Retrieval recall@k |
| Temporal gap | Corpus doesn't cover the applicable policy period | Effective-date checks |
| Evidence insufficiency | Available material can't establish the answer | Abstention and verifier evaluation |

This separation enables meaningful **root-cause error analysis**.

## 9. Policy exceptions the benchmark should test — REQ-EVL-034 [APP p.21–22]

The candidate exceptions are listed in [02 §5](02_policy_sources.md#5-policy-nuances-flagged-for-structured-reasoning-app-p2122):
- HFE validity and timing;
- income assessment (only within D-013);
- household composition (applicants / occupiers / core family nucleus; fiancé(e) under 21);
- non-selection consequences and waivers.

Each must be **verified against frozen sources** before it is labelled.

Additional candidate (author observation): the VR-1 30-day Step-2 window, as an
extraction-gap test ([02 Row 2](02_policy_sources.md)).

## 10. Evaluation risks and what would strengthen the evaluation [APP p.27–28]
- **Automated verification is not automatically trustworthy:**
  - two LLMs can share a misunderstanding;
  - a verifier can approve a claim from a passage that omits an exception.

  Mitigation: independent labels and a separate verifier evaluation.
- **Strong signals named in the approach:**
  - a well-designed benchmark;
  - an error taxonomy;
  - a baseline comparison;
  - evidence that the system catches subtle policy inaccuracies more reliably than a simpler
    approach;
  - evidence that hybrid rules + RAG **reduces unsupported eligibility recommendations**
    compared with a general-purpose chatbot.
- **Demo honesty:** demo examples must represent real behaviour (REQ-SCP-014).
