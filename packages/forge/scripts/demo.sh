#!/usr/bin/env bash
# Reference demonstrator: Governed Spreadsheet-to-Application Factory.
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
export PYTHONPATH=src
"$PY" -m wisegen_forge.cli demo "$@"
echo
echo "Verifying the witness chain"
"$PY" -m wisegen_forge.cli verify --run .forge/demo
echo
echo "Gate packet:"
"$PY" -m wisegen_forge.cli gate --run .forge/demo | head -40
