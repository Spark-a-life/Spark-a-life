# WiseGen MAIE HRBP Demand Intelligence

**Release:** v0.1.0
**Estate:** MAIE (Management and Organisational Intelligence Estate)
**Status:** Overlay for the WiseGen APE Intelligence OS v0.1.0
**Design rule:** The system describes demand and recommends a coverage shape. Employment decisions remain human.

The first capability set registered to MAIE. Before this overlay the estate was declared but had no capability, so its human gate over employment-impacting recommendations had nothing to gate.

## What this contains

| Path | Purpose |
| --- | --- |
| `config/capabilities.maie.json` | Three capability manifest entries, drop-in mergeable |
| `config/policies/captains-gate.maie-addendum.json` | Five MAIE-specific automatic denials |
| `config/demand-rubric.json` | Six-dimension demand index with bounded population modifier |
| `scripts/scorer.mjs` | Deterministic scorer with ingestion guards |
| `scripts/score-portfolio.mjs` | Score a portfolio and print the result |
| `scripts/verify-integration.mjs` | Merge into a real APE OS copy and exercise Captain's Gate |
| `examples/` | Five action requests covering allow, hold and three denial paths |
| `tests/scorer.test.mjs` | 11 tests |
| `docs/capability-design.md` | Tiering, data ceiling, CAF-OS transposition |
| `docs/findings.md` | Three findings against the baseline, with a patch |

## Capabilities

```
maie.demand-signal-harvest        medium   unit-aggregated ingestion, min cell size 20
maie.work-distribution-analysis   medium   strategic vs operational effort, tiering leakage
maie.coverage-model-recommend     high     coverage recommendation, human_approval_for: all
```

The recommender declares a `routing_dependency` on a certified `extraction` route from the GAIE routing harness. It may not select its own model.

## Run

```bash
node --test                                          # 11 tests
node scripts/score-portfolio.mjs                     # score the sample portfolio
node scripts/verify-integration.mjs <path-to-ape-os> # live Captain's Gate verification
```

## Integration verification

`scripts/verify-integration.mjs` copies a real APE Intelligence OS tree, merges this overlay, validates every capability entry and action request against the OS's own JSON Schemas, then evaluates the examples through the actual `CaptainsGate` and `CapabilityRegistry` classes. It finishes by running the OS's own `verify` command and test suite with the overlay merged.

Verified result against v0.1.0:

```
3 capabilities added, 5 denials merged
capability entries          3/3 conform
action requests             5/5 conform
Captain's Gate              5/5 decisions as designed
  harvest                   allow
  recommend                 allow
  headcount directive       deny   (automatic denial)
  ceiling breach            deny   (data classification not permitted)
  unapproved recommend      hold   (human approval required)
OS verify                   valid, no configuration issues
OS test suite               passes with overlay merged
```

## Merge procedure

1. Append the three entries in `config/capabilities.maie.json` to the `capabilities` array of the OS `config/capabilities.json`.
2. Append the five action names in `config/policies/captains-gate.maie-addendum.json` to `automatic_denials` in the OS `config/policies/captains-gate.json`.
3. Run `node src/cli.mjs verify` in the OS to confirm no configuration issues.

`scripts/verify-integration.mjs` performs all three against a temporary copy, so run it before merging into a live tree.

## Before production use

- The demand rubric is marked `provisional`. Weights encode professional judgement and have not been fitted against outcome data. Treat first deployment as calibration.
- Apply the `second_review` patch in `docs/findings.md`, or the high tier on the recommender behaves identically to medium.
- Confirm a certified `extraction` route exists in the GAIE routing harness before invoking the recommender.
- Confirm the minimum cell size of 20 meets your PDPA position for the units in scope.

Start with the work. Keep the human accountable.
