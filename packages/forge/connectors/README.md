# Connectors

Every external system is mediated through a connector contract. No direct calls, no unlogged side effects, no credential in the artefact.

Version 1 ships the contract and one reference stub rather than a catalogue. A connector earns its place when a customer asks for it, per `docs/decision-records/ADR-0006-scope-boundary.md`.

## The contract

```yaml
id: connector.<system>
version: 1.0.0
network: true                 # anything true here is denied unless policy allows it
credentials:
  source: environment         # never a file in the repository, never an artefact
  names: [SYSTEM_API_TOKEN]
capabilities:
  - read_records
  - write_records
classification_ceiling: internal   # the highest classification this connector may carry
evidence:
  - request digest, never the payload
  - response status and shape, never the body
```

`classification_ceiling` is the important field. A connector approved for internal data must not become the path by which restricted data leaves the boundary, and the ceiling is checked before the call, not after.
