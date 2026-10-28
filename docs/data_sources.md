# Data Sources: Discovery, Scope, Rights and Acquisition

Current state of Dataset A's official sources, as of 2026-10-28.

**Where things live:**
- **Per-source records** (URLs, classification, hashes, timestamps):
  [`data/sources_manifest.json`](../data/sources_manifest.json).
- **Decisions:** D-044 to D-056 in [decisions.md](decisions.md), still PROPOSED.
- **Chronology:** [development_log.md](development_log.md).
- **Original source-discovery matrix:** [02 §3](project_context/02_policy_sources.md), kept as
  recorded. This document reconciles it against the approved scope (D-008, D-013, D-033)
  and against the live site at capture.

**Status:** 7 sources acquired manually and held privately: S01–S05 (HTML) and S07–S08
(PDF). Fact authoring hasn't started.

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
| S10 | HFE FAQs (`/hdb-flat-portal/hfe/get-help`) | Pending (Q-08) | Not acquired: robots.txt disallows it |
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
 ├─ → S10 HFE FAQs [robots-disallowed path]          → S17 Flat Portal [never accessed]
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
| Restricted | S17, plus S10 (blocked by robots.txt) |

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

### 8.2 Rights review before a fact is tracked (D-054)

1. **Write independently worded statements**, one condition each. Only proper names, numbers,
   dates and durations are kept as-is.
2. **Run a local overlap check:** flag any 8+ consecutive words shared with L1, and reword.
3. **Read it manually,** then set `rights_review: cleared`.
4. **Run the anonymity and secret scans** before suggesting a commit.

The developer drafts facts from L1, and the coding agent works only on the drafts (D-054
option (a), recommended).

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
| G-04 | HFE FAQ sub-links (S10) unmapped; the path is robots-disallowed | Possible HFE exceptions missed | The developer reads the titles in a browser; any capture needs separate approval (Q-08) |
| G-05 | First-timer definition: the term is present in S01, S04 and S05; exact wording unconfirmed | Limited priority area | Confirm at authoring |
| G-06 | No effective dates; only page "last updated" and PDF metadata | Temporal validity | Retrieval-date statement in the UI and README |
| G-07 | Conditions may vary by flat classification or sales exercise (*agent knowledge*) | Application and non-selection facts | Record conditions in `applies_to`; never generalise |
| G-11 | No grants redirect page | Excluded-topic redirect | Redirect to S02 |
| G-15 | S02 changed on capture day | Currency | Facts from the snapshot; drift check before submission |
| R-ToU | Terms read (2026-10-28). Copying ban (handled under s 244/s 187) and linking-permission clause | Residual contractual risk | D-057; disclose in the README; optionally ask HDB for written permission |
| R-evidence | The ToU 403 block page (sha256 `df0a74…c9d6`) was overwritten by the manual copy | That piece of evidence is lost; its hash stays in §6.1 | None needed |
| R-dates | S01 and S05 files modified 2–8 min after creation | Hash fidelity | The developer confirms no edits after pasting |

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
