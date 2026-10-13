#!/usr/bin/env bash
# Policy-aware shared HTML source lint. Exit 2 means the check did not run.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/html_lint.py" "$@"
