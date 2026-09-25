# ADR-007: Witness Chain captures execution events

- Status: Accepted for alpha
- Date: 2026-08-30
- Decider: Human Captain

## Context

If execution logs collapse technical success into business success, or omit digest and approval binding, reconciliation and audit fail. Overcollection creates a second leak path.

## Decision

Consequential execution records proposal, digest, approval, request, response, technical execution state, business outcome state, amendments, rollback and compensation where applicable. Technical and business states remain separate. Secrets are not stored.

## Consequences

- Receipt fields follow `governance/AIOS_v1.2.md` §31.1.
- `approval_id` may be null for Green events that policy allows without an individual gate.
- Indeterminate is recorded rather than guessed.
- This snapshot provides schemas and examples. It does not provide a Witness store.
