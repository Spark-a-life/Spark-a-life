# ADR-0001: Zero-dependency core

- Status: Accepted
- Date: 2026-07-28

## Context

The platform must remain portable, inspectable and locally executable without an external package supply chain for its core governance path.

## Decision

Implement the control plane using Node.js built-ins and the native test runner. External adapters may be added behind explicit contracts, but the default policy, approval, evidence, HTTP and CDP-pipe paths have no npm runtime dependencies.

## Consequences

- Reduced package supply-chain exposure
- Straightforward offline installation
- More code is maintained internally
- Advanced schema validation and observability integrations require deliberate additions
