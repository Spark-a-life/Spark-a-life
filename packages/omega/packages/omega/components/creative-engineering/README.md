# WiseGen Creative Engineering Framework v1.1

A delivery-ready reference implementation for Creative Engineering with Model-Agnostic Mission Teams (MAMT), runtime safety, credential isolation, model routing, evaluation and witness-chain audit.

This repository treats creative work as an engineered system, not as a collection of prompts. It compiles a structured creative mission into role-based work packages, applies deterministic safety controls, routes to model adapters, evaluates results, and records an auditable execution trace.

## What this version adds

- **MAMT as the organising architecture**: each mission is executed by a governed team of role agents.
- **Operational safety by design**: risk budgets, loop detection, circuit breaker states and deterministic termination.
- **Credential isolation**: agents receive scoped capability tokens, never raw credentials.
- **Creative contracts**: YAML briefs are validated before execution.
- **Model-agnostic adapters**: manual Muse bridge, local deterministic adapter, and extension points for OpenAI, Gemini, Veo, Seedance, Kling, Higgsfield and Flux.
- **Witness Chain**: append-only JSONL audit events with digest chaining.
- **Executable CLI**: validate, compile, run, evaluate and inspect missions.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
pytest
wcef validate examples/briefs/linkedin_social_creative.yaml
wcef run examples/briefs/linkedin_social_creative.yaml --output outputs/run.json
wcef inspect outputs/run.json
```

## Repository map

```text
configs/                         Runtime, MAMT and model configuration
contracts/                       JSON Schemas for mission, role, tool and evaluation contracts
docs/                            Operating handbook, architecture, governance and safety notes
examples/briefs/                 Complete executable mission briefs
src/wisegen_creative_engineering/ Python implementation
tests/                           Unit and integration tests
outputs/                         Generated run artefacts, git-ignored except .gitkeep
```

## Core execution path

```text
Mission Brief
  -> Contract Validator
  -> Mission Admission
  -> MAMT Planner
  -> Runtime Governor
  -> Credential Broker
  -> Model Router
  -> Adapter Execution
  -> Evaluation
  -> Captain's Gate
  -> Witness Chain
```

## Muse integration posture

Meta Muse is handled through a **manual bridge** because a stable public Muse API is not assumed. The adapter generates an operational prompt pack for Meta AI, Instagram or WhatsApp workflows, records required paste-back fields and evaluates returned artefacts once provided. When a public API becomes available, only the adapter must change. The mission contract, evaluator, MAMT layer and witness chain remain stable.

## No hidden automation claim

This repository does not pretend to automate systems without an available public API. Manual adapters are explicit, auditable and testable. That keeps the framework honest and deployable.
