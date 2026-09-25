# Action State Machine

Status: Draft  
Version: 1.2.0-alpha  
Canonical source: `governance/AIOS_v1.2.md` §30

## Execution lifecycle states

Canonical names. Do not use `UNKNOWN` as the canonical name for Indeterminate.

```text
Proposed
Awaiting Authorisation
Authorised
Rejected
Expired
Revoked
Executing
Succeeded
Failed
Partially Succeeded
Indeterminate
Rolled Back
Irreversible
```

Schema enumerations:

`PROPOSED`, `AWAITING_AUTHORISATION`, `AUTHORISED`, `REJECTED`, `EXPIRED`, `REVOKED`, `EXECUTING`, `SUCCEEDED`, `FAILED`, `PARTIALLY_SUCCEEDED`, `INDETERMINATE`, `ROLLED_BACK`, `IRREVERSIBLE`

| State | Meaning | Execution |
|---|---|---|
| Proposed | Proposal exists but is not yet authorised | No |
| Awaiting Authorisation | Waiting for externally verifiable approval | No |
| Authorised | Valid approval exists for the exact proposal | May proceed within validity and scope |
| Rejected | Denied or forbidden | No |
| Expired | Proposal or approval validity ended | Re-propose if still required |
| Revoked | Approval withdrawn | No |
| Executing | Authorised attempt in flight | Do not duplicate |
| Succeeded | External effect confirmed | Reconcile |
| Failed | Authorised effect did not occur | Contain; do not blindly retry |
| Partially Succeeded | Only part of the authorised effect occurred | Contain, reconcile, escalate |
| Indeterminate | Result cannot be determined safely | Reconcile before any retry |
| Rolled Back | Known prior state restored | Record; stop or re-propose |
| Irreversible | Effect cannot be undone by this system | Contain, disclose, escalate |

## Business outcome states

Separate from execution states. A successful API response is technical evidence only.

`NOT_ASSESSED`, `PENDING`, `OBSERVED`, `NOT_ACHIEVED`, `CONFLICTED`, `INDETERMINATE`

## Rules

1. A proposal is immutable once submitted for approval. Binding uses `proposal_digest`.
2. Approval binds to the exact proposal identity, version, digest, scope, policy version and validity window.
3. Material changes require a new proposal and new approval.
4. Indeterminate is not failure and is not success. It means the execution result cannot be determined safely.
5. Never blindly retry a consequential operation after timeout or ambiguous response.
6. Use idempotency keys and status checks before resubmission.
7. Technical execution and business outcome remain separate.
8. Prohibited never enters Executing.
