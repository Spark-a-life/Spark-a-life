# Operations Manual

## Local execution

```bash
wisegen-witl run --case examples/leadgen_case.json --workflow workflows/leadgen_workflow.json --out outputs/leadgen_decision.json
```

## Audit inspection

```bash
wisegen-witl audit --log audit/witness-chain.jsonl
```

## Adding a new workflow

1. Copy an existing file in `workflows/`.
2. Change `workflow_id`, `domain`, `criteria`, and thresholds.
3. Add a matching example case in `examples/`.
4. Run the CLI.
5. Commit the workflow and output report for traceability.

## Adding a new lane

Create a new lane function that accepts workspace state and returns a lane assessment with:

- lane name
- finding
- confidence
- risks
- recommendations

Then register it in `lanes/default_lanes.py`.

## Production hardening checklist

- Replace local JSONL witness chain with append-only object storage or database table.
- Add identity provider integration.
- Add role-based access control.
- Add encrypted evidence storage for confidential data.
- Add external LLM adapters with deterministic prompt contracts.
- Add policy packs for regulated domains.
- Add outcome-review cadence.
