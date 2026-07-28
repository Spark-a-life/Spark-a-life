# Capability Design Rationale

## Why three capabilities, not one

A single `maie.hrbp-sizing` capability would have to carry the risk ceiling of its most consequential operation, forcing routine signal ingestion through the same high-tier gate as a coverage recommendation. Splitting the work lets each stage carry its own tier, which is the difference between governance that people follow and governance they route around.

| Capability | Tier | Gate behaviour |
| --- | --- | --- |
| `maie.demand-signal-harvest` | medium | Human approval, witness record |
| `maie.work-distribution-analysis` | medium | Human approval, witness record |
| `maie.coverage-model-recommend` | high | Human approval, second review, witness record |

The dependency is one-directional: the recommender consumes the outputs of the other two and cannot be invoked without them.

## The data ceiling decision

MAIE holds a `confidential` ceiling. Employee relations data at individual level, with case narratives and identifiers, arguably belongs at `highly-confidential`, which only PAIE carries.

Two options were available. Raise the MAIE ceiling, or aggregate before ingestion. This overlay takes the second.

**Reasoning.** Raising an estate's ceiling to accommodate one capability widens the blast radius for every capability that estate will ever hold. Aggregation costs almost nothing analytically, because the rubric operates on unit-level rates rather than case detail, and it removes the PDPA exposure at the point of ingestion rather than managing it downstream. `assertIngestable` enforces this in code: prohibited fields are rejected, and units below a minimum cell size of 20 are reported as insufficient rather than scored.

The sample portfolio includes a 14-person legal unit specifically to exercise that exclusion. Small-cell suppression is standard practice in workforce analytics for a reason: at that size, a unit-level ER rate is effectively an individual disclosure.

## Why the recommender is tiered high

The MAIE estate declares a human gate over employment-impacting recommendations. A coverage model recommendation is employment-impacting even when it recommends adding capacity, because the same instrument that says "dedicated" for one unit says "shared services" for another, and the second reads as a reduction to the people in it.

The capability therefore carries `human_approval_for: ["all"]` and a high risk ceiling, and `output_constraints.never_outputs` prohibits headcount targets, named role eliminations and redeployment lists. The system describes demand and recommends a coverage shape. Converting that into an employment decision is a human act with statutory consequences in Singapore, and the denial `headcount_reduction_directive` blocks the system from taking it.

## Why scoring is deterministic and routing is certified

The arithmetic is not a model task. Weighted sums must be reproducible, inspectable and identical across runs, so `scripts/scorer.mjs` implements them directly. The test suite asserts determinism explicitly.

The model's role is narrower: extracting structured signals from unit briefs, which is genuinely a language task and genuinely variable across models. That extraction is what the GAIE routing harness benchmarks and certifies. The recommender declares a `routing_dependency` on a certified `extraction` route and may not select its own model, because `capability_self_certification` is a constitutional denial.

This split is worth stating plainly because it inverts the common pattern. Most AI-for-HR tooling puts the model in the judgement seat and the deterministic code in the plumbing. Here the deterministic code makes the judgement reproducible, and the model does the reading.

## The CAF-OS transposition

The scoring output contract is lifted from the CAF-OS capability router, which scores each shot across weighted dimensions and returns a recommended engine, an alternative, rationale, risk and confidence. The transposition is exact:

| CAF-OS shot routing | MAIE coverage routing |
| --- | --- |
| character count, pose change, dialogue, camera complexity, motion, occlusion | change load, manager capability gap, ER intensity, structural ambiguity, workforce volatility, industrial relations load |
| cost, latency, editability | population modifier, evidence freshness, completeness |
| recommended engine, alternative, rationale, risk, confidence | coverage recommendation, alternative, rationale, risk, confidence |
| Captain's Gate before release | Captain's Gate before recommendation |

Same architecture, different domain. That is the reusability claim the WiseGen estate model makes, demonstrated rather than asserted.

## Headcount as a bounded modifier

The population modifier is capped at plus or minus 0.5 on a ten-point index, log-scaled against median unit size. This is the argument made structural: headcount is real, so it is not excluded, but it cannot outweigh demand.

The sample portfolio demonstrates the consequence. Manufacturing at 780 staff scores 2.47 and lands in shared services. Logistics at 410 staff scores 7.17 and lands in dedicated. A ratio-based model would have reached the opposite conclusion, and would have been defensible in a budget deck the whole way there.

## What the rubric does not claim

The weights are a starting calibration reflecting professional judgement. They have not been fitted against outcome data and the rubric is marked `provisional` in config, surfaced in every scored output, and capped at 0.95 confidence for that reason.

This matters for the argument, not just for honesty. The critique of the employee-to-HRBP ratio is that a legible number substituted for a real diagnosis. Shipping an equally unvalidated seven-dimension index and presenting it as rigorous would repeat the error with more decimal places. The first deployment is a calibration exercise: score the portfolio, compare against practitioner judgement, examine the disagreements, adjust the weights, and record what changed.
