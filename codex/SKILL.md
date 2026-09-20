---
name: codex-chat-transfer
description: Copy or relocate a local Codex conversation to another computer or workspace folder and prepare it for resuming, optionally transferring project files. Use for Codex chat migration, not ChatGPT web chats or Cursor chat databases.
---

# Codex chat transfer

Transfer the saved conversation and its workspace association. Running terminals,
processes, in-memory tool state, and remote service connections do not move with it.
This is a local-storage migration workflow, not an official Codex export/import API.

## Establish the scope

Use the user's request and existing context to determine:

- The session to transfer. For “this chat,” use `CODEX_THREAD_ID` when available,
  then verify that ID against the local thread metadata. Do not select the newest
  session by timestamp when several sessions exist.
- Destination SSH host or local machine, destination user, and absolute workspace
  path. Inspect the destination rather than assuming its home or folder layout.
- Whether project files should also be copied. An existing destination project
  does not need to be overwritten just to resume a chat.
- Copy versus move. Default to retaining the source; remove it only when the user
  explicitly requests removal and successful destination continuation is confirmed.

Ask only for missing information that affects the transfer. An explicit request
to transfer authorizes the scoped copy; do not ask again merely because this skill
is being used. Honor tool-level execution and network approval requirements.

## Choose the workflow

### Continue in another folder on the same machine

Check the installed `codex resume --help`. When supported, resume the existing
session with an explicit working directory:

```bash
codex resume <SESSION_ID> --cd /absolute/destination/project
```

`codex resume --all` can locate chats outside the current folder. This reuses the
same session; it does not create an independent copy or move project files.
Explain that distinction when the user specifically requests duplication.

### Copy to another computer or Codex home

Read [the storage transfer procedure](references/storage-transfer.md) before
exporting or importing. It covers the transcript, paginated history, schema
compatibility, collision handling, and verification.

Use the destination's `CODEX_HOME` when configured, otherwise its user's
`~/.codex`. Never assume the source and destination use the same home path.
Transfer only the selected conversation and required related records. Do not
replace the destination's entire Codex directory or database.

If project files are requested, transfer them separately using an appropriate
transport such as rsync or scp. Respect requested exclusions and existing files;
do not use mirror deletion by default. Database restores and application
configuration changes are separate from copying chat history.

## Finish

- Verify the destination transcript and database records, including their workspace
  and transcript paths. Distinguish storage verification from an actual interactive
  resume test; do not claim the latter unless performed.
- Give the exact destination-specific `codex resume` command, optionally preceded
  by the SSH command. For a nondefault Codex home, include that environment setting.
- State whether the source remains and whether project files were copied.
- For a snapshot of the currently active chat, explain that messages after the
  snapshot, including the final transfer confirmation, are not included.
- Remove temporary bundles created for the transfer after verification. Keep
  recovery backups until success is confirmed, and report their locations.

Do not publish actual chat exports, database files, credentials, machine names,
or user paths as part of this skill or a public example.
