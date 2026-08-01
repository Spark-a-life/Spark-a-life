# External Standards Map

This map translates external governance expectations into implementation controls in this repository. It is not legal advice. It is a release engineering checklist for client-facing MAMT fundraising deployments.

## AI and agent safety

| External reference area | Repository control |
|---|---|
| Prompt injection and indirect instruction attacks | `safeguards/prompt_injection.py`, blocked egress, local deterministic default |
| Excessive agency and tool misuse | `configs/tool_capability_contracts.yaml`, `RiskBudget`, `RuntimeGovernor`, Captain Gate |
| Sensitive information disclosure | `governance.personal_data_used`, `check_contact_privacy`, egress approval policy |
| Model denial-of-service and runaway loops | `RuntimeGovernor`, `LoopDetector`, circuit breaker, budget checks |
| Supply-chain quality | `pyproject.toml`, CI, release manifest, export exclusions, local-first dependency set |

## Fundraising governance

| Risk area | Repository control |
|---|---|
| Public fundraising disclosure | `governance.public_appeal`, `disclosure_requirements`, compliance finding generation |
| Foreign charitable purpose or cross-border appeals | `governance.foreign_charitable_purpose`, permit/control mapping, block on missing controls |
| Donor acceptance and reputational risk | `donor_acceptance_policy`, `fundraising/donor_due_diligence.py` |
| Undue pressure in outreach | restricted terms and undue-pressure phrase checks |
| Data-room egress | `data_room_checklist`, `egress_policy`, Captain Gate |

## Client shipment controls

| Control | Command |
|---|---|
| Validate mission contracts | `wg-fund validate examples/missions/fundraising_500k_programme.yaml` |
| Run deterministic mission | `wg-fund run examples/missions/fundraising_500k_programme.yaml` |
| Inspect generated mission | `wg-fund inspect outputs/fundraising_run.json` |
| Review safeguards only | `wg-fund review examples/missions/fundraising_500k_programme.yaml` |
| Verify audit chain | `wg-fund verify-audit outputs/witness_chain.jsonl` |
| Run release preflight | `wg-fund preflight --output outputs/preflight.json` |
| Generate release manifest | `wg-fund manifest --output outputs/release_manifest.json` |
