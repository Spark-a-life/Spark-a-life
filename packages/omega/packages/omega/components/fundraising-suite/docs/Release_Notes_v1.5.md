# Release Notes v1.5.0

## Release intent

v1.5 turns the v1.2 reference implementation into a more client-shippable MAMT fundraising suite. The emphasis is not more automation. The emphasis is governed portability, release preflight, stricter contracts, fundraising compliance surfaces, donor due diligence and evidence-safe creativity.

## Major upgrades from v1.2

1. Added a mandatory governance profile to mission contracts.
2. Hardened the JSON Schema with `additionalProperties: false` and stricter enumerations.
3. Added fundraising governance checks for public appeal, foreign charitable purpose, personal data use, vulnerable audiences, restricted terms and required approvals.
4. Added prompt-injection surface scanning across prospect, evidence and claim fields.
5. Added donor due-diligence output for prospect-level acceptance review.
6. Added model-routing decisions with rationale and external-call policy.
7. Added release preflight and release manifest commands.
8. Added audit verification command.
9. Updated examples to include governance metadata.
10. Added external standards mapping for AI-agent safety, fundraising governance and client shipment controls.

## Non-goals

- The suite does not send outreach automatically.
- The suite does not connect to a live CRM by default.
- The suite does not claim legal compliance. It provides structured controls for human legal and compliance review.
- The local deterministic adapter does not call external models.

## Client acceptance baseline

A release candidate must pass:

```bash
pytest
ruff check .
wg-fund validate examples/missions/fundraising_500k_programme.yaml
wg-fund run examples/missions/fundraising_500k_programme.yaml --output outputs/fundraising_run.json
wg-fund inspect outputs/fundraising_run.json
wg-fund verify-audit outputs/witness_chain.jsonl
wg-fund preflight --output outputs/preflight.json
wg-fund manifest --output outputs/release_manifest.json
python scripts/export_repo_zip.py --output outputs/wisegen-mamt-fundraising-suite-v1.5.zip
```
