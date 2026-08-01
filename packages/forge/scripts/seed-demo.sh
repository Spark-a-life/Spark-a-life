#!/usr/bin/env bash
# Seed a fresh working copy of the demonstrator inputs into a scratch directory.
set -euo pipefail
cd "$(dirname "$0")/.."
DEST="${1:-.forge/seed}"
mkdir -p "$DEST"
cp -r examples/employee-onboarding/* "$DEST"/
echo "Seeded demonstrator inputs into $DEST"
ls -1 "$DEST"
