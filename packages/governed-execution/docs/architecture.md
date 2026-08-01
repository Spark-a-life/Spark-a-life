# Architecture

## 1. Purpose

The control plane translates an authorised request into a bounded action and records enough evidence to determine what was requested, which policy applied, who authorised it, what was executed and whether the intended postcondition was observed.

It deliberately separates four concerns:

1. Model or human intent
2. Tool and system integration
3. Policy-constrained execution
4. Assurance, evidence and controlled learning

## 2. Component model

```mermaid
flowchart TB
  I[Model or human intent] --> E[Governed Execution Engine]
  E --> C[Capability Registry]
  E --> P[Policy Engine]
  P --> A[Approval Service]
  E --> H[HTTP Adapter]
  E --> B[Isolated Browser Adapter]
  H --> S[Authorised API or event interface]
  B --> U[Authorised user interface]
  E --> V[Semantic Verifier]
  C --> W[Witness Chain]
  P --> W
  A --> W
  E --> W
  V --> W
```

## 3. Control sequence

```mermaid
sequenceDiagram
  participant R as Requester
  participant E as Execution Engine
  participant C as Capability Registry
  participant P as Policy Engine
  participant A as Approval Service
  participant T as Target Adapter
  participant V as Verifier
  participant W as Witness Chain

  R->>E: Bound action request
  E->>C: Resolve capability and entitlement
  E->>P: Evaluate versioned policy
  P-->>E: Allow, deny, step-up or approval required
  E->>W: Record policy decision
  alt Approval required
    E-->>R: Await independent approval
    R->>A: Submit exact action and approver identity
    A-->>R: Short-lived, single-use bound token
    R->>E: Re-submit exact action with token
    E->>A: Validate and consume token
  end
  E->>T: Authorised tool invocation
  T-->>E: Result and observed state
  E->>V: Check semantic postconditions
  V-->>E: Verified or state uncertain
  E->>W: Record outcome and evidence
  E-->>R: Final disposition
```

## 4. Trust boundaries

| Boundary | Controlled by | Primary controls |
|---|---|---|
| Requester to control plane | Control API or CLI | Authentication, schema checks, body limits, role claims |
| Control plane to policy | Governance configuration | Versioning, default deny, precedence, negative tests |
| Control plane to adapter | Capability Registry | Adapter binding, parameter allowlists, origin and file boundaries |
| Adapter to target system | Target contract | Idempotency, timeouts, fixed selectors, semantic verification |
| Control plane to evidence store | Witness Chain | Redaction, sequence, previous hash, HMAC signature, single writer |
| Requester to approver | Approval Service | Separation of duties, exact-action binding, expiry, single use |

## 5. Browser execution

The browser adapter uses Chromium's DevTools Protocol through `--remote-debugging-pipe`. The browser process is created per action with a new temporary user-data directory. The adapter supports:

- allowlisted navigation
- allowlisted local content fixtures for repeatable tests
- CSS-selector resolution from capability configuration
- focus, text insertion and browser-level mouse input
- constrained observations of text, value or checked state

It does not accept arbitrary JavaScript from the request and does not persist authenticated state.

## 6. Reliability model

Reliability is defined as bounded and evidenced execution, not guaranteed success. The engine distinguishes:

- **BLOCKED:** policy prohibited execution
- **AWAITING_APPROVAL:** exact action requires independent approval
- **STEP_UP_REQUIRED:** stronger authentication or human presence is required
- **FAILED:** execution could not complete within the defined contract
- **STATE_UNCERTAIN:** an action may have occurred, but semantic postconditions were not established
- **SUCCEEDED:** all required semantic postconditions passed

Automatic retry is permitted only when the adapter classifies the failure as retryable and the capability contract marks the operation idempotent.
