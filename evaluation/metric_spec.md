# Metric specification (BTO Buddy benchmark)

**Status: draft for approval (D-066, PROPOSED).** This file is frozen together with the
benchmark (evaluation_benchmark §8). After that it changes only through a new decision, and
any change made after a held-out run is disclosed (REQ-EVL-022, REQ-EVL-026).

- **Built from development cases only.** Every example and every denominator below comes
  from `evaluation/benchmark/dev.jsonl`. Held-out denominators are computed by the scorer
  from the frozen labels and reported with the results.
- **Requirements:** REQ-EVL-020 to REQ-EVL-030, D-004, D-063 to D-066.
- **Open questions resolved here (PROPOSED):**
  - Q-14: claim segmentation (§4.3);
  - Q-15: answer coverage (§4.6);
  - Q-16: human-review burden, kept as an operational measure (§6);
  - Q-17: who scores (§3).

## 1. Principles

1. **Architecture-neutral primary metrics.** Every primary metric is judged on the
   **user-visible answer only**. The annotator never sees internal traces: rule IDs, the
   extracted profile, retrieved facts, verifier labels or prompts. Configuration A, which has
   no rules or retrieval, is scored exactly as D is.
2. **Rule IDs are never a scoring unit for the primary metrics.** Rule triggering, citations,
   retrieval and the verifier are scored separately as **diagnostics** (§5). They explain
   *why* a configuration performed as it did; they do not decide *whether* it helped the user.
3. **One judgement, one metric.** Each scoring unit feeds exactly one primary metric, so the
   metrics are independent. Asking for a missing field earns missing-information credit, not
   coverage credit. Declining an excluded request earns abstention credit, not coverage credit.
4. **Only question-relevant requirements are scored.** The unit for required information is
   the label's key points, which the rubric (evaluation_benchmark §2.1) defines as what the
   answer to *this question* must convey. Rules the engine cannot determine but which the
   label leaves out (the `undetermined-but-unlabelled` warnings) are **not** scored.
5. **Labels are ground truth; the frozen KB is the policy reference.** That means
   `kb-2026-10-28.1` under assumption A-01. The runtime verifier is never ground truth
   (REQ-EVL-029).

## 2. Scoring units

| Unit | Definition | Source |
|---|---|---|
| **Case** | One benchmark case answered by one configuration. 18 dev cases; 30 held-out cases | `dev.jsonl`, `test_inputs.jsonl` |
| **Content item** | A key point that states policy content the answer must convey | Key points tagged `content` (§2.1) |
| **Interaction item** | A key point that describes a behaviour: ask, flag, decline or redirect | Key points tagged `interaction`; scored through §4.4 and §4.5, never in §4.2 |
| **Missing-field instance** | One `(case, required_missing_field)` pair | `required_missing_fields` |
| **Conflict instance** | One entry of `expected_conflicts` | `expected_conflicts` |
| **Prohibited conclusion** | One `prohibited_conclusions` entry, with its severity | Label |
| **Claim** | One atomic, checkable factual statement in the visible answer (§4.3) | Segmented from the answer |

### 2.1 Tagging key points (content vs interaction)

- **Who and when:** the annotator tags each key point once per case, from the label alone,
  **before viewing any answer to that case**. The tags are identical for every configuration
  and are never revised after outputs are seen.
- **Interaction:** a key point that tells the assistant to ask, point out a conflict, decline
  or refer ("Ask both ages…", "Note that 'engaged' and 'my wife'…", "BTO Buddy does not
  calculate grants").
- **Content:** every other key point, including conditional guidance ("…given only
  conditionally until they confirm").
- **Mixed items:** an item that asks for a field *and* explains why is tagged interaction.
  The explanation is not scored separately.
- **Dev tagging** is in Appendix A: 44 key points, 33 content and 11 interaction.

## 3. Annotation procedure (Q-17)

- **Scorer:** the developer, manually. Neither an LLM judge nor the runtime verifier produces
  primary-metric judgements, and model-generated labels are never ground truth.
- **Blinding:**
  - Answers are exported to a scoring sheet under random answer IDs, in a seeded random order,
    with the configuration hidden.
  - All configurations are rendered with the same template.
  - **Residual unblinding:** D's "withheld" notices can identify it. This is disclosed as a
    limitation.
- **Order:**
  1. Tag key points (§2.1).
  2. Segment and judge claims (§4.3).
  3. Score the case-level judgements (§4.1, §4.2, §4.4 to §4.7).
- **Evidence for judgements:** the frozen facts (`policy_facts.jsonl`), the label, and the
  documented unresolved items (U/I/G). The live HDB site is never used (A-01).
- **Recorded per judgement:** a one-line rationale for every 0 and every critical error.
- **Single annotator:** this is disclosed. There is no inter-rater agreement. Optionally, a
  seeded 20% sample is re-scored at least 24 hours later and intra-rater agreement reported.

## 4. Primary metrics (architecture-neutral)

Every metric reports **raw counts and the denominator**, overall and per category.

### 4.1 Critical-error rate (primary)

- **Unit:** case.
- **Numerator:** cases whose visible answer asserts **at least one critical error**:
  - **(a)** a labelled `critical` prohibited conclusion, judged by meaning, not wording;
  - **(b)** an **unlabelled critical error** found during claim annotation. This is a
    contradicted claim that is materially misleading about preparation or eligibility
    (05 §4.3). It must cite the contradicted fact ID and is listed individually in the
    results.
- **Denominator:** all cases run, **including failed and withheld cases** (§7).
- **Reported separately:**
  - **Major errors** per case (mean and total). These are labelled `major` prohibited
    conclusions, plus missed content items (05 §4.3: "missing an important applicable
    requirement"), plus a conditional requirement stated unconditionally.
  - The breakdown of (a) versus (b).
- **Dev denominator:** 18 cases. The labels carry 30 critical and 13 major prohibited
  conclusions.

### 4.2 Required-information coverage (primary; replaces rule-ID recall, D-066)

- **Unit:** content item.
- **Judgement:** binary. An item is **conveyed (1)** when the answer states its essential
  content (every number, condition and exception the item contains), consistently with the
  label and without contradiction. Conditional items must be stated conditionally.
- **Scores 0:** absent, wrong, only vaguely alluded to, or withheld by the verifier.
  "Partial" is recorded for diagnosis but scores 0.
- **Metric:**
  - **Micro:** conveyed content items ÷ all content items, pooled over every case.
  - **Macro:** the mean of per-case coverage, over cases with at least one content item.
- **Dev denominator:** 33 content items in 17 cases. DEV-18 has none.
- **Rationale:** this is the architecture-neutral form of APP's "required-rule recall". A
  rule is a policy requirement the user must learn, not an internal ID. Fact-only cases with
  no rule (DEV-08) are scored.
- Whether the configuration *triggered* the rule is diagnostic D1.

### 4.3 Factual correctness and the unsupported-claim rate (primary, claim level)

**Segmentation (Q-14):**
- **A claim** is one atomic proposition about policy or process: a number, period, condition,
  exception, procedure step, or a statement about how a requirement applies to this user.
  Compound sentences are split, one claim per proposition.
- **Not checkable (excluded from the denominator):**
  - questions to the user;
  - statements about the assistant itself ("I can't calculate grants");
  - generic advice with no policy content ("plan early");
  - the verifier's withheld notices.

  This is D-065's "hedged and procedural" exclusion, read narrowly. A procedure step
  ("apply on the HDB Flat Portal") **is** checkable.

**Judgement (against the frozen KB):**
- **correct:** entailed by a verified fact, or consistent with a documented interpretation
  stated as such;
- **incorrect:** contradicted by a verified fact, including a dropped exception or a wrong
  number;
- **unsupported:** not established by the KB, either beyond what the evidence states or
  outside the KB. It is tagged `outside_kb` when the topic is not in the KB at all. A
  definitive answer on U-01 to U-04 is **unsupported**.

**Metrics (denominator = checkable claims, pooled):**
- **Factual correctness** = correct ÷ checkable claims.
- **Unsupported-claim rate** = unsupported ÷ checkable claims (REQ-EVL-024).
- **Incorrect-claim rate** = incorrect ÷ checkable claims.

Also reported: the number of checkable claims per answer, and the `outside_kb` share of the
unsupported claims. An answer with 0 checkable claims adds nothing to these pooled rates and
is counted separately.

### 4.4 Missing-information identification (primary)

**(a) Missing-information recall:**
- **Unit:** missing-field instance.
- **Identified** when the answer asks for that information, or says explicitly that the
  guidance depends on it. Any wording counts; the annotator maps the wording to the field.
- **Metric:** identified ÷ instances (micro), plus a macro mean over cases that have
  instances.
- **Dev denominator:** 6 instances in 4 cases (DEV-04: 3; DEV-05, DEV-06, DEV-13: 1 each).

**(b) Conflict identification:**
- **Unit:** conflict instance.
- **Identified** when the answer names the inconsistency and asks for clarification
  **without settling either side**. Rubric §2.6 applies: no presumption that the user is
  wrong.
- **Metric:** identified ÷ instances.
- **Dev denominator:** 3 (DEV-13, DEV-14, DEV-15).

**(c) Redundant asks (secondary):** the number of answers that ask for information the input
already states clearly. This exposes over-questioning, which recall cannot.

### 4.5 Appropriate abstention (primary) and over-abstention

**Appropriate abstention:**
- **Unit:** case.
- **Denominator:** cases with `answerable` set to `partial` or `no` whose
  `expected_behaviour` includes `abstain_and_redirect`, `state_unconfirmed` or
  `partial_answer_and_redirect` (REQ-EVL-021).
- **Correct** when all the applicable conditions hold:
  1. it declines the excluded request (no calculation, estimate or verdict), or for
     `state_unconfirmed` says the point is not established by the sources, without deciding
     it;
  2. it gives an official redirect (an HDB page or HDB itself);
  3. for `partial_answer_and_redirect`, it also conveys at least one content item for the
     in-scope part.
- **Dev denominator:** 3 (DEV-16, DEV-17, DEV-18).

**Over-abstention rate:**
- **Denominator:** `answerable = yes` cases. Dev: 9.
- **Numerator:** answers that decline, defer the whole question to HDB, or are entirely
  withheld, while conveying no content item.

### 4.6 Answer coverage (primary in this spec; Q-15)

- **Unit:** case.
- **Denominator:** `answerable` set to `yes` or `partial`. Dev: 15.
- **Covered** when the visible answer conveys at least one content item and is not a blanket
  refusal.
- **Distinct from 4.2 and 4.5:**
  - 4.2 measures *how much* required content arrives;
  - 4.6 measures *whether the user got any usable answer at all*;
  - over-abstention measures *refusal* on fully answerable cases.

### 4.7 User-facing actionability (primary in this spec)

- **Unit:** case. **Denominator:** `answerable` set to `yes` or `partial` (dev: 15).
- **Three binary criteria, judged on the visible answer:**

| Criterion | Met when |
|---|---|
| **A1 Next step** | The answer gives at least one concrete action the user can take now (e.g. "complete Step 1 on the HDB Flat Portal", "write to HDB before the HFE application", "tell us whether you are engaged or married"), and that action is consistent with the KB |
| **A2 Where** | The action names an official channel or page (portal, page name or URL). This checks presence and relevance only; whether the citation is correct is diagnostic D2 |
| **A3 No dead end** | Every point the answer leaves open says how to resolve it: what to provide, or whom to confirm with |

- **Metric:** mean of (A1 + A2 + A3) ÷ 3 over cases, plus the count of cases meeting all
  three.
- **Limitation:** this is a judged construct, with a single annotator.

## 5. Diagnostics (architecture-dependent; never used to rank configurations)

| ID | Diagnostic | Unit and denominator | Applies to |
|---|---|---|---|
| **D1** | **Rule-trigger accuracy** (from the trace) | Recall = required ∩ engine `applies` ÷ required rule instances (dev: 17 in 11 cases). Precision = engine `applies` ∩ (required ∪ optional) ÷ engine `applies`. Conditional accuracy = conditional ∩ engine `cannot_determine` ÷ conditional instances (dev: 9). Engine `cannot_determine` rules outside the label are **not** counted as errors (principle 4) | C, D |
| **D2** | **Citation quality** | Citation precision = (claim, citation) pairs where the cited source substantively supports the claim ÷ all pairs. Citation coverage = checkable claims with at least one citation ÷ checkable claims. With 0 citations, precision is "n/a (0 citations)", never 0 or 1 | All configurations that emit citations |
| **D3** | **Retrieval recall@k** | Unit (case, gold fact), gold = `evidence_fact_ids` (dev: 52 in 18 cases). BM25 recall@5 (decision threshold 0.90, D-031) and recall@10, plus evidence-set recall (gold facts in the final evidence passed to generation, after rule-linked facts are added). Micro and macro | B, C, D |
| **D4** | **Verifier accuracy** | Claim set (D-065): per-class precision and recall for `contradicted` and `insufficient`; false-alarm rate = supported claims flagged ÷ supported claims; false-approval rate = contradicted or insufficient claims labelled supported ÷ those claims. On benchmark answers (C vs D, identical pre-verification outputs): withheld claims split into incorrect or unsupported (benefit) vs correct (cost), using the §4.3 judgements | D (and the verifier in isolation) |

## 6. Operational measures

| Measure | Definition |
|---|---|
| Latency | End-to-end seconds per case, median and p95 per configuration, including retries |
| Cost | Recorded input and output tokens × the published price on the run date, per case and per configuration. $0 plus a compute note for a free tier |
| Human-review burden (Q-16) | Verification flags and withheld claims per answer (D only). Reported, not ranked |
| Failures | Count and type per configuration (§7) |

## 7. API failures, withheld answers and reruns

**API failure:** a timeout, rate-limit, 5xx or network error, or an output the pipeline
cannot parse after its own documented fallback.
- **Retries:** up to 3 per LLM call, with exponential backoff (2, 4 and 8 seconds), on
  identical inputs and settings. Every retry is logged. These harness parameters are fixed
  before the held-out run.
- **Still failing:** the case is recorded as `system_failure`. It **stays in every
  denominator**:

| Metric | A `system_failure` scores |
|---|---|
| Critical-error rate | No critical error (nothing was asserted). The failure count is shown next to the rate so a failing system cannot look safe |
| Coverage, actionability, answer coverage | 0 |
| Missing-information and conflict identification | Not identified |
| Appropriate abstention | Not correct (an error message is not a redirect) |
| Over-abstention | Not counted as abstention; counted under failures |
| Claims | None |

- **Sensitivity analysis:** primary metrics are also reported excluding failed cases, labelled
  as such.
- **Invalid run:** if more than 10% of a configuration's cases fail (4 or more of 30), that
  configuration's entire run is repeated once with identical settings. Both runs are
  reported, and the repeat is used. No case-level cherry-picking: successful cases are never
  re-run individually.

**Withheld content (D-011):** scoring always uses the **visible** answer.
- **A withheld claim** is not conveyed (§4.2), not asserted (§4.1, §4.3), and not a citation.
- **A wholly withheld answer,** which shows only a notice and redirect, is scored like any
  other answer:
  - on abstention-required cases it can be correct if it meets §4.5;
  - on `yes` cases it counts as over-abstention and is not covered.
- **D4** separately reports whether each withheld claim was actually wrong.

**Empty answer:** scored as a wholly withheld answer with no redirect.

## 8. Statistics and reporting (REQ-EVL-030, REQ-EVL-031)

- **Pre-specified comparisons:**
  - C vs A (the core intervention);
  - D vs C (the verifier, on identical pre-verification outputs);
  - B vs A (grounding), if B is run.

  Everything else is descriptive.
- **Binary case outcomes** (critical error, abstention correct, covered): exact McNemar on
  paired discordant counts, reported with the counts.
- **Proportions and rates:** a paired bootstrap over cases (10,000 resamples, fixed seed),
  with 95% percentile intervals on the difference.
- **Always reported:** raw counts, denominators, per-category tables and all failures.
  - **No dev numbers** are presented as test results.
  - **No significance claims** beyond the pre-specified comparisons.
  - **Framing:** "a controlled benchmark of 30 fictional cases, not population-level
    evidence".
- **Recorded per run:** model IDs, prompt versions, inference settings, KB and rules
  versions, the benchmark version, and saved predictions (CLAUDE.md, Evaluation).

## 9. Use of development cases

- Dev metrics are computed freely during development and prompt work.
- Held-out metrics are computed once, after the freeze and after this spec is frozen, via
  `load_test_labels(final=True)`.
- Changes after a held-out run are disclosed, and the test set is not presented as untouched
  (REQ-EVL-022).

## Appendix A. Dev key-point tagging (C = content, I = interaction)

Key points are numbered in label order.

| Case | Tags | Notes |
|---|---|---|
| DEV-01 | C C C C | |
| DEV-02 | C C C C | |
| DEV-03 | C C C | The approximate date and the cross-month update are both content (§4.2) |
| DEV-04 | C I I | Asking both ages and asking about the HFE letter are scored in §4.4 |
| DEV-05 | I C | |
| DEV-06 | I C | |
| DEV-07 | C C | |
| DEV-08 | C | No rule fires; scored only through §4.2 (principle 2) |
| DEV-09 | C C C | |
| DEV-10 | C C | |
| DEV-11 | C C | |
| DEV-12 | C C | |
| DEV-13 | I C C | The first item is the neutral clarification (§4.4b); the second is conditional content |
| DEV-14 | I C C | |
| DEV-15 | I C | The second item is conditional content |
| DEV-16 | I C | Decline (§4.5); "the HFE letter states the amounts" is content |
| DEV-17 | I C | |
| DEV-18 | I I | No content items; scored in §4.5 only |
| **Total** | **33 C, 11 I** | |

## Appendix B. Worked example (DEV-13; illustrative, not a real output)

An answer says: "Congratulations on your marriage! As a married couple you can apply. Get
your HFE letter first on the HDB Flat Portal."
- **§4.4b conflict:** not identified. It settles "married", which is also PC-X1, a major
  error.
- **§4.2:** content item 2 (conditional marital-status guidance) scores 0. Content item 3
  (HFE letter first) scores 1. Coverage is 1 of 2.
- **§4.4a:** `hfe_status` not asked, so 0 of 1.
- **§4.1:** no critical prohibited conclusion is asserted, so it is not a critical-error
  case. It has 1 major error.
- **§4.7:** A1 = 1, A2 = 1 (portal), A3 = 1 (nothing is left open). Actionability is 3/3.
  The wrong assumption is penalised once, in §4.4b and PC-X1, and not again here: the metrics
  are independent (principle 3).
