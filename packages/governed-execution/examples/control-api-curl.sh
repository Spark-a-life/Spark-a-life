#!/usr/bin/env bash
set -euo pipefail

API=${CONTROL_API_URL:-http://127.0.0.1:8787}
KEY=${CONTROL_API_KEY:-demo-control-api-key-rotate-before-use}

curl --fail --silent --show-error \
  -H "Authorization: Bearer ${KEY}" \
  -H "Content-Type: application/json" \
  --data @examples/note-create.json \
  "${API}/v1/execute" | python3 -m json.tool
