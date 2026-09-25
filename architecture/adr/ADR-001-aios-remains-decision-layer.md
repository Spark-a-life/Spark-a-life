# ADR-001: AIOS remains the decision layer

- Status: Accepted for alpha
- Date: 2026-08-30
- Decider: Human Captain

## Context

External APIs, GPT Actions and tool runtimes can execute operations. If those execution surfaces also decide whether an operation should happen, AIOS ceases to be a governance layer and becomes commentary after the fact.

## Decision

AIOS evaluates whether an action is warranted. External Actions execute approved operations but do not become independent decision makers. API capability does not imply decision authority.

## Consequences

- The four evaluation layers remain the decision logic.
- Governed Action is an operational stage, not a fifth evaluation layer.
- A future Action Gateway may only execute what AIOS and the Human Captain have already authorised.
- This snapshot specifies that split. It does not implement a gateway.
