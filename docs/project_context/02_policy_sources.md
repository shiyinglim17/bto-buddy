# 02 — Policy Sources

The legend is in [INDEX.md](INDEX.md#legend).

> **Copyright note (D-016):** this file records source *locations, structure and media
> types*. Policy content appears only as short, independently paraphrased **AUTHORED-FACT
> (unverified)** notes. Each must be verified against a frozen source in Phase 2 before it
> enters `data/policy_facts.jsonl`. The project-approach document quoted HDB text verbatim
> in places, marked **COPIED-SOURCE** below. Those quotations are *not* reproduced here; only
> their location and a paraphrase are kept.

## 1. Seed sources — REQ-SRC-001 (APPROVED as seeds, D-007) [APP p.4]

These are **seed sources**, not necessarily the complete corpus. The minimum MVP source set
is decided in Phase 2 (REQ-SRC-014).

| Seed ID (proposed) | Page | URL | What it provides |
|---|---|---|---|
| SEED-1 | Couples and Families | https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/couples-and-families | Household composition and broad eligibility conditions |
| SEED-2 | Application for an HDB Flat Eligibility (HFE) Letter | https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/application-for-an-hdb-flat-eligibility-hfe-letter | HFE requirements, validity and process |
| SEED-3 | Income Guidelines and Documents for HFE Letter Application | https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/application-for-an-hdb-flat-eligibility-hfe-letter/income-guidelines-and-documents | Assessment periods, income calculation and documents |
| SEED-4 | Application for a New Flat | https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/process-for-buying-a-new-flat/application | Application and non-selection consequences |

## 2. Discovery method (APPROVED) [APP p.5]

- **Discovery path:** seed pages → relevant anchors → linked pages → PDFs and visual
  content (REQ-SRC-005).
- Relevant sources and hyperlinks are mapped **manually** (done for the matrix below).
- A **frozen, versioned corpus** is used for evaluation, so website changes can't alter
  benchmark results between runs (REQ-SRC-004).
- **Observed site structure:**
  - hyperlinks go to anchors on the same page, other portal pages, or external resources
    (PDFs in a new tab, other sites);
  - user-group information is scattered, and irrelevant content is still shown;
  - some content exists only in infographics (images) or YouTube videos.

## 3. Source-discovery matrix (complete) [APP p.5–11]

> **Status:** this matrix lists *candidate* sources. It is **not scoped to the MVP** and
> does not expand it (REQ-SCP-007, BD-02). Each row notes its MVP tier relation for
> orientation only.
>
> **Phase 2a (2026-10-28):** the reconciled, MVP-classified version with stable source IDs
> (S01–S17, M00–M04) is in [../data_sources.md](../data_sources.md)
> (PROPOSED, D-044 to D-055). It was re-checked against APP p.4–12; nothing below was lost
> in extraction.
>
> **Live-site differences found at capture (2026-10-28):**
> - FT(PMC) and FPPS are no longer on "Couples and Families"; they are on "Priority
>   Schemes" (S05).
> - "Priority Schemes" also lists an assistance scheme for second-timer divorced or widowed
>   parents (Outside MVP).
> - The HFE page has an "Income guidelines" accordion, and its timing details appear in the
>   text as well as the infographic.
> - The two HFE PDF guides are linked through `go.gov.sg` short links.
>
> The matrix below is kept as recorded.

### Row 1 — Applicant composition and types: definitions and eligibility conditions [APP p.5–8]

**MVP tier relation:** Core for first-timer couples; other groups are OPEN (Q-05).

**Main source 1: "Couples and Families" (SEED-1).** URL in §1.

- **Content structure:** eligibility conditions per user group / applicant category, mostly
  as **expandable sections on the same page**, formatted as **tables, sometimes nested**.
- **Applicant categories listed** (names only):
  - Fiancé and fiancée;
  - Married couples and/or parent(s) with child(ren), as a Singapore Citizen (SC) or
    Singapore Permanent Resident (SPR) household;
  - Multi-generation families (buying with fiancé(e)/spouse and parents);
  - Orphaned siblings (buying with sibling(s) who are orphans and single);
  - Families with non-residents (an SC buying with a non-resident spouse or parent(s)/child(ren)).
- **Defined priority schemes on this page** (expandable sections):
  - First-Timer (Parents & Married Couples), **FT(PMC)**;
  - **Family and Parenthood Priority Scheme (FPPS)**, which supports first-timer married
    couples with children and young married couples.

**Main source 2: "Priority Schemes".**
URL: https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/process-for-buying-a-new-flat/application/priority-schemes

Expandable section per scheme, grouped by target group:

| Target group | Scheme | Format |
|---|---|---|
| Couples expecting a child, and families with child(ren) | Third Child Priority Scheme (**TCPS**), for families with 3+ children | expandable section |
| Parents and children who want to live with or near each other (fiancé/fiancée applicants may also qualify) | Family Care Scheme (**FCS**) (Proximity) | expandable section |
| (same group) | Family Care Scheme (**FCS**) (Joint Balloting) | expandable section |
| Seniors who want to live near their existing home (2-room Flexi, to age in place) | Senior Priority Scheme (**SPS**) (near existing home) | expandable section |
| Public rental tenants who want to buy their own home | Tenants' Priority Scheme (**TPS**), for HDB rental tenants buying 2-room Flexi or 3-room | expandable section |

**Specific user groups / exclusions** (linked sources and conditions):

| Item | Source | Notes | Provenance |
|---|---|---|---|
| Seniors (both aged 55+, buying a short-lease 2-room Flexi or Community Care Apartment) | Separate page: https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/seniors | Separate page on the HDB site | Structure note |
| First-timer households with exactly 1 SC + 1 or more SPR members | SEED-1; Citizen Top-Up page: https://www.hdb.gov.sg/managing-my-home/finances/citizen-topup | Paraphrase: such households pay a premium at flat purchase (amount stated on the source, recorded as $10,000). A Citizen Top-Up may be claimed later when an SPR member becomes a citizen or an SC child is born | COPIED-SOURCE in APP p.7 → AUTHORED-FACT (unverified) here. **OPEN (Q-06):** is this a premium/financing matter (Excluded) or a first-timer consideration (Limited)? |
| Fiancé/fiancée below 21 | SEED-1 | Paraphrase: an under-21 fiancé(e) can only be listed as a core occupier. Applicants must contact HDB with both parties' details *before* applying for the HFE letter | COPIED-SOURCE in APP p.7 → AUTHORED-FACT (unverified). Benchmark candidate ([05 §9](05_evaluation.md)) |
| Validity of flat applications | SEED-1 | Paraphrase: a flat application is valid only if the persons listed don't change | COPIED-SOURCE in APP p.7 → AUTHORED-FACT (unverified) |
| Unwed parent buying with child(ren) | SEED-1 | Paraphrase: must write to HDB, which assesses the request holistically. This is **discretionary**, so it must not be a binary rule (REQ-DAT-014) | COPIED-SOURCE in APP p.7 → AUTHORED-FACT (unverified) |

**Additional details (linked):**

| Item | URL | MVP relation |
|---|---|---|
| Minimum occupation period (MOP) | https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/conditions-after-buying-a-new-flat?anchor=mop | Post-purchase → **Excluded** |
| Resale levy | https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/conditions-after-buying-a-new-flat?anchor=resale-levy | **OPEN (Q-07):** the matrix lists it on a "conditions after buying" page without a tier. Treat it as post-purchase (Excluded) or as an application consideration (Limited)? |
| Subsidies, grants | (not given) | **Not in scope** [APP p.7]. May be mentioned at a high level, or users directed to where to find it |
| Income ceiling guide (extended family) — **PDF** | https://www.hdb.gov.sg/-/media/buying-a-flat/flat-grant-and-loan-eligibility/couples-and-families/Income-ceiling-for-extended-family-guide.pdf?sc_lang=en&hash=0E76F0C419381FFAE7EE01691C5D0E8C | Income-ceiling determination is **Excluded** (D-013). Retain only if it helps preparation |

### Row 2 — HFE prerequisites [APP p.8–10]

**MVP tier relation:** Core.

**Main source:** "Application for an HDB Flat Eligibility (HFE) Letter" (SEED-2), plus the
anchor `#how-to-apply`.

**Content structure and media:**

| Element | Type | Content summary (paraphrased, AUTHORED-FACT unverified) |
|---|---|---|
| "What is the HDB Flat Eligibility (HFE) letter?" | **Infographic** (the project approach transcribed its text) | The HFE letter states the applicant's eligibility to (a) buy a new or resale flat, (b) receive CPF housing grants and their amounts, and (c) take an HDB housing loan and its amount |
| Financial-institution (FI) loan note | Text | Applicants planning an FI loan should request an In-Principle Approval (IPA) from participating FIs when applying for HFE. The FIs notify the outcome |
| "When to apply" | **Expandable section** | (content not captured in the project approach → extraction pending) |
| "How to apply" | **Expandable section** containing an **infographic** (flowchart of stages and what you need), a link to an **external step-by-step guide**, and **2 YouTube videos** | See VR-1, external guide and VID-1/VID-2 below |
| "Validity and possible review of HFE letter" | **Expandable section** | When and why an HFE letter may be reviewed (content pending extraction) |
| "Next steps with your HFE letter" | **Expandable section** containing an **infographic** | Steps from HFE application to key collection. See VR-2 |
| HFE FAQs | Separate page: https://www.hdb.gov.sg/hdb-flat-portal/hfe/get-help | Contains **5 sub-links** to separate HDB pages (not yet mapped → Q-08) |
| Integrated loan application service | https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/housing-loan/housing-loan-from-financial-institutions?anchor=integrated-loan-service | Financing → Context only / Excluded |
| HDB Flat Portal (apply/cancel) | Redirect, requires **Singpass login** | **Transactional service: must not be accessed or automated** (REQ-SRC-006) |
| External step-by-step guide | https://www.mynicehome.gov.sg/get-started/hdb-hfe-guide/ | A different government-run site. Rights and robots status to check in Phase 2 |

**Infographic VR-1: "Apply for an HDB Flat Eligibility (HFE) letter"** (inside "How to
apply") [APP p.9, image 1]. Independent summary of its *structure*:
- **Prerequisites shown:** Singpass login details; particulars of the flat applicants and
  occupiers.
- **Step 1 — Check Preliminary HFE:**
  - log in to the HDB Flat Portal;
  - give the particulars of all applicants and occupiers;
  - declare any local or overseas private-property interest;
  - indicate whether a housing loan is intended.
  - An instant *preliminary* outcome gives an overview of eligibility for flat purchase,
    CPF grants and an HDB loan.
- **Step 2 — Apply for HFE letter:**
  - must be completed within a stated window after starting Step 1 (shown as 30 calendar
    days);
  - choose housing-loan option(s): confirm HDB-loan eligibility and/or apply for an IPA from
    participating FIs;
  - give all required information before the due date;
  - review and confirm.
- **Get your results:**
  - the letter is issued after a stated processing time (shown as about one month; longer
    in peak periods around sales launches);
  - notification by SMS and email;
  - validity is shown as 9 months from issue;
  - FIs notify IPA outcomes separately.
- **Category-B relevance:** the 30-day Step-2 window and the processing time appear in the
  image. It is not yet confirmed whether the HTML text carries them too, so this is an
  **extraction-gap test case** ([05 §8](05_evaluation.md)).

**Infographic VR-2: "Your flat buying journey via the HDB Flat Portal"** (inside "Next
steps with your HFE letter") [APP p.9, image 2]. Structure only:

**Shared stages:**
1. Apply for HFE letter (shown as valid 9 months).
2. Optionally, apply concurrently for an IPA from participating FIs.
3. Search for flats (budget calculator).
4. Check your sums (payment-plan calculator; make sure the budget is sufficient).

**New-flat branch** (MVP-relevant up to "Book flat"):
1. Apply online during a sales launch.
2. Receive ballot results.
3. Book flat.
4. If taking an FI loan: request a Letter of Offer.
5. Sign Agreement for Lease.
6. Collect keys.

**Resale branch** (out of scope): Option to Purchase → Request for Value → FI Letter of Offer
→ exercise OTP and submit resale application → completion appointment.

**Videos (excluded from the corpus, REQ-SRC-011):**

| ID | Title (as recorded) | URL |
|---|---|---|
| VID-1 | Step 1: Check Preliminary HDB Flat Eligibility (HFE) | https://youtu.be/Lfmf3KJZy8k?si=gp9yeZg7eB67yqNh |
| VID-2 | Step 2: Apply for HDB Flat Eligibility (HFE) Letter | https://youtu.be/bsno0iJUocs?si=wDpu7tB0j7v7Ymd3 |

The recorded URLs carry `si=` share-tracking parameters. Whether to strip them is OPEN
(Q-09, minor).

### Row 3 — Income-related preparation [APP p.10]

**MVP tier relation:** Core (as HFE documentation), limited by D-013.

**Main source:** "Income Guidelines and Documents for HFE Letter Application" (SEED-3).

| Linked resource | Type | URL |
|---|---|---|
| Supporting documents | Section on SEED-3 | (same page) |
| Income ceiling guide (extended family) | **PDF**, linked from the "Couples and Families" page | See Row 1 |
| Employment Status Guide | **PDF** | https://file.go.gov.sg/hfe-employment-status-guide.pdf |
| Income Declaration Guide | **PDF** | https://file.go.gov.sg/hfe-income-declaration-guide.pdf |

### Row 4 — High-level overview of the BTO application process [APP p.10–11]

**MVP tier relation:** Core.

| Item | URL as recorded |
|---|---|
| Main source: "Application for a New Flat" page | Recorded as `https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/application-for-an-hdb-flat-eligibility-hfe-letter#how-to-apply` — **this is the HFE page URL, not the Application page (SEED-4). See C-14** |
| Process and ballot mechanisms: "Modes of Sale" | https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/process-for-buying-a-new-flat/modes-of-sales |

The exceptions / linked-sources column is empty.

### Row 5 — Non-selection consequences [APP p.11]

**MVP tier relation:** Limited, source-verified.

| Item | Detail |
|---|---|
| Main source | The "Cancellation of flat application" expandable section of "Application for a New Flat": https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/process-for-buying-a-new-flat/application?anchor=cancellation |
| Exceptions / linked | "Exceptions and waivers" (no URL given → locate in Phase 2) |

## 4. Media-handling decisions (APPROVED) [APP p.11–12, 18]

| Media | Decision | ID |
|---|---|---|
| General | Handle PDFs, infographics and videos **only when they hold unique information essential to MVP coverage**. Use the **simplest extraction method** suited to each content type | REQ-SRC-008 |
| PDFs | Extract when policy-critical. First check whether an official HTML page carries the same information. Otherwise extract text and tables with PyMuPDF and manually validate the relevant pages. Keep the title, URL, page number, publication date and section heading. OCR only if text extraction fails **and** the content is essential | REQ-SRC-009 |
| Infographics (VR-1, VR-2) | Registered as **contextual visual resources**. Reasoning uses independently verified text and structured rules, **with no image interpretation at runtime**. The UI may link to the infographic or its parent page. Embedding or reproduction only with a source reference **and** where usage rights permit. The registry records title, source URL, applicable topic, application stage and display conditions | REQ-SRC-010 |
| YouTube videos (VID-1, VID-2) | **Excluded** from the text-retrieval and reasoning corpus. Verified titles, URLs and preparation stages may go in the registry and be shown as supplementary learning resources when contextually relevant. **Never treated as policy evidence** unless independently validated against an approved authoritative source. Videos don't expand the MVP | REQ-SRC-011, REQ-SCP-009 |

Registry location: `data/visual_resources.json` (D-022).

## 5. Policy nuances flagged for structured reasoning [APP p.21–22]

All are **AUTHORED-FACT (unverified)** and come from the project approach, not from a frozen
source. Each must be verified in Phase 2 before it is used as a fact, rule or benchmark label.

| Nuance | Paraphrase of claim to verify | Tier |
|---|---|---|
| HFE validity and timing | The HFE letter is valid for nine months from issue. A valid letter is needed to apply for a new flat. Changes to household details may affect eligibility or invalidate the letter | Core |
| Income assessment | The assessment period is 12 months, ending two months before the HFE application month. For employed persons, the average depends on months worked in that period, not necessarily on dividing by 12 | Core (documentation/follow-up only, D-013) |
| Household composition | The rules distinguish *applicants*, *occupiers* and the *core family nucleus*. The fiancé(e)-under-21 situation is addressed | Core |
| Non-selection consequences | Declining a BTO doesn't simply "make you a second-timer". The rules involve available units, non-selection counts and waivers, including a waiver when there are 10 or fewer flats to choose from | Limited |

**Architecture implication (APPROVED):** policies are not stored as bare paragraphs. Their
conditions, exceptions, effective dates and source references are structured metadata
wherever possible (REQ-ARC-006).
