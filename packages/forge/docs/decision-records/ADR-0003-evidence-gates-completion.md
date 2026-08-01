# ADR-0003: Evidence gates completion

- Status: accepted
- Date: 2026-07-25
- Deciders: Captain, Assurance Engineer

## Context

An agent reporting completion has no standing on its own. Fluent self-report is the single most common failure mode in multi-agent systems, and it is indistinguishable from success at the point of reading.

## Decision

A task is complete only when its evidence satisfies the acceptance contract. Failing blocking evidence keeps the gate packet from becoming ready, and a packet that is not ready cannot be approved, branch-selected or deployed.

## Consequences

- Lower nominal throughput, auditable completion claims.
- Gates must be cheap enough to run on every candidate, which constrains gate design.
- Evidence storage grows with runs; retention policy exists for this reason.

## Alternatives considered

- **Trust agent self-report with sampling.** Rejected: sampling detects patterns, not the specific release in front of the reviewer.
