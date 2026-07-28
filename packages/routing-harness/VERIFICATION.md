# Verification Record

**Release:** v1.1.0
**Verified:** 2026-07-28
**Runtime:** Node.js 22.22.2 (engines: >=20)
**Dependencies:** none

## Results

| Check | Command | Result |
| --- | --- | --- |
| Test suite | `node --test` | 10 passed, 0 failed |
| End-to-end scaffold | `node src/cli.mjs demo` | Completed |
| Config advisories | `node src/cli.mjs verify` | 3 advisories (expected: pricing unverified) |
| Witness chain integrity | `node src/cli.mjs witness` | Valid, 2 records |

## Tests covered

1. Schema validator accepts conforming objects, rejects type, enum, required and array-item violations
2. Strict JSON test rejects code fences and preambles
3. Leaf node counting
4. Witness chain appends, verifies, and detects tampering
5. Aggregation computes compliance rate; cost metric returns null when pricing is unset
6. Router refuses to certify from mock evidence
7. Router refuses to certify below the minimum trial count
8. Router certifies live evidence above thresholds and prefers lower cost per validated node
9. Router escalates when no candidate meets the compliance threshold
10. Build lane reports as delegated and is never routed by this harness

## Observed guard behaviour in the scaffold run

- `mock-flaky` recorded the lowest cost per validated node but fell below the 98 percent compliance threshold and was correctly excluded from ranking rather than selected on price.
- The winning candidate was blocked from the production routing matrix by `certify_from_mock_evidence`.
- The build lane returned `delegated` without a routing decision.
- Three pricing advisories were raised, which is the expected state of a release shipped without provider prices.

## Not verified in this release

Live provider calls. The Anthropic, OpenAI and xAI adapters are written against each provider's documented request shape but have not been executed against live endpoints in this environment. Verify model identifiers, structured-output field names and pricing against current provider documentation before the first certification run.
