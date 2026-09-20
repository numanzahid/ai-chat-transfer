# AI Chat Transfer

One `ai-chat-transfer` skill for moving saved Codex, Claude Code, and Cursor conversations between computers or project folders.

Every distribution below contains the same skill and supporting files. Any of the three assistants can transfer conversations belonging to any of the three tools.

| Assistant running the skill | Complete distribution | Transfers |
| --- | --- | --- |
| Codex | [codex/](codex/SKILL.md) | Codex, Claude Code, Cursor |
| Claude Code | [claude/](claude/SKILL.md) | Codex, Claude Code, Cursor |
| Cursor | [cursor/](cursor/SKILL.md) | Codex, Claude Code, Cursor |

## Install

Copy one distribution folder, including `references/` and `scripts/`, into the assistant's skill directory and name the installed folder **`ai-chat-transfer`**. All three distributions are identical; installing more than one in the same assistant is unnecessary.

The single `SKILL.md` selects the procedure by the application that owns the conversation. Detailed Codex storage guidance is in `references/storage-transfer.md`; a limited Claude Code helper is in `scripts/transfer-chat.sh`.

## Examples

- Ask Codex: “Transfer my Claude Code session to another computer.”
- Ask Claude Code: “Copy this Cursor conversation to another project folder.”
- Ask Cursor: “Move my Codex conversation so I can resume it on another machine.”

Provide the source application, session ID or title, and destination when they are not already clear from context.

## Scope

Transferring a conversation preserves its original application's format. A Claude Code conversation is still resumed in Claude Code, even when Codex performs the copy. This skill does not convert conversations between applications.

Project files are separate from chat history. Active conversations are copied as snapshots, and later messages are not automatically synchronized. Storage formats vary by version; read the skill's compatibility and verification instructions.

The Claude helper supports only a limited storage layout. Without an explicit session selection it can copy every session in a project, and it can overwrite existing destination transcripts. The skill explains when it can be used and when to perform a scoped transfer another way.

## Maintaining the distributions

Keep `codex/`, `claude/`, and `cursor/` byte-for-byte identical, including supporting files, so each can be installed independently.

This repository contains instructions and supporting code, not chat exports or account credentials.
