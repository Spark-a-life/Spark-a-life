# AGENTS.md

## Cursor Cloud specific instructions

This repository is the **WiseGen estate front door** — the Spark-a-life GitHub profile README, documentation hub (GitHub Pages), and staging area for 7 software modules pending multi-repo split.

### Repository structure

- `README.md` — GitHub profile page and estate overview
- `docs/` — GitHub Pages site (Builder's Handbook with SEO, sitemap, robots.txt)
- `packages/` — 7 modules staged for independent-repo distribution (see `MULTI_REPO_SETUP.md`)
- `.github/workflows/` — GitHub Actions for Pages deployment, Sigstore releases, PyPI publishing

### Running tests

All modules have zero or near-zero external dependencies. No `npm install` or `pip install` is required for most modules.

**Python modules:**
- `packages/forge/` — `cd packages/forge && make test` (100 tests, Python 3.10+ stdlib only)
- `packages/omega/packages/omega/` — `cd packages/omega/packages/omega && pip install -e ".[dev]" && python3 -m pytest` (11 tests, needs PyYAML + jsonschema + Jinja2)

**Node.js modules (all require Node 20+, zero npm dependencies):**
- `packages/governed-execution/` — `node --test --test-reporter=spec test/*.test.js` (22 tests, 1 skipped browser test)
- `packages/routing-harness/` — `node --test tests/harness.test.mjs` (10 tests)
- `packages/maie-hrbp/` — `node --test tests/scorer.test.mjs` (11 tests)
- `packages/ape-intelligence-os/` — `node --test tests/*.test.mjs` (12 tests)
- `packages/caf-os/` — `node --test` (3 tests) + `npm run lint` for syntax check

### Running demos

- `cd packages/forge && make demo` — Spreadsheet-to-Application demonstrator with witness chain
- `cd packages/governed-execution && npm run demo` — 5 end-to-end execution cases (allow, hold, approve, block, browser)
- `cd packages/routing-harness && npm run demo` — Mock multi-model benchmark with routing decision
- `cd packages/ape-intelligence-os && npm run demo` — Source verification with Captain's Gate

### Key caveats

- The `omega` module has a nested structure: the Python package is at `packages/omega/packages/omega/`, not `packages/omega/`.
- The `governed-execution` demo starts a temporary HTTP server on a random port — it cleans up automatically.
- The `routing-harness` demo uses mock providers. Mock results carry `certifiable: false` by design — this is not a bug.
- `caf-os` and `ape-intelligence-os` are `private: true` — this is a deliberate governance decision, not an oversight.
- Use `python3` not `python` — the VM has Python available at `python3`.
