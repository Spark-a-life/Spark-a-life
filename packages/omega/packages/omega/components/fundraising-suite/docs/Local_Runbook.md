# Local Runbook

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
wg-fund validate examples/missions/fundraising_500k_programme.yaml
wg-fund run examples/missions/fundraising_500k_programme.yaml --output outputs/fundraising_run.json
wg-fund inspect outputs/fundraising_run.json
python scripts/export_repo_zip.py --output outputs/wisegen-mamt-fundraising-suite.zip
```

The reference run should produce a local JSON run artefact and append material events to `outputs/witness_chain.jsonl`.
