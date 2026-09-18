# Changelog

## 1.2.0-alpha - 2026-09-18 (this snapshot)

### Honest status
Docs-only governance snapshot. Not a runtime. Not a complete product. Not approved for production external execution. Markdown files under `tests/` are acceptance specifications, not a passing regression suite. The OpenAPI file is a draft non-production schema and is non-functional until implemented.

### Added
- Canonical specification `governance/AIOS_v1.2.md` (control-complete reconstruction of the review-time `AIOS v1.2.md`; replace with the original 63,543-byte file if still held).
- Sixteen-step External Action Protocol generated from v1.2 §26.
- Prohibited action class, Layer 0, immutable `proposal_digest`, externally verifiable approval fields, and three-way reconciliation in derived docs and schemas.
- Sanitised fictional examples under `actions/examples/`.
- Receipt schema separate from the Witness event schema.
- v1.2 system instruction (Declared, not Enforced).
- All-rights-reserved `LICENSE`.
- `.env.example` with placeholder names only.

### Changed
- Packaged v1.1 kernel moved to `archive/superseded/AIOS_v1.1.md`.
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
