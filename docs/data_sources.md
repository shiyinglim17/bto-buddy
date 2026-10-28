# Data Sources: Discovery, Scope, Rights, Acquisition and Processing

Current state of Dataset A's official sources, as of 2026-10-28.

**Where things live:**
- **Per-source records** (URLs, classification, hashes, timestamps):
  [`data/sources_manifest.json`](../data/sources_manifest.json).
- **Decisions:** D-044 to D-062 in [decisions.md](decisions.md). All are APPROVED (D-054
  and D-058 as revised).
- **Processing outputs (tracked, no source text):** `data/corpus/` (expected-section
  checklist, extraction report, fact-check report, corpus version), `data/policy_facts.jsonl`,
  `data/source_coverage.csv`, `data/visual_resources.json`.
- **Chronology:** [development_log.md](development_log.md).
- **Original source-discovery matrix:** [02 §3](project_context/02_policy_sources.md), kept as
  recorded. This document reconciles it against the approved scope (D-008, D-013, D-033)
  and against the live site at capture.

**Status:** 7 sources acquired manually and held privately: S01–S05 (HTML) and S07–S08
(PDF). Phase 2b processed them into 80 private L1 passages and **89 authored facts**
(`kb-2026-10-28.1`, freeze **candidate**), with the supported scope approved (D-061, §16) and scope boundaries in §17.

**Provenance tags:**
- *matrix* = recorded in the developer's matrix;
- *agent knowledge* = the coding agent's general knowledge. It is unverified and never used
  as a fact.

---

## 1. Classification and IDs

| Class | Meaning |
|---|---|
| **Essential** | Needed for a Core area, or the only source for a planned Limited area (REQ-SRC-013) |
| **Supporting** | Adds detail to an in-scope area. Acquired only with item-level approval |
| **Context only** | Explains the HFE ↔ grant/loan relationship, or serves as a link/redirect target. No calculation (REQ-SCP-004) |
| **Outside MVP** | Excluded tier, out-of-scope household (D-033) or income determination (D-013). It may be a redirect URL, but its content is never authored |
| **Pending** | Depends on an open question |

IDs are stable and never reused:
- `S##` is a document;
- `S##.x` is a section inside a document;
- `M##` is a media item.

The same IDs are the `source_id` values in the manifest.

---

## 2. Sources

### 2.1 Documents and media

The full URLs, matrix references and reasons are in the manifest.

| ID | Source | Class | Acquisition |
|---|---|---|---|
| S01 | Couples and Families (seed) | Essential | Manual rendered DOM |
| S02 | Application for an HFE Letter (seed) | Essential | Manual rendered DOM |
| S03 | Income Guidelines and Documents for HFE (seed) | Essential | Manual rendered DOM |
| S04 | Application for a New Flat (seed) | Essential | Manual rendered DOM |
| S05 | Priority Schemes | Essential (Limited area) | Manual rendered DOM |
| S06 | Modes of Sale | Supporting | Link only |
| S07 | HFE Employment Status Guide (PDF) | Essential (HFE documents) | Manual PDF download |
| S08 | HFE Income Declaration Guide (PDF) | Essential (HFE documents) | Manual PDF download |
| S09 | Income ceiling guide, extended families (PDF) | Outside (D-013, D-033) | Not acquired |
| ~~S10~~ | HFE FAQs (`/hdb-flat-portal/hfe/get-help`) | **Excluded from the source list (D-060)** | Never acquired or inspected: robots.txt disallows `/hdb-flat-portal`. Kept in the manifest's `excluded_sources` only |
| S11 | HFE step-by-step guide (mynicehome.gov.sg) | Context only | Link only. S02's text already covers its timing facts |
| S12 | Seniors | Outside (D-033) | Link only (redirect) |
| S13 | Citizen Top-Up | Outside: financing (D-046) | Link only (redirect) |
| S14 | Minimum occupation period | Outside: post-purchase | Link only (redirect) |
| S15 | Resale levy | Outside: financing/post-purchase (D-046) | Link only (redirect) |
| S16 | Integrated loan service (FI loans) | Context only | Link only |
| S17 | HDB Flat Portal (Singpass) | Outside | Never accessed (REQ-SRC-006) |
| M00 | Infographic: what the HFE letter is | Context only | Link only (no image download) |
| M01 | Infographic: applying for the HFE letter | Supporting | Link only. Its timing details are also in S02's text |
| M02 | Infographic: flat-buying journey | Supporting | Link only |
| M03, M04 | HFE Step 1 / Step 2 videos | Context only | Link only. `si=` stripped (D-049); never evidence (REQ-SRC-011) |

The matrix also mentions "subsidies, grants" with no URL. That is Context only, covered by
S02's HFE↔grant explanation. No grants page is acquired.

### 2.2 Sections that are authored vs not authored

| Parent | Authored (in scope) | Captured but never authored |
|---|---|---|
| S01 | Fiancé and fiancée; married couples (couple rows only; SC/SPR combinations); families with non-residents, **non-resident spouse rows only** (D-047); notes on fiancé(e) under 21 and no change of persons listed; core family nucleus; property ownership | Multi-generation families; orphaned siblings; non-resident parents or children; parent-with-child rows; income-ceiling tables (D-013); Fresh Start Housing Scheme; the SC+SPR premium (link to S13) |
| S02 | When to apply; How to apply (Step 1, Step 2, additional information); Validity and possible review; Income guidelines (summary that points to S03); Next steps (text only); the HFE ↔ grant/loan relationship (Context) | Integrated loan service detail (link to S16) |
| S03 | Income guidelines (assessment period, for documentation only); Documents | Any income calculation (D-013) |
| S04 | Application sections (sales launch, ballot, fees, valid HFE); Cancellation of flat application, including "financial forfeitures and consequences after cancellation" (holds the non-selection and waiver content) | Fresh Start Housing Scheme; application status |
| S05 | FT(PMC); FPPS; Family Care Scheme (Proximity); Family Care Scheme (Joint Balloting). These are Limited: identify and link, and ballot-chance wording never becomes probabilities | Third Child Priority Scheme; assistance scheme for second-timer divorced/widowed parents; Senior Priority Scheme; Tenants' Priority Scheme |
| S07, S08 | Employment categories and the documents to prepare (D-013) | Income computation |

### 2.3 Reconciliation with the matrix

| Item | Finding | Resolution |
|---|---|---|
| C-14 / Q-24 | Row 4 names the Application page but links the HFE page. The slip is in the original | S04 is Row 4's source (D-045) |
| FT(PMC), FPPS | The matrix places them on S01. The live S01 (updated 23 Aug 2026) no longer has them; they're on S05 | S05 promoted to Essential (D-044) |
| "Exceptions and waivers" | No URL in the matrix | Found inside S04's cancellation section (G-03 closed) |
| HFE timing in the infographic | The matrix recorded the Step-2 window and processing time from the image | Also present in S02's text, so text is the evidence (D-051 not triggered) |
| New on the live site | S02 has an "Income guidelines" accordion. S05 has an assistance scheme for second-timer parents. The PDF links now use `go.gov.sg` short links | Recorded above and in the manifest |
| Duplicate references | S02, S04 and S09 appear in two matrix rows each | One ID each; every ref is kept in `matrix_refs` |
| URL forms | `#fragment` and `?anchor=` are both used | `canonical_url` drops the anchor; `original_url` keeps it |

---

## 3. Source relationships

```
S01 Couples and Families ............ [accordions, nested tables]
 ├─ → S13 Citizen Top-Up, S12 Seniors, S14/S15 conditions after buying (?anchor=) [outside: links]
 └─ → S09 income-ceiling PDF ........ [outside]
S02 HFE letter ...................... [accordions; infographics M00–M02; videos M03–M04]
 ├─ → S03 Income guidelines and documents [child page]
 │     └─ → S07, S08 PDFs (go.gov.sg → file.go.gov.sg)
 ├─ → S11 mynicehome guide [external, link only]   → S16 FI loans [link only]
 ├─ → (S10 HFE FAQs: excluded, robots-disallowed, D-060) → S17 Flat Portal [never accessed]
S04 Application for a New Flat ...... [accordions; cancellation, ?anchor=cancellation]
 └─ → S05 Priority Schemes ......... [child page, 8 scheme accordions]
S06 Modes of Sale ................... [link only]
```

**Formats found:**

| Format | Where |
|---|---|
| Same-page anchors | S02 `#how-to-apply`; S04, S14, S15 and S16 use `?anchor=` |
| Accordions | All panels are already in the DOM: S01 has 5, S02 5, S04 5, S05 8; S03 has none |
| Nested tables | S01 |
| PDFs | S07, S08, S09 |
| Images | M00–M02 |
| Videos | M03, M04 |
| External hosts | file.go.gov.sg, mynicehome.gov.sg, YouTube |
| Restricted | S17; former S10 excluded (robots.txt, D-060) |

---

## 4. Policy dependencies and exceptions

| ID | Rule area (tier) | Source | Necessary exception or condition | If unavailable |
|---|---|---|---|---|
| P-01 | Who may apply as a couple (Core) | S01 | Fiancé(e) under 21 (S01 note) | Wrong preparation steps |
| P-02 | Application validity (Core) | S01, S02 | No change of listed persons; HFE review triggers | Change not flagged |
| P-03 | Valid HFE before applying (Core) | S02, S04 | Validity period; when to apply | Timing unanswerable |
| P-04 | HFE documents (Core, D-013) | S03, S07, S08 | Employment category | Evidence gap per category |
| P-05 | First-timer status (input to Limited) | S01, S04, S05 | Prior ownership/subsidy; private property | Limited priority area becomes link-only |
| P-06 | Household gate and citizenship combinations (Core) | S01 | Non-resident spouse rows (D-047); out-of-scope categories | Wrong conditions, or a wrong refusal |
| P-07 | FT(PMC), FPPS, FCS (Limited) | S05 | Scheme conditions | Identify and link only |
| P-08 | Cancellation and non-selection (Limited) | S04 | Waivers and fewer-flats conditions, inside the cancellation section | Area reduced (D-048) |
| P-09 | SC + SPR cost question (Outside) | S01 → S13 | Link only | No redirect |

---

## 5. MVP coverage (pre-authoring)

The post-authoring version, with fact IDs, goes in `data/source_coverage.csv`.

| MVP area (tier) | Sources | Status |
|---|---|---|
| First-timer couple household composition (Core) | S01 | Sources acquired; concepts present |
| Broad BTO application requirements (Core) | S04, S02, S01 | Acquired |
| HFE prerequisites, timing, documentation (Core) | S02, S03, S07, S08 | Acquired. Timing is in the text; per-employment documents are in the PDFs |
| Missing applicant information (Core) | Derived from the above | No separate source |
| First-timer and priority considerations (Limited) | S05 | Acquired |
| Application and non-selection consequences (Limited) | S04 | Acquired, including waiver content |
| HFE ↔ grant/loan relationship (Context) | S02 (M00 is a link) | Acquired |
| Excluded topics → redirect | S02, S06, S12–S16 | Links only |

Policy areas: 4 Core, 2 Limited, 1 Context, matching REQ-SCP-012. Keyword presence in the
audit is **not** verification; every fact is checked against its source at authoring.

---

## 6. Rights and access

### 6.1 Checks (2026-10-28)

| Check | Result |
|---|---|
| `www.hdb.gov.sg/robots.txt` | Read via a web-fetch tool; curl got HTTP 403. No rule matches S01–S06 or `/-/media/`. **`Disallow: /hdb-flat-portal`** matches S10. No crawl delay. No raw copy is held |
| HDB Terms of Use | **Read in full** on 2026-10-28. The developer captured it manually (`raw/rights/2026-10-28T134435Z_hdb_terms_of_use.html`, sha256 `99e1ae2a5e82…`); HDB's page date is 24 Jul 2026. The authored clause summary is in the manifest `R-HDB-WWW` record. Key points are in §6.2 |
| Bot protection | curl and headless Chromium with an honest user agent both get **403**. The block pages are kept privately as evidence |
| Copyright Act 2021 s 244 (secondary source; Statutes Online returned 403) | Allows copies made for computational data analysis, subject to: no other use; no supply to others except to verify results or for collaborative research; lawful access (not obtained by breaching terms or circumventing controls); a non-infringing source |
| s 187 | Contract terms restricting that exception are void |
| `file.go.gov.sg`, `mynicehome.gov.sg` robots/terms | Not checked. No automated access was used |

### 6.2 What the Terms of Use say, and what follows

These are authored paraphrases. The terms are contractual, and this is the project's own
reading, not legal advice.

| Clause | Effect on this project |
|---|---|
| **IP:** no copying, reuse, adaptation or transmission of site Materials "for commercial or any other purpose" without HDB's prior written permission. No research or personal-use carve-out | The contract alone would forbid even the local snapshots. They rely instead on **s 244**, and **s 187** voids contract terms to the extent they restrict that permitted use. Redistribution and LLM transmission aren't covered by s 244 either, so both stay prohibited, which is consistent with the clause |
| **Facts vs expression** | Copyright protects expression, not facts. Authored, independently worded facts (§8.2) don't reproduce Materials. Residual risk: the clause's "adapted / derivative work" wording is broad. Mitigated by the overlap check and disclosure |
| **Hyperlinks:** prior written permission is required before caching, linking or framing; linking counts as accepting the terms; HDB may object to or disable links | **Conflicts with REQ-ARC-009** (answers link to HDB pages). Proposed handling in **D-057**: links stay in the private, locally run prototype, are disclosed as a deployment condition, and a public deployment would need HDB's permission |
| **Duties:** no interference, unreasonable load, probing, or breaching security or authentication measures | Supports the decision not to get past the bot protection (D-055). Manual, one-page-at-a-time access complies |
| No clause on robots, crawling, scraping or AI | Nothing beyond the duties above |
| **Reliance:** Materials are general information only, may be incomplete, and must be verified by the user | Aligns with the app's disclaimer (REQ-PRB-010). The README and UI repeat that guidance isn't official advice |
| Terms change without notice | The version read is pinned by hash and page date in the manifest |
| Open Data Licence covers only published open datasets | **Not** applicable to these pages. No open-data licence is claimed |
| Privacy section (HDB's handling of its users' data) | Not applicable: the app uses fictional profiles only (REQ-PRIV-001) |

| Use | Position |
|---|---|
| Automated capture | **Not used.** Getting past bot protection would undermine lawful access, so capture is manual (D-055) |
| Local raw/processed copies (Git-ignored) | Lawful manual access; analysis only; s 244, with s 187 overriding the terms' copying ban. **Defensible, with the residual contractual risk disclosed** |
| Committing copies or copied passages to GitHub | **Not permitted** (outside s 244(2)(c); REQ-LIC-010/011) |
| Sending source text to an LLM provider (runtime, evaluation or coding agent) | **Not permitted** ("supply" to a third party). Only authored facts, rules and fictional profiles are sent (D-054) |
| Authored facts, URLs, titles, short headings, hashes | Tracked, after rights review (§8.2) |
| robots.txt | Treated as an access signal, **not** a licence. Nothing is described as licensed (REQ-LIC-012) |

### 6.3 How the acquisition approach meets provenance and licensing requirements

| Requirement / condition | How it is met |
|---|---|
| REQ-SRC-006: approved pages only; no crawling, link-following or transactional services | Only the sources classified in §2 were captured, one by one, by the developer. Links were never followed automatically. S10 (robots-disallowed) and S17 (Singpass portal) were not accessed |
| REQ-LIC-001 / REQ-LIC-014: robots.txt | HDB robots.txt checked. Every captured path is allowed. The only disallowed path in scope (S10) was skipped. No automated client was used on the other hosts |
| s 244(2)(d): lawful access | Normal public browser access. Bot protection was **not** bypassed: automated attempts stopped at the first 403, and no spoofed client was used (D-055). The tooling for automated capture was removed (D-056) |
| s 244(2)(a)–(b): copy made for, and used only for, computational analysis | Snapshots are used only for the local audit, passage extraction and fact verification |
| s 244(2)(c): no supply to others | Snapshots and passages are Git-ignored (REQ-LIC-010/011) and excluded from Docker (`.dockerignore`). Source text is never sent to an LLM provider, including the coding agent (D-054). Scripts print structure only |
| s 244(2)(e): non-infringing source | Official HDB pages and HDB-linked government PDFs only |
| REQ-SRC-002 / REQ-LIC-016: provenance | Each acquired file has `retrieved_at` (UTC creation time; for PDFs this matches the browser download record), `raw_sha256`, `text_sha256`, size, private path, requested and final URL, and method in the manifest. It is regenerated by `snapshots.py register` |
| REQ-SRC-015 / D-021: temporal metadata | The page "last updated" date or PDF metadata date is recorded, never presented as an effective date |
| REQ-LIC-012 / REQ-LIC-015: no licence claim; review of tracked data | Tracked files hold authored text, URLs, titles, short headings and hashes only. The anonymity and secret scans run before each suggested push |
| HDB Terms of Use | Read and pinned (§6.2). The copying ban is handled under s 244/s 187. The linking clause is handled by D-057 |
| Still provisional | Statute read from a secondary source. No written permission from HDB has been sought (optional; D-057) |

---

## 7. Acquisition method and completeness

**Capture method (D-055):**
1. The developer opens each page in a normal browser, not logged in.
2. Runs a read-only console check of the accordions.
3. Copies `document.documentElement.outerHTML`. This takes the live DOM, not the image files.
   "Save as complete" is avoided because it would also save the infographics.
4. Saves the copy to `data/private_corpus/raw/<source_id>/<UTC>_<name>.html`.

PDFs are downloaded in the browser, never re-saved. Their final URLs come from the
download record. The UTC prefix is the file's creation time; for the PDFs it matches
Chrome's download timestamp to within 2 s.

Accordions open exclusively, but every panel is present in the DOM in the default state
(console check, confirmed by the offline audit). So **one default-state copy per page is
complete**.

**Offline tooling:** stdlib only. Output is structure only, never source text.

| Command | Purpose |
|---|---|
| `python3 -I scripts/snapshots.py audit` | Headings, accordion labels, expected-concept presence, page-data coverage, PDF page/date/text-layer facts |
| `python3 -I scripts/snapshots.py register` | Writes `retrieved_at`, `raw_sha256`, `text_sha256`, size and private path into the manifest |

**Results:**

| Source | Captured (UTC) | sha256 (first 12) | Page date | Page data rendered | Concepts |
|---|---|---|---|---|---|
| S01 | 2026-10-28T09:18:06Z | `f0d477655219` | 23 Aug 2026 | 355/362 | 11/13 (FT(PMC)/FPPS moved to S05) |
| S02 | 2026-10-28T09:30:08Z | `e2e44274bad8` | **28 Oct 2026** | 98/106 | 13/14 ("what is HFE" is image-only) |
| S03 | 2026-10-28T09:30:57Z | `0e8793a9221b` | 24 Jul 2026 | 47/53 | 7/8 |
| S04 | 2026-10-28T09:38:29Z | `4397707f5878` | 22 Oct 2026 | 69/77 | 9/10 (waiver content present) |
| S05 | 2026-10-28T10:29:58Z | `595eb09b0822` | 23 Oct 2026 | 126/134 | 9/9 |
| S07 | 2026-10-28T10:30:40Z | `891c00138e72` | PDF metadata 19 Dec 2025 | n/a. About 2 pages, text layer | — |
| S08 | 2026-10-28T10:30:35Z | `918bfebc82eb` | PDF metadata 19 Dec 2025 | n/a. About 4 pages, text layer | — |

Every page-data item missing from the DOM is metadata: page or meta descriptions, and the
descriptions of link cards to other pages. No policy content is unrendered.

S02 was updated on capture day, and its HFE infographic file is dated 27 Oct 2026. Facts come
from these snapshots, never from the matrix's earlier paraphrases.

---

## 8. Corpus design

### 8.1 Layers

| Layer | Content | Path | Git |
|---|---|---|---|
| L0 raw | HTML and PDF snapshots; rights-check evidence | `data/private_corpus/raw/` | Ignored |
| L1 processed | Structured passages (heading path, text, tables, links) and any local index | `data/private_corpus/processed/` | Ignored |
| L2 authored KB | `policy_facts.jsonl` (paraphrased, fact IDs, source pointers, **no quotes**); `policy_rules.yaml` | `data/` | Tracked after rights review |
| L3 metadata | `sources_manifest.json`, `source_coverage.csv`, `visual_resources.json` | `data/` | Tracked |

The app, BM25 index, Docker image and evaluation use **only L2 and L3** (D-005,
REQ-DAT-011/012). Each claim cites a fact ID. The fact resolves to an official URL and section
through the manifest (D-006), so reviewers check it against HDB's live page, not a copy.

### 8.2 Rights review before a fact is tracked (D-054, approved as revised)

1. **Write independently worded statements**, one condition each. Only proper names, numbers,
   dates and durations are kept as-is.
2. **Run the local overlap check** (`python3 -I scripts/corpus.py facts`): it flags any run of
   8+ consecutive words shared with the whole L1 source, and the fact is reworded.
3. **Read it manually**, then set `rights_review` to `overlap_checked` (author) and later
   `cleared` (developer, REQ-LIC-015).
4. **Run the anonymity and secret scans** before suggesting a commit.

Under revised D-054 the coding agent may read L0/L1 for the approved in-scope sections (the
developer turned off model training). Source text never enters tracked files or reports.

### 8.3 Manifest schema (D-053, PROPOSED)

Top level: `manifest_version`, `rights_records[]`, `sources[]`.

| `rights_records[]` fields | `sources[]` fields |
|---|---|
| `rights_id`, `host`, `terms_url`, `terms_checked_at`, `terms_sha256`, `terms_summary` (authored), `robots_url`, `robots_checked_at`, `robots_sha256`, `robots_relevant_rules`, `robots_permits_planned_paths`, `legal_basis`, `redistribution`, `llm_transmission`, `notes` | `source_id`, `record_kind`, `title`, `original_url`, `canonical_url`, `host`, `parent_source_id`, `link_relation`, `content_format`, `matrix_refs`, `policy_areas` (architecture §5 `Topic`), `mvp_class`, `mvp_class_reason`, `page_last_updated`, `effective_date`, `effective_date_status` (`stated` / `page_last_updated_only` / `pdf_metadata_date_only` / `unknown`), `acquisition` {`method`, `requested_url`, `final_url`, `retrieved_at`, `retrieved_at_basis`, `raw_sha256`, `text_sha256`, `byte_size`, `private_path`}, `rights_id`, `permission_status`, `review` |

- **`text_sha256`** hashes the normalised page text. A future re-capture can then tell real
  content change apart from page noise.
- **Section-level records** (`S01.a`, …) and **extraction counts** are added when L1 is
  built.
- **`data/source_coverage.csv` columns:** `area_tier, sub_area, rule_or_fact_ids,
  essential_source_ids, supporting_source_ids, exceptions_required, exceptions_verified,
  coverage_status, evidence_gap_kind, notes`.

---

## 9. Reviewer reproducibility

| Reviewer action | Needs | Doesn't need |
|---|---|---|
| Run the app (Docker or `uv`) | Tracked L2/L3; an LLM key for live answers | L0/L1, network access to HDB |
| Re-score the evaluation | Saved predictions and labels | API key |
| Check a cited fact | The fact's URL and section in a browser | L0 |

**Not claimed:**
- Re-capturing pages later does **not** reproduce this corpus. HDB pages change without
  versions. Re-running `snapshots.py register` on a new capture only *detects* drift against
  the recorded hashes (REQ-LIC-016).
- The README states the policy period as "HDB sources retrieved 28 Oct 2026" (D-021). It
  never claims effective dates the sources don't give.

---

## 10. Open gaps and risks

| ID | Item | Effect | Next step |
|---|---|---|---|
| ~~G-04~~ | HFE FAQ sub-links (S10) | **Closed by exclusion (D-060):** the page is robots-disallowed, so it is not a source. Whatever HFE exceptions it holds are unrepresented | Stated in §17; no further action |
| ~~G-05~~ | First-timer definition | **Closed (Phase 2b):** S01 defines second-timer via a previous housing subsidy (HH-SUBSIDY-001); FT(PMC) adds a never-owned test (PRI-FTPMC-001) | Developer verifies both (checklist C-03, C-15) |
| G-06 | No effective dates; only page "last updated" and PDF metadata | Temporal validity | Retrieval-date statement in the UI and README |
| G-07 | Conditions may vary by flat classification or sales exercise (*agent knowledge*) | Application and non-selection facts | Record conditions in `applies_to`; never generalise |
| G-11 | No grants redirect page | Excluded-topic redirect | Redirect to S02 |
| G-15 | S02 changed on capture day | Currency | Facts from the snapshot; drift check before submission |
| R-ToU | Terms read (2026-10-28). Copying ban (handled under s 244/s 187) and linking-permission clause | Residual contractual risk | D-057; disclose in the README; optionally ask HDB for written permission |
| R-evidence | The ToU 403 block page (sha256 `df0a74…c9d6`) was overwritten by the manual copy | That piece of evidence is lost; its hash stays in §6.1 | None needed |
| ~~R-dates~~ | S01 and S05 files modified 2–8 min after creation | **Closed:** developer confirmed on 2026-10-29 that neither was edited after pasting | — |
| G-16 | Sales-exercise FAQs (linked from S04) not in the approved list | Possible application-procedure detail missed | Link only; capture needs separate approval |
| G-17 | **No approved source lists documents per employment status.** S07 defines statuses, S08 explains multi-job declarations, S03 says HDB asks for documents case by case after Myinfo | Core HFE-documents area: per-status document checklists cannot be given | Outside the KB (D-061): state the gap and HDB's case-by-case process (DOC-MYINFO-001). Never invent lists. The only other candidate (S10) is excluded (D-060) |
| U-01 | Does an engaged couple marrying after HFE approval count as a "marital status" change needing action? Not stated | HFE-HOUSEHOLD-002 applicability | Outside the KB (D-061): reported as unconfirmed, with a redirect (§17) |
| U-02 | FT(PMC) criteria name married couples; engaged couples not mentioned | PRI-FTPMC-* applicability | Outside the KB (D-061): reported as unconfirmed, with a redirect (§17) |
| U-03 | S01's non-resident section speaks of a spouse; an engaged SC + non-resident partner is not addressed | D-047 coverage | Outside the KB (D-061): reported as unconfirmed, with a redirect (§17) |
| M-01 | Manifest M00–M02 have null `original_url`/`canonical_url`; the S02 capture shows their image paths | Visual-resource provenance | Not changed silently: `visual_resources.json` records the page URL plus the observed `media_url`; the developer approves filling the manifest |

---

## 11. Requirement traceability

| Section | Requirements |
|---|---|
| §2 sources and scope | REQ-SRC-001, REQ-SRC-005, REQ-SRC-014, REQ-SCP-001, REQ-SCP-007, REQ-SCP-012, D-007, D-008, D-013, D-033 |
| §3–§4 relationships and dependencies | REQ-SRC-003, REQ-SRC-005, REQ-SRC-013, REQ-ARC-006, REQ-DAT-014, REQ-EVL-034 |
| §5 coverage | REQ-SRC-013, REQ-SCP-002 to 005, REQ-SCP-008, REQ-SCP-013 |
| §6 rights | REQ-LIC-001, REQ-LIC-012 to 014, REQ-DAT-001, D-024 |
| §7 acquisition | REQ-SRC-002, REQ-SRC-006 to 012, REQ-LIC-016 |
| §8 corpus | REQ-DAT-010 to 013, REQ-DAT-019, REQ-LIC-010/011/015, D-005, D-006, D-022 |
| §9 reproducibility | REQ-DAT-021, REQ-DAT-022, REQ-NFR-001, REQ-SCP-011, D-021 |
| §12 processing and completeness | REQ-SRC-003, REQ-SRC-007, REQ-SRC-009, REQ-SRC-010, REQ-SRC-012, D-052, D-059 |
| §13 coverage and review | REQ-SRC-013, REQ-SRC-015, REQ-SCP-002 to 005, REQ-DAT-010, D-058 |
| §14 rights review | REQ-LIC-010, REQ-LIC-011, REQ-LIC-015, REQ-LIC-017, D-054, D-057 |
| §15 freeze | REQ-DAT-011, REQ-DAT-012, REQ-DAT-013, REQ-DAT-020, REQ-LIC-016, D-005, D-006, D-021 |

---

## 12. Offline processing and extraction completeness (Phase 2b)

**Pipeline** (`scripts/corpus.py`, stdlib only, D-059 approved; never used by `src/` or
Docker):

| Command | Input → output | Tracked output |
|---|---|---|
| `python3 -I scripts/snapshots.py register` | L0 → manifest hashes (unchanged since capture) | `sources_manifest.json` |
| `python3 -I scripts/corpus.py extract` | L0 HTML → `private_corpus/processed/Sxx.json`: sections, blocks (headings, paragraphs, lists with depth, tables with spans and nesting, footnotes, media), links, passages | — (private) |
| `python3 -I scripts/corpus.py validate` | L1 + L0 + `data/corpus/expected_sections.json` → completeness checks | `data/corpus/extraction_report.json` (counts, IDs, short heading labels) |
| `python3 -I scripts/corpus.py facts` | facts + manifest + L1 → integrity and overlap checks | `data/corpus/fact_check_report.json` |
| `python3 -I scripts/corpus.py freeze` | everything above → version record | `data/corpus/corpus_version.json` |

Extraction refuses to run if a raw file's hash differs from the manifest. Two full runs gave
byte-identical outputs.

**Passages.** There is one passage per section, so a condition always travels with the
heading that names its applicant group (REQ-SRC-003). Tables are never split. Sub-headings
keep their accordion parent: S01's "Eligibility conditions" appears under three household
types as S01.a.2, S01.b.2 and S01.e.4. Each passage carries a source URL with HDB's
`?anchor=` (inherited from the nearest ancestor), the retrieval time, the page date and a
text hash.

**Completeness results** (from `extraction_report.json`):

| Check | S01 | S02 | S03 | S04 | S05 | Method |
|---|---|---|---|---|---|---|
| Accordions extracted / raw toggles | 5/5 | 5/5 | 0/0 | 5/5 | 8/8 | Independent regex count on raw HTML |
| Tables extracted / raw | 20/20 | 7/7 | 3/3 | 4/4 | 4/4 | Includes nested and list-embedded tables |
| Expected sections missing / unexpected | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | Checklist from §2.2 and the matrix |
| Page headings not accounted for | 0 | 0 | 0 | 0 | 0 | Each heading is a section, inside table text, or site chrome |
| Page-data sentences in extracted blocks | 527/542 | 115/125 | 47/59 | 80/88 | 138/148 | Sitecore `__NEXT_DATA__` vs L1 |
| …of the remainder: site chrome / unrendered metadata | 12/3 | 6/4 | 9/3 | 6/2 | 8/2 | **Rendered content missing from L1: 0 on every page** |
| Merged cells flagged for manual check | 5 tables | 0 | 2 | 3 | 3 | `colspan`/`rowspan` kept in `spans` |
| Duplicate passages | 0 | 1 pair* | 0 | 0 | 0 | *S02 Step 1/Step 2 are video-only, so their passages match |
| Links unresolved | 0 | 0 | 0 | 0 | 0 | Resolved to the manifest or classified (`link_dependencies`) |

**What this does and does not show:**
- **Single snapshot per page.** No default-versus-expanded comparison is possible, and that
  is recorded as a limitation for every source. The mitigation is evidence-based: every
  accordion panel was in the DOM while collapsed (`aria-expanded="false"`), and every
  rendered page-data sentence is in L1.
- Successful parsing and matching counts are **not** taken as policy completeness. Policy
  coverage is assessed separately (§13).
- **PDFs (S07, S08):** there is no text extraction (D-052 approved, option (a): no parser dependency).
  Every page was reviewed manually (S07 2 pages, S08 4 pages), and facts cite pages in
  `source.locator`. A second-pass page check was done on 2026-10-29. **Finding:** neither PDF lists documents per employment status (G-17).
  That was the reason they were acquired (D-044).
- **Media-only sections:** S02 "Step 1" and "Step 2" hold only the M03/M04 videos. The
  infographics M00–M02 are recorded as media blocks; their timing content is also in S02's
  text.

## 13. Policy coverage and manual review checklist

The full matrix is in [`data/source_coverage.csv`](../data/source_coverage.csv): 36 rows,
mapping every fact to its sub-area, sources, applicability, exceptions, effective-date
status, extraction status and review status. Summary:

| Area (tier) | Facts | Status | Gap kind |
|---|---|---|---|
| Household composition (Core) | 21 | Covered | SPR-only couples derived, not stated (insufficient evidence); engaged SC + non-resident partner not addressed (U-03) |
| Application requirements (Core) | 11 | Covered | Sales-exercise FAQs not acquired (G-16) |
| HFE process (Core) | 14 | Covered | U-01 unconfirmed, outside the KB; HFE FAQs excluded (D-060) |
| HFE documents (Core) | 15 | **Partial** | **Per-status document lists: source coverage gap (G-17)** |
| Missing applicant information (Core) | — | Derived | Defined in the rules phase |
| Priority considerations (Limited) | 15 | Covered | FT(PMC) for engaged couples unconfirmed (U-02) |
| Application and non-selection consequences (Limited) | 8 | Covered | D-048's waiver condition met; merged-cell inference to confirm |
| HFE ↔ grant/loan (Context) | 5 | Covered | Explain and link only |
| Excluded areas | 0 | Redirect | Income ceilings and computation, grant amounts, premiums and levy, post-purchase, ballot odds, other households |

**Temporal gap (all sources):** no source states an effective date. Facts record
`retrieved_at` and `page_last_updated`. The supported policy period is "HDB sources retrieved
28 Oct 2026" (D-021). S02 was updated on capture day (G-15).

**Manual review checklist (developer, against the live official pages).** 47 facts are
marked `critical` and are held back at runtime until they are set to `verified` (D-058).
Check each fact's numbers, conditions and applicant group:

| # | Source / section | Facts | Check especially |
|---|---|---|---|
| C-01 | S01 `?anchor=fs` Fiancé and fiancée: core family nucleus | HH-COUPLE-001 | Engaged couple as a nucleus |
| C-02 | S01 `?anchor=fs` Eligibility conditions (new-flat column) | HH-CIT-001, HH-AGE-001 | SC + SC/SPR; age 21 (merged cell spans both columns) |
| C-03 | S01 `?anchor=fs` Eligibility conditions: property and subsidy rows | HH-PROP-001, HH-SUBSIDY-001, HH-SUBSIDY-002 | 30-month wait-out; subsidy list; two-subsidy bar |
| C-04 | S01 `?anchor=fs` Solemnisation; below 21; no change of persons | HH-MARRY-001, HH-AGE-002, HH-CHANGE-001 | 3 months; core-occupier-only; break-up cancels |
| C-05 | S01 `?anchor=pa` Married couples | HH-COUPLE-002 | Nucleus wording |
| C-06 | S01 `?anchor=nc-families` Non-resident spouse and table | HH-NONRES-001 to 003 | 2-room Flexi only; age 35; pass at HFE and application; renewal by key collection |
| C-07 | S02 When to apply | HFE-TIME-001 | Up to one month; longer around sales exercises |
| C-08 | S02 `?anchor=how-to-apply` Additional information | HFE-SINGPASS-001, HFE-STEPS-001/002 | 30 calendar days; different calendar month means updating details |
| C-09 | S02 `?anchor=review-HFE` Validity and review | HFE-VALID-001/002, HFE-RENEW-001, HFE-REVIEW-001, HFE-HOUSEHOLD-001/002 | 9 months; expiry after application; 30-day renewal; change procedure |
| C-10 | S02 intro; S04 intro | HFE-APPLY-001, APP-HFE-001, APP-FEE-001, APP-BALLOT-001 | Free, online only; $10 non-refundable fee |
| C-11 | S04 `?anchor=changes-to-flat-application` | APP-CHANGE-001 to 003 | During vs after the sales exercise (merged header cells) |
| C-12 | S03 Income guidelines; Documents | DOC-PERIOD-001, DOC-MYINFO-001 | 12 months ending 2 months before; worked example |
| C-13 | S07 pages 1–2 | DOC-STATUS-001 | Six statuses |
| C-14 | S04 `?anchor=cancellation` Forfeitures table | NS-CANCEL-001/002, NS-QUEUE-001, NS-COUNT-001, NS-WAIVE-001, NS-FT-001, NS-BOOKED-001 | Waiver 10 BTO / 5 SBF; 1-year consequences; **the consequences cell spans the two post-booking rows (rowspan)**; 5% |
| C-15 | S05 FT(PMC), FPPS, general | PRI-FT-001, PRI-GEN-001/002, PRI-FTPMC-001/003, PRI-FPPS-001 | Age 40; 5-year rule; 3 ballot chances; child aged 18 or below |
| C-16 | S05 `?anchor=fcs-proximity` | PRI-FCS-002 | 4 km; SC/SPR condition |

**Uncertain interpretations to decide:** U-01 to U-03 (§10). **Not authored, by design:**
income-ceiling values, income computation and components, grant amounts, the $10,000 SC+SPR
premium and the $15,000 non-resident amount, resale levy, MOP detail, other priority schemes,
and other household types.

## 14. Independent-authorship and rights review of the facts

- Every statement was written fresh from the L1 passage or PDF page, one rule per fact,
  with conditions in `applies_to` and exceptions linked by `fact_id`.
- **Overlap check:** for HTML sources, each fact's statement and exception text is compared
  with the **whole** L1 source. The first draft had 12 facts at or above 8 shared words,
  mostly fixed terms of art such as pass names and stage names. They were reworded and
  re-checked. **The final maximum shared run is 7 words, with 0 flags.**
- PDF facts (S07, S08) were compared manually against the pages, because no L1 text exists
  (D-052).
- All 89 facts are `rights_review: overlap_checked`. Developer clearance (`cleared`) is
  still outstanding (REQ-LIC-015).
- **Not claimed:**
  - The overlap check does not establish legal compliance.
  - Turning content into JSON does not grant redistribution rights.
  - Even paraphrased facts reproduce HDB's *information*. The project relies on facts not
    being protected expression, plus s 244 for the private copies, and discloses the Terms
    of Use clauses (D-057).
- Facts contain no quotations, no private paths (a test enforces this) and no personal data.

## 15. Freeze, reproducibility and versions

- **`data/corpus/corpus_version.json`** records the version, the policy period, the
  extractor version, per-source retrieval times, raw and text hashes, page dates, L1 passage
  counts and fact counts, fact counts by topic, tier, validation and rights status, and the
  SHA-256 of every tracked KB file.
  - Status: **candidate**, pending the developer's approval of corpus and scope.
  - Version: `kb-2026-10-28.1`, extractor `1.0.0`.
- **Reviewer path without the private corpus:**
  - `bto_buddy.policy.load_kb()` loads `policy_facts.jsonl` and `sources_manifest.json`,
    validates every fact (Pydantic) and resolves each one to a citable manifest source and
    official URL (`tests/test_policy_kb.py`).
  - The Docker image copies only these L2/L3 files (`BTO_BUDDY_DATA_DIR`).
- **Same KB for app and evaluation:** both read `policy_facts.jsonl` through `load_kb()`.
  The private corpus is used only for provenance and auditing, never as a runtime source
  (D-050).
- **Tests:** `tests/test_corpus.py` uses an invented HTML fixture covering nested
  accordions, a repeated sub-heading under two parents, a merged cell, a nested table, a
  nested list, footnotes, same-page anchors, PDF and media links, site chrome, duplicates,
  missing and unexpected sections, broken references and copied wording.

## 16. Recommended supported scope (for approval)

Keep the approved MVP (D-008) with these evidence-based narrowings:

1. **HFE documents (Core):** support employment-status selection, the assessment period,
   multi-job declaration, Myinfo, and upload and translation rules. **Do not** give
   per-status document checklists (G-17). Answer such questions with HDB's case-by-case
   process and an evidence gap. (S10 is excluded, D-060, so this gap cannot be closed from
   the approved sources.)
2. **Household composition (Core):**
   - Full support for engaged or married SC + SC/SPR couples, and for **married** SC +
     non-resident spouse couples (new 2-room Flexi only).
   - Engaged SC + non-resident partners and SPR-only couples get an evidence gap plus a
     redirect (U-03, derived rule).
3. **Priority (Limited):** FT(PMC), FPPS and FCS (Proximity, Joint Balloting) are identified
   and their conditions explained. FT(PMC) for engaged couples is "unconfirmed" (U-02).
   Ballot-chance counts are never turned into odds.
4. **Non-selection (Limited):** supported, including the waiver and first-timer
   consequences, once checklist C-14 is verified.
5. **Before held-out evaluation:**
   - every critical fact used by benchmark labels must be `verified` (D-058);
   - ~~the developer confirms R-dates~~ (confirmed 2026-10-29).

**Approved (D-061, 2026-10-29)** as written above. Unconfirmed items stay unconfirmed and
outside the knowledge base (§17).

## 17. Scope boundaries and evidence gaps (D-060, D-061)

This section gives an honest account of what BTO Buddy's knowledge base does **not**
support, and why. In every case below there is **no authored fact**. The app must report the
item as unconfirmed or as an evidence gap and point to the official source. It must not
decide it.

**A. Content intentionally excluded because of data-access policy**

| Item | Why | What is lost | How the app responds |
|---|---|---|---|
| HFE FAQs, former S10 (`/hdb-flat-portal/hfe/get-help`) and its sub-pages | HDB's robots.txt disallows `/hdb-flat-portal`. The developer removed the page from the source list rather than capture or inspect it (D-060), consistent with the lawful-access position (§6) | Any HFE exceptions, edge cases or document lists those pages contain. This is the most likely place for answers to G-17 and U-01, so those gaps are **caused or deepened** by the exclusion | Links on S02–S04 are recorded as `excluded_by_policy`, never followed or cited. The app points users to the S02 page, which links to the FAQs on HDB's site |
| HDB Flat Portal (S17) | Transactional, behind Singpass (REQ-SRC-006) | Application-status detail | Redirect only |

**B. Evidence gaps inside the supported scope (no approved source states the answer)**

| ID | Question | What the sources say | Response |
|---|---|---|---|
| G-17 | Which documents should each employment status prepare? | S03: HDB retrieves Myinfo data and asks for documents case by case. S07 defines the statuses. S08 covers multi-job declarations | Give the status definitions and the process facts. Say the per-status list is not available. Redirect to S03 |
| U-01 | Does an engaged couple marrying after the HFE letter is approved need to act? | S02 lists "marital status" among changes that need action, but doesn't say whether that covers a planned marriage | "Unconfirmed". Redirect to S02 and MyRequest@HDB |
| U-02 | Can an engaged couple qualify for FT(PMC)? | S05 names married couples (and families with children) only | "Unconfirmed; HDB assesses FT(PMC) after the flat application" (PRI-FTPMC-002). Redirect to S05 |
| U-03 | Can an engaged SC with a non-resident partner buy a new flat before marrying? | S01's non-resident section covers spouses only; the fiancé/fiancée scheme requires an SC or SPR partner | Evidence gap. Redirect to S01 and HDB's write-to-us channel |
| — | SPR-only couple and a new flat | Derived from the stated rule that the new-flat applicant must be an SC (HH-CIT-001). There is no separate statement | State the SC requirement. Resale routes are Other housing (Excluded) |
| — | Effective dates | None stated; page dates only | Policy period "HDB sources retrieved 28 Oct 2026" |

**C. Captured but excluded by the approved scope (D-008, D-013, D-033, D-046)**

These include:
- income-ceiling values, income computation and income components;
- grant amounts and grant eligibility;
- the $10,000 SC+SPR premium, the Citizen Top-Up and the $15,000 non-resident additional
  amount;
- the resale levy;
- MOP and other post-purchase conditions (beyond noting that they exist);
- ballot probabilities;
- priority schemes other than FT(PMC), FPPS and FCS;
- household types other than first-timer couples;
- resale flats.

The coverage gate redirects all of these to the official page named in
`data/source_coverage.csv`.

**Machine-readable form:** these items are the rows of `data/source_coverage.csv` whose
`coverage_status` is `unconfirmed`, `gap`, `excluded_by_policy` or `excluded_redirect`. The
rules phase (Dataset B) will use them to generate evidence gaps and redirects.


## 18. Verification of the policy-critical facts (checklist C-01 to C-16)

**Method** (D-058 as revised, approved). For each fact, `scripts/corpus.py verify` checks
that every number in the statement and every authored term anchor (at most 6 words) occurs
in the fact's **cited** L1 section of the hash-pinned 2026-10-28 snapshot. I then re-read
the section for conditions, applicant group and exceptions. The anchors and notes are in
[`data/corpus/critical_fact_review.json`](../data/corpus/critical_fact_review.json), and
the results are in `data/corpus/fact_verification.json`. PDF facts (S07, S08) are checked
manually page by page (D-052).

**This is not a check of the live pages**: HDB blocks automated access, and G-15 drift is
possible. The developer should spot-check the live pages before submission.

**Result:** all 47 critical facts, plus 4 non-critical facts cited by rules (PRI-FTPMC-002,
DOC-MULTIJOB-001/002, HH-OTHER-001), pass. That makes 51 `verified`, with 0 failures and 0
critical facts left unreviewed.

**Corrections made before verifying:**

| Fact | Problem found | Fix |
|---|---|---|
| HH-SUBSIDY-002 | Said "a person who has taken two subsidies". The source says "you and/or any core members", without saying how subsidies are counted | Keeps the source's scope; states that the counting basis is unstated (I-09) |
| HH-COUPLE-002 | Said "with or without children". S01 lists "you, your spouse and child(ren)" | The childless reading is now attributed to S05's FT(PMC) criteria, not to S01 |
| HFE-APPLY-001 | "Free" and "online only" were cited to the wrong section | Moved to S02 *When to apply › Additional notes* |

## 19. Policy rule registry (Dataset B, D-062 approved)

[`data/policy_rules.yaml`](../data/policy_rules.yaml), version `rules-2026-10-29.1`:
24 rules, each citing only `verified` facts and listing their official URLs.
- **Interpreter and validator:** `bto_buddy.policy` (`evaluate_rules`, `validate_registry`).
- **Tests:** `tests/test_rules.py` (62 cases: operators, three-valued logic, the age 20/21,
  35 and 40/41 boundaries, HFE expiry at 31/30/0/−1 days, month-end clamping, missing
  fields, exceptions that can't be checked, and validator mutations).

| Rule | Topic | Kind | Basis | Human review |
|---|---|---|---|---|
| R-APP-001 HFE letter before applying | application, HFE | preparation | source | no |
| R-APP-002 fee and ballot | application | preparation | source | no |
| R-APP-003 keep household and finances unchanged | application | caution | source | no |
| R-HFE-001 plan the two steps | HFE | preparation | source | no |
| R-HFE-002 processing time | HFE | preparation | source | no |
| R-HFE-003 letter close to expiry | HFE | caution | **interpretation** (I-02, I-03) | yes |
| R-HFE-004 letter appears expired | HFE | caution | **interpretation** (I-02) | yes |
| R-HFE-005 changes after approval (U-01 exception for engaged couples) | HFE | caution | source | engaged: yes |
| R-HH-001 engaged: marriage, no change of persons | household | preparation | source | no |
| R-HH-002 engaged partner under 21 | household | preparation | source | no |
| R-HH-003 married partner under 21 | household | caution | source | yes |
| R-HH-004 two SPR partners | household | caution | source | yes |
| R-HH-005 married SC + non-resident spouse (age-35 and child exceptions) | household | preparation | source | if an exception applies |
| R-GAP-U03 engaged SC + non-resident partner | household | **evidence gap** | interpretation | yes |
| R-HH-006 private residential property | household | caution | source | yes |
| R-HH-007 a partner took a housing subsidy | household, priority | caution | **interpretation** (I-08, I-09) | yes |
| R-DOC-001 employment status and documents (G-17 stated) | HFE documents | preparation | source | no |
| R-DOC-002 more than one job | HFE documents | preparation | source | no |
| R-PRI-001 how priority schemes work | priority | preparation | source | no |
| R-PRI-002 FT(PMC) may apply | priority | preparation | **interpretation** (I-01, I-08) | yes |
| R-PRI-003 FPPS may apply | priority | preparation | source | yes (child details not captured) |
| R-GAP-U02 engaged couples and married-couple criteria (U-02, U-04) | priority | **evidence gap** | interpretation | yes |
| R-NS-001 booking when invited, and the waiver | non-selection | caution | source | no |
| R-NS-002 cancelling | non-selection | caution | source | no |

Every rule's `effective` scope is "as published at retrieval (2026-10-28); no stated
effective date". The validator rejects any rule that claims dates its facts don't state.

**Incomplete source information, identified before implementation.** No direct
contradictions were found between the sources. Each item below is either handled as an
interpretation (always routed to human review) or stated as a limitation:

| ID | Item | Rule handling |
|---|---|---|
| I-01 | FT(PMC): whose age counts towards "married couples aged 40 and below"? | R-PRI-002 always reviewed; flagged if either partner is over 40 |
| I-02 | HFE "valid for 9 months from the date of issue": the month-end convention is unstated | Issue date + 9 calendar months, clamped to month end; R-HFE-003/004 reviewed |
| I-03 | "Expiring in the next 30 days": inclusive or not? | Treated as 0–30 days inclusive; reviewed |
| I-04 | 30-calendar-day window *and* a same-month preference for Steps 1 and 2 | Complementary, not contradictory: both are stated in R-HFE-001 |
| I-05 | The date at which ages 21 and 35 are assessed is unstated | Age taken as given; recorded as a limitation |
| I-08 | The profile's `prior_flat_or_subsidy` is narrower than S01's subsidy list and FT(PMC)'s "never owned or sold a residential property" | R-HH-007, R-PRI-002 marked interpretation |
| I-09 | Two-subsidy bar: counted per person or across the household? | Stated as unknown; reviewed |
| U-01 to U-04 | Engaged couples: marriage after HFE approval; FT(PMC); non-resident partner; FPPS | Exceptions or evidence-gap rules; nothing inferred |
| G-17 | No per-status document lists | R-DOC-001 states the gap |

**Inconsistencies between the registry, the corpus and the design, flagged before
implementation:**
1. **Employment values (I-10):** architecture §5's four `employment` values don't match
   the six statuses in S07. The registry uses the six (D-062, proposed).
2. **Job count (I-11):** there is no `job_count` field in the profile, but R-DOC-002 needs
   one (proposed).
3. **`RuleResult` contract:** extended with `kind` and `notes` (proposed).
4. **Verification rule:** architecture §5 requires `validation_status == "verified"`, while
   D-058 allows non-critical `snapshot_checked` facts at runtime. Rules themselves cite
   verified facts only.
5. **Three facts** were corrected during verification (§18).
6. **Undetectable private-property sales:** the profile can't detect a private-property sale
   within 30 months (R-HH-006 limitation).

**Not encoded, by design:**
- eligibility outcomes;
- income ceilings and any calculation;
- ballot odds;
- FCS proximity checks (they need address data that is not in the profile);
- discretionary cases, which redirect to HDB (HH-OTHER-001).
