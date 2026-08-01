# ADR-0001: The specification is the authoritative artefact

- Status: accepted
- Date: 2026-07-25
- Deciders: Captain, Solution Architect

## Context

Generated code drifts. Chat history is not an artefact that survives a staffing change, a model change or an audit. Teams that treat the repository as the source of truth end up unable to say what the system was supposed to do, only what it currently does.

## Decision

The approved specification is authoritative. Code, tests, schema and deployment are derived from it. Drift is measured against it, and regeneration is a governed operation rather than a rewrite.

## Consequences

- Every acceptance criterion must map to at least one executable check. The `acceptance.coverage` gate is blocking.
- Changing behaviour requires changing the specification first. Contributing rules enforce this.
- The platform's durable product is governed regeneration, not the first generation.

## Alternatives considered

- **Repository as source of truth.** Rejected: cannot answer intent questions.
- **Conversation as source of truth.** Rejected: not an artefact, not versioned, not reviewable.
