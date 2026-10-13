#!/usr/bin/env bash
# Shared validated artifact I/O; use --help for flags. Python 3 and curl required.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/artifact_io.py" create "$@"
