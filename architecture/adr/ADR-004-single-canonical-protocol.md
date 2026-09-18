# ADR-004: One canonical External Action Protocol

- Status: Accepted for alpha
- Date: 2026-08-30
- Decider: Human Captain

## Context

A standalone 12-step protocol that stops at "Captain's Gate 9" can weaken the v1.2 16-step protocol. v1.2 forbids standalone copies that diverge.

## Decision

`governance/AIOS_v1.2.md` §26 is the protocol source. `governance/EXTERNAL_ACTION_PROTOCOL.md` is the extracted copy and must not diverge. Architecture notes reference those files rather than duplicating or independently modifying the protocol.

## Consequences

- Derived documents lose if they disagree with §26.
- Layer 0, Prohibited, immutable digest, externally verifiable approval and three-way reconciliation cannot be omitted.
- Opportunity Gate 9 is not the only gate and is not sufficient for consequential external execution.
