# Architecture

WiseGen Creative Engineering Framework v1.1 uses MAMT as the organising architecture. A mission is not sent directly to a model. It is first admitted, decomposed into role contracts, governed by budgets, and routed through model-specific adapters.

## Layers

1. **Mission Contract Layer**: validates objective, audience, channel, brand, references, outputs and risk budget.
2. **MAMT Layer**: assigns work to specialist role agents with explicit scope and limits.
3. **Runtime Governor**: enforces budgets, wall-clock limits, retry limits, repeated-state detection and circuit-breaker transitions.
4. **Credential Broker**: issues short-lived capability tokens based on declared tool contracts.
5. **Model Router**: chooses the adapter without changing the mission contract.
6. **Evaluation Layer**: scores fidelity, brand fit, governance, accessibility, platform readiness and operational risk.
7. **Captain's Gate**: determines whether output is approved, requires revision, or must be blocked.
8. **Witness Chain**: creates a digest-linked audit trail.

## Principle

MAMT decides who does what. The Runtime Governor decides how far execution may go. The Credential Broker decides what can be touched. Captain's Gate decides what may ship. The Witness Chain records what happened.
