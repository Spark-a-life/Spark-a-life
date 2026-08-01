# Governance Model

## Captain's Gate

Captain's Gate is the decision boundary that determines whether an action may proceed. It combines:

- actor entitlement
- capability and operation identity
- exact parameters and target
- risk thresholds
- segregation of duties
- approval and step-up requirements
- prohibition rules

The implementation is fail-closed. If no explicit policy rule matches, the default effect is `DENY`.

## Witness Chain

The Witness Chain records the minimum operational evidence needed for accountability. Each record contains:

- a monotonically increasing sequence
- the previous record hash
- an event type and timestamps
- a redacted payload
- a canonical record hash
- an HMAC signature

This provides process-local tamper evidence. It does not prove that the operator controlling the HMAC key did not rewrite the entire chain. Higher-assurance deployments should send records to an independently governed append-only store.

## Capability Registry

A capability contract specifies:

- capability identifier and description
- adapter type
- eligible actor roles
- permitted operations
- parameter allowlist
- idempotency and retry boundary
- target origin or file boundary
- execution plan where applicable
- observations and semantic postconditions

Requests cannot supply additional fields, arbitrary selectors or executable code.

## Governance-as-Code

Policy rules are ordered by explicit priority. Each rule contains conditions, an effect and a reason. Supported effects are:

| Effect | Meaning |
|---|---|
| `ALLOW` | Execute within the capability contract |
| `DENY` | Block before target-system invocation |
| `REQUIRE_APPROVAL` | Require an independent approver with the configured role |
| `REQUIRE_STEP_UP` | Require stronger authentication or human presence |

## Approval contract

An approval token is bound to:

- request identifier
- requester identity and roles
- capability and operation
- target base URL
- exact parameters
- idempotency key
- approver identity and required role
- issue and expiry times
- a unique nonce

Tokens are HMAC-signed and consumed once. Self-approval is prohibited.

## Decision rights

Recommended operating roles:

| Role | Decision right |
|---|---|
| Capability owner | Defines tool purpose and operating boundary |
| Policy owner | Defines allow, deny and approval conditions |
| Risk owner | Accepts residual operational and security risk |
| Approver | Authorises a specific consequential action |
| Operator | Initiates actions within assigned roles |
| Auditor | Verifies evidence integrity and control operation |
| Platform custodian | Operates keys, runtime and evidence storage |

No single person should define policy, operate signing keys and approve their own consequential actions.
