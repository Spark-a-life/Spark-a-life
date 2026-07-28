# Customer VPC

The primary institutional estate. Data residency and sovereignty requirements dominate hosting convenience for the customers this platform is built for.

## What the customer provides

- A private subnet with no inbound internet exposure
- Object storage for evidence bundles, in-region
- A managed PostgreSQL instance if substituting file-backed state
- A key management service holding the manifest signing key

## What the customer keeps

Everything. The run store, the evidence chain, the generated system and the bundle never leave the customer boundary. The platform holds no copy, which is why there is no telemetry callback and no licence check.

## Residency

Recorded in the architecture plan at stage 3, carried into the release manifest, and part of what the Captain approves. It is not discovered at deployment time.

## Egress

Denied by default. If a hosted model adapter is approved, the allow list is explicit, per endpoint, recorded as a policy change, and reviewable in the witness chain as `tool.invoked` entries against a network tool.
