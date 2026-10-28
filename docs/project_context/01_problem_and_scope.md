# 01 — Problem and Scope

The status and provenance legend is in [INDEX.md](INDEX.md#legend). Requirement IDs are
defined in [requirements_register.md](requirements_register.md).

## 1. Project identity

| Item | Value | Status | Source |
|---|---|---|---|
| Project | **BTO Buddy**: a pre-application preparation assistant for Build-To-Order (BTO) flat applicants | APPROVED | [APP p.1], D-002 |
| Repository / package / app | `bto-buddy` / `bto_buddy` / "BTO Buddy" | APPROVED | D-002 |
| "BTOPath" | Earlier working name, found in some tables and figures | SUPERSEDED | [APP p.3, 21, 24, 25] |
| "PolicyProof" | Earlier brainstorming concept for evidence-grounded factual verification. Never implemented. BTO Buddy borrows its verification principles only | HISTORICAL | [APP p.21], D-015 |
| Stakeholder | Citizen group (prospective BTO applicants) | APPROVED | [APP p.29], REQ-PRB-001 |
| Assessment theme | Retrieval & knowledge (primary). The verification layer also touches "generation with guardrails" | APPROVED (primary), inference (secondary) | [APP p.29], [ASM p.1] |

## 2. Final revised idea — REQ-PRB-010 (APPROVED) [APP p.1–2]

- BTO applicants face a **sequence of decisions**:
  - applicant eligibility;
  - household composition;
  - income;
  - HDB Flat Eligibility (HFE) letter requirements;
  - priority schemes;
  - application consequences.
- The problem is **not** that official information is missing. Applicants struggle to work
  out which rules apply to *their* circumstances, and what information they still need
  before they proceed.
- Official tools already exist: HFE assessments, eligibility guidance and application
  information. BTO Buddy adds a **pre-application preparation layer** that helps applicants:
  - understand the relevant published rules;
  - identify missing information;
  - prepare questions before they use the official application process.
- **Differentiation:** transparency and preparation. BTO Buddy does not replace the
  authoritative assessment.

### 2.1 Observed gap in existing channels [APP p.1–2] (developer observation)

**The HDB website's virtual assistant.**
- A screenshot in the project approach shows a test query: a first-timer with four previous
  unsuccessful BTO attempts asks whether they have an advantage at the next attempt.
- The assistant replied that it did not understand and asked the user to rephrase. It then
  listed three generic links:
  - a First-Timer (Parents & Married Couples) priority-scheme page on an external
    government services directory;
  - "Application for a New Flat";
  - "Modes of Sale".
- The user is left to read through the linked pages themselves.

**The website itself.**
- Pages link to anchors on the same page, to other portal pages, or to external resources
  such as PDFs and other sites.
- Information relevant to one user group is scattered across pages, and irrelevant content
  is still shown, so important clauses are easy to miss unless every expandable section is
  opened.
- Some content exists only in infographics (images) or in videos hosted on YouTube.
- An applicant may qualify for several schemes without realising it. The site works more as
  an **information dump** than as applicant-centred guidance.

**Effect on users:** a generic, non-personalised experience that causes fatigue.

### 2.2 Potential downstream benefit — HYPOTHESIS ONLY (REQ-PRB-015) [APP p.2]
Better-prepared citizens *could* reduce HDB operational load: fewer hotline enquiries and
fewer ineligible applications to process. This needs future user testing to validate and
quantify, and must not be claimed as a result.

## 3. Problem statement — REQ-PRB-011 (APPROVED) [APP p.3]
> BTO applicants must navigate multiple interdependent eligibility and application rules.
> While authoritative guidance exists, translating these rules into personalised, actionable
> preparation steps can require substantial manual interpretation. BTO Buddy aims to reduce
> that burden while keeping official sources and human verification central to the process.

*(This is the developer's own text; "bto-buddy" is normalised to "BTO Buddy" per D-002.)*

## 4. Research question — REQ-PRB-012 (APPROVED) [APP p.3]
> Can a hybrid AI assistant combining structured applicant profiling, authoritative policy
> retrieval and evidence verification provide more reliable BTO pre-application guidance than
> a conventional LLM assistant?

**Intended narrative [APP p.3]:**
1. Identify a real public-service information challenge.
2. Build an assistant that turns complex published requirements into personalised
   preparation guidance.
3. Evaluate whether structured reasoning and evidence verification make it more reliable
   than simpler approaches.

## 5. Problem validation — REQ-PRB-013, REQ-PRB-014 [APP p.3, 29–30], D-025

- **APPROVED stance:**
  - Policy *complexity* can be substantiated from official documentation: multiple
    eligibility pathways, detailed income rules, HFE requirements, application consequences
    and exceptions.
  - The *frequency* of applicant confusion needs separate supporting evidence.
  - **Never invent** statistics about call-centre volume, citizen frustration or operational
    benefit.
- **Optional research tasks (OPEN, not started):**
  - volume of BTO applications;
  - demographics of BTO applicants;
  - general sentiment about BTO applications, including applicant confidence and the share
    of young applicants who feel confused;
  - volume of avoidable hotline enquiries.
- **Optional evidence route (PROPOSED) [APP p.29–30]:** given the short timeframe, cite
  findings from *past public-sector hackathon projects* as predecessors. Use them only where
  they are publicly documented, and cite them accurately.

## 6. MVP scope — REQ-SCP-001 (APPROVED, authoritative) [APP p.17–18], D-008

This table is the approved functional scope. Earlier source-discovery findings, ideas and
proposed enhancements **do not** expand it automatically (REQ-SCP-007).

| Policy area | Tier | Source |
|---|---|---|
| First-timer couple household composition | **Core** | [APP p.17] |
| Broad BTO application requirements | **Core** | [APP p.18] |
| HFE prerequisites, timing and documentation | **Core** | [APP p.18] |
| Missing applicant information | **Core** | [APP p.18] |
| Relevant first-timer and priority considerations | **Limited, source-verified** | [APP p.18] |
| Application and non-selection consequences | **Limited, source-verified** | [APP p.18] |
| High-level HFE / loan / grant explanations (relationship only) | **Context only** | [APP p.18] |
| Grant and loan eligibility calculations | **Excluded** | [APP p.18] |
| Detailed affordability and financing | **Excluded** | [APP p.18] |
| Post-purchase conditions | **Excluded** | [APP p.18] |
| Ballot probability prediction | **Excluded** | D-008 (new 2026-10-28) |
| Comprehensive official eligibility determination | **Excluded** | D-008 (new 2026-10-28) |
| Videos explaining existing written guidance | **Excluded from the core retrieval corpus.** Optional contextual links only, when the topics "Step 1: Check Preliminary HFE" or "Step 2: Apply for HFE Letter" are relevant to the query | [APP p.18] |

### 6.1 Tier semantics (APPROVED) [APP p.17]

| Tier | Rule | ID |
|---|---|---|
| Core | Must be implemented **and** evaluated | REQ-SCP-002 |
| Limited | May be implemented only where authoritative evidence and testable requirements exist | REQ-SCP-003 |
| Context only | May be explained or linked. Must **not** trigger independent eligibility calculations | REQ-SCP-004 |
| Excluded | Handled by the **coverage gate**, with redirection to the official source | REQ-SCP-005 |

Any scope expansion needs explicit approval **and** an update to the evaluation plan
(REQ-SCP-006).

### 6.2 HFE boundary statement — REQ-SCP-008 (APPROVED) [APP p.18]

**BTO Buddy does:**
- explain how the HFE process relates to flat-purchase eligibility, CPF housing grants and
  HDB housing-loan eligibility;
- identify the relevant preparation requirements;
- direct applicants to authoritative sources.

**BTO Buddy does not:**
- calculate grant amounts;
- determine loan eligibility or financing amounts;
- compare loan products;
- replace the official HFE assessment.

Questions that need these determinations are redirected to the relevant official services.

### 6.3 Income and employment boundary — REQ-SCP-010 (APPROVED) D-013
- Income and employment details are used **only** for HFE preparation: identifying required
  documents and asking relevant follow-up questions.
- No comprehensive income-eligibility calculation, no income-ceiling determination and no
  financing calculation.
- Income-assessment exceptions enter the benchmark only if they are within preparation scope
  and backed by verified evidence.

### 6.4 Supported-question inventory — DRAFT (PROPOSED; finalised in Phase 2 per D-007/D-008)

The original list [APP p.5] is SUPERSEDED by D-008. It read: high-level BTO process and
requirements, first-timer couples, HFE preparation, missing information, non-selection
consequences. The draft below is derived from the approved tiers.

| Tier | Example question types |
|---|---|
| Core | "We're a first-timer couple. What do we need to prepare before applying for a BTO?"; "Do we need an HFE letter, and when should we apply?"; "What documents does HFE need for my employment situation?"; "Who can be listed as applicant/occupier?" |
| Limited | "Are there first-timer or priority considerations that may be relevant to us?" (identify and link only); "What happens if we don't select a flat when invited?" |
| Context only | "How does the HFE letter relate to grants and loans?" (explanation only, no amounts) |
| Excluded → gate | "How much grant will we get?"; "Can we afford a 4-room?"; "What are our chances in the ballot?"; "Can we rent out after MOP?"; "Confirm that we are eligible." |

**OPEN (Q-05):** whether non-couple household types count as out-of-scope, or as "Limited"
recognition with redirection. Examples are multi-generation, orphaned siblings,
non-resident family members, seniors and unwed parents (see [02](02_policy_sources.md)).

## 7. Missing information: two distinct categories — REQ-SCP-013 (APPROVED) [APP p.18–19]

These must be kept separate in the architecture, the benchmark and the documentation.

| Category | Meaning | Examples | Required behaviour |
|---|---|---|---|
| **A. Missing applicant information** | The applicant hasn't given a detail needed to identify the relevant preparation requirements | One partner's citizenship status is unknown; HFE application/approval status is unspecified; prior flat ownership or application is not stated; employment information is needed but not supplied | Ask a targeted follow-up, or name the information to prepare. **Never assume missing values** |
| **B. Missing policy information in the corpus** | The frozen KB lacks enough authoritative evidence to answer reliably | A linked FAQ with an exception was never included; an accordion condition wasn't extracted; an infographic has a step absent from the text; the policy changed after capture; the passage exists but retrieval missed it | Don't invent an answer. Flag insufficient evidence or unsupported coverage and direct the user to the official source |

The failure sub-types of category B are listed in [05 §8](05_evaluation.md).
The runtime contract is in [04 §3](04_architecture.md).

## 8. Demo archetypes — REQ-SCP-014 [APP p.20–21]

These are for the 3–5 minute video. They are **not** the evaluation dataset and can still be
refined.

| Scenario | Description | Capability shown |
|---|---|---|
| A — Straightforward applicant | A fictional first-time couple gives a complete profile. BTO Buddy identifies the relevant preparation requirements and links official sources | Straightforward guidance |
| B — Missing information | A couple gives incomplete employment or household information. BTO Buddy asks targeted follow-ups instead of making an unsupported determination | Missing-information handling |
| C — Policy misconception | An applicant assumes something incorrect about application consequences. BTO Buddy retrieves the official guidance, explains the distinction and flags uncertainty where needed | Verification layer |

- **APPROVED constraint:** the demo examples must represent actual system behaviour. Don't
  pick only unusually easy cases that hide known failure modes.
- The original text called Scenario C valuable for the "PolicyProof-inspired" verification
  layer. That label is HISTORICAL (D-015).

## 9. Scope discipline and non-claims (APPROVED) [APP p.28]

- **REQ-SCP-012:** a small system that handles **4–5 policy areas** accurately, with a
  rigorous baseline comparison, beats a broad, unreliable assistant.
- **REQ-SCP-011:** never claim comprehensive coverage of all current and historical BTO
  policies. Rules vary by application date, flat classification, applicant category and
  policy changes. A statement can be correct for one sales exercise and wrong for another.

## 10. Positioning against the brief's illustrative sketches [ASM p.5–6]

The brief offers optional, anonymised problem sketches, and choosing any of them is not
required. The nearest ones are:
- profile-driven benefits matching;
- citizen-enquiry triage with escalation;
- out-of-knowledge-base robustness for RAG ("I do not know" vs confabulation).

*(Author note: neither source document says which sketch, if any, BTO Buddy derives from.
The developer should confirm the wording before using this in the README.)*
