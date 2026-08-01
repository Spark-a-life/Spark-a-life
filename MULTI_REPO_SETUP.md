# Multi-Repo Setup Guide

This document describes how to split the staged `packages/` directory into independent GitHub repositories under the Spark-a-life organisation.

## Prerequisites

- GitHub CLI (`gh`) authenticated with org admin rights
- Git configured with your identity

## Step 1: Create the repositories

```bash
# Core
gh repo create Spark-a-life/wisegen-forge --public --description "Governed intent-to-system application factory" --license MIT
gh repo create Spark-a-life/wisegen-ape-intelligence-os --public --description "Governance-native operating architecture for human-AI intelligence systems" --license MIT
gh repo create Spark-a-life/wisegen-ape-omega --public --description "Governance-first, model-agnostic mission operating system" --license MIT

# Execution and routing
gh repo create Spark-a-life/wisegen-governed-execution --public --description "Local-first governed execution control plane for enterprise AI agents" --license MIT
gh repo create Spark-a-life/wisegen-routing-harness --public --description "Governed multi-model routing benchmark and certification harness" --license Apache-2.0

# Domain overlays
gh repo create Spark-a-life/wisegen-maie-hrbp --public --description "MAIE capability overlay for HRBP demand intelligence" --license Apache-2.0
gh repo create Spark-a-life/wisegen-caf-os --public --description "Governance-first conversational AI filmmaking operating system" --license MIT
```

## Step 2: Push each module

```bash
#!/usr/bin/env bash
set -euo pipefail

MODULES=(
  "forge:wisegen-forge"
  "omega:wisegen-ape-omega"
  "ape-intelligence-os:wisegen-ape-intelligence-os"
  "governed-execution:wisegen-governed-execution"
  "routing-harness:wisegen-routing-harness"
  "maie-hrbp:wisegen-maie-hrbp"
  "caf-os:wisegen-caf-os"
)

for entry in "${MODULES[@]}"; do
  LOCAL="${entry%%:*}"
  REMOTE="${entry##*:}"
  echo "=== Pushing $LOCAL → Spark-a-life/$REMOTE ==="

  cd "packages/$LOCAL"
  git init
  git add .
  git commit -m "Initial commit — $(jq -r '.name // empty' package.json 2>/dev/null || python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml","rb"))["project"]["name"])' 2>/dev/null || echo "$REMOTE")"
  git branch -M main
  git remote add origin "https://github.com/Spark-a-life/$REMOTE.git"
  git push -u origin main
  cd ../..
done
```

## Step 3: Claim the npm scope

```bash
# One-time: create the @spark-a-life npm organisation (free for public packages)
npm login
npm org create spark-a-life
```

## Step 4: Configure PyPI Trusted Publishing

For each Python module (`wisegen-forge`, `wisegen-ape-omega`):

1. Go to [pypi.org/manage/account/publishing](https://pypi.org/manage/account/publishing/)
2. Add a new pending publisher:
   - **PyPI project name:** `wisegen-forge` (or `wisegen-ape-omega`)
   - **Owner:** `Spark-a-life`
   - **Repository:** `wisegen-forge` (or `wisegen-ape-omega`)
   - **Workflow name:** `publish-pypi.yml`
   - **Environment:** `release`
3. Copy the `publish-pypi.yml` workflow from `.github/workflows/` in this repo into the new repo's `.github/workflows/`

## Step 5: Configure GitHub Pages

After merging this branch to `main`:

1. Go to the repo Settings → Pages
2. Source: **GitHub Actions**
3. The `pages.yml` workflow will deploy `docs/` automatically on push to `main`
4. Optionally add a custom domain via a `CNAME` file in `docs/`

## Step 6: Enable Sigstore releases

For each module repo:

1. Copy `release-with-provenance.yml` from `.github/workflows/` to the new repo
2. Create a `release` environment in the repo Settings → Environments
3. Optionally add required reviewers to the `release` environment (Captain's Gate for releases)

## Repository Map

After splitting, the Spark-a-life org will contain:

```
Spark-a-life/
├── Spark-a-life                    ← This repo (profile README + docs + GitHub Pages)
├── wisegen-forge                   ← Python — application factory
├── wisegen-ape-intelligence-os     ← Node — core OS
├── wisegen-ape-omega               ← Python — mission engine
├── wisegen-governed-execution      ← Node — execution control plane
├── wisegen-routing-harness         ← Node — model benchmarking
├── wisegen-maie-hrbp               ← Node — HR overlay
└── wisegen-caf-os                  ← Node — filmmaking overlay
```

## After Splitting

Once modules are in their own repos, remove the `packages/` directory from this repo:

```bash
git rm -r packages/
git commit -m "Remove staged packages — now in individual repos"
git push
```

Update the README.md links to point to the individual repos instead of `packages/` directories.
