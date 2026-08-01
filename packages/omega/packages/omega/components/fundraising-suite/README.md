# WiseGen MAMT Fundraising Suite v1.5

A local-first, model-agnostic fundraising mission-team reference implementation for Spark-a-life | APE Intelligence.

v1.5 upgrades the v1.2 convergence repo into a more client-shippable suite. It keeps fundraising, safeguards, creative generation, evidence integrity, donor due diligence, release preflight and witness-chain audit inside one governed MAMT architecture.

## Product framing

```text
WiseGen / APE Intelligence
  -> MAMT: Model-Agnostic Mission Teams
    -> Superpower AI Teams
      -> Fundraising Mission Team
        -> Governance Profile
        -> Safeguard Layer
        -> Creative Layer
        -> Donor Due Diligence
        -> Evidence Layer
        -> Model Router
        -> Captain Gate
        -> Witness Chain
        -> Release Preflight
```

The repository is deliberately local-first. It performs deterministic execution without external model calls. Manual and future adapter surfaces are represented as auditable adapter contracts, not hidden automation claims.

## What is included

- Fundraising Mission Team roles: Captain, Sourcer, Enricher, Narrative Architect, Memo Writer, Financial Analyst, Compliance Reviewer, Outreacher, Data Room Curator, Tracker, Creative Director, Safeguard Governor, Evidence Librarian and QA Evaluator.
- Fundraising workflow: mission admission, prospect scoring, enrichment, memo generation, outreach drafting, data-room mapping, donor due diligence, compliance review, creative pack generation, evaluation and Captain Gate decision.
- Safeguards: runtime budget, loop detection, circuit breaker, approval gate, claim-to-evidence checking, prompt-injection scanning, data-egress discipline and credential-scoped tool access.
- Creative engineering: narrative pack, outreach variants, LinkedIn post draft, visual prompt pack and channel-specific messaging discipline.
- Model-agnostic routing: task-to-model-class selection with rationale and external-call policy.
- Witness Chain: append-only JSONL audit with digest chaining and verification command.
- Release controls: preflight report and release manifest with SHA-256 file hashes.
- Master Super Prompt generator: Route A local zip scaffolding prompt and Route B no-zip text-to-workspace prompt with chunking and expert review checkpoints.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
ruff check .
wg-fund validate examples/missions/fundraising_500k_programme.yaml
wg-fund run examples/missions/fundraising_500k_programme.yaml --output outputs/fundraising_run.json
wg-fund inspect outputs/fundraising_run.json
wg-fund review examples/missions/fundraising_500k_programme.yaml
wg-fund verify-audit outputs/witness_chain.jsonl
wg-fund preflight --output outputs/preflight.json
wg-fund manifest --output outputs/release_manifest.json
wg-fund prompt --project-name wisegen-mamt-fundraising-suite --route zip > outputs/master_prompt_route_a.md
wg-fund prompt --project-name wisegen-mamt-fundraising-suite --route no-zip > outputs/master_prompt_route_b.md
python scripts/export_repo_zip.py --output outputs/wisegen-mamt-fundraising-suite-v1.5.zip
```

## Repository map

```text
configs/                         Mission roles, safety, routing, creative and safeguard rules
contracts/                       JSON Schemas for fundraising missions and evidence records
docs/                            Architecture, playbooks, safeguards, standards map and release notes
examples/missions/               Executable local-first mission contracts
scripts/                         Local export and verification helpers
src/wisegen_mamt_fundraising/    Python implementation
tests/                           Unit and integration tests
outputs/                         Generated local artefacts
```

## Core execution path

```text
Mission Contract
  -> Contract Validator
  -> Mission Admission
  -> Governance Profile Review
  -> Fundraising Mission Team Planner
  -> Runtime Governor
  -> Credential Broker
  -> Model Router
  -> Fundraising Workflow
  -> Donor Due Diligence
  -> Safeguard Review
  -> Creative Pack Generation
  -> Evaluation
  -> Captain Gate
  -> Witness Chain
  -> Release Preflight
```

## Design stance

This is not a chatbot wrapper and not a single-provider fundraising assistant. It is a governed mission-team operating pattern where roles, contracts, permissions and evidence remain stable while models can be swapped underneath.

No outbound outreach, CRM write, data-room release or funder-facing claim is approved by default. The system generates reviewable artefacts and keeps external egress behind Captain Gate.
