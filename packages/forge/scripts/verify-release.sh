#!/usr/bin/env bash
# The release gate. Every check must pass before a tag is considered releasable.
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
export PYTHONPATH=src
FAIL=0

check() {
  printf '%-46s' "$1"
  shift
  if "$@" >/tmp/forge-release-check.log 2>&1; then
    echo "PASS"
  else
    echo "FAIL"
    sed 's/^/    /' /tmp/forge-release-check.log | tail -15
    FAIL=1
  fi
}

echo "WiseGen Forge release gate"
echo "=========================="
check "environment and repository readiness"  "$PY" -m wisegen_forge.cli doctor
check "test suite"                            "$PY" -m unittest discover -s tests -t . 
check "reference demonstrator"                "$PY" -m wisegen_forge.cli demo
check "witness chain verification"            "$PY" -m wisegen_forge.cli verify --run .forge/demo
check "portable bundle export"                "$PY" -m wisegen_forge.cli export --run .forge/demo --out dist/portable-bundle.zip
check "no runtime dependencies declared"      grep -q '^dependencies = \[\]$' pyproject.toml
check "licence present"                       test -s LICENSE
check "changelog updated"                     test -s CHANGELOG.md

echo "=========================="
if [ "$FAIL" -eq 0 ]; then
  echo "RELEASE GATE: PASS. Captain sign-off still required before deployment."
else
  echo "RELEASE GATE: FAIL. Do not tag."
  exit 1
fi
