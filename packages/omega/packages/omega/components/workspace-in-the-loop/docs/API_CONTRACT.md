# API Contract

This repo is JSON-native. A production API can expose the following endpoints.

## POST /workspace/run

Input:

```json
{
  "case": {},
  "workflow": {}
}
```

Output:

```json
{
  "report_id": "report-...",
  "recommendation": "...",
  "ranked_options": [],
  "risk": {},
  "captain_gate": {},
  "witness_hash": "..."
}
```

## GET /audit

Returns witness-chain events.

## POST /outcome

Stores outcome feedback against a report ID.
