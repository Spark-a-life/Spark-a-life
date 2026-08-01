# WiseGen Workspace-in-the-Loop

A complete executable reference repo for **WiseGen APE Intelligence**: a governed cognitive operating system that makes organisational reasoning inspectable, repeatable, auditable, and improvable.

The core doctrine is simple:

> Do not govern only the final AI output. Govern the workspace that produces the decision.

This repo converts that doctrine into working infrastructure: evidence registers, workspace state, multi-lane deliberation, ranking intelligence, adversarial review, Captain's Gate, witness chain, outcome feedback, and reproducible CLI workflows.

## Why this exists

Most AI systems expose only:

```text
Prompt -> Output
```

WiseGen exposes:

```text
Goal -> Evidence -> Workspace -> Deliberation -> Ranking -> Risk Review -> Captain Gate -> Decision -> Witness Chain -> Retrospective Learning
```

This makes AI-assisted decisions more trustworthy because the decision has a passport even when the model does not.

## What is included

```text
wisegen_workspace_in_the_loop/
  wisegen_witl/             Python package
  configs/                  Evaluation criteria, lane registry, risk thresholds
  workflows/                JSON workflow definitions
  examples/                 Example decision inputs
  tests/                    Executable pytest suite
  docs/                     Architecture, doctrine, operations manual
  scripts/                  Smoke test and demo scripts
  audit/                    Witness chain output folder
  outputs/                  Decision reports output folder
```

## Quick start

```bash
cd wisegen_workspace_in_the_loop
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
wisegen-witl run --case examples/leadgen_case.json --workflow workflows/leadgen_workflow.json --out outputs/leadgen_decision.json
wisegen-witl audit --log audit/witness-chain.jsonl
```

No API key is required. The default implementation is deterministic and local-first. LLM adapters can be added later without changing the governance spine.

## Run tests

```bash
pip install pytest
pytest -q
```

## Core concepts

### Workspace-in-the-loop

Every significant decision produces a governed workspace state:

- objective
- constraints
- evidence
- assumptions
- hypotheses
- options
- criteria
- scores
- risks
- counterarguments
- decision rationale
- human gate status
- witness hash

### Captain's Gate

AI proposes. Human or delegated authority decides. High-impact or high-risk decisions cannot auto-execute.

### Witness Chain

Every run is written to an append-only JSONL witness chain with a deterministic hash. This supports audit, replay, and retrospective learning.

### Multi-lane deliberation

The default lanes are:

- Professor: evidence quality and conceptual rigour
- General: feasibility and execution
- CEO-Shadow: commercial viability
- Chief Librarian: provenance and traceability
- Red Team: abuse, gaming, and failure modes
- Captain: decision synthesis

## Example use cases

- LeadGen qualification and prioritisation
- AI video evaluation before release
- AI model and vendor selection
- policy review and governance assessment
- procurement ranking
- institutional risk review
- programme design and prioritisation

## Design principles

- model-agnostic
- local-first
- reproducible by default
- auditable by construction
- human-governed, not human-theatre
- explainable enough for institutional use
- extensible without vendor lock-in

## Repo status

This is a full reference implementation suitable for extension, pilot deployment, and conversion into a production-grade service.
