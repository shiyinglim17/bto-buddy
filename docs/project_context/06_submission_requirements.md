# 06 — Submission Requirements

The legend is in [INDEX.md](INDEX.md#legend).

> Requirements from the assessment brief are **paraphrased** (D-016). Organisation, role,
> collaborator handle and submission-portal details are kept privately (D-017) and
> deliberately left out here.

## 1. Overall task — MANDATORY [ASM p.1]
- Pick a problem relevant to Singapore public-sector stakeholders: an agency, a ministry or
  a citizen group (REQ-PRB-001).
- Build an AI-powered prototype, evaluate it comprehensively, and deliver a **Dockerised
  solution** with professional documentation (REQ-SUB-002).
- **AI must be in the core functionality** (REQ-PRB-002).
- **Themes:**
  - unstructured → structured;
  - retrieval & knowledge;
  - generation with guardrails;
  - agents & workflows.

  Any one theme, a combination, or an alternative is acceptable.
- Classification, detection, retrieval, multimodal and agentic methods are all acceptable.
- **The brief's stated intent:** assess problem identification, scoping and technical
  judgement in using AI tools, especially judging viability and validating outputs
  rigorously.

## 2. Deliverables — MANDATORY [ASM p.2]

| ID | Requirement | Planned evidence |
|---|---|---|
| REQ-SUB-001 | Complete instructions for full deployment and execution | README "Run with Docker" section, tested on a clean machine |
| REQ-PRB-002 | **Significant** AI integration, not just an API call inside a standard web app | Architecture section plus ablation results (A–D) |
| REQ-EVL-001 | Choose and justify a specific evaluation method (e.g. benchmarking, LLM-as-judge, human evaluation, ablation, comparison), with the rationale in the README. Soundness outranks results | README evaluation section; [05](05_evaluation.md) |
| REQ-DAT-001 | Provenance, creation/processing, licensing and privacy for **all** data. Resourcefulness in finding data is assessed | README data section; `data/sources_manifest.json`; [03](03_data_and_licensing.md) |
| REQ-LIC-001 | Comply with source licensing and **robots.txt** | Rights review record (Phase 2) |
| REQ-PRIV-001 | If personal data is involved, address the ethics and handling | Synthetic-only statement |
| REQ-DAT-002 | Synthetic data is fine if meaningful and high-fidelity; **defend its use** | README defence ([03 §4](03_data_and_licensing.md)) |
| REQ-DOC-001 | **Documentation is the primary artifact:** objectives, rationale, implementation, results, execution instructions, limitations | README |
| REQ-DOC-002 | A **150–250-word** README section: target user and environment; projected inference cost or compute footprint at scale; key post-deployment monitoring metrics; assessment of **one specific** deployment risk. *Only described, not implemented* | README section, word-count check |
| REQ-DOC-003 | A brief development narrative: iterations, discarded strategies, tool-selection rationale, decision justification | README section, drawing on [../decisions.md](../decisions.md) |
| REQ-SUB-003 | A **3–5 minute** demo video of the running application. **Its URL goes in the README** | README link (placeholder until recorded) |

## 3. Submission protocol — MANDATORY [ASM p.2] (details private)

| ID | Requirement |
|---|---|
| REQ-SUB-004 | Deliver via a **private** GitHub repository with the assessor collaborator invited. *Handle kept in private notes* |
| REQ-SUB-005 | **The repository must remain anonymous** about the organisation and role |
| REQ-SUB-006 | The repository must **remain unchanged** throughout the evaluation period |
| REQ-SUB-007 | Submit the URL through the designated channel. *Details kept in private notes* |
| REQ-SUB-008 | **Deadline:** 5 days from receipt. **Estimated effort:** 12–16 hours of focused work. Submission time isn't scored. The receipt date isn't recorded (Q-18) |

## 4. Scoring dimensions — MANDATORY reference [ASM p.3]

| Dimension | Weight | What is assessed (paraphrased) | Main requirement links |
|---|---|---|---|
| Problem framing & creativity | 20% | Worth solving? A non-obvious angle rather than a first idea or low effort? | REQ-PRB-010..015 |
| Technical execution | 25% | Runs from the README on a clean machine; code quality. AI-assisted coding is expected, careless output is not | REQ-NFR-001, REQ-NFR-002 |
| Evaluation & effectiveness | 30% | Sound methodology. Novelty counts only with effectiveness; a proven approach that works beats a novel one that underperforms. Honest limitations | REQ-EVL-* |
| Data thinking | 15% | Provenance, licensing, representativeness, resourceful sourcing, awareness of what the data does and doesn't cover | REQ-DAT-*, REQ-LIC-* |
| Communication | 10% | The write-up matches the code. No overclaiming, no README features that aren't in the repo | REQ-DOC-004 |

## 5. Critical non-compliance indicators — MANDATORY [ASM p.4]

| ID | Indicator to avoid |
|---|---|
| REQ-NFR-001 | **Not reproducible:** the solution fails when following the README |
| REQ-DOC-004 | **Code/write-up mismatch:** features, architecture or results described that aren't in the repo |
| REQ-NFR-003 | **Insufficient technical justification:** the developer must be able to explain the rationale behind code and architecture |
| REQ-MOD-001 | **Unsubstantiated model selection:** choices must be justified by operational needs such as privacy, latency or task fit |
| REQ-NFR-002 | **Substandard code quality:** AI-assisted code must still meet professional quality and maintainability standards |
| REQ-PRB-003 | **Recycled past project:** must be a fresh project (see D-015 on "PolicyProof") |

## 6. Methods and resources — MANDATORY [ASM p.4]
- **Any accessible AI tools** may be used, including open weights and local inference. **No
  API keys or compute are provided.**
- **REQ-DOC-005:** clearly state the technical limitations, and the enhancements possible if
  those constraints were removed.
- **REQ-NFR-004:** the solution should work within free-tier limits. Note any paid
  infrastructure that production scale would need.
- **REQ-SUB-009:** coding agents are allowed. If used, **include a section at the end of the
  README** on how they supported the work.
- **REQ-SUB-010:** **upload all coding-agent session and chat logs** (e.g. JSONL from the
  Claude Code projects directory) to the repo, and give their location in the README.
- **REQ-MOD-001:** local vs API doesn't matter; the justification must hold up.
  - Valid grounds: data sensitivity, latency, task fit, fine-tuning needs, cost at scale.
  - Invalid grounds: free, cool, already available.
- **Listed free resources:**
  - LLM APIs: Google AI Studio, Groq, OpenRouter, Hugging Face Inference Providers,
    Cerebras, Together AI;
  - local inference: Ollama, llama.cpp, LM Studio;
  - GPU: Google Colab, Kaggle Notebooks, Lightning AI;
  - weights and data: Hugging Face, Kaggle.
- **Supplementary guidance:**
  - anonymised example problem sketches (optional);
  - a gallery of past public-sector hackathon projects, as a calibration of feasible scope.
    *The link is kept privately.*

## 7. AI-assisted development logs — D-009, D-010 [ASM p.4][APP p.30–31]

**Planned layout [APP p.30–31]:**

```
ai_logs/
├── README.md
├── claude_code/
│   ├── session_01.jsonl
│   ├── session_02.jsonl
│   └── session_03.jsonl
└── redactions.md
```

- **Scope (D-009):** the **complete project-specific coding-agent session and chat logs**,
  including Phase 0. Not selected or successful sessions only. Full non-coding brainstorming
  transcripts are not included automatically.
- **Pre-submission audit (D-010), REQ-SUB-020.** Check for:
  - identifying information;
  - credentials;
  - sensitive local paths;
  - restricted source material.

  Redact only what genuinely needs protection. Keep the structure and substance. Document
  every redaction in `redactions.md`. Never delete failed sessions or rewrite prompts.
- **Known risk (C-09):** the logs contain organisation-identifying text copied from the
  brief, plus rendered source material. If completeness and anonymity can't both be met with
  confidence, **escalate to the developer**.

**Draft AI-usage disclosure (PROPOSED, revised per D-009) [APP p.31]:**
> **AI-Assisted Development** — Claude Code was used to support implementation, testing,
> debugging and documentation. Technical decisions, evaluation methodology, reference labels,
> experimental results and final code were reviewed and validated by the developer. Complete
> project-specific coding-agent logs are available under `ai_logs/`. Any security or privacy
> redactions are documented in that directory.

The original draft opened with a paragraph on early-stage brainstorming with a
general-purpose chat assistant. Per D-009, disclosing it is **optional, not required**.

## 8. Developer's own README requirements (APPROVED) [APP p.30–31]

**REQ-DOC-010:** format the README with **HTML** for readability and clear organisation.
Diagrams and flowcharts may explain the methodology and system design where appropriate.

**REQ-DOC-011:** the README holds the essential project story directly:
1. problem;
2. objectives;
3. architecture;
4. dataset provenance summary;
5. evaluation methodology;
6. results;
7. limitations;
8. Docker instructions;
9. deployment considerations;
10. demo link (placeholder);
11. AI-usage disclosure.

**REQ-DOC-012:** separate files are only for supporting detail, such as:
- full benchmark construction;
- extensive error analysis;
- policy-source manifests;
- development decisions.

A reviewer must understand the whole project without opening six documents.

**Other items:**
- **REQ-DOC-015 (optional):** `docs/project_selection.md`, explaining why this problem was
  chosen over the alternatives.
- **REQ-DOC-016:** short code comments where relevant, showing the technical rationale
  (supports REQ-NFR-003).
- **REQ-DOC-019:** demo tooling: Loom, a screen recorder, Supabase for annotation (D-018).

**Earlier open questions, now resolved:**
- "Should documentation be in README or a separate file?" [APP p.29] → resolved by
  REQ-DOC-011 and REQ-DOC-012 [APP p.30].
- "Can the dataset be uploaded here?" [APP p.30] → resolved by D-005 and §5.2 of
  [03](03_data_and_licensing.md). Authored facts and labels are tracked; HDB snapshots are not.

## 9. Ordering and format constraints to remember
- The **coding-agent section goes at the end** of the README (REQ-SUB-009).
- The **demo URL goes in the README** (REQ-SUB-003).
- The deployment section is **150–250 words** (REQ-DOC-002).
- **REQ-DOC-010 / REQ-DOC-011 tension (author observation):** GitHub sanitises some HTML
  (scripts, styles, some attributes are stripped). Mermaid diagrams render in Markdown
  fences but not inside raw HTML blocks. Plan the README format with this in mind.
