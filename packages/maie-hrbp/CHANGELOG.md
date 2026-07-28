# Changelog

## v0.1.0 (2026-07-28)

First capability set registered to the MAIE estate.

### Added
- Three capability manifest entries: demand signal harvest (medium), work distribution analysis (medium), coverage model recommend (high).
- Five MAIE-specific automatic denials operationalising the estate human gate.
- Provisional six-dimension demand rubric with a bounded population modifier.
- Deterministic scorer with prohibited-field and minimum-cell-size guards.
- Integration verifier that exercises the real Captain's Gate and capability registry.
- Eleven scorer tests and five example action requests covering allow, hold and three denial paths.

### Findings raised against the baseline
- `second_review` declared for the high risk tier is never read by the gate implementation.
- The capability schema omits two fields the registry dereferences at runtime.
- The registry previously held no MAIE capability, leaving the estate human gate unreachable.
