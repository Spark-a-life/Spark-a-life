#!/usr/bin/env bash
# WiseGen Forge bootstrap. Performs no network calls and installs nothing by default.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "WiseGen Forge bootstrap"
echo "-----------------------"

PY="${PYTHON:-python3}"
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "FAIL: python3 not found. Install Python 3.10 or later." >&2
  exit 1
fi

VER=$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
echo "python      : $VER"
"$PY" - <<'PY'
import sys
if sys.version_info < (3, 10):
    sys.exit("FAIL: Python 3.10 or later is required")
PY

[ -f .env ] || { cp .env.example .env; echo "config      : .env crafted from .env.example"; }
mkdir -p .forge dist
echo "run root    : .forge"

echo "core import :"
PYTHONPATH=src "$PY" -c "import wisegen_forge; print('  wisegen_forge', wisegen_forge.__version__)"

echo
echo "Bootstrap complete. Next: ./scripts/doctor.sh then make demo"
