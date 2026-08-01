# Role Charter: Design to Fruition

**WiseGen Forge v1.0.0**

This charter names the roles that carry a WiseGen Forge engagement from a sentence of intent to a deployed, owned, reversible system. Roles are executable: each one exists as a versioned contract in `agents/registry.yaml`, is loaded by the agent runtime, and is bound by the policy engine at run time. A role that cannot be enforced is decoration, so nothing here is aspirational.

Three rules govern the whole roster.

1. **The Captain decides.** Every consequential action terminates at a human approval gate. No agent may approve its own work, and no agent may amend constitutional policy.
2. **Authority is scoped, not assumed.** Each role carries an explicit allow list and prohibit list. The tool gateway denies by default; capability is granted per task, per run.
3. **Completion is evidentiary.** A role exits by producing its named artefact and the evidence that the artefact satisfies its acceptance criteria. Self-reported completion has no standing.

---

## 1. Layer map

| Layer | Estate | Standing | Function |
|---|---|---|---|
| Council | Kaie Sovereign, Paie Command | Always active, cannot be bypassed | Authority, truth, security, policy, budget, reversal |
| Forge | Gaie Forge | Activated per mission | Intent compilation, architecture, generation, assurance |
| Command | Paie Command | Activated at release | Packaging, deployment, operation |
| Commons | Saie Commons, Raie | Activated at close | Reuse, learning, human translation |
| Market | Taie Market | Activated at engagement boundaries | Framing, packaging, client fit |

---

## 2. The roster

### Council (7 roles, continuous)

| Role | Id | Mandate | Exit artefact |
|---|---|---|---|
| **Captain** (human principal) | `kaie.captain` | Decide. Approve, reject, revise, select or combine candidate branches, escalate. | Signed Captain's Gate decision |
| **Epistemic Sentinel** | `kaie.sentinel` | Flag any claim not traceable to evidence, observation or an explicit decision, and any drift between what is optimised and what the engagement is for. | Verification and value-drift report |
| **Gate Steward** | `kaie.gatekeeper` | Assemble the gate packet so the reviewer sees what changed, why, by whom, on what evidence, at what cost, and how to reverse it. | Gate packet |
| **Security Auditor** | `kaie.security-auditor` | Treat the model as an untrusted executor. Validate inputs, tools, credentials, agent identity and context persistence before anything ships. | Static analysis and threat findings |
| **Policy Steward** | `kaie.policy-steward` | Own policy-as-code. Constitutional rules are amended by the Captain alone, never by an agent mid-run. | Policy change record |
| **Telemetrist** | `paie.telemetrist` | Keep budgets, traces and refusals visible in real time. Escalate at threshold, halt at cap. | Cost and telemetry snapshot |
| **Contingency Officer** | `paie.contingency` | Own the reversal path. Every consequential action has a tested way back before it is taken. | Rollback plan and incident record |

The Council is the reason this is a factory rather than a generator. It runs at every stage, including stages it did not initiate.

### Forge (8 roles, per mission)

| Role | Id | Mandate | Exit artefact |
|---|---|---|---|
| **Intent Compiler** | `gaie.intent-compiler` | Convert loose intent, documents and datasets into a specification with users, outcomes, constraints and acceptance criteria. Refuse to proceed on unstated acceptance criteria. | Executable specification |
| **Solution Architect** | `kaie.architect` | Craft the architecture, threat model, data classification, model selection, cost envelope, test strategy and rollback strategy as one artefact. | Architecture decision record |
| **Data Engineer** | `gaie.data-engineer` | Infer schema from real organisational artefacts, assess data quality, classify sensitivity, and design migrations. | Data model and quality report |
| **Backend Engineer** | `gaie.backend-engineer` | Build services against the specification, not against the conversation. | Service implementation and contract tests |
| **Interface Engineer** | `gaie.frontend-engineer` | Build the human surface, including the states that failure produces. | Interface implementation |
| **Integration Engineer** | `gaie.connector-engineer` | Mediate every external system through the connector contract. No direct calls, no unlogged side effects. | Connector and integration tests |
| **Adversarial Engineer** | `gaie.adversary` | Attack the candidate before the customer does: injection, privilege escalation, data leakage, silent failure, cost exhaustion. | Adversarial findings |
| **Assurance Engineer** | `kaie.assurance-engineer` | Run the quality gates and declare the acceptance contract satisfied or not. Never both. | Evaluation report |

### Command (2 roles, at release)

| Role | Id | Mandate | Exit artefact |
|---|---|---|---|
| **Release Engineer** | `paie.release-engineer` | Package signed, reversible releases. Deployment happens through manifests, never through conversation. | Release manifest and runbook |
| **Platform Operator** | `paie.operator` | Run the deployed estate: health, drift, incident response, kill switch. | Operations log and incident record |

### Commons and Market (3 roles, at close and boundary)

| Role | Id | Mandate | Exit artefact |
|---|---|---|---|
| **Commons Librarian** | `saie.librarian` | Turn one-off outputs into reusable templates, patterns and learning records, without letting production behaviour change itself. | Template or learning record |
| **Principal Mediator** | `raie.mediator` | Translate between the machine record and the human principal. State plainly what was decided, what remains open, and what the decision costs. | Principal briefing |
| **Solution Lead** | `taie.solution-lead` | Hold the client frame: what problem is worth solving, what is out of scope, what the customer must own afterwards. | Engagement charter and scope boundary |

---

## 3. The journey, stage by stage

Each stage names its lead role, its Council overlay, its gate and its exit artefact. The pipeline in `src/wisegen_forge/pipeline.py` implements these stages in this order.

| Stage | Lead | Council overlay | Gate | Exit artefact |
|---|---|---|---|---|
| 0. Frame | Solution Lead | Sentinel, Policy Steward | Captain ratifies scope | Engagement charter |
| 1. Intake | Intent Compiler | Security Auditor scans inputs | Automatic, provenance required | Immutable intake record |
| 2. Intent compilation | Intent Compiler | Sentinel checks unverified claims | **Captain approves the specification before any generation** | Specification |
| 3. Architecture and risk | Solution Architect | Security Auditor, Telemetrist | Captain approves the cost envelope and estate | Architecture decision record, threat model |
| 4. Mission planning | Solution Architect | Telemetrist sets budget | Automatic within budget | Dependency graph |
| 5. Branchable execution | Backend, Interface, Data, Integration Engineers | Contingency prepares reversal, Telemetrist meters | Automatic within authority | Candidate branches, separately costed |
| 6. Continuous verification | Assurance Engineer, Adversarial Engineer | Sentinel, Security Auditor | Hard gate: fail closed | Evaluation report |
| 7. Captain's Gate | Gate Steward assembles, **Captain decides** | Full Council | **Human decision, recorded** | Signed decision |
| 8. Deployment | Release Engineer | Contingency, Security Auditor | Manifest signed, rollback named | Release manifest |
| 9. Operation and learning | Platform Operator, Commons Librarian | Telemetrist, Sentinel | Captain approves any policy or template change | Learning record |

Two stages are non-negotiable human gates: stage 2 (nothing is generated against an unapproved specification) and stage 7 (nothing ships without a recorded decision). Everything else can be automated within bounded authority.

---

## 4. Responsibility assignment

R = responsible, A = accountable, C = consulted, I = informed. The Captain is accountable at every stage by constitutional design; the table shows where the Captain is also the actor.

| Stage | Captain | Sentinel | Security | Telemetrist | Contingency | Forge roles | Command roles | Commons |
|---|---|---|---|---|---|---|---|---|
| Frame | A, R | C | I | I | I | I | I | I |
| Intake | A | C | R | I | I | R | I | I |
| Intent | A, R | R | C | I | I | R | I | I |
| Architecture | A | C | R | R | C | R | C | I |
| Planning | A | I | C | R | C | R | I | I |
| Execution | A | C | C | R | R | R | I | I |
| Verification | A | R | R | C | C | R | I | I |
| Gate | A, R | C | C | C | C | I | I | I |
| Deployment | A | I | C | C | R | I | R | I |
| Operation | A | C | C | R | R | I | R | R |

---

## 5. Best-fit assignment in a small practice

A sole proprietorship does not staff twenty people. The roster is still correct, because the roles are separations of *stance*, not headcount. The realistic assignment is:

| Bearer | Roles held |
|---|---|
| **Human principal (Dr Will)** | Captain, Solution Lead, and final Policy Steward. These three are never delegated. |
| **Reasoning-class model** | Sentinel, Solution Architect, Adversarial Engineer, Principal Mediator |
| **Coding-class model** | Backend, Interface, Data, Integration Engineers, Intent Compiler |
| **Deterministic code, no model** | Gate Steward, Telemetrist, Contingency Officer, Assurance Engineer, Release Engineer, Security Auditor (static passes), Commons Librarian |
| **Human plus operator tooling** | Platform Operator |

The third row is the important one. Six roles carry no model dependency at all: they are arithmetic, hashing, schema validation and policy evaluation. Governance that depends on a model behaving well is not governance. In this repository those six are implemented as ordinary Python with tests, which is why the guarantees hold offline.

**Separation of duties, enforced:** the role that generates never approves; the role that approves never generates; the role that meters cost never spends; the role that audits never deploys. `tests/adversarial/` contains the tests that prove these separations cannot be crossed by configuration.

---

## 6. Handoff contract

Every handoff between roles carries the same envelope, defined in `packages`-equivalent form in `src/wisegen_forge/domain.py`:

```
handoff:
  from_role: gaie.backend-engineer
  to_role: kaie.assurance-engineer
  object_type: Artefact
  object_id: art-...
  version: 1
  produced_by_model: <provider>/<class> or none
  tools_invoked: [...]
  evidence_refs: [...]
  policy_decisions: [...]
  cost: {tokens, tool_calls, seconds, sgd}
  witness_ref: sha256:...
```

A handoff missing `evidence_refs` or `witness_ref` is rejected by the runtime. This is what makes the chain reconstructable months later by someone who was not present.

---

## 7. Adding a role

Do not add a role because a task looks unowned. Add one only when all four hold:

1. the stance is genuinely distinct from every role above (not the same stance with a different topic);
2. it has an exit artefact nobody else produces;
3. its authority can be expressed as an allow list and a prohibit list;
4. its evidence requirements are testable.

Then follow `docs/agent-authoring/AGENT-CONTRACTS.md`, register the contract in `agents/registry.yaml`, and add its authority tests. The registry is versioned; role changes pass the Captain like any other policy change.

---

*WiseGen Forge role charter v1.0.0. Control meets compassion: systematic rigour in service of human dignity.*
