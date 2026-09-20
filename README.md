# AI Chat Transfer

Skills for transferring saved AI coding conversations between computers or project folders.

| Tool | Skill | Supporting files |
| --- | --- | --- |
| Codex | [codex/SKILL.md](codex/SKILL.md) | Storage migration reference |
| Claude Code | [claude/SKILL.md](claude/SKILL.md) | Bash transfer helper |
| Cursor | [cursor/SKILL.md](cursor/SKILL.md) | Transfer instructions |

Copy the relevant tool folder, including its supporting files, into your tool’s skill directory. Use `codex-chat-transfer` as the installed folder name for Codex and `chat-transfer` for Claude Code or Cursor.

These skills transfer conversations within the same tool; they do not convert conversations between tools. Project files are separate from chat history. Active conversations are copied as snapshots, and later messages are not automatically synchronized.

Review the selected skill before use. Local storage formats can change between tool versions. The Claude helper can copy every session in a project when no session is specified and no current-session environment variable is available; pass `--session` to select a specific conversation. Its copy operations can overwrite existing destination transcripts.

This repository contains skill instructions and supporting code, not chat exports or account credentials.
