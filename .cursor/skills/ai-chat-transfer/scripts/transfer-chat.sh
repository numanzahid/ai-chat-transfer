#!/usr/bin/env bash
# Transfers Claude Code chat session file(s) between project folders,
# locally or over SSH, preserving the ~/.claude/projects/<slug> layout
# Claude Code expects so the session can be resumed at the destination.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  transfer-chat.sh --to-path REMOTE_OR_LOCAL_ABS_PATH [--to-host HOST] [--from-path LOCAL_ABS_PATH] [--session ID]...

Options:
  --to-host HOST     SSH alias/host to transfer to (omit for a local folder-to-folder transfer)
  --to-path PATH     Absolute path of the destination project folder (the cwd Claude Code
                      was/would be run from at the destination) - NOT the .claude/projects slug
  --from-path PATH   Absolute path of the source project folder (default: $PWD)
  --session ID       Session id to transfer (repeatable). Default: current session
                      ($CLAUDE_CODE_SESSION_ID) or, if unset, every session in the source project dir
  -h, --help         Show this help
EOF
}

slug() { # abs path -> claude project dir slug
  local p="$1"
  printf '%s' "${p//\//-}"
}

HOST=""
TO_PATH=""
FROM_PATH="$PWD"
SESSIONS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --to-host) HOST="$2"; shift 2 ;;
    --to-path) TO_PATH="$2"; shift 2 ;;
    --from-path) FROM_PATH="$2"; shift 2 ;;
    --session) SESSIONS+=("$2"); shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -n "$TO_PATH" ]] || { echo "--to-path is required" >&2; usage; exit 1; }

FROM_SLUG=$(slug "$FROM_PATH")
TO_SLUG=$(slug "$TO_PATH")
SRC_DIR="$HOME/.claude/projects/$FROM_SLUG"

[[ -d "$SRC_DIR" ]] || { echo "Source project dir not found: $SRC_DIR" >&2; exit 1; }

if [[ ${#SESSIONS[@]} -eq 0 ]]; then
  if [[ -n "${CLAUDE_CODE_SESSION_ID:-}" && -f "$SRC_DIR/$CLAUDE_CODE_SESSION_ID.jsonl" ]]; then
    SESSIONS=("$CLAUDE_CODE_SESSION_ID")
  else
    while IFS= read -r f; do
      SESSIONS+=("$(basename "$f" .jsonl)")
    done < <(find "$SRC_DIR" -maxdepth 1 -name '*.jsonl')
  fi
fi

[[ ${#SESSIONS[@]} -gt 0 ]] || { echo "No session files found to transfer in $SRC_DIR" >&2; exit 1; }

if [[ -n "$HOST" ]]; then
  ssh "$HOST" "mkdir -p -m 700 ~/.claude/projects/$TO_SLUG"
  for sid in "${SESSIONS[@]}"; do
    f="$SRC_DIR/$sid.jsonl"
    [[ -f "$f" ]] || { echo "Missing session file: $f" >&2; exit 1; }
    scp -p "$f" "$HOST:~/.claude/projects/$TO_SLUG/"
  done
  echo "Transferred ${#SESSIONS[@]} session(s) to $HOST:~/.claude/projects/$TO_SLUG/"
  ssh "$HOST" "ls -la ~/.claude/projects/$TO_SLUG/"
else
  DEST_DIR="$HOME/.claude/projects/$TO_SLUG"
  mkdir -p -m 700 "$DEST_DIR"
  for sid in "${SESSIONS[@]}"; do
    f="$SRC_DIR/$sid.jsonl"
    [[ -f "$f" ]] || { echo "Missing session file: $f" >&2; exit 1; }
    cp -p "$f" "$DEST_DIR/"
  done
  echo "Transferred ${#SESSIONS[@]} session(s) to $DEST_DIR"
  ls -la "$DEST_DIR"
fi
