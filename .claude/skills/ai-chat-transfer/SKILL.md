---
name: ai-chat-transfer
description: Copy or move saved Codex, Claude Code, or Cursor conversations between computers or workspace folders so they can be resumed in their original application. Any of these assistants can perform the transfer; this does not convert chat formats between applications.
---

# AI chat transfer

Codex, Claude Code, and Cursor can each transfer saved chats from all three
applications. Choose the procedure by the application that owns the chat,
regardless of which agent is executing this skill. Chats resume in their original
application; this skill does not convert formats between applications.

## Resolve the request

Identify the source application and client, selected session, source workspace,
destination machine/user, and absolute destination workspace. Inspect actual
paths on each machine. Ask only for missing information that affects the transfer.

For “this chat,” verify the executing application's session identifier against
storage. `CODEX_THREAD_ID` identifies a Codex thread; `CLAUDE_CODE_SESSION_ID`,
when present, may identify a Claude Code session. Neither selects another
application's chat. Resolve other chats by ID or title from their own metadata.
Never silently choose the newest chat or copy all chats because an ID is unknown.

Default to copying the selected chat and retaining the source. Copy project files
only when requested. An explicit transfer request authorizes the scoped copy;
honor tool permissions without adding a second approval for the same action.
Remove the source only after explicit removal authorization and confirmed
successful continuation at the destination.

## Read the matching procedure

Before transferring, read the reference for the application that owns the chat.
Load only the relevant reference; for a multi-application request, read each needed
procedure before handling its chats. Reference paths are relative to this skill.

| Chat owner | Required reference | Covers |
| --- | --- | --- |
| Codex | [references/codex.md](references/codex.md) | Resume elsewhere, independent copies, storage migration |
| Claude Code | [references/claude-code.md](references/claude-code.md) | Transcripts, companions, copy helper |
| Cursor | [references/cursor.md](references/cursor.md) | Client discovery, chat store, workspace metadata |

Inspect installed versions and storage layouts on both sides. These procedures
use implementation details, not a guaranteed export/import API. If required data
or its layout is unsupported, stop and explain the specific incompatibility.

## Shared transfer rules

- Prefer idle chats. Active-chat copies are snapshots; later messages and the
  final transfer confirmation are excluded.
- Check collisions and use creation that refuses replacement. Do not overwrite
  existing chats, merge divergent histories, or replace shared databases by default.
- Use an authorized transport and safe quoting. Pass paths and structured data
  through private files or stdin rather than executable shell text.
- Copy only the selected chat and required related records. Exclude credentials,
  global settings, unrelated conversations, and memory unless requested.
- Use private temporary storage. Capture SQLite through consistent backups or
  idle databases; copying a live database alone can omit committed WAL changes.
- Project files, database restores, processes, and services are separate from chat
  history. Do not use mirror deletion for project copies unless requested.
  Historical paths can remain source-specific.

## Verify and hand off

Verify content and required metadata using the selected procedure; a file listing
alone does not establish resumability. State the destination, selected session,
whether project files were copied, and whether the source remains. Give the owning
application's exact resume command or UI steps. Distinguish storage verification
from actual interactive continuation; never claim a test that was not performed.

For compatibility evidence, record source/destination client versions, storage
layout, checks performed, and whether resume accepted a follow-up message. Do not
claim tested compatibility from procedure coverage alone.

Remove transfer-only temporary data after verification. Retain recovery backups
until successful continuation is confirmed and report their locations. Prefer
trash for user files; never delete a shared database to remove one chat. Keep real
chat exports, credentials, personal paths, and host names out of published examples.
