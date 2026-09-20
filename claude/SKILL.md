---
name: chat-transfer
description: Transfer Claude Code chat session(s) between local folders, or to another machine over SSH, so they can be resumed at the destination. Use when the user asks to move, copy, sync, or transfer a chat/conversation/session to another folder or machine.
---

# Chat transfer

Claude Code stores each chat session as a plain JSONL file at:

```
~/.claude/projects/<slug-of-absolute-cwd>/<session-id>.jsonl
```

where `<slug-of-absolute-cwd>` is the project's absolute working-directory path
with every `/` replaced by `-` (e.g. `/home/alice/myproject` → `-home-alice-myproject`).
There's no database involved, so transferring a session is just copying that file
into the correctly-named directory at the destination — no rewriting of the file's
contents is needed, since the session id inside the file already matches the filename.

Use `scripts/transfer-chat.sh` to do this rather than re-deriving the slug/copy
logic by hand — it handles both local folder→folder and SSH machine→machine cases.

## Usage

```
scripts/transfer-chat.sh --to-path DEST_ABS_PATH [--to-host HOST] [--from-path SRC_ABS_PATH] [--session ID]...
```

- `--to-path` is the **absolute cwd path** the destination project corresponds to
  (not the `.claude/projects` slug) — e.g. `/home/bob/myproject`, not
  `-home-bob-myproject`. The script computes the slug itself.
- `--to-host` is an SSH alias/host (from `~/.ssh/config` or as the user names it).
  Omit it for a same-machine folder-to-folder transfer.
- `--from-path` defaults to `$PWD`.
- `--session` may be repeated to transfer specific sessions. If omitted, it
  defaults to the currently running session (`$CLAUDE_CODE_SESSION_ID`), or,
  if that's unset, every session file in the source project directory.

## Steps to follow

1. **Figure out the destination path.** If the user gives an explicit absolute
   path (or host + path), use it directly. If they just say "transfer to
   `<host>`, similar folder structure exists" without a path, find the
   destination folder first — don't guess:
   ```
   ssh HOST "find ~ -maxdepth 3 -iname '<basename-of-source-folder>'"
   ```
   If there are multiple candidates, ask the user (or pick the one that best
   matches the source's relative structure) rather than assuming.
2. **Run the script** with the resolved paths/host/session id(s).
3. **Verify** — the script already lists the destination directory contents
   at the end; confirm the expected file(s) are present with a sane size.
4. **Tell the user** where the session landed and how to resume it there:
   `claude --resume <session-id>` (or `--continue`) run from the destination
   folder.

## Caveats to mention

- If the session is still live (the one currently running), this is a
  **snapshot** — anything said after the transfer won't be on the other side
  until re-run.
- Absolute file paths referenced *inside* the transcript (tool results, file
  reads) still point at the source machine/folder; resuming shows full
  history, but re-touching those old paths will fail if they don't exist at
  the destination.
- This only copies session transcripts, not the `memory/` subdirectory next
  to them — mention that if the user also wants memory carried over, and
  confirm before copying it (it may contain content scoped to the source
  project only).
