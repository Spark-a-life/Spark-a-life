# AGENTS.md

## Governance protocol — mandatory for all agents

### Pre-push gate (Captain's Gate)

**No commit and no push without explicit human signoff.** This is non-negotiable.

The required sequence for every change:

1. **Stage and describe** — prepare changes and present a clear summary to the Captain
2. **Security scan** — before requesting signoff, scan all staged content for:
   - Personal names (individuals)
   - Organisation names (companies, institutions)
   - Email addresses, API keys, tokens, credentials
   - Strategic intelligence, internal planning, unratified assessments
3. **Captain reviews** — the human inspects, amends, or rejects
4. **Captain says "push"** — only the explicit word authorises the push
5. **Agent executes** — only after authorisation

Failure to follow this sequence is a governance violation.

### No personal names, no organisation names

**Never commit or push content that contains the names of individuals or organisations** unless:
- The name is the repository owner's own public identity (already published by them)
- The Captain has explicitly authorised that specific name for public distribution

This applies to:
- Source code, comments, and documentation
- Intelligence briefs, case studies, and strategic documents
- Commit messages and PR descriptions
- Any file added to the repository

When in doubt, redact. Use `[Source redacted]`, `[Organisation redacted]`, or equivalent markers. The `.gitignore` contains patterns that block known unredacted intelligence brief filenames as an additional safeguard.

### Intelligence brief handling

- Only `*-redacted.md` files are permitted in `docs/intelligence-briefs/`
- Unredacted originals must never enter the repository — they belong in the private Governed Intelligence Library
- The `.gitignore` enforces this with filename pattern blocks
- Before committing any intelligence brief, verify zero personal names and zero organisation names appear in the content

## Cursor Cloud specific instructions

This repository is the **WiseGen estate front door** — the profile README, documentation hub (GitHub Pages), and staging area for 7 software modules pending multi-repo split.

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
