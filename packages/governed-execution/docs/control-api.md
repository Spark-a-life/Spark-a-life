# Control API

The API binds to `127.0.0.1:8787` by default. All routes except `/health` require:

```http
Authorization: Bearer ${CONTROL_API_KEY}
```

The service applies a 1 MiB request-body limit and a process-local rate limit.

## GET /health

Returns service status and runtime mode.

```json
{
  "status": "ok",
  "service": "wisegen-ape-governed-execution",
  "mode": "production"
}
```

## POST /v1/execute

Executes or disposes a governed action request.

Possible dispositions:

- `SUCCEEDED`
- `AWAITING_APPROVAL`
- `STEP_UP_REQUIRED`
- `BLOCKED`
- `STATE_UNCERTAIN`
- `REJECTED`
- `FAILED`

Example:

```bash
curl --fail --silent --show-error \
  -H "Authorization: Bearer ${CONTROL_API_KEY}" \
  -H "Content-Type: application/json" \
  --data @examples/note-create.json \
  http://127.0.0.1:8787/v1/execute
```

## POST /v1/approve

Issues a single-use, short-lived token bound to an exact action. The policy engine must independently determine that the action requires approval.

Request:

```json
{
  "request": {
    "requestId": "request_transfer_0001",
    "actor": {"id": "finance.morgan", "roles": ["finance_operator"]},
    "capabilityId": "payments.transfer",
    "operation": "submit",
    "targetBaseUrl": "http://127.0.0.1:8899",
    "parameters": {
      "amount": 2500,
      "currency": "SGD",
      "beneficiary": "Approved Demonstration Vendor",
      "purpose": "Governed execution demonstration"
    },
    "idempotencyKey": "idem_transfer_0001"
  },
  "approver": {
    "id": "approver.riley",
    "roles": ["finance_approver"]
  }
}
```

Response:

```json
{
  "requestId": "request_transfer_0001",
  "approvalToken": "[REDACTED]",
  "expiresInSeconds": 300
}
```

Add the token as `approvalToken` to the unchanged action request and re-submit it to `/v1/execute`.


## GET /v1/requests/{requestId}

Returns the latest durable execution-state snapshot for one request. Returns `404` when the request identifier is unknown.

```json
{
  "requestId": "request_note_0001",
  "state": "SUCCEEDED",
  "history": [
    {"state": "RECEIVED", "at": "..."},
    {"state": "POLICY_EVALUATED", "at": "..."},
    {"state": "AUTHORISED", "at": "..."},
    {"state": "EXECUTING", "at": "..."},
    {"state": "VERIFYING", "at": "..."},
    {"state": "SUCCEEDED", "at": "..."}
  ]
}

## GET /v1/witness/verify

Verifies the full record sequence, previous-hash links, record hashes and HMAC signatures.

```json
{
  "valid": true,
  "records": 42,
  "headHash": "..."
}
```

## Production integration notes

- Replace the static API key with organisation-approved workload identity.
- Place the service behind TLS, network policy and an authenticated gateway.
- Use a shared transactional store for approval nonces in multi-instance deployments.
- Export logs and metrics without copying sensitive payloads.
- Treat `STATE_UNCERTAIN` as an operational incident requiring reconciliation.
