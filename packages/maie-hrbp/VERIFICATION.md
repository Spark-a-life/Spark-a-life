# Verification Record

**Release:** v0.1.0
**Verified:** 2026-07-28
**Runtime:** Node.js 22.22.2
**Baseline:** WiseGen APE Intelligence OS v0.1.0
**Dependencies:** none

## Results

| Check | Result |
| --- | --- |
| Scorer test suite (`node --test`) | 11 passed, 0 failed |
| Capability entries vs `schemas/capability.schema.json` | 3/3 conform |
| Action requests vs `schemas/action-request.schema.json` | 5/5 conform |
| Live Captain's Gate evaluation | 5/5 decisions as designed |
| OS `verify` with overlay merged | valid, no configuration issues |
| OS test suite with overlay merged | passes |

## Captain's Gate decision paths exercised

| Request | Decision | Mechanism |
| --- | --- | --- |
| `action-request-harvest.json` | allow | Medium tier, approval recorded, classification within ceiling |
| `action-request-recommend.json` | allow | High tier, approval and second review references present |
| `action-request-denied.json` | deny | `headcount_reduction_directive` in automatic denials |
| `action-request-ceiling-breach.json` | deny | `highly-confidential` not in capability permitted classifications |
| `action-request-unapproved.json` | hold | `human_approval_for: ["all"]` with no approval recorded |

## Scorer behaviour verified

- Prohibited individual-level fields rejected before scoring
- Units below minimum cell size excluded rather than scored
- Band assignment follows the demand index
- A 120-person unit in crisis outranks a 900-person stable unit
- Population modifier stays within its declared bounds at both extremes
- Leakage caution fires above the operational share threshold
- Missing evidence lowers confidence and raises a caution
- Stale evidence lowers confidence
- Confidence capped at 0.95 while the rubric is provisional
- Scoring is deterministic across runs

## Sample portfolio result

```
Logistics         hc= 410  index=7.17  dedicated
Commercial        hc= 320  index=6.80  pooled
Regional office   hc= 340  index=5.28  pooled          risk=high  conf=0.40  (evidence gaps)
Customer service  hc= 620  index=5.24  pooled          leakage caution
Technology        hc= 150  index=4.88  pooled
Manufacturing     hc= 780  index=2.47  shared-services
EXCLUDED Corporate legal (headcount 14, below minimum cell size 20)
```

Manufacturing carries the largest population and the lightest coverage. Logistics carries roughly half the headcount and the heaviest. A ratio-based model would invert both.

## Not verified in this release

- The rubric weights against outcome data. The rubric is marked `provisional` and confidence is capped accordingly.
- Behaviour after the `second_review` patch in `docs/findings.md`. The expected-decision map in `scripts/verify-integration.mjs` reflects current unpatched gate behaviour and must be updated when the patch lands.
- Any live client data. The sample portfolio is synthetic.
