# WiseGen Forge task runner. No network, no installs required.
PY ?= python3
export PYTHONPATH := src

.PHONY: help doctor demo test lint typecheck roles verify export clean release-check all

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":.*?## "}; {printf "  \033[1m%-14s\033[0m %s\n", $$1, $$2}'

doctor: ## check environment and repository readiness
	$(PY) -m wisegen_forge.cli doctor

roles: ## print the role roster
	$(PY) -m wisegen_forge.cli roles

demo: ## run the reference Spreadsheet-to-Application demonstrator
	$(PY) -m wisegen_forge.cli demo

test: ## run the full test suite
	$(PY) -m unittest discover -s tests -t . -v

lint: ## lint (skipped when ruff is absent)
	@command -v ruff >/dev/null 2>&1 && ruff check src tests || echo "ruff not installed, skipping"

typecheck: ## type check (skipped when mypy is absent)
	@command -v mypy >/dev/null 2>&1 && mypy src || echo "mypy not installed, skipping"

verify: ## verify the demo witness chain
	$(PY) -m wisegen_forge.cli verify --run .forge/demo

export: ## craft the portable ownership bundle from the demo run
	$(PY) -m wisegen_forge.cli export --run .forge/demo --out dist/portable-bundle.zip

release-check: doctor test demo verify ## the gate a release must pass
	./scripts/verify-release.sh

clean:
	rm -rf .forge dist build **/__pycache__ .mypy_cache .ruff_cache

all: doctor lint typecheck test demo verify
