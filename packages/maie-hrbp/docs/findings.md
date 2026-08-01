# Findings Against the Baseline

## Finding 1: `second_review` is declared but never enforced

**Severity:** medium. A declared control that does not execute.

`config/policies/captains-gate.json` defines the high risk tier as:

```json
"high": {
  "human_approval": true,
  "witness_chain": true,
  "external_side_effects": false,
  "second_review": true
}
```

`src/governance/captains-gate.mjs` reads `tier.human_approval` and `tier.decision`. It never reads `tier.second_review`. A high-tier request with a single `human_approved: true` therefore returns `allow`, identically to a medium-tier request. The distinction between medium and high exists in policy and not in behaviour.

This surfaced while verifying `maie.coverage-model-recommend`, which is deliberately tiered high because coverage recommendations are employment-impacting. The integration run returns `allow` on a request carrying one approval, when the policy says two reviews are required.

**Why it matters here specifically.** The MAIE estate's human gate names employment-impacting recommendations as requiring a gate. If high tier collapses into medium tier at runtime, the strongest control the estate declares over its most consequential output is decorative. For a capability whose entire governance claim is that headcount-adjacent recommendations get more scrutiny, this is the control that has to work.

### Proposed patch

In `src/governance/captains-gate.mjs`, after the existing human approval check:

```javascript
const requires = tier.human_approval===true
  || capability.human_approval_for.includes("all")
  || capability.human_approval_for.includes(request.action);
if(requires && request.human_approved!==true)
  return {decision:"hold", reason:"Human approval is required before execution",
          obligations:["record_approval","append_witness_record"], capability};

// ADD:
if(tier.second_review===true && !request.second_review_reference)
  return {decision:"hold", reason:"Second review is required for this risk tier",
          obligations:["record_second_review","append_witness_record"], capability};
```

Add `second_review_reference` as an optional string property to `schemas/action-request.schema.json`. The example request `examples/action-request-recommend.json` in this overlay already carries the field, so it will continue to pass once the patch lands.

**Verification after patching.** `examples/action-request-recommend.json` should still return `allow`. A copy with `second_review_reference` removed should return `hold`. This overlay ships both expectations in `scripts/verify-integration.mjs` under the current unpatched behaviour, so update the expected map when you patch.

## Finding 2: the capability schema omits fields the registry requires

`schemas/capability.schema.json` requires eight fields. `CapabilityRegistry.assertUsable` additionally dereferences `permitted_data_classifications` and `human_approval_for`. A capability that validates against the schema but omits either field throws a `TypeError` at gate evaluation rather than a `GovernanceError`, which surfaces as an unhandled exception instead of a clean denial.

All three capabilities in this overlay carry both fields. The suggested fix is to add them to the schema's `required` array so the omission is caught at configuration time rather than at request time.

## Finding 3: the registry has no MAIE entries

Before this overlay, `config/capabilities.json` held three capabilities owned by TAIE, SAIE and GAIE. MAIE was defined as an estate with a purpose and a human gate, but had no capability through which that gate could ever be exercised. The estate was declared, not operational. This overlay is the first work that makes the MAIE human gate reachable.
