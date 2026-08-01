# Architecture

## Runtime pipeline

```text
CaseInput
  -> EvidenceRegister
  -> WorkspaceState
  -> LaneDeliberation
  -> RankingEngine
  -> RiskEngine
  -> CaptainGate
  -> DecisionReport
  -> WitnessChain
```

## Package modules

- `core.models`: dataclasses for workspace state, evidence, options, scores, and decisions
- `core.engine`: orchestration runtime
- `core.ranking`: weighted multi-criteria ranking
- `core.risk`: risk and gate logic
- `core.witness`: deterministic hashing and append-only witness logs
- `lanes.default_lanes`: deterministic lane deliberators
- `storage.json_store`: JSON IO utilities
- `adapters.local_adapter`: local deterministic reasoning adapter
- `cli`: executable command line interface

## Interoperability

The repo uses JSON for inputs, workflows, and outputs. This makes it compatible with:

- Python services
- Node/Express APIs
- GitHub Actions
- Trigger.dev style scheduled workflows
- database-backed audit stores
- spreadsheet import/export
- LLM providers through future adapters

## Reproducibility

All default scoring is deterministic. The same case plus same workflow produces the same ranking and witness hash unless the workflow version changes.
