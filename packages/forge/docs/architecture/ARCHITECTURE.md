# Architecture

## Position in the estate

```
WISEGEN APE MAINFRAME
├── Kaie Sovereign   authority, policy enforcement, identity, approvals
├── Gaie Forge       intent compilation, architecture, code and application production
├── Paie Command     execution control, observability, budgets, rollback, kill switch
├── Saie Commons     templates, components, patterns, reusable capability
├── Taie Market      packaging, solution catalogue, client deployment
└── WiseGen Forge    user-facing intent-to-system product surface
```

WiseGen Forge is not a sixth autonomous estate. It is the application factory interface spanning the five, which is why role ids carry the estate prefix of the estate whose authority they exercise.

## The twelve-service spine

Version 1 implements one production-grade vertical slice rather than an incomplete platform. Everything else evolves around this spine.

| Service | Module | Responsibility |
|---|---|---|
| Intent Compiler | `intent_compiler.py` | Converts natural-language requests, documents and datasets into validated specifications |
| Project Service | `pipeline.ForgeRun` | Maintains the run, its objects, versions and lifecycle state |
| Orchestration Engine | `orchestrator.py` | Creates and executes dependency-aware mission graphs |
| Agent Runtime | `agent_runtime.py` | Runs roles with scoped identity and permissions |
| Model Router | `model_router.py` | Selects models by capability, risk, cost and availability |
| Tool Gateway | `tool_gateway.py` | Mediates every external action, denies by default |
| Policy Engine | `policy.py` | Evaluates whether a requested action is permitted |
| Evaluation Engine | `evaluation.py` | Runs deterministic and evidence-based quality gates |
| Witness Service | `witness.py` | Records tamper-evident execution evidence |
| Approval Service | `approval.py` | Implements the Captain's Gate |
| Deployment Service | `deployment.py` | Produces and applies signed, reversible release manifests |
| Cost Governor | `cost.py` | Enforces project and role resource limits |

Two further modules serve the reference workflow: `spreadsheet_compiler.py` (schema inference, classification, workflow discovery, data quality) and `generators/webapp.py` (application, schema, tests, OpenAPI, container recipe).

## Runtime sequence

```
Stage 1  Intake                 immutable record, provenance attached
Stage 2  Intent compilation     specification with acceptance criteria   [Captain approves]
Stage 3  Architecture and risk  threat model, classification, cost envelope, rollback
Stage 4  Mission planning       dependency graph, parallel only where dependencies permit
Stage 5  Branchable execution   competing candidates, separately costed and witnessed
Stage 6  Continuous verification quality gates, fail closed
Stage 7  Captain's Gate         human decision, recorded                 [Captain decides]
Stage 8  Deployment             signed manifest, named rollback target
Stage 9  Operational learning   evidence feeds back through a governed gate, never automatically
```

Stages 2 and 7 are hard human gates. Everything else is automatable within bounded authority.

## Intent compilation

The compiler is the difference between an application factory and a prompt-to-code tool. It transforms:

```
Human intent
    -> structured product brief
    -> executable specification
    -> architecture decision record
    -> task dependency graph
    -> generated and verified system
```

Each arrow is an artefact with an owner, a version and evidence, not a conversational turn.

## Branchable execution

Material choices produce parallel candidates rather than the first plausible answer:

```
Task
 ├── Candidate A  conservative implementation
 ├── Candidate B  performance-oriented implementation
 ├── Candidate C  sovereign or local implementation
 └── Candidate D  adversarial challenge
```

Each candidate is separately costed, tested and witnessed. The evaluation layer scores them; the Captain selects, combines or rejects. This converts orchestration from linear delegation into governed deliberation.

## Data flow and trust boundaries

```
[intake files] --digest--> [intake record] --> [specification] --> [mission graph]
                                                     |
                              policy engine <--------+--------> cost governor
                                                     |
                                            [tool gateway]  (deny by default, no network)
                                                     |
                                            [run workspace]  (sandbox, no repo access)
                                                     |
                              witness chain <--- every action, refusal and failure
```

Everything crossing a boundary is witnessed, including refusals and failures. A trail that records only successes overstates what happened.

## Technology position

The control plane is deliberately standard library only. The brief proposed TypeScript, PostgreSQL, Redis, NATS or Temporal, OPA and OpenTelemetry, and that remains the right institutional target. Version 1 is written so that each of those is a substitution rather than a rewrite:

| Concern | Version 1 | Institutional substitution |
|---|---|---|
| Transactional state | JSON objects under the run root | PostgreSQL |
| Queue and locks | in-process wave scheduling | Redis, NATS or Temporal |
| Policy | `policy.py` over YAML rules | Open Policy Agent, same request shape |
| Telemetry | witness chain plus cost snapshots | OpenTelemetry traces and metrics |
| Artefact storage | run workspace | S3-compatible object storage |
| Signing | HMAC over the manifest payload | Cosign with an organisational key |

The reason for holding the line at zero dependencies in version 1 is the air-gapped estate: if the spine cannot run without a package index, sovereignty claims are decorative.

## What is deliberately not built yet

Real-time co-editing, the connector marketplace, the mobile companion and cross-institutional learning are all out of scope for version 1. Each needs a named deployment before it earns maintenance cost. See `docs/decision-records/ADR-0006-scope-boundary.md`.
