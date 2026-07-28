# WiseGen APE Omega v2.0

A local-first, model-agnostic and governance-first mission operating system. This release consolidates four working repositories into one interoperable control plane:

- Creative Engineering with MAMT safety
- Fundraising Mission Suite
- Presentation Intelligence Playbook
- Workspace-in-the-Loop
- Strategic Deliberation and Intent Assurance (SDIA)

The system does not claim certainty. It makes intent, assumptions, evidence, disagreement, authority and execution traceable.

## Execution lifecycle

```text
Request -> Mission registration -> Intent assurance -> Clarification gate
-> Evidence readiness -> Independent advisory council -> Cross-examination
-> Chair synthesis -> Captain's Gate -> Domain execution -> Verification
-> Release decision -> Witness Chain -> Retrospective
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
wisegen-omega validate examples/strategy_mission.yaml
wisegen-omega run examples/strategy_mission.yaml --output outputs/strategy_run.json
wisegen-omega inspect outputs/strategy_run.json
wisegen-omega verify-audit outputs/witness-chain.jsonl
```

## Safety posture

- External or irreversible actions are never executed by the deterministic reference runtime.
- High-impact ambiguity blocks execution.
- Assumptions are explicit, scored and recorded.
- Advisory reviews are isolated before cross-examination.
- The Chair recommends; the Captain authorises.
- All state transitions are fail-closed and hash-chained.

## Component preservation

Original component repositories are retained under `components/` for provenance and independent use. The root `wisegen_omega` package provides the converged orchestration spine.

See `docs/ARCHITECTURE.md`, `docs/OPERATING_HANDBOOK.md`, `docs/MIGRATION.md` and `docs/RELIABILITY_CLAIMS.md`.
