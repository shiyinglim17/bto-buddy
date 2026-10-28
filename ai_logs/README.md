# Coding-agent session logs

These are the complete logs of the five Claude Code sessions in which I built BTO Buddy
(REQ-SUB-010), redacted only for secrets, identifying details, private files and
substantial HDB source text. Every redaction is listed in [REDACTIONS.md](REDACTIONS.md).

| Session | Started (UTC) | Readable transcript | Full redacted log |
|---|---|---|---|
| 01 | 2026-10-25 | [session_01.md](session_01.md) | `sessions/session_01.jsonl` |
| 02 | 2026-10-27 | [session_02.md](session_02.md) | `sessions/session_02.jsonl` |
| 03 | 2026-10-28 | [session_03.md](session_03.md) | `sessions/session_03.jsonl` |
| 04 | 2026-10-28 | [session_04.md](session_04.md) | `sessions/session_04.jsonl` |
| 05 | 2026-10-28 | [session_05.md](session_05.md) | `sessions/session_05.jsonl` |

- **Transcripts** show user prompts, Claude's replies, its reasoning (collapsed), every tool
  call and every tool result (collapsed; very long ones shortened).
- **JSONL files** are Claude Code's own record format, with full text after redaction.
- **Regenerate** from raw copies placed in `ai_logs/private_staging/` (Git-ignored):
  `python3 -I scripts/export_ai_logs.py`. This needs the private term list and corpus, so
  only I can run it.
