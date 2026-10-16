#!/usr/bin/env bash
# Compatibility entrypoint for the Claude Code transcript-copy helper.
set -euo pipefail
exec python3 "$(dirname -- "${BASH_SOURCE[0]}")/transfer-chat.py" "$@"
