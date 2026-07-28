.PHONY: install test lint validate demo clean
install:
	pip install -e ".[dev]"
test:
	pytest -q
lint:
	ruff check src tests
validate:
	wisegen-pip validate examples/executive-brief/project.yaml
demo:
	wisegen-pip run examples/executive-brief/project.yaml
clean:
	rm -rf build .pytest_cache .ruff_cache
