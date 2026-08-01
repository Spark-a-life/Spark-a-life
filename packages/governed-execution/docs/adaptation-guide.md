# Adaptation Guide

## Add an HTTP capability

1. Add a capability entry in `config/capabilities.json`.
2. Declare the exact HTTP method and path.
3. Specify eligible roles and a parameter allowlist.
4. Mark idempotency truthfully.
5. Add semantic postconditions that verify the business outcome.
6. Add one or more explicit policy rules.
7. Add positive, denied, malformed and uncertain-state tests.

Example shape:

```json
{
  "id": "crm.case.update",
  "adapter": "http-json",
  "allowedRoles": ["case_operator"],
  "operations": {
    "update": {
      "method": "PATCH",
      "path": "/api/cases/${parameters.caseId}",
      "idempotent": true,
      "maxRetries": 1,
      "parameterAllowlist": ["caseId", "status", "reason"],
      "postconditions": [
        {"type": "httpStatus", "equals": 200},
        {"type": "jsonPointerEqualsFromRequest", "pointer": "/status", "requestPath": "parameters.status"}
      ]
    }
  }
}
```

## Add a browser capability

Use browser interaction only when the UI is the authorised operating surface or a suitable supported API is unavailable.

- declare one or more allowlisted origins or file prefixes
- keep selectors in capability configuration, not in model output
- avoid arbitrary JavaScript
- define exact observations and semantic postconditions
- use an isolated profile
- treat authentication and MFA as security boundaries
- do not persist personal browser state

## Add a policy rule

Rules are evaluated by descending priority. Denial rules should normally outrank approval and allow rules.

```json
{
  "id": "approve-high-risk-case-change",
  "priority": 800,
  "all": [
    {"path": "capabilityId", "operator": "equals", "value": "crm.case.update"},
    {"path": "parameters.status", "operator": "equals", "value": "CLOSED"}
  ],
  "effect": "REQUIRE_APPROVAL",
  "requiredApproverRole": "case_manager",
  "approvalTtlSeconds": 300,
  "reason": "Closing a case requires accountable managerial approval."
}
```

## Add a postcondition

Extend `src/core/verifier.js` with a narrowly defined condition type. It must return observed and expected values without silently coercing them. Add tests that prove both pass and fail behaviour.

## Add an adapter

An adapter must:

- accept only resolved capability contracts
- reject unauthorised targets and inputs
- enforce a timeout
- classify retryability conservatively
- return structured observations
- avoid leaking credentials into evidence
- support shutdown and cleanup

Register it in `src/adapters/index.js` and add integration tests.

## Readiness gate

Before release, confirm:

- capability owner and risk owner are named
- system-of-record semantics are understood
- exact actor authority is validated
- failure and partial-completion modes are documented
- postconditions verify the intended business result
- policy has negative tests
- key and evidence storage meet the risk tier
- rollback and incident procedures are rehearsed
