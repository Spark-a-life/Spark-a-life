# The Captain's Gate

AI proposes. The human decides. This document is the contract that makes that sentence enforceable rather than aspirational.

## What the reviewer receives

A gate packet answers ten questions without further enquiry:

1. What changed
2. Why it changed
3. Which role changed it
4. Which model was used
5. Which tools were invoked
6. What evidence passed
7. What evidence failed
8. What risks remain
9. What deployment will cost
10. How to reverse the change

If a packet cannot answer all ten, the packet is defective, not the reviewer.

## Available actions

| Action | Meaning | Precondition |
|---|---|---|
| `approve` | Ship as presented | Packet ready |
| `approve_with_conditions` | Ship, with named follow-up obligations | Packet ready, conditions recorded |
| `reject` | Do not ship, close the mission | Always available |
| `request_revision` | Return with named deficiencies | Always available |
| `select_branch` | Ship one candidate | Packet ready, branch named |
| `combine_branches` | Ship a composition of candidates | Packet ready, composition described |
| `escalate` | Refer upward or outward | Always available |

Reject, request revision and escalate are always available. That asymmetry is deliberate: stopping must never be harder than proceeding.

## Readiness

```
ready = no blocking evidence failed
```

A packet that is not ready cannot be approved, cannot have a branch selected, and cannot reach deployment. `ApprovalService.decide` raises rather than warns. `tests/adversarial/test_authority.py::test_failing_evidence_blocks_approval` holds the line.

## What the Captain may not do

The Captain decides; the Captain does not generate. `kaie.captain` prohibits `generate_application`. A reviewer who authored the work is not reviewing it.

## What no role may do

No role other than the Captain may amend constitutional policy, approve a release, or deploy to production. This is asserted for every registered role in `tests/adversarial/test_authority.py::test_no_role_may_amend_constitutional_policy`.

## Unattended runs

The demonstrator runs with an unattended profile so the deployment path is exercised in CI. It records the decision explicitly as `captain (unattended demo profile)` and deploys in dry-run mode only. Two properties make this safe: the decision is never anonymous, and the profile cannot apply a release. In an attended run, the decision belongs to a named human and the record says so.

## Dual control

Set `FORGE_APPROVAL_MODE=dual-control` where organisational policy requires two signatures, for example production releases touching restricted data. The approval service then requires two distinct `decided_by` values before a packet is considered decided. Use it where the cost of a wrong approval exceeds the cost of a slower one.

## Evidence

Every submission and every decision is witnessed:

```
gate.submitted  packet id, readiness, packet digest
gate.decided    action, decided_by, rationale, conditions, selected branch
```

A decision without a rationale is refused at the API level. Recording who decided but not why produces an audit trail that cannot answer the only question an auditor asks.
