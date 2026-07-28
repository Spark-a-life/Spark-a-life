# ADR-0006: Version 1 scope boundary

- Status: accepted
- Date: 2026-07-25
- Deciders: Captain, Solution Lead

## Context

The strategic brief describes a platform spanning intent compilation, application assembly, spreadsheet conversion, system-prompt control, task forking, real-time co-editing, credit governance, customer-environment deployment and engineering handover. Attempting all of it in a first release produces a demonstration that governs nothing.

## Decision

Version 1 ships one production-grade vertical slice: the twelve-service spine, the twenty-role registry, the nine-stage runtime, and one demonstrator, the Governed Spreadsheet-to-Application Factory.

Deferred, each with an activation criterion:

| Capability | Activates when |
|---|---|
| Real-time co-editing workspace | A named engagement has two or more concurrent reviewers on one run |
| Connector marketplace | Three connectors exist that a customer actually requested |
| Mobile companion | A deployed customer asks to approve gates away from a desk |
| Cross-institutional learning | Three institutional deployments with signed data-sharing agreements |
| Managed multi-tenant cloud | A customer prefers managed hosting over their own VPC |

## Consequences

- The demonstrator claim is narrow and true, rather than broad and unprovable.
- Deferred capabilities carry no maintenance cost until they earn it.
- Some prospects will want the broad platform. The Solution Lead holds that boundary.

## Alternatives considered

- **Ship a generic build-any-app claim.** Rejected: it is the claim the market has already heard, and it cannot be demonstrated to an institutional buyer's satisfaction.
