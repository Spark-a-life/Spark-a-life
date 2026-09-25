# ADR-003: Server-side approval binding

- Status: Accepted for alpha
- Date: 2026-08-30
- Decider: Human Captain

## Context

Approvals that bind only to a proposal identifier, or to a mutable payload, can be replayed, substituted across cases, or applied after the payload has drifted.

## Decision

Approval binds to proposal ID, proposal version, `proposal_digest`, approved scope, approver identity, policy version and validity window. Any material mismatch invalidates approval. Binding is validated server-side, independently of model text.

## Consequences

- Canonical field names follow `governance/AIOS_v1.2.md` §27.3.
- Replay and cross-case substitution are in-scope threats (`architecture/threat-model.md`).
- Expired and revoked approvals cannot execute.
- This snapshot specifies the envelope. It does not implement the service.
