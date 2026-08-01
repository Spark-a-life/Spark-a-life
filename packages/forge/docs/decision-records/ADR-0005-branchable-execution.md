# ADR-0005: Material choices produce candidate branches

- Status: accepted
- Date: 2026-07-25
- Deciders: Captain, Solution Architect

## Context

A single generated answer hides the choice that produced it. Reviewers then approve an implementation without ever seeing that an alternative existed, which converts a design decision into an invisible default.

## Decision

Material choices produce parallel candidates, each separately costed, tested and witnessed. The evaluation layer scores them; the Captain selects, combines or rejects. Version 1 ships conservative and performance candidates, with sovereign and adversarial candidates defined and deferred.

## Consequences

- Generation cost scales with candidate count, which the cost governor bounds.
- The gate packet gains a genuine comparison rather than a summary.
- Orchestration becomes governed deliberation rather than linear delegation.

## Alternatives considered

- **Generate once, revise on rejection.** Rejected: the reviewer never sees the alternative, and revision loops cost more than parallel candidates.
