# Release Notes: v1.1 MAMT Safety Upgrade

## Verification

- Contract validation: implemented through JSON Schema.
- MAMT compilation: implemented through role-agent contracts.
- Runtime safety: implemented through risk budgets, loop detection and circuit states.
- Credential isolation: implemented through scoped capability tokens.
- Muse integration: implemented as an honest manual bridge, with no unsupported API assumption.
- Witness Chain: implemented as digest-linked JSONL event records.
- Test status: 9 pytest tests passed in the build environment.

## CLI smoke path

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m wisegen_creative_engineering.cli validate examples/briefs/linkedin_social_creative.yaml
PYTHONPATH=src python -m wisegen_creative_engineering.cli run examples/briefs/local_ci_mission.yaml --output outputs/sample_run.json
PYTHONPATH=src python -m wisegen_creative_engineering.cli inspect outputs/sample_run.json
```
