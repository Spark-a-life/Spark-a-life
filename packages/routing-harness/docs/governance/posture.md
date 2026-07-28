# Governance Posture

## Estate placement

The harness sits in **GAIE**, the General Intelligence and Capability Forge Estate, whose declared purpose is to experiment, evaluate and forge reusable capabilities **without direct production authority**. That placement is deliberate. The harness decides which model is fit to be routed. It does not itself perform governed work, and it holds no authority over the estates that consume its decisions.

Registry entry:

```
capability.evaluate.routing
  owner_estate: GAIE
  risk_ceiling: low
  permitted_data_classifications: [public, internal]
  witness_chain: required
```

The reference dataset is synthetic and carries no personal data. If a real reference dataset is ever built from client material, it must be aggregated at unit level before ingestion and the capability's permitted classifications revisited.

## Constitutional alignment

| Principle | How the harness honours it |
| --- | --- |
| evidence-before-trust | Mock results are marked non-certifiable and blocked from the production matrix. Certification requires live provider evidence, verified pricing, and a minimum trial count. |
| bounded-authority | The harness proposes routes. It cannot expand its own permitted data classifications, cannot certify a capability, and cannot write to any estate's registry. |
| minimum-necessary-access | Public and internal classifications only. No client data, no personal data. |
| reversibility | The routing matrix is a plain JSON file and every change is witnessed with its evidence reference. Any route flip can be traced and reverted. |
| portability | Providers sit behind one adapter contract. Substituting or adding a vendor is a config change plus one adapter function. |

## Captain's Gate tier

Routing decisions are tiered **low**: no human approval, witness chain mandatory, no external side effects. This is defensible because a route change alters which model performs work, not what the work is permitted to do. The consuming capability's own risk tier still governs the work itself.

Two escalation paths are not automated by design:

1. **Escalate on no eligible candidate.** If no candidate meets the compliance threshold, the harness emits `decision: escalate` and routes nothing. It does not silently pick the least-bad option.
2. **Build-lane certification is delegated.** Routing between Sonnet and a Codex-class model for code generation is scored on test-pass rate against a Task Specification Card by the Build Lifecycle Orchestrator. This harness records the intent and defers the decision.

## Automatic denials

```
certify_from_mock_evidence
certify_without_pricing_for_cost_metric
certify_below_minimum_trials
```

These mirror the Captain's Gate denial pattern: conditions that produce a refusal rather than a warning, because each one would otherwise let a confident number stand in for absent evidence.

## What remains human

- Setting and periodically re-verifying provider pricing.
- Expert validation of the reference dataset, and any extension of it.
- Deciding whether a certified route is acceptable for a specific governed capability, which is a separate judgement from whether the model performed well on the benchmark.
- Any decision to raise the harness's data classification ceiling.
