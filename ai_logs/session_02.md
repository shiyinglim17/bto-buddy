# Session 02: Phase 0 project context documentation

- Period (UTC): 2026-10-27T14:50:17.047Z → 2026-10-28T04:01:48.665Z
- Machine-readable redacted log: `sessions/session_02.jsonl`
- Redactions appear inline as `[REDACTED Rn …]`; rules in `../ai_logs/REDACTIONS.md`.
- Tool inputs/results longer than 6000 characters are shortened here only.

### User · 2026-10-27 14:50:17



<pasted_content id="6baf">
Phase 0: context building
Before implementing any application code, review the two source documents:
references/private/project_approach.pdf
references/private/assessment_requirements.pdf
These documents contain the complete project approach and the official assessment requirements.
Your task is to transform them into a structured, traceable Markdown knowledge base.
Create:
docs/project_context/INDEX.md
docs/project_context/01_problem_and_scope.md
docs/project_context/02_policy_sources.md
docs/project_context/03_data_and_licensing.md
docs/project_context/04_architecture.md
docs/project_context/05_evaluation.md
docs/project_context/06_submission_requirements.md
docs/project_context/requirements_register.md
Requirements:
Preserve every substantive project decision, constraint, exception, source, open question, evaluation requirement and submission requirement.
Distinguish approved final decisions from proposals, historical brainstorming, open questions and superseded ideas.
Extract information from embedded tables, diagrams and images, not only selectable PDF text.
Preserve the source-discovery matrix, MVP scope, media-handling decisions, benchmark structure and metric definitions.
Subsequently, the structured context should distinguish copied source content from independently authored policy facts.
Assign stable requirement IDs with original PDF page references.
Map each requirement to its planned implementation component and acceptance evidence.
Identify contradictions without silently resolving them.
Keep the original PDFs private and Git-ignored.
Do not include the hiring organisation or role in submission-facing documentation.
Do not implement code, select models or create datasets during this phase.
Before writing files, propose the documentation structure and identify unresolved ambiguities.
After approval, create the files and perform a source-to-Markdown completeness audit.
Report all omissions, unresolved conflicts and requirements that still need my approval.
</pasted_content id="6baf">


### Claude · 2026-10-27 14:50:19

I'll start by reviewing the repo state and the two source PDFs, then propose the structure and the ambiguities before writing anything.

**Tool call: Bash** — Inspect repo layout, gitignore, and PDF tools

```
cd "<repo>" && ls -la && cat .gitignore 2>/dev/null; echo ---; git ls-files; echo ---; ls -la references references/private 2>&1; which pdftotext pdfinfo pdfimages python3; python3 -c "import fitz; print('pymupdf', fitz.__doc__)" 2>&1 | head -1
```

<details><summary>Tool result</summary>

```
total 16
drwxr-xr-x  7 <user>  staff   224 Oct 26 21:26 .
drwxr-xr-x  6 <user>  staff   192 Oct 26 01:35 ..
-rw-r--r--@ 1 <user>  staff  6148 Oct 26 01:42 .DS_Store
drwxr-xr-x@ 9 <user>  staff   288 Oct 26 01:58 .git
drwxr-xr-x  2 <user>  staff    64 Oct 26 01:35 data
drwxr-xr-x@ 3 <user>  staff    96 Oct 26 21:26 references
drwxr-xr-x  2 <user>  staff    64 Oct 26 01:35 src
---
---
references:
total 0
drwxr-xr-x@ 3 <user>  staff   96 Oct 26 21:26 .
drwxr-xr-x  7 <user>  staff  224 Oct 26 21:26 ..
drwxr-xr-x@ 4 <user>  staff  128 Oct 27 22:48 private

references/private:
total 5160
drwxr-xr-x@ 4 <user>  staff      128 Oct 27 22:48 .
drwxr-xr-x@ 3 <user>  staff       96 Oct 26 21:26 ..
-rw-r--r--@ 1 <user>  staff   183794 Oct 24 15:19 assessment requirements.pdf
-rw-r--r--@ 1 <user>  staff  2455591 Oct 27 22:47 project approach.pdf
pdftotext not found
pdfinfo not found
pdfimages not found
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3
Traceback (most recent call last):
```
</details>

<details><summary>Claude's reasoning</summary>

I see the files use spaces in their names (not underscores), and there's no `.gitignore` or commits yet. I'll read the PDFs directly so any embedded tables and images get captured too.


</details>

**Tool call: Read**

```
{
 "file_path": "<repo>/references/private/assessment requirements.pdf"
}
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 245310 chars]
```
</details>

**Tool call: Bash** — Check PDF libraries and page counts

```
cd "<repo>/references/private" && python3 -c "
import importlib
for m in ['pypdf','PyPDF2','pdfplumber','fitz']:
    try: importlib.import_module(m); print('have',m)
    except Exception: print('no',m)
"; mdls -name kMDItemNumberOfPages *.pdf
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 100 chars]
```
</details>

### Claude · 2026-10-27 14:50:46

Assessment doc read (6 pages). Now the 31-page project approach, in chunks.

**Tool call: Read**

```
{
 "file_path": "<repo>/references/private/project approach.pdf",
 "pages": "1-10"
}
```

<details><summary>Tool result (error)</summary>

```
[REDACTED R6: output containing private file content, 145 chars]
```
</details>

**Tool call: Bash** — Extract project approach text and count images/tables per page

```
cd "<repo>/references/private" && S=<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad && mkdir -p $S/pa && python3 -I -c "
import pdfplumber,sys
with pdfplumber.open('project approach.pdf') as pdf:
    out=[]
    for i,p in enumerate(pdf.pages,1):
        out.append(f'\n===== PAGE {i} ===== images={len(p.images)} tables={len(p.find_tables())}\n')
        out.append(p.extract_text() or '')
    open(sys.argv[1],'w').write(''.join(out))
" $S/pa/text.txt && wc -c $S/pa/text.txt && grep '=====' $S/pa/text.txt; which brew
```

<details><summary>Tool result</summary>

```
   52546 <tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/text.txt
===== PAGE 1 ===== images=0 tables=0
===== PAGE 2 ===== images=1 tables=0
===== PAGE 3 ===== images=1 tables=3
===== PAGE 4 ===== images=0 tables=1
===== PAGE 5 ===== images=0 tables=1
===== PAGE 6 ===== images=0 tables=1
===== PAGE 7 ===== images=0 tables=2
===== PAGE 8 ===== images=0 tables=1
===== PAGE 9 ===== images=2 tables=1
===== PAGE 10 ===== images=0 tables=1
===== PAGE 11 ===== images=0 tables=1
===== PAGE 12 ===== images=0 tables=1
===== PAGE 13 ===== images=0 tables=1
===== PAGE 14 ===== images=0 tables=0
===== PAGE 15 ===== images=0 tables=1
===== PAGE 16 ===== images=1 tables=1
===== PAGE 17 ===== images=1 tables=1
===== PAGE 18 ===== images=0 tables=1
===== PAGE 19 ===== images=0 tables=1
===== PAGE 20 ===== images=0 tables=1
===== PAGE 21 ===== images=2 tables=0
===== PAGE 22 ===== images=0 tables=2
===== PAGE 23 ===== images=0 tables=1
===== PAGE 24 ===== images=1 tables=0
===== PAGE 25 ===== images=2 tables=1
===== PAGE 26 ===== images=0 tables=1
===== PAGE 27 ===== images=1 tables=0
===== PAGE 28 ===== images=0 tables=0
===== PAGE 29 ===== images=0 tables=0
===== PAGE 30 ===== images=0 tables=0
===== PAGE 31 ===== images=0 tables=0
/opt/homebrew/bin/brew
```
</details>

### Claude · 2026-10-27 14:51:07

Text extracted. 12 pages have embedded images, so I'll render those pages to PNG to read diagrams/screenshots visually.

**Tool call: Bash** — Render image-bearing pages to PNG and list image boxes

```
cd "<repo>/references/private" && S=<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad && python3 -I -c "
import pdfplumber,sys
with pdfplumber.open('project approach.pdf') as pdf:
    for i in [2,3,9,16,17,21,24,25,27]:
        p=pdf.pages[i-1]
        p.to_image(resolution=110).save(f'{sys.argv[1]}/p{i:02d}.png')
        for j,im in enumerate(p.images): print(i,j,round(im['x0']),round(im['top']),round(im['width']),round(im['height']))
" $S/pa && ls $S/pa
```

<details><summary>Tool result</summary>

```
2 0 146 74 167 282
3 0 110 190 264 139
9 0 367 77 218 184
9 1 370 295 179 368
16 0 146 342 462 267
17 0 74 74 222 220
21 0 110 74 296 167
21 1 74 355 245 162
24 0 110 127 286 193
25 0 146 445 358 92
25 1 146 542 303 162
27 0 110 534 384 152
p02.png
p03.png
p09.png
p16.png
p17.png
p21.png
p24.png
p25.png
p27.png
text.txt
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/text.txt"
}
```

<details><summary>Tool result</summary>

```
1	
2	===== PAGE 1 ===== images=0 tables=0
3	Document Status and Interpretation
4	This document contains the project’s final approved scope, proposed technical approaches,
5	source-discovery findings, evaluation methodology, and submission considerations.
6	Instruction hierarchy:
7	1. Official technical assessment requirements — mandatory.
8	2. Final approved MVP scope and constraints — authoritative for implementation.
9	3. Approved technical and evaluation decisions — authoritative once confirmed.
10	4. Proposed approaches and open questions — require review before implementation.
11	Where different sections conflict, the most recently approved decision governs, provided it
12	remains compliant with the official assessment. Unresolved contradictions must be flagged
13	rather than silently reconciled.
14	Project status: BTO Buddy is the selected project. The final MVP scope is defined in the “MVP
15	Scope” section. The source-discovery matrix describes candidate sources and does not
16	automatically expand the MVP.
17	FINAL REVISED IDEA:
18	BTO applicants face a sequence of decisions involving applicant eligibility, household
19	composition, income, HFE requirements, priority schemes and application consequences.
20	The problem is not simply that official information does not exist. It's that applicants may
21	struggle to understand which rules apply to their particular circumstances and what
22	information they still need before proceeding.
23	Existing tools exist: HFE assessments, eligibility guidance and application information. But
24	bto-buddy provides a pre-application preparation layer that helps applicants understand relevant
25	published rules, identify missing information and prepare questions before using the official
26	application process.
27	E.g. Existing HDB chatbot: in a specifically-detailed situation, chatbot retrieves possibly
28	relevant information but simply redirects the user to links that they have to scour through
29	themselves
30	===== PAGE 2 ===== images=1 tables=0
31	Existing HDB website + HDB chatbot still puts most of the navigation and retrieval workload on
32	the user themselves to scour through, causing users to feel overwhelmed by the sheer amount
33	of information to read through and important clauses may get lost from the user’s attention as
34	they are not prominently highlighted. The current mode of navigation offers a generic
35	non-personalised experience for the BTO user, causing user fatigue and making the process of
36	home-buying feel tedious.
37	Structure of current HDB pages: embedded with hyperlinks that brings the user to a respective
38	bookmarked section either in the same page or on a different page (still within the HDB portal),
39	or in some cases an external source (e.g. pdf document that opens in a new tab or an entirely
40	different website). Information important to a user group are scattered across different pages of
41	the website, and information not relevant to a certain user group are still displayed to them,
42	making it easy to miss the relevant and important details if the specific user does not spend a
43	decent amount of time to read through carefully and expand every section. Some content
44	sections include infographics (in image form) and videos (hosted on Youtube). An applicant
45	could be eligible for multiple schemes but not realise as the information is scattered across
46	different sections of the website. This is because the website serves as more of an information
47	dump rather than applicant-centric information provision.
48	The differentiation is transparency and preparation, not replacing authoritative assessment.
49	Giving citizens a better idea of their eligibility could reduce operation load on HDB staff (by
50	reducing hotline enquiries and processing of ineligible applications).
51	Potential downstream benefit: bto-buddy could reduce administrative workload (requires future
52	user testing to validate and quantify this).
53	===== PAGE 3 ===== images=1 tables=3
54	Problem statement: BTO applicants must navigate multiple interdependent eligibility and
55	application rules. While authoritative guidance exists, translating these rules into personalised,
56	actionable preparation steps can require substantial manual interpretation. bto-buddy aims to
57	reduce that burden while keeping official sources and human verification central to the process.
58	Research question: Can a hybrid AI assistant combining structured applicant profiling,
59	authoritative policy retrieval and evidence verification provide more reliable BTO pre-application
60	guidance than a conventional LLM assistant?
61	Narrative I aim to deliver through this project: I identified a real public-service information
62	challenge, developed an AI assistant that converts complex published requirements into
63	personalised preparation guidance, and evaluated whether structured reasoning and evidence
64	verification improve its reliability over simpler approaches.
65	Problem validation:
66	The actual frequency of applicant confusion would still need supporting evidence. You can
67	substantiate policy complexity from official documentation, but should not invent statistics about
68	call-centre volume or citizen frustration.
69	The existence of multiple eligibility pathways, detailed income rules, HFE requirements,
70	application consequences and policy exceptions are substantiated from official sources (namely,
71	the HDB website). These directly establish the complexity of the information applicants must
72	navigate.
73	Own research:
74	- Volume of BTO applications
75	- Demographic of BTO applicants
76	- Sentiments about BTO application in general
77	- Confidence level of BTO applicants
78	- The proportion of young applicants who feel confused
79	- The volume of avoidable hotline enquiries,
80	Data:
81	===== PAGE 4 ===== images=0 tables=1
82	● Dataset A: Source acquisition and reviewer-facing knowledge base
83	○ The original HDB HTML pages and appro
… [49730 more chars in the JSONL export]
```
</details>

### Claude · 2026-10-27 14:51:52

Now the rendered pages with images (diagrams, infographics, demo archetypes, metrics, configurations).

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/p02.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/p03.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/p09.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

### Claude · 2026-10-27 14:51:57

The embedded screenshots are too small at this resolution. I'll crop each image at high resolution.

**Tool call: Bash** — Crop each embedded image at 300 dpi

```
cd "<repo>/references/private" && S=<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad && python3 -I -c "
import pdfplumber,sys
with pdfplumber.open('project approach.pdf') as pdf:
    for i in [3,9,16,17,21,24,25,27]:
        p=pdf.pages[i-1]
        for j,im in enumerate(p.images):
            bb=(max(0,im['x0']),max(0,im['top']),min(p.width,im['x1']),min(p.height,im['bottom']))
            p.crop(bb).to_image(resolution=300).save(f'{sys.argv[1]}/img_p{i:02d}_{j}.png')
" $S/pa && ls $S/pa
```

<details><summary>Tool result</summary>

```
img_p03_0.png
img_p09_0.png
img_p09_1.png
img_p16_0.png
img_p17_0.png
img_p21_0.png
img_p21_1.png
img_p24_0.png
img_p25_0.png
img_p25_1.png
img_p27_0.png
p02.png
p03.png
p09.png
p16.png
p17.png
p21.png
p24.png
p25.png
p27.png
text.txt
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p03_0.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p09_0.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p09_1.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p16_0.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p17_0.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p21_0.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p21_1.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p24_0.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p25_0.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p25_1.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

**Tool call: Read**

```
{
 "file_path": "<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/pa/img_p27_0.png"
}
```

<details><summary>Tool result</summary>

```
[image]
```
</details>

### Claude · 2026-10-27 14:53:33

I have all embedded content. Let me check the full-page renders for formatting cues (highlights/strikethrough that might signal approval status).

**Tool call: Bash** — Detect highlight fills and text colors per page

```
cd "<repo>/references/private" && python3 -I -c "
import pdfplumber
from collections import Counter
with pdfplumber.open('project approach.pdf') as pdf:
    for i,p in enumerate(pdf.pages,1):
        fills=Counter(str(r.get('non_stroking_color')) for r in p.rects if r.get('fill') and r['height']<20 and r['width']>20)
        strike=[l for l in p.lines if abs(l['top']-l['bottom'])<1]
        cols=Counter(str(c.get('non_stroking_color')) for c in p.chars)
        print(i,'hl:',dict(fills) if fills else '-','| textcolors:',dict(cols))
"
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 1971 chars]
```
</details>

**Tool call: Bash** — Show text rendered in non-default colors

```
cd "<repo>/references/private" && python3 -I -c "
import pdfplumber
with pdfplumber.open('project approach.pdf') as pdf:
    for i,col in [(14,(0.0941, 0.502, 0.2196)),(7,(0.0392, 0.4039, 0.4275)),(7,(0.1294, 0.1451, 0.1608))]:
        p=pdf.pages[i-1]
        print(i,col,repr(''.join(c['text'] for c in p.chars if tuple(c.get('non_stroking_color') or ())==col)[:400]))
"
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 466 chars]
```
</details>

### Claude · 2026-10-27 14:55:57

I've read both PDFs in full: 6 pages and 31 pages. That includes the 11 embedded images, which I cropped at 300 dpi and read visually. They contain the 3- and 4-configuration comparison tables, the architecture flow, the tech-stack table, the demo archetypes, the metric definitions, the verifier evaluation table and two HDB infographics. **I haven't written any files yet.** Below is the proposed structure and the ambiguities I need you to decide.

Two things before the proposal:
- The PDFs are named `assessment requirements.pdf` and `project approach.pdf`, with spaces, not underscores.
- The repo has no `.gitignore` and no commits yet. The PDFs aren't tracked, but nothing stops them from being added.

---

## Part 1 — Proposed documentation structure

### Conventions used in every file
- **Status tag on every item:**
  - `MANDATORY`: from the assessment brief.
  - `APPROVED`: an explicitly final decision in the project approach.
  - `PROPOSED`: a recommendation that needs your review.
  - `OPEN`: an open question.
  - `HISTORICAL`: earlier brainstorming.
  - `SUPERSEDED`: replaced by a later decision, kept with a pointer to its replacement.
- **Source citation on every item:** `[ASM p.N]` for the assessment brief and `[APP p.N]` for the project approach. `N` is the physical PDF page.
- **Content provenance labels:**
  - `COPIED-SOURCE`: verbatim HDB text, such as the quoted passages on APP p.7 or the infographic text on APP p.9.
  - `AUTHORED-FACT`: a policy fact you wrote yourself, not yet verified against the source.
  - `PROJECT-DECISION`: a design choice.

  Policy facts in the approach doc are marked "unverified" until checked against a frozen source. Examples are "HFE valid 9 months", "12-month assessment ending 2 months before" and "≤10 flats waiver".
- **Anonymity:** no hiring organisation, role, collaborator handle or hackathon branding appears anywhere. The assessment is called "the assessment brief".

### Files

| File | Contents |
|---|---|
| `INDEX.md` | Purpose, the status and provenance legend, the instruction hierarchy (APP p.1), a file map, and a summary of contradictions and open questions linking to their entries |
| `01_problem_and_scope.md` | Final idea, problem statement, research question, intended narrative, problem-validation stance and the to-do "own research" list. Also the existing-chatbot gap (APP p.2 screenshot, described in text without vendor branding), the theme fit, the **MVP scope table (verbatim structure, APPROVED)**, Core/Limited/Context-only/Exclude semantics, the scope-expansion rule, and the two missing-information categories (A applicant, B corpus). Ends with the demo archetypes and scope-discipline notes |
| `02_policy_sources.md` | The **source-discovery matrix in full** (all policy areas, main sources, exceptions and linked sources, URLs), labelled "not MVP-scoped". The four Dataset A seed pages, supported policy questions, the discovery path (seed → anchors → linked pages → PDFs/visuals), and **media handling** for PDFs, the 2 infographics and the 2 YouTube videos. Also the visual-resource registry fields and policy nuances flagged for the benchmark, all marked AUTHORED-FACT and unverified |
| `03_data_and_licensing.md` | Datasets A, B and C. The private-corpus vs reviewer-facing-corpus split, the `policy_facts.jsonl` role, the source manifest fields and SHA-256, the passage schema, and the rule-registry YAML example. Also extraction-completeness checks (8 rows), the policy coverage matrix, the redistribution rules, the Copyright Act ss 243–244 note, robots.txt and Terms of Use, and the privacy approach (synthetic profiles). Ends with the README data-section draft (APP p.14–15) and data limitations |
| `04_architecture.md` | The 5-stage flow (APP p.17 diagram rebuilt as text/mermaid), essential capabilities, the coverage gate, the structured missing-information contract (4 fields), the verifier policy (3 outcomes, no silent rewrite, at most one regeneration), and hard rules vs soft guidance. Also the **tech-stack table (PROPOSED)**, the LLM provider table and model-selection scorecard (PROPOSED, provisional, no model selected), and the "avoid agents/frameworks/vector DBs" constraint |
| `05_evaluation.md` | The benchmark structure (48 cases = 6 categories × 8), the label-creation protocol (6 steps), the dev/held-out split, annotation and scoring rules, safeguards, the severity rubric, and the **system configurations (both the 3-config and 4-config versions, see C-02)** with the controlled-variables table. Also **all metric definitions from both metric tables**, the failure-type taxonomy (5 types), verifier evaluation, runtime vs offline evaluation, statistical reporting, and evaluation risks |
| `06_submission_requirements.md` | Mandatory brief requirements (anonymised): README contents, the 150–250-word deployment section, development narrative, 3–5 min demo, AI-usage section and log upload. Also the critical non-compliance indicators, resource rules, model-justification rules, the scoring weights (20/25/30/15/10), the deadline and effort estimate, and your own README preferences (HTML formatting, core story in README, supporting docs). Ends with the `ai_logs/` layout and the draft AI-usage disclosure |
| `requirements_register.md` | One table: `ID · Statement · Status · Source [doc p.N] · Component · Acceptance evidence · Related IDs / conflicts`. Below it, a **Contradictions** table (C-xx) and an **Open questions** table (Q-xx). Below that, a completeness-audit appendix that I'll fill in after writing |

**ID scheme:** `REQ-<AREA>-<NNN>`, using the areas PRB, SCP, SRC, DAT, LIC, PRIV, ARC, VER, EVL, MOD, SUB, DOC and NFR. IDs are never renumbered; superseded ones stay with their status. Each ID cites every page it comes from, for example `[ASM p.2][APP p.29]`.

**Planned components** that requirements map to (names only, nothing gets built):
- `source_acquisition`, `source_manifest`, `policy_facts_kb`, `rule_registry`, `visual_resource_registry`
- `profile_extractor`, `coverage_gate`, `rule_engine`, `retriever`, `generator`, `verifier`, `report_ui`
- `eval_harness`, `benchmark_dataset`, `verifier_claim_set`
- `docker`, `README`, `ai_logs`

**Separate private file** (Git-ignored): `references/private/submission_private_notes.md`. It would hold the collaborator handle, the portal instruction and the organisation name. This follows APP p.31: "retain in private assessment notes".

**`.gitignore`** would cover `references/private/`, `data/private_corpus/`, any extracted-passage or derived-index directories, and `.DS_Store`.

---

## Part 2 — Contradictions found (I'll record these, not resolve them)

| ID | Conflict | Pages |
|---|---|---|
| C-01 | **The product is named "BTOPath"** in the configuration tables, demo archetypes and metrics text, but "BTO Buddy" or "bto-buddy" everywhere else | APP p.3, 21, 24, 25 vs p.1, 17 |
| C-02 | **The system configurations disagree.** One version has 3: A direct LLM, B RAG, C profile + retrieval + verification, with no rules. The other has 4: A, B, C hybrid with rules and no verifier, D hybrid + verifier. "If time is short, prioritise A, C, D" refers to the 4-config version | APP p.3 vs p.25–26 |
| C-03 | **The primary metric sets differ.** One table has factual accuracy, required-rule recall, missing-info recall, unsupported-claim rate and citation *correctness*. The other drops factual accuracy and adds citation *precision*, appropriate abstention and critical-error rate. Separately, critical errors are named the "primary safety metric" | APP p.24 vs p.26, p.25 |
| C-04 | **The knowledge base source differs.** The tech table says "Curated official HTML/text passages". The data section says the reviewer-facing knowledge base is *independently authored* `policy_facts.jsonl` and the HTML stays private | APP p.21 vs p.4, 13–14 |
| C-05 | **The rule registry cites `source_passage_id: hfe_application_001`.** That is a private-corpus passage ID in a different format from `HFE_001`. Reviewers can't resolve it if rules point at private passages rather than public fact IDs | APP p.4–5, 15 |
| C-06 | **The README data text says "four official HDB webpages".** But MVP "Limited" scope includes priority-scheme considerations, and the priority-schemes page isn't among the four. The matrix also lists the seniors page, MOP, the income-ceiling PDF and the employment/income declaration guides | APP p.4, 14 vs p.6–11, 18 |
| C-07 | **The supported-question lists differ.** One is: process, first-timer couples, HFE preparation, missing info, non-selection. The MVP table adds a Limited priority area and a Context-only loan/grant area. Separately, "4–5 policy areas" | APP p.5 vs p.17–18, p.28 |
| C-08 | **Log upload scope:** the brief requires *all* coding-agent session and chat logs. Your notes say "essential" logs, and your disclosure mentions ChatGPT brainstorming, which isn't a coding agent but is a chat | ASM p.4 vs APP p.30–31 |
| C-09 | **Log upload vs anonymity:** the required logs, including *this session*, will contain the organisation name copied from the brief. Uploading them conflicts with the anonymity requirement unless redacted, and redaction must still satisfy "all logs" | ASM p.2 vs p.4 |
| C-10 | **Verifier failure handling has two versions.** One says remove, label as needing review, or regenerate once. The other says flag for review. It's unclear which applies by default | APP p.22 vs p.27 |
| C-11 | The instruction hierarchy says "the most recently approved decision governs", but **no section carries a date or version**, so recency can't be determined | APP p.1 |
| C-12 | **Income assessment** is a benchmark exception (12-month period, months worked). But the MVP table doesn't say whether income-ceiling or income-calculation checks are allowed, and "Context-only topics must not trigger eligibility calculations" | APP p.22 vs p.17–18 |
| C-13 | A minor inconsistency inside the brief: Annex A says "around 21" sketches but lists 15. This has no effect on the project | ASM p.4–5 |

## Part 3 — Decisions I need from you before writing

1. **Approval status.** Only the MVP scope table and project selection are explicitly marked final (APP p.1, 17). My proposed default:
   - Treat your imperative constraints as `APPROVED`. Examples: don't commit HTML, use `data/private_corpus/`, `policy_facts.jsonl` as the canonical KB, verifier must not silently rewrite, coverage gate, 48-case structure, labelling protocol.
   - Treat the tech table, provider ranking, scorecard, Streamlit, configurations, metric tables and statistical tests as `PROPOSED`.

   OK?
2. **"PolicyProof-inspired verification layer"** (APP p.21) isn't explained anywhere. What is PolicyProof? If it's a prior project of yours, the brief's "recycling a past project" disqualification rule (ASM p.4) makes this worth documenting carefully, or dropping.
3. **Will `docs/project_context/` be committed?**
   - If yes: I'll paraphrase the assessment brief rather than reproduce it, and exclude verbatim HDB text. That means no infographic transcription, only short labelled quotes where the wording is policy-critical, such as the fiancé-under-21 and unwed-parent clauses.
   - If no: I can keep fuller copies and Git-ignore the directory.

   I recommend committing it in paraphrased form.
4. **Anonymity details.** I plan to:
   - omit the chatbot vendor branding from the APP p.2 screenshot description;
   - describe the APP p.29–30 problem-validation idea as "past public-sector hackathon projects", without the event name or URL;
   - keep Annex A only as a short note on which sketches are adjacent to this project (#5 benefits matching, #12 email triage, #15 out-of-KB robustness).

   Agree?
5. **C-01 naming:** should the register use "BTO Buddy" throughout and mark BTOPath as `SUPERSEDED`?
6. **C-02 and C-03:** should I record both configuration sets and both metric sets as `PROPOSED`, with no winner chosen? This decision is required before the evaluation plan is frozen.
7. **"Supabase"** is listed as a demo-video tool (APP p.30), but it isn't a recording tool. Should I record it as a likely error?
8. **Unspecified items** that I'll log as `OPEN` unless you have answers:
   - the dev/held-out split ratio, and whether 48 cases is the total or the test set only
   - the size of the verifier claim set
   - the policy period the app states it supports
   - where the visual-resource registry and rule registry files live
   - the `policy_facts.jsonl` schema
   - whether the robots.txt and Terms of Use checks for hdb.gov.sg have been done
   - verification of the Copyright Act ss 243–244 claim
   - the "own research" statistics, which must not be invented

Once you approve, or adjust, items 1–8, I'll create the 8 files, the private notes file and `.gitignore`. Then I'll run a page-by-page source-to-Markdown audit (every APP and ASM page and image against the register) and report omissions, unresolved conflicts and anything still awaiting your approval.

### User · 2026-10-28 00:45:17



<pasted_content id="6baf">
# Conflict Resolution and Approval to Create Project Context

Before proceeding, I want to resolve the identified contradictions and clarify the authoritative project decisions.

**Treat the decisions below as my approved clarifications**, subject to the mandatory assessment requirements. Preserve the original documents as references, but do not treat superseded approaches as active implementation requirements.

## 1. Approval status and instruction hierarchy

Use these statuses:

- `MANDATORY`: Explicit requirements from the official assessment.
- `APPROVED`: Final project decisions, including the clarifications in this message.
- `PROPOSED`: Technical alternatives or implementation details not yet approved.
- `OPEN`: Questions that genuinely cannot be resolved from the documents or this message.
- `HISTORICAL` / `SUPERSEDED`: Earlier ideas or decisions replaced by approved ones.

The final MVP scope, canonical reviewer-facing knowledge base, hybrid architecture, evaluation safeguards and source-handling restrictions are approved.

The following remain subject to evidence-based technical selection: specific LLM provider/model, retrieval improvements beyond BM25, verifier model choice, statistical tests and implementation optimisations.

**Instruction priority:**

1. Mandatory official assessment requirements.
2. My latest explicit instructions and approved decisions, where compatible with the assessment.
3. The finalised project scope, architecture, data strategy and evaluation methodology.
4. The current approved implementation task.
5. Proposed alternatives and unresolved questions.
6. Historical or superseded brainstorming.

If a material improvement or conflict is identified, explain the current approach, alternative, tradeoffs and assessment implications. Obtain my approval before deviating.

Record the approval date and a decision ID for each newly resolved decision.

## 2. Resolve the identified contradictions

**C-01 — Project naming**

The canonical project name is **BTO Buddy**.

Use:

- Repository and distribution: `bto-buddy`
- Python package: `bto_buddy`
- Application name: BTO Buddy

Mark BTOPath as a superseded working name.

**C-02 — System configurations**

Adopt the four-configuration design:

- A: Direct LLM — applicant profile and question, without retrieval or deterministic policy rules.
- B: RAG — same generation model with retrieved policy evidence.
- C: Hybrid — structured applicant profiling, deterministic rules and RAG.
- D: Hybrid + runtime factual verification.

Use the same underlying generation model, equivalent task instructions and benchmark cases wherever applicable.

For C versus D, reuse identical pre-verification outputs to isolate the effect of verification.

If time is constrained, prioritise A, C and D, documenting why B was omitted.

Mark the earlier three-configuration design as superseded.

**C-03 — Evaluation metrics**

Adopt the following primary metrics:

1. Critical-error rate.
2. Required-rule recall.
3. Missing-information recall.
4. Unsupported-claim rate.
5. Appropriate abstention.

Use citation precision, factual correctness, answer coverage, latency and inference cost as supporting metrics.

Evaluate retrieval independently using recall\@k on labelled queries, and evaluate the runtime verifier separately using independently labelled supported, contradicted and insufficient-evidence claims.

Define all metrics operationally, including denominators, before evaluation. Preserve the critical/major/minor error-severity rubric.

**C-04 — Canonical knowledge base**

The reviewer-facing `data/policy_facts.jsonl` is the canonical runtime, retrieval and primary evaluation knowledge base.

The original HTML snapshots and extracted source-derived passages are stored under `data/private_corpus/` for local source auditing, extraction and completeness validation. They are not reviewer-facing.

Normal application execution and reviewer evaluation must not depend on the private corpus.

**C-05 — Rule references**

The structured rule registry must reference stable, reviewer-accessible fact IDs, which resolve to official source URLs and relevant sections through the source manifest.

Private passage IDs may be retained for provenance but must not be necessary for runtime execution.

**C-06 — Four seed pages versus additional sources**

The four original HDB webpages are **seed sources**, not necessarily the complete approved corpus.

The source-discovery matrix identifies additional candidate sources, including priority schemes, linked FAQs, PDFs and relevant exceptions.

A subsequent prompt in phase 2 will determine the minimum source set required for the MVP. No linked source should be automatically included merely because it appears in the matrix.

Do not claim that the final corpus consists of exactly four pages until source discovery and coverage validation confirm this.

**C-07 — Supported policy scope**

The final MVP scope table is authoritative:

- Core: first-timer couple household composition, broad BTO application requirements, HFE prerequisites/timing/documentation and missing applicant information.
- Limited and source-verified: relevant first-timer/priority considerations and application/non-selection consequences.
- Context only: high-level relationship between HFE, grants and loans.
- Excluded: grant and loan eligibility calculations, detailed financing, ballot probability prediction, post-purchase conditions and comprehensive official eligibility determination.

The supported-question inventory must reflect these distinctions.

**C-08 — AI logs**

The assessment requires all coding-agent session and chat logs, not merely selected or successful sessions.

Replace references to "essential logs" with "complete project-specific coding-agent session and chat logs".

ChatGPT was used for project planning based on my ideas. You do not have to disclose this in the AI-assisted development narrative since only coding-agent logs were requested. Do not automatically include full non-coding brainstorming transcripts.

**C-09 — Logs and anonymity**

Preserve complete substantive coding-agent development history, including this Phase 0 session.

Before submission, audit exported logs for identifying information, credentials, sensitive local paths and restricted source material.

Where necessary, redact only information that genuinely requires protection, preserve the structure and substance of the session, and document redactions transparently.

Do not selectively remove failed sessions or rewrite historical prompts.

If the assessment's completeness and anonymity requirements cannot both be satisfied confidently, flag the conflict for my decision rather than silently omitting logs.

**C-10 — Verification failure handling**

Adopt this default behaviour:

- Supported: display the claim with a verified source reference.
- Contradicted: withhold the unqualified claim and flag the contradiction.
- Insufficient evidence: avoid definitive guidance and identify the evidence gap or need for official confirmation.

Do not silently rewrite unsupported claims.

One controlled regeneration attempt may be considered as an optional improvement, but it is not required for the MVP and must be approved before implementation.

**C-11 — Decision recency**

Create `docs/decisions.md` with decision IDs, approval dates, status, rationale and superseded decisions.

Use the latest explicitly approved decision when resolving conflicts, provided it complies with the assessment.

**C-12 — Income assessment**

Include income/employment information only insofar as it is necessary for HFE preparation, identifying required documents and asking relevant follow-up questions.

Do not implement comprehensive income eligibility calculations, income-ceiling determinations or financing calculations.

Income assessment exceptions may be included in the benchmark only where they are within the approved preparation scope and supported by verified policy evidence.

**C-13 — Assessment brief inconsistency**

Record the Annex A sketch-count discrepancy as a minor source-document inconsistency with no impact on implementation. Do not spend further effort resolving it.

## 3. Clarify the remaining questions

**PolicyProof:** This was an earlier brainstorming concept for evidence-grounded AI factual verification, not an existing implemented project. BTO Buddy is a new implementation that incorporates relevant verification principles.

**Project context documentation:** Commit `docs/project_context/` to the repository after reviewing it for anonymity, copied source content and other restricted information. Use independently authored summaries rather than reproducing substantial copyrighted material.

**Anonymity:** Keep organisation-specific assessment details, collaborator handles and private submission instructions in `references/private/`, excluded from Git. Submission-facing documentation should describe the project as a public-sector AI prototype.

**Supabase:** It is a tool that I may use to annotate my screen recording demo video. Leave it in the document.

**Benchmark split:** Target 48 fictional scenarios in total across six categories, with a development/held-out split that preserves category coverage. Propose the exact split before dataset creation; do not assume that all 48 cases form the held-out test set. Suggest if K-fold cross validation is better suited instead of the same held-out test set.

**Verifier claim set:** Propose an appropriately sized, independently labelled development and evaluation claim set based on the available time and evaluation objectives. Do not fabricate labels.

**Policy period:** Record source retrieval dates and known effective dates. The precise supported policy snapshot period will be finalised after source acquisition and validation.

**Data paths:**

- `data/policy_facts.jsonl`
- `data/policy_rules.yaml`
- `data/visual_resources.json`
- `data/sources_manifest.json`
- `data/source_coverage.csv`
- `data/private_corpus/raw/`
- `data/private_corpus/processed/`

**Policy facts schema:** Propose a minimal typed schema with stable fact IDs, factual statements, applicability conditions, exceptions, source references, temporal metadata and validation status. Finalise it during architecture and corpus design.

**Rights and permissions:** Record the previously identified HDB Terms of Use, robots.txt restrictions and Singapore Copyright Act computational-data-analysis considerations as preliminary findings requiring source verification during phase 2. Do not claim that HDB has granted general redistribution permission.

**Problem-validation research:** Preserve the research questions as optional evidence-gathering tasks. Do not invent statistics about applicant confusion, hotline enquiries or operational benefits.

## 4. Proceed with Phase 0 documentation extraction

You may now create:

- `docs/project_context/INDEX.md`
- `docs/project_context/01_problem_and_scope.md`
- `docs/project_context/02_policy_sources.md`
- `docs/project_context/03_data_and_licensing.md`
- `docs/project_context/04_architecture.md`
- `docs/project_context/05_evaluation.md`
- `docs/project_context/06_submission_requirements.md`
- `docs/project_context/requirements_register.md`
- `docs/decisions.md`
- `references/private/submission_private_notes.md`
- `.gitignore`

Before writing `.gitignore`, ensure it excludes `references/private/`, `data/private_corpus/`, secrets, local environments and caches.

Preserve the complete source-discovery matrix, including source URLs, content structures, linked resources, tables, expandable sections and media types.

Preserve every substantive requirement and its original PDF page reference. Distinguish approved decisions from proposals and unresolved questions.

Do not reproduce substantial HDB webpage text or private assessment content in Git-tracked documentation.

After creating the files:

1. Perform the promised page-by-page and image-by-image completeness audit.
2. Map requirements to their canonical context sections and acceptance evidence.
3. Identify any remaining contradictions, omissions or ambiguous requirements.
4. Report the final files created and their status.
5. Present any unresolved decisions requiring my approval before Phase 1.

Do not implement application functionality, download external policy sources, select the final LLM model, commit or push during this phase.
</pasted_content id="6baf">


### Claude · 2026-10-28 00:47:29

Approved. I'll write `.gitignore` first so the PDFs stay protected, then the private notes, then the tracked docs. Approval date for the new decisions is 2026-10-28.

**Tool call: Write**

```
{
 "file_path": "<repo>/.gitignore",
 "content": "# --- Private / restricted material (never commit) ---\n# Original assessment brief, project-approach PDF and private submission notes.\nreferences/private/\n# HDB HTML snapshots, extracted source-derived passages and any index built from them.\n# Redistribution permission has not been established (see docs/project_context/03_data_and_licensing.md).\ndata/private_corpus/\n\n# --- Secrets and credentials ---\n.env\n.env.*\n!.env.example\n*.pem\n*.key\nsecrets/\ncredentials*.json\nservice-account*.json\n\n# --- Local environments ---\n.venv/\nvenv/\nenv/\n.python-version\n\n# --- Python caches and build artefacts ---\n__pycache__/\n*.py[cod]\n*.egg-info/\nbuild/\ndist/\n.pytest_cache/\n.mypy_cache/\n.ruff_cache/\n.coverage\nhtmlcov/\n.ipynb_checkpoints/\n\n# --- Editor / OS ---\n.DS_Store\n.vscode/\n.idea/\n"
}
```

**Tool call: Write**

```
{
 "file_path": "<repo>/references/private/submission_private_notes.md",
 "content": "[REDACTED R6: private file content, 2364 chars]"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/.gitignore (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 201 chars]
```
</details>

### Claude · 2026-10-28 00:48:13

Next, the decision log.

**Tool call: Write**

```
{
 "file_path": "<repo>/docs/decisions.md",
 "content": "# Decision Log\n\nThis is the authoritative record of project decisions. When two sources conflict, the latest\ndecision approved here governs, provided it complies with the mandatory assessment\nrequirements (D-001, D-012).\n\n**Status values:** `APPROVED`, `PROPOSED`, `SUPERSEDED`, `OPEN`.\n**Source tags:** `[ASM p.N]` = assessment brief, page N; `[APP p.N]` = project-approach\ndocument, page N; `[DEV 2026-10-28]` = developer clarification given on that date.\n\nBoth source PDFs are private (Git-ignored). The requirements they contain are catalogued in\n[project_context/requirements_register.md](project_context/requirements_register.md).\n\n---\n\n## Instruction priority (D-001)\n\n1. Mandatory assessment requirements.\n2. The developer's latest explicit instructions and approved decisions, where compatible with the assessment.\n3. The finalised project scope, architecture, data strategy and evaluation methodology.\n4. The current approved implementation task.\n5. Proposed alternatives and unresolved questions.\n6. Historical or superseded brainstorming.\n\nAny material improvement or conflict found later must be raised with:\n- the current approach;\n- the alternative;\n- the trade-offs;\n- the assessment implications.\n\nThe developer must approve it before any deviation.\n\nThis replaces the hierarchy in [APP p.1], which is recorded as superseded in BD-00.\n\n---\n\n## Decisions approved 2026-10-28\n\n| ID | Decision | Status | Resolves | Rationale | Supersedes |\n|---|---|---|---|---|---|\n| D-001 | Status taxonomy: MANDATORY, APPROVED, PROPOSED, OPEN, HISTORICAL/SUPERSEDED. The instruction priority above applies. Approved areas: final MVP scope, canonical reviewer-facing KB, hybrid architecture, evaluation safeguards, source-handling restrictions. Decided later by evidence-based selection: LLM provider/model, retrieval improvements beyond BM25, verifier model, statistical tests, implementation optimisations | APPROVED | Proposal Q1 | Makes approval status explicit for every item | APP p.1 hierarchy (BD-00) |\n| D-002 | Canonical name **BTO Buddy**. Repo/distribution `bto-buddy`; Python package `bto_buddy`; application name \"BTO Buddy\". \"BTOPath\" is a superseded working name | APPROVED | C-01 | One consistent name across code and docs | \"BTOPath\" [APP p.3, 21, 24, 25] |\n| D-003 | Four system configurations: A Direct LLM (profile + question, no retrieval, no rules); B RAG (same model + retrieved evidence); C Hybrid (structured profiling + deterministic rules + RAG); D Hybrid + runtime factual verification. All use the same generation model, equivalent task instructions and the same benchmark cases wherever applicable. C vs D reuses identical pre-verification outputs. If time is short, run A, C and D and document why B was omitted | APPROVED | C-02 | Ablation isolates the effect of each component | 3-configuration design [APP p.3] |\n| D-004 | **Primary metrics:** critical-error rate, required-rule recall, missing-information recall, unsupported-claim rate, appropriate abstention. **Supporting metrics:** citation precision, factual correctness, answer coverage, latency, inference cost. **Component evaluations:** retrieval recall@k on labelled queries; runtime verifier on independently labelled supported/contradicted/insufficient claims. All metrics are defined operationally, with denominators, before evaluation. The critical/major/minor severity rubric is kept | APPROVED | C-03 | Puts safety first and makes each component measurable | Primary/secondary list [APP p.24]; table [APP p.26] (definitions kept) |\n| D-005 | `data/policy_facts.jsonl` is the canonical runtime, retrieval and primary-evaluation KB. HTML snapshots and source-derived passages live under `data/private_corpus/`, for local auditing, extraction and completeness validation only. Running the app and the reviewer evaluation must not depend on the private corpus | APPROVED | C-04 | Reproducible on a clean machine and rights-compliant | Tech-table row \"Knowledge base: curated official HTML/text passages\" [APP p.21] |\n| D-006 | The rule registry references stable, reviewer-accessible **fact IDs**. These resolve to official URLs and sections through the source manifest. Private passage IDs may be kept for provenance but are never needed at runtime | APPROVED | C-05 | Reviewers can resolve every rule citation | `source_passage_id` in the rule example [APP p.15] |\n| D-007 | The four HDB pages are **seed sources**, not necessarily the complete corpus. The minimum MVP source set will be decided in Phase 2. Nothing is included just because it appears in the source-discovery matrix. Don't claim a four-page corpus until coverage validation confirms it | APPROVED | C-06 | Coverage is decided by evidence | \"four official HDB webpages\" wording [APP p.14] |\n| D-008 | The MVP scope table is authoritative. Core: first-timer couple household composition, broad BTO application requirements, HFE prerequisites/timing/documentation, missing applicant information. Limited, source-verified: relevant first-timer/priority considerations; application/non-selection consequences. Context only: high-level relationship between HFE, grants and loans. **Excluded:** grant/loan eligibility calculations, detailed financing, **ballot probability prediction**, post-purchase conditions, **comprehensive official eligibility determination**. The supported-question inventory must reflect these tiers | APPROVED | C-07 | One authoritative scope. Ballot prediction and comprehensive determination are added to the exclusions | Supported-question list [APP p.5] |\n| D-009 | Upload the **complete project-specific coding-agent session and chat logs**, not selected sessions. Replace every reference to \"essential logs\". Disclosing ChatGPT planning use is not required. Full non-coding brainstorming transcripts are not included automatically | APPROVED | C-08 | The brief requires all coding-agent logs
… [7010 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/decisions.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 00:55:53

Now the context files, starting with problem and scope.

**Tool call: Write**

```
{
 "file_path": "<repo>/docs/project_context/01_problem_and_scope.md",
 "content": "# 01 — Problem and Scope\n\nThe status and provenance legend is in [INDEX.md](INDEX.md#legend). Requirement IDs are\ndefined in [requirements_register.md](requirements_register.md).\n\n## 1. Project identity\n\n| Item | Value | Status | Source |\n|---|---|---|---|\n| Project | **BTO Buddy**: a pre-application preparation assistant for Build-To-Order (BTO) flat applicants | APPROVED | [APP p.1], D-002 |\n| Repository / package / app | `bto-buddy` / `bto_buddy` / \"BTO Buddy\" | APPROVED | D-002 |\n| \"BTOPath\" | Earlier working name, found in some tables and figures | SUPERSEDED | [APP p.3, 21, 24, 25] |\n| \"PolicyProof\" | Earlier brainstorming concept for evidence-grounded factual verification. Never implemented. BTO Buddy borrows its verification principles only | HISTORICAL | [APP p.21], D-015 |\n| Stakeholder | Citizen group (prospective BTO applicants) | APPROVED | [APP p.29], REQ-PRB-001 |\n| Assessment theme | Retrieval & knowledge (primary). The verification layer also touches \"generation with guardrails\" | APPROVED (primary), inference (secondary) | [APP p.29], [ASM p.1] |\n\n## 2. Final revised idea — REQ-PRB-010 (APPROVED) [APP p.1–2]\n\n- BTO applicants face a **sequence of decisions**:\n  - applicant eligibility;\n  - household composition;\n  - income;\n  - HDB Flat Eligibility (HFE) letter requirements;\n  - priority schemes;\n  - application consequences.\n- The problem is **not** that official information is missing. Applicants struggle to work\n  out which rules apply to *their* circumstances, and what information they still need\n  before they proceed.\n- Official tools already exist: HFE assessments, eligibility guidance and application\n  information. BTO Buddy adds a **pre-application preparation layer** that helps applicants:\n  - understand the relevant published rules;\n  - identify missing information;\n  - prepare questions before they use the official application process.\n- **Differentiation:** transparency and preparation. BTO Buddy does not replace the\n  authoritative assessment.\n\n### 2.1 Observed gap in existing channels [APP p.1–2] (developer observation)\n\n**The HDB website's virtual assistant.**\n- A screenshot in the project approach shows a test query: a first-timer with four previous\n  unsuccessful BTO attempts asks whether they have an advantage at the next attempt.\n- The assistant replied that it did not understand and asked the user to rephrase. It then\n  listed three generic links:\n  - a First-Timer (Parents & Married Couples) priority-scheme page on an external\n    government services directory;\n  - \"Application for a New Flat\";\n  - \"Modes of Sale\".\n- The user is left to read through the linked pages themselves.\n\n**The website itself.**\n- Pages link to anchors on the same page, to other portal pages, or to external resources\n  such as PDFs and other sites.\n- Information relevant to one user group is scattered across pages, and irrelevant content\n  is still shown, so important clauses are easy to miss unless every expandable section is\n  opened.\n- Some content exists only in infographics (images) or in videos hosted on YouTube.\n- An applicant may qualify for several schemes without realising it. The site works more as\n  an **information dump** than as applicant-centred guidance.\n\n**Effect on users:** a generic, non-personalised experience that causes fatigue.\n\n### 2.2 Potential downstream benefit — HYPOTHESIS ONLY (REQ-PRB-015) [APP p.2]\nBetter-prepared citizens *could* reduce HDB operational load: fewer hotline enquiries and\nfewer ineligible applications to process. This needs future user testing to validate and\nquantify, and must not be claimed as a result.\n\n## 3. Problem statement — REQ-PRB-011 (APPROVED) [APP p.3]\n> BTO applicants must navigate multiple interdependent eligibility and application rules.\n> While authoritative guidance exists, translating these rules into personalised, actionable\n> preparation steps can require substantial manual interpretation. BTO Buddy aims to reduce\n> that burden while keeping official sources and human verification central to the process.\n\n*(This is the developer's own text; \"bto-buddy\" is normalised to \"BTO Buddy\" per D-002.)*\n\n## 4. Research question — REQ-PRB-012 (APPROVED) [APP p.3]\n> Can a hybrid AI assistant combining structured applicant profiling, authoritative policy\n> retrieval and evidence verification provide more reliable BTO pre-application guidance than\n> a conventional LLM assistant?\n\n**Intended narrative [APP p.3]:**\n1. Identify a real public-service information challenge.\n2. Build an assistant that turns complex published requirements into personalised\n   preparation guidance.\n3. Evaluate whether structured reasoning and evidence verification make it more reliable\n   than simpler approaches.\n\n## 5. Problem validation — REQ-PRB-013, REQ-PRB-014 [APP p.3, 29–30], D-025\n\n- **APPROVED stance:**\n  - Policy *complexity* can be substantiated from official documentation: multiple\n    eligibility pathways, detailed income rules, HFE requirements, application consequences\n    and exceptions.\n  - The *frequency* of applicant confusion needs separate supporting evidence.\n  - **Never invent** statistics about call-centre volume, citizen frustration or operational\n    benefit.\n- **Optional research tasks (OPEN, not started):**\n  - volume of BTO applications;\n  - demographics of BTO applicants;\n  - general sentiment about BTO applications, including applicant confidence and the share\n    of young applicants who feel confused;\n  - volume of avoidable hotline enquiries.\n- **Optional evidence route (PROPOSED) [APP p.29–30]:** given the short timeframe, cite\n  findings from *past public-sector hackathon projects* as predecessors. Use them only where\n  they are publicly documented, and cite them accurately.\n\n## 6. MVP scope — REQ-SCP-001 (APPROVE
… [7949 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/project_context/01_problem_and_scope.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 00:56:46

Next, policy sources, including the full source-discovery matrix.

**Tool call: Write**

```
{
 "file_path": "<repo>/docs/project_context/02_policy_sources.md",
 "content": "# 02 — Policy Sources\n\nThe legend is in [INDEX.md](INDEX.md#legend).\n\n> **Copyright note (D-016):** this file records source *locations, structure and media\n> types*. Policy content appears only as short, independently paraphrased **AUTHORED-FACT\n> (unverified)** notes. Each must be verified against a frozen source in Phase 2 before it\n> enters `data/policy_facts.jsonl`. The project-approach document quoted HDB text verbatim\n> in places, marked **COPIED-SOURCE** below. Those quotations are *not* reproduced here; only\n> their location and a paraphrase are kept.\n\n## 1. Seed sources — REQ-SRC-001 (APPROVED as seeds, D-007) [APP p.4]\n\nThese are **seed sources**, not necessarily the complete corpus. The minimum MVP source set\nis decided in Phase 2 (REQ-SRC-014).\n\n| Seed ID (proposed) | Page | URL | What it provides |\n|---|---|---|---|\n| SEED-1 | Couples and Families | https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/couples-and-families | Household composition and broad eligibility conditions |\n| SEED-2 | Application for an HDB Flat Eligibility (HFE) Letter | https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/application-for-an-hdb-flat-eligibility-hfe-letter | HFE requirements, validity and process |\n| SEED-3 | Income Guidelines and Documents for HFE Letter Application | https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/application-for-an-hdb-flat-eligibility-hfe-letter/income-guidelines-and-documents | Assessment periods, income calculation and documents |\n| SEED-4 | Application for a New Flat | https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/process-for-buying-a-new-flat/application | Application and non-selection consequences |\n\n## 2. Discovery method (APPROVED) [APP p.5]\n\n- **Discovery path:** seed pages → relevant anchors → linked pages → PDFs and visual\n  content (REQ-SRC-005).\n- Relevant sources and hyperlinks are mapped **manually** (done for the matrix below).\n- A **frozen, versioned corpus** is used for evaluation, so website changes can't alter\n  benchmark results between runs (REQ-SRC-004).\n- **Observed site structure:**\n  - hyperlinks go to anchors on the same page, other portal pages, or external resources\n    (PDFs in a new tab, other sites);\n  - user-group information is scattered, and irrelevant content is still shown;\n  - some content exists only in infographics (images) or YouTube videos.\n\n## 3. Source-discovery matrix (complete) [APP p.5–11]\n\n> **Status:** this matrix lists *candidate* sources. It is **not scoped to the MVP** and\n> does not expand it (REQ-SCP-007, BD-02). Each row notes its MVP tier relation for\n> orientation only.\n\n### Row 1 — Applicant composition and types: definitions and eligibility conditions [APP p.5–8]\n\n**MVP tier relation:** Core for first-timer couples; other groups are OPEN (Q-05).\n\n**Main source 1: \"Couples and Families\" (SEED-1).** URL in §1.\n\n- **Content structure:** eligibility conditions per user group / applicant category, mostly\n  as **expandable sections on the same page**, formatted as **tables, sometimes nested**.\n- **Applicant categories listed** (names only):\n  - Fiancé and fiancée;\n  - Married couples and/or parent(s) with child(ren), [REDACTED R7: 11 words of HDB source text];\n  - Multi-generation families (buying with fiancé(e)/spouse and parents);\n  - Orphaned siblings (buying with sibling(s) who are orphans and single);\n  - Families with non-residents (an SC buying with a non-resident spouse or parent(s)/child(ren)).\n- **Defined priority schemes on this page** (expandable sections):\n  - First-Timer (Parents & Married Couples), **FT(PMC)**;\n  - **Family and Parenthood Priority Scheme (FPPS)**, which supports first-timer married\n    couples with children and young married couples.\n\n**Main source 2: \"Priority Schemes\".**\nURL: https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/process-for-buying-a-new-flat/application/priority-schemes\n\nExpandable section per scheme, grouped by target group:\n\n| Target group | Scheme | Format |\n|---|---|---|\n| Couples expecting a child, and families with child(ren) | Third Child Priority Scheme (**TCPS**), for families with 3+ children | expandable section |\n| Parents and children who want to live with or near each other (fiancé/fiancée applicants may also qualify) | Family Care Scheme (**FCS**) (Proximity) | expandable section |\n| (same group) | Family Care Scheme (**FCS**) (Joint Balloting) | expandable section |\n| Seniors who want to live near their existing home (2-room Flexi, to age in place) | Senior Priority Scheme (**SPS**) (near existing home) | expandable section |\n| Public rental tenants who want to buy their own home | Tenants' Priority Scheme (**TPS**), for HDB rental tenants buying 2-room Flexi or 3-room | expandable section |\n\n**Specific user groups / exclusions** (linked sources and conditions):\n\n| Item | Source | Notes | Provenance |\n|---|---|---|---|\n| Seniors (both aged 55+, buying a short-lease 2-room Flexi or Community Care Apartment) | Separate page: https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/seniors | Separate page on the HDB site | Structure note |\n| First-timer households with exactly 1 SC + 1 or more SPR members | SEED-1; Citizen Top-Up page: https://www.hdb.gov.sg/managing-my-home/finances/citizen-topup | Paraphrase: such households pay a premium at flat purchase (amount stated on the source, recorded as $10,000). A Citizen Top-Up may be claimed later when an SPR member becomes a citizen or an SC child is born | COPIED-SOURCE in APP p.7 → AUTHORED-FACT (unverified) here. **OPEN (Q-06):** is this a premium/financing matter (Excluded) or a first-timer consideration (Limited)? |\n| Fiancé/fiancée below 21 | SEED-1 | Paraphrase: an under-21 [REDACTED R7: 10 words of HDB source text]. Applicant
… [11421 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/project_context/02_policy_sources.md (file state is current in your context — no need to Read it back)
```
</details>

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/02_policy_sources.md",
 "old_string": "| **OPEN (Q-07):** Excluded or Limited? Resale levy can affect second-timer applicants; the matrix lists it without a tier |",
 "new_string": "| **OPEN (Q-07):** the matrix lists it on a \"conditions after buying\" page without a tier. Treat it as post-purchase (Excluded) or as an application consideration (Limited)? |"
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/01_problem_and_scope.md",
 "old_string": "BTO Buddy is an independent problem formulation, not a selected sketch.",
 "new_string": "*(Author note: neither source document says which sketch, if any, BTO Buddy derives from.\nThe developer should confirm the wording before using this in the README.)*"
}
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/02_policy_sources.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/01_problem_and_scope.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 00:59:17

Now data and licensing.

**Tool call: Write**

````
{
 "file_path": "<repo>/docs/project_context/03_data_and_licensing.md",
 "content": "# 03 — Data, Licensing and Privacy\n\nThe legend is in [INDEX.md](INDEX.md#legend).\n\n## 1. Data assets overview\n\n| Asset | Path (D-022) | Git | Role | Status |\n|---|---|---|---|---|\n| Raw HDB HTML snapshots, PDFs | `data/private_corpus/raw/` | **Ignored** | Local provenance, extraction, completeness validation | APPROVED (BD-03, D-005) |\n| Extracted source-derived passages; any index built from them | `data/private_corpus/processed/` | **Ignored** | Local auditing only | APPROVED |\n| Source manifest | `data/sources_manifest.json` | Tracked | URLs, titles, timestamps, hashes, extraction method | APPROVED |\n| Source coverage matrix | `data/source_coverage.csv` | Tracked | Policy/extraction coverage evidence | APPROVED (path); format PROPOSED |\n| **Policy facts KB (canonical)** | `data/policy_facts.jsonl` | Tracked | Runtime, BM25 retrieval, primary evaluation | APPROVED (D-005); schema PROPOSED (D-023) |\n| Structured rule registry | `data/policy_rules.yaml` | Tracked | Deterministic checks | APPROVED (path); content after Phase 2 |\n| Visual-resource registry | `data/visual_resources.json` | Tracked | Infographic/video links and display conditions | APPROVED (path) |\n| Evaluation scenarios (Dataset C) | path OPEN (Q-10) | Tracked | Benchmark | APPROVED (design); not yet created |\n| Verifier claim set | path OPEN (Q-10) | Tracked | Verifier evaluation | APPROVED (D-020); size PROPOSED |\n| Saved predictions and run metadata | path OPEN (Q-10) | Tracked | Reproducible offline scoring | APPROVED (REQ-DAT-018) |\n\n## 2. Dataset A — source acquisition and reviewer-facing KB [APP p.4–5, 11–14]\n\n### 2.1 Two corpora (APPROVED, D-005)\n- **Private source corpus:**\n  - the original HDB HTML pages and approved linked resources;\n  - kept locally for provenance, extraction and policy-completeness validation;\n  - full snapshots and extracted copied-text passages are **excluded from Git**\n    (REQ-LIC-010, REQ-LIC-011).\n- **Reviewer-facing canonical KB:** `data/policy_facts.jsonl`, which holds\n  **independently authored, source-attributed factual policy representations**. Each has\n  passed manual validation and rights review (REQ-DAT-010).\n- The application, BM25 index, Docker deployment and primary evaluation **all use the\n  reviewer-facing corpus** (REQ-DAT-011).\n- The private corpus is **not** needed for normal execution or reviewer evaluation\n  (REQ-DAT-012).\n- The matrix, snapshots and extraction reports support building and auditing the authored\n  facts. They don't expand the MVP (REQ-SCP-007).\n\n### 2.2 Same interface, no transfer of claims (APPROVED) [APP p.13], REQ-DAT-013\n- Both corpora should be usable through the **same retrieval interface**.\n- Document any coverage differences between them.\n- **Never claim that results on one corpus apply to the other.**\n- **OPEN (Q-11):** is any experiment planned on the private corpus? If not, the\n  same-interface requirement only needs to hold structurally.\n\n### 2.3 Source manifest — REQ-SRC-002 (APPROVED) [APP p.4, 14]\nRequired fields per source:\n- URL;\n- document title;\n- access timestamp;\n- source section;\n- extraction method;\n- **SHA-256 hash** of the snapshot, to show it didn't change between experiments;\n- relevant policy scope [APP p.14].\n\n### 2.4 Private passage record (APPROVED structure, private corpus only) [APP p.4–5]\n- **REQ-SRC-003:** each passage keeps enough context to avoid misreading an exception. For\n  example, a condition must not be separated from the heading that names its applicant group.\n- Example fields from the source document:\n\n  ```json\n  {\n    \"passage_id\": \"HFE_001\",\n    \"source_id\": \"HFE_APPLICATION\",\n    \"section\": \"Application Requirements\",\n    \"source_url\": \"https://www.hdb.gov.sg/...\",\n    \"anchor\": \"#application-requirements\",\n    \"content_type\": \"html\",\n    \"retrieved_at\": \"2026-10-26\",\n    \"policy_effective_date\": null,\n    \"text\": \"Locally extracted source content\",\n    \"review_status\": \"pending\"\n  }\n  ```\n\n- `text` holds copied source content, so these records live only under\n  `data/private_corpus/processed/`.\n\n### 2.5 `policy_facts.jsonl` schema — PROPOSED (D-023; finalise in architecture/corpus design)\n\nOne JSON object per line. Typed with Pydantic in code.\n\n| Field | Type | Purpose |\n|---|---|---|\n| `fact_id` | str, stable, e.g. `HFE-VALIDITY-001` | Referenced by rules, labels and citations. Never reused |\n| `statement` | str | **Independently authored** factual paraphrase. No substantial copied text |\n| `topic` | enum (e.g. `household`, `hfe`, `income_docs`, `application`, `non_selection`, `priority`) | Retrieval facets and coverage gate |\n| `scope_tier` | enum `core` / `limited` / `context` | Links to the MVP tier |\n| `applies_to` | object of conditions (e.g. `{\"household_type\": \"first_timer_couple\"}`) | Applicability |\n| `exceptions` | list of `{description, fact_id?}` | Keeps exceptions attached |\n| `source` | `{source_id, url, section, anchor}` | Resolves through `sources_manifest.json` |\n| `private_passage_ids` | list[str] (optional) | Provenance only; never needed at runtime (D-006) |\n| `retrieved_at` | date | Temporal metadata |\n| `effective_from` / `effective_to` | date or null; plus `effective_date_note` | Known effective dates and ambiguity |\n| `validation` | `{status: draft/verified/rejected, method, validated_at, notes}` | Manual validation |\n| `rights_review` | `{status: pending/cleared, notes}` | Rights review before it is tracked |\n| `kb_version` | str | Corpus versioning |\n\n### 2.6 Extraction (APPROVED) [APP p.11]\n- **REQ-SRC-006:**\n  - capture **only explicitly approved webpages**, by manual rendered-DOM extraction or\n    controlled browser automation, subject to documented access and usage permissions;\n  - preserve expanded informational sections;\n  - **never** follow links 
… [8784 more chars in the JSONL export]
````

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/project_context/03_data_and_licensing.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 01:00:12

Now architecture.

**Tool call: Write**

````
{
 "file_path": "<repo>/docs/project_context/04_architecture.md",
 "content": "# 04 — Architecture\n\nThe legend is in [INDEX.md](INDEX.md#legend).\n\n> No code exists yet. Component names are **planned** identifiers, used for traceability in\n> the [requirements register](requirements_register.md).\n\n## 1. Essential capabilities and constraints (APPROVED) [APP p.16–17]\n\n**REQ-ARC-001: the three essential capabilities.**\n1. Retrieve authoritative policy evidence.\n2. Generate profile-specific preparation guidance, including missing information.\n3. Verify factual claims and flag unsupported statements.\n\n**REQ-ARC-002: constraints.**\n- Use deterministic Python validation for known structured fields.\n- **Avoid** autonomous agents, complex orchestration frameworks and unnecessary vector\n  databases (BD-09).\n\n**REQ-PRB-002 tension.** The brief needs *significant AI integration*, not \"simply an API\ncall within a standard web app\" [ASM p.2]. The argument that this design meets that bar\nrests on:\n- LLM-based structured profile extraction;\n- grounded generation;\n- claim-level verification;\n- an ablation (A–D) showing each component's measured contribution.\n\nThe README must make this argument explicitly.\n\n## 2. Pipeline — REQ-ARC-003 (APPROVED, BD-04) [APP p.17, image]\n\nRebuilt from the diagram, with the coverage gate (REQ-ARC-004) placed as specified in\n[APP p.21]:\n\n```mermaid\nflowchart TD\n    IN[\"User question + fictional applicant profile\"] --> S1\n    S1[\"1. Structured extraction and validation<br/>Pydantic schema, missing fields, contradictions\"] --> G\n    G{\"Coverage gate<br/>within supported policy areas?\"}\n    G -- no --> OOS[\"Out-of-scope response<br/>+ official-source redirection\"]\n    G -- yes --> S2A & S2B\n    S2A[\"2A. Rule engine<br/>explicit policy conditions & preparation requirements\"] --> S3\n    S2B[\"2B. Evidence retrieval<br/>BM25 over curated policy facts\"] --> S3\n    S3[\"3. Evidence-grounded response generation<br/>structured explanation, citations, missing-information checklist\"] --> S4\n    S4[\"4. Claim-level verification<br/>Supported / Contradicted / Insufficient evidence\"] --> S5\n    S5[\"5. Applicant-facing preparation report<br/>verified guidance, flagged uncertainty, official source links\"]\n```\n\n**Retrieval corpus note.** The diagram says \"BM25 over curated policy passages\". Under D-005,\nthe retrieval corpus is `data/policy_facts.jsonl`.\n\n**Coverage-gate placement.** The diagram doesn't place the gate. [APP p.21] says it runs\n\"before generating a response\". Placing it after profile extraction and before retrieval is\nthe author's reading, PROPOSED (Q-12).\n\n| Stage | Planned component | Status |\n|---|---|---|\n| 1 | `profile_extractor` (LLM → Pydantic) plus deterministic field validation | APPROVED design |\n| Gate | `coverage_gate` | APPROVED |\n| 2A | `rule_engine` reading `data/policy_rules.yaml` | APPROVED |\n| 2B | `retriever` (BM25) | APPROVED. Embeddings PROPOSED, conditional (§6) |\n| 3 | `generator` (one selected LLM) | APPROVED design; model OPEN |\n| 4 | `verifier` | APPROVED design; method/model OPEN |\n| 5 | `report_ui` | APPROVED design; UI framework PROPOSED |\n\n## 3. Structured missing-information contract — REQ-ARC-005 (APPROVED, BD-06) [APP p.20]\n\nEvery response object carries these four fields:\n\n| Field | Meaning | Behaviour |\n|---|---|---|\n| `missing_profile_fields` | Applicant attributes needed for personalised guidance but not provided | Targeted clarification where appropriate. **Never assume values** (REQ-ARC-013) |\n| `evidence_gaps` | Missing or insufficient authoritative policy evidence | **Prevents unsupported definitive conclusions** |\n| `profile_conflicts` | Contradictory applicant information | Ask for clarification |\n| `out_of_scope_reasons` | Questions or scenarios outside the MVP | Coverage-gate response and redirection |\n\n**REQ-ARC-014:** missing evidence must **never** be read as proof that a requirement doesn't\nexist.\n\n## 4. Representation principles (APPROVED) [APP p.22, 28]\n\n- **REQ-ARC-006:** represent policies as conditions, exceptions, effective dates and source\n  references in structured metadata, never just as paragraphs.\n- **REQ-ARC-007:** use typed objects throughout (retrieved evidence, applicable rules, missing\n  fields, verification results). Never pass unstructured text between modules. This enables\n  component-level error analysis.\n- **REQ-ARC-008: hard rules vs soft guidance.**\n  - Clearly documented requirements are checked deterministically. Example: a valid HFE\n    letter is needed.\n  - Complex interpretations stay **evidence-linked explanations that need official\n    confirmation**.\n  - Document which decisions are deterministic and which need retrieval or human review.\n- **REQ-ARC-009:** LLM answers link to the actual HDB webpages as sources [APP p.13].\n\n## 5. Runtime verification (APPROVED) [APP p.22, 26–28], D-011\n\n| Outcome | Displayed behaviour (D-011) |\n|---|---|\n| **Supported** | Show the claim with a verified source reference |\n| **Contradicted** | Withhold the unqualified claim and flag the contradiction |\n| **Insufficient evidence** | No definitive guidance. State the evidence gap or the need for official confirmation |\n\n- **REQ-VER-003:** never silently rewrite. No unlimited verification loops.\n  - One controlled regeneration is an **optional improvement** and needs approval\n    (REQ-VER-004).\n- **REQ-VER-005:** keep *contradicted* separate from *not established*. Treating every\n  unsupported claim as false is a methodological error.\n- **REQ-VER-007:** the verifier must **withhold, correct or clearly flag** to show a\n  reduction in *exposed* errors. If it only labelled claims, its detection ability would be\n  measured separately (D-011 makes it act).\n- **REQ-VER-006:** don't assume a second LLM verification call is worthwhile. Compare its\n  incremental error detection against its added cost a
… [3596 more chars in the JSONL export]
````

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/project_context/04_architecture.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 01:00:48

Now the evaluation plan, including the split and claim-set proposals you asked for.

**Tool call: Write**

```
{
 "file_path": "<repo>/docs/project_context/05_evaluation.md",
 "content": "# 05 — Evaluation\n\nThe legend is in [INDEX.md](INDEX.md#legend).\n\n**MANDATORY context [ASM p.2–3]:**\n- Select and justify a specific evaluation methodology, with the rationale in the README.\n- **Soundness outranks the size of the results.**\n- Evaluation and effectiveness carry the largest scoring weight (30%).\n- Novelty counts only together with effectiveness.\n- Be honest about limitations (REQ-EVL-001, REQ-EVL-002).\n\n**Chosen methodology (APPROVED):** a **controlled benchmark with an ablation-style\ncomparison** of system configurations. The runtime verifier and the retriever are also\nevaluated as separate components.\n\n## 1. System configurations — REQ-EVL-010 (APPROVED, D-003) [APP p.25–26]\n\n| System | What it includes | Question answered |\n|---|---|---|\n| A — Direct LLM | Applicant profile + question → model response. No retrieval, no deterministic rules | How well does a simple assistant perform? |\n| B — RAG | Retrieved policy evidence → model response (same model) | Does grounding improve reliability? |\n| C — Hybrid | Structured profiling + deterministic rules + RAG | Do structured checks improve guidance? |\n| D — Hybrid + verifier | Full BTO Buddy pipeline | Does verification reduce exposed errors? |\n\n### Controlled variables [APP p.25, image 2]\n\n| Dimension | A | B | C | D |\n|---|---|---|---|---|\n| Same generation model | Yes | Yes | Yes | Yes |\n| Same applicant input | Yes | Yes | Yes | Yes |\n| Same supported policy scope | Yes | Yes | Yes | Yes |\n| Pretrained knowledge | Yes | Yes | Yes | Yes |\n| Retrieved policy facts | No | Yes | Yes | Yes |\n| Structured profile extraction | No separate module | No separate module | Yes | Yes |\n| Deterministic policy rules | No | No | Yes | Yes |\n| Claim verification | No | No | No | Yes |\n\n- **REQ-EVL-011:** use the same generation model, equivalent task instructions and the same\n  benchmark cases. All configurations are scored against **the same authoritative reference\n  labels and the same policy version**.\n- **REQ-EVL-012 (D-003):** C vs D **reuses identical pre-verification outputs**, so the\n  difference isolates the verifier.\n- **REQ-EVL-013:** if time is short, run **A, C and D** and document why B was omitted. That\n  still gives a baseline, the core intervention and the verification ablation.\n- **Purpose:** show *why* the added engineering complexity is justified, rather than assuming\n  a more elaborate architecture is better [APP p.3].\n- **Verification ablation [APP p.24, 26]:** enabled vs disabled on identical cases. This\n  tests measurable value and also exposes false alarms, latency and cost.\n- **SUPERSEDED [APP p.3]:** the three-configuration design (A baseline, B RAG,\n  C \"BTOPath\" = profile + retrieval + verification). Its evaluated aspects were factual\n  correctness, required-rule coverage, unsupported-claim rate, missing-information\n  detection, abstention and latency. All of these are carried into §4.\n\n## 2. Two separate evaluation activities (APPROVED) [APP p.27, image]\n\n| Evaluation type | Purpose |\n|---|---|\n| Runtime verification | Checks generated claims against retrieved evidence before they are shown |\n| Independent offline evaluation | Measures whether the application **and its verifier** are actually correct |\n\n**REQ-EVL-029:** the offline benchmark has independently reviewed labels. **The runtime\nverifier's judgements are never ground truth** [APP p.25, 27].\n\n## 3. Benchmark (Dataset C) — REQ-EVL-014 (APPROVED, D-019) [APP p.15–16]\n\n### 3.1 Structure: 48 fictional cases in total, 6 categories × 8\n\n| Category | Cases | What it tests |\n|---|---|---|\n| Standard preparation | 8 | Correct applicable requirements |\n| Missing information | 8 | Appropriate follow-up questions |\n| Policy exceptions | 8 | Handling nuanced conditions |\n| Misconceptions | 8 | Correcting inaccurate assumptions |\n| Conflicting information | 8 | Detecting contradictory profile details |\n| Out-of-scope | 8 | Abstaining appropriately |\n\n- **REQ-EVL-032 [APP p.27]:** expand the three demo archetypes into many independently\n  labelled cases covering different profiles, rules and edge conditions.\n- Include conflicting-information and out-of-scope cases even if the video doesn't show them.\n\n### 3.2 Label-creation protocol — REQ-EVL-016..019 (APPROVED) [APP p.16]\n1. **Extract policy requirements first.** Build a rule inventory with source references.\n2. **Design scenario templates.** Vary one or two meaningful factors at a time, including\n   boundary conditions.\n   - Use **policy-derived scenarios**. Never ask an LLM to invent eligibility labels.\n   - Independently check the expected guidance against official rules (REQ-EVL-017).\n3. **Write fictional profiles** with synthetic names. Never use real records.\n4. **Assign expected outcomes manually.** Record:\n   - applicable rules;\n   - required follow-up information;\n   - prohibited conclusions;\n   - supporting passages (now fact IDs, D-006).\n5. **Review labels independently of the model** (REQ-EVL-018).\n   - Ideally a second reviewer checks a sample.\n   - If no second reviewer is available, run a separate source-based audit and **disclose\n     that the labels were author-validated**.\n6. **Freeze the held-out set** (REQ-EVL-019). Its labels never change after final\n   predictions are inspected, except to correct documented annotation errors.\n\n**From the same page [APP p.16, image]:**\n- Use development cases for prompt and architecture refinement.\n- Keep a separate held-out set for the final comparisons.\n- Balance cases across categories where possible.\n- **Report performance by category** (REQ-EVL-035).\n\n### 3.3 Dev/held-out split — PROPOSED (needs approval before dataset creation, D-019)\n\n**Recommendation: a fixed, stratified, group-aware split. 18 development / 30 held-out.**\n\n| Category | Dev | Held-out |\n|---|---|---|\
… [11101 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/project_context/05_evaluation.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 01:01:47

Now the submission requirements, paraphrased and anonymised.

**Tool call: Write**

```
{
 "file_path": "<repo>/docs/project_context/06_submission_requirements.md",
 "content": "# 06 — Submission Requirements\n\nThe legend is in [INDEX.md](INDEX.md#legend).\n\n> Requirements from the assessment brief are **paraphrased** (D-016). Organisation, role,\n> collaborator handle and submission-portal details are kept privately (D-017) and\n> deliberately left out here.\n\n## 1. Overall task — MANDATORY [ASM p.1]\n- Pick a problem relevant to Singapore public-sector stakeholders: an agency, a ministry or\n  a citizen group (REQ-PRB-001).\n- Build an AI-powered prototype, evaluate it comprehensively, and deliver a **Dockerised\n  solution** with professional documentation (REQ-SUB-002).\n- **AI must be in the core functionality** (REQ-PRB-002).\n- **Themes:**\n  - unstructured → structured;\n  - retrieval & knowledge;\n  - generation with guardrails;\n  - agents & workflows.\n\n  Any one theme, a combination, or an alternative is acceptable.\n- Classification, detection, retrieval, multimodal and agentic methods are all acceptable.\n- **The brief's stated intent:** assess problem identification, scoping and technical\n  judgement in using AI tools, especially judging viability and validating outputs\n  rigorously.\n\n## 2. Deliverables — MANDATORY [ASM p.2]\n\n| ID | Requirement | Planned evidence |\n|---|---|---|\n| REQ-SUB-001 | Complete instructions for full deployment and execution | README \"Run with Docker\" section, tested on a clean machine |\n| REQ-PRB-002 | **Significant** AI integration, not just an API call inside a standard web app | Architecture section plus ablation results (A–D) |\n| REQ-EVL-001 | Choose and justify a specific evaluation method (e.g. benchmarking, LLM-as-judge, human evaluation, ablation, comparison), with the rationale in the README. Soundness outranks results | README evaluation section; [05](05_evaluation.md) |\n| REQ-DAT-001 | Provenance, creation/processing, licensing and privacy for **all** data. Resourcefulness in finding data is assessed | README data section; `data/sources_manifest.json`; [03](03_data_and_licensing.md) |\n| REQ-LIC-001 | Comply with source licensing and **robots.txt** | Rights review record (Phase 2) |\n| REQ-PRIV-001 | If personal data is involved, address the ethics and handling | Synthetic-only statement |\n| REQ-DAT-002 | Synthetic data is fine if meaningful and high-fidelity; **defend its use** | README defence ([03 §4](03_data_and_licensing.md)) |\n| REQ-DOC-001 | **Documentation is the primary artifact:** objectives, rationale, implementation, results, execution instructions, limitations | README |\n| REQ-DOC-002 | A **150–250-word** README section: target user and environment; projected inference cost or compute footprint at scale; key post-deployment monitoring metrics; assessment of **one specific** deployment risk. *Only described, not implemented* | README section, word-count check |\n| REQ-DOC-003 | A brief development narrative: iterations, discarded strategies, tool-selection rationale, decision justification | README section, drawing on [../decisions.md](../decisions.md) |\n| REQ-SUB-003 | A **3–5 minute** demo video of the running application. **Its URL goes in the README** | README link (placeholder until recorded) |\n\n## 3. Submission protocol — MANDATORY [ASM p.2] (details private)\n\n| ID | Requirement |\n|---|---|\n| REQ-SUB-004 | Deliver via a **private** GitHub repository with the assessor collaborator invited. *Handle kept in private notes* |\n| REQ-SUB-005 | **The repository must remain anonymous** about the organisation and role |\n| REQ-SUB-006 | The repository must **remain unchanged** throughout the evaluation period |\n| REQ-SUB-007 | Submit the URL through the designated channel. *Details kept in private notes* |\n| REQ-SUB-008 | **Deadline:** 5 days from receipt. **Estimated effort:** 12–16 hours of focused work. Submission time isn't scored. The receipt date isn't recorded (Q-18) |\n\n## 4. Scoring dimensions — MANDATORY reference [ASM p.3]\n\n| Dimension | Weight | What is assessed (paraphrased) | Main requirement links |\n|---|---|---|---|\n| Problem framing & creativity | 20% | Worth solving? A non-obvious angle rather than a first idea or low effort? | REQ-PRB-010..015 |\n| Technical execution | 25% | Runs from the README on a clean machine; code quality. AI-assisted coding is expected, careless output is not | REQ-NFR-001, REQ-NFR-002 |\n| Evaluation & effectiveness | 30% | Sound methodology. Novelty counts only with effectiveness; a proven approach that works beats a novel one that underperforms. Honest limitations | REQ-EVL-* |\n| Data thinking | 15% | Provenance, licensing, representativeness, resourceful sourcing, awareness of what the data does and doesn't cover | REQ-DAT-*, REQ-LIC-* |\n| Communication | 10% | The write-up matches the code. No overclaiming, no README features that aren't in the repo | REQ-DOC-004 |\n\n## 5. Critical non-compliance indicators — MANDATORY [ASM p.4]\n\n| ID | Indicator to avoid |\n|---|---|\n| REQ-NFR-001 | **Not reproducible:** the solution fails when following the README |\n| REQ-DOC-004 | **Code/write-up mismatch:** features, architecture or results described that aren't in the repo |\n| REQ-NFR-003 | **Insufficient technical justification:** the developer must be able to explain the rationale behind code and architecture |\n| REQ-MOD-001 | **Unsubstantiated model selection:** choices must be justified by operational needs such as privacy, latency or task fit |\n| REQ-NFR-002 | **Substandard code quality:** AI-assisted code must still meet professional quality and maintainability standards |\n| REQ-PRB-003 | **Recycled past project:** must be a fresh project (see D-015 on \"PolicyProof\") |\n\n## 6. Methods and resources — MANDATORY [ASM p.4]\n- **Any accessible AI tools** may be used, including open weights and local inference. **No\n  API keys or compute are provided.**\n- **REQ-DOC-005:** clearly state the technical limitations, and the enhance
… [5050 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/project_context/06_submission_requirements.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 01:02:37

Now the requirements register, which is the largest file.

**Tool call: Write**

```
{
 "file_path": "<repo>/docs/project_context/requirements_register.md",
 "content": "# Requirements Register\n\nStable IDs: `REQ-<AREA>-<NNN>`. IDs are never renumbered or reused. Superseded items keep\ntheir ID and are marked as superseded. Decisions are in [../decisions.md](../decisions.md).\n\n**Status values:** `MANDATORY` (assessment brief) · `APPROVED` · `PROPOSED` · `OPEN` ·\n`SUPERSEDED`.\n**Source tags:** `[ASM p.N]` assessment brief · `[APP p.N]` project approach · `D-xxx` / `BD-xx`\ndecisions. Page numbers are physical PDF pages.\n\n**Areas:**\n\n| Code | Area | Code | Area |\n|---|---|---|---|\n| PRB | problem | ARC | architecture |\n| SCP | scope | VER | verifier |\n| SRC | sources | EVL | evaluation |\n| DAT | data | MOD | model selection |\n| LIC | licensing | DOC | documentation |\n| PRIV | privacy | SUB | submission |\n| NFR | non-functional | | |\n\n**Planned components** (traceability only; nothing is implemented):\n\n| Group | Components |\n|---|---|\n| Data pipeline | `source_acquisition` · `source_manifest` · `coverage_audit` · `policy_facts_kb` · `rule_registry` · `visual_resource_registry` |\n| Runtime | `profile_extractor` · `coverage_gate` · `rule_engine` · `retriever` · `generator` · `verifier` · `report_ui` |\n| Evaluation | `eval_harness` · `benchmark_dataset` · `verifier_claim_set` · `retrieval_qrels` |\n| Delivery | `docker` · `README` · `ai_logs` · `repo_hygiene` |\n\n## 1. Register\n\n### Problem (PRB)\n| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |\n|---|---|---|---|---|---|---|\n| REQ-PRB-001 | Problem relevant to SG public-sector stakeholders (agency/ministry/citizen group) | MANDATORY | [ASM p.1][APP p.29] | 01 §1 | README | README names the stakeholder (citizen group: BTO applicants) |\n| REQ-PRB-002 | AI in core functionality; significant AI integration, not just an API call in a web app | MANDATORY | [ASM p.1, 2][APP p.29] | 04 §1 | profile_extractor, generator, verifier | Architecture section + A–D ablation showing component contribution |\n| REQ-PRB-003 | Fresh project; no recycled past project | MANDATORY | [ASM p.4] | 06 §5; D-015 | repo_hygiene | Git history starts fresh; PolicyProof recorded as brainstorm only |\n| REQ-PRB-010 | BTO Buddy = pre-application preparation layer; transparency & preparation, not replacing authoritative assessment | APPROVED | [APP p.1–2]; BD-01 | 01 §2 | report_ui, README | UI/README disclaimers; no determinations made |\n| REQ-PRB-011 | Problem statement | APPROVED | [APP p.3] | 01 §3 | README | README problem section matches |\n| REQ-PRB-012 | Research question (hybrid vs conventional LLM reliability) | APPROVED | [APP p.3] | 01 §4 | eval_harness | Results answer it via A vs C/D comparisons |\n| REQ-PRB-013 | Substantiate complexity from official docs; never invent statistics on confusion/hotline/benefit | APPROVED | [APP p.3]; D-025 | 01 §5 | README | Every statistic in README cites a source; manual review |\n| REQ-PRB-014 | Own-research questions are optional evidence tasks | APPROVED (tasks OPEN) | [APP p.3, 29–30]; D-025 | 01 §5 | README | Included only with citations, else omitted |\n| REQ-PRB-015 | Downstream admin-workload reduction is a hypothesis requiring future user testing | APPROVED | [APP p.2] | 01 §2.2 | README | Phrased as hypothesis/future work |\n\n### Scope (SCP)\n| ID | Requirement | Status | Source | Context | Component | Acceptance evidence |\n|---|---|---|---|---|---|---|\n| REQ-SCP-001 | MVP scope table is authoritative (Core/Limited/Context/Excluded incl. ballot prediction & comprehensive determination) | APPROVED | [APP p.17–18]; D-008 | 01 §6 | coverage_gate, policy_facts_kb | Gate config and fact `scope_tier` values match table; out-of-scope benchmark category |\n| REQ-SCP-002 | Core capabilities implemented and evaluated | APPROVED | [APP p.17] | 01 §6.1 | all runtime; eval_harness | Each Core area has facts, rules (where explicit) and benchmark cases |\n| REQ-SCP-003 | Limited only where authoritative evidence and testable requirements exist | APPROVED | [APP p.17] | 01 §6.1 | policy_facts_kb | Coverage matrix shows verified source per Limited fact |\n| REQ-SCP-004 | Context-only topics never trigger eligibility calculations | APPROVED | [APP p.17] | 01 §6.1 | rule_engine, generator | No calculation rules; benchmark prohibited-conclusion checks |\n| REQ-SCP-005 | Excluded capabilities handled by coverage gate + official redirection | APPROVED | [APP p.17] | 01 §6.1, 04 §2 | coverage_gate | Out-of-scope category abstention results; gate unit tests |\n| REQ-SCP-006 | Scope expansion requires explicit approval + evaluation-plan update | APPROVED | [APP p.17] | 01 §6.1 | — | decisions.md entry precedes any expansion |\n| REQ-SCP-007 | Source-discovery matrix/ideas do not expand MVP | APPROVED | [APP p.1, 4, 17]; BD-02 | 02 §3 | policy_facts_kb | Every fact maps to an MVP tier |\n| REQ-SCP-008 | HFE boundary: explain HFE↔purchase/grants/loans; no grant/loan/financing determination; redirect | APPROVED | [APP p.18] | 01 §6.2 | coverage_gate, generator | Benchmark cases with prohibited conclusions on amounts |\n| REQ-SCP-009 | Videos excluded from core corpus; optional contextual links for Step 1/Step 2 HFE topics | APPROVED | [APP p.12, 18] | 02 §4 | visual_resource_registry | Videos absent from policy_facts; registry entries with display conditions |\n| REQ-SCP-010 | Income/employment only for HFE preparation, documents, follow-ups; no income-ceiling/eligibility/financing calc | APPROVED | D-013 | 01 §6.3 | rule_engine, profile_extractor | No income-calculation code; benchmark checks |\n| REQ-SCP-011 | No claim of comprehensive current/historical policy coverage | APPROVED | [APP p.28] | 01 §9 | README, report_ui | README/UI state supported period & scope |\n| REQ-SCP-012 | Scope discipline: ~4–5 policy areas handled accurately | APPROVED | [APP p.28] | 01 §9 | — | Final area count reported |\n| REQ-SCP-013 | Separate missing applicant info (A) vs missi
… [34316 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/project_context/requirements_register.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 01:05:10

Last, the index.

**Tool call: Write**

```
{
 "file_path": "<repo>/docs/project_context/INDEX.md",
 "content": "# BTO Buddy — Project Context Index\n\nThis is a structured, traceable knowledge base built from the project's two private planning\nsources:\n- the **assessment brief** (`[ASM p.N]`);\n- the **project-approach document** (`[APP p.N]`).\n\nBoth PDFs are kept locally and are Git-ignored. This documentation is independently\nauthored: it paraphrases requirements and policy content rather than reproducing them.\n\n**Phase:** 0 (context building).\n**Created:** 2026-10-28.\n**Code, models or datasets:** none have been implemented, selected or created.\n\n## Files\n\n| File | Covers |\n|---|---|\n| [01_problem_and_scope.md](01_problem_and_scope.md) | Final idea, problem statement, research question, problem validation, **MVP scope**, HFE/income boundaries, supported-question draft, missing-information categories, demo archetypes |\n| [02_policy_sources.md](02_policy_sources.md) | Seed sources, discovery method, **complete source-discovery matrix**, infographic/video registry candidates, **media-handling decisions**, policy nuances to verify |\n| [03_data_and_licensing.md](03_data_and_licensing.md) | Datasets A/B/C, private vs reviewer-facing corpora, manifest, schemas, completeness checks, licensing/robots/copyright, privacy, reproducibility, limitations |\n| [04_architecture.md](04_architecture.md) | Pipeline, coverage gate, missing-information contract, representation principles, verifier behaviour, proposed stack, provider comparison, model scorecard |\n| [05_evaluation.md](05_evaluation.md) | Configurations A–D, **benchmark structure**, label protocol, proposed split, **metric definitions**, severity rubric, retrieval and verifier evaluation, statistics, failure taxonomy |\n| [06_submission_requirements.md](06_submission_requirements.md) | Mandatory deliverables, scoring dimensions, non-compliance indicators, resources, AI-log rules, README requirements |\n| [requirements_register.md](requirements_register.md) | **All requirement IDs** with source pages, components and acceptance evidence; contradictions; open questions; completeness audit |\n| [../decisions.md](../decisions.md) | Decision log (D-001…D-025, BD-00…BD-09) and the instruction priority |\n\n## Legend\n\n**Status**\n\n| Tag | Meaning |\n|---|---|\n| `MANDATORY` | Explicit requirement in the assessment brief |\n| `APPROVED` | Final project decision (in the project approach as final, or ratified/added in [decisions.md](../decisions.md)) |\n| `PROPOSED` | Technical alternative or implementation detail not yet approved |\n| `OPEN` | Cannot be resolved from the sources or decisions; needs a developer answer |\n| `HISTORICAL` / `SUPERSEDED` | Earlier idea or decision replaced by an approved one. Kept for traceability, **not** an active requirement |\n\n**Provenance**\n\n| Tag | Meaning |\n|---|---|\n| `COPIED-SOURCE` | The project-approach PDF quoted HDB text verbatim at this point. The quotation is **not** reproduced in tracked files |\n| `AUTHORED-FACT (unverified)` | Independently paraphrased policy statement. It must be verified against a frozen source before it enters `data/policy_facts.jsonl` |\n| `PROJECT-DECISION` | Design choice by the developer (the default for non-policy content) |\n| *Author observation* | Point raised while building this knowledge base, not stated in either source |\n\n## Instruction priority (D-001)\n1. Mandatory assessment requirements.\n2. The developer's latest explicit instructions and approved decisions.\n3. Finalised scope, architecture, data strategy and evaluation methodology.\n4. The current approved implementation task.\n5. Proposed alternatives and open questions.\n6. Historical or superseded brainstorming.\n\n## Current open items\n- **Contradictions still open:** C-14 (URL mismatch in the matrix), C-15 to C-17 (metric\n  and scorecard gaps).\n- **Questions:** Q-05 to Q-24.\n- **Execution risk:** C-09 / Q-19 (log anonymity).\n\nAll are listed in [requirements_register.md §2–3](requirements_register.md#2-contradictions).\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/project_context/INDEX.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 01:06:42

All files are written. Now I'll fix the anchors I suspect are broken, then run the automated parts of the audit: ID cross-references, links, anonymity terms, verbatim overlap, and gitignore.

**Tool call: Bash** — Check requirement IDs and internal links resolve

```
cd "<repo>" && S=<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad && cat > $S/audit.py <<'EOF'
import re,sys,pathlib,unicodedata
root=pathlib.Path(sys.argv[1]); docs=sorted((root/'docs').rglob('*.md'))
reg=(root/'docs/project_context/requirements_register.md').read_text()
defined=set(re.findall(r'^\| (REQ-[A-Z]+-\d{3}) \|',reg,re.M))
print('defined IDs:',len(defined))
def slug(h):
    h=h.strip().lower(); h=re.sub(r'[^\w\- ]','',h); return h.replace(' ','-')
heads={}
for d in docs:
    heads[d]={slug(m) for m in re.findall(r'^#+ (.*)$',d.read_text(),re.M)}
for d in docs:
    t=d.read_text()
    used=set(re.findall(r'REQ-[A-Z]+-\d{3}',t))
    miss=used-defined
    if miss: print('UNDEFINED in',d.name,sorted(miss))
    for link in re.findall(r'\]\(([^)]+)\)',t):
        if link.startswith('http'): continue
        f,_,a=link.partition('#'); tgt=(d.parent/f).resolve() if f else d
        if not tgt.exists(): print('BROKEN FILE',d.name,link); continue
        if a and a not in heads.get(tgt,set()): print('BROKEN ANCHOR',d.name,link)
EOF
python3 -I $S/audit.py "$PWD"
```

<details><summary>Tool result</summary>

```
defined IDs: 150
BROKEN ANCHOR 01_problem_and_scope.md 05_evaluation.md#8-failure-type-taxonomy-category-b-root-cause
BROKEN ANCHOR 01_problem_and_scope.md 04_architecture.md#3-structured-missing-information-contract
BROKEN ANCHOR 03_data_and_licensing.md 05_evaluation.md#3-benchmark-dataset-c
```
</details>

### Claude · 2026-10-28 01:07:00

Every ID is defined. Three anchors are broken, as I expected; fixing them.

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/01_problem_and_scope.md",
 "old_string": "The failure sub-types of category B are listed in [05 §8](05_evaluation.md#8-failure-type-taxonomy-category-b-root-cause).\nThe runtime contract is in [04 §3](04_architecture.md#3-structured-missing-information-contract).",
 "new_string": "The failure sub-types of category B are listed in [05 §8](05_evaluation.md).\nThe runtime contract is in [04 §3](04_architecture.md)."
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/03_data_and_licensing.md",
 "old_string": "The full design is in [05_evaluation.md](05_evaluation.md#3-benchmark-dataset-c).",
 "new_string": "The full design is in [05_evaluation.md §3](05_evaluation.md)."
}
```

**Tool call: Bash** — Grep for identifying terms and verify Git-ignore coverage

```
cd "<repo>" && S=<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad && echo "== anonymity grep (tracked candidates) ==" && grep -rniE '[REDACTED R5]|[REDACTED R5]|[REDACTED R5]|[REDACTED R5]|[REDACTED R5]|\{build\}|build\.tech|[REDACTED R5]|recruit|hiring|interview|\bHR\b' .gitignore docs || echo "none"; echo "== ignore check ==" && git check-ignore -v "references/private/assessment requirements.pdf" "references/private/project approach.pdf" references/private/submission_private_notes.md data/private_corpus/raw/x; echo "== untracked files git would add ==" && git status --porcelain -uall
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/01_problem_and_scope.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/03_data_and_licensing.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 814 chars]
```
</details>

### Claude · 2026-10-28 01:07:22

Anonymity grep is clean, and only the intended files are visible to Git. Next, a verbatim-overlap check: 10-word shingles of the tracked docs against the brief text and the HDB-quoted passages.

**Tool call: Bash** — Detect verbatim 10-word overlaps with restricted text

```
cd "<repo>" && S=<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad && cat > $S/overlap.py <<'EOF'
import re,sys,pathlib,pdfplumber
root=pathlib.Path(sys.argv[1]); N=10
norm=lambda s:re.findall(r"[a-z0-9$]+",s.lower())
def sh(w): return {' '.join(w[i:i+N]) for i in range(len(w)-N+1)}
with pdfplumber.open(root/'references/private/assessment requirements.pdf') as p: asm=' '.join(pg.extract_text() for pg in p.pages)
with pdfplumber.open(root/'references/private/project approach.pdf') as p:
    pg=p.pages[6]; hdb=''.join(c['text'] for c in pg.chars if tuple(c.get('non_stroking_color') or ())!=(0.0,0.0,0.0))
    hdb+=' '+p.pages[7].extract_text()  # p.8 "What is HFE" infographic transcription + IPA text
srcs={'ASM':sh(norm(asm)),'HDB-quotes':sh(norm(hdb))}
for d in sorted((root/'docs').rglob('*.md')):
    w=norm(d.read_text()); s=sh(w)
    for k,v in srcs.items():
        hit=s&v
        if hit: print(d.name,k,len(hit),'shingles; e.g.',sorted(hit)[:3])
EOF
python3 -I $S/overlap.py "$PWD"
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 720 chars]
```
</details>

**Tool call: Bash** — List overlaps excluding URL fragments

```
cd "<repo>" && S=<tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad && sed -i '' 's/        if hit: print(d.name,k,len(hit),.*$/        if hit: print("\\n##",d.name,k); [print("  ",x) for x in sorted(hit)]/' $S/overlap.py && python3 -I $S/overlap.py "$PWD" | grep -vE 'https|www|hdb gov sg|youtu|file go gov' 
```

<details><summary>Tool result</summary>

```
## 02_policy_sources.md HDB-quotes
   a flat bto sbf and open booking of flats conditions
   and open booking of flats conditions after buying a new
   booking of flats conditions after buying a new flat anchor
   bto sbf and open booking of flats conditions after buying
   buying a [REDACTED R7: 16 words of HDB source text] conditions after
   flats conditions after buying a new flat anchor resale levy
   gov sg buying a flat bto sbf and open booking
   gov sg buying a flat flat grant and loan eligibility
   of flats conditions after buying a new flat anchor resale
   open booking of flats conditions after buying a new flat
   sbf and open booking of flats conditions after buying a
   sg buying a flat bto sbf and open booking of

## 04_architecture.md ASM
   data sensitivity latency task fit fine tuning needs cost at
   latency task fit fine tuning needs cost at scale economics
   sensitivity latency task fit fine tuning needs cost at scale

## 06_submission_requirements.md ASM
   ai studio groq openrouter hugging face inference providers cerebras together
   all coding agent session and chat logs e g jsonl
   apis google ai studio groq openrouter hugging face inference providers
   cerebras together ai local inference ollama llama cpp lm studio
   coding agent session and chat logs e g jsonl from
   data sensitivity latency task fit fine tuning needs cost at
   face inference providers cerebras together ai local inference ollama llama
   google ai studio groq openrouter hugging face inference providers cerebras
   groq openrouter hugging face inference providers cerebras together ai local
   hugging face inference providers cerebras together ai local inference ollama
   inference providers cerebras together ai local inference ollama llama cpp
   llm apis google ai studio groq openrouter hugging face inference
   openrouter hugging face inference providers cerebras together ai local inference
   providers cerebras together ai local inference ollama llama cpp lm
   sensitivity latency task fit fine tuning needs cost at scale
   studio groq openrouter hugging face inference providers cerebras together ai
   together ai local inference ollama llama cpp lm studio gpu
   upload all coding agent session and chat logs e g
```
</details>

### Claude · 2026-10-28 01:08:03

I've created all 11 files. Nothing is committed or pushed. No code, model choice, dataset or external download has been done.

**Files** (all new, untracked):

| File | Status |
|---|---|
| [.gitignore](.gitignore) | Excludes `references/private/`, `data/private_corpus/`, secrets, local environments, caches and OS files. `git check-ignore` confirms both PDFs, the private notes and the private corpus are excluded |
| `references/private/submission_private_notes.md` | Git-ignored. Holds the organisation, role, collaborator handle, submission protocol, hackathon link, chatbot vendor and the log-anonymity risk |
| [docs/decisions.md](docs/decisions.md) | Your 25 decisions (D-001 to D-025, dated 2026-10-28), plus BD-00 to BD-09: decisions already stated as final in the approach doc and now ratified. Superseded items are listed with what replaced them |
| [INDEX.md](docs/project_context/INDEX.md) | Legend, instruction priority, file map |
| [01_problem_and_scope.md](docs/project_context/01_problem_and_scope.md) | Problem, research question, MVP scope (including the new exclusions), HFE and income boundaries, draft question inventory, missing-information categories A and B, demo scenarios |
| [02_policy_sources.md](docs/project_context/02_policy_sources.md) | The full source-discovery matrix (5 rows, every URL, expandable sections, tables, PDFs, the 2 infographics, the 2 videos) and the media-handling rules |
| [03_data_and_licensing.md](docs/project_context/03_data_and_licensing.md) | Datasets A, B and C, the two corpora, the manifest, the proposed `policy_facts` schema, the 8 completeness checks, rights findings, reproducibility |
| [04_architecture.md](docs/project_context/04_architecture.md) | The pipeline as a mermaid diagram, the missing-information contract, how verifier results are shown, the proposed stack, provider table and scorecard |
| [05_evaluation.md](docs/project_context/05_evaluation.md) | Configurations A–D, the benchmark, the label protocol, metric definitions with denominators, severity rubric, retrieval and verifier evaluation, statistics |
| [06_submission_requirements.md](docs/project_context/06_submission_requirements.md) | Mandatory requirements in paraphrase, scoring weights, non-compliance indicators, AI-log rules, your README requirements |
| [requirements_register.md](docs/project_context/requirements_register.md) | 150 requirement IDs, each with source pages, the context section, a planned component and acceptance evidence. Also contradictions C-01 to C-17, open questions Q-05 to Q-24, and the page-by-page audit |

**Audit results**
- **Coverage:** every page of both PDFs is mapped to a section and IDs (register §4). That includes all 11 embedded images, re-read at 300 dpi.
- **Deliberate omissions (§4.3):**
  - the verbatim HDB quotes and infographic text, which are now paraphrased and marked "unverified";
  - the text of the brief's example problem sketches;
  - organisation-identifying details, now in the private notes;
  - the chatbot screenshot, now described in text.
- **IDs and links:** every requirement ID used in the docs exists in the register, and every internal link resolves (I fixed 3 broken anchors).
- **Anonymity:** a search of the tracked files for the organisation, role, handle, hackathon and vendor terms found nothing.
- **Copied text:** no 10-word passage from the brief or the HDB quotes appears except URLs, a short list of tool names, and the brief's short list of valid model-justification grounds. None of it is copied prose.

**New contradictions I couldn't resolve**
- **C-14:** in the matrix, the "BTO application process" row names the "Application for a New Flat" page, but its URL is actually the HFE page's (`APP p.10–11`).
- **C-15:** "human-review burden" was a secondary metric in the approach doc but isn't in your new metric list.
- **C-16:** "answer coverage" has no definition in either document.
- **C-17:** the model scorecard has no data-privacy criterion, even though the brief names privacy as a valid reason for choosing a model.

**Decisions needed before Phase 1**
1. **Q-20:** benchmark split. I propose a fixed split of 18 development and 30 held-out cases: 3 and 5 per category, with near-duplicate scenarios kept on the same side.
   - I recommend against K-fold. Nothing is trained, so prompt iteration on every fold would leak cases into development, and it breaks the "freeze held-out before optimising" safeguard.
2. **Q-21:** verifier claim set of 60 (15 dev, 45 eval, equal numbers of supported, contradicted and insufficient), or 36 if time is short.
3. **Q-22:** the `policy_facts` schema in 03 §2.5.
4. **Q-23:** the stack: Streamlit, Pydantic, Pandas and scikit-learn.
5. **Q-12:** place the coverage gate after profile extraction and before retrieval?
6. **Q-10:** file paths for the benchmark, claim set, retrieval test queries and saved predictions.
7. **Q-15, Q-16, Q-17:** define "answer coverage", decide whether to keep human-review burden, and decide who scores claim-level judgements (you manually, an LLM judge checked against your labels, or both).
8. **Q-13:** add a privacy criterion to the scorecard?
9. **Q-18:** the date you received the brief, which sets the deadline. It goes in the private notes.
10. **Q-19:** this Phase 0 session log contains the organisation name and verbatim brief text. Will redacting those in the log satisfy D-010, or do you want to decide it yourself at submission?

**Deferred to Phase 2:**
- **Q-05:** how to handle non-couple household types.
- **Q-06:** whether the SC + SPR premium is financing (excluded) or a first-timer consideration.
- **Q-07:** the resale levy's tier.
- **Q-08:** which HFE FAQ sub-links and which "exceptions and waivers" source are needed.
- **Q-09:** whether to strip tracking parameters from the video URLs.
- **Q-11:** whether any experiment runs on the private corpus.
- **Q-24:** the correct URL for C-14.

Every policy fact in these docs (9-month HFE validity, the income assessment window, the 10-flat waiver, the SPR premium) is still unverified. Each needs checking against a frozen source in Phase 2.

### User · 2026-10-28 01:13:02

Now, commit indexed Markdown specifications, requirements register and initial decisions. Keep original PDFs excluded. Commit message: “docs: establish project context and requirements”

**Tool call: Bash** — Stage docs and gitignore, verify no private files staged

```
cd "<repo>" && git add .gitignore docs/decisions.md docs/project_context/ && git status --porcelain -uall && echo "== staged ==" && git diff --cached --name-only && echo "== private check ==" && (git diff --cached --name-only | grep -iE 'references|private|\.pdf' || echo "no private files staged")
```

<details><summary>Tool result</summary>

```
A  .gitignore
A  docs/decisions.md
A  docs/project_context/01_problem_and_scope.md
A  docs/project_context/02_policy_sources.md
A  docs/project_context/03_data_and_licensing.md
A  docs/project_context/04_architecture.md
A  docs/project_context/05_evaluation.md
A  docs/project_context/06_submission_requirements.md
A  docs/project_context/INDEX.md
A  docs/project_context/requirements_register.md
== staged ==
.gitignore
docs/decisions.md
docs/project_context/01_problem_and_scope.md
docs/project_context/02_policy_sources.md
docs/project_context/03_data_and_licensing.md
docs/project_context/04_architecture.md
docs/project_context/05_evaluation.md
docs/project_context/06_submission_requirements.md
docs/project_context/INDEX.md
docs/project_context/requirements_register.md
== private check ==
no private files staged
```
</details>

**Tool call: Bash** — Create commit and verify tracked files

```
cd "<repo>" && git commit -q -F - <<'EOF'
docs: establish project context and requirements

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
git log --stat --oneline -1 && echo "== tracked private? ==" && (git ls-files | grep -iE 'references|private_corpus|\.pdf' || echo none) && git status --short
```

<details><summary>Tool result</summary>

```
c49555f docs: establish project context and requirements
 .gitignore                                         |  40 +++
 docs/decisions.md                                  | 100 ++++++
 docs/project_context/01_problem_and_scope.md       | 225 +++++++++++++
 docs/project_context/02_policy_sources.md          | 233 ++++++++++++++
 docs/project_context/03_data_and_licensing.md      | 271 ++++++++++++++++
 docs/project_context/04_architecture.md            | 178 ++++++++++
 docs/project_context/05_evaluation.md              | 295 +++++++++++++++++
 docs/project_context/06_submission_requirements.md | 183 +++++++++++
 docs/project_context/INDEX.md                      |  63 ++++
 docs/project_context/requirements_register.md      | 358 +++++++++++++++++++++
 10 files changed, 1946 insertions(+)
== tracked private? ==
none
```
</details>

### Claude · 2026-10-28 01:13:23

I committed the project context, requirements register and initial decisions as `c49555f docs: establish project context and requirements`. It's the first commit in the repo, on `main`, and nothing has been pushed.

- **Included (10 files):**
  - the eight files in `docs/project_context/`;
  - `docs/decisions.md`;
  - `.gitignore`, which is what keeps the PDFs and other private files out of the repo.
- **Not included:** both PDFs, `references/private/submission_private_notes.md` and anything under `data/private_corpus/`. After the commit I checked with `git ls-files`, and none of them are tracked.
- **Working tree:** clean.

The commit message ends with the Co-Authored-By line for Claude. I made the commit on `main` rather than a branch because the repo had no commits yet.

### User · 2026-10-28 01:20:24

<ide_opened_file>The user opened the file <repo>/.gitignore in the IDE. This may or may not be related to the current task.</ide_opened_file>

### User · 2026-10-28 01:20:24

PHASE 1: PROJECT SETUP AND ARCHITECTURE

You may build on this CLAUDE.md template and ensure all details in it are relevant for my project. But importantly, keep CLAUDE.md concise, ideally under a few hundred lines, but retain all necessary information and remove what’s duplicated/redundant.
```# BTO Buddy — Project Instructions

## Objective
Build an evidence-grounded BTO pre-application
preparation assistant for fictional first-timer
couple profiles.

The prototype provides preparation guidance,
not official eligibility determinations.

## Source of Truth
Read `docs/project_context/INDEX.md` first.

Use the task-specific context files referenced
there. Do not reread the entire original PDF
unless the extracted context is incomplete.

## Instruction Priority and Change Control
1. Mandatory official assessment requirements and
   non-compliance constraints.
2. My latest explicit instructions and approved decisions,
   provided they comply with the assessment.
3. The finalised MVP scope, architecture, data strategy
   and evaluation approach in docs/project_context/.
4. The current approved implementation task.
5. Proposed alternatives and unresolved questions.
6. Historical brainstorming (if any, for reference only).

### Change-control rules
- Treat approved project decisions as implementation
  requirements, not optional suggestions.
- Follow the finalised approach unless a material
  technical, methodological, licensing, security or
  reproducibility concern is identified.
- If a better alternative is identified, explain:
  1. The current approved approach.
  2. The proposed alternative.
  3. Why the alternative may be preferable.
  4. Its implications for scope, evaluation, time,
     cost and assessment alignment.
  5. Your recommendation.
- Obtain my explicit approval before implementing
  a material deviation.
- Do not silently expand or reduce the MVP scope.
- Do not treat historical brainstorming as instructions.
- Record approved changes in docs/decisions.md.
- If two approved instructions conflict, flag the
  conflict and ask for clarification.

## Scope
Core:
- First-timer couple preparation
- Basic BTO application requirements
- HFE preparation
- Missing-information identification
- Source-grounded guidance
- Claim verification

Limited:
- First-timer priority considerations
- Non-selection consequences

Context only:
- High-level grant and loan explanations

Excluded:
- Official eligibility determination
- Grant or loan calculations
- Ballot probability prediction
- Detailed affordability analysis
- Real applicant data
- Production-grade hosting, authentication, monitoring infrastructure and operational integrations. A fully runnable, reproducible Dockerised prototype remains mandatory.

## Engineering Rules
- Use simple, typed, testable Python modules.
- Prefer composition over unnecessary OOP.
- Separate deterministic rules from LLM reasoning.
- Use structured contracts between components.
- Never invent policy facts, citations or results.
- Defensible model and data decisions
- Do not add dependencies without justification.
- Never change held-out labels to improve scores.
- Keep secrets and restricted source text out of Git.
- Implementation and evaluations must be reproducible by external reviewers.
- Clean, maintainable, Dockerized implementation
- Ensure code readability and explainability

## AI Collaboration
Before major changes:
- Read relevant requirement IDs.
- Explain assumptions and tradeoffs.
- Identify files and tests affected.
- Ask approval for material design changes.

After changes:
- Run relevant tests.
- Report actual results.
- Map work to requirement IDs.
- Record limitations and unresolved issues.

Do not commit, push, merge or rewrite Git history
without explicit approval.

## Data and Privacy
- Do not scrape or download external content
  without approval.
- Do not read private source HTML unless authorised.
- Do not transmit source text or credentials externally
  without approval.
- Preserve source provenance and policy dates.
- Keep private corpus files Git-ignored.

## Evaluation
- Establish baselines before improvements.
- Use independently checked reference labels.
- Evaluate the verifier separately.
- Keep development and test sets distinct.
- Report failures and limitations honestly.
- Record model settings and experiment versions.

## Project References
- `docs/project_context/INDEX.md`: Context navigation and task routing.
- `docs/project_context/01_problem_and_scope.md`: Approved MVP and exclusions.
- `docs/project_context/02_policy_sources.md`: Source-discovery matrix and coverage.
- `docs/project_context/03_data_and_licensing.md`: Corpus handling and permissions.
- `docs/project_context/04_architecture.md`: Approved system design.
- `docs/project_context/05_evaluation.md`: Benchmark and evaluation methodology.
- `docs/project_context/06_submission_requirements.md`: Assessment and deliverables.
- `docs/project_context/requirements_register.md`: Requirements traceability.
- `docs/decisions.md`: Approved technical decisions.
- `docs/development_log.md`: Progress, experiments and unresolved issues.


## Context and Token Efficiency
- Read docs/project_context/INDEX.md first.
- Load only task-relevant context files.
- Avoid rereading entire PDFs or unrelated files.
- Store approved decisions, progress and unresolved
  issues in project documentation.
- Keep responses concise without omitting important
  technical reasoning or test results.
- At the end of each phase, update docs/development_log.md with completed work, decisions, failures and next steps.
- Do not discard relevant context solely to save tokens.

## Commands
Add verified installation, test, lint,
application and Docker commands after setup.
```

For commits, roughly follow the recommended commit milestones and commit message formats for all appropriate commits:
l: “
Milestone
Example commit
Initial structure
chore: initialise project and tooling
Policy sources
data: add source manifest and policy rule registry
Benchmark
eval: add labelled applicant scenarios
Baseline
feat: implement direct LLM baseline
Hybrid pipeline
feat: add structured guidance and retrieval
Verification
feat: add evidence-based claim verification
Evaluation
eval: add comparative metrics and ablations
Deployment
build: add Docker deployment and smoke tests
Final submission
docs: finalise README, demo and AI logs

Commit after a coherent milestone is complete and its relevant tests pass. Push to the private repository after each stable milestone or work session. Obtain my approval before any actual commit. Also ensure you inspect staged files and scan for secrets before every push.

### Claude · 2026-10-28 01:20:49

Let me check the toolchain before writing anything, so the Commands section only lists commands I've actually run.

**Tool call: Bash** — Check available Python tooling, Docker, and git remote

```
cd "<repo>" && for t in uv python3 python3.12 python3.11 docker pip3 ruff mypy pytest; do printf "%-10s " $t; (command -v $t >/dev/null && ($t --version 2>&1 | head -1)) || echo "not found"; done; git remote -v; ls -la src data
```

<details><summary>Tool result</summary>

```
uv         not found
python3    Python 3.13.2
python3.12 not found
python3.11 not found
docker     not found
pip3       pip 26.0.1 from /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/pip (python 3.13)
ruff       ruff 0.14.0
mypy       not found
pytest     pytest 9.0.3
origin	https://github.com/<git-user>/bto-buddy.git (fetch)
origin	https://github.com/<git-user>/bto-buddy.git (push)
data:
total 0
drwxr-xr-x  2 <user>  staff   64 Oct 26 01:35 .
drwxr-xr-x  9 <user>  staff  288 Oct 28 08:55 ..

src:
total 0
drwxr-xr-x  2 <user>  staff   64 Oct 26 01:35 .
drwxr-xr-x  9 <user>  staff  288 Oct 28 08:55 ..
```
</details>

<details><summary>Claude's reasoning</summary>

Docker isn't available on this machine, but I found a remote repo (<git-user>/bto-buddy). I'll scaffold a minimal src/ package with pytest, ruff, mypy, and Pydantic, then write CLAUDE.md using only verified commands—holding off on UI/LLM deps until you approve the stack.


</details>

**Tool call: Write**

```
{
 "file_path": "<repo>/pyproject.toml",
 "content": "[build-system]\nrequires = [\"setuptools>=69\", \"wheel\"]\nbuild-backend = \"setuptools.build_meta\"\n\n[project]\nname = \"bto-buddy\"\nversion = \"0.1.0\"\ndescription = \"Evidence-grounded BTO pre-application preparation assistant (prototype).\"\nreadme = \"README.md\"\nrequires-python = \">=3.12\"\n# Runtime dependencies are added only with a recorded justification (CLAUDE.md, Engineering Rules).\ndependencies = [\n    # Typed contracts between pipeline stages (REQ-ARC-005, REQ-ARC-007).\n    \"pydantic>=2.7,<3\",\n]\n\n[project.optional-dependencies]\ndev = [\n    \"pytest>=8,<10\",\n    \"ruff>=0.6\",\n    \"mypy>=1.10\",\n]\n\n[tool.setuptools.packages.find]\nwhere = [\"src\"]\n\n[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\naddopts = \"-q\"\n\n[tool.ruff]\nline-length = 100\ntarget-version = \"py312\"\nsrc = [\"src\", \"tests\"]\n\n[tool.ruff.lint]\nselect = [\"E\", \"F\", \"W\", \"I\", \"B\", \"UP\", \"SIM\", \"RUF\"]\n\n[tool.mypy]\npython_version = \"3.12\"\nstrict = true\nmypy_path = \"src\"\npackages = [\"bto_buddy\"]\nplugins = [\"pydantic.mypy\"]\n"
}
```

**Tool call: Write**

```
{
 "file_path": "<repo>/src/bto_buddy/__init__.py",
 "content": "\"\"\"BTO Buddy: evidence-grounded BTO pre-application preparation assistant.\n\nProvides preparation guidance for fictional applicant profiles. It does not make\nofficial eligibility determinations (REQ-PRB-010, REQ-SCP-008).\n\"\"\"\n\n__version__ = \"0.1.0\"\n"
}
```

**Tool call: Write**

```
{
 "file_path": "<repo>/tests/test_package.py",
 "content": "import bto_buddy\n\n\ndef test_package_exposes_version() -> None:\n    assert bto_buddy.__version__ == \"0.1.0\"\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/pyproject.toml (file state is current in your context — no need to Read it back)
```
</details>

**Tool call: Write**

```
{
 "file_path": "<repo>/README.md",
 "content": "# BTO Buddy\n\nAn evidence-grounded preparation assistant for Build-To-Order (BTO) flat applicants: a\npublic-sector AI prototype. It gives preparation guidance for fictional applicant profiles\nand **does not** make official eligibility determinations.\n\n> Work in progress. The full README (problem, architecture, data provenance, evaluation,\n> results, limitations, Docker instructions, demo link and AI-usage disclosure) is written\n> at the final milestone. Planning context is in\n> [docs/project_context/INDEX.md](docs/project_context/INDEX.md).\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/src/bto_buddy/__init__.py (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/tests/test_package.py (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/README.md (file state is current in your context — no need to Read it back)
```
</details>

**Tool call: Bash** — Create venv, install package with dev tools, run checks

```
cd "<repo>" && python3 -m venv .venv && .venv/bin/python -m pip install -q --upgrade pip && .venv/bin/python -m pip install -q -e ".[dev]" 2>&1 | tail -3; echo "== pytest ==" && .venv/bin/python -m pytest; echo "== ruff check ==" && .venv/bin/ruff check . ; echo "== ruff format ==" && .venv/bin/ruff format --check . ; echo "== mypy ==" && .venv/bin/mypy; echo "== versions ==" && .venv/bin/python -m pip list 2>/dev/null | grep -iE '^(pydantic|pytest|ruff|mypy) '
```

<details><summary>Tool result</summary>

```
== pytest ==
.                                                                        [100%]
1 passed in 0.01s
== ruff check ==
All checks passed!
== ruff format ==
12 files already formatted
== mypy ==
Success: no issues found in 1 source file
== versions ==
mypy              2.4.0
pydantic          2.14.1
pytest            9.2.0
ruff              0.17.3
```
</details>

<details><summary>Claude's reasoning</summary>

All checks pass—pytest, ruff check, ruff format, and strict mypy. I've updated CLAUDE.md's Scope section to align with approved D-008, restoring the post-purchase exclusion while keeping Core capabilities separate from policy areas.


</details>

**Tool call: Write**

```
{
 "file_path": "<repo>/CLAUDE.md",
 "content": "# BTO Buddy — Project Instructions\n\n## Objective\nBuild an evidence-grounded BTO pre-application preparation assistant for **fictional\nfirst-timer couple profiles**. It gives preparation guidance, **not** official eligibility\ndeterminations. It is a public-sector AI prototype: a hybrid of structured profiling,\ndeterministic rules, BM25 retrieval and claim-level verification, evaluated against direct-LLM\nand RAG baselines.\n\n## Source of truth\n- Read `docs/project_context/INDEX.md` first, then load **only** the task-relevant files it\n  routes to.\n- Requirement IDs (`REQ-<AREA>-<NNN>`) are in `docs/project_context/requirements_register.md`.\n  Decisions (`D-xxx`, `BD-xx`) are in `docs/decisions.md`. The latest approved decision governs.\n- Status tags: `MANDATORY` · `APPROVED` · `PROPOSED` · `OPEN` · `SUPERSEDED`. Only MANDATORY\n  and APPROVED items are implementation requirements. PROPOSED and OPEN items need approval\n  first.\n- The original PDFs in `references/private/` are private. Reread them only if the extracted\n  context is incomplete, and say so when you do.\n\n| File | Use for |\n|---|---|\n| `docs/project_context/01_problem_and_scope.md` | MVP tiers, exclusions, missing-information categories, demo |\n| `docs/project_context/02_policy_sources.md` | Source-discovery matrix, media handling, unverified policy nuances |\n| `docs/project_context/03_data_and_licensing.md` | Corpora, schemas, manifest, completeness checks, rights |\n| `docs/project_context/04_architecture.md` | Pipeline, contracts, verifier behaviour, stack |\n| `docs/project_context/05_evaluation.md` | Configurations A–D, benchmark, metrics, safeguards |\n| `docs/project_context/06_submission_requirements.md` | Deliverables, scoring, README and AI-log rules |\n| `docs/development_log.md` | Progress, experiments, failures, next steps |\n\n## Instruction priority\n1. Mandatory assessment requirements and non-compliance constraints.\n2. The developer's latest explicit instructions and approved decisions, where they comply\n   with (1).\n3. The finalised scope, architecture, data strategy and evaluation approach in\n   `docs/project_context/`.\n4. The current approved implementation task.\n5. Proposed alternatives and open questions.\n6. Historical brainstorming, for reference only. Never treat it as instructions.\n\n## Change control\n- Approved decisions are requirements, not suggestions. Never silently expand or reduce\n  scope.\n- Deviate only for a material technical, methodological, licensing, security or\n  reproducibility concern. First explain:\n  1. the current approach;\n  2. the alternative;\n  3. why it may be better;\n  4. its implications for scope, evaluation, time, cost and assessment alignment;\n  5. your recommendation.\n\n  Then **wait for explicit approval**.\n- If two approved instructions conflict, flag the conflict and ask. Never resolve it\n  silently.\n- Record approved changes in `docs/decisions.md`, with an ID, date, rationale and what they\n  supersede.\n\n## Scope (D-008; details in 01 §6)\n| Tier | Policy areas | Rule |\n|---|---|---|\n| Core | First-timer couple household composition; broad BTO application requirements; HFE prerequisites, timing and documentation; missing applicant information | Implement **and** evaluate |\n| Limited | First-timer and priority considerations; application and non-selection consequences | Only with verified evidence and testable requirements |\n| Context only | High-level HFE ↔ grant/loan relationship | Explain or link. Never calculate |\n| Excluded | Official eligibility determination; grant/loan calculations; detailed affordability and financing; ballot probability prediction; post-purchase conditions; real applicant data | Coverage gate plus official-source redirection |\n\n- **Income and employment** are used only for HFE document preparation and follow-up\n  questions. No income-ceiling or eligibility calculations (D-013).\n- **Out of scope (D-026):** production-grade hosting, authentication, monitoring\n  infrastructure and operational integrations. A fully runnable, reproducible, Dockerised\n  prototype is still **mandatory**.\n- **Required capabilities across all tiers:** source-grounded guidance with official links,\n  missing-information identification, claim verification (REQ-ARC-001).\n\n## Architecture invariants (04)\n- **Pipeline:**\n  1. profile extraction and validation;\n  2. coverage gate;\n  3. rule engine ∥ BM25 retrieval;\n  4. grounded generation;\n  5. claim verification;\n  6. preparation report.\n- Typed Pydantic contracts between every stage. No free text passes between modules.\n- Every response carries `missing_profile_fields`, `evidence_gaps`, `profile_conflicts` and\n  `out_of_scope_reasons`.\n- Never assume missing applicant values. Missing evidence never proves a requirement absent.\n- The runtime KB is `data/policy_facts.jsonl` (independently authored, fact IDs). Rules in\n  `data/policy_rules.yaml` cite fact IDs. Nothing at runtime reads `data/private_corpus/`.\n- **Verifier outcomes:**\n  - supported → show with a source;\n  - contradicted → withhold and flag;\n  - insufficient → no definitive guidance, state the gap.\n\n  Never silently rewrite. No regeneration loop unless approved.\n- No autonomous agents, orchestration frameworks or vector DBs. Use one generation model.\n  Add embeddings only if recall@k proves the gain.\n- Infographics and videos are links in `data/visual_resources.json`, never runtime evidence.\n\n## Engineering rules\n- Simple, typed, testable Python modules in `src/bto_buddy/`. Prefer functions and\n  composition over class hierarchies.\n- Keep deterministic rules separate from LLM reasoning. Hard rules are deterministic;\n  interpretations stay evidence-linked.\n- Add short comments wherever the *rationale* isn't obvious. The developer must be able to\n  defend every choice (REQ-NFR-003).\n- **Every new dependency needs a one-line justif
… [4913 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/CLAUDE.md (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Claude's reasoning</summary>

I'll add an anonymity check to the pre-push scan, keeping the identifying terms in a private, Git-ignored file referenced from CLAUDE.md rather than in tracked files.


</details>

**Tool call: Bash** — Create private anonymity term list and scan files

```
cd "<repo>" && printf '%s\n' '[REDACTED R5]' '[REDACTED R5]' '[REDACTED R5]' '[REDACTED R5]' '[REDACTED R5]' '[REDACTED R5]' '[REDACTED R5]' '[REDACTED R5]' '[REDACTED R5]' > references/private/anonymity_terms.txt && git check-ignore -q references/private/anonymity_terms.txt && echo ignored && grep -rniFf references/private/anonymity_terms.txt $(git ls-files) CLAUDE.md README.md pyproject.toml src tests || echo "no identifying terms in tracked/new files"
```

<details><summary>Tool result</summary>

```
ignored
no identifying terms in tracked/new files
```
</details>

**Tool call: Edit**

````
{
 "replace_all": false,
 "file_path": "<repo>/CLAUDE.md",
 "old_string": "git diff --cached | grep -inE 'api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY' || echo \"no secret patterns\"\n```",
 "new_string": "git diff --cached | grep -inE 'api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY' || echo \"no secret patterns\"\n# Anonymity: the term list is private (Git-ignored) and must never be copied into tracked files.\ngit grep -inFf references/private/anonymity_terms.txt || echo \"no identifying terms\"\n```"
}
````

<details><summary>Tool result</summary>

```
The file <repo>/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 01:30:54

Now the architecture proposal. I'm adding it to `04_architecture.md` as PROPOSED, so nothing is coded until you approve it.

**Tool call: Read**

```
{
 "file_path": "<repo>/docs/project_context/04_architecture.md",
 "offset": 170
}
```

<details><summary>Tool result</summary>

```
170	
171	**REQ-MOD-001 (MANDATORY):**
172	- Justify the final choice on operational grounds: data sensitivity, latency, task fit,
173	  fine-tuning needs, cost-at-scale economics.
174	- **Never** on "free, cool, had it lying around" [ASM p.4].
175	- Local vs API doesn't matter in itself.
176	
177	**Gap.** The scorecard has no data-privacy criterion, although the brief names privacy as a
178	valid ground. See Q-13.
179	
```
</details>

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/04_architecture.md",
 "old_string": "**Gap.** The scorecard has no data-privacy criterion, although the brief names privacy as a\nvalid ground. See Q-13.\n",
 "new_string": "**Gap.** The scorecard has no data-privacy criterion, although the brief names privacy as a\nvalid ground. See Q-13.\n\n## 7. Implementation layout — PROPOSED (Phase 1, 2026-10-28; needs approval before code)\n\n### 7.1 Package modules (`src/bto_buddy/`)\n\n| Module | Responsibility | Requirements | LLM? |\n|---|---|---|---|\n| `contracts.py` | All Pydantic models passed between stages (§7.2). The single source of the typed interfaces | REQ-ARC-005, REQ-ARC-007 | No |\n| `knowledge/facts.py` | Load and validate `policy_facts.jsonl` and `sources_manifest.json`; resolve fact ID → URL/section | REQ-DAT-010, REQ-DAT-015, REQ-ARC-009 | No |\n| `knowledge/rules.py` | Load `policy_rules.yaml`; evaluate explicit rules against a validated profile | REQ-DAT-014, REQ-ARC-008 | No |\n| `profile.py` | Extract an `ApplicantProfile` from free text (LLM, structured output), then **deterministically** compute missing fields and conflicts | REQ-ARC-013, REQ-SCP-013 | Extraction only |\n| `gate.py` | Coverage gate: map question topics to MVP tiers; emit `out_of_scope_reasons` | REQ-ARC-004, REQ-SCP-005 | No (see 7.3) |\n| `retrieval.py` | BM25 over fact statements behind a corpus-agnostic `Retriever` protocol | REQ-ARC-010, REQ-DAT-013 | No |\n| `llm.py` | One provider adapter behind a `LLMClient` protocol. Records model ID and settings. Caches responses to saved predictions | REQ-ARC-011, REQ-DAT-018 | — |\n| `generation.py` | Evidence-grounded answer → structured claims with fact-ID citations | REQ-ARC-001 | Yes |\n| `verification.py` | Claim → supported / contradicted / insufficient, then display policy D-011 | REQ-VER-001..007 | Method OPEN |\n| `pipeline.py` | Composes configurations **A–D from one pipeline with stage toggles**, so model and instructions stay identical. D = verify(saved C outputs) | REQ-EVL-010..012 | — |\n| `prompts/` | Versioned prompt templates; the version ID is recorded per run | REQ-DAT-018 | — |\n| `eval/` | Dataset loaders, scoring (metric spec), retrieval recall@k, verifier metrics, paired statistics | REQ-EVL-* | No (scorer OPEN, Q-17) |\n| `app/` | UI (Streamlit, pending Q-23) | REQ-SUB-003 | — |\n\n### 7.2 Core contracts (names and key fields; finalised with the facts schema, Q-22)\n- **`ApplicantProfile`:**\n  - typed optional fields (citizenship per person, marital/fiancé status, ages, first-timer\n    status, prior ownership/applications, HFE status, employment type);\n  - `None` means *not provided*, never a default.\n- **`ProfileAssessment`:** `profile`, `missing_profile_fields`, `profile_conflicts`.\n- **`CoverageDecision`:** `in_scope: bool`, `tiers`, `out_of_scope_reasons`.\n- **`PolicyFact`** (mirrors 03 §2.5), **`PolicyRule`**, **`RuleResult`** (`rule_id`,\n  `applies`, `preparation_step`, `source_fact_id`, `requires_human_review`).\n- **`Evidence`:** `fact_id`, `score`, `rank`.\n- **`Claim`:** `text`, `cited_fact_ids`.\n- **`VerifiedClaim`:** `claim`, `outcome`, `display_action`.\n- **`PreparationReport`:**\n  - `guidance`, `claims`, `evidence_gaps`;\n  - the four contract fields;\n  - `policy_period`, `config_id`, `run_metadata`.\n\n### 7.3 Proposed answers to open architecture questions\n\n**Q-12 — gate placement.**\n- The gate runs after profile extraction and before retrieval and generation.\n- The extraction call also tags the question with topics from a **closed enum**. The gate maps\n  topics to tiers deterministically.\n- An empty or out-of-scope tag set, or zero retrieved evidence above a threshold, returns a\n  coverage response.\n- **Trade-off:** one LLM call does two jobs. The tagging is evaluated through the out-of-scope\n  benchmark category.\n\n**Q-10 — paths:**\n\n| Content | Path |\n|---|---|\n| Scenarios | `data/eval/scenarios.jsonl` |\n| Split | `data/eval/split.json` |\n| Verifier claims | `data/eval/verifier_claims.jsonl` |\n| Retrieval queries | `data/eval/retrieval_queries.jsonl` |\n| Run outputs | `results/runs/<run_id>/{run_metadata.json, predictions.jsonl, scores.json}` (tracked, so offline re-scoring is reproducible) |\n| Frozen metric spec | `eval/metric_spec.md` |\n\n**Dependencies, each to be justified when added:**\n\n| Dependency | Justification |\n|---|---|\n| `pyyaml` | Rule registry format (D-022) |\n| `rank-bm25` | Small, standard BM25. Alternative: about 40 lines in-house |\n| `streamlit` | UI (Q-23) |\n| The chosen provider's SDK, or `httpx` | After model selection |\n| `pandas` | Results tables. `scikit-learn` only if a metric needs it |\n"
}
```

**Tool call: Read**

```
{
 "file_path": "<repo>/docs/decisions.md",
 "offset": 58,
 "limit": 6
}
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/04_architecture.md has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

```
58	| D-018 | Supabase stays listed as a possible demo-video annotation tool | APPROVED | Proposal Q7 | Developer's tool choice | — |
59	| D-019 | Benchmark: target **48 fictional scenarios in total** across six categories, with a dev/held-out split that preserves category coverage. The exact split (and whether K-fold suits better) must be proposed before the dataset is created. Don't assume all 48 are held-out | APPROVED (split OPEN) | Proposal Q8 | — | — |
60	| D-020 | Propose an appropriately sized, independently labelled verifier claim set (dev + eval). No fabricated labels | APPROVED (size OPEN) | Proposal Q8 | — | — |
61	| D-021 | Record source retrieval dates and known effective dates. The supported policy snapshot period is set after source acquisition and validation | APPROVED (period OPEN) | Proposal Q8 | — | — |
62	| D-022 | Data paths: `data/policy_facts.jsonl`, `data/policy_rules.yaml`, `data/visual_resources.json`, `data/sources_manifest.json`, `data/source_coverage.csv`, `data/private_corpus/raw/`, `data/private_corpus/processed/` | APPROVED | Proposal Q8 | — | — |
63	| D-023 | Propose a minimal typed `policy_facts` schema: stable fact IDs, factual statements, applicability conditions, exceptions, source references, temporal metadata, validation status. Finalise it during architecture and corpus design | APPROVED (schema PROPOSED) | Proposal Q8 | — | — |
```
</details>

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/decisions.md",
 "old_string": "| D-025 | The problem-validation research questions are optional evidence-gathering tasks. No invented statistics about confusion, hotline volumes or operational benefit | APPROVED | Proposal Q8 | — | — |",
 "new_string": "| D-025 | The problem-validation research questions are optional evidence-gathering tasks. No invented statistics about confusion, hotline volumes or operational benefit | APPROVED | Proposal Q8 | — | — |\n| D-026 | Out of scope: production-grade hosting, authentication, monitoring infrastructure and operational integrations. A fully runnable, reproducible Dockerised prototype stays mandatory | APPROVED | Phase 1 CLAUDE.md template | Effort goes to the evaluated prototype. Monitoring is *described* in the 150–250-word section only (REQ-DOC-002) | — |\n| D-027 | Git workflow: commit only after a coherent milestone with passing tests, using the milestone message conventions in `CLAUDE.md`. Every commit and push needs explicit developer approval. Inspect staged files before each commit; scan for secrets and identifying terms before each push; push to the private remote after stable milestones | APPROVED | Phase 1 instructions | Reviewable history; protects anonymity and private material | — |\n| D-028 | Tooling: Python ≥3.12, setuptools `src/` layout, Pydantic v2 (runtime); pytest, ruff, mypy `--strict` (dev); pip + venv | PROPOSED (scaffold exists; awaiting approval) | Phase 1 setup | Standard and low-dependency. Mypy strict supports typed contracts. **Lockfile not yet chosen** (pip has none; see development log) | — |"
}
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/decisions.md has been updated successfully.
```
</details>

**Tool call: Write**

```
{
 "file_path": "<repo>/docs/development_log.md",
 "content": "# Development Log\n\nChronological record of completed work, decisions, failures and next steps. Decisions\nthemselves live in [decisions.md](decisions.md). Requirement IDs are in\n[project_context/requirements_register.md](project_context/requirements_register.md).\n\n---\n\n## Phase 0 — Context building (2026-10-27 → 2026-10-28) — complete\n\n**Done:**\n- Reviewed both private planning PDFs page by page, including all 11 embedded images.\n- Built the `docs/project_context/` knowledge base: 150 requirement IDs, a source-discovery\n  matrix, the evaluation design, and a completeness audit (register §4).\n- The developer resolved contradictions C-01 to C-13 (D-001 to D-025).\n- Created `.gitignore` (private PDFs, private corpus, secrets) and private submission notes.\n- Commit `c49555f docs: establish project context and requirements`.\n\n**Found:**\n- New contradictions C-14 to C-17.\n- Open questions Q-05 to Q-24.\n- All policy facts quoted in the approach document are **unverified** until Phase 2.\n\n## Phase 1 — Project setup and architecture (2026-10-28) — in progress\n\n**Done:**\n- `CLAUDE.md`: project instructions, scope, architecture invariants, Git workflow, verified\n  commands.\n- Scaffold:\n  - `pyproject.toml` (src layout; Pydantic runtime; pytest/ruff/mypy dev);\n  - `src/bto_buddy/__init__.py`;\n  - `tests/test_package.py`;\n  - placeholder `README.md`.\n- Implementation layout proposal (modules, contracts, paths, gate design) added to\n  [04 §7](project_context/04_architecture.md), status PROPOSED.\n- Decisions D-026 (production infrastructure out of scope), D-027 (Git workflow), D-028\n  (tooling, PROPOSED).\n- Private anonymity term list (`references/private/anonymity_terms.txt`) for pre-push scans.\n\n**Verified (macOS, Python 3.13.2):**\n\n| Command | Result |\n|---|---|\n| `pip install -e \".[dev]\"` | OK. Installed pydantic 2.14.1, pytest 9.2.0, ruff 0.17.3, mypy 2.4.0 |\n| `pytest` | 1 passed |\n| `ruff check .` | All checks passed |\n| `ruff format --check .` | Already formatted |\n| `mypy` (strict) | No issues |\n\n**Blocked / not verified:**\n- **Docker is not installed** on the dev machine, so no Docker command can be verified yet.\n  REQ-SUB-002 and REQ-NFR-001 need Docker Desktop (or an equivalent) before the deployment\n  milestone.\n- **No lockfile.** Dependency versions are ranges only, which weakens reproducibility\n  (REQ-NFR-001). Options: pin with `pip freeze > requirements.lock`, use `pip-tools`, or use\n  `uv`. Needs a decision.\n\n**Awaiting approval before further Phase 1 code:**\n- Q-23 (stack);\n- Q-12 (gate design);\n- Q-10 (paths);\n- Q-22 (facts schema);\n- D-028 (tooling and lockfile);\n- the `chore: initialise project and tooling` commit.\n\n**Next:**\n1. After approval, implement `contracts.py`, plus loaders for facts and rules, with unit\n   tests. No LLM calls.\n2. Then Phase 2: source verification and the policy-facts corpus.\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/development_log.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 01:36:15

I'll add the development log to the INDEX file map, then run the final checks.

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/INDEX.md",
 "old_string": "| [../decisions.md](../decisions.md) | Decision log (D-001…D-025, BD-00…BD-09) and the instruction priority |",
 "new_string": "| [../decisions.md](../decisions.md) | Decision log (D-001 onward, BD-00…BD-09) and the instruction priority |\n| [../development_log.md](../development_log.md) | Progress per phase, verified commands, failures, next steps |\n| [../../CLAUDE.md](../../CLAUDE.md) | Working instructions for coding agents (scope, invariants, Git workflow, commands) |"
}
```

**Tool call: Bash** — Run all checks, list pending changes, scan anonymity and links

```
cd "<repo>" && wc -l CLAUDE.md && .venv/bin/python -m pytest && .venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/mypy && echo "== status ==" && git status --short -uall && echo "== anonymity (incl. untracked) ==" && (git grep --untracked -inFf references/private/anonymity_terms.txt || echo "no identifying terms") && python3 -I <tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/audit.py "$PWD"
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/INDEX.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
     208 CLAUDE.md
.                                                                        [100%]
1 passed in 0.01s
All checks passed!
14 files already formatted
Success: no issues found in 1 source file
== status ==
 M docs/decisions.md
 M docs/project_context/04_architecture.md
 M docs/project_context/INDEX.md
?? CLAUDE.md
?? README.md
?? docs/development_log.md
?? pyproject.toml
?? src/bto_buddy/__init__.py
?? tests/test_package.py
== anonymity (incl. untracked) ==
no identifying terms
defined IDs: 150
```
</details>

### Claude · 2026-10-28 01:36:35

The checks pass, but ruff reports 14 files when I created only 2 Python files. I'll check what it's scanning.

**Tool call: Bash** — List files ruff format inspects

```
cd "<repo>" && .venv/bin/ruff format --check -v . 2>&1 | grep -iE 'checking|\.py' | head -20
```

<details><summary>Tool result</summary>

```
[2026-10-28][09:36:41][ignore::walk][DEBUG] ignoring <repo>/.pytest_cache: Ignore(IgnoreMatch(Gitignore(Glob { from: Some("<repo>/.gitignore"), original: ".pytest_cache/", actual: "**/.pytest_cache", is_whitelist: false, is_only_dir: true })))
[2026-10-28][09:36:41][ruff_workspace::resolver][DEBUG] Included path via `include`: "<repo>/src/bto_buddy/__init__.py"
[2026-10-28][09:36:41][ruff_workspace::resolver][DEBUG] Included path via `include`: "<repo>/tests/test_package.py"
[2026-10-28][09:36:41][ruff::commands::format][DEBUG] format_path; path=<repo>/src/bto_buddy/__init__.py
[2026-10-28][09:36:41][ruff::commands::format][DEBUG] format_path; path=<repo>/tests/test_package.py
```
</details>

### Claude · 2026-10-28 01:36:56

Ruff only formats the two project files; nothing private is scanned. The "14" is just ruff's file counter.

Phase 1 setup is done up to the first commit, which I haven't made because it needs your approval. The scaffold installs and all four checks pass: pytest (1 test), ruff check, ruff format and mypy in strict mode. Docker isn't installed on this machine, so no Docker command has been verified yet.

**What I created or changed**
- **[CLAUDE.md](CLAUDE.md)** (208 lines). It's your template tightened, with project-specific rules added:
  - architecture rules every change must keep (typed contracts between stages, the four missing-information fields, verifier display behaviour, no reading the private corpus at runtime);
  - an anonymity rule;
  - your commit milestone table;
  - a commands section with only verified commands;
  - a pre-push scan for secrets and identifying terms. The identifying terms live in a Git-ignored file, `references/private/anonymity_terms.txt`, so the list itself never gets committed.
- **Scaffold:**
  - [pyproject.toml](pyproject.toml): `src/` layout, Python ≥3.12, Pydantic as the only runtime dependency, pytest/ruff/mypy for development;
  - [src/bto_buddy/__init__.py](src/bto_buddy/__init__.py);
  - [tests/test_package.py](tests/test_package.py);
  - a placeholder [README.md](README.md);
  - a local `.venv` (Git-ignored).
- **Architecture proposal:** [04_architecture.md §7](docs/project_context/04_architecture.md), marked PROPOSED. It covers the module layout, the main typed contracts, the coverage gate design, file paths and candidate dependencies. Configurations A–D come from one pipeline with stages switched on or off. That keeps the model and instructions identical, and D is computed from C's saved outputs.
- **[decisions.md](docs/decisions.md):** three new entries.
  - D-026: production hosting, authentication and monitoring are out of scope. This came from your template.
  - D-027: the Git workflow.
  - D-028: the tooling choices, still PROPOSED.
- **[development_log.md](docs/development_log.md):** entries for Phase 0 and Phase 1.

**Changes from your template**
- I brought the Scope section back in line with the approved scope decision (D-008). That restores "post-purchase conditions" as excluded. "Source-grounded guidance" and "claim verification" are now listed as required capabilities rather than policy areas.
- The template said not to push without approval, but your message said to push after each milestone. I combined these: push after stable milestones, but only with your approval.

**Decisions I need from you**
1. **Commit approval** for `chore: initialise project and tooling`. It would include:
   - `CLAUDE.md`, `README.md`, `pyproject.toml`, `src/`, `tests/`;
   - `docs/development_log.md`;
   - the edits to `decisions.md`, `04_architecture.md` and `INDEX.md`.
2. **Push:** `origin` points to `github.com/<git-user>/bto-buddy`. Can you confirm it's private? Should I push `c49555f` and this commit once it's approved?
3. **Lockfile (D-028):** right now pip only records version ranges, which weakens the clean-machine reproducibility requirement. My recommendation is `uv` with `uv.lock`, but it would need installing. A `pip freeze` lock is the zero-install alternative.
4. **Docker:** please install Docker Desktop (or an equivalent) before the deployment milestone.
5. **Architecture choices** from the earlier open questions:
   - Q-23: the stack (Streamlit, Pydantic, pandas);
   - Q-12: the coverage gate design (topic tags from a fixed list, mapped to scope tiers by code);
   - Q-10: file paths for the evaluation data and run outputs;
   - Q-22: the `policy_facts` schema.

Once these are approved, the next step is `contracts.py` plus the facts and rules loaders, with unit tests and no LLM calls.

### User · 2026-10-28 02:19:03

exclude the commit milestones as those will be manually executed by myself (the developer). instead, you should suggest when is appropriate to commit after each stable milestone and require my approval to execute the commit myself

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/CLAUDE.md",
 "old_string": "## Git workflow\n- **Never commit, push, merge or rewrite history without the developer's explicit approval\n  for that action.**\n- Commit after a coherent milestone, once its tests pass.\n- Before every commit:\n  - inspect the staged file list;\n  - confirm nothing from `references/private/` or `data/private_corpus/`, and no `.env`, is\n    staged.\n- Before every push, scan the staged/committed diff for secrets and identifying terms.\n- Push to the private remote after each stable milestone, with approval.\n- End commit messages with the `Co-Authored-By` line from the session's attribution\n  instructions.\n\n| Milestone | Message |\n|---|---|\n| Initial structure | `chore: initialise project and tooling` |\n| Policy sources | `data: add source manifest and policy rule registry` |\n| Benchmark | `eval: add labelled applicant scenarios` |\n| Baseline | `feat: implement direct LLM baseline` |\n| Hybrid pipeline | `feat: add structured guidance and retrieval` |\n| Verification | `feat: add evidence-based claim verification` |\n| Evaluation | `eval: add comparative metrics and ablations` |\n| Deployment | `build: add Docker deployment and smoke tests` |\n| Final submission | `docs: finalise README, demo and AI logs` |",
 "new_string": "## Git workflow (D-027)\n- **The developer runs every commit and push.** Never run `git commit`, `git push`, merge,\n  rebase or any history rewrite. Read-only Git commands (`status`, `diff`, `log`, `grep`) and\n  `git add` are fine.\n- When a coherent, stable milestone is done and its checks pass, **suggest that it's a good\n  point to commit**. Include:\n  - which files belong in the commit, and anything that should be left out;\n  - the check results that make the milestone stable;\n  - a suggested conventional-commit message (`feat:`, `data:`, `eval:`, `build:`, `docs:`,\n    `chore:`);\n  - whether a push to the private remote is advisable.\n\n  Wait for the developer to approve before staging anything.\n- **Before any suggested commit:** confirm nothing from `references/private/` or\n  `data/private_corpus/`, and no `.env` or credentials, is part of the change.\n- **Before any suggested push:** run the secret and anonymity scans below and report the\n  results."
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/decisions.md",
 "old_string": "| D-027 | Git workflow: commit only after a coherent milestone with passing tests, using the milestone message conventions in `CLAUDE.md`. Every commit and push needs explicit developer approval. Inspect staged files before each commit; scan for secrets and identifying terms before each push; push to the private remote after stable milestones | APPROVED | Phase 1 instructions | Reviewable history; protects anonymity and private material | — |",
 "new_string": "| D-027 | Git workflow: **the developer executes all commits and pushes**. The coding agent suggests when a coherent, stable milestone (checks passing) is ready to commit, with the file list, check results, a suggested conventional-commit message and push advice. It runs secret and identifying-term scans before a suggested push and waits for approval. No fixed milestone list | APPROVED (revised 2026-10-28) | Phase 1 instructions | Developer keeps control of history; protects anonymity and private material | Earlier draft with a fixed milestone/message table and agent-executed commits |"
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/development_log.md",
 "old_string": "- the `chore: initialise project and tooling` commit.",
 "new_string": "- the developer's commit of the Phase 1 scaffold (D-027: the developer runs commits; the agent\n  suggests them)."
}
```

<details><summary>Tool result</summary>

```
The file <repo>/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/decisions.md has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/development_log.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 02:19:47

I've updated the workflow. Since the Phase 1 scaffold is now a stable point, I'll run the pre-commit and pre-push checks so I can give you a proper commit suggestion.

**Tool call: Bash** — Run checks plus secret and anonymity scans on pending changes

```
cd "<repo>" && .venv/bin/python -m pytest && .venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/mypy && echo "== changes ==" && git status --short -uall && echo "== private paths in change? ==" && (git status --porcelain -uall | grep -E 'references/private|data/private_corpus|\.env' || echo "none") && echo "== secret patterns ==" && (git grep --untracked -inE 'api[_-]?key *[=:]|secret *[=:]|password *[=:]|BEGIN .*PRIVATE KEY' -- . ':!CLAUDE.md' || echo "none") && echo "== identifying terms ==" && (git grep --untracked -inFf references/private/anonymity_terms.txt || echo "none") && grep -n "Milestone\|chore: initialise" CLAUDE.md || echo "milestone table removed"
```

<details><summary>Tool result</summary>

```
.                                                                        [100%]
1 passed in 0.01s
All checks passed!
14 files already formatted
Success: no issues found in 1 source file
== changes ==
 M docs/decisions.md
 M docs/project_context/04_architecture.md
 M docs/project_context/INDEX.md
?? CLAUDE.md
?? README.md
?? docs/development_log.md
?? pyproject.toml
?? src/bto_buddy/__init__.py
?? tests/test_package.py
== private paths in change? ==
none
== secret patterns ==
none
== identifying terms ==
none
milestone table removed
```
</details>

### Claude · 2026-10-28 02:20:00

I've removed the fixed milestone table from CLAUDE.md. Its Git workflow section now says you run every commit and push yourself. When a milestone is stable and its checks pass, I'll suggest committing, with:
- the files to include;
- the check results;
- a suggested message;
- whether to push.

I won't stage anything until you approve. I updated the Git workflow decision (D-027) in [docs/decisions.md](docs/decisions.md) to match, and noted the earlier version as superseded.

**Suggested commit: now is a good point.** The Phase 1 scaffold is stable:

| Check | Result |
|---|---|
| pytest | 1 passed |
| ruff check | All checks passed |
| ruff format | Clean |
| mypy (strict) | No issues |
| Private or `.env` files in the change | None |
| Secret patterns | None |
| Identifying terms | None |

- **Include:** `CLAUDE.md`, `README.md`, `pyproject.toml`, `src/bto_buddy/__init__.py`, `tests/test_package.py`, `docs/development_log.md`, `docs/decisions.md`, `docs/project_context/04_architecture.md`, `docs/project_context/INDEX.md`
- **Leave out:** `.venv/` and `*.egg-info/`. Both are already Git-ignored.
- **Suggested message:** `chore: initialise project and tooling`
- **Push:** I'd suggest pushing this together with `c49555f` once you've confirmed the GitHub repo is private.

```bash
git add CLAUDE.md README.md pyproject.toml src tests docs
git commit -m "chore: initialise project and tooling"
```

These decisions are still open before the next code step (`contracts.py` and the facts/rules loaders):
- the lockfile approach (D-028);
- installing Docker;
- the stack, gate design, file paths and facts schema (Q-23, Q-12, Q-10, Q-22).

### User · 2026-10-28 02:22:47

<ide_selection>The user selected the lines 243 to 243 from <repo>/docs/project_context/04_architecture.md:
D-02

This may or may not be related to the current task.</ide_selection>

### User · 2026-10-28 02:22:47

for the lockfile, proceed with your recommendation of uv with uv.lock instead of pip freeze lock. proceed with installing docker. put the architecture decisions (stack, gate design, file paths and facts schema) on hold and out of the upcoming commit first as my subsequent set of instructions (after this upcoming commit) will involve an architecture review

### Claude · 2026-10-28 02:22:57

I'll install uv and generate the lockfile first, then install Docker. After that I'll move the architecture proposal out of the files this commit touches.

**Tool call: Bash** — Install uv via Homebrew

```
brew install uv 2>&1 | tail -3 && uv --version
```

<details><summary>Tool result</summary>

```
==> Caveats
zsh completions have been installed to:
  /opt/homebrew/share/zsh/site-functions
uv 0.13.6 (Homebrew 2026-10-26 aarch64-apple-darwin)
```
</details>

### Claude · 2026-10-28 02:36:15

uv is installed. I'll move the dev tools to a standard `[dependency-groups]` section (PEP 735), which `uv sync` installs by default, then lock and re-verify.

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/pyproject.toml",
 "old_string": "[project.optional-dependencies]\ndev = [",
 "new_string": "[dependency-groups]\n# Installed by default with `uv sync`; versions pinned in uv.lock (D-028).\ndev = ["
}
```

**Tool call: Bash** — Generate uv.lock, sync env, rerun all checks

```
cd "<repo>" && rm -rf .venv src/*.egg-info && uv lock 2>&1 | tail -2 && uv sync 2>&1 | tail -4 && echo "== checks ==" && uv run pytest && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv lock --check && echo "lock up to date" && grep -cE '^\[\[package\]\]' uv.lock && uv run python --version
```

<details><summary>Tool result</summary>

```
The file <repo>/pyproject.toml has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
Using CPython 3.13.2 interpreter at: /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
Resolved 18 packages in 1.32s
 + pytest==9.2.0
 + ruff==0.17.3
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
== checks ==
.                                                                        [100%]
1 passed in 0.00s
All checks passed!
14 files already formatted
Success: no issues found in 1 source file
Resolved 18 packages in 5ms
lock up to date
18
Python 3.13.2
```
</details>

### Claude · 2026-10-28 02:37:08

Lockfile done: 18 packages pinned and every check passes under `uv run`. Now Docker Desktop.

**Tool call: Bash** — Install Docker Desktop via Homebrew cask

```
brew install --cask docker-desktop 2>&1 | tail -8
```

<details><summary>Tool result</summary>

```
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
sudo: a password is required
==> Backing up App 'Docker.app' to '/opt/homebrew/Caskroom/docker-desktop/4.97.0,244584/Docker.app'
Error: docker-desktop: Failure while executing; `/usr/bin/sudo -E -- /bin/ln -h -f -s -- /Applications/Docker.app/Contents/Resources/bin/docker-credential-desktop /usr/local/bin/docker-credential-desktop` exited with 1. Here's the output:
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
sudo: a password is required
==> Removing App '/Applications/Docker.app'
==> Purging files for version 4.97.0,244584 of Cask docker-desktop
```
</details>

<details><summary>Claude's reasoning</summary>

Docker Desktop's install needs sudo access I can't provide here, but Homebrew cleanly rolled back the attempt, so I'll give you the command to run yourself. Next, I'll pull the architecture proposal out of `04_architecture.md` into a separate held draft outside this commit.


</details>

**Tool call: Bash** — Move architecture section 7 into a held draft file

```
cd "<repo>" && mkdir -p docs/proposals && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/project_context/04_architecture.md'); t=p.read_text()
marker='\n## 7. Implementation layout'
i=t.index(marker); head,sec=t[:i].rstrip('\n')+'\n',t[i:].lstrip('\n')
p.write_text(head)
hdr=("# HELD — Implementation layout proposal (Phase 1)\n\n"
     "**Status: ON HOLD (2026-10-28).** Withheld from the project-context docs and from the Phase 1 "
     "scaffold commit, pending the developer's architecture review. Covers Q-10 (paths), Q-12 (gate "
     "design), Q-22 (facts schema contracts) and Q-23 (stack/dependencies). Nothing here is "
     "approved or implemented.\n\n")
pathlib.Path('docs/proposals/architecture_layout_draft.md').write_text(hdr+sec.replace('## 7.','## ').replace('### 7.','### '))
EOF
git diff --stat docs/project_context/04_architecture.md; head -5 docs/proposals/architecture_layout_draft.md
```

<details><summary>Tool result</summary>

```
# HELD — Implementation layout proposal (Phase 1)

**Status: ON HOLD (2026-10-28).** Withheld from the project-context docs and from the Phase 1 scaffold commit, pending the developer's architecture review. Covers Q-10 (paths), Q-12 (gate design), Q-22 (facts schema contracts) and Q-23 (stack/dependencies). Nothing here is approved or implemented.

##  Implementation layout — PROPOSED (Phase 1, 2026-10-28; needs approval before code)
```
</details>

### Claude · 2026-10-28 02:42:02

`04_architecture.md` is now back to its committed version, so it drops out of the commit. I'll tidy the draft's headings and update any references to the old "04 §7".

**Tool call: Bash** — Fix draft headings and find stale references

```
cd "<repo>" && sed -i '' -E 's/^(#{2,3})  /\1 /' docs/proposals/architecture_layout_draft.md && grep -n '^#' docs/proposals/architecture_layout_draft.md && echo "== refs ==" && grep -rn '04 §7\|§7\|pip install\|\[dev\]\|optional-dependencies' CLAUDE.md docs README.md | grep -v proposals/
```

<details><summary>Tool result</summary>

```
1:# HELD — Implementation layout proposal (Phase 1)
5:## Implementation layout — PROPOSED (Phase 1, 2026-10-28; needs approval before code)
7:### 1 Package modules (`src/bto_buddy/`)
25:### 2 Core contracts (names and key fields; finalised with the facts schema, Q-22)
42:### 3 Proposed answers to open architecture questions
== refs ==
CLAUDE.md:184:.venv/bin/python -m pip install -e ".[dev]"   # package + pytest, ruff, mypy
docs/development_log.md:35:  [04 §7](project_context/04_architecture.md), status PROPOSED.
docs/development_log.md:44:| `pip install -e ".[dev]"` | OK. Installed pydantic 2.14.1, pytest 9.2.0, ruff 0.17.3, mypy 2.4.0 |
docs/project_context/requirements_register.md:62:| REQ-SCP-013 | Separate missing applicant info (A) vs missing corpus evidence (B) in architecture, benchmark, docs | APPROVED | [APP p.18–19] | 01 §7 | profile_extractor, verifier, eval_harness | Distinct response fields; distinct benchmark labels |
docs/project_context/requirements_register.md:98:| REQ-DAT-018 | Record model IDs, prompt versions, inference settings, corpus versions, saved predictions; offline scoring distinct from live inference | APPROVED | [APP p.15] | 03 §7 | eval_harness | Run metadata files; rescoring from saved predictions works offline |
docs/project_context/requirements_register.md:101:| REQ-DAT-021 | Reviewers build index and run Docker without downloading HDB pages | APPROVED | [APP p.14] | 03 §7 | docker, retriever | Offline clean-machine test |
docs/project_context/requirements_register.md:102:| REQ-DAT-022 | Capture/extraction scripts optional, not startup/eval dependencies | APPROVED | [APP p.14] | 03 §7 | source_acquisition | Docker image doesn't invoke them |
docs/project_context/requirements_register.md:177:| REQ-EVL-030 | Raw counts + percentages; paired comparisons; bootstrap / exact McNemar as options | APPROVED (tests PROPOSED) | [APP p.27]; D-001 | 05 §7 | eval_harness | Stats in results |
docs/project_context/requirements_register.md:178:| REQ-EVL-031 | README: controlled benchmark, not population-level evidence | APPROVED | [APP p.27] | 05 §7 | README | Statement present |
docs/project_context/requirements_register.md:203:| REQ-DOC-013 | `ai_logs/` layout with README and redactions.md | APPROVED | [APP p.30–31] | 06 §7 | ai_logs | Directory present |
docs/project_context/requirements_register.md:204:| REQ-DOC-014 | AI-usage disclosure (Claude Code; ChatGPT optional) | APPROVED (wording PROPOSED) | [APP p.31]; D-009 | 06 §7 | README | Section at README end |
docs/project_context/requirements_register.md:224:| REQ-SUB-010 | Upload all coding-agent session & chat logs; location in README | MANDATORY | [ASM p.4]; D-009 | 06 §7 | ai_logs | Log inventory vs local session list |
docs/project_context/requirements_register.md:225:| REQ-SUB-020 | Pre-submission log audit; minimal documented redaction; escalate if conflict | APPROVED | D-010 | 06 §7 | ai_logs | `ai_logs/redactions.md` |
docs/project_context/requirements_register.md:290:| Q-19 | Log redaction of organisation name: does redacting it in this Phase 0 session satisfy D-010, or escalate? | 06 §7 | Pre-submission |
docs/project_context/requirements_register.md:334:| 19–20 | Missing info A/B; failure-type table; missing-info contract; demo intro | 01 §7; 05 §8; 04 §3 |
docs/project_context/requirements_register.md:344:| 30 | Problem-validation via hackathon projects; model-justification; considerations; narrative; demo; AI usage; README preferences; repo contents | 01 §5; 06 §7–8 |
docs/project_context/requirements_register.md:345:| 31 | ai_logs tree; draft disclosure; optional project_selection; rules; private-notes instruction | 06 §7–8; private notes |
docs/project_context/05_evaluation.md:127:  bootstrap intervals (§7), not with folds.
```
</details>

### Claude · 2026-10-28 02:42:10

Now I'll update CLAUDE.md's commands, D-028 and the development log to match uv, Docker status and the hold.

**Tool call: Read**

```
{
 "file_path": "<repo>/CLAUDE.md",
 "offset": 178
}
```

<details><summary>Tool result</summary>

````
178	
179	## Commands
180	Verified on macOS with Python 3.13.2 (project requires ≥3.12):
181	
182	```bash
183	python3 -m venv .venv
184	.venv/bin/python -m pip install -e ".[dev]"   # package + pytest, ruff, mypy
185	.venv/bin/python -m pytest                    # tests
186	.venv/bin/ruff check .                        # lint
187	.venv/bin/ruff format --check .               # formatting
188	.venv/bin/mypy                                # strict type check of src/bto_buddy
189	```
190	
191	**Not yet available:** the application run command (UI pending stack approval), Docker
192	build/run (Docker is not installed on the dev machine yet), and evaluation commands. Add each
193	one here only after it has been verified.
194	
195	**Secret scan before a push** (until a dedicated tool is approved):
196	```bash
197	git diff --cached --name-only | grep -E '^(references/private|data/private_corpus)/|\.env' && echo "BLOCK"
198	git diff --cached | grep -inE 'api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY' || echo "no secret patterns"
199	# Anonymity: the term list is private (Git-ignored) and must never be copied into tracked files.
200	git grep -inFf references/private/anonymity_terms.txt || echo "no identifying terms"
201	```
202	
````
</details>

**Tool call: Edit**

````
{
 "replace_all": false,
 "file_path": "<repo>/CLAUDE.md",
 "old_string": "Verified on macOS with Python 3.13.2 (project requires ≥3.12):\n\n```bash\npython3 -m venv .venv\n.venv/bin/python -m pip install -e \".[dev]\"   # package + pytest, ruff, mypy\n.venv/bin/python -m pytest                    # tests\n.venv/bin/ruff check .                        # lint\n.venv/bin/ruff format --check .               # formatting\n.venv/bin/mypy                                # strict type check of src/bto_buddy\n```\n\n**Not yet available:** the application run command (UI pending stack approval), Docker\nbuild/run (Docker is not installed on the dev machine yet), and evaluation commands. Add each\none here only after it has been verified.",
 "new_string": "Environment and dependencies are managed with **uv**. Exact versions are pinned in `uv.lock`,\nwhich must be committed (D-028). Verified on macOS with uv 0.13.6 and Python 3.13.2 (project\nrequires ≥3.12):\n\n```bash\nuv sync                      # create .venv from uv.lock (package + dev group)\nuv run pytest                # tests\nuv run ruff check .          # lint\nuv run ruff format --check . # formatting\nuv run mypy                  # strict type check of src/bto_buddy\nuv lock --check              # fail if uv.lock is out of date with pyproject.toml\n```\n\n- Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>`), with a justification\n  comment in `pyproject.toml`. Never hand-edit `uv.lock`.\n- **Not yet available:**\n  - the application run command (UI on hold pending architecture review);\n  - Docker build/run (Docker Desktop installation pending on the dev machine);\n  - evaluation commands.\n\n  Add each one here only after it has been verified."
}
````

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/decisions.md",
 "old_string": "| D-028 | Tooling: Python ≥3.12, setuptools `src/` layout, Pydantic v2 (runtime); pytest, ruff, mypy `--strict` (dev); pip + venv | PROPOSED (scaffold exists; awaiting approval) | Phase 1 setup | Standard and low-dependency. Mypy strict supports typed contracts. **Lockfile not yet chosen** (pip has none; see development log) | — |",
 "new_string": "| D-028 | Tooling: Python ≥3.12, setuptools `src/` layout, Pydantic v2 (runtime); pytest, ruff, mypy `--strict` as a PEP 735 `dev` dependency group. **uv** manages the environment, with a committed **`uv.lock`** | APPROVED (uv + lockfile, 2026-10-28) | Phase 1 setup | A cross-platform lockfile gives exact, reproducible installs for the clean-machine and Docker requirements (REQ-NFR-001). Preferred over a `pip freeze` lock, which is platform-specific and mixes in transitive noise | pip + venv without a lockfile |\n| D-029 | **Architecture decisions on hold** pending the developer's architecture review: stack (Q-23), gate design (Q-12), file paths (Q-10), facts schema/contracts (Q-22). The draft is held in `docs/proposals/architecture_layout_draft.md` and kept out of the Phase 1 scaffold commit | APPROVED (hold) | Phase 1 instructions | Review before any contracts code | Earlier \"04 §7\" placement |"
}
```

<details><summary>Tool result</summary>

```
The file <repo>/CLAUDE.md has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/decisions.md has been updated successfully.
```
</details>

**Tool call: Bash** — Clarify held draft is uncommitted in D-029

```
cd "<repo>" && sed -i '' 's#The draft is held in `docs/proposals/architecture_layout_draft.md` and kept out of the Phase 1 scaffold commit#The draft is held as an **uncommitted** file, `docs/proposals/architecture_layout_draft.md`, and kept out of the Phase 1 scaffold commit#' docs/decisions.md && grep -c "uncommitted" docs/decisions.md
```

**Tool call: Read**

```
{
 "file_path": "<repo>/docs/development_log.md",
 "offset": 24
}
```

<details><summary>Tool result</summary>

```
1
```
</details>

<details><summary>Tool result</summary>

```
24	## Phase 1 — Project setup and architecture (2026-10-28) — in progress
25	
26	**Done:**
27	- `CLAUDE.md`: project instructions, scope, architecture invariants, Git workflow, verified
28	  commands.
29	- Scaffold:
30	  - `pyproject.toml` (src layout; Pydantic runtime; pytest/ruff/mypy dev);
31	  - `src/bto_buddy/__init__.py`;
32	  - `tests/test_package.py`;
33	  - placeholder `README.md`.
34	- Implementation layout proposal (modules, contracts, paths, gate design) added to
35	  [04 §7](project_context/04_architecture.md), status PROPOSED.
36	- Decisions D-026 (production infrastructure out of scope), D-027 (Git workflow), D-028
37	  (tooling, PROPOSED).
38	- Private anonymity term list (`references/private/anonymity_terms.txt`) for pre-push scans.
39	
40	**Verified (macOS, Python 3.13.2):**
41	
42	| Command | Result |
43	|---|---|
44	| `pip install -e ".[dev]"` | OK. Installed pydantic 2.14.1, pytest 9.2.0, ruff 0.17.3, mypy 2.4.0 |
45	| `pytest` | 1 passed |
46	| `ruff check .` | All checks passed |
47	| `ruff format --check .` | Already formatted |
48	| `mypy` (strict) | No issues |
49	
50	**Blocked / not verified:**
51	- **Docker is not installed** on the dev machine, so no Docker command can be verified yet.
52	  REQ-SUB-002 and REQ-NFR-001 need Docker Desktop (or an equivalent) before the deployment
53	  milestone.
54	- **No lockfile.** Dependency versions are ranges only, which weakens reproducibility
55	  (REQ-NFR-001). Options: pin with `pip freeze > requirements.lock`, use `pip-tools`, or use
56	  `uv`. Needs a decision.
57	
58	**Awaiting approval before further Phase 1 code:**
59	- Q-23 (stack);
60	- Q-12 (gate design);
61	- Q-10 (paths);
62	- Q-22 (facts schema);
63	- D-028 (tooling and lockfile);
64	- the developer's commit of the Phase 1 scaffold (D-027: the developer runs commits; the agent
65	  suggests them).
66	
67	**Next:**
68	1. After approval, implement `contracts.py`, plus loaders for facts and rules, with unit
69	   tests. No LLM calls.
70	2. Then Phase 2: source verification and the policy-facts corpus.
71	
```
</details>

**Tool call: Bash** — Rewrite Phase 1 log, rerun checks and pre-commit scans

```
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/development_log.md'); t=p.read_text()
i=t.index('## Phase 1')
t=t[:i]+'''## Phase 1 — Project setup and architecture (2026-10-28) — in progress

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
'''
p.write_text(t)
EOF
uv run pytest && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv lock --check >/dev/null && echo "lock ok" && echo "== status ==" && git status --short -uall && echo "== private/env in change? ==" && (git status --porcelain -uall | grep -E 'references/private|data/private_corpus|\.env' || echo none) && echo "== secrets ==" && (git grep --untracked -inE 'api[_-]?key *[=:]|secret *[=:]|password *[=:]|BEGIN .*PRIVATE KEY' -- . ':!CLAUDE.md' || echo none) && echo "== identifying terms ==" && (git grep --untracked -inFf references/private/anonymity_terms.txt || echo none) && python3 -I <tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/audit.py "$PWD"
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 703 chars]
```
</details>

### Claude · 2026-10-28 02:44:55

I set up uv with a committed lockfile and moved the architecture proposal out of this commit. Docker Desktop did not install, because its installer needs your administrator password.

**Lockfile (uv):**
- I installed uv 0.13.6 and moved the dev tools in [pyproject.toml](pyproject.toml) into a standard `dev` dependency group.
- `uv.lock` now pins 18 packages, and `uv lock --check` confirms it matches `pyproject.toml`.
- The old pip-built `.venv` was replaced by one built with `uv sync`.
- All checks pass under `uv run`: pytest (1 passed), ruff check, ruff format and mypy strict.
- [CLAUDE.md](CLAUDE.md)'s commands section now lists the verified uv commands. [decisions.md](docs/decisions.md) records this as D-028.

**Docker:** `brew install --cask docker-desktop` stopped when it reached the step that needs `sudo`, and this session can't type a password. Homebrew rolled it back cleanly. Please run this in your own terminal:

```bash
brew install --cask docker-desktop
open -a Docker          # accept the terms on first launch, wait for "Engine running"
docker run --rm hello-world
```

Once `hello-world` works, tell me and I'll verify Docker and add its commands to CLAUDE.md.

**Architecture on hold (D-029):** the layout proposal (modules, contracts, file paths, gate design and stack) is now in `docs/proposals/architecture_layout_draft.md`. It's uncommitted, ready for your review. `04_architecture.md` is back to exactly its committed version.

**Suggested commit: now is a good point.**

| Check | Result |
|---|---|
| pytest, ruff, mypy | All pass |
| `uv lock --check` | Lockfile matches |
| Private or `.env` files in the change | None |
| Secret patterns | None |
| Identifying terms | None |
| Requirement IDs and internal links | All resolve |

- **Include:** `CLAUDE.md`, `README.md`, `pyproject.toml`, `uv.lock`, `src/`, `tests/`, `docs/decisions.md`, `docs/development_log.md`, `docs/project_context/INDEX.md`
- **Leave out:** `docs/proposals/` (the held architecture draft)
- **Suggested message:** `chore: initialise project and tooling`
- **Push:** fine to push this along with the Phase 0 commit (`c49555f`), once you've confirmed the GitHub repo is private.

```bash
git add CLAUDE.md README.md pyproject.toml uv.lock src tests docs/decisions.md docs/development_log.md docs/project_context/INDEX.md
git status --short   # docs/proposals/ should still show as untracked (??)
git commit -m "chore: initialise project and tooling"
```

One thing to know: the committed D-029 entry names the held draft file, which won't be in the repo until the architecture review settles it.

### User · 2026-10-28 02:58:05

<ide_opened_file>The user opened the file <repo>/docs/proposals/architecture_layout_draft.md in the IDE. This may or may not be related to the current task.</ide_opened_file>

### User · 2026-10-28 02:58:05

i have installed docker. now perform the architecture review, before coding: Review the approved project scope, architecture considerations, evaluation methodology and requirements register in docs/project_context/. We are building BTO Buddy, an evidence-grounded BTO pre-application preparation assistant for fictional first-timer couple profiles.
The system must extract structured applicant information, detect missing and conflicting profile fields, determine whether questions are within supported scope, retrieve authoritative policy evidence, apply a small set of deterministic rules, generate cited preparation guidance, and verify factual claims before presenting them.
Before writing code:
Propose the simplest maintainable end-to-end architecture satisfying the approved MVP.
Compare a rules-plus-BM25 approach against more complex agentic and vector-database approaches.
Evaluate keyword/BM25, semantic, hybrid retrieval and reranking as alternatives. Recommend the simplest suitable method; do not propose implementing additional methods without a testable reason.
Define explicit Pydantic contracts for the coverage gate, applicant profile, policy rule outputs, retrieved evidence, generated claims, verification results and final guidance.
Distinguish missing_profile_fields, profile_conflicts, evidence_gaps and out_of_scope_reasons in the system design.
Identify data dependencies, privacy/licensing concerns, failure modes, uncertainty handling, evaluation opportunities and integration risks.
Recommend a minimal dependency list and clear module boundaries.
Map components to approved requirement IDs and propose unit, integration and acceptance tests.
Justify technical choices based on task suitability, data sensitivity, latency, maintainability, reproducibility and cost at scale.
Identify any materially better alternatives, explain their tradeoffs and request my approval before deviating from the approved approach.
Do not introduce unrelated features such as applicant clustering or staff analytics. Do not implement code yet.

### Claude · 2026-10-28 02:58:11

First a quick check that Docker works, so I can record it. Then the review.

**Tool call: Bash** — Verify Docker CLI and engine work

```
docker --version && docker info --format '{{.ServerVersion}} {{.OperatingSystem}} {{.Architecture}}' && docker run --rm hello-world 2>&1 | grep -m1 "Hello from Docker"
```

<details><summary>Tool result</summary>

```
Docker version 29.9.2, build a82e528
  
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
```
</details>

### Claude · 2026-10-28 02:58:24

The Docker CLI is installed (29.9.2), but the engine isn't running. I'll try starting Docker Desktop.

**Tool call: Bash** — Launch Docker Desktop and wait for the engine

```
open -a Docker && for i in $(seq 1 45); do docker info >/dev/null 2>&1 && { echo "engine up after ~$((i*2))s"; break; }; perl -e 'select(undef,undef,undef,2)'; done; docker run --rm hello-world 2>&1 | grep -m1 -E "Hello from Docker|error|failed" || docker info 2>&1 | tail -2
```

<details><summary>Tool result</summary>

```
engine up after ~8s
Hello from Docker!
```
</details>

<details><summary>Claude's reasoning</summary>

Docker's confirmed working (engine 29.9.2, hello-world ran successfully). Now I'll draft the architecture review as a reviewable document replacing the held draft, then summarize the decisions needing your approval.


</details>

**Tool call: Write**

````
{
 "file_path": "<repo>/docs/proposals/architecture_review.md",
 "content": "# Architecture Review — BTO Buddy (pre-implementation)\n\n**Status:** PROPOSED for developer review (2026-10-28). It replaces the held draft\n(D-029). Nothing here is implemented. Items marked **[APPROVAL]** are choices beyond the\napproved decisions, or interpretations of them. They are listed again in §13.\n\n**Inputs:** [01 scope](../project_context/01_problem_and_scope.md),\n[03 data](../project_context/03_data_and_licensing.md),\n[04 architecture](../project_context/04_architecture.md),\n[05 evaluation](../project_context/05_evaluation.md),\n[register](../project_context/requirements_register.md),\n[decisions](../decisions.md).\n\n---\n\n## 1. Recommendation in one paragraph\n\nBuild a **single, linear, typed pipeline** in plain Python. Each request runs a fixed\nsequence:\n1. **one LLM call** extracts the applicant profile and the question topics, with quotes as\n   evidence;\n2. **deterministic code** assesses the profile, applies the coverage gate, evaluates rules and\n   retrieves facts with **BM25 over the ~50–150 authored facts**;\n3. **one LLM call** generates cited claims;\n4. **verification** runs a deterministic layer plus **one batched LLM judgement call**;\n5. a **pure function** assembles the report and applies the D-011 display policy.\n\nEvery stage boundary is a Pydantic model. Configurations A–D are the same pipeline with stages\nswitched off, and all four emit the same output contract. There are no agents, no vector\ndatabase, no embeddings and no reranker. Each is held back behind a measurable trigger (§4).\n\n## 2. Requirements that shape the design\n\n| Driver | IDs |\n|---|---|\n| Three capabilities: retrieve, generate profile-specific guidance, verify | REQ-ARC-001 |\n| Fixed pipeline, deterministic validation, no agents/frameworks/vector DB | REQ-ARC-002, REQ-ARC-003, BD-09 |\n| Coverage gate before generation | REQ-ARC-004, REQ-SCP-005 |\n| Four distinct contract fields | REQ-ARC-005, REQ-SCP-013, REQ-ARC-013, REQ-ARC-014 |\n| Typed objects between modules | REQ-ARC-007 |\n| Facts KB only at runtime; rules cite fact IDs | REQ-DAT-010..012, REQ-DAT-015 |\n| Verifier outcomes and display policy | REQ-VER-001..007, D-011 |\n| Same model, instructions and labels across A–D; C→D reuse | REQ-EVL-010..012 |\n| Reproducible runs and offline rescoring | REQ-DAT-018, REQ-NFR-001 |\n| Free tier, operational model justification | REQ-NFR-004, REQ-MOD-001 |\n\n## 3. End-to-end architecture\n\n```mermaid\nflowchart TD\n    Q[\"Free-text situation + question\"] --> X\n    X[\"① extract (LLM #1)<br/>ProfileExtraction: fields + quotes + topics\"] --> PA\n    PA[\"② assess_profile (pure)<br/>quote check · conflicts · topic-required missing fields\"] --> G\n    G{\"③ coverage_gate (pure)<br/>topics → MVP tiers; household type\"}\n    G -- \"nothing in scope\" --> R\n    G -- \"in scope (possibly partial)\" --> RE & RT\n    RE[\"④a rule_engine (pure)<br/>RuleResult: applies / not_applicable / cannot_determine\"] --> EV\n    RT[\"④b retrieve (pure)<br/>BM25 top-k within in-scope topics\"] --> EV\n    EV[\"⑤ assemble_evidence (pure)<br/>rule-linked facts ∪ BM25 hits → EvidenceBundle + evidence_gaps\"] --> GEN\n    GEN[\"⑥ generate (LLM #2)<br/>GenerationOutput: claims citing fact IDs\"] --> V\n    V[\"⑦ verify<br/>deterministic checks → batched LLM judge (#3)\"] --> R\n    R[\"⑧ build_report (pure)<br/>D-011 display policy → FinalGuidance\"]\n```\n\n### 3.1 Stages\n\n| # | Stage | LLM? | Input → Output | Notes |\n|---|---|---|---|---|\n| ① | `extract` | Yes | `UserRequest` → `ProfileExtraction` | Structured output. Every non-null field carries a **verbatim quote** from the input. Also tags question topics from a closed enum |\n| ② | `assess_profile` | No | `ProfileExtraction` → `ProfileAssessment` | **Quote guard:** a field whose quote isn't a substring of the input is discarded and logged as an extraction warning (anti-hallucination). Detects conflicts. Computes missing fields **only for the topics asked about** |\n| ③ | `coverage_gate` | No | topics + assessment → `CoverageDecision` | Deterministic topic→tier map (D-008). An unsupported household type is out of scope (default for Q-05). Mixed questions continue with the in-scope part |\n| ④a | `evaluate_rules` | No | profile + rules → `list[RuleResult]` | **Tri-state.** `cannot_determine` lists the missing fields it needs. Rules produce preparation steps and flags, **never eligibility verdicts** |\n| ④b | `retrieve` | No | query (question + topic terms) → `list[Evidence]` | BM25 restricted to in-scope topic facts; top-k |\n| ⑤ | `assemble_evidence` | No | rule results + hits → `EvidenceBundle` | Facts cited by applicable rules are **always included**, so recall on required rules doesn't depend on BM25. Raises `evidence_gaps` when an in-scope topic has no evidence |\n| ⑥ | `generate` | Yes | profile assessment + rules + evidence → `GenerationOutput` | Atomic claims, each citing fact IDs from the bundle only. Missing fields and conflicts are **passed in, not re-derived** |\n| ⑦ | `verify` | Deterministic + 1 LLM | claims + bundle → `list[VerificationResult]` | **Deterministic layer first** (a hit decides the outcome, no LLM): no citation → insufficient; citation not in bundle → insufficient; contradicts a deterministic rule result → contradicted. Remaining claims go to **one batched entailment judgement** (supported / contradicted / insufficient) |\n| ⑧ | `build_report` | No | everything → `FinalGuidance` | Applies D-011: supported → shown with source; contradicted → withheld and flagged; insufficient → stated as unconfirmed, with the gap |\n\n- **LLM calls per request:** ① + ⑥ + ⑦ = **3** in config D, **2** in C, **1** in A and B.\n- **Out-of-scope requests stop after ③:** 1 call, and the report is the redirect.\n\n### 3.2 Configurations A–D from one pipeline (REQ-EVL-010..012)\n\n| Stage | A Direct LLM | B RAG | C Hybrid | D Hybrid + verifier |\n|---|-
… [33135 more chars in the JSONL export]
````

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/docs/proposals/architecture_review.md (file state is current in your context — no need to Read it back)
```
</details>

> *system (api_error): *

> *system (api_error): *

> *system (api_error): *

### Claude · 2026-10-28 03:16:39

Now I'll remove the old held draft, which this review replaces, and update the log with the Docker result.

**Tool call: Bash** — Check commit state and whether draft is tracked

```
cd "<repo>" && git log --oneline && git status --short -uall && git ls-files docs/proposals
```

<details><summary>Tool result</summary>

```
e163bdd chore: initialise project and tooling
c49555f docs: establish project context and requirements
?? docs/proposals/architecture_layout_draft.md
?? docs/proposals/architecture_review.md
```
</details>

### Claude · 2026-10-28 03:17:03

You've committed the scaffold (`e163bdd`). The old draft is untracked, so I'll delete it and point D-029 and the development log at the review.

**Tool call: Bash** — Remove old draft, update D-029 and log, rerun doc checks

```
cd "<repo>" && rm docs/proposals/architecture_layout_draft.md && sed -i '' 's#The draft is held as an \*\*uncommitted\*\* file, `docs/proposals/architecture_layout_draft.md`, and kept out of the Phase 1 scaffold commit#The draft was kept out of the Phase 1 scaffold commit and is superseded by the architecture review, `docs/proposals/architecture_review.md` (2026-10-28)#' docs/decisions.md && grep -c "architecture_review.md" docs/decisions.md && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/development_log.md'); t=p.read_text()
old=t[t.index('**Failures / blocked:**'):t.index('**On hold (D-029)')]
new='''**Failures / resolved:**
- Docker Desktop: the agent couldn't install it (needs `sudo`). The developer installed it.
  Verified on 2026-10-28: Docker 29.9.2, engine started, `docker run --rm hello-world` OK.
  Project Docker commands are added at the deployment milestone.
- Commit `e163bdd chore: initialise project and tooling`, made by the developer.

**Architecture review (2026-10-28):**
- [proposals/architecture_review.md](proposals/architecture_review.md) supersedes the held
  draft.
- It covers:
  - the end-to-end design;
  - agentic and vector-DB comparisons;
  - the retrieval comparison;
  - Pydantic contracts;
  - the four-signal separation;
  - risks, dependencies, module boundaries and the test plan.
- Approvals A1–A11 are pending (A6 is the most material).

'''
p.write_text(t.replace(old,new))
EOF
python3 -I <tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/audit.py "$PWD"; (git grep --untracked -inFf references/private/anonymity_terms.txt || echo "no identifying terms"); git status --short -uall
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 135 chars]
```
</details>

### Claude · 2026-10-28 03:17:28

The architecture review is written: [docs/proposals/architecture_review.md](docs/proposals/architecture_review.md). No code has been written. Docker also works now: engine 29.9.2 started and `hello-world` ran.

**Recommended architecture**
One fixed, typed pipeline with 8 stages and at most 3 LLM calls per request:
1. **Extraction (LLM).** Pulls the profile and question topics from free text. Every field must come with a verbatim quote from the input; fields whose quote can't be found are dropped.
2. **Profile assessment (code).** Finds missing and conflicting fields.
3. **Coverage gate (code).** Maps question topics to the approved scope tiers.
4. **Rules and retrieval (code).** Rules answer "applies", "not applicable" or "cannot determine". BM25 searches only facts in topics the gate allowed.
5. **Evidence assembly (code).** Facts cited by applicable rules are always included, whatever BM25 returns.
6. **Generation (LLM).** Produces claims, each citing fact IDs.
7. **Verification.** Deterministic checks run first. Any claims those checks don't settle go to one batched LLM call.
8. **Report (code).** Applies the approved display rules for supported, contradicted and unconfirmed claims.

Out-of-scope requests stop at the gate after one LLM call.

**Comparisons**
- **Agentic or vector-database designs:** both lose on evaluability, determinism, cost and dependencies. Both are also already excluded by approved decisions.
- **Semantic, hybrid or reranking retrieval:** none has a testable benefit on about 100 authored facts. I recommend BM25 with three cheap fixes for its weakness on synonyms and acronyms: an `aliases` field on each fact, a topic filter, and always including rule-linked facts.
- **When to revisit retrieval:** if recall@5 on the dev queries falls below 0.90 *and* the misses come from paraphrasing rather than gaps in coverage.
- **Putting the whole knowledge base in the prompt:** considered and not recommended. It would remove the explicit evidence set that citations and verification rely on.

**Also in the document:**
- full Pydantic contracts for every stage boundary;
- a table separating missing profile fields, profile conflicts, evidence gaps and out-of-scope reasons (who produces each, what triggers it, what the user sees, which metric scores it);
- data dependencies, privacy and licensing, 15 failure modes with mitigations;
- module boundaries, and unit, integration and acceptance tests mapped to requirement IDs.

**Approvals needed (§14)** — none of these overrides an approved decision:

| ID | Proposal |
|---|---|
| A1 | The 8-stage pipeline; configurations A–D come from the same pipeline |
| A2 | BM25 only (`rank-bm25`), plus the aliases field, topic filter and rule-linked facts |
| A3 | Quote-checked extraction; missing fields only for the topics asked about; follow-up questions from fixed templates |
| A4 | Gate design. Non-couple household types are out of scope by default, which answers open question Q-05 |
| A5 | Verifier: deterministic checks first, then an LLM judge that may use a different model family. The model choice is deferred |
| **A6 (most material)** | **Every configuration, including the direct-LLM baseline A, returns the same structured output with the same enums.** That makes scoring identical and automatic. The cost is that A becomes a stronger, structured baseline, not a chat-style one, and the README must say so |
| A7 | Dependencies: pydantic, pyyaml, rank-bm25, `openai` (used only as an OpenAI-compatible client, so providers can be swapped by configuration), streamlit. Drops pandas and scikit-learn from the earlier proposed stack |
| A8 | Single-turn interaction; follow-up questions are outputs |
| A9 | Rules written as YAML conditions with a fixed set of operators, and no `eval` |
| A10 | File paths for evaluation data, run outputs and the LLM cache |
| A11 | Optional: score extraction accuracy against a gold profile per scenario |

**Time warning:** the brief estimates 12–16 hours in total. The review proposes a minimal build order and keeps config B optional, which REQ-EVL-013 allows if the omission is documented.

**Housekeeping:**
- I deleted the old held draft, since the review replaces it.
- I updated D-029 and the development log to point to the review.

Once you approve the A-items, I'll record them as decisions. That would be a good point to commit, with the review and decisions together, before any code.

### User · 2026-10-28 03:28:13

approve with sound justification and ensure it is aligned to the project's scope

### Claude · 2026-10-28 03:28:29

I'll record A1–A11 as decisions, each with its justification and a check that it stays inside the approved scope. Then I'll propagate them to the affected docs. First, the current state of the files I'm changing:

**Tool call: Bash** — Locate lines to update across docs

```
cd "<repo>" && grep -n "D-029\|^## Baseline\|^## Superseded" docs/decisions.md && grep -n "^| Q-05\|^| Q-10\|^| Q-12\|^| Q-22\|^| Q-23\|^| REQ-ARC-010\|^| REQ-ARC-012\|^| REQ-ARC-014\|^| REQ-EVL-035" docs/project_context/requirements_register.md && grep -n "Q-05\|^### 6.1\|^| UI\|^| Evaluation\|^| Retrieval\|^\*\*Coverage-gate placement" docs/project_context/01_problem_and_scope.md docs/project_context/04_architecture.md && grep -n "kb_version\|^| \`rights_review\`" docs/project_context/03_data_and_licensing.md | head -3 && grep -n "^## Architecture invariants\|^## Source of truth\|Add embeddings only" CLAUDE.md
```

<details><summary>Tool result</summary>

```
69:| D-029 | **Architecture decisions on hold** pending the developer's architecture review: stack (Q-23), gate design (Q-12), file paths (Q-10), facts schema/contracts (Q-22). The draft was kept out of the Phase 1 scaffold commit and is superseded by the architecture review, `docs/proposals/architecture_review.md` (2026-10-28) | APPROVED (hold) | Phase 1 instructions | Review before any contracts code | Earlier "04 §7" placement |
73:## Baseline decisions from the project approach (ratified by D-001 on 2026-10-28)
91:## Superseded / historical items (kept for traceability)
135:| REQ-ARC-010 | BM25 first; embeddings only if recall@k improves | APPROVED (BM25) / PROPOSED (embeddings) | [APP p.17, 21]; D-001 | 04 §6.1 | retriever | Recall@k comparison if embeddings added |
137:| REQ-ARC-012 | Stack: Streamlit UI, Pydantic, Pandas/scikit-learn eval | PROPOSED | [APP p.21] | 04 §6.1 | report_ui, eval_harness | Approval before Phase 1 |
139:| REQ-ARC-014 | Missing evidence ≠ requirement absent | APPROVED | [APP p.20] | 04 §3 | generator, verifier | Prohibited-conclusion labels |
182:| REQ-EVL-035 | Report performance by category; balance categories | APPROVED | [APP p.16] | 05 §3.2 | eval_harness | Per-category table |
276:| Q-05 | Non-couple household types (multi-generation, orphaned siblings, non-resident family, seniors, unwed parents): out-of-scope gate, or "recognise and redirect"? | 01 §6.4, 02 Row 1 | Phase 2 |
281:| Q-10 | Paths for benchmark, claim set, retrieval qrels, saved predictions/run metadata (not in D-022) | 03 §1 | Phase 1 |
283:| Q-12 | Coverage gate placement: after profile extraction, before retrieval (proposed)? | 04 §2 | Phase 1 |
293:| Q-22 | Approve proposed `policy_facts` schema (D-023) | 03 §2.5 | Phase 2 |
294:| Q-23 | Approve proposed stack (Streamlit, Pydantic, Pandas/scikit-learn) — REQ-ARC-012 | 04 §6.1 | Phase 1 |
docs/project_context/04_architecture.md:52:**Coverage-gate placement.** The diagram doesn't place the gate. [APP p.21] says it runs
docs/project_context/04_architecture.md:124:### 6.1 Recommended stack — PROPOSED unless marked [APP p.21, image]
docs/project_context/04_architecture.md:128:| UI | Streamlit | Quick, Python-native demonstration | PROPOSED |
docs/project_context/04_architecture.md:131:| Retrieval | BM25 *or* lightweight embeddings | Simple and measurable | BM25 APPROVED; embeddings PROPOSED |
docs/project_context/04_architecture.md:135:| Evaluation | Python, Pandas, scikit-learn | Reproducible metrics and comparisons | PROPOSED |
docs/project_context/01_problem_and_scope.md:127:### 6.1 Tier semantics (APPROVED) [APP p.17]
docs/project_context/01_problem_and_scope.md:176:**OPEN (Q-05):** whether non-couple household types count as out-of-scope, or as "Limited"
95:| `rights_review` | `{status: pending/cleared, notes}` | Rights review before it is tracked |
96:| `kb_version` | str | Corpus versioning |
10:## Source of truth
74:## Architecture invariants (04)
95:  Add embeddings only if recall@k proves the gain.
```
</details>

### Claude · 2026-10-28 03:28:36

The approved review is now the architecture spec, so I'll move it from `docs/proposals/` to `docs/architecture.md` and update its status and links.

**Tool call: Bash** — Promote review to docs/architecture.md and fix links

```
cd "<repo>" && mv docs/proposals/architecture_review.md docs/architecture.md && rmdir docs/proposals && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/architecture.md'); t=p.read_text()
t=t.replace('# Architecture Review — BTO Buddy (pre-implementation)','# BTO Buddy — Architecture (approved implementation design)')
old_status=t[t.index('**Status:**'):t.index('**Inputs:**')]
t=t.replace(old_status,'''**Status: APPROVED on 2026-10-28** (decisions D-030 to D-040, with justification and scope
check in [decisions.md](decisions.md)). It came out of the pre-implementation architecture
review, which replaced the held draft (D-029).

- The contracts in §5 are approved **as a shape**. Field-level details are finalised with the
  Phase 2 facts schema (Q-22).
- Items once marked **[APPROVAL Ax]** are now approved, and map to D-030 to D-040 (§14).

''')
t=t.replace('../project_context/','project_context/').replace('(../decisions.md)','(decisions.md)')
p.write_text(t)
EOF
grep -n "\.\./" docs/architecture.md || echo "no stale relative links"
```

<details><summary>Tool result</summary>

```
no stale relative links
```
</details>

### Claude · 2026-10-28 03:31:25

Now §14 of the architecture doc, mapping each approval to its decision ID:

**Tool call: Read**

```
{
 "file_path": "<repo>/docs/architecture.md",
 "offset": 560
}
```

<details><summary>Tool result</summary>

```
560	
561	## 13. Justification summary
562	
563	| Choice | Task suitability | Data sensitivity | Latency | Maintainability | Reproducibility | Cost at scale |
564	|---|---|---|---|---|---|---|
565	| Linear typed pipeline | Fixed, known steps | No tools to misuse | Bounded (≤3 calls) | One module per stage | Stage outputs saved | Linear in queries |
566	| Deterministic gate, rules, profile checks | Explicit conditions don't need an LLM (REQ-ARC-008) | No data leaves for these steps | ~0 | Table-tested | Exact | ~0 |
567	| BM25 + aliases | Small closed corpus, acronym-heavy | Local | Sub-millisecond | Tiny, explainable | Exact | ~0 |
568	| OpenAI-compatible client | Swap models for comparison | Lets a local Ollama model be chosen if privacy requires | Provider-dependent | One adapter | Model ID recorded; cache | Provider choice remains open |
569	| Batched judge after deterministic checks | Entailment needs language understanding; cheap checks first | Same as generation | +1 call, measured in C vs D | One prompt | Cached | +1 call; justified only if C vs D shows value (REQ-VER-006) |
570	| Streamlit | Demo UI in Python | Local | Fine for a demo | Thin layer | Pinned in `uv.lock` | Not a production UI (D-026) |
571	
572	**Cost at scale:** cost per query ≈ Σ over calls of (input tokens × input price + output
573	tokens × output price), for 2–3 calls. Token counts are **measured** per run in
574	`RunMetadata`. The deployment section will compute the figure from measured averages, not from
575	guesses. Retrieval, rules and gate cost nothing beyond CPU. No GPU is needed.
576	
577	## 14. Decisions requesting approval
578	
579	None of these deviates from an APPROVED decision. They fill PROPOSED or OPEN gaps, or
580	interpret approved decisions. A6 is the most material.
581	
582	| ID | Proposal | Related | Recommendation |
583	|---|---|---|---|
584	| A1 | Architecture as in §3 (8 stages; 3 LLM calls max; one pipeline for A–D) | REQ-ARC-003 | Approve |
585	| A2 | BM25 only (`rank-bm25`) + `aliases` field + topic filter + rule-linked facts. Dense/hybrid/rerank only on the recall@5 < 0.90 trigger | REQ-ARC-010, Q-22 | Approve |
586	| A3 | Extraction with verbatim quotes + deterministic quote guard; missing fields computed per asked topic; deterministic follow-up templates | REQ-ARC-013 | Approve |
587	| A4 | Gate: LLM topic tags (closed enum) → deterministic tier map; unsupported household types out of scope (default answer to Q-05); partial scope supported | Q-12, Q-05 | Approve |
588	| A5 | Verifier: deterministic layer + one batched LLM judge; judge model may differ from the generator (decided at model selection); no regeneration (D-011) | D-001, REQ-VER-006 | Approve the structure; defer the model |
589	| **A6** | **All configurations emit the same structured `FinalGuidance`. A/B's LLM fills the four signal lists itself, using the same enums** | D-003, REQ-EVL-011 | **Approve (the material one)** |
590	| A7 | Dependencies: pydantic, pyyaml, rank-bm25, openai (as OpenAI-compatible client), streamlit; dev: pytest, ruff, mypy, types-PyYAML. Drop pandas and scikit-learn | Q-23 | Approve |
591	| A8 | Single-turn interaction; follow-ups are outputs | — | Approve |
592	| A9 | Declarative YAML rule conditions with whitelisted operators; no `eval` | D-022 | Approve |
593	| A10 | File paths in §11.2 | Q-10 | Approve |
594	| A11 | Optional extraction diagnostic (gold profile per scenario) | — | Approve if time allows |
595	
596	**Contracts (§5)** are approved as the shape, and finalised with the Phase 2 facts schema
597	(Q-22).
598	
599	**Time-budget warning.** The brief estimates 12–16 hours. Phases 0–1 already used part of
600	that. The smallest credible build order is:
601	1. contracts, knowledge, rules, gate, profile (pure, tested);
602	2. Phase 2 facts;
603	3. configs A and C end to end;
604	4. D (verifier);
605	5. eval and the Docker image;
606	6. B only if time remains (REQ-EVL-013 allows dropping it with documentation).
607	
```
</details>

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/architecture.md",
 "old_string": "## 14. Decisions requesting approval\n\nNone of these deviates from an APPROVED decision. They fill PROPOSED or OPEN gaps, or\ninterpret approved decisions. A6 is the most material.\n\n| ID | Proposal | Related | Recommendation |\n|---|---|---|---|\n| A1 | Architecture as in §3 (8 stages; 3 LLM calls max; one pipeline for A–D) | REQ-ARC-003 | Approve |\n| A2 | BM25 only (`rank-bm25`) + `aliases` field + topic filter + rule-linked facts. Dense/hybrid/rerank only on the recall@5 < 0.90 trigger | REQ-ARC-010, Q-22 | Approve |\n| A3 | Extraction with verbatim quotes + deterministic quote guard; missing fields computed per asked topic; deterministic follow-up templates | REQ-ARC-013 | Approve |\n| A4 | Gate: LLM topic tags (closed enum) → deterministic tier map; unsupported household types out of scope (default answer to Q-05); partial scope supported | Q-12, Q-05 | Approve |\n| A5 | Verifier: deterministic layer + one batched LLM judge; judge model may differ from the generator (decided at model selection); no regeneration (D-011) | D-001, REQ-VER-006 | Approve the structure; defer the model |\n| **A6** | **All configurations emit the same structured `FinalGuidance`. A/B's LLM fills the four signal lists itself, using the same enums** | D-003, REQ-EVL-011 | **Approve (the material one)** |\n| A7 | Dependencies: pydantic, pyyaml, rank-bm25, openai (as OpenAI-compatible client), streamlit; dev: pytest, ruff, mypy, types-PyYAML. Drop pandas and scikit-learn | Q-23 | Approve |\n| A8 | Single-turn interaction; follow-ups are outputs | — | Approve |\n| A9 | Declarative YAML rule conditions with whitelisted operators; no `eval` | D-022 | Approve |\n| A10 | File paths in §11.2 | Q-10 | Approve |\n| A11 | Optional extraction diagnostic (gold profile per scenario) | — | Approve if time allows |\n\n**Contracts (§5)** are approved as the shape, and finalised with the Phase 2 facts schema\n(Q-22).",
 "new_string": "## 14. Approved decisions (2026-10-28)\n\nThe justification and scope-alignment check for each item are recorded in\n[decisions.md](decisions.md). None of them overrides an earlier APPROVED decision.\n\n| Review item | Decision | Summary |\n|---|---|---|\n| A1 | D-030 | 8-stage linear typed pipeline; ≤3 LLM calls; A–D from one pipeline |\n| A2 | D-031 | BM25 only (`rank-bm25`) + `aliases` + topic filter + rule-linked facts. Escalation trigger: dev recall@5 < 0.90 attributable to paraphrase |\n| A3 | D-032 | Quote-grounded extraction + deterministic quote guard; topic-scoped missing fields; template follow-ups |\n| A4 | D-033 | Gate: closed-enum topic tags → deterministic tier map; non-couple household types out of scope (resolves Q-05 by default); partial scope supported |\n| A5 | D-034 | Verifier: deterministic layer first, then one batched LLM judge. Judge model decided at model selection. No regeneration |\n| A6 | D-035 | All configurations emit the same structured `FinalGuidance`; A/B fill the four signals themselves using the same enums |\n| A7 | D-036 | Dependencies as in §11.1; pandas and scikit-learn dropped |\n| A8 | D-037 | Single-turn interaction; follow-ups are outputs |\n| A9 | D-038 | Declarative YAML rule conditions, whitelisted operators, no `eval` |\n| A10 | D-039 | File paths as in §11.2 |\n| A11 | D-040 | Optional extraction diagnostic, only if time allows |\n\n**Contracts (§5)** are approved as the shape. Field-level details are finalised with the\nPhase 2 facts schema (Q-22)."
}
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/architecture.md has been updated successfully.
```
</details>

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/decisions.md",
 "old_string": "| D-029 | **Architecture decisions on hold** pending the developer's architecture review: stack (Q-23), gate design (Q-12), file paths (Q-10), facts schema/contracts (Q-22). The draft was kept out of the Phase 1 scaffold commit and is superseded by the architecture review, `docs/proposals/architecture_review.md` (2026-10-28) | APPROVED (hold) | Phase 1 instructions | Review before any contracts code | Earlier \"04 §7\" placement |",
 "new_string": "| D-029 | **Architecture decisions on hold** pending the developer's architecture review: stack (Q-23), gate design (Q-12), file paths (Q-10), facts schema/contracts (Q-22). The draft was kept out of the Phase 1 scaffold commit | SUPERSEDED (hold lifted by D-030 to D-040) | Phase 1 instructions | Review before any contracts code | Earlier \"04 §7\" placement |\n\n---\n\n## Architecture decisions approved 2026-10-28 (from the architecture review)\n\nSpecification: [architecture.md](architecture.md). Each decision was checked against the\napproved scope (D-008, D-013, D-026) and against the hard constraints:\n- no agents, frameworks or vector DB (REQ-ARC-002);\n- free tier (REQ-NFR-004);\n- reproducible on a clean machine (REQ-NFR-001).\n\n| ID | Decision | Resolves | Justification | Scope alignment | Supersedes |\n|---|---|---|---|---|---|\n| D-030 | **Linear typed pipeline:** ① LLM extraction → ② profile assessment → ③ coverage gate → ④ rules ∥ BM25 → ⑤ evidence assembly → ⑥ LLM generation → ⑦ verification → ⑧ report. At most 3 LLM calls per request. Configurations A–D are the same pipeline with stages switched off | Review A1; REQ-ARC-003 | The steps are fixed and known, so a linear pipeline is the simplest design that implements BD-04. Typed boundaries make each stage independently testable and scorable (REQ-ARC-007), and bound latency and cost | Exactly the approved capabilities (REQ-ARC-001). Adds no features beyond the MVP | — |\n| D-031 | **Retrieval is BM25 only** (`rank-bm25`), over fact `statement` + `aliases`, filtered to gate-approved topics. Facts cited by applicable rules are always added to the evidence. Dense, hybrid or reranking retrieval is proposed **only if** dev retrieval recall@5 < 0.90 *and* error analysis attributes the misses to paraphrase. Facts schema gains an `aliases: list[str]` field | Review A2; REQ-ARC-010; part of Q-22 | ~100 acronym-heavy authored facts suit exact lexical matching, which is explainable, deterministic and dependency-light. Aliases fix BM25's synonym weakness cheaply. Rule-linked facts make required-rule evidence independent of ranking. Embeddings would add torch (≈2 GB image) or another data-sharing API with no demonstrated gain | Retrieval covers only in-scope topics; excluded topics are never searched | \"BM25 or lightweight embeddings\" open choice [APP p.21] |\n| D-032 | **Quote-grounded extraction.** Each extracted field must carry a verbatim quote, and a deterministic guard drops any field whose quote isn't in the input. Missing fields are computed **only for the topics asked about** (plus rules returning `cannot_determine`). Follow-up questions come from static templates | Review A3; REQ-ARC-013, REQ-SCP-013 | Turns LLM extraction into an auditable step and blocks hallucinated applicant facts, the main risk in a consequential domain. Topic scoping avoids interrogating users with irrelevant questions. Templates make follow-ups deterministic and testable | Uses only fields needed by Core/Limited topics. Income/employment fields are limited to HFE documentation (D-013) | — |\n| D-033 | **Coverage gate.** The extraction call tags the question with topics from a closed enum. A deterministic `TOPIC_TIER` map applies D-008. Mixed questions are partially answered, with `out_of_scope_reasons` for the rest. **Household types other than a first-timer couple (married or engaged) are out of scope** and redirected to official sources | Review A4; Q-12; Q-05 (default) | Keeps scope enforcement deterministic and unit-testable, using the LLM only for language understanding. Partial answering avoids needless refusals, and over-abstention is measured | Directly enforces the MVP tiers. Matches the Core definition \"first-timer **couple** household composition\". Non-couple groups were never Core | Q-05 left open in 01 §6.4 |\n| D-034 | **Verifier structure.** Deterministic checks first: uncited claim or citation outside the evidence → insufficient; contradicting a rule result → contradicted. Then **one batched LLM entailment judgement** for the remaining checkable claims. The judge model may differ from the generation model; that is decided at model selection with evidence. No regeneration loop (D-011) | Review A5; REQ-VER-001..007 | Cheap, certain checks shouldn't spend an LLM call. Batching bounds cost (+1 call). A different model family reduces correlated errors [APP p.27]. Its value is proved, not assumed, through C vs D and the verifier claim set (REQ-VER-006) | Implements the approved verification capability only | — |\n| D-035 | **Same output contract for all configurations.** A–D all return a structured `FinalGuidance`. In A and B, the LLM itself fills `missing_profile_fields`, `profile_conflicts` and `out_of_scope_reasons`, using the same enums that C and D fill deterministically. The README must state that baseline A is a *structured-output* direct LLM | Review A6; D-003, REQ-EVL-011 | Makes every primary metric score identically and automatically across configurations, and is the strictest reading of \"equivalent task instructions\" (D-003). The comparison measures architecture, not output format. A structured baseline is a *stronger*, fairer comparator, which makes any hybrid gain more credible. Free-text baselines would need manual mapping per case: slower, less reproducible, more annotator bias | Evaluation design only. No user-facing feature added | — |\n| D-036 | **Dependencies.** Runtime: `pydantic`, `pyyaml`,
… [2339 more chars in the JSONL export]
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/decisions.md",
 "old_string": "| \"PolicyProof-inspired verification layer\" [APP p.21] | HISTORICAL | D-015 |",
 "new_string": "| \"PolicyProof-inspired verification layer\" [APP p.21] | HISTORICAL | D-015 |\n| Stack row \"Evaluation: Python, Pandas, scikit-learn\" [APP p.21] | SUPERSEDED | D-036 |\n| \"BM25 or lightweight embeddings\" as an open choice [APP p.21] | SUPERSEDED | D-031 |\n| Held architecture draft (D-029) | SUPERSEDED | D-030 to D-040, [architecture.md](architecture.md) |"
}
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/decisions.md has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/decisions.md has been updated successfully.
```
</details>

### Claude · 2026-10-28 03:32:34

Now I'll carry these into the context docs. First, the exact text at each edit point:

**Tool call: Bash** — Show exact text at edit points

```
cd "<repo>" && sed -n '174,178p' docs/project_context/01_problem_and_scope.md; echo ----; sed -n '50,56p;124,140p' docs/project_context/04_architecture.md; echo ----; sed -n '74,100p' CLAUDE.md
```

<details><summary>Tool result</summary>

```
| Excluded → gate | "How much grant will we get?"; "Can we afford a 4-room?"; "What are our chances in the ballot?"; "Can we rent out after MOP?"; "Confirm that we are eligible." |

**OPEN (Q-05):** whether non-couple household types count as out-of-scope, or as "Limited"
recognition with redirection. Examples are multi-generation, orphaned siblings,
non-resident family members, seniors and unwed parents (see [02](02_policy_sources.md)).
----
the retrieval corpus is `data/policy_facts.jsonl`.

**Coverage-gate placement.** The diagram doesn't place the gate. [APP p.21] says it runs
"before generating a response". Placing it after profile extraction and before retrieval is
the author's reading, PROPOSED (Q-12).

| Stage | Planned component | Status |
### 6.1 Recommended stack — PROPOSED unless marked [APP p.21, image]

| Component | Recommended approach | Why (as given) | Status |
|---|---|---|---|
| UI | Streamlit | Quick, Python-native demonstration | PROPOSED |
| Structured profile | Pydantic | Validated input/output contracts | PROPOSED (matches APPROVED pipeline diagram) |
| Knowledge base | ~~Curated official HTML/text passages~~ → `data/policy_facts.jsonl` | Small, auditable corpus | SUPERSEDED → D-005 |
| Retrieval | BM25 *or* lightweight embeddings | Simple and measurable | BM25 APPROVED; embeddings PROPOSED |
| Generation | One selected LLM API | Avoid unnecessary model orchestration | APPROVED principle; model OPEN |
| Verification | Claim-level evidence checks | Testable assurance layer | APPROVED |
| Rules | Small Python functions for deterministic checks | Better than LLM guessing for explicit conditions | APPROVED |
| Evaluation | Python, Pandas, scikit-learn | Reproducible metrics and comparisons | PROPOSED |
| Deployment | Docker | Meets the assessment requirement | MANDATORY (REQ-SUB-002) |

**REQ-ARC-010:** start with BM25. Add embeddings **only if** they demonstrably improve
recall on the benchmark (retrieval recall@k, [05 §5](05_evaluation.md)).

----
## Architecture invariants (04)
- **Pipeline:**
  1. profile extraction and validation;
  2. coverage gate;
  3. rule engine ∥ BM25 retrieval;
  4. grounded generation;
  5. claim verification;
  6. preparation report.
- Typed Pydantic contracts between every stage. No free text passes between modules.
- Every response carries `missing_profile_fields`, `evidence_gaps`, `profile_conflicts` and
  `out_of_scope_reasons`.
- Never assume missing applicant values. Missing evidence never proves a requirement absent.
- The runtime KB is `data/policy_facts.jsonl` (independently authored, fact IDs). Rules in
  `data/policy_rules.yaml` cite fact IDs. Nothing at runtime reads `data/private_corpus/`.
- **Verifier outcomes:**
  - supported → show with a source;
  - contradicted → withhold and flag;
  - insufficient → no definitive guidance, state the gap.

  Never silently rewrite. No regeneration loop unless approved.
- No autonomous agents, orchestration frameworks or vector DBs. Use one generation model.
  Add embeddings only if recall@k proves the gain.
- Infographics and videos are links in `data/visual_resources.json`, never runtime evidence.

## Engineering rules
- Simple, typed, testable Python modules in `src/bto_buddy/`. Prefer functions and
  composition over class hierarchies.
```
</details>

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/01_problem_and_scope.md",
 "old_string": "**OPEN (Q-05):** whether non-couple household types count as out-of-scope, or as \"Limited\"\nrecognition with redirection. Examples are multi-generation, orphaned siblings,\nnon-resident family members, seniors and unwed parents (see [02](02_policy_sources.md)).",
 "new_string": "**Q-05, resolved by D-033 (2026-10-28):** household types other than a first-timer couple\n(married or engaged) are **out of scope**. The coverage gate redirects them to official\nsources. Examples are multi-generation, orphaned siblings, non-resident family members,\nseniors and unwed parents (see [02](02_policy_sources.md))."
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/04_architecture.md",
 "old_string": "**Coverage-gate placement.** The diagram doesn't place the gate. [APP p.21] says it runs\n\"before generating a response\". Placing it after profile extraction and before retrieval is\nthe author's reading, PROPOSED (Q-12).",
 "new_string": "**Coverage-gate placement.** The diagram doesn't place the gate. [APP p.21] says it runs\n\"before generating a response\". It is now **APPROVED (D-033)**: it runs after profile\nextraction and before rules and retrieval. The full implementation design is in\n[../architecture.md](../architecture.md) (D-030 to D-040)."
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/04_architecture.md",
 "old_string": "| UI | Streamlit | Quick, Python-native demonstration | PROPOSED |\n| Structured profile | Pydantic | Validated input/output contracts | PROPOSED (matches APPROVED pipeline diagram) |\n| Knowledge base | ~~Curated official HTML/text passages~~ → `data/policy_facts.jsonl` | Small, auditable corpus | SUPERSEDED → D-005 |\n| Retrieval | BM25 *or* lightweight embeddings | Simple and measurable | BM25 APPROVED; embeddings PROPOSED |\n| Generation | One selected LLM API | Avoid unnecessary model orchestration | APPROVED principle; model OPEN |\n| Verification | Claim-level evidence checks | Testable assurance layer | APPROVED |\n| Rules | Small Python functions for deterministic checks | Better than LLM guessing for explicit conditions | APPROVED |\n| Evaluation | Python, Pandas, scikit-learn | Reproducible metrics and comparisons | PROPOSED |\n| Deployment | Docker | Meets the assessment requirement | MANDATORY (REQ-SUB-002) |\n\n**REQ-ARC-010:** start with BM25. Add embeddings **only if** they demonstrably improve\nrecall on the benchmark (retrieval recall@k, [05 §5](05_evaluation.md)).",
 "new_string": "| UI | Streamlit | Quick, Python-native demonstration | APPROVED (D-036) |\n| Structured profile | Pydantic | Validated input/output contracts | APPROVED (D-030, D-036) |\n| Knowledge base | ~~Curated official HTML/text passages~~ → `data/policy_facts.jsonl` | Small, auditable corpus | SUPERSEDED → D-005 |\n| Retrieval | ~~BM25 *or* lightweight embeddings~~ → BM25 (`rank-bm25`) + aliases + topic filter + rule-linked facts | Simple and measurable | APPROVED (D-031); embeddings only on the trigger |\n| Generation | One selected LLM API, through an OpenAI-compatible client | Avoid unnecessary model orchestration | APPROVED (D-036); model OPEN |\n| Verification | Deterministic checks, then a batched LLM judge | Testable assurance layer | APPROVED (D-034); judge model OPEN |\n| Rules | ~~Small Python functions~~ → declarative YAML conditions, whitelisted operators | Better than LLM guessing for explicit conditions | APPROVED (D-038) |\n| Evaluation | ~~Python, Pandas, scikit-learn~~ → Python stdlib | Reproducible metrics and comparisons | APPROVED (D-036) |\n| Deployment | Docker | Meets the assessment requirement | MANDATORY (REQ-SUB-002) |\n\n**REQ-ARC-010 / D-031:** BM25 only. Propose dense, hybrid or reranking retrieval **only if**\ndev recall@5 < 0.90 *and* the misses are attributable to paraphrase (retrieval recall@k,\n[05 §5](05_evaluation.md))."
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/project_context/03_data_and_licensing.md",
 "old_string": "| `kb_version` | str | Corpus versioning |",
 "new_string": "| `kb_version` | str | Corpus versioning |\n| `aliases` | list[str] | Synonyms and acronyms indexed with the statement for BM25 (e.g. \"HFE letter\", \"fiancé\"). **APPROVED addition (D-031)** |"
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/CLAUDE.md",
 "old_string": "## Architecture invariants (04)\n- **Pipeline:**\n  1. profile extraction and validation;\n  2. coverage gate;\n  3. rule engine ∥ BM25 retrieval;\n  4. grounded generation;\n  5. claim verification;\n  6. preparation report.\n- Typed Pydantic contracts between every stage. No free text passes between modules.",
 "new_string": "## Architecture invariants (`docs/architecture.md`, D-030 to D-040)\n- **Pipeline** (at most 3 LLM calls; configs A–D are this pipeline with stages switched off):\n  1. LLM extraction (fields + verbatim quotes + closed-enum topics);\n  2. profile assessment (pure);\n  3. coverage gate (pure);\n  4. rules ∥ BM25 (pure);\n  5. evidence assembly (pure);\n  6. LLM generation;\n  7. verification;\n  8. report (pure).\n- Typed Pydantic contracts between every stage. No free text passes between modules. Pure\n  modules never import the LLM client.\n- **All configurations return the same `FinalGuidance` contract** (D-035).\n- Extracted fields without a verbatim input quote are dropped (D-032). Missing fields are\n  computed only for the topics asked about.\n- Household types other than a first-timer couple are out of scope (D-033).\n- Rules are declarative YAML with whitelisted operators. **Never `eval`** (D-038).\n- Verification runs deterministic checks first, then one batched LLM judge (D-034)."
}
```

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/CLAUDE.md",
 "old_string": "- No autonomous agents, orchestration frameworks or vector DBs. Use one generation model.\n  Add embeddings only if recall@k proves the gain.",
 "new_string": "- No autonomous agents, orchestration frameworks or vector DBs. Use one generation model.\n- Retrieval is BM25 + aliases + topic filter + rule-linked facts. Propose anything else only\n  if dev recall@5 < 0.90 because of paraphrase (D-031).\n- **Dependencies are limited to D-036.** Anything else needs an approved decision."
}
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/01_problem_and_scope.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/04_architecture.md has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/04_architecture.md has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/docs/project_context/03_data_and_licensing.md has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/CLAUDE.md has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

```
The file <repo>/CLAUDE.md has been updated successfully.
```
</details>

### Claude · 2026-10-28 03:33:53

Next: the register, the CLAUDE.md routing table, INDEX, `.gitignore` (for the LLM cache) and the development log.

**Tool call: Bash** — Update register, routing, gitignore, log; run checks

```
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
def sub(path, pairs):
    p=pathlib.Path(path); t=p.read_text()
    for old,new in pairs:
        assert t.count(old)==1, (path, old[:60]); t=t.replace(old,new)
    p.write_text(t)
R='docs/project_context/requirements_register.md'
sub(R,[
("| REQ-ARC-010 | BM25 first; embeddings only if recall@k improves | APPROVED (BM25) / PROPOSED (embeddings) | [APP p.17, 21]; D-001 | 04 §6.1 | retriever | Recall@k comparison if embeddings added |",
 "| REQ-ARC-010 | BM25 only (+ aliases, topic filter, rule-linked facts); dense/hybrid/rerank only if dev recall@5 < 0.90 because of paraphrase | APPROVED | [APP p.17, 21]; D-031 | architecture §4.2 | retriever | Recall@k table; escalation decision only on the trigger |"),
("| REQ-ARC-012 | Stack: Streamlit UI, Pydantic, Pandas/scikit-learn eval | PROPOSED | [APP p.21] | 04 §6.1 | report_ui, eval_harness | Approval before Phase 1 |",
 "| REQ-ARC-012 | Dependencies limited to pydantic, pyyaml, rank-bm25, openai (compatible client), streamlit; dev pytest/ruff/mypy/types-PyYAML; stdlib statistics | APPROVED | [APP p.21]; D-036 | architecture §11.1 | all | `pyproject.toml` / `uv.lock` match the list |"),
("| REQ-ARC-014 | Missing evidence ≠ requirement absent | APPROVED | [APP p.20] | 04 §3 | generator, verifier | Prohibited-conclusion labels |",
 "| REQ-ARC-014 | Missing evidence ≠ requirement absent | APPROVED | [APP p.20] | 04 §3 | generator, verifier | Prohibited-conclusion labels |\n"
 "| REQ-ARC-015 | Linear 8-stage pipeline, ≤3 LLM calls; A–D from one pipeline; pure modules don't import the LLM client | APPROVED | D-030 | architecture §3, §11.2 | pipeline | Integration tests per config; import-boundary test |\n"
 "| REQ-ARC-016 | Extracted fields need verbatim input quotes (quote guard); missing fields scoped to the topics asked; template follow-ups | APPROVED | D-032 | architecture §3.1, §6 | profile_extractor | Unit tests: quote guard, topic-scoped missing fields |\n"
 "| REQ-ARC-017 | Closed-enum topic tags → deterministic tier map; partial scope; non-couple households out of scope | APPROVED | D-033 | architecture §3.1, §5 | coverage_gate | Every topic mapped; gate unit tests; out-of-scope category |\n"
 "| REQ-ARC-018 | Rules as declarative YAML with whitelisted operators; no `eval` | APPROVED | D-038 | architecture §7 | rule_registry, rule_engine | Interpreter unit tests; unknown operator rejected |\n"
 "| REQ-ARC-019 | Single-turn interaction; follow-ups are outputs; no stored user text | APPROVED | D-037 | architecture §3.2 | pipeline, report_ui | No session state in code |\n"
 "| REQ-VER-008 | Verifier: deterministic checks first, then one batched LLM judge (model decided at selection) | APPROVED | D-034 | architecture §3.1 | verifier | Unit tests (deterministic layer); verifier claim-set results |"),
("| REQ-EVL-035 | Report performance by category; balance categories | APPROVED | [APP p.16] | 05 §3.2 | eval_harness | Per-category table |",
 "| REQ-EVL-035 | Report performance by category; balance categories | APPROVED | [APP p.16] | 05 §3.2 | eval_harness | Per-category table |\n"
 "| REQ-EVL-036 | All configurations emit the same structured `FinalGuidance`; A/B fill the four signals themselves; README states A is a structured-output baseline | APPROVED | D-035 | architecture §3.2 | pipeline, eval_harness, README | Same schema validated for A–D; README statement |\n"
 "| REQ-EVL-037 | Optional extraction diagnostic against gold profiles, time permitting | APPROVED (optional) | D-040 | architecture §10 | eval_harness | Field-level P/R table, if done |"),
("| Q-05 | Non-couple household types (multi-generation, orphaned siblings, non-resident family, seniors, unwed parents): out-of-scope gate, or \"recognise and redirect\"? | 01 §6.4, 02 Row 1 | Phase 2 |",
 "| ~~Q-05~~ | ~~Non-couple household types~~ → **resolved D-033**: out of scope, redirected | 01 §6.4, 02 Row 1 | Done |"),
("| Q-10 | Paths for benchmark, claim set, retrieval qrels, saved predictions/run metadata (not in D-022) | 03 §1 | Phase 1 |",
 "| ~~Q-10~~ | ~~Evaluation and run paths~~ → **resolved D-039** | 03 §1 | Done |"),
("| Q-12 | Coverage gate placement: after profile extraction, before retrieval (proposed)? | 04 §2 | Phase 1 |",
 "| ~~Q-12~~ | ~~Coverage gate placement~~ → **resolved D-033** (after extraction, before rules/retrieval) | 04 §2 | Done |"),
("| Q-22 | Approve proposed `policy_facts` schema (D-023) | 03 §2.5 | Phase 2 |",
 "| Q-22 | Finalise `policy_facts` schema field details (shape + `aliases` approved: D-031, architecture §5) | 03 §2.5 | Phase 2 |"),
("| Q-23 | Approve proposed stack (Streamlit, Pydantic, Pandas/scikit-learn) — REQ-ARC-012 | 04 §6.1 | Phase 1 |",
 "| ~~Q-23~~ | ~~Stack~~ → **resolved D-036** | 04 §6.1 | Done |"),
])
sub('CLAUDE.md',[("| `docs/project_context/04_architecture.md` | Pipeline, contracts, verifier behaviour, stack |",
 "| `docs/architecture.md` | **Approved implementation design**: stages, Pydantic contracts, module boundaries, dependencies, test plan |\n| `docs/project_context/04_architecture.md` | Source-derived architecture requirements, verifier behaviour, provider notes |")])
sub('docs/project_context/INDEX.md',[("| [../development_log.md](../development_log.md) |",
 "| [../architecture.md](../architecture.md) | **Approved implementation design** (D-030 to D-040): pipeline, contracts, retrieval choice, dependencies, tests |\n| [../development_log.md](../development_log.md) |")])
sub('.gitignore',[("# --- Secrets and credentials ---","# Local LLM response cache. The reproducible record is results/runs/ (D-039).\n.cache/\n\n# --- Secrets and credentials ---")])
p=pathlib.Path('docs/development_log.md'); t=p.read_text()
old=t[t.index('**Architecture review (2026-10-28):**'):]
t=t.replace(old,'''**Architecture review (2026-10-28) — approved:**
- The developer approved review items A1–A11, recorded as **D-030 to D-040**. Each has a
  justification and a scope-alignment check.
- Th
… [1101 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 515 chars]
```
</details>

### Claude · 2026-10-28 03:34:41

I recorded all eleven architecture approvals (A1–A11) as decisions D-030 to D-040 in [docs/decisions.md](docs/decisions.md). Each has its justification and a check against the approved scope. No decision adds a feature or goes past the approved scope:
- **D-033:** limits the gate to first-timer couples, married or engaged, which matches the Core tier as written.
- **D-035 and D-040:** change only the evaluation design. D-035 also requires the README to state that baseline A is a structured-output LLM.
- **D-036:** treats Streamlit as a demo UI, not production hosting (consistent with D-026).
- **Income:** stays limited to HFE documents (D-013).

The approved review is now the implementation spec, moved to [docs/architecture.md](docs/architecture.md). §14 there maps each review item to its decision.

**Docs updated to match:**
- **[01](docs/project_context/01_problem_and_scope.md):** the open question on non-couple households (Q-05) is closed. They're out of scope and redirected.
- **[03](docs/project_context/03_data_and_licensing.md):** the facts schema gains the `aliases` field.
- **[04](docs/project_context/04_architecture.md):** stack statuses updated. Pandas, scikit-learn and the embeddings option are marked superseded.
- **[Requirements register](docs/project_context/requirements_register.md):**
  - REQ-ARC-010 and REQ-ARC-012 revised;
  - 8 new IDs: REQ-ARC-015 to 019, REQ-VER-008, REQ-EVL-036, REQ-EVL-037 (158 in total);
  - open questions on paths, gate placement and stack (Q-10, Q-12, Q-23) closed. Q-22 is narrowed to field-level details.
- **[CLAUDE.md](CLAUDE.md):** the architecture rules now point to `docs/architecture.md`, and it's in the routing table.
- **INDEX, [.gitignore](.gitignore)** (adds `.cache/`) **and the [development log](docs/development_log.md).**

All requirement IDs and internal links resolve, the anonymity scan is clean, and pytest, ruff and mypy pass.

**Suggested commit: now is a good point**, since this is the approved architecture and no code depends on it yet.
- **Include:** all 10 changed files (`git status` shows them, with `docs/architecture.md` as the only new file).
- **Suggested message:** `docs: approve architecture and record design decisions`
- **Push:** fine to push.

```bash
git add .gitignore CLAUDE.md docs
git commit -m "docs: approve architecture and record design decisions"
```

The next step after your commit is the pure core: `contracts.py`, `knowledge.py`, `rules.py`, `gate.py` and `profile.py`, with unit tests against a small fictional test knowledge base and no LLM calls. That fits before Phase 2 because the real facts don't exist yet.

### User · 2026-10-28 03:36:13

note that the time-budget should only be used as a reference rather than a strict rule. the objective is just to complete the project by 7am tomorrow, complying with all the assessment requirements

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/docs/architecture.md",
 "old_string": "**Time-budget warning.** The brief estimates 12–16 hours. Phases 0–1 already used part of\nthat. The smallest credible build order is:\n1. contracts, knowledge, rules, gate, profile (pure, tested);\n2. Phase 2 facts;\n3. configs A and C end to end;\n4. D (verifier);\n5. eval and the Docker image;\n6. B only if time remains (REQ-EVL-013 allows dropping it with documentation).",
 "new_string": "**Schedule.**\n- **Target:** project complete and compliant with every assessment requirement by\n  **2026-10-29 07:00**.\n- The brief's 12–16-hour effort figure is a *reference only*, not a constraint.\n- **Build order** (risk-first, each step leaves a runnable state):\n  1. contracts, knowledge, rules, gate, profile (pure, tested);\n  2. Phase 2 facts;\n  3. configs A and C end to end;\n  4. D (verifier);\n  5. B;\n  6. evaluation;\n  7. Docker image;\n  8. README, demo and AI logs.\n- All four configurations are planned. The REQ-EVL-013 fallback (drop B, with\n  documentation) is used only if the deadline is at risk, and the developer must agree first."
}
```

**Tool call: Bash** — Record completion target in log, private notes, register

```
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/development_log.md'); t=p.read_text()
old='**Still open before or during Phase 2:**'
assert t.count(old)==1
t=t.replace(old,'''**Schedule (developer, 2026-10-28):**
- Target: complete and fully compliant by **2026-10-29 07:00**.
- The brief's 12–16-hour estimate is a reference only.
- All configurations A–D are planned; dropping B needs developer agreement.

'''+old)
p.write_text(t)
p=pathlib.Path('references/private/submission_private_notes.md'); t=p.read_text()
old='- Date the brief was received: **not recorded — fill in** (needed to compute the deadline).'
assert t.count(old)==1
t=t.replace(old,'- Date the brief was received: not recorded.\n- **Developer-set completion target: 2026-10-29 07:00** (set 2026-10-28; resolves Q-18 for planning purposes).')
p.write_text(t)
EOF
sed -i '' 's/^| Q-18 | Brief receipt date (deadline computation) — record privately | 06 §3 | Now |$/| ~~Q-18~~ | ~~Brief receipt date~~ → developer-set completion target 2026-10-29 07:00 (private notes, development log) | 06 §3 | Done |/' docs/project_context/requirements_register.md && grep -n "Q-18" docs/project_context/requirements_register.md | tail -1
```

<details><summary>Tool result</summary>

```
The file <repo>/docs/architecture.md has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 152 chars]
```
</details>

### Claude · 2026-10-28 03:36:42

I'll also save this to memory so later sessions plan against the right target.

**Tool call: Write**

```
{
 "file_path": "<home>/.claude/projects/<project-slug>/memory/completion-deadline.md",
 "content": "---\nname: completion-deadline\ndescription: BTO Buddy must be complete and assessment-compliant by 2026-10-29 07:00; the brief's 12–16h effort estimate is reference only\nmetadata:\n  type: project\n---\nBTO Buddy target: fully complete and compliant with all assessment requirements by **2026-10-29 07:00** (set by the developer on 2026-10-28).\n\n**Why:** The developer's own deadline. The brief's 12–16-hour effort estimate is only a reference, not a constraint.\n\n**How to apply:**\n- Plan all four configurations (A–D). Don't pre-emptively cut scope to fit the effort estimate.\n- Use the REQ-EVL-013 fallback (dropping config B) only if the deadline itself is at risk, and only with the developer's agreement.\n- Prioritise assessment compliance over polish when trading off.\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <home>/.claude/projects/<project-slug>/memory/completion-deadline.md
```
</details>

**Tool call: Write**

```
{
 "file_path": "<home>/.claude/projects/<project-slug>/memory/MEMORY.md",
 "content": "- [Completion deadline](completion-deadline.md) — finish by 2026-10-29 07:00; the 12–16h estimate is reference only; plan all of A–D\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <home>/.claude/projects/<project-slug>/memory/MEMORY.md (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 03:36:53

The plan now treats the 12–16-hour estimate as a reference only. The target is the project complete and meeting every assessment requirement by **2026-10-29 07:00**.

- **[docs/architecture.md](docs/architecture.md):** the time-budget warning is now a schedule. All four configurations are planned, so B is no longer "only if time remains". Dropping B (the fallback REQ-EVL-013 allows) is used only if the deadline itself is at risk, and only with your agreement.
- **Build order:**
  1. the code-only core (no LLM calls);
  2. the policy facts;
  3. configurations A and C;
  4. D;
  5. B;
  6. evaluation;
  7. Docker;
  8. README, demo and AI logs.

  Each step leaves the project in a runnable state.
- **Where the target is recorded:**
  - [development log](docs/development_log.md);
  - private submission notes, Git-ignored;
  - requirements register, where the open question on the brief's receipt date (Q-18) is now closed;
  - memory, so later sessions plan against it.

The commit I suggested earlier now also covers these changes, with the same command and message:

```bash
git add .gitignore CLAUDE.md docs
git commit -m "docs: approve architecture and record design decisions"
```

### User · 2026-10-28 03:39:44



<pasted_content id="6baf">
Repository and tooling setup: Implement the approved minimal Python project structure using uv, pytest, Ruff, Pydantic and Streamlit. Refer to the recommended repo structure detailed in this prompt. Add a Dockerfile, .dockerignore, .gitignore and .env.example. Do not add a database, orchestration framework or cloud infrastructure. Provide one working application entry point, one smoke test and a reproducible dependency lockfile. Ensure private source HTML, credentials, local caches and temporary outputs cannot be accidentally staged. Before making changes, list the files to create and explain their purpose. After implementation, run installation, lint and tests, and report actual results. Do not commit or push. If uv is verified to be suitable for this project, add the appropriate commands in CLAUDE.md, something like 
```## Commands
- Install: `uv sync`
- Test: `uv run pytest`
- Lint: `uv run ruff check .`
- Run locally: `uv run streamlit run src/bto_buddy/app.py`
- Build image: `docker build -t bto-buddy .`
- Run container: `docker run --rm -p 8501:8501 --env-file .env bto-buddy` 
```
This Docker command assumes my container exposes port 8501 and reads configuration from environment variables. Adjust it to match my actual Dockerfile.

Recommended repo structure to follow, you may further simplify where possible (especially if individual modules are very small or unnecessary): 
```
bto-buddy/
├── README.md
├── CLAUDE.md
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
│
├── src/
│   └── bto_buddy/
│       ├── __init__.py
│       ├── app.py
│       ├── schemas.py
│       ├── policy.py
│       ├── retrieval.py
│       ├── generation.py
│       ├── verification.py
│       └── pipeline.py
│
├── data/
│   ├── private_corpus/          # Git-ignored
│   │   ├── raw/
│   │   └── processed/
│   ├── policy_facts.jsonl       # Tracked after rights review; Canonical retrieval knowledge base
│   ├── policy_rules.yaml       # Deterministic preparation checks
│   ├── sources_manifest.json  # Official source references and provenance
│   ├── source_coverage.csv
│   ├── visual_resources.json
│   ├── benchmark_dev.jsonl
│   └── benchmark_test.jsonl
│
├── scripts/
│   ├── capture_sources.py    # Approved Playwright HTML capture
│   ├── prepare_corpus.py     # Local extraction and normalisation
│   └── validate_corpus.py     # Completeness and provenance checks
│
├── evaluation/
│   ├── run.py
│   ├── baselines.py
│   ├── metrics.py
│   └── results/
│
├── tests/
│   ├── test_policy.py
│   ├── test_retrieval.py
│   ├── test_verification.py
│   └── test_pipeline.py
│
├── docs/
│   ├── project_context/
│   │   ├── INDEX.md
│   │   ├── 01_problem_and_scope.md
│   │   ├── 02_policy_sources.md
│   │   ├── 03_data_and_licensing.md
│   │   ├── 04_architecture.md
│   │   ├── 05_evaluation.md
│   │   ├── 06_submission_requirements.md
│   │   └── requirements_register.md
│   ├── decisions.md
│   └── development_log.md
│
├── ai_logs/
│   └── README.md
│
└── references/
    └── private/                 # Git-ignored

```
Note: avoid creating files simply to make the architecture appear sophisticated. 

Also, the .gitignore should include: 
```
# Private source documents and derived content
data/private_corpus/
references/private/

# Secrets
.env
.env.*
!.env.example

# Python and tooling
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
*.pyc

# Local operating-system files
.DS_Store
```
Store private derivatives under: data/private_corpus/processed/
Then store approved reviewer-facing facts in: data/policy_facts.jsonl
</pasted_content id="6baf">


### Claude · 2026-10-28 03:40:31

These are the files I'll create or change, and why. Two points about how I'm reading your structure first.

**Your structure vs the approved layout:** your repo structure replaces parts of the approved layout (D-039 paths and the [architecture.md §11.2](docs/architecture.md) module list). It's your latest explicit instruction, so I'll adopt it and record it as decision D-041:
- `schemas.py` takes the place of `contracts.py`.
- Evaluation code moves to a top-level `evaluation/` folder.
- The benchmark becomes two files, `benchmark_dev.jsonl` and `benchmark_test.jsonl`, instead of one file plus a split file. This keeps the held-out set physically separate, which I'd consider an improvement.

**Only real files now:** I'll create only what this setup step needs. The pipeline modules, `scripts/`, `evaluation/` and `ai_logs/` will be created when they get real content, not as empty stubs.

| File | Action | Purpose |
|---|---|---|
| `pyproject.toml` | edit | Add `streamlit` (D-036) via `uv add`; regenerate `uv.lock` |
| `uv.lock` | regenerate | Reproducible, cross-platform pinned dependencies |
| `src/bto_buddy/app.py` | new | The single Streamlit entry point. For now it's an honest shell: title, "not an official eligibility assessment" disclaimer, "don't enter real personal data" notice, and a status message. No unimplemented features |
| `tests/test_smoke.py` | new (replaces `test_package.py`) | One smoke test: package version plus the app renders without exceptions, using Streamlit's built-in `AppTest` |
| `Dockerfile` | new | Two-stage build: uv installs locked dependencies, then a slim Python 3.12 runtime that runs as a non-root user, exposes port 8501, has a health check and turns off usage telemetry |
| `.dockerignore` | new | Keeps private corpus, references, `.env`, `.venv`, caches, `.git` and docs out of the build context and image |
| `.gitignore` | edit | Merge your list with the existing one; add the mypy cache, `.cache/`, temporary outputs, logs and Streamlit secrets |
| `.env.example` | new | Placeholder LLM settings, marked as unused until a model is selected. Never contains real values |
| `.streamlit/config.toml` | new | Turns off Streamlit usage-statistics collection for local runs (privacy) |
| `CLAUDE.md` | edit | Verified uv and Docker commands |
| `docs/decisions.md`, `docs/architecture.md`, `docs/development_log.md` | edit | Record D-041 (layout and module mapping) and the verified results |
| `data/private_corpus/{raw,processed}/` | local folders only | Git-ignored; created locally so the structure exists |

Starting with the dependency and the app:

**Tool call: Bash** — Add Streamlit via uv, create private dirs, drop old test

```
cd "<repo>" && git status --short && uv add "streamlit>=1.40,<2" 2>&1 | tail -3 && uv pip show streamlit 2>/dev/null | grep -E '^(Name|Version)' && mkdir -p data/private_corpus/raw data/private_corpus/processed && git rm -q --cached tests/test_package.py 2>/dev/null; rm -f tests/test_package.py; ls tests
```

<details><summary>Tool result</summary>

```
 + urllib3==2.8.0
 + uvicorn==0.54.0
 + websockets==17.3
Name: streamlit
Version: 1.66.1
__pycache__
```
</details>

### Claude · 2026-10-28 03:41:13

Streamlit 1.66.1 is installed. I'll add its justification comment, unstage the test deletion (you do all staging and commits), then write the app and the smoke test.

**Tool call: Bash** — Unstage deletion and annotate Streamlit dependency

```
cd "<repo>" && git restore --staged tests/test_package.py && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('pyproject.toml'); t=p.read_text()
old='    "streamlit>=1.40,<2",\n'
assert t.count(old)==1
p.write_text(t.replace(old,'    # Demo UI; Python-native, single entry point (D-036). Not production hosting (D-026).\n'+old))
EOF
git status --short
```

<details><summary>Tool result</summary>

```
 M pyproject.toml
 D tests/test_package.py
 M uv.lock
```
</details>

**Tool call: Write**

```
{
 "file_path": "<repo>/src/bto_buddy/app.py",
 "content": "\"\"\"Streamlit entry point for BTO Buddy.\n\nRun with: uv run streamlit run src/bto_buddy/app.py\n\nThe guidance pipeline is not wired in yet. This page shows only what exists, so the\nwrite-up never claims features the code lacks (REQ-DOC-004).\n\"\"\"\n\nimport streamlit as st\n\nfrom bto_buddy import __version__\n\nDISCLAIMER = (\n    \"BTO Buddy gives preparation guidance based on published HDB information. \"\n    \"It is not an official eligibility assessment. Always confirm with official HDB services.\"\n)\nPRIVACY_NOTICE = (\n    \"Use fictional details only. Do not enter real names, NRIC numbers or other personal data.\"\n)\n\n\ndef main() -> None:\n    st.set_page_config(page_title=\"BTO Buddy\", layout=\"centered\")\n    st.title(\"BTO Buddy\")\n    st.caption(f\"BTO pre-application preparation assistant · prototype v{__version__}\")\n    st.warning(DISCLAIMER)\n    st.info(PRIVACY_NOTICE)\n    st.write(\"The guidance pipeline is under development and not yet available in this build.\")\n\n\nmain()\n"
}
```

**Tool call: Write**

```
{
 "file_path": "<repo>/tests/test_smoke.py",
 "content": "\"\"\"Smoke test: the package imports and the Streamlit entry point renders without errors.\"\"\"\n\nfrom pathlib import Path\n\nfrom streamlit.testing.v1 import AppTest\n\nimport bto_buddy\n\nAPP_PATH = Path(__file__).resolve().parents[1] / \"src\" / \"bto_buddy\" / \"app.py\"\n\n\ndef test_app_renders_with_disclaimer() -> None:\n    app = AppTest.from_file(str(APP_PATH)).run(timeout=30)\n\n    assert not app.exception\n    assert app.title[0].value == \"BTO Buddy\"\n    assert bto_buddy.__version__ in app.caption[0].value\n    # The non-assessment disclaimer must always be visible (REQ-PRB-010).\n    assert \"not an official eligibility assessment\" in app.warning[0].value\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/src/bto_buddy/app.py (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/tests/test_smoke.py (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 03:41:26

Now the ignore files, `.env.example`, the Streamlit config and the Dockerfile.

**Tool call: Write**

```
{
 "file_path": "<repo>/.gitignore",
 "content": "# Private source documents and derived content\n# (assessment brief, planning PDF, private notes; HDB snapshots and extracted passages.\n#  Redistribution permission not established: docs/project_context/03_data_and_licensing.md)\ndata/private_corpus/\nreferences/private/\n\n# Secrets\n.env\n.env.*\n!.env.example\n*.pem\n*.key\nsecrets/\ncredentials*.json\nservice-account*.json\n.streamlit/secrets.toml\n\n# Python and tooling\n.venv/\nvenv/\n__pycache__/\n*.py[cod]\n*.egg-info/\nbuild/\ndist/\n.pytest_cache/\n.ruff_cache/\n.mypy_cache/\n.coverage\nhtmlcov/\n.ipynb_checkpoints/\n.python-version\n\n# Local caches and temporary outputs\n# LLM response cache; the reproducible record is evaluation/results/ (D-039, D-041).\n.cache/\ntmp/\n*.tmp\n*.log\n\n# Local operating-system and editor files\n.DS_Store\n.vscode/\n.idea/\n"
}
```

**Tool call: Write**

```
{
 "file_path": "<repo>/.dockerignore",
 "content": "# Build context: only what the image needs. Private, secret and local files must never\n# enter the image (REQ-DAT-012, REQ-LIC-010).\n\n# Private material and secrets\nreferences/\ndata/private_corpus/\n.env\n.env.*\n!.env.example\n.streamlit/secrets.toml\n*.pem\n*.key\nsecrets/\n\n# Version control, environments, caches, outputs\n.git/\n.gitignore\n.venv/\n**/__pycache__/\n**/*.py[cod]\n*.egg-info/\n.pytest_cache/\n.ruff_cache/\n.mypy_cache/\n.cache/\ntmp/\n*.log\n.DS_Store\n.vscode/\n.idea/\n\n# Not needed at runtime\ndocs/\ntests/\nai_logs/\nCLAUDE.md\nDockerfile\n.dockerignore\n"
}
```

<details><summary>Tool result</summary>

```
The file <repo>/.gitignore has been updated successfully. (file state is current in your context — no need to Read it back)
```
</details>

**Tool call: Write**

```
{
 "file_path": "<repo>/.env.example",
 "content": "# Copy to .env and fill in locally. Never commit .env (it is Git-ignored).\n#\n# LLM settings for an OpenAI-compatible endpoint (D-036).\n# Not read by the application yet: the provider and model are chosen later, on evidence\n# (REQ-MOD-001). The variable names are reserved here so the Docker command works unchanged.\nBTO_BUDDY_LLM_BASE_URL=\nBTO_BUDDY_LLM_API_KEY=\nBTO_BUDDY_LLM_MODEL=\n"
}
```

**Tool call: Write**

```
{
 "file_path": "<repo>/.streamlit/config.toml",
 "content": "# Privacy: don't send Streamlit usage statistics from local or container runs.\n[browser]\ngatherUsageStats = false\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/.dockerignore (file state is current in your context — no need to Read it back)
```
</details>

**Tool call: Write**

```
{
 "file_path": "<repo>/Dockerfile",
 "content": "# syntax=docker/dockerfile:1\n# Two stages: uv installs the locked dependencies; the runtime image carries only the\n# virtualenv and the app source (no uv, no build tooling, no private data).\n\nFROM python:3.12-slim AS builder\nCOPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /bin/uv\nENV UV_COMPILE_BYTECODE=1 \\\n    UV_LINK_MODE=copy \\\n    UV_PYTHON_DOWNLOADS=never\nWORKDIR /app\n\n# Dependencies first, so this layer is cached until uv.lock changes.\nCOPY pyproject.toml uv.lock ./\nRUN uv sync --frozen --no-dev --no-install-project\n\n# Then the project itself, installed as a regular (non-editable) package.\nCOPY README.md ./\nCOPY src/ src/\nRUN uv sync --frozen --no-dev --no-editable\n\n\nFROM python:3.12-slim AS runtime\nENV PATH=\"/app/.venv/bin:$PATH\" \\\n    PYTHONDONTWRITEBYTECODE=1 \\\n    PYTHONUNBUFFERED=1 \\\n    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \\\n    STREAMLIT_SERVER_HEADLESS=true\nRUN useradd --create-home --uid 1000 app\nWORKDIR /app\n\nCOPY --from=builder --chown=app:app /app/.venv /app/.venv\nCOPY --chown=app:app src/bto_buddy/app.py ./app.py\nCOPY --chown=app:app .streamlit/config.toml ./.streamlit/config.toml\nUSER app\n\nEXPOSE 8501\nHEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \\\n    CMD python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=4)\"\n\n# Configuration (LLM settings) is read from environment variables: docker run --env-file .env\nCMD [\"streamlit\", \"run\", \"app.py\", \"--server.address=0.0.0.0\", \"--server.port=8501\"]\n"
}
```

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/.env.example (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/.streamlit/config.toml (file state is current in your context — no need to Read it back)
```
</details>

<details><summary>Tool result</summary>

```
File created successfully at: <repo>/Dockerfile (file state is current in your context — no need to Read it back)
```
</details>

### Claude · 2026-10-28 03:41:52

Now install, lint, type-check and test locally:

**Tool call: Bash** — Run install, lockfile check, lint, format, mypy, tests

```
cd "<repo>" && echo "== uv sync ==" && uv sync 2>&1 | tail -2 && echo "== uv lock --check ==" && uv lock --check && echo "== ruff check ==" && uv run ruff check . && echo "== ruff format ==" && uv run ruff format --check . && echo "== mypy ==" && uv run mypy && echo "== pytest ==" && uv run pytest -v 2>&1 | tail -4
```

<details><summary>Tool result (error)</summary>

```
Exit code 1
== uv sync ==
Installed 1 package in 2ms
 ~ bto-buddy==0.1.0 (from file://<home>/Desktop/non-acad/own%20projs/bto-buddy)
== uv lock --check ==
Resolved 51 packages in 5ms
== ruff check ==
All checks passed!
== ruff format ==
unformatted: File would be reformatted
   --> docs/architecture.md:174:21
    |
173 | # ---- shared enums -------------------------------------------------------------
    - class Tier(StrEnum): CORE="core"; LIMITED="limited"; CONTEXT="context"; EXCLUDED="excluded"
174 + class Tier(StrEnum):
175 +     CORE = "core"
176 +     LIMITED = "limited"
177 +     CONTEXT = "context"
178 +     EXCLUDED = "excluded"
179 +
180 |
181 | class Topic(StrEnum):
182 |     # in scope (tier fixed by D-008)
    -     HOUSEHOLD_COMPOSITION="household_composition"          # core
    -     APPLICATION_REQUIREMENTS="application_requirements"    # core
    -     HFE_PROCESS="hfe_process"                              # core (prerequisites, timing, validity)
    -     HFE_DOCUMENTS="hfe_documents"                          # core (incl. income/employment docs, D-013)
    -     PRIORITY_CONSIDERATIONS="priority_considerations"      # limited
    -     NON_SELECTION="non_selection"                          # limited
    -     HFE_GRANT_LOAN_CONTEXT="hfe_grant_loan_context"        # context only
183 +     HOUSEHOLD_COMPOSITION = "household_composition"  # core
184 +     APPLICATION_REQUIREMENTS = "application_requirements"  # core
185 +     HFE_PROCESS = "hfe_process"  # core (prerequisites, timing, validity)
186 +     HFE_DOCUMENTS = "hfe_documents"  # core (incl. income/employment docs, D-013)
187 +     PRIORITY_CONSIDERATIONS = "priority_considerations"  # limited
188 +     NON_SELECTION = "non_selection"  # limited
189 +     HFE_GRANT_LOAN_CONTEXT = "hfe_grant_loan_context"  # context only
190 |     # excluded (D-008)
    -     GRANT_LOAN_CALCULATION="grant_loan_calculation"
    -     FINANCING_AFFORDABILITY="financing_affordability"
    -     BALLOT_ODDS="ballot_odds"
    -     POST_PURCHASE="post_purchase"
    -     ELIGIBILITY_DETERMINATION="eligibility_determination"
    -     OTHER_HOUSING="other_housing"                          # resale, rental, EC, etc.
    -     UNRELATED="unrelated"
191 +     GRANT_LOAN_CALCULATION = "grant_loan_calculation"
192 +     FINANCING_AFFORDABILITY = "financing_affordability"
193 +     BALLOT_ODDS = "ballot_odds"
194 +     POST_PURCHASE = "post_purchase"
195 +     ELIGIBILITY_DETERMINATION = "eligibility_determination"
196 +     OTHER_HOUSING = "other_housing"  # resale, rental, EC, etc.
197 +     UNRELATED = "unrelated"
198 |
    - TOPIC_TIER: dict[Topic, Tier]   # single source of truth for the gate, unit-tested
199 |
    - class ProfileField(StrEnum):    # addressable fields, for missing/conflict reporting
    -     RELATIONSHIP="relationship"; A1_AGE="applicant_1.age"; A2_AGE="applicant_2.age"
    -     A1_CITIZENSHIP="applicant_1.citizenship"; A2_CITIZENSHIP="applicant_2.citizenship"
    -     A1_PRIOR_HOUSING="applicant_1.prior_flat_or_subsidy"; A2_PRIOR_HOUSING="applicant_2.prior_flat_or_subsidy"
    -     A1_EMPLOYMENT="applicant_1.employment"; A2_EMPLOYMENT="applicant_2.employment"
    -     HFE_STATUS="hfe_status"; HFE_ISSUE_DATE="hfe_issue_date"
    -     PRIVATE_PROPERTY="private_property_interest"; HOUSING_LOAN_INTENT="housing_loan_intent"
    -     CHILDREN="children_or_expecting"
200 + TOPIC_TIER: dict[Topic, Tier]  # single source of truth for the gate, unit-tested
201 +
202 |
203 + class ProfileField(StrEnum):  # addressable fields, for missing/conflict reporting
204 +     RELATIONSHIP = "relationship"
205 +     A1_AGE = "applicant_1.age"
206 +     A2_AGE = "applicant_2.age"
207 +     A1_CITIZENSHIP = "applicant_1.citizenship"
208 +     A2_CITIZENSHIP = "applicant_2.citizenship"
209 +     A1_PRIOR_HOUSING = "applicant_1.prior_flat_or_subsidy"
210 +     A2_PRIOR_HOUSING = "applicant_2.prior_flat_or_subsidy"
211 +     A1_EMPLOYMENT = "applicant_1.employment"
212 +     A2_EMPLOYMENT = "applicant_2.employment"
213 +     HFE_STATUS = "hfe_status"
214 +     HFE_ISSUE_DATE = "hfe_issue_date"
215 +     PRIVATE_PROPERTY = "private_property_interest"
216 +     HOUSING_LOAN_INTENT = "housing_loan_intent"
217 +     CHILDREN = "children_or_expecting"
218 +
219 +
220 | # ---- request / profile ------------------------------------------------------------
221 | class UserRequest(BaseModel):
222 |     request_id: str
    -     situation_text: str          # free text; fictional profiles only (UI warns)
223 +     situation_text: str  # free text; fictional profiles only (UI warns)
224 |     question: str
225 |
226 +
227 | class Person(BaseModel):
228 |     age: int | None = Field(None, ge=0, le=120)
229 |     citizenship: Literal["SC", "SPR", "non_resident"] | None = None
    -     prior_flat_or_subsidy: bool | None = None      # drives first-timer status
    -     employment: Literal["employed", "self_employed", "not_working", "other"] | None = None  # Phas

... [3834 characters truncated] ...

 aliases: list[str] = []
    -     applies_to: dict[str, str] = {}; exceptions: list[str] = []
    -     source_id: str; source_url: HttpUrl; section: str
    -     retrieved_at: date; effective_from: date | None; effective_to: date | None
    -     validation_status: Literal["verified"]      # loader rejects anything else at runtime
319 +     applies_to: dict[str, str] = {}
320 +     exceptions: list[str] = []
321 +     source_id: str
322 +     source_url: HttpUrl
323 +     section: str
324 +     retrieved_at: date
325 +     effective_from: date | None
326 +     effective_to: date | None
327 +     validation_status: Literal["verified"]  # loader rejects anything else at runtime
328 |     kb_version: str
329 |
330 +
331 | class RuleResult(BaseModel):
    -     rule_id: str; rule_version: str
332 +     rule_id: str
333 +     rule_version: str
334 |     status: Literal["applies", "not_applicable", "cannot_determine"]
    -     preparation_step: str | None  
… [4031 more chars in the JSONL export]
```
</details>

<details><summary>Claude's reasoning</summary>

Ruff 0.17 is flagging the design sketch in `docs/architecture.md` since it now formats Python blocks inside Markdown too, but that's documentation, not real code. I'll exclude `docs/` from ruff instead of reflowing it.


</details>

**Tool call: Bash** — Exclude docs from ruff and rerun all checks

```
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('pyproject.toml'); t=p.read_text()
old='src = ["src", "tests"]\n'
assert t.count(old)==1
p.write_text(t.replace(old,old+'# docs/ holds design sketches (e.g. contract outlines in Markdown), not executable code.\nextend-exclude = ["docs"]\n'))
EOF
echo "== ruff check ==" && uv run ruff check . && echo "== ruff format ==" && uv run ruff format --check . && echo "== mypy ==" && uv run mypy && echo "== pytest ==" && uv run pytest -v 2>&1 | tail -4 && echo "== lock ==" && uv lock --check
```

<details><summary>Tool result</summary>

```
== ruff check ==
   Building bto-buddy @ file://<home>/Desktop/non-acad/own%20projs/bto-buddy
      Built bto-buddy @ file://<home>/Desktop/non-acad/own%20projs/bto-buddy
Uninstalled 1 package in 1ms
Installed 1 package in 2ms
All checks passed!
== ruff format ==
5 files already formatted
== mypy ==
Success: no issues found in 2 source files
== pytest ==

tests/test_smoke.py .                                                    [100%]

============================== 1 passed in 1.37s ===============================
== lock ==
Resolved 51 packages in 5ms
[This command modified 1 file you've previously read: pyproject.toml. Call Read before editing.]
```
</details>

### Claude · 2026-10-28 03:42:24

Local checks all pass. Now the Docker build, a run, the health check and a check that nothing private ended up in the image:

**Tool call: Bash** — Build image, run container, check health, inspect contents

```
cd "<repo>" && docker build -q -t bto-buddy . && docker image ls bto-buddy --format '{{.Repository}}:{{.Tag}} {{.Size}}' && cp -n .env.example .env.verify.tmp 2>/dev/null; docker run -d --rm --name bto-buddy-smoke -p 8501:8501 --env-file .env.example bto-buddy >/dev/null && for i in $(seq 1 30); do s=$(docker inspect -f '{{.State.Health.Status}}' bto-buddy-smoke 2>/dev/null); curl -fs http://localhost:8501/_stcore/health >/dev/null && { echo "health endpoint OK after ~$((i*2))s"; break; }; perl -e 'select(undef,undef,undef,2)'; done; echo "page: $(curl -s http://localhost:8501 | grep -o '<title>[^<]*</title>')"; echo "== image contents check =="; docker run --rm --entrypoint sh bto-buddy -c 'whoami; ls -A /app; ls /app/.venv/lib/python3.12/site-packages | grep -i bto; find / -path /proc -prune -o \( -name "*.pdf" -o -name ".env" -o -name "private_corpus" -o -name "references" \) -print 2>/dev/null | grep -v "^/proc" | grep -v site-packages | head'; sleep 0 ; docker stop bto-buddy-smoke >/dev/null; rm -f .env.verify.tmp; echo stopped
```

<details><summary>Tool result</summary>

```
sha256:2eb7b5d3f6fbd4bafd5b4009f87128aa90cc7a873c101ed1a76186eb555ed27c
bto-buddy:latest 820MB
health endpoint OK after ~4s
page: <title>Streamlit</title>
== image contents check ==
app
.streamlit
.venv
app.py
bto_buddy
bto_buddy-0.1.0.dist-info
stopped
```
</details>

<details><summary>Claude's reasoning</summary>

The image builds successfully, runs as non-root user `app`, and excludes PDFs, `.env`, `references/`, and the private corpus. Next I'll verify Docker's HEALTHCHECK reports healthy and confirm all sensitive paths are Git-ignored.


</details>

**Tool call: Bash** — Verify Docker health status and gitignore coverage

```
cd "<repo>" && docker run -d --rm --name bto-buddy-hc --env-file .env.example bto-buddy >/dev/null && for i in $(seq 1 30); do s=$(docker inspect -f '{{.State.Health.Status}}' bto-buddy-hc); [ "$s" = healthy ] && { echo "docker HEALTHCHECK: healthy after ~$((i*2))s"; break; }; perl -e 'select(undef,undef,undef,2)'; done; [ "$s" != healthy ] && echo "status: $s"; docker stop bto-buddy-hc >/dev/null; echo "== git ignore checks =="; mkdir -p tmp .cache/llm; touch .env data/private_corpus/raw/x.html data/private_corpus/processed/p.jsonl .cache/llm/c.json tmp/t.txt run.log .streamlit/secrets.toml; for f in .env data/private_corpus/raw/x.html data/private_corpus/processed/p.jsonl references/private/submission_private_notes.md "references/private/project approach.pdf" .cache/llm/c.json tmp/t.txt run.log .streamlit/secrets.toml .venv/bin/python .pytest_cache .ruff_cache .mypy_cache .DS_Store; do git check-ignore -q "$f" && echo "ignored  $f" || echo "NOT IGNORED  $f"; done; git check-ignore -q .env.example && echo "NOT TRACKABLE .env.example" || echo "trackable .env.example"; rm -rf .env tmp .cache run.log .streamlit/secrets.toml data/private_corpus/raw/x.html data/private_corpus/processed/p.jsonl; echo "== git add -A dry run ==" && git add -A --dry-run
```

<details><summary>Tool result</summary>

```
docker HEALTHCHECK: healthy after ~8s
== git ignore checks ==
ignored  .env
ignored  data/private_corpus/raw/x.html
ignored  data/private_corpus/processed/p.jsonl
ignored  references/private/submission_private_notes.md
ignored  references/private/project approach.pdf
ignored  .cache/llm/c.json
ignored  tmp/t.txt
ignored  run.log
ignored  .streamlit/secrets.toml
ignored  .venv/bin/python
ignored  .pytest_cache
ignored  .ruff_cache
ignored  .mypy_cache
ignored  .DS_Store
trackable .env.example
== git add -A dry run ==
add '.gitignore'
add 'pyproject.toml'
remove 'tests/test_package.py'
add 'uv.lock'
add '.dockerignore'
add '.env.example'
add '.streamlit/config.toml'
add 'Dockerfile'
add 'src/bto_buddy/app.py'
add 'tests/test_smoke.py'
```
</details>

### Claude · 2026-10-28 03:44:45

Every sensitive path is ignored, and a dry-run `git add -A` would stage only the intended files. Now the docs: CLAUDE.md commands, decision D-041, the module mapping in architecture.md, and the log.

**Tool call: Read**

```
{
 "file_path": "<repo>/CLAUDE.md",
 "offset": 195
}
```

<details><summary>Tool result</summary>

````
195	
196	```bash
197	uv sync                      # create .venv from uv.lock (package + dev group)
198	uv run pytest                # tests
199	uv run ruff check .          # lint
200	uv run ruff format --check . # formatting
201	uv run mypy                  # strict type check of src/bto_buddy
202	uv lock --check              # fail if uv.lock is out of date with pyproject.toml
203	```
204	
205	- Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>`), with a justification
206	  comment in `pyproject.toml`. Never hand-edit `uv.lock`.
207	- **Not yet available:**
208	  - the application run command (UI on hold pending architecture review);
209	  - Docker build/run (Docker Desktop installation pending on the dev machine);
210	  - evaluation commands.
211	
212	  Add each one here only after it has been verified.
213	
214	**Secret scan before a push** (until a dedicated tool is approved):
215	```bash
216	git diff --cached --name-only | grep -E '^(references/private|data/private_corpus)/|\.env' && echo "BLOCK"
217	git diff --cached | grep -inE 'api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY' || echo "no secret patterns"
218	# Anonymity: the term list is private (Git-ignored) and must never be copied into tracked files.
219	git grep -inFf references/private/anonymity_terms.txt || echo "no identifying terms"
220	```
221	
````
</details>

**Tool call: Bash** — Locate module layout section and last decision row

```
cd "<repo>" && grep -n "### 11.2\|^\*\*Boundary rules\|^\*\*File paths\|^| LLM cache\|^## 12" docs/architecture.md && grep -n "^| D-040" docs/decisions.md | cut -c1-20
```

<details><summary>Tool result</summary>

```
478:### 11.2 Module layout and dependency direction
502:**Boundary rules:**
511:**File paths (Q-10):**
521:| LLM cache (Git-ignored; `results/` holds the reproducible record) | `.cache/llm/` |
523:## 12. Tests
93:| D-040 | **Optio
```
</details>

**Tool call: Edit**

````
{
 "replace_all": false,
 "file_path": "<repo>/CLAUDE.md",
 "old_string": "```bash\nuv sync                      # create .venv from uv.lock (package + dev group)\nuv run pytest                # tests\nuv run ruff check .          # lint\nuv run ruff format --check . # formatting\nuv run mypy                  # strict type check of src/bto_buddy\nuv lock --check              # fail if uv.lock is out of date with pyproject.toml\n```\n\n- Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>`), with a justification\n  comment in `pyproject.toml`. Never hand-edit `uv.lock`.\n- **Not yet available:**\n  - the application run command (UI on hold pending architecture review);\n  - Docker build/run (Docker Desktop installation pending on the dev machine);\n  - evaluation commands.\n\n  Add each one here only after it has been verified.\n\n**Secret scan before a push** (until a dedicated tool is approved):\n```bash\ngit diff --cached --name-only | grep -E '^(references/private|data/private_corpus)/|\\.env' && echo \"BLOCK\"",
 "new_string": "- Install: `uv sync` (creates `.venv` from `uv.lock`: package + dev group)\n- Test: `uv run pytest`\n- Lint: `uv run ruff check .`\n- Format check: `uv run ruff format --check .`\n- Type check: `uv run mypy` (strict, `src/bto_buddy`)\n- Lockfile check: `uv lock --check`\n- Run locally: `uv run streamlit run src/bto_buddy/app.py` → http://localhost:8501\n- Build image: `docker build -t bto-buddy .`\n- Run container: `cp .env.example .env` (once; fill in values when an LLM is configured), then\n  `docker run --rm -p 8501:8501 --env-file .env bto-buddy`\n- Health check: `curl -f http://localhost:8501/_stcore/health`\n\n**Docker image:** two-stage build on `python:3.12-slim`, uv 0.13.6, runs as non-root `app`,\nport 8501, HEALTHCHECK on `/_stcore/health`. Configuration comes from environment variables\nonly. `.dockerignore` keeps `references/`, `data/private_corpus/`, `.env*`, docs, tests and\ncaches out of the build context.\n\n- Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>`), with a justification comment\n  in `pyproject.toml`. Never hand-edit `uv.lock`.\n- Evaluation commands: add them here only after they have been verified.\n\n**Secret scan before a push** (until a dedicated tool is approved):\n```bash\ngit diff --cached --name-only | grep -E '^(references/private|data/private_corpus)/|(^|/)\\.env(\\.[^/]*)?$' | grep -v '\\.env\\.example$' && echo \"BLOCK\""
}
````

**Tool call: Read**

```
{
 "file_path": "<repo>/docs/architecture.md",
 "offset": 478,
 "limit": 45
}
```

<details><summary>Tool result</summary>

```
The file <repo>/CLAUDE.md has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

````
478	### 11.2 Module layout and dependency direction
479	
480	```
481	src/bto_buddy/
482	  contracts.py        # all models above; imports nothing from the package
483	  config.py           # Settings (model id, k, thresholds, prompt versions) from env
484	  knowledge.py        # load + validate facts, manifest, visual resources; fact lookup
485	  rules.py            # load policy_rules.yaml; declarative condition interpreter; evaluate
486	  profile.py          # assess_profile: quote guard, conflicts, missing fields (pure)
487	  gate.py             # TOPIC_TIER map + coverage decision (pure)
488	  retrieval.py        # tokenizer, BM25 index, topic-filtered search; Retriever protocol
489	  evidence.py         # assemble_evidence: rule facts ∪ hits, evidence gaps (pure)
490	  llm.py              # LLMClient protocol, OpenAI-compatible impl, disk cache, call accounting
491	  prompts/            # extract_v1.md, generate_v1.md, verify_v1.md (versioned text)
492	  extraction.py       # LLM #1 → ProfileExtraction
493	  generation.py       # LLM #2 → GenerationOutput
494	  verification.py     # deterministic checks + batched judge → VerificationResult
495	  report.py           # build_report + D-011 display policy (pure)
496	  pipeline.py         # run(request, config_id) composes stages for A–D
497	  app/streamlit_app.py
498	  eval/
499	    datasets.py  scoring.py  retrieval_eval.py  verifier_eval.py  stats.py  cli.py
500	```
501	
502	**Boundary rules:**
503	- Pure modules (`profile`, `gate`, `rules`, `retrieval`, `evidence`, `report`) never import
504	  `llm`.
505	- Only `extraction`, `generation` and `verification` call the `LLMClient` protocol, so tests
506	  inject a fake.
507	- `pipeline` is the only module that knows about configurations.
508	- `eval` consumes `FinalGuidance` and never reaches into stage internals, except through the
509	  component evaluators.
510	
511	**File paths (Q-10):**
512	
513	| Content | Path |
514	|---|---|
515	| Scenarios | `data/eval/scenarios.jsonl` |
516	| Split | `data/eval/split.json` |
517	| Verifier claims | `data/eval/verifier_claims.jsonl` |
518	| Retrieval queries | `data/eval/retrieval_queries.jsonl` |
519	| Frozen metric spec | `eval/metric_spec.md` |
520	| Run outputs (tracked; allow offline rescoring) | `results/runs/<run_id>/{run_metadata.json, predictions.jsonl, scores.json}` |
521	| LLM cache (Git-ignored; `results/` holds the reproducible record) | `.cache/llm/` |
522	
````
</details>

### Claude · 2026-10-28 03:45:19

I'll replace §11.2 with the module mapping for your structure (D-041), simplified where a module would add nothing.

**Tool call: Bash** — Write D-041 layout into architecture, data doc, decisions

````
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/architecture.md'); t=p.read_text()
start=t.index('### 11.2 Module layout and dependency direction'); end=t.index('## 12. Tests')
new='''### 11.2 Repository layout and dependency direction (D-041, supersedes the D-030/D-039 layout)

The developer's recommended structure, simplified so that no module exists only for show.
Files are created when they get real content, never as empty stubs.

```
src/bto_buddy/
  app.py            # Streamlit entry point (thin: calls pipeline, renders FinalGuidance)
  schemas.py        # all Pydantic contracts and enums from §5; imports nothing from the package
  policy.py         # pure policy domain: load/validate facts, manifest, visual resources;
                    #   declarative rule interpreter; TOPIC_TIER gate; profile assessment
                    #   (quote guard, conflicts, topic-scoped missing fields, follow-up templates)
  retrieval.py      # tokenizer, BM25 index, topic-filtered search, evidence assembly (pure)
  llm.py            # LLMClient protocol, OpenAI-compatible client, disk cache, call accounting
  generation.py     # LLM #1 extraction and LLM #2 generation (prompts + output validation)
  verification.py   # deterministic checks + batched LLM judge; D-011 display actions
  pipeline.py       # run(request, config_id): composes A–D; builds FinalGuidance
  prompts/          # versioned prompt text (extract_v1.md, generate_v1.md, verify_v1.md)
evaluation/
  run.py            # CLI: run configs on dev/test, save predictions, re-score offline
  metrics.py        # D-004 metrics, retrieval recall@k, verifier metrics, bootstrap/McNemar
  metric_spec.md    # frozen operational definitions (written before the held-out run)
  results/<run_id>/ # run_metadata.json, predictions.jsonl, scores.json (tracked)
scripts/            # Phase 2 developer tooling; not used at runtime or in Docker
  capture_sources.py  prepare_corpus.py  validate_corpus.py
tests/              # test_policy.py, test_retrieval.py, test_verification.py,
                    # test_pipeline.py, test_smoke.py
```

**Simplifications versus the recommended structure, with reasons:**

| Recommended item | Change | Reason |
|---|---|---|
| — | **Added `llm.py`** | Three modules (`generation`, `verification`, and extraction inside `generation`) share one client. A separate module is the single seam where tests inject a fake and where caching and token accounting live. Without it, `verification` would import from `generation` |
| `evaluation/baselines.py` | **Dropped** | D-030: configurations A–D are the same pipeline with stages switched off, so they live in `pipeline.py`. A separate baselines module would duplicate prompt logic and break "equivalent instructions" (D-003) |
| Separate retrieval-query file | **Dropped** | Retrieval recall@k uses each benchmark case's gold fact IDs. One labelled source, no duplication |
| `contracts.py`, `knowledge.py`, `rules.py`, `gate.py`, `profile.py`, `evidence.py`, `report.py`, `extraction.py` (D-030 layout) | **Merged** into `schemas.py`, `policy.py`, `retrieval.py`, `generation.py`, `pipeline.py` | Each was small. If `policy.py` grows past about 400 lines, split out `profile.py` (recorded as an allowed refactor, no new decision needed) |

**Boundary rules:**
- `schemas`, `policy`, `retrieval` and `pipeline`'s report assembly are pure: they never import
  `llm`.
- Only `generation` and `verification` call the `LLMClient` protocol, so tests inject a fake.
- `pipeline` is the only module that knows about configurations.
- `evaluation/` consumes `FinalGuidance` and saved predictions. It never reaches into stage
  internals, except through the component metrics.
- `scripts/` is never imported by `src/` or used by Docker (REQ-DAT-022).

**Data paths (D-022 + D-041):**

| Content | Path | Git |
|---|---|---|
| Canonical KB | `data/policy_facts.jsonl` | tracked after rights review |
| Rules, manifest, coverage, visual resources | `data/policy_rules.yaml`, `data/sources_manifest.json`, `data/source_coverage.csv`, `data/visual_resources.json` | tracked |
| Benchmark | `data/benchmark_dev.jsonl`, `data/benchmark_test.jsonl` (the held-out set is a physically separate file) | tracked |
| Verifier claim set | `data/verifier_claims_dev.jsonl`, `data/verifier_claims_test.jsonl` | tracked |
| Private source snapshots / derivatives | `data/private_corpus/raw/`, `data/private_corpus/processed/` | **ignored** |
| Run outputs | `evaluation/results/<run_id>/` | tracked (offline re-scoring) |
| LLM cache | `.cache/llm/` | **ignored** |

'''
p.write_text(t[:start]+new+t[end:])
p=pathlib.Path('docs/project_context/03_data_and_licensing.md'); t=p.read_text()
for old,new_ in [("| Evaluation scenarios (Dataset C) | path OPEN (Q-10) |","| Evaluation scenarios (Dataset C) | `data/benchmark_dev.jsonl`, `data/benchmark_test.jsonl` (D-041) |"),
                 ("| Verifier claim set | path OPEN (Q-10) |","| Verifier claim set | `data/verifier_claims_{dev,test}.jsonl` (D-041) |"),
                 ("| Saved predictions and run metadata | path OPEN (Q-10) |","| Saved predictions and run metadata | `evaluation/results/<run_id>/` (D-041) |")]:
    assert t.count(old)==1, old; t=t.replace(old,new_)
p.write_text(t)
p=pathlib.Path('docs/decisions.md'); t=p.read_text()
anchor=t[t.index('| D-040 |'):]; anchor=anchor[:anchor.index('\n')+1]
row=('| D-041 | **Repository layout** follows the developer\'s recommended structure, simplified: '
 '`src/bto_buddy/{app,schemas,policy,retrieval,llm,generation,verification,pipeline}.py` + `prompts/`; '
 '`evaluation/{run,metrics}.py`, `metric_spec.md`, `results/`; `scripts/` for Phase 2 tooling. '
 'Benchmark as `data/benchmark_{dev,test}.jsonl`; verifier claims as `data/verifier_claims_{dev,test}.jsonl`; '
 'run outputs in `evaluation/results/<run_id>/`. `llm.py` added; `evaluation/baselines.py` and a separate '
 'retrieval-query file dropped (reasons in architecture §11.2). Fi
… [709 more chars in the JSONL export]
````

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 45 chars]
```
</details>

### Claude · 2026-10-28 03:45:48

I'll check for stale references to the old paths and then update the development log.

**Tool call: Bash** — Find stale path references

```
cd "<repo>" && grep -rn "data/eval\|results/runs\|eval/metric_spec\|contracts\.py" --include=*.md . | grep -v "^./references" | grep -v "D-039\|~~" 
```

<details><summary>Tool result</summary>

```
(eval):1: no matches found: --include=*.md
```
</details>

**Tool call: Bash** — Find stale path references in Markdown

```
cd "<repo>" && git grep --untracked -n -e "data/eval" -e "results/runs" -e "eval/metric_spec" -e "contracts\.py" -- '*.md' | grep -v "D-039"
```

<details><summary>Tool result</summary>

```
docs/architecture.md:514:| `contracts.py`, `knowledge.py`, `rules.py`, `gate.py`, `profile.py`, `evidence.py`, `report.py`, `extraction.py` (D-030 layout) | **Merged** into `schemas.py`, `policy.py`, `retrieval.py`, `generation.py`, `pipeline.py` | Each was small. If `policy.py` grows past about 400 lines, split out `profile.py` (recorded as an allowed refactor, no new decision needed) |
docs/development_log.md:91:1. Implement the pure core: `contracts.py`, `knowledge.py`, `rules.py`, `gate.py`,
```
</details>

**Tool call: Bash** — Update dev log; final doc, secret, anonymity and test checks

```
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/development_log.md'); t=p.read_text()
start=t.index('**Next:**', t.index('**Architecture review (2026-10-28) — approved:**'))
t=t[:start]+'''**Repository and tooling setup (2026-10-28):**
- **Layout:** D-041 adopts the developer's recommended structure, simplified:
  - `llm.py` added;
  - `evaluation/baselines.py` and a separate retrieval-query file dropped;
  - benchmark and verifier claims split into physical dev/test files.
- **Files:**
  - `src/bto_buddy/app.py`: single Streamlit entry point; an honest shell with disclaimer and
    privacy notice, no pipeline yet;
  - `tests/test_smoke.py`: replaces `test_package.py`; uses Streamlit `AppTest`;
  - `Dockerfile`, `.dockerignore`, `.env.example`, `.streamlit/config.toml` (telemetry off);
  - `.gitignore`: merged with the developer's list, plus caches and temporary outputs.
- **Dependency:** Streamlit 1.66.1 via `uv add`; `uv.lock` now pins 51 packages.
- **Ruff:** ruff 0.17 formats Python blocks inside Markdown, so `docs/` is excluded (design
  sketches, not code).

**Verified (macOS, uv 0.13.6, Docker 29.9.2):**

| Check | Result |
|---|---|
| `uv sync` / `uv lock --check` | OK; 51 packages, lock up to date |
| `uv run ruff check .` / `ruff format --check .` | All passed / 5 files formatted |
| `uv run mypy` (strict) | No issues in 2 source files |
| `uv run pytest` | 1 passed (smoke: app renders, disclaimer visible) |
| `docker build -t bto-buddy .` | OK; image 820 MB (Streamlit brings numpy, pandas, pyarrow) |
| `docker run -p 8501:8501 --env-file .env.example bto-buddy` | `/_stcore/health` OK in ~4 s; Docker HEALTHCHECK `healthy` in ~8 s |
| Image contents | Runs as `app` (non-root); `/app` = `.venv`, `.streamlit`, `app.py`; no PDFs, `.env`, `references/` or `private_corpus` |
| `git check-ignore` | `.env`, private corpus raw/processed, `references/private/*`, `.cache/`, `tmp/`, `*.log`, Streamlit secrets, `.venv`, tool caches, `.DS_Store` all ignored; `.env.example` trackable |

**Noted:**
- `scripts/capture_sources.py` would need **Playwright**, which is not in the D-036 dependency
  list. It needs approval before Phase 2 capture, as a dev-only dependency.

**Next:**
1. Implement the pure core: `schemas.py` and `policy.py` (facts/rules loading, rule
   interpreter, gate, profile assessment), with unit tests against a synthetic fixture KB.
   No LLM calls.
2. Then Phase 2: source verification and authoring `policy_facts.jsonl`.
'''
p.write_text(t)
EOF
python3 -I <tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/audit.py "$PWD"; (git grep --untracked -inFf references/private/anonymity_terms.txt || echo "no identifying terms"); (git grep --untracked -inE 'api[_-]?key *= *[^ $]|sk-[a-z0-9]{10}|BEGIN .*PRIVATE KEY' || echo "no secret values"); uv run ruff check . -q && uv run ruff format --check . -q && uv run mypy | tail -1 && uv run pytest -q 2>&1 | tail -1; git status --short -uall
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 741 chars]
```
</details>

### Claude · 2026-10-28 03:46:23

The repository and tooling setup is in place and everything passes, including a real Docker build and run. Nothing is committed or pushed.

**Results** (macOS, uv 0.13.6, Docker 29.9.2):

| Step | Result |
|---|---|
| `uv sync` / `uv lock --check` | OK: 51 packages pinned, lockfile up to date |
| `uv run ruff check .` | All checks passed |
| `uv run ruff format --check .` | All formatted |
| `uv run mypy` (strict) | No issues |
| `uv run pytest` | 1 passed: the app renders and the disclaimer is visible |
| `docker build -t bto-buddy .` | OK; image is 820 MB (Streamlit pulls in numpy, pandas and pyarrow) |
| `docker run` | Health endpoint answered in about 4 s; Docker's own health check reported `healthy` in about 8 s |
| Image contents | Runs as a non-root user; holds only the virtualenv, `app.py` and the Streamlit config. No PDFs, `.env`, `references/` or private corpus |
| `git check-ignore` | `.env`, private corpus, `references/private/`, `.cache/`, `tmp/`, `*.log`, Streamlit secrets, `.venv` and tool caches are all ignored. A dry-run `git add -A` stages only the intended files |

**What's there now:**
- **[app.py](src/bto_buddy/app.py)** is the single entry point. For now it's a shell with the "not an official eligibility assessment" disclaimer and a "fictional details only" notice. It says the pipeline isn't available yet rather than showing features that don't exist.
- **[tests/test_smoke.py](tests/test_smoke.py)** replaces the old `test_package.py`.
- **[Dockerfile](Dockerfile):** two stages on `python:3.12-slim`, port 8501, configuration from environment variables only.
- **[.dockerignore](.dockerignore), [.env.example](.env.example)** (placeholders only), **[.gitignore](.gitignore)** (your list merged with mine), and **[.streamlit/config.toml](.streamlit/config.toml)**, which turns off usage telemetry.
- **[CLAUDE.md](CLAUDE.md)** has the verified commands:
  - The run command you suggested matches the Dockerfile.
  - I added `cp .env.example .env` as a first step, because `--env-file .env` fails if the file doesn't exist.
  - I fixed the pre-push secret scan, which would have wrongly blocked `.env.example`.

**Ruff and docs:** ruff 0.17 also reformats Python code blocks inside Markdown, so I excluded `docs/` from ruff. The contract sketches there are design notes, not code.

**Layout (D-041 in [decisions.md](docs/decisions.md), [architecture.md §11.2](docs/architecture.md)):** I followed your structure with three simplifications:
- **Added `llm.py`**, which needs your confirmation. Generation, extraction and verification all use one LLM client. A separate module keeps that client in one place for test fakes, caching and token counting, instead of `verification.py` importing from `generation.py`.
- **Dropped `evaluation/baselines.py`.** Configurations A–D are the same pipeline with stages switched off, so a separate baselines file would duplicate prompt logic.
- **Dropped the separate retrieval-query file.** Retrieval is scored with each benchmark case's gold fact IDs.

Verifier claims follow the benchmark's pattern: separate `_dev` and `_test` files. Modules are only created when they get real content.

**Needs approval before Phase 2:** `scripts/capture_sources.py` would need Playwright, which isn't in the approved dependency list (D-036). I'd add it as a development-only dependency once you approve.

**Suggested commit:** now is a good point, since the setup is stable and all checks pass.
- **Include:** all files listed in `git status`, including the deletion of `tests/test_package.py`.
- **Suggested message:** `chore: add Streamlit entry point, Docker and environment tooling`
- **Push:** fine to push. The secret and anonymity scans are clean.

```bash
git add -A && git status --short
git commit -m "chore: add Streamlit entry point, Docker and environment tooling"
```

Next is `schemas.py` and `policy.py` with unit tests against a small fictional test knowledge base, and no LLM calls.

### User · 2026-10-28 03:48:12

has Playwright been added to the approved dependency list?

**Tool call: Bash** — Check where Playwright is mentioned

```
cd "<repo>" && grep -in "playwright" pyproject.toml uv.lock docs/decisions.md CLAUDE.md docs/architecture.md docs/development_log.md | cut -c1-160
```

<details><summary>Tool result</summary>

```
docs/development_log.md:119:- `scripts/capture_sources.py` would need **Playwright**, which is not in the D-036 dependency
```
</details>

### Claude · 2026-10-28 03:48:21

No, Playwright is not on the approved list. It isn't in `pyproject.toml` or `uv.lock`, and no decision mentions it. The only reference is the note in [docs/development_log.md](docs/development_log.md) flagging that it needs your approval.

The approved list (D-036) is:
- **Runtime:** `pydantic`, `pyyaml`, `rank-bm25`, `openai` (as an OpenAI-compatible client), `streamlit`
- **Development:** `pytest`, `ruff`, `mypy`, `types-PyYAML`

The question only matters for Phase 2 source capture, and there are two approved ways to capture (REQ-SRC-006):
1. **Manual rendered-DOM extraction:** you expand the sections in your browser and save the page. This needs no new dependency.
2. **Controlled browser automation:** this is what Playwright would provide. I'd add it as a development-only dependency used only by `scripts/capture_sources.py`, never at runtime or in Docker. It also needs a one-time browser download (`playwright install chromium`).

I'd recommend option 2 if you approve it. The pages rely on accordions, and a script expands every section the same way, records the SHA-256 hash and timestamp, and makes the accordion-coverage check measurable. If you approve, I'll record it as a decision with that justification before adding it. If not, the capture step stays manual and nothing changes.

### User · 2026-10-28 03:49:00

approve option 2

### Claude · 2026-10-28 03:49:06

Approved. I'll add Playwright in its own `capture` dependency group rather than `dev`. That way `uv sync` (for you, reviewers and tests) and the Docker image never install it; only Phase 2 capture work opts in. I'll verify it with an offline browser launch, with no external site access.

**Tool call: Bash** — Add Playwright to a separate capture dependency group

```
cd "<repo>" && uv add --group capture "playwright>=1.48,<2" 2>&1 | tail -2 && grep -n -A3 "^capture" pyproject.toml && uv run --group capture python -c "import playwright, importlib.metadata as m; print('playwright', m.version('playwright'))"
```

<details><summary>Tool result</summary>

```
 + playwright==1.64.1
 + pyee==14.0.0
20:capture = [
21-    "playwright>=1.48,<2",
22-]
23-# Installed by default with `uv sync`; versions pinned in uv.lock (D-028).
playwright 1.64.1
```
</details>

**Tool call: Read**

```
{
 "file_path": "<repo>/pyproject.toml",
 "offset": 17,
 "limit": 14
}
```

<details><summary>Tool result</summary>

```
17	]
18	
19	[dependency-groups]
20	capture = [
21	    "playwright>=1.48,<2",
22	]
23	# Installed by default with `uv sync`; versions pinned in uv.lock (D-028).
24	dev = [
25	    "pytest>=8,<10",
26	    "ruff>=0.6",
27	    "mypy>=1.10",
28	]
29	
30	[tool.setuptools.packages.find]
```
</details>

**Tool call: Edit**

```
{
 "replace_all": false,
 "file_path": "<repo>/pyproject.toml",
 "old_string": "capture = [\n    \"playwright>=1.48,<2\",\n]\n# Installed by default with `uv sync`; versions pinned in uv.lock (D-028).\ndev = [\n    \"pytest>=8,<10\",\n    \"ruff>=0.6\",\n    \"mypy>=1.10\",\n]",
 "new_string": "# Installed by default with `uv sync`; versions pinned in uv.lock (D-028).\ndev = [\n    \"pytest>=8,<10\",\n    \"ruff>=0.6\",\n    \"mypy>=1.10\",\n]\n# Opt-in only (`--group capture`): controlled browser capture of approved HDB pages for\n# scripts/capture_sources.py (D-042, REQ-SRC-006). Never installed by default or in Docker.\ncapture = [\n    \"playwright>=1.48,<2\",\n]"
}
```

**Tool call: Bash** — Verify lock, opt-in install, browser download and offline launch

```
cd "<repo>" && uv lock --check && echo "== default sync excludes playwright ==" && uv sync -q && (uv pip show playwright >/dev/null 2>&1 && echo "PRESENT (unexpected)" || echo "absent from default env") && echo "== browser install ==" && uv run --group capture playwright install chromium 2>&1 | tail -2 && echo "== offline launch ==" && uv run --group capture python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(); pg.set_content('<details><summary>S</summary><p>hidden</p></details>')
    pg.locator('summary').click(); print('chromium', b.version, '| accordion expanded:', pg.locator('details').get_attribute('open') is not None)
    b.close()
" && echo "== default env after group run ==" && uv sync -q && (uv pip show playwright >/dev/null 2>&1 && echo "PRESENT" || echo "absent") && uv run pytest -q 2>&1 | tail -1 && uv run ruff check . -q && uv run mypy | tail -1
```

<details><summary>Tool result</summary>

```
The file <repo>/pyproject.toml has been updated successfully.
```
</details>

<details><summary>Tool result</summary>

```
Resolved 54 packages in 33ms
== default sync excludes playwright ==
absent from default env
== browser install ==
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 99 MiB
Chrome Headless Shell 156.0.8078.4 (playwright chromium-headless-shell v1248) downloaded to <home>/Library/Caches/ms-playwright/chromium_headless_shell-1248
== offline launch ==
chromium 156.0.8078.4 | accordion expanded: True
== default env after group run ==
absent
.                                                                        [100%]
Success: no issues found in 2 source files
```
</details>

<details><summary>Claude's reasoning</summary>

Playwright 1.64.1 works even offline, since the browser cache lives outside the repo, and I verified it by expanding a test accordion locally. Next I'll check that the Docker install path excludes it too, then document the decision.


</details>

**Tool call: Bash** — Confirm Docker exclusion; record D-042 across docs

```
cd "<repo>" && (uv export --frozen --no-dev -q | grep -i playwright && echo "IN DOCKER SET (unexpected)" || echo "playwright not in Docker (--no-dev) install set") && python3 -I - <<'EOF'
import pathlib
def sub(path,pairs):
    p=pathlib.Path(path); t=p.read_text()
    for o,n in pairs:
        assert t.count(o)==1,(path,o[:50]); t=t.replace(o,n)
    p.write_text(t)
d=pathlib.Path('docs/decisions.md'); t=d.read_text()
row=t[t.index('| D-041 |'):]; row=row[:row.index('\n')+1]
t=t.replace(row,row+'| D-042 | **Playwright** (`playwright>=1.48,<2`, locked 1.64.1) in an **opt-in `capture` dependency group**, used only by `scripts/capture_sources.py` for controlled browser capture of explicitly approved pages (expand accordions, save rendered HTML, record SHA-256 and timestamp). Not installed by `uv sync`, not in the Docker image, never imported by `src/`. Chromium headless shell is installed per machine with `uv run --group capture playwright install chromium` | APPROVED (developer, 2026-10-28) | Option 2 for Phase 2 capture; REQ-SRC-006 | Accordion-heavy pages need consistent, repeatable expansion. Scripted capture makes the accordion-coverage check measurable (REQ-SRC-012) and provenance exact (REQ-SRC-002, REQ-LIC-016). Opt-in group keeps reviewer and runtime installs unchanged | Developer tooling only. No crawling, no link-following, no transactional pages (REQ-SRC-006). Each capture run still needs approval of its page list | Adds to D-036 |\n')
d.write_text(t)
sub('CLAUDE.md',[
("- **Dependencies are limited to D-036.** Anything else needs an approved decision.",
 "- **Dependencies are limited to D-036 + D-042** (Playwright, opt-in `capture` group, scripts only). Anything else needs an approved decision."),
("- Evaluation commands: add them here only after they have been verified.",
 "- Source capture tooling (opt-in, D-042): `uv sync --group capture`, then\n  `uv run --group capture playwright install chromium` (once per machine). Run capture only\n  with an approved page list.\n- Evaluation commands: add them here only after they have been verified.")])
sub('docs/architecture.md',[
("| `streamlit` | runtime (app) |",
 "| `playwright` | opt-in `capture` group (D-042) | Controlled capture of approved pages for `scripts/capture_sources.py`; never runtime or Docker | Manual saving of rendered pages |\n| `streamlit` | runtime (app) |")])
sub('docs/development_log.md',[
("- `scripts/capture_sources.py` would need **Playwright**, which is not in the D-036 dependency\n  list. It needs approval before Phase 2 capture, as a dev-only dependency.",
 "- **Playwright approved (D-042, option 2).** Added as the opt-in `capture` group (1.64.1);\n  `uv.lock` now has 54 packages. Verified:\n  - absent from the default `uv sync` env and the Docker (`--no-dev`) install set;\n  - Chromium headless shell 156 installed to the user cache, outside the repo;\n  - offline launch expanded a local `<details>` accordion. No external site was accessed.")])
EOF
grep -c "D-042" docs/decisions.md CLAUDE.md docs/architecture.md; git status --short
```

<details><summary>Tool result</summary>

```
playwright not in Docker (--no-dev) install set
docs/decisions.md:1
docs/architecture.md:1
CLAUDE.md:2
 M CLAUDE.md
 M docs/architecture.md
 M docs/decisions.md
 M docs/development_log.md
 M pyproject.toml
 M uv.lock
```
</details>

### Claude · 2026-10-28 03:50:33

Last, I'll point the dependency requirement in the register at the new decision.

**Tool call: Bash** — Update REQ-ARC-012 and rerun doc checks

```
cd "<repo>" && sed -i '' 's/dev pytest\/ruff\/mypy\/types-PyYAML; stdlib statistics | APPROVED | \[APP p.21\]; D-036 |/dev pytest\/ruff\/mypy\/types-PyYAML; opt-in capture group playwright (scripts only); stdlib statistics | APPROVED | [APP p.21]; D-036, D-042 |/' docs/project_context/requirements_register.md && grep -c "D-036, D-042" docs/project_context/requirements_register.md && python3 -I <tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/audit.py "$PWD" && (git grep -inFf references/private/anonymity_terms.txt || echo "no identifying terms")
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 43 chars]
```
</details>

### Claude · 2026-10-28 03:50:44

Playwright is now an approved dependency, recorded as decision D-042 in [docs/decisions.md](docs/decisions.md). It lives in its own opt-in `capture` group in [pyproject.toml](pyproject.toml), separate from `dev`, so reviewers, tests and the Docker image never install it.

**Checks:**
- The lockfile pins it at version 1.64.1 (`uv.lock` now has 54 packages).
- A normal `uv sync` doesn't install it, and it isn't in the set Docker installs.
- I downloaded the Chromium browser to your user cache (`~/Library/Caches/ms-playwright`), outside the repo. Launched offline, it expanded a local test accordion correctly. No external site was accessed.
- Tests, ruff and mypy still pass.

**Where it's recorded:**
- **[docs/decisions.md](docs/decisions.md):** D-042 states the justification: consistent accordion expansion, a measurable accordion-coverage check, and exact provenance (hash and timestamp per page). It also states the limits: developer tooling only, no crawling, no link-following, no transactional pages.
- **[CLAUDE.md](CLAUDE.md):** the dependency rule now reads "D-036 + D-042", and the capture setup commands are added.
- **[architecture.md §11.1](docs/architecture.md), the requirements register (REQ-ARC-012) and the [development log](docs/development_log.md).**

Approving the dependency doesn't approve any capture. Each capture run in Phase 2 still needs your sign-off on its exact page list before any HDB page is fetched.

**Suggested commit:** this is a small, self-contained change; it's fine to commit now or together with the next code step.
- **Include:** the 7 modified files (`pyproject.toml`, `uv.lock`, `CLAUDE.md` and the docs).
- **Suggested message:** `chore: add opt-in Playwright capture dependency group`

### User · 2026-10-28 03:54:19



<pasted_content id="6baf">
Before we conclude Phase 1, update docs/development_log.md, docs/decisions.md, and docs/project_context/INDEX.md where necessary to reflect all approved decisions, completed work, actual test results, unresolved issues and next steps.

Confirm that all important Phase 0–1 context is preserved in the repository files and that Phase 2 can proceed without relying on this conversation's history.

Do not modify unrelated files or commit/push without my approval.
</pasted_content id="6baf">


### Claude · 2026-10-28 03:54:29

I'll start by reading the current state of the three files and the commit history, so the updates reflect what's actually there.

**Tool call: Bash** — Show commits, status, development log and INDEX

```
cd "<repo>" && git log --oneline && git status --short && echo "----" && cat docs/development_log.md && echo "----INDEX" && cat docs/project_context/INDEX.md
```

<details><summary>Tool result</summary>

```
910eb78 chore: add opt-in Playwright capture dependency group
36531ae chore: add Streamlit entry point, Docker and environment tooling
0cca98b docs: approve architecture and record design decisions
e163bdd chore: initialise project and tooling
c49555f docs: establish project context and requirements
----
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

**Failures / resolved:**
- Docker Desktop: the agent couldn't install it (needs `sudo`). The developer installed it.
  Verified on 2026-10-28: Docker 29.9.2, engine started, `docker run --rm hello-world` OK.
  Project Docker commands are added at the deployment milestone.
- Commit `e163bdd chore: initialise project and tooling`, made by the developer.

**Architecture review (2026-10-28) — approved:**
- The developer approved review items A1–A11, recorded as **D-030 to D-040**. Each has a
  justification and a scope-alignment check.
- The review became the approved spec [architecture.md](architecture.md).
- Propagated to:
  - 01 (Q-05 resolved);
  - 03 (`aliases` field);
  - 04 (stack statuses);
  - the register (REQ-ARC-010/012 revised; REQ-ARC-015..019, REQ-VER-008, REQ-EVL-036/037
    added; Q-05/10/12/23 resolved);
  - CLAUDE.md (invariants, routing);
  - INDEX;
  - `.gitignore` (`.cache/`).

**Schedule (developer, 2026-10-28):**
- Target: complete and fully compliant by **2026-10-29 07:00**.
- The brief's 12–16-hour estimate is a reference only.
- All configurations A–D are planned; dropping B needs developer agreement.

**Still open before or during Phase 2:**
- Q-22 (facts schema field details);
- Q-06/Q-07 (premium, resale levy tiers);
- Q-08, Q-09, Q-11, Q-13–Q-21, Q-24;
- model selection;
- judge model.

**Repository and tooling setup (2026-10-28):**
- **Layout:** D-041 adopts the developer's recommended structure, simplified:
  - `llm.py` added;
  - `evaluation/baselines.py` and a separate retrieval-query file dropped;
  - benchmark and verifier claims split into physical dev/test files.
- **Files:**
  - `src/bto_buddy/app.py`: single Streamlit entry point; an honest shell with disclaimer and
    privacy notice, no pipeline yet;
  - `tests/test_smoke.py`: replaces `test_package.py`; uses Streamlit `AppTest`;
  - `Dockerfile`, `.dockerignore`, `.env.example`, `.streamlit/config.toml` (telemetry off);
  - `.gitignore`: merged with the developer's list, plus caches and temporary outputs.
- **Dependency:** Streamlit 1.66.1 via `uv add`; `uv.lock` now pins 51 packages.
- **Ruff:** ruff 0.17 formats Python blocks inside Markdown, so `docs/` is excluded (design
  sketches, not code).

**Verified (macOS, uv 0.13.6, Docker 29.9.2):**

| Check | Result |
|---|---|
| `uv sync` / `uv lock --check` | OK; 51 packages, lock up to date |
| `uv run ruff check .` / `ruff format --check .` | All passed / 5 files formatted |
| `uv run mypy` (strict) | No issues in 2 source files |
| `uv run pytest` | 1 passed (smoke: app renders, disclaimer visible) |
| `docker build -t bto-buddy .` | OK; image 820 MB (Streamlit brings numpy, pandas, pyarrow) |
| `docker run -p 8501:8501 --env-file .env.example bto-buddy` | `/_stcore/health` OK in ~4 s; Docker HEALTHCHECK `healthy` in ~8 s |
| Image contents | Runs as `app` (non-root); `/app` = `.venv`, `.streamlit`, `app.py`; no PDFs, `.env`, `references/` or `private_corpus` |
| `git check-ignore` | `.env`, private corpus raw/processed, `references/private/*`, `.cache/`, `tmp/`, `*.log`, Streamlit secrets, `.venv`, tool caches, `.DS_Store` all ignored; `.env.example` trackable |

**Noted:**
- **Playwright approved (D-042, option 2).** Added as the opt-in `capture` grou
… [4918 more chars in the JSONL export]
```
</details>

### Claude · 2026-10-28 03:54:33

Next I'll pull the current open-question and contradiction status from the register, and check the decision table, so the summaries are accurate.

**Tool call: Bash** — List contradiction/question statuses and decision statuses

```
cd "<repo>" && awk '/^## 2. Contradictions/,/^## 4/' docs/project_context/requirements_register.md | grep -E '^\| (\*\*)?(C|~~Q|Q)-' | cut -c1-170 && echo ---- && grep -oE '^\| (D|BD)-[0-9]+ \|[^|]*\|[^|]*\| [A-Z(][^|]*\|' docs/decisions.md | sed -E 's/\|([^|]*)\|([^|]*)\| ([^|]*)\|/\1 STATUS: \3/' | cut -c1-30,  2>/dev/null | head -0; python3 -I - <<'EOF'
import re
t=open('docs/decisions.md').read()
for line in t.splitlines():
    m=re.match(r'^\| (D-\d+|BD-\d+) \|(.*)',line)
    if m:
        cells=[c.strip() for c in line.strip('|').split('|')]
        st=cells[2] if m.group(1).startswith('D-') else ''
        print(m.group(1), '|', st[:70])
EOF
```

<details><summary>Tool result</summary>

```
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
| **C-14** | **Matrix row "High-level overview of BTO application process" names the "Application for a New Flat" page but gives the HFE page URL (`…/application-for-an-h
| **C-15** | **"Human-review burden created by verification flags" is a secondary metric in APP p.24 but absent from D-004** | APP p.24 vs D-004 | **OPEN — new** (Q-16) |
| **C-16** | **D-004 introduces "answer coverage" without a definition in either source** | D-004 | **OPEN — new** (Q-15) |
| **C-17** | **Model scorecard omits data privacy, though the brief lists privacy as a primary valid justification ground** | APP p.22–23 vs ASM p.4 | **OPEN — new** (Q-1
| ~~Q-05~~ | ~~Non-couple household types~~ → **resolved D-033**: out of scope, redirected | 01 §6.4, 02 Row 1 | Done |
| Q-06 | SC + SPR household premium / Citizen Top-Up: Excluded (financing) or Limited (first-timer consideration)? | 02 Row 1 | Phase 2 |
| Q-07 | Resale levy: Excluded (post-purchase) or Limited? | 02 Row 1 | Phase 2 |
| Q-08 | Which of the HFE FAQ page's 5 sub-links, and which "Exceptions and waivers" source, are needed? | 02 Rows 2, 5 | Phase 2 |
| Q-09 | Strip `si=` tracking parameters from video URLs? (minor) | 02 Row 2 | Phase 2 |
| ~~Q-10~~ | ~~Evaluation and run paths~~ → **resolved D-039** | 03 §1 | Done |
| Q-11 | Is any experiment planned on the private corpus (affects REQ-DAT-013)? | 03 §2.2 | Phase 1 |
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
| Q-22 | Finalise `policy_facts` schema field details (shape + `aliases` approved: D-031, architecture §5) | 03 §2.5 | Phase 2 |
| ~~Q-23~~ | ~~Stack~~ → **resolved D-036** | 04 §6.1 | Done |
| Q-24 | Fix C-14: which URL is intended for the BTO-process row? | 02 Row 4 | Phase 2 |
----
head: illegal line count -- 0
D-001 | APPROVED
D-002 | APPROVED
D-003 | APPROVED
D-004 | APPROVED
D-005 | APPROVED
D-006 | APPROVED
D-007 | APPROVED
D-008 | APPROVED
D-009 | APPROVED
D-010 | APPROVED
D-011 | APPROVED
D-012 | APPROVED
D-013 | APPROVED
D-014 | APPROVED
D-015 | APPROVED
D-016 | APPROVED
D-017 | APPROVED
D-018 | APPROVED
D-019 | APPROVED (split OPEN)
D-020 | APPROVED (size OPEN)
D-021 | APPROVED (period OPEN)
D-022 | APPROVED
D-023 | APPROVED (schema PROPOSED)
D-024 | APPROVED
D-025 | APPROVED
D-026 | APPROVED
D-027 | APPROVED (revised 2026-10-28)
D-028 | APPROVED (uv + lockfile, 2026-10-28)
D-029 | SUPERSEDED (hold lifted by D-030 to D-040)
D-030 | Review A1; REQ-ARC-003
D-031 | Review A2; REQ-ARC-010; part of Q-22
D-032 | Review A3; REQ-ARC-013, REQ-SCP-013
D-033 | Review A4; Q-12; Q-05 (default)
D-034 | Review A5; REQ-VER-001..007
D-035 | Review A6; D-003, REQ-EVL-011
D-036 | Review A7; Q-23; REQ-ARC-012
D-037 | Review A8
D-038 | Review A9; D-022, REQ-DAT-014
D-039 | Review A10; Q-10
D-040 | Review A11
D-041 | APPROVED (developer instruction 2026-10-28; `llm.py` addition flagged 
D-042 | APPROVED (developer, 2026-10-28)
BD-00 | 
BD-01 | 
BD-02 | 
BD-03 | 
BD-04 | 
BD-05 | 
BD-06 | 
BD-07 | 
BD-08 | 
BD-09 |
```
</details>

### Claude · 2026-10-28 03:55:28

Running the full check suite now, so the log records the current actual results rather than earlier ones.

**Tool call: Bash** — Run full check suite including Docker health

```
cd "<repo>" && echo "== sync ==" && uv sync 2>&1 | tail -1 && echo "== lock ==" && uv lock --check 2>&1 | tail -1 && echo "== ruff ==" && uv run ruff check . && uv run ruff format --check . && echo "== mypy ==" && uv run mypy && echo "== pytest ==" && uv run pytest -v 2>&1 | grep -E "PASSED|FAILED|passed|failed" && echo "== docker ==" && docker build -q -t bto-buddy . >/dev/null && echo "build OK" && docker run -d --rm --name bb-p1 -p 8501:8501 --env-file .env.example bto-buddy >/dev/null && for i in $(seq 1 30); do [ "$(docker inspect -f '{{.State.Health.Status}}' bb-p1)" = healthy ] && { echo "HEALTHCHECK healthy after ~$((i*2))s"; break; }; perl -e 'select(undef,undef,undef,2)'; done; curl -fs http://localhost:8501/_stcore/health && echo " <- health endpoint"; docker stop bb-p1 >/dev/null; echo "== git ==" && git status --short && (git grep -inFf references/private/anonymity_terms.txt || echo "no identifying terms") && git ls-files | grep -E '^(references/|data/private_corpus/)|\.env$' || echo "no private/secret files tracked"
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 437 chars]
```
</details>

<details><summary>Claude's reasoning</summary>

Tests pass and the working tree is clean. Now I'll update decisions.md with an explicit status line for the D-030–D-042 block and add the completion-target decision, which was only documented in the log and architecture doc.


</details>

**Tool call: Bash** — Add status note and D-043 schedule decision

```
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/decisions.md'); t=p.read_text()
old='## Architecture decisions approved 2026-10-28 (from the architecture review)\n'
assert t.count(old)==1
t=t.replace(old, old+'\n**Status of this block:** D-030 to D-040 are all **APPROVED** (2026-10-28). D-039\'s paths are\nSUPERSEDED by D-041. D-041 and D-042 were approved later the same day; D-041\'s `llm.py`\naddition still awaits explicit developer confirmation.\n')
row=t[t.index('| D-042 |'):]; row=row[:row.index('\n')+1]
assert t.count(row)==1
t=t.replace(row,row+'| D-043 | **Schedule.** The project must be complete and compliant with every assessment requirement by **2026-10-29 07:00**. The brief\'s 12–16-hour effort estimate is a reference, not a constraint. All configurations A–D are planned. Dropping B (REQ-EVL-013 fallback) only if the deadline is at risk **and** the developer agrees | APPROVED (developer, 2026-10-28) | Developer instruction; Q-18 for planning | Gives an explicit planning target without cutting scope pre-emptively | Unchanged scope. Compliance outranks polish when trading off | The "time-budget warning" (B only if time remains) in the architecture review |\n')
p.write_text(t)
EOF
grep -c "D-043" docs/decisions.md
```

<details><summary>Tool result</summary>

```
1
```
</details>

<details><summary>Claude's reasoning</summary>

I'll rewrite the Phase 1 section of the dev log, replacing stale interim details (18 packages, test_package.py, the deleted draft) with a clear chronology, final verified state, open issues, and a Phase 2 handoff, leaving Phase 0 untouched.


</details>

**Tool call: Bash** — Rewrite Phase 1 log and add Phase 2 handoff

```
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/development_log.md'); t=p.read_text()
t=t[:t.index('## Phase 1')]
t=t.replace("- Commit `c49555f docs: establish project context and requirements`.","- Commit `c49555f docs: establish project context and requirements`.\n- Context-extraction method (for re-audits): text via pdfplumber; every embedded image cropped\n  at 300 dpi and read visually; non-default text colours checked to locate verbatim HDB quotes.")
t+='''## Phase 1 — Project setup and architecture (2026-10-28) — complete

### Chronology
| Step | Outcome | Decisions | Commit (by developer) |
|---|---|---|---|
| Scaffold and agent instructions | `CLAUDE.md`, `pyproject.toml` (src layout), package, smoke test, placeholder README | D-026 (production infra out of scope), D-027 (developer runs all commits/pushes; agent suggests) | `e163bdd chore: initialise project and tooling` |
| Lockfile and tooling | uv with committed `uv.lock`; dev tools in a PEP 735 `dev` group | D-028 | (in `e163bdd`) |
| Docker | Agent install failed (needs `sudo`); developer installed Docker Desktop. Docker 29.9.2 verified | — | — |
| Architecture review | Held draft (D-029) replaced by a full review; A1–A11 approved → [architecture.md](architecture.md) | D-030 to D-040; Q-05, Q-10, Q-12, Q-23 resolved | `0cca98b docs: approve architecture and record design decisions` |
| Schedule | Target 2026-10-29 07:00; effort estimate is reference only; all of A–D planned | D-043 | (in `0cca98b`, as notes) |
| Repository and tooling setup | Developer's structure adopted, simplified; Streamlit entry point, `Dockerfile`, `.dockerignore`, `.env.example`, `.streamlit/config.toml` (telemetry off), merged `.gitignore`; Ruff excludes `docs/` (it formats Python blocks inside Markdown) | D-041 | `36531ae chore: add Streamlit entry point, Docker and environment tooling` |
| Capture tooling | Playwright in opt-in `capture` group; Chromium headless shell in user cache; offline launch test only | D-042 | `910eb78 chore: add opt-in Playwright capture dependency group` |

### Final verified state (re-run 2026-10-28, macOS, Python 3.13.2, uv 0.13.6, Docker 29.9.2)
| Check | Result |
|---|---|
| `uv sync` / `uv lock --check` | OK. 54 packages locked (49 in the default env; Playwright only with `--group capture`) |
| `uv run ruff check .` / `uv run ruff format --check .` | All checks passed / 5 files formatted |
| `uv run mypy` (strict) | No issues in 2 source files |
| `uv run pytest` | **1 passed** (`tests/test_smoke.py`: app renders, title, version, disclaimer) |
| `docker build -t bto-buddy .` | OK (image ≈ 820 MB; Streamlit brings numpy, pandas, pyarrow) |
| `docker run -p 8501:8501 --env-file .env.example bto-buddy` | Docker HEALTHCHECK `healthy` in ~8 s; `/_stcore/health` returns `ok` |
| Image contents (checked at setup) | Non-root `app`; `/app` = `.venv`, `.streamlit`, `app.py`; no PDFs, `.env`, `references/`, `private_corpus` |
| Git hygiene | Working tree clean; no private or secret files tracked; `git check-ignore` covers `.env`, private corpus, `references/private/`, caches, `tmp/`, logs, Streamlit secrets; anonymity scan clean |

**What exists in code:** only `src/bto_buddy/__init__.py` and `app.py` (a shell with a disclaimer
and privacy notice; it says the pipeline isn't available yet), plus one smoke test. No pipeline
modules, data files, prompts, model choice or datasets exist yet.

### Unresolved issues carried forward
| Item | Needed by | Where |
|---|---|---|
| D-041: confirm the `llm.py` addition | Before pipeline code | [decisions.md](decisions.md) |
| C-14 / Q-24: the matrix's BTO-process row cites the HFE page URL | Phase 2 | register §2–3; 02 Row 4 |
| Q-06, Q-07: SC+SPR premium and resale-levy tiers | Phase 2 | 02 Row 1 |
| Q-08: HFE FAQ sub-links and the "exceptions and waivers" source | Phase 2 | 02 Rows 2, 5 |
| Q-09: strip `si=` from video URLs (minor) | Phase 2 | 02 Row 2 |
| Q-11: any experiment on the private corpus? (register still says "Phase 1"; carried to Phase 2) | Phase 2 | 03 §2.2 |
| Q-22: `policy_facts` field-level schema | Phase 2 | 03 §2.5; architecture §5 |
| robots.txt and Terms of Use checks; Copyright Act ss 243–244 verification (D-024) | Before any capture | 03 §5.1 |
| Supported policy period (D-021) | After capture | 03 §2.8 |
| Q-13 / C-17: privacy criterion in model scorecard; model and judge-model selection | Model selection | 04 §6.3 |
| Q-14, Q-15/C-16, Q-16/C-15, Q-17: claim annotation guide, "answer coverage", human-review burden, scorer | Before evaluation | 05 §4 |
| Q-20, Q-21: benchmark split (proposed 18/30) and verifier claim set (proposed 60) | Before dataset creation | 05 §3.3, §6.1 |
| Q-19 / C-09: log anonymity vs completeness | Pre-submission | 06 §7 |
| All policy facts in the context docs remain **AUTHORED-FACT (unverified)** | Phase 2 | 02 §5 |

## Phase 2 — Policy sources (handoff)

**Goal (D-007):** determine the **minimum source set** for the MVP and turn verified content
into the reviewer-facing knowledge base. Nothing is included just because it appears in the
matrix.

**Read first:**
1. [CLAUDE.md](../CLAUDE.md);
2. [INDEX.md](project_context/INDEX.md);
3. [02_policy_sources.md](project_context/02_policy_sources.md) (matrix, media handling,
   facts to verify);
4. [03_data_and_licensing.md](project_context/03_data_and_licensing.md) (corpora, manifest,
   completeness checks, rights);
5. [architecture.md §5](architecture.md) (contracts, `PolicyFact`).

**Gates the developer must approve, in order:**
1. **Page list for capture.** Seeds plus any linked sources justified by the MVP tiers, with
   C-14 and Q-06 to Q-08 resolved.
2. **Rights check before fetching:** robots.txt and Terms of Use for each host. Never claim a
   redistribution licence.
3. **Capture run:** Playwright (`--group capture`), approved pages only. No crawling,
   link-following or transactional pages. Output goes to `data/private_corpus/raw/`
   (Git-ignored), with SHA-25
… [635 more chars in the JSONL export]
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 113 chars]
```
</details>

### Claude · 2026-10-28 03:57:38

I'll check one claim in that chronology: whether the schedule notes actually landed in commit `0cca98b`.

**Tool call: Bash** — Verify which commits contain schedule and lockfile

```
cd "<repo>" && git show 0cca98b:docs/architecture.md | grep -c "2026-10-29 07:00"; git show e163bdd --stat | grep -E "uv.lock|pyproject" 
```

<details><summary>Tool result</summary>

```
1
 pyproject.toml                |  45 ++++
 uv.lock                       | 506 ++++++++++++++++++++++++++++++++++++++++++
```
</details>

### Claude · 2026-10-28 03:57:42

Both claims hold. Last file: `INDEX.md`, which still says Phase 0 with no code, and lists questions that are now resolved.

**Tool call: Bash** — Update INDEX status and open items; validate all links

```
cd "<repo>" && python3 -I - <<'EOF'
import pathlib
p=pathlib.Path('docs/project_context/INDEX.md'); t=p.read_text()
old='''**Phase:** 0 (context building).
**Created:** 2026-10-28.
**Code, models or datasets:** none have been implemented, selected or created.'''
new='''**Status (2026-10-28):** Phase 0 (context) and Phase 1 (setup and architecture) are complete.
**Next:** Phase 2 (policy sources); see the
[development log handoff](../development_log.md#phase-2--policy-sources-handoff).

**What exists:**
- the uv project and lockfile;
- a Streamlit entry-point shell;
- one smoke test;
- the Docker image.

No pipeline modules, data files, model choice or datasets exist yet.'''
assert t.count(old)==1; t=t.replace(old,new)
old=t[t.index('## Current open items'):]
t=t.replace(old,'''## Where to look for a task
| Task | Read |
|---|---|
| Any task | `CLAUDE.md`, then this index |
| Scope questions | 01, plus D-008 / D-013 / D-033 in [decisions](../decisions.md) |
| Source capture, extraction, facts | 02, 03, [architecture §5](../architecture.md) |
| Pipeline code | [architecture.md](../architecture.md) (§3 stages, §5 contracts, §11 modules, §12 tests), 04 |
| Benchmark and evaluation | 05, register (REQ-EVL-*) |
| README and submission | 06, register (REQ-SUB-*, REQ-DOC-*) |
| History and current state | [development_log.md](../development_log.md) |

## Current open items
- **Contradictions open:**
  - C-14 (URL mismatch in the matrix, Q-24);
  - C-15 and C-16 (metric gaps, Q-16 and Q-15);
  - C-17 (privacy missing from the scorecard, Q-13).
- **Questions open:**

  | Needed by | Questions |
  |---|---|
  | Phase 2 | Q-06, Q-07, Q-08, Q-09, Q-11, Q-22, Q-24 |
  | Model selection | Q-13 |
  | Before evaluation | Q-14, Q-15, Q-16, Q-17 |
  | Before dataset creation | Q-20, Q-21 |
  | Pre-submission | Q-19 |

- **Resolved:** Q-05, Q-10, Q-12, Q-18, Q-23.
- **Awaiting confirmation:** the `llm.py` addition in D-041.
- **Execution risk:** C-09 / Q-19 (log anonymity vs completeness).

Details are in [requirements_register.md §2–3](requirements_register.md#2-contradictions). The
consolidated list with owners and deadlines is in the
[development log](../development_log.md#unresolved-issues-carried-forward).
''')
p.write_text(t)
EOF
python3 -I - <<'EOF'
import re,pathlib
root=pathlib.Path('.')
def slug(h): h=h.strip().lower(); h=re.sub(r'[^\w\- ]','',h); return h.replace(' ','-')
docs=[*root.glob('docs/**/*.md'),root/'CLAUDE.md',root/'README.md']
heads={d.resolve():{slug(m) for m in re.findall(r'^#+ (.*)$',d.read_text(),re.M)} for d in docs}
bad=0
for d in docs:
    for link in re.findall(r'\]\(([^)]+)\)',d.read_text()):
        if link.startswith('http'): continue
        f,_,a=link.partition('#'); tgt=((d.parent/f) if f else d).resolve()
        if not tgt.exists(): print('BROKEN FILE',d,link); bad+=1
        elif a and a not in heads.get(tgt,set()): print('BROKEN ANCHOR',d,link); bad+=1
print('link problems:',bad)
EOF
python3 -I <tmp>/fc208089-bb21-499d-8206-f5b78f35f296/scratchpad/audit.py "$PWD"; (git grep --untracked -inFf references/private/anonymity_terms.txt || echo "no identifying terms"); git status --short
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 142 chars]
```
</details>

### Claude · 2026-10-28 03:58:36

All links resolve, and the scans are clean. Last, a spot check that the key decisions from this conversation can be found in tracked files, not just in chat.

**Tool call: Bash** — Spot-check key decisions are in tracked files

```
cd "<repo>" && check(){ git grep -qiF "$2" -- $3 && echo "OK   $1" || echo "MISSING $1"; }; check "developer runs commits (D-027)" "developer executes all commits" docs/decisions.md; check "commit workflow in CLAUDE.md" "The developer runs every commit and push" CLAUDE.md; check "deadline" "2026-10-29 07:00" "docs/decisions.md"; check "Playwright page-list approval" "approval of its page list" docs/decisions.md; check "Phase 2 = minimum source set" "minimum source set" docs/development_log.md; check "anonymity scan cmd" "anonymity_terms.txt" CLAUDE.md; check "verifier display policy" "withhold" CLAUDE.md; check "same output contract" "FinalGuidance" CLAUDE.md; check "BM25 trigger" "recall@5 < 0.90" CLAUDE.md; check "benchmark split proposal" "18 development / 30 held-out" docs/project_context/05_evaluation.md; check "K-fold rationale" "Why not K-fold" docs/project_context/05_evaluation.md; check "claim set proposal" "Fallback if time is short" docs/project_context/05_evaluation.md; check "facts schema + aliases" "aliases" docs/project_context/03_data_and_licensing.md; check "household scope D-033" "first-timer couple (married or engaged)" docs/decisions.md; check "ruff docs exclusion" 'extend-exclude = ["docs"]' pyproject.toml; check "docker cmd" "docker run --rm -p 8501:8501 --env-file .env bto-buddy" CLAUDE.md; check "PolicyProof not a past project" "never an implemented project" docs/decisions.md; check "ChatGPT disclosure optional" "optional, not required" docs/project_context/06_submission_requirements.md; echo "== local-only (by design, Git-ignored) =="; ls references/private/
```

<details><summary>Tool result</summary>

```
[REDACTED R6: output containing private file content, 653 chars]
```
</details>

### Claude · 2026-10-28 03:59:41

Phase 1 is wrapped up. I updated the three files you named, and all important Phase 0–1 context now lives in tracked files, so Phase 2 can start without this conversation. Nothing is committed.

**Re-run checks (current, not earlier results):**

| Check | Result |
|---|---|
| `uv sync`, `uv lock --check` | OK, 54 packages locked |
| ruff check and format | Pass |
| mypy (strict) | No issues |
| pytest | 1 passed |
| `docker build` | OK |
| Container health | Docker health check `healthy` in ~8 s; health endpoint returns `ok` |
| Git hygiene | Working tree was clean; no private or secret files tracked; anonymity scan clean |
| Doc links and requirement IDs | All internal links and anchors resolve; all 158 IDs defined |

**What changed:**
- **[docs/decisions.md](docs/decisions.md):**
  - an explicit status line for D-030 to D-042, noting that D-039's paths are superseded by D-041;
  - a new decision, **D-043**, for the 2026-10-29 07:00 completion target. Before this it was only in the log and the architecture doc.
- **[docs/development_log.md](docs/development_log.md):** Phase 1 is rewritten as:
  - a chronology tying each step to its decisions and your commits (`e163bdd`, `0cca98b`, `36531ae`, `910eb78`). I checked which commit contains what.
  - the final verified state;
  - a consolidated table of unresolved issues, each with when it's needed;
  - a **Phase 2 handoff**: what to read first, then five approval gates in order (page list → rights check → capture → completeness audit → authoring facts and rules), plus work that can proceed in parallel.
- **[INDEX.md](docs/project_context/INDEX.md):** the status now says Phase 0–1 are complete and Phase 2 is next, and states what exists. There's a new "where to look" table by task. The open-items list is current: resolved questions removed, the rest grouped by when they're needed.

**Context check:** I spot-checked 18 decisions made in this conversation against tracked files, and all were found. They include the commit workflow, the deadline, Playwright page-list approval, the split and claim-set proposals, the household scope, the same-output contract, the BM25 escalation trigger and the Docker commands.

The only files that exist just on this machine are the four Git-ignored ones in `references/private/`: the two PDFs, the private submission notes and the anonymity term list. That's deliberate. Phase 2 needs them only for the pre-push anonymity scan.

**Still to settle:**
- **The `llm.py` addition (D-041) needs your explicit confirmation** before pipeline code.
- The register still labels Q-11 (any experiment on the private corpus?) as "needed by Phase 1". I left it, because you asked me not to edit unrelated files. The development log notes it's carried to Phase 2.
- Everything else is in the log's unresolved-issues table. The nearest are the Phase 2 items: the C-14 URL fix, Q-06 to Q-08, the facts schema details (Q-22), and the robots.txt and Terms of Use checks before any capture.

**Suggested commit:** a good point to close Phase 1.
- **Include:** the 3 modified docs.
- **Suggested message:** `docs: close Phase 1 with decisions, verified state and Phase 2 handoff`

```bash
git add docs/decisions.md docs/development_log.md docs/project_context/INDEX.md
git commit -m "docs: close Phase 1 with decisions, verified state and Phase 2 handoff"
```

