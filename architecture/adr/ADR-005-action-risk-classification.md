# ADR-005: Green / Amber / Red / Prohibited Action classification

- Status: Accepted for alpha
- Date: 2026-08-30
- Decider: Human Captain

## Context

Technical read versus write status does not capture consequence. A read can leak confidential data. A write can be trivial. A missing Prohibited class lets forbidden operations be argued down to Red.

## Decision

Action controls are selected by consequence, authority, sensitivity, purpose, destination and reversibility. Classes are Green, Amber, Red and Prohibited. Schema enumerations are `GREEN`, `AMBER`, `RED`, `PROHIBITED`.

## Consequences

- Read-only is not automatically Green.
- Prohibited is refused and cannot be split into smaller Amber Actions to evade class.
- Green must remain representable without an individual approval object.
- Amber and Red require the governance minimum in §27.1 without making Green impossible.
