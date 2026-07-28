# Operator Runbook

## 1. Initialisation

```bash
npm run keygen
npm run check
```

Review `.env`, `config/capabilities.json` and `config/policies.json`. Do not enable a real capability until its target, identity model, data classification, postconditions and failure semantics have been approved.

## 2. Start services

For the local demonstration:

```bash
node src/cli.js demo-target
npm run serve
```

For production-oriented operation, bind the service to a private interface behind an authenticated reverse proxy. Terminate TLS outside the Node process or add an organisation-approved TLS layer.

## 3. Health and evidence checks

```bash
curl --silent http://127.0.0.1:8787/health
curl --silent \
  -H "Authorization: Bearer ${CONTROL_API_KEY}" \
  http://127.0.0.1:8787/v1/witness/verify
```

Treat an invalid Witness Chain as an incident. Stop consequential execution, preserve the file and key state, and investigate before resuming.

## 4. Approval workflow

1. Submit the action to `/v1/execute`.
2. Receive `AWAITING_APPROVAL` and the policy decision.
3. Present the exact action to an eligible independent approver.
4. Submit the action and approver identity to `/v1/approve`.
5. Attach the returned token to the unchanged action request.
6. Re-submit to `/v1/execute` before expiry.

Changing any bound action field invalidates the token.

## 5. Backup and retention

Back up:

- Witness Chain files
- policy and capability versions
- approval nonce records
- key identifiers and rotation records
- release manifests and test evidence

Do not back up raw temporary browser profiles. The adapter deletes them after each run.

## 6. Key rotation

1. Stop the control plane.
2. Archive the current chain with its key identifier and verification result.
3. Generate new keys using an approved secrets system.
4. Start a new Witness Chain file.
5. Record the rotation event in the organisation's external audit system.
6. Restart and run smoke tests.

The bundled `npm run keygen` refuses to overwrite an existing `.env`.

## 7. Incident dispositions

| Condition | Immediate action |
|---|---|
| `BLOCKED` | Confirm policy operated as intended; no target action should have occurred |
| `AWAITING_APPROVAL` | Route to an eligible independent approver |
| `STEP_UP_REQUIRED` | Pause and complete approved human authentication |
| `FAILED` | Examine adapter error and target availability; retry only within idempotency contract |
| `STATE_UNCERTAIN` | Do not repeat blindly; reconcile against the system of record and escalate |
| Witness verification failure | Freeze consequential execution and preserve evidence |
| Suspected key exposure | Revoke, rotate, inspect historical evidence and invalidate active approvals |
