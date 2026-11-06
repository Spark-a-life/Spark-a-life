# Portfolio evaluation and portable architecture pack

**Status:** Docs-only. Evaluation snapshot. Not a runtime. Not production.  
**Version:** 1.0.0-eval  
**Date:** 5 November 2026  
**Branch:** `cursor/portfolio-eval-architecture-8465`  
**Base:** `cursor/aios-v1-2-alpha-repo-8465` (AIOS v1.2.0-alpha governance snapshot)

## Do not merge this branch to profile `main`

`main` currently holds the GitHub profile README for `spark-a-life/spark-a-life`.  
The AIOS v1.2 snapshot already lives at repository root on the parent branch. Merging either this branch or the parent AIOS branch to `main` would replace that profile README. Do not merge unless that replacement is intended.

This pack lives under `portfolio/` so that `governance/AIOS_v1.2.md` remains the canonical AIOS specification. Nothing here silently supersedes AIOS.

## What this pack is

A four-artefact review plus a small kernel of shared contracts, plus a Human Captain coordination plan. The four artefacts are sibling practice materials, not one product:

| Artefact | What it actually is | Publish posture |
| --- | --- | --- |
| `claude_sensemaking_meta_prompt.md` | A review prompt for the VFX manual | Private prompt. Not an engine. |
| `vfx_ai_pipeline_integration_manual.md` | A design sketch with inlined sample code | Private design notes. Not a pipeline. |
| Salwise Local AI Productivity PaP2 v1.2 | A reviewed local-execution brief with mechanical package checks | Private-repo-ready execution candidate. Runtime `NOT_ASSESSED`. |
| Adaptive Learning Tutor v1.0 | A Cursor skill pack with markdown acceptance tests | Skill drop. Behaviour `NOT_RUN`. |

## What this pack is not

- Not a unified platform.
- Not an Action Gateway.
- Not evidence that any model, GPU cluster, Nuke tree, or tutor session was run.
- Not a reason to weaken or rewrite AIOS v1.2.

## Layout

```text
portfolio/
  README.md                 This file
  LICENSE                   All Rights Reserved
  EVALUATION.md             Verdicts, evidence, blockers, sequenced actions
  INTEROP.md                Kernel, adapters, data classes, trust boundaries
  PLAN.md                   Coordination plan a Human Captain can execute
  JOURNEY.md                Sequenced path from current disk/PR state to plan lock
  FILE_INVENTORY.json       sha256 of tracked pack files
  kernel/                   Shared vocabulary and JSON Schema envelopes
  artifacts/salwise-local-ai-pap2-v1.2/     Vendored package + STATUS
  artifacts/adaptive-learning-tutor-v1.0/   Vendored skill + STATUS
  artifacts/vfx-ai-pipeline-manual/         Index and defects only; source not copied
  artifacts/claude-sensemaking-meta-prompt/ Prompt + STATUS
  verify_portfolio_pack.py  Repeatable verification
```

## How to re-run the evaluation

From this directory:

```text
python3 verify_portfolio_pack.py
python3 artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py
```

The Salwise checker confirms frozen document consistency. It does not prove LM Studio, model behaviour, or human benefit. The pack verifier confirms inventories, JSON parse, schema parse, declared path existence, and the absence of high-risk secret patterns in committed files.

## Authority

The Human Captain retains decision rights. This pack confers none. Possession of sample code or a prompt is not authority to execute it.

## Licence

All rights reserved. See `LICENSE`.
