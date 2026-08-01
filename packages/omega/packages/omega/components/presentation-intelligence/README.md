# WiseGen Presentation Intelligence Playbook

A governance-first, model-agnostic pipeline for transforming raw intent, evidence and constraints into decision-ready artefacts.

## Lifecycle

`Intent -> Audience -> Knowledge -> Reasoning -> Planning -> Generation -> Composition -> Verification -> Governance -> Publication`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
wisegen-pip validate examples/executive-brief/project.yaml
wisegen-pip run examples/executive-brief/project.yaml
pytest -q
```

Generated files are written to `build/<project-id>/`.

## Outputs

- `artefact.md`
- `quality-report.json`
- `witness-record.json`
- `release-manifest.json`

## Design stance

Prompts are versioned production components. The governed workflow is the product.

## Licence

Apache-2.0.
