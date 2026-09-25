# Changelog

## 1.2.0-alpha - 2026-09-25 (follow-up)

### Honest status
Re-searched this VM, uploads, artifacts, git objects and prior-session transcripts for the original packaged `AIOS_v1.1.md` (969 lines / 24,042 bytes, sha256 `8eb81d6906a2a9b19f6e07a314eafef9059aedc338d7d16121ab17ffda512b13`). Not recovered. Archive header, README and this changelog now state reconstructed stand-in explicitly. No runtime change. `production_external_execution` remains false.

## 1.2.0-alpha - 2026-09-18 (this snapshot)

### Honest status
Docs-only governance snapshot. Not a runtime. Not a complete product. Not approved for production external execution. Markdown files under `tests/` are acceptance specifications, not a passing regression suite. The OpenAPI file is a draft non-production schema and is non-functional until implemented.

### Added
- Canonical specification `governance/AIOS_v1.2.md` (original `AIOS v1.2.md`: 1,886 lines, 63,543 bytes).
- Sixteen-step External Action Protocol generated from v1.2 §26.
- Prohibited action class, Layer 0, immutable `proposal_digest`, externally verifiable approval fields, and three-way reconciliation in derived docs and schemas.
- Sanitised fictional examples under `actions/examples/`.
- Receipt schema separate from the Witness event schema.
- v1.2 system instruction (Declared, not Enforced).
- All-rights-reserved `LICENSE`.
- `.env.example` with placeholder names only.

### Changed
- v1.1 kernel archived at `archive/superseded/AIOS_v1.1.md` as a reconstructed stand-in; the original 969-line / 24,042-byte packaged file was not available.
- v1.0 GPT instruction moved to `archive/superseded/`.
- Evidence vocabulary aligned to v1.2 states.
- Formal Decision Record now includes Evidence assurance, Authority assurance and Permitted next action.
- Action states aligned to v1.2 (Indeterminate, not UNKNOWN as the canonical name).
- Threat model includes replay, cross-case substitution, credential leakage and silent fallback.
- Proposal schema `additionalProperties` is false and includes `action_class` with `PROHIBITED`.
- OpenAPI `$ref`s JSON Schema envelopes. Server remains `https://example.invalid`.
- ADRs expanded from stubs. ADR-004 names v1.2 §26 as protocol source.
- README layout claims match directories that exist.
- Tests labelled as markdown specifications / Custom-GPT prompt checks.

### Status
Alpha. Private-repo-ready after this alignment. Not approved for production external execution.

## 1.2.0-alpha - 2026-08-30 (original zip/bundle)

Original packaged overlay around a v1.1 kernel. Retained here only as history. That package was not consistent with `AIOS v1.2.md`.
