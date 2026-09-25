# ADR-002: Actions execute but do not authorise

- Status: Accepted for alpha
- Date: 2026-08-30
- Decider: Human Captain

## Context

A language model can emit `human_authorisation=true` or similar fields. If a schema or runtime accepts that field as approval, the system self-authorises.

## Decision

Human authorisation is enforced outside model-generated content. The Action service must reject consequential execution without a valid, server-issued approval object. The proposal schema must not accept smuggled authorisation fields (`additionalProperties` is false).

## Consequences

- Model text is never an approval record.
- Amber and Red require externally verifiable approval bound to `proposal_digest`.
- Green read-only may proceed without an individual gate only where Layer 0 and policy already authorise the retrieval.
- Prohibited cannot be approved into execution.
- This snapshot is Declared, not Enforced: there is no approval service yet.
