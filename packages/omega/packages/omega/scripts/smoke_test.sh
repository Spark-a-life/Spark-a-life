#!/usr/bin/env bash
set -euo pipefail
python -m pytest -q
python -m wisegen_omega.cli validate examples/strategy_mission.yaml
python -m wisegen_omega.cli run examples/strategy_mission.yaml --output outputs/strategy_run.json
python -m wisegen_omega.cli verify-audit outputs/witness-chain.jsonl
