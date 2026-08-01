# Authoring a role

A role is a versioned authority contract, not a prompt. This is what makes the roster enforceable.

## The contract

```yaml
- id: gaie.backend-engineer          # <estate>.<role>, lowercase, hyphenated
  version: 1.0.0                     # semantic; a change in authority is a minor bump at least
  layer: forge                       # council | forge | command | commons | market
  role: Backend Engineer
  mandate: Build services against the specification, not against the conversation.
  exit_artefact: Service implementation and contract tests
  approval_gate: captain             # captain | assurance | self | none
  authority:
    allowed:
      - generate_application
      - execute_tests
    prohibited:
      - approve_release
      - deploy_production
      - modify_security_policy
  model_policy:
    capability: coding               # reasoning | coding | summarisation | classification
  evidence_requirements:
    - tests
    - static_analysis
```

## Rules the contract must satisfy

1. **No wildcard authority.** `allowed: ["*"]` is rejected by the contract tests.
2. **Allow and prohibit must not overlap.** An ambiguous contract is an unenforceable one.
3. **Prohibit is not decorative.** `prohibited` wins over `allowed` in `AgentDefinition.may()`, so it is the safe place to state a boundary you never want widened by a later edit.
4. **Every role names an exit artefact.** A role that produces nothing is a stance, not a role.
5. **Every role names its approval gate.** Who signs off on this role's output.
6. **Ids carry the estate prefix.** Authority should be readable at a glance: `kaie.` sovereign, `gaie.` forge, `paie.` command, `saie.` commons, `raie.` reasoning bridge, `taie.` market.

## Adding a role

Only when all four hold:

1. the stance is genuinely distinct from every existing role, not the same stance on a different topic;
2. it has an exit artefact nobody else produces;
3. its authority can be expressed as an allow list and a prohibit list;
4. its evidence requirements are testable.

Then:

```bash
# 1. add the contract to agents/registry.yaml
# 2. register a capability handler in pipeline._register_handlers
# 3. add authority tests
PYTHONPATH=src python3 -m unittest tests.contract.test_contracts tests.adversarial.test_authority
# 4. update docs/ROLES.md; the contract tests assert the two agree
```

The registry is versioned and owned by the Captain and the Policy Steward. A role change is a policy change.

## Capability handlers

The runtime binds a capability name to a handler:

```python
@runtime.handler("generate_application")
def generate(context: AgentContext) -> dict[str, Any]:
    # context.task, context.agent, context.tools, context.router
    return {"artefacts": [...], "evidence": [...]}
```

The runtime checks the contract, then policy, then witnesses the start, then calls the handler. A handler asked for a capability the role does not hold never runs.

## Model policy

`model_policy.capability` states what class of model the role needs, never which vendor. The router resolves capability to a concrete model by policy, risk tier and cost ceiling. Roles that name a vendor create the dependency the platform exists to avoid.
