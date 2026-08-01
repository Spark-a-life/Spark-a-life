# WiseGen APE Intelligence OS + Omega

Canonical consolidated monorepo combining the WiseGen APE Intelligence OS governance control plane with the WiseGen APE Omega mission operating suite.

## Architectural contract

One OS, multiple estates, many runtimes, governed capabilities, and one accountable evidence model.

- `packages/intelligence-os`: constitutional controls, estate lanes, capability registry, Captain's Gate, runtime boundaries, and Witness Chain.
- `packages/omega`: mission lifecycle, intentionality analysis, evidence register, independent deliberation, Captain decision, execution planning, delivery, and retrospective.
- `scripts/run_governed_mission.py`: enforced integration path. It derives an OS action request from an Omega mission, requires an `ALLOW` decision from Captain's Gate, then executes Omega.

Neither package silently overrides the other. Intelligence OS governs authority and capability boundaries. Omega governs the mission lifecycle within those boundaries.

## Requirements

- Node.js 20 or later
- Python 3.10 or later
- GNU Make

## Run

```bash
make setup
make test
make demo
```

Expected demo outputs:

- `outputs/derived-action-request.json`
- `outputs/governed-mission.json`
- `outputs/omega-witness-chain.jsonl`

## Direct commands

```bash
cd packages/intelligence-os && npm test
.venv/bin/pytest -q packages/omega/tests
.venv/bin/python scripts/run_governed_mission.py examples/governed-strategy-mission.yaml
```

## Fail-closed behaviour

A mission is not passed to Omega unless Captain's Gate returns `ALLOW`. Missing or insufficient Captain approval produces a blocked result and a non-zero exit code.

## Repository status

This release preserves both original implementations and adds a deterministic integration boundary. External model providers, identity providers, secret stores, and remote execution runtimes remain outside the trusted default path and must be explicitly configured and governed before use.

## Licence

MIT. See package licences.
