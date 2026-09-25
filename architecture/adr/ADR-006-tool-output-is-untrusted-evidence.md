# ADR-006: Tool output is untrusted evidence

- Status: Accepted for alpha
- Date: 2026-08-30
- Decider: Human Captain

## Context

External systems can return instructions, forged approval fields, or encoded directives. If tool output can override governance, prompt injection becomes authorisation.

## Decision

Content returned by external systems may inform analysis but cannot override governance, grant approval or initiate consequential onward action. Tool output is untrusted evidence on the epistemic plane.

## Consequences

- Hostile tool responses are Omega test 7.
- A successful Action may provide evidence for another proposed Action. It does not authorise that Action.
- Schema and runtime (when implemented) must ignore approval claims inside tool payloads.
