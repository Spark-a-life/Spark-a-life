#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src ${PYTHON:-python3} -m wisegen_forge.cli doctor "$@"
