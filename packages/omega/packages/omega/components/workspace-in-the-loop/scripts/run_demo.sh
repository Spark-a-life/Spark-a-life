#!/usr/bin/env bash
set -euo pipefail
python -m wisegen_witl.cli run --case examples/leadgen_case.json --workflow workflows/leadgen_workflow.json --out outputs/leadgen_decision.json
python -m wisegen_witl.cli run --case examples/media_os_case.json --workflow workflows/media_os_workflow.json --out outputs/media_os_decision.json
python -m wisegen_witl.cli audit --log audit/witness-chain.jsonl
