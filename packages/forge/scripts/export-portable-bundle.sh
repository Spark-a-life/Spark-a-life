#!/usr/bin/env bash
# Craft the portable ownership bundle and prove it operates without WiseGen Forge.
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
export PYTHONPATH=src
RUN="${1:-.forge/demo}"
OUT="${2:-dist/portable-bundle.zip}"

[ -d "$RUN" ] || { echo "No run at $RUN. Run 'make demo' first." >&2; exit 1; }
mkdir -p "$(dirname "$OUT")"
"$PY" -m wisegen_forge.cli export --run "$RUN" --out "$OUT"

echo
echo "Exit test: unpacking the bundle outside the repository"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"$PY" -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$OUT" "$TMP"
echo "Bundle contents:"
find "$TMP" -maxdepth 2 -type f | sed "s|$TMP/|  |" | head -30
echo
echo "The bundle is the customer's. It carries source, schema, tests, manifests, policies and evidence."
