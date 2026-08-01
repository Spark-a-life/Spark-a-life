.PHONY: install test lint validate run inspect review audit prompt preflight manifest export verify clean

install:
	python -m pip install -e .[dev]

test:
	pytest

lint:
	ruff check .

validate:
	wg-fund validate examples/missions/fundraising_500k_programme.yaml

run:
	wg-fund run examples/missions/fundraising_500k_programme.yaml --output outputs/fundraising_run.json

inspect:
	wg-fund inspect outputs/fundraising_run.json

review:
	wg-fund review examples/missions/fundraising_500k_programme.yaml

audit:
	wg-fund verify-audit outputs/witness_chain.jsonl

prompt:
	mkdir -p outputs
	wg-fund prompt --project-name wisegen-mamt-fundraising-suite --route zip > outputs/master_prompt_route_a.md
	wg-fund prompt --project-name wisegen-mamt-fundraising-suite --route no-zip > outputs/master_prompt_route_b.md

preflight:
	wg-fund preflight --output outputs/preflight.json

manifest:
	wg-fund manifest --output outputs/release_manifest.json

export:
	python scripts/export_repo_zip.py --output outputs/wisegen-mamt-fundraising-suite-v1.5.zip

verify: test lint validate run inspect audit preflight manifest

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info outputs/*.json outputs/*.jsonl outputs/*.md outputs/*.zip outputs/data_room
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
