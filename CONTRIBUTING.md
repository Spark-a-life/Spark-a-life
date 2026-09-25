# Contributing

This repository is governance-first. It is a docs-only snapshot, not a runtime.

1. Do not silently modify `governance/AIOS_v1.2.md`. Derived files lose if they disagree with it.
2. `governance/EXTERNAL_ACTION_PROTOCOL.md` is generated from v1.2 §26 and must not diverge.
3. Create or update an ADR for consequential architectural changes.
4. Preserve evidence provenance and uncertainty. Use the v1.2 evidence states.
5. Update markdown acceptance specifications when a control changes. Do not describe them as a passing suite.
6. Update `CHANGELOG.md`, `VERSION` and `manifest.json` for releases.
7. Do not commit secrets, client records, CVs, opportunity corpora or unredacted case files.
8. Do not implement a fake Action Gateway in order to make tests appear to pass.
9. Do not enable consequential external execution.
10. Human Captain approval remains required for release decisions.
