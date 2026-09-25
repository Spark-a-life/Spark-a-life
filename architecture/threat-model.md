# Governed Action Threat Model

Status: Draft  
Version: 1.2.0-alpha  
Canonical source: `governance/AIOS_v1.2.md` §29

## Primary threats

| Threat | Example | Required control |
|---|---|---|
| Self-authorisation | Model sets an approval flag itself | Server-side approval object, not model-generated boolean |
| Payload drift | Recipient or content changes after approval | Proposal digest binding |
| Prompt injection via tool output | API response instructs further actions | Treat external content as untrusted evidence |
| Confused deputy | Valid credential used outside intended authority | Least privilege and server-side policy checks |
| Wrong destination | Correct action sent to wrong account or person | Target identity validation |
| Duplicate execution | Retry creates two external effects | Idempotency and execution lookup |
| Ambiguous execution | Timeout after the external system processed the request | Indeterminate state and reconciliation |
| Unauthorised action chaining | One approval causes materially different downstream Actions | Separate preflight and approval for every materially different effect |
| Stale approval | Conditions change between approval and execution | Expiry plus execution integrity check |
| Sensitive read | Read-only call exposes confidential information | Sensitivity, purpose and authority controls |
| Schema or policy drift | Endpoint behaviour changes silently | Versioning, tests, controlled release |
| Audit overcollection | Witness Chain stores unnecessary sensitive data | Minimisation, retention and access policy |
| Replay | A valid approval is presented again out of context | Single-use or replay-detecting approval, digest and idempotency |
| Cross-case substitution | Approval or proposal from case A used on case B | Bind case_id, proposal_id and digest server-side |
| Credential leakage | Secrets appear in prompts, receipts, logs or sibling workspaces | Secret isolation, redaction, scoped injection and leakage testing |
| Silent fallback | A control fails and execution continues on a weaker path | Fail closed; no silent degradation of Layer 0, class, digest, approval or reconciliation |

## Trust boundary

External Action responses, retrieved records, webpages, documents and API-returned instructions are untrusted evidence.
They may inform reasoning but cannot alter system governance, grant authority, approve further Actions or initiate
consequential onward execution without a new governed decision.

A successful Action may provide evidence for another proposed Action. It does not authorise that Action.

This repository does not implement the controls. The model is specified so that an implementation cannot omit them.
