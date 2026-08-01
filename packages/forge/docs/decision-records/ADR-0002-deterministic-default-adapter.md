# ADR-0002: The deterministic offline adapter is the default

- Status: accepted
- Date: 2026-07-25
- Deciders: Captain, Security Auditor

## Context

The factory must run in air-gapped estates and in CI with no vendor credential. It must also produce reproducible artefacts, because an audit cannot proceed against a system that generates something different each time.

## Decision

The default model adapter is deterministic and local. Hosted and local-runtime adapters are opt-in. Changing the adapter changes fidelity, never control flow, policy evaluation, evidence capture or the gate.

## Consequences

- The full pipeline and its 90 tests run offline in about two seconds.
- Output quality varies by adapter; governance behaviour does not.
- Sovereignty claims are demonstrable rather than asserted.

## Alternatives considered

- **Require a hosted model for all stages.** Rejected: excludes air-gapped estates and makes CI vendor-dependent.
- **Mock the model only in tests.** Rejected: the tested path would differ from the shipped path.
