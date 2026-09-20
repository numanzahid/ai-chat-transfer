---
name: chat-transfer
description: >-
  Moves or copies Cursor agent chats between machines or workspace folders.
  Covers chat store, transcripts, cwd remapping, and optional project file
  transfer via rsync, scp, or SMB. Use when the user asks to move, copy,
  migrate, or re-home a Cursor chat or conversation to another computer or path.
disable-model-invocation: true
---

# Cursor chat transfer

## Before you start

Ask the user:

1. **Move or copy?** After a move, remove the source chat (and optional files) only if they confirm.
2. **Destination:** host (SSH reachable), absolute **workspace path** to open in Cursor on that side, and chat id or title if unclear.
3. **Project files too?** Whether to transfer only the chat metadata, or also files under the workspace directory (and any related paths they name).

Confirm you can reach the destination (SSH, or SMB mount path for file copy).

## What to transfer (chat minimum)

On the **source** machine, for chat id `<uuid>`:

| Piece | Typical location |
|-------|------------------|
| Chat store | `~/.cursor/chats/<workspace_hash>/<uuid>/` |
| Transcript | `~/.cursor/projects/<project_slug>/agent-transcripts/<uuid>/<uuid>.jsonl` |

Include `store.db` and WAL sidecars when present; omit them only if the user accepts a transcript-only backup.

Optional: `agent-tools/`, `repo.json`, `worker.log` under the same `~/.cursor/projects/<project_slug>/`.

**Workspace hash:** `md5(absolute_workspace_path)` as lowercase hex. Destination path differs => new hash directory on the target.

**Project slug:** Derived from the workspace path (Cursor creates it under `~/.cursor/projects/`). On the target, list that directory once and match the naming pattern; do not guess from memory.

## Transfer steps

1. Create the destination workspace directory if missing (empty is fine for chat-only moves).
2. Copy chat store and transcript to the target user's home (same paths under `~/.cursor/`).
3. Set **`cwd`** in destination `meta.json` to the **destination** absolute workspace path (`jq` or equivalent).
4. Fix ownership on the target if copies ran as another user.
5. Verify: `meta.json` title, `cwd`, and transcript file exist on the target.

**Transport:** `rsync` over SSH is preferred for large `store.db` files. `scp` works for small trees. **SMB:** copy the same relative tree from `~/.cursor/` into the target user's profile on the share, then fix permissions locally on that machine.

## Workspace files (optional)

If the user wants project files moved:

- Copy the workspace tree with rsync/scp/SMB (respect excludes they specify, e.g. large backups, `node_modules`, `db_data`, `*.wpress`).
- Do not rewrite chat transcript paths unless they ask; remapping `meta.json` `cwd` is enough for Cursor workspace association.
- For app stacks (Docker WordPress, etc.), treat database and URL fixes as a **separate** step from chat transfer; confirm before importing DB or running search-replace.

## After transfer

- **Move:** delete source chat dirs after the user confirms success; prefer trash over hard delete when available.
- **Staging cleanup:** remove temporary archives or SQL dumps created only for transfer on both sides.
- Tell the user to open the **destination workspace folder** in Cursor on that machine and restart the IDE if the chat does not appear in history.

## Pitfalls

- Import paths for containerized CLI tools must lie inside volumes the tool container mounts.
- Large backup extensions (e.g. site export archives): exclude by default unless requested.
- Same workspace path string on two machines yields the same chat hash; different paths require moving the chat into the new hash folder on the target.
