#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e '.[dev]'
pytest
ruff check .
wg-fund validate examples/missions/fundraising_500k_programme.yaml
wg-fund run examples/missions/fundraising_500k_programme.yaml --output outputs/fundraising_run.json
wg-fund inspect outputs/fundraising_run.json
wg-fund verify-audit outputs/witness_chain.jsonl
wg-fund preflight --output outputs/preflight.json
wg-fund manifest --output outputs/release_manifest.json
