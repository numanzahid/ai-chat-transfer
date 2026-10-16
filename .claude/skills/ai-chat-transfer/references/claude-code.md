# Claude Code conversations

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

The bundled `scripts/transfer-chat.sh` invokes a Python 3 helper for main
transcripts. Verify that slash-only workspace encoding matches both installations
before using it, even for paths it can safely transport. It requires explicit
`--session` selection, checks the entire batch before writing, and installs files
with atomic collision protection. Existing files and symlinks cause failure.
Paths and chat data travel over SSH as JSON on stdin, not executable shell text.
Python 3 is required locally and, for SSH transfers, on the destination.

Use `--source-config-dir` and `--destination-config-dir` for independently resolved
nondefault Claude config directories; both default to that machine's `~/.claude`.
Supply normalized absolute POSIX paths and quote shell arguments. The helper
validates complete JSONL records and SHA-256 hashes but copies main transcripts
only. Handle required companions and destination workspace creation separately.
Prefer idle sources; successful capture is a snapshot, not continuous sync.
If a batch fails after writing begins, inspect the reported created files before
retrying. The helper retains them and never replaces existing destination files.

Run the helper relative to this skill's directory when those conditions hold:

```bash
bash scripts/transfer-chat.sh --from-path /absolute/source/project --to-path /absolute/destination/project --to-host HOST --session SESSION_ID
```

Omit `--to-host` for a local transfer. Project memory is separate; include it only
when requested and scoped to the destination project.
