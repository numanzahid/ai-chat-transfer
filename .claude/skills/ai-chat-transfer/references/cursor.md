# Cursor conversations

Identify the Cursor client that owns the chat (CLI or editor), its version, and
its actual storage before selecting a procedure. Do not assume that editor and
CLI histories share a layout or discovery mechanism. For installations with the
following observed layout:

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
