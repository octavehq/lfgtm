#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 scripts/validate_package.py
python3 -m unittest discover -s tests
python3 -m unittest discover -s skills/get-brand-components/tests
for script in scripts/*.sh skills/asset-manager/scripts/*.sh skills/get-brand-components/scripts/*.sh skills/shared/scripts/*.sh; do
  bash -n "$script"
done
bash scripts/build-codex.sh
bash scripts/build-cursor.sh
python3 scripts/validate_package.py build/codex
python3 scripts/validate_package.py build/cursor
