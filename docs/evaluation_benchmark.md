# Evaluation Benchmark (Dataset C): Design, Rubric and Protocols

**Phase 3a, 2026-10-29.**

**Status: CANDIDATE.** These labels are not frozen. The developer reviews and approves them
first (§8). Decisions D-063 to D-065 are PROPOSED.

**Requirements:** REQ-EVL-014 to 022, REQ-EVL-028, REQ-EVL-032 to 035, D-019, D-020.

**Files:**

| File | Holds | Git |
|---|---|---|
| `evaluation/benchmark/dev.jsonl` | 18 development cases: input + label | Tracked |
| `evaluation/benchmark/test_inputs.jsonl` | 30 held-out **inputs only** | Tracked |
| `evaluation/heldout/test_labels.jsonl` | 30 held-out labels | **Ignored until final scoring** (D-064) |
| `evaluation/benchmark/manifest.json` | Counts, families, `as_of`, versions, and the **SHA-256 of the held-out labels** | Tracked |
| `evaluation/benchmark/dev_review_sheet.csv`, `evaluation/heldout/test_review_sheet.csv` | Annotation and review templates, with REVIEW columns | Dev sheet tracked; test sheet ignored |
| `evaluation/claims/claim_template.jsonl` | Claim-level protocol template with 4 dev examples | Tracked |
| `evaluation/benchmark.py` | Schema (`CaseInput`, `CaseLabel`), locked loaders, validator | Tracked |

---

## 1. What the benchmark measures

The benchmark is the same for configurations A–D. It feeds the primary metrics (D-004):

- critical-error rate;
- required-rule recall;
- missing-information recall;
- unsupported-claim rate;
- appropriate abstention, plus over-abstention.

It also feeds the supporting metrics. Labels are **policy-derived**. They come only from
**verified** facts (D-058) and **approved** rules (D-062). They are never derived from
outputs of any system under test.

---

## 2. Annotation rubric (defined before the cases were written)

Each case's label (`CaseLabel`) records five dimensions, plus scope metadata.

### 2.1 Applicable policy requirements

| Field | Meaning | Scoring use |
|---|---|---|
| `required_rule_ids` | Rules that apply to the stated profile **and** answer the question. The answer must convey each one's preparation step | Required-rule recall (numerator and denominator) |
| `conditional_rule_ids` | Rules whose applicability depends on a missing or conflicting field. The answer should raise them conditionally ("if…") | Not in recall. Asserting them unconditionally counts towards a prohibited conclusion |
| `optional_rule_ids` | Relevant to the profile but not needed for this question | Never penalised; excluded from recall |
| `key_points` | Short, authored statements of what the answer must convey, including fact-only corrections when no rule fires | Used by the annotator to judge each required item |

**Labelling rules:**
- A rule is `required` only when its conditions are fully stated in the input.
- It must be traceable to `policy_rules.yaml`, and its facts must be `verified`.
- A requirement stated by a verified fact without a matching rule goes in `key_points` and
  `evidence_fact_ids`, and the case records why.

### 2.2 Missing applicant fields

- **`required_missing_fields`:** essential fields that are not stated, without which a
  required or conditional rule cannot be applied. Missing-information recall is computed
  over these.
- **`acceptable_follow_ups`:** questions that are reasonable to ask but not essential. These
  are neither rewarded nor penalised.
- Field names are the registry's field catalogue (`policy_rules.yaml › fields`).
- Fields never asked about are not "missing" (architecture: missing fields are computed only
  for the topics asked).

### 2.3 Expected conversational behaviour (`expected_behaviour`, one or more)

| Behaviour | Expected when | A correct answer… |
|---|---|---|
| `provide_guidance` | Requirements are determinable | gives the preparation steps with sources |
| `ask_follow_up` | `required_missing_fields` is not empty | asks for each field; guidance that depends on it stays conditional |
| `flag_conflict` | `expected_conflicts` is not empty | names the contradiction and asks. If the conflict is `material`, it gives no guidance that relies on either side; if immaterial, it may continue |
| `correct_misconception` | The user asserts something the facts contradict | states the correction with the fact |
| `state_unconfirmed` | The question turns on U-01 to U-04 (D-061) | says the point is not established by the sources, without deciding it either way, and redirects |
| `abstain_and_redirect` | The topic is Excluded or the household is unsupported | declines and gives the official redirect |
| `partial_answer_and_redirect` | The question mixes in-scope and Excluded parts | answers the in-scope part and redirects the rest |

`answerable` is `yes`, `partial` or `no`. Appropriate abstention is scored only on `partial`
or `no` cases that carry `abstain_and_redirect`, `state_unconfirmed` or
`partial_answer_and_redirect`. Over-abstention is scored on `yes` cases.

### 2.4 Prohibited conclusions (`prohibited_conclusions`)

- Each item has an ID, a description, a **severity** and a **basis**.
- **Severity** follows 05 §4.3:
  - *critical* means a materially misleading preparation or eligibility conclusion;
  - *major* means a misleading omission or an unsupported assumption.
- **Basis:** fact IDs, rule IDs, decision IDs, or U/I/G items. Every basis is checked for
  traceability.
- Reused items include `PC-VERDICT`, `PC-NO-HFE`, `PC-VALIDITY`, `PC-GRANT`, `PC-CEILING`,
  `PC-ODDS`, `PC-GUARANTEE`, `PC-DOCLIST`, `PC-UNCONFIRMED`, `PC-CONFLICT` and `PC-ASSUME`.
  Case-specific items are `PC-X1`, `PC-X2`, …

A case has at least one critical error if the answer asserts any critical prohibited
conclusion (critical-error rate).

### 2.5 Evidence support (`evidence_fact_ids`)

- These are the verified facts that establish every required rule and key point. The
  validator rejects unverified or unknown facts.
- Evidence must be **reviewer-accessible**: fact IDs that resolve to official URLs through the
  manifest, never private passages (D-006).
- Citation precision checks that a cited fact *substantively* supports the claim (05 §4.2).
- These IDs are also the gold set for **retrieval recall@k** (05 §5).

### 2.6 Scope metadata
- **`question_topics`:** the closed `Topic` enum.
- **`out_of_scope`:** the code, the topic and the redirect source ID.
- **`expected_conflicts`:** the fields, `stated_contradiction` or `logical_inconsistency`, and
  whether the conflict is `material`.
  - **A conflict label does not presume the user is wrong.** Wording may be informal (e.g.
    "my wife" for a fiancée) or circumstances may have changed (engaged, then married). Neither
    statement is authoritative: the reference profile sets the field to `None`, and the
    expected behaviour is a neutral clarifying question that allows for both readings.
    Settling either side, or telling the user a statement is wrong, is a prohibited
    conclusion (e.g. DEV-13).
- **`unresolved_refs`:** the U/I/G items the case touches. **No definitive reference answer is
  given on these points.** The label specifies only the behaviour (§2.3) and prohibits
  answering them definitively.
- **`reference_profile`:** the expected extraction (`None` means not stated, or conflicting).
  It is used to evaluate the profile-extraction stage.

### 2.7 Severity and scoring alignment

| Rubric element | Metric |
|---|---|
| `required_rule_ids` | Required-rule recall; a missed one is a **major** error |
| `key_points` | Key-point coverage (annotator-judged), reported next to rule recall so that fact-only cases with no rule (e.g. DEV-08) are still scored. Definition to be frozen in `metric_spec.md` |
| `required_missing_fields` | Missing-information recall |
| Critical `prohibited_conclusions` | Critical-error rate |
| `expected_behaviour` with abstention-type behaviours | Appropriate abstention, and over-abstention |
| `evidence_fact_ids` | Citation precision; retrieval recall@k |
| Claim-level annotation (§3) | Unsupported-claim rate; verifier metrics |

---

## 3. Claim-level annotation protocol (verifier evaluation; D-065 PROPOSED)

This protocol is separate from the case labels. The verifier evaluation uses a fixed claim
set, built from verified facts, so it does not depend on any model's outputs (D-020).

**Record** (`evaluation/claims/claim_template.jsonl`):
- `claim_id`;
- `split` (dev or eval);
- `text`: one atomic factual claim;
- `evidence_fact_ids`: exactly what the verifier is given;
- `gold_label`: `supported`, `contradicted` or `insufficient_evidence`;
- `construction`;
- `source_fact_id`;
- `rationale`;
- `review`.

**Construction types:**

| Label | Allowed constructions |
|---|---|
| supported | `faithful_paraphrase` of one verified fact (same numbers, applicant group and conditions) |
| contradicted | Single-attribute perturbation: `changed_number`, `changed_period`, `changed_applicant_group`, or **`dropped_exception`** (targets the risk in 05 §10) |
| insufficient_evidence | `out_of_kb` (an Excluded topic or a G-17/U-item) or `beyond_evidence` (adds a condition the facts don't state) |

**Annotation steps:**
1. Pick a verified fact.
2. Write the claim from the fact, not from a model.
3. Give the verifier the cited facts.
4. Assign the gold label from the construction.
5. Record the rationale.
6. Have the developer review it.

**Atomicity rules:**
- one proposition per claim;
- conjunctions are split;
- hedged or procedural statements ("check with HDB") are **not checkable** and are excluded
  from the unsupported-claim denominator.

**Scoring generated answers:** each answer is split into atomic factual claims. Each claim is
labelled `supported` if a cited verified fact substantively supports it, `contradicted` if a
verified fact states otherwise, and `insufficient` otherwise. The runtime verifier's own
judgement is never the reference (REQ-EVL-029).

**Proposed size:** 60 claims, from 05 §6.1:
- dev: 5/5/5 across supported/contradicted/insufficient;
- eval: 15/15/15.

The eval claims are sealed like the held-out labels (D-064). The template holds 4 dev
examples only.

---

## 4. Sampling strategy

- **Stratified by category:** 6 categories × 8 cases (D-019). Dev/held-out is 3/5 per
  category (05 §3.3).
- **Policy-derived templates:** each case starts from one or two rules or facts. One or two
  meaningful factors vary at a time:
  - relationship (married / engaged);
  - citizenship combination;
  - age at a published boundary (20/21, 33/35, 40/41);
  - HFE stage and date (30-day window, 9-month expiry, already submitted);
  - first-timer status;
  - children;
  - property;
  - employment and jobs;
  - non-selection stage.
- **Boundary pairs:** under 21 vs exactly 21 (DEV-07/08); expiry within 30 days vs already
  expired; non-resident spouse SC aged 38 vs 33.
- **Coverage:** 22 of 24 rules are required or conditional in at least one case. R-HH-003
  (married under 21) and R-HH-004 (two SPR partners) are covered only by unit tests: they are
  rare preparation paths and the 48-case limit was kept.
- **Excluded topics sampled:** grant calculation, income ceilings, ballot odds, an unsupported
  household (single), a mixed in-scope/excluded question, and a demand for an eligibility
  verdict.
- **Unresolved items:** U-01, U-02 and U-03 each have a case labelled `state_unconfirmed`.
- **Fictional names only.** Profiles are synthetic and contain no real records.
- **Fixed evaluation date:** `as_of = 2026-11-01`, so date-dependent guidance is
  reproducible.
- **Snapshot-applicability assumption (A-01).** The policy corpus was captured on
  2026-10-28; the evaluation date is 2026-11-01. The benchmark **assumes the frozen
  snapshot (`kb-2026-10-28.1`, `rules-2026-10-29.1`) still states the applicable policy on
  the evaluation date.** It does not check this: there is no live re-fetch (D-055/D-056),
  and the drift check (§10, G-15) happens only before submission. The assumption matters
  most for date-sensitive policies used in labels:

  | Date-sensitive element | Facts / rules | Cases depend on |
  |---|---|---|
  | Steps 1 and 2 within 30 calendar days; cross-month update | HFE-STEPS-001, R-HFE-001 | Day counts and month boundaries relative to `as_of` |
  | HFE letter valid 9 months from issue; expiry handling | HFE-VALID-001, R-HFE-004/005, I-02 | `hfe_days_to_expiry` computed at `as_of` |
  | HFE processing "up to a month" | HFE-TIME-001, R-HFE-002 | Planning advice only (no fixed date) |
  | Age thresholds (21; 35 for a non-resident spouse; 40 for FT(PMC) married couples) | HH-AGE-001/002, HH-NONRES-002, PRI-FTPMC-001 | Ages taken as stated at `as_of` (I-05) |
  | 30-month private-property disposal; 5-year BTO-chance window | HH-PROP-001, PRI-FTPMC-001 | Window comparisons relative to `as_of` |
  | Marriage registration within 3 months after purchase | HH-MARRY-001, R-HH-001 | Conditional guidance for engaged couples |

  If a drift check finds a change to any of these before the held-out run, the affected
  facts are re-verified, the KB version is bumped and the affected labels are re-reviewed
  and disclosed. Labels are never changed in response to model output. Changes found only
  after the held-out run are reported as a limitation, not retro-fitted.

**Totals:**

| Measure | Count |
|---|---|
| Cases | 48 |
| Families | 34 |
| Prohibited conclusions | 98 (76 critical, 22 major) |
| Essential missing fields | 11 |
| Cases with an unresolved/interpretation reference | 14 |

## 5. Split, leakage control and access to held-out labels (D-063, D-064)

- **Split:** 18 dev / 30 held-out, made **before any prompt or model work**.
- **Group-aware:** each case has a `family_id` for its near-duplicate group. Families are
  assigned to one side only, and `validate` fails if a family spans both.
  - Example: F-UNDER21 (DEV-07, DEV-08 and DEV-12) is entirely dev. Held-out families are
    not described here, so this document leaks nothing about held-out labels.
- **Near-duplicate check:** token-set Jaccard similarity between every pair. There are 0
  cross-split pairs at ≥ 0.6 (the maximum cross-split similarity is 0.49). One within-split
  pair is intended: the DEV-07/08 boundary twins.
- **Held-out access protocol (D-064):**
  1. Held-out **labels** live only in `evaluation/heldout/`, which is Git- and
     Docker-ignored. The tracked manifest commits their SHA-256.
  2. `load_test_labels()` refuses unless `final=True`, `BTO_BUDDY_FINAL_EVAL=1`, the manifest
     `status` is `frozen`, and the hash matches. Developer review uses `review=True`.
  3. Prompt tuning, model selection and pipeline debugging use `dev.jsonl` only. Agents may
     load `test_inputs.jsonl` **only** to check schema compatibility, and **must not read**
     `evaluation/heldout/` (CLAUDE.md).
  4. Labels are never changed after held-out predictions are inspected, except to correct
     documented annotation errors. Any such change is disclosed, and that set is no longer
     reported as untouched (REQ-EVL-019, REQ-EVL-022).
  5. At final scoring the developer commits the labels file. Its hash must equal the
     pre-registered value.
- **Disclosure:** the coding agent authored the held-out labels in this session, before any
  prompt work. It will not read them again before final scoring. The developer should keep a
  backup of `evaluation/heldout/` (it is not in Git until then).

## 6. Label quality assurance

**Automated checks** (`python -m evaluation.benchmark validate`; tests in
`tests/test_benchmark.py`):
- every rule ID exists;
- every fact is `verified`;
- fields are in the catalogue;
- missing or conflicting fields are absent from the reference profile;
- every prohibited-conclusion basis is traceable;
- behaviours are consistent with missing fields, conflicts, excluded topics and unresolved
  items;
- split, family and hash integrity.

**Engine cross-check (annotation QA only).** Labels were authored by hand, then compared with
the deterministic rule engine. Disagreements are reviewed against the **source**, never
adopted automatically:
- one label error was corrected: DEV-05 listed the two-SPR rule as conditional, but
  applicant 1 is stated to be an SC (HH-CIT-001);
- the fee-and-ballot rule was added as **optional** to 3 cases.
- **Report-only warning (added in dev review):** `validate` also lists rules the engine
  returns `cannot_determine` for that the label omits entirely (the cross-check above missed
  this class, which is how DEV-13 lacked a conditional R-HH-001). Warnings never fail the run,
  because most are legitimate omissions. Dev triage (2026-10-29), 13 warnings in 10 cases:
  - **Legitimate omissions (10):**
    - R-HH-006 in 9 cases: `private_property_interest` was never asked about (§2.2);
    - R-APP-003 and R-HFE-004 in DEV-04/13: downstream of `hfe_status`, already a required
      missing field.
  - **Real omissions (3), fixed:**
    - DEV-13: R-APP-002 added as optional, since it applies whether "married" or "engaged";
    - DEV-14: R-HH-007 and R-PRI-002 added as conditional, since both depend on the
      conflicting subsidy field.
- **Caveat:** the rule registry is part of configurations C and D. Agreement between labels
  and the engine is therefore **not** evidence that the labels are correct. That comes only
  from source review (§7). Labels that rest on facts without a rule deliberately expose gaps
  in the registry.

## 7. Labels requiring the developer's manual source verification

- **Dev labels: all 18 approved by the developer (2026-10-29)**, after source checks of the 4 flagged dev cases and review batches 1–2 (development log). **Held-out labels stay `candidate`** until the developer reviews them; the agent cannot open them (D-064).
- **20 cases** (dev 4, held-out 16) have `review.requires_source_check = true`, with reasons.
  The reasons are:
  - date arithmetic or conventions (I-02, I-03, the 30-day and 30-month windows);
  - interpretation rules (R-HFE-003/004, R-HH-007, R-PRI-002);
  - human-review exceptions (non-resident spouse under 35);
  - the G-17 gap wording;
  - unresolved U-items, where only a behaviour is labelled;
  - a rule-registry limitation (the 30-month wait-out after a past sale);
  - the materiality of a conflict;
  - whether "flats available to choose from" matches HDB's waiver count.
- **Dev:** open `evaluation/benchmark/dev_review_sheet.csv`.
- **Held-out:** open `evaluation/heldout/test_review_sheet.csv`. Only you review this one.
- For each case, fill in:
  - `REVIEW_decision` (approve / edit / reject);
  - `REVIEW_source_checked`;
  - `REVIEW_notes`.
- **Second reviewer:** none is available, so a separate source-based audit is done and the
  labels are disclosed as **author-validated** (03 §4, REQ-EVL-018).

## 8. Review and freeze procedure
1. The developer reviews both sheets. Edits are applied to the JSONL files, then
   `validate --heldout` is re-run (developer only).
2. Recompute the held-out SHA-256, and set the manifest `status` to `frozen` with a new
   `benchmark_version`.
3. Record the freeze in decisions.md and the development log. **Prompt work starts only
   after this.**
4. `evaluation/metric_spec.md` (written 2026-10-29, D-066) is frozen at the same time as the
   benchmark, before the held-out run (REQ-EVL-026).

## 9. Limitations of synthetic cases
- **Author-built:** the cases reflect the author's reading of the sources, not real
  applicant language or the real distribution of questions. They are a controlled benchmark
  and say nothing about population-level effectiveness (REQ-EVL-031).
- **Small:** 30 held-out cases give wide intervals. Results are reported with raw counts,
  paired comparisons and bootstrap intervals (05 §7).
- **Narrow profiles:** the profile covers only the registry's field catalogue. Real
  situations (divorce, adoption, joint ownership details) are simplified.
- **Single snapshot:** the policy is the 28 Oct 2026 snapshot, assumed to still apply on the
  1 Nov 2026 evaluation date (A-01, §4). Answers that are correct against the live site
  after drift are not credited (G-15).
- **Author validation:** the agent authored both the labels and the rules; disclosed in §5–§7.
- **Unresolved points:** U-items only test behaviour, not policy correctness.
- **Cases are short and English-only,** with explicit facts. Robustness to noisy or
  multilingual input is not measured.

## 10. Carried-over Phase 3 to-dos (from Phase 2b)
1. **Live-page drift check:** the developer spot-checks the live HDB pages for the critical
   facts before submission (G-15, D-058).
2. **Rights clearance:** the developer clears the facts, moving `rights_review` to `cleared`
   (REQ-LIC-015).
3. **README data section:** write it (03 §8), with the D-054 and D-057 disclosures.
