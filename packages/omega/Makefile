.PHONY: setup test verify demo clean
setup:
	python3 scripts/check_python_deps.py
	node --version

test:
	cd packages/intelligence-os && npm test
	PYTHONPATH=packages/omega/src python3 -m pytest -q packages/omega/tests

verify:
	cd packages/intelligence-os && node src/cli.mjs verify
	PYTHONPATH=packages/omega/src python3 -m wisegen_omega.cli verify-audit outputs/omega-witness-chain.jsonl

demo:
	PYTHONPATH=packages/omega/src python3 scripts/run_governed_mission.py examples/governed-strategy-mission.yaml --output outputs/governed-mission.json --audit outputs/omega-witness-chain.jsonl

clean:
	rm -rf .pytest_cache outputs/*.json outputs/*.jsonl
