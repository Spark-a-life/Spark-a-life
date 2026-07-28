.PHONY: install test lint demo package
install:
	pip install -e ".[dev]"
test:
	pytest -q
lint:
	ruff check src tests

demo:
	wisegen-omega run examples/strategy_mission.yaml --output outputs/strategy_run.json
package:
	python scripts/export_repo_zip.py --output outputs/wisegen-ape-omega-v2.0.zip
