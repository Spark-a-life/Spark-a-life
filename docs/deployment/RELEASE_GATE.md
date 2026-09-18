# Release Gate for External Actions

Status: Draft  
This snapshot is not a production release. Every box remains unchecked. That is correct.

A production release must not proceed until:

- [ ] OpenAPI schema reflects implemented endpoints.
- [ ] Authentication and authorisation are independently reviewed.
- [ ] Human approval is server-issued and payload-bound.
- [ ] Least-privilege scopes are documented.
- [ ] GREEN / AMBER / RED / PROHIBITED classification rules are approved.
- [ ] Sensitive read operations are governed.
- [ ] Idempotency and INDETERMINATE-state reconciliation are tested.
- [ ] Prompt injection from tool outputs is tested.
- [ ] Action chaining is bounded.
- [ ] Kill switch / revocation is tested.
- [ ] Witness Chain retention and access rules are approved.
- [ ] Technical execution and business outcome are separately recorded.
- [ ] Credential leakage and silent control failure tests are recorded.
- [ ] All action-governance and adversarial acceptance specifications are run against an implementation.
- [ ] Human Captain approves the release.
