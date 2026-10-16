# Transferring Codex local conversation storage

## Compatibility and discovery

Codex's storage is an implementation detail. This procedure was derived from a
transfer between CLI versions 0.155.1 and 0.154.0 with `paginated` history. The
stored records and transcript were verified; interactive resume was not tested.
Do not interpret that observation as a compatibility guarantee for other builds.

Inspect both installations before writing:

1. Resolve the Codex home, CLI version, `resume --help`, destination workspace,
   and relevant database files. Do not print authentication files or unrelated
   conversation contents.
2. Open source SQLite databases read-only, for example with Python's
   `sqlite3.connect("file:" + path + "?mode=ro", uri=True)`. Inspect table definitions
   in `sqlite_master` and columns using `PRAGMA table_info`.
3. Resolve the chosen session in the thread table and inspect its `rollout_path`,
   `cwd`, `history_mode`, version, and identifiers. Verify that the transcript's
   opening session metadata identifies the same conversation.
4. Inspect destination schemas and check for existing records or transcript paths
   belonging to that session ID. Stop before writing if a collision exists. Do not
   silently overwrite, merge histories, or create a new ID by changing one field.

Observed storage pieces:

| Piece | Observed location or table | Treatment |
| --- | --- | --- |
| Conversation transcript | `sessions/YYYY/MM/DD/rollout-*.jsonl` | Copy the selected transcript; follow the recorded path rather than guessing its filename. |
| Archived transcript | `archived_sessions/` | Inspect archived state and agree whether to restore as archived or active. |
| Thread metadata | `state_5.sqlite`, `threads` | Copy the selected row, adapting destination paths and optional local UI associations. |
| Per-thread dynamic tool declarations | `thread_dynamic_tools` | Inspect and preserve selected-thread records when present; declarations do not install their tools. |
| Paginated history | `thread_history_1.sqlite` | Preserve selected-thread rows in the tables below. |

Observed paginated history tables:

- `thread_turns`
- `thread_items`
- `thread_history_projection_state`
- `thread_realtime_items`

Filter these tables by `thread_id`. Projection state stores byte offsets and
ordinals into the transcript, so a transcript-only copy is not assumed sufficient.
Do not import `_sqlx_migrations` from the source into the destination.

Inspect other thread-linked tables and references in the installed version.
Parent/child agent relationships, artifacts, or future storage modes may require
additional records. Do not recursively transfer other chats without authorization.
If required data or schema meaning is unclear, stop and explain the specific gap
rather than dropping it. Do not change `history_mode` to bypass a missing database.

## Capture a snapshot

Prefer a completed, idle source conversation and an idle destination Codex
process. If transferring the active conversation, clearly identify the result as
a point-in-time snapshot. Do not claim a clean turn boundary when one was not
observed, or forge completed status for an active turn.

Use SQLite transactions or its backup API to obtain consistent database reads;
copying a live `.sqlite` file without accounting for its WAL can lose data.
Do not copy live database files and sidecars over destination databases.

For an append-only active transcript:

1. Capture the selected history records within a read transaction, then read the
   transcript. Keep only complete newline-terminated JSONL records.
2. Verify that all projection offsets and recorded turn offsets fit within the
   captured transcript. Check that offsets fall on record boundaries and ordinals
   are consistent with the captured records using the installed format.
3. Check that the source transcript was not replaced or truncated during capture.
   If the records cannot be reconciled, discard the snapshot and retry once; if
   still inconsistent, request an idle source before proceeding.

Separate databases do not automatically share a snapshot transaction. Validate
cross-database thread and turn references. Unresolved inconsistencies are a reason
to stop, not to copy a larger portion of the user's Codex home.

Keep transcript bytes unchanged. Rewriting old paths inside JSONL shifts byte
offsets and can invalidate paginated history. Update the destination thread's
`cwd` and `rollout_path`, and use `resume --cd` for the new workspace. Old paths
may remain in historical messages and session metadata; tell the resumed agent
the new workspace root. If a version requires transcript rewriting, use a verified
version-specific projection rebuild or stop rather than retaining stale offsets.

Stage only the chosen transcript and required records in a private temporary
directory with restrictive permissions. Record their sizes, counts, and a SHA-256
digest. Bundles contain conversation data: never place them in a public project.
Exclude `auth.json`, credentials, shell snapshots, global settings, unrelated
memory, and other conversations. Authenticate separately on the destination.

## Import without replacing existing history

Use SSH with properly quoted arguments or another user-authorized transport.
Pass structured data through stdin or private files instead of interpolating chat
text, host names, or file paths into executable shell strings. A destination SSH
alias can be used directly; do not weaken SSH configuration to bypass errors.

Before mutation, validate every row and schema mapping:

- Preserve IDs and relational references within the selected conversation.
- Map the transcript path into the destination Codex home and `cwd` to the chosen
  workspace. Validate paths stay within the intended destination locations.
- Preserve required source columns. A missing destination column is not safe to
  discard merely because its value is empty, zero, or null; inspect its meaning.
- Confirm required destination columns have supplied values or valid defaults.
- Clear optional source-machine UI associations, such as project or section IDs,
  only when nullable and semantically safe, or map them to verified destination
  records. Do not import dangling references to source-only projects.
- Preserve destination schema versions. If unsupported, explain whether a
  compatible Codex installation is needed; do not silently upgrade the user's CLI.

Back up destination databases consistently using SQLite's backup API before
writing. Use parameterized SQL and insert-only operations inside transactions;
avoid `INSERT OR REPLACE`. Acquire the write transaction and recheck collisions
before importing. Use schema-derived, validated identifiers for dynamic SQL.

Stage the transcript and install it with exclusive creation so an existing file
cannot be replaced. Insert just the selected rows. Check foreign-key integrity
where the schema declares it, and logical relationships where it does not.

A transaction using attached SQLite databases is not necessarily crash-atomic
across files in WAL mode, and no SQLite transaction covers the transcript file.
Keep a recovery record of the newly inserted keys and created file. If an import
partially fails, report the state and remove only records/files proven to belong
to this attempt. Restore whole-database backups only when no intervening writes
would be lost. Do not automatically repeat a partially completed import.

## Verify and hand off

Reopen destination storage read-only and verify:

- The selected thread is present once, with the intended workspace, transcript
  path, archive state, and history mode.
- The transcript's size and SHA-256 digest match the captured source snapshot,
  and every JSONL record parses.
- Selected-thread record counts and contents match the export after intentional
  path/UI association changes; paginated offsets remain valid.
- The destination workspace exists and requested project files are available.

Use explicit-session resume as the primary handoff:

```bash
codex resume <SESSION_ID> --cd /absolute/destination/project
```

For a custom home, supply its destination value through `CODEX_HOME`. If the chat
does not appear in a picker, try the explicit ID and inspect the installed
version's indexing behavior; do not fabricate global index entries from memory.
Refreshing an app may be needed, but GUI discovery is not proven by a database
check. Report whether interactive resume was actually tested.

Remove transfer-only temporary data after verification. Retain the source unless
deletion was explicitly requested and successful continuation confirmed. Prefer
trash for user files; never delete a shared Codex database to remove one chat.
