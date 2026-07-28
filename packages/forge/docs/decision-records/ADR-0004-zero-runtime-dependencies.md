# ADR-0004: Zero runtime dependencies in version 1

- Status: accepted
- Date: 2026-07-25
- Deciders: Captain, Security Auditor, Solution Architect

## Context

The strategic brief proposed TypeScript, PostgreSQL, Redis, Temporal, OPA and OpenTelemetry. That is the right institutional target. It is the wrong version 1, because a spine that cannot start without a package index cannot run in the estate that most needs it.

## Decision

The version 1 control plane uses the Python standard library only. Every proposed component has a named substitution path with an unchanged interface: policy requests keep their shape for OPA, manifests keep their shape for Cosign, cost snapshots keep their shape for OpenTelemetry.

## Consequences

- Runs air-gapped, in CI, and on a customer laptop with no installation.
- Supply-chain surface for the platform itself is the interpreter.
- Scale limits are real: in-process wave scheduling, file-backed state. Institutional deployment substitutes rather than rewrites.

## Alternatives considered

- **Build the institutional stack first.** Rejected: months before the first demonstrator, and the governance properties would be unproven when the infrastructure arrived.
- **Adopt a light dependency set.** Rejected: each dependency reopens the air-gap question, and the standard library covers what the spine needs.
