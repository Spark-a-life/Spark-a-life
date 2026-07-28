# WiseGen Forge

**Governed Intent-to-System Application Factory**

Convert human intent, documents, spreadsheets and existing processes into tested, governed, deployable and maintainable digital capabilities, with an evidence trail that survives the removal of this platform.

WiseGen Forge is not a coding-agent collection. It is an application factory with a constitution: the Captain Rule (AI proposes, the human decides) is enforced in code, not in prose.

---

## Status

| Property | Position |
|---|---|
| Version | 1.0.0 |
| Runtime dependencies | None. Python 3.10+ standard library only |
| Network required | No. The default model adapter is deterministic and offline |
| Estates supported | Local workstation, Docker, Kubernetes, customer VPC, air-gapped |
| Governance | Captain's Gate, Witness Chain, policy-as-code, cost governor |
| Portability | `forge export` produces a bundle that runs without WiseGen Forge |

---

## Quickstart

```bash
git clone <your-remote> wisegen-forge && cd wisegen-forge
./scripts/bootstrap.sh          # no network calls, no installs required
./scripts/doctor.sh             # environment and repository readiness
make demo                       # reference Spreadsheet-to-Application run
make test                       # full test suite
```

Or without the Makefile:

```bash
PYTHONPATH=src python3 -m wisegen_forge.cli demo
PYTHONPATH=src python3 -m wisegen_forge.cli verify --run .forge/demo
PYTHONPATH=src python3 -m wisegen_forge.cli export --run .forge/demo --out bundle.zip
```

## What the demonstrator proves

Input: an employee onboarding spreadsheet, an HR policy document, an organisation chart and a one-paragraph requirement.

Output, in one governed run:

1. an immutable intake record with provenance;
2. a validated specification with acceptance criteria;
3. an inferred data model with PDPA-relevant data classification;
4. an architecture plan, threat model and cost envelope;
5. a dependency-aware mission graph;
6. two competing candidate implementations, separately costed, tested and witnessed;
7. a generated role-based application with schema, API, tests, OpenAPI description and container recipe;
8. an evaluation report against declared quality gates;
9. a Captain's Gate packet holding what changed, why, by whom, on what evidence, at what cost and how to reverse it;
10. a signed release manifest with a rollback target;
11. a tamper-evident witness chain;
12. a portable ownership bundle.

## Core commands

| Command | Purpose |
|---|---|
| `forge doctor` | Verify interpreter, repository layout, policies and agent registry |
| `forge roles` | Print the role roster and each role's mandate and exit artefact |
| `forge compile-sheet FILE` | Inspect a spreadsheet: schema, classification, workflow, quality |
| `forge plan --statement ...` | Craft a specification and mission graph without executing |
| `forge run --statement ... --input FILE` | Execute the full pipeline |
| `forge demo [--keep]` | Run the reference demonstrator; `--keep` appends to an existing run root |
| `forge gate --run DIR [--action approve --by NAME --rationale "..."]` | Inspect or decide the Captain's Gate packet |
| `forge verify --run DIR` | Verify the witness chain, given a run directory or a chain file |
| `forge export --run DIR --out FILE` | Produce the portable ownership bundle |

Install as a console script with `pip install -e .`, then call `forge` directly.

## The eight guarantees

1. **Model independence.** Models are replaceable execution resources behind a provider-neutral adapter. No capability depends on one vendor.
2. **Deployment independence.** Managed cloud, customer VPC, on-premises and local workstation are first-class targets.
3. **Evidentiary completion.** A task is complete only when its evidence satisfies the acceptance contract. An agent reporting "done" has no standing.
4. **Reversible autonomy.** Every consequential action has bounded authority, observable execution and a tested reversal path.
5. **Organisational governance.** Policies, owners, approval thresholds and retention rules are inherited from the organisation, not invented per project.
6. **Portable ownership.** Code, specifications, policies, agent contracts, evidence and deployment machinery all export.
7. **Deliberative branches.** Competing solutions are evaluated, not silently collapsed into the first generated answer.
8. **Regenerative maintenance.** The specification stays authoritative. Drift is detected and regeneration is proposed, never applied unattended.

## Architecture in one view

```
WISEGEN APE MAINFRAME
├── Kaie Sovereign   authority, policy, identity, approvals
├── Gaie Forge       intent compilation, architecture, code production
├── Paie Command     execution control, observability, budgets, rollback
├── Saie Commons     templates, components, reusable capability
├── Taie Market      packaging, catalogue, client deployment
└── WiseGen Forge    the user-facing intent-to-system product surface
```

WiseGen Forge is not a sixth estate. It is the factory interface spanning the five.

## Documentation

| Document | Read it for |
|---|---|
| `docs/ROLES.md` | The role roster from design to fruition, and who signs what |
| `docs/architecture/ARCHITECTURE.md` | Services, runtime sequence, boundaries |
| `docs/architecture/DATA-MODEL.md` | The canonical objects and their required fields |
| `docs/governance/CAPTAINS-GATE.md` | The approval contract |
| `docs/governance/WITNESS-CHAIN.md` | Tamper-evidence and verification |
| `docs/governance/THREAT-MODEL.md` | Adversarial posture and the five security layers |
| `docs/agent-authoring/AGENT-CONTRACTS.md` | How to craft a new role |
| `docs/deployment/DEPLOYMENT.md` | The four estates |
| `docs/operations/RUNBOOK.md` | Day-two operation, incident response, kill switch |
| `docs/PORTABILITY.md` | The export contract and exit test |
| `docs/decision-records/` | Architecture decision records |

## Licence and ownership

See `LICENSE`. Generated applications belong to the customer. The portability contract in `docs/PORTABILITY.md` is a design obligation, and `tests/acceptance/` holds the test that enforces it.

Copyright 2026 Dr William Siew, Spark-a-life. WiseGen APE Intelligence.
