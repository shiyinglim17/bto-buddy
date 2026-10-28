# Redactions in the coding-agent logs

All five Claude Code sessions for this project are exported here (REQ-SUB-010). Redaction
was minimal, rule-based and offline (`scripts/export_ai_logs.py`; nothing was sent to any
external service). Every redaction is marked inline as `[REDACTED Rn …]`, and per-session
counts are in `redaction_report.json`. The raw logs are not in the repository.

## Rules

| Rule | What was removed | Why | Replaced with |
|---|---|---|---|
| R1 | API keys and tokens (Groq, Anthropic, OpenAI, Google, GitHub, Bearer shapes) | Credentials | `[REDACTED R1: secret]`. **0 found** |
| R2 | Groq organisation IDs inside provider error messages | Account identifier | `org_[REDACTED R2]` |
| R3 | Personal e-mail addresses (public addresses such as `noreply@anthropic.com` kept) | Personal data | `[REDACTED R3: email]` |
| R4 | Home directory, project path, scratchpad path, OS user name, Git handle | Identifying local paths | `<home>`, `<repo>`, `<tmp>`, `<project-slug>`, `<user>`, `<git-user>` |
| R5 | Terms that identify the assessing organisation, the role or the collaborator (from a private list, word-bounded) | Repository anonymity (REQ-SUB-005) | `[REDACTED R5]` |
| R6 | Content written to, or printed from, private files (`references/private/`, `data/private_corpus/`): the assessment brief, my approach document, private notes and HDB snapshots. The tool call, its command and the file path are kept | Private and copyrighted material; anonymity | `[REDACTED R6: …, N chars]` |
| R7 | Runs of **10 or more consecutive words** found verbatim in the captured HDB pages. URLs, file paths and slugs are never counted as source text | Copyright in HDB text (D-054, D-057) | `[REDACTED R7: N words of HDB source text]` |
| R8 | Base64 images and PDF documents (screenshots, PDF pages read by the agent) | They render private PDFs and cannot be text-scanned | `R8: image/document omitted` |

**Not redacted:** prompts, responses, Claude's reasoning blocks, tool calls and results,
failed attempts, errors, and technical decisions. Shorter verbatim overlaps (8–9 words,
mostly section headings and short phrases) were kept as non-substantial.

## Counts

| Session | Source (Claude Code session ID prefix) | Started (UTC) | Title | R2 | R3 | R4 | R5 | R6 | R7 spans (words) | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| [01](session_01.md) | `04a82c3b` | 2026-10-25 | Bto-buddy project setup verification | 0 | 2 | 42 | 0 | 0 | 0 | 0 |
| [02](session_02.md) | `fc208089` | 2026-10-27 | Phase 0 project context documentation | 0 | 2 | 1,456 | 48 | 20 | 41 (669) | 28 |
| [03](session_03.md) | `b764a348` | 2026-10-28 | Phase 2: Data & Benchmark | 0 | 8 | 4,827 | 3 | 52 | 513 (24,499) | 4 |
| [04](session_04.md) | `02a65132` | 2026-10-28 | Phase 2: Data & Benchmark (title carried over) | 0 | 2 | 1,447 | 0 | 1 | 0 | 0 |
| [05](session_05.md) | `ffcbef25` | 2026-10-28 | Phase 2: Data & Benchmark (title carried over) | 2 | 4 | 1,080 | 0 | 11 | 0 | 0 |

R1 found nothing in any session.

## What else differs from the raw logs

- **Dropped records: client wire copies** (`api-request`, `api-request-blob`,
  `api-request-shape`). These are Claude Code's copies of each API request: the same
  messages again, plus Claude Code's own system prompt and tool schemas. A check found that
  almost all of their text is already in the kept records. **Known gap:** a few text blocks
  exist only in these copies. Most are Claude Code notices (environment updates, `/clear` and
  `/compact` markers, progress nudges, a date change), but **two are my prompts from session
  03**, sent during manual page capture: one asking how to proceed after step 1's output, and
  one reporting step 1 run on the second seed page. They are not in the export.
- **Not included:** three oversized tool outputs that Claude Code saved to separate files.
  The logs keep their preview and the reference.
- **Transcripts** (`session_NN.md`) shorten tool inputs and results over 6,000 characters.
  The JSONL files (`sessions/session_NN.jsonl`) keep the full redacted text.
- **Session 05 is a snapshot.** It was copied while the session was still running, so it
  ends partway through. The final exchange (this export) is not included.

## Verification (after export)

An independent scan of every exported file found:
- 0 key-like strings;
- 0 Groq org IDs;
- 0 identifying terms;
- 0 local paths, user names or Git handles;
- 0 personal e-mail addresses (the only remaining "@" matches are `@pytest` decorators);
- 0 base64 blobs outside the opaque reasoning `signature` fields;
- **0 verbatim HDB runs of 10+ words.** 8–9-word runs remain (non-substantial):
  session 02: 42, 03: 317, 04: 62 (JSONL).

Every user and assistant record, and every content block, from the raw logs is present in
the JSONL. Each transcript shows every tool call (137, 528, 165 and 115 in sessions 02–05;
1 in session 01).
