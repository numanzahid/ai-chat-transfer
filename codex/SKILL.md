---
name: ai-chat-transfer
description: Copy or move saved Codex, Claude Code, or Cursor conversations between computers or workspace folders so they can be resumed in their original application. Any of these assistants can perform the transfer; this does not convert chat formats between applications.
---

# AI chat transfer

Choose the procedure by the application that owns the saved conversation, not
by the assistant executing this skill. Codex can transfer Claude Code or Cursor
chats, and Claude Code or Cursor can transfer Codex chats. A transferred chat
continues in its original application; cross-application conversion is not covered.

## Resolve the request

Use existing context to identify the source application, selected session, source
workspace, destination machine/user, and absolute destination workspace. Inspect
matching folders instead of assuming both machines have the same home path.
Ask only for missing information that affects the transfer.

For “this chat,” use the executing application's session identifier if available
and verify it against its storage. `CODEX_THREAD_ID` identifies a Codex thread;
`CLAUDE_CODE_SESSION_ID`, when present, may identify a Claude Code session. Neither
selects a chat in another application. When transferring another application's
chat, resolve its ID or title from that application's metadata. Never silently
choose the newest chat or copy all chats because the requested ID is unknown.

Default to copying the selected conversation and retaining the source. Copy
project files only when requested. Remove the source only after explicit removal
authorization and confirmed successful continuation at the destination. An explicit
transfer request authorizes the scoped copy; honor tool-level permissions without
adding a second approval requirement for the same action.

Inspect the installed versions and actual storage layout. These procedures use
local implementation details, not a guaranteed export/import API. If the layout
or required data is unsupported, stop and explain the specific incompatibility.

## Shared transfer rules

- Prefer idle conversations. A copy of an active conversation is a snapshot;
  later messages and the final transfer confirmation are not included.
- Check destination collisions before copying. Do not overwrite an existing chat,
  merge divergent histories, or replace shared application databases by default.
- Use SSH/rsync/scp or another authorized transport. Quote paths safely and pass
  structured data through private files or stdin, not executable shell text.
- Copy only the selected chat and required related records. Do not bundle account
  credentials, global settings, unrelated conversations, or memory by default.
- Use private temporary storage. For SQLite data, use consistent backups or an
  idle database; copying a live database without its committed WAL changes can
  lose history. A file listing alone does not verify a resumable conversation.
- Project files, database restores, running processes, and service connections are
  separate from saved chat history. Do not use mirror deletion for project copies
  unless requested. Historical absolute paths can remain source-specific.

## Codex conversations

### Another folder on the same machine

Inspect `codex resume --help`. When supported:

```bash
codex resume <SESSION_ID> --cd /absolute/destination/project
```

`codex resume --all` finds sessions across folders. This reuses the existing
session; it does not create an independent copy or transfer project files.

### Another computer or Codex home

Read [the Codex storage procedure](references/storage-transfer.md) before copying.
Resolve `CODEX_HOME` independently on each machine, defaulting to `~/.codex`.
The procedure covers thread metadata, transcripts, paginated history, schema
compatibility, destination path mapping, collision handling, and recovery.
A transcript-only copy is not assumed sufficient for paginated sessions.

Preserve transcript bytes when history projections contain byte offsets. Map the
thread's destination paths and resume with an explicit working directory instead
of rewriting historical transcript paths and invalidating the projections.

Verify the imported records and provide the explicit `codex resume` command.
Include the destination `CODEX_HOME` setting when it is nondefault.

## Claude Code conversations

Locate the selected session in the actual Claude Code configuration directory.
A commonly used layout is:

```text
~/.claude/projects/<encoded-absolute-workspace>/<SESSION_ID>.jsonl
```

Inspect the installed directory naming before computing a destination name.
Simple paths commonly replace `/` with `-`; punctuation, platform differences,
or custom configuration directories may require different handling. Do not assume
a slash-only transformation works for every workspace.

1. Verify the selected transcript and look for session-specific companion files
   or directories, such as subagent transcripts. Inspect their purpose and include
   those needed for the requested session; do not assume the main JSONL always
   contains the entire conversation's supporting state.
2. Resolve the destination workspace and encoded project directory. Create the
   destination workspace if needed and copy the selected transcript and required
   companions without changing the session ID or historical text.
3. Verify content hashes and JSONL parsing against a consistent source snapshot.
   Confirm the expected destination files and permissions.
4. From the destination workspace, resume with `claude --resume <SESSION_ID>`.
   Check the installed CLI's help if the syntax differs. Use the explicit ID rather
   than `--continue`, which can select a different conversation.

The bundled `scripts/transfer-chat.sh` is a limited helper for the conventional
home-directory layout and simple paths. Use it only after verifying its slash-only
encoding matches both installations, explicitly selecting every `--session`, and
checking that destinations do not already exist. Its default can copy every
session when no current-session variable exists, and its copy operations can
overwrite files. Its remote commands do not safely quote arbitrary path strings:
use another properly quoted transfer for paths containing spaces or shell syntax.
The helper copies main transcripts only; handle required companions separately.

Run the helper relative to this skill's directory when those conditions hold:

```bash
bash scripts/transfer-chat.sh --from-path /absolute/source/project --to-path /absolute/destination/project --to-host HOST --session SESSION_ID
```

Omit `--to-host` for a local transfer. Project memory is separate; include it only
when requested and scoped to the destination project.

## Cursor conversations

Inspect the installed Cursor storage. For versions with this layout:

| Piece | Typical location |
| --- | --- |
| Chat store | `~/.cursor/chats/<workspace_hash>/<SESSION_ID>/` |
| Transcript | `~/.cursor/projects/<project_slug>/agent-transcripts/<SESSION_ID>/<SESSION_ID>.jsonl` |

The observed workspace hash is the lowercase MD5 of the absolute workspace path.
Confirm it against the source layout before using it at the destination. Determine
project slugs from Cursor's existing directories; do not guess their encoding.
If necessary, open the destination workspace in Cursor to establish its layout.

1. Capture the selected chat directory, including metadata and a consistent
   `store.db`. For an idle file-based copy, preserve any required WAL sidecars;
   do not assemble independently copied live database/WAL files into a snapshot.
   SQLite's backup API is an alternative for producing a standalone consistent DB.
2. Copy the chat under the destination workspace hash and the transcript under
   the destination project slug. Do not transfer only the transcript and call it
   a full chat migration unless a transcript-only backup was requested.
3. Set `cwd` in the destination `meta.json` to the destination absolute workspace.
   Preserve other metadata and historical transcript paths. Fix destination
   ownership if the transfer ran under a different user.
4. Verify session ID, title, `cwd`, transcript, and database integrity. Compare
   copied file hashes where no intentional changes were made.
5. Open the destination workspace in Cursor and find the conversation in history.
   Refresh or restart Cursor if needed; report whether UI continuation was tested.

Project-level `agent-tools/`, `repo.json`, or `worker.log` may contain unrelated
sessions. Inspect and scope any needed additions instead of copying them wholesale.

## Complete the handoff

State the destination, selected session, whether project files were copied, and
whether the source remains. Give the original application's exact resume command
or UI steps. Distinguish storage verification from actual interactive continuation;
never claim an interactive test that was not performed.

Remove transfer-only temporary data after verification. Retain recovery backups
until successful continuation is confirmed and report their locations. Prefer
trash when removing user files; never delete a shared database to remove one chat.
Do not put real chat exports, credentials, personal paths, or host names into the
published skill or its examples.
