# Codex conversations

### Another folder on the same machine

Inspect `codex resume --help`. When supported:

```bash
codex resume <SESSION_ID> --cd /absolute/destination/project
```

`codex resume --all` finds sessions across folders. This reuses the existing
session; it does not create an independent copy or transfer project files.
Use this route when the request is to continue the existing session elsewhere.
If an independent copy is requested, use a separate destination Codex home and
follow the storage procedure below. Resolve that home's path from context or ask
if needed; do not silently reuse the original. Duplicating within one Codex home
requires a verified application-supported fork operation. Do not invent a new ID
by editing the transcript or database rows.

### Another computer or Codex home

Read [the Codex storage procedure](storage-transfer.md) before copying.
Resolve `CODEX_HOME` independently on each machine, defaulting to `~/.codex`.
The procedure covers thread metadata, transcripts, paginated history, schema
compatibility, destination path mapping, collision handling, and recovery.
A transcript-only copy is not assumed sufficient for paginated sessions.

Preserve transcript bytes when history projections contain byte offsets. Map the
thread's destination paths and resume with an explicit working directory instead
of rewriting historical transcript paths and invalidating the projections.

Verify the imported records and provide the explicit `codex resume` command.
Include the destination `CODEX_HOME` setting when it is nondefault.
