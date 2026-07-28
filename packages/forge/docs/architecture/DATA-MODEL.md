# Canonical data model

The architecture revolves around durable objects, not chat history. A conversation is not an artefact that survives a staffing change.

## The objects

| Object | Purpose | Written by |
|---|---|---|
| Organisation, Workspace, User, Role | Who is acting and under whose authority | Identity |
| Project, Mission | The unit of work and its execution plan | Project Service |
| Specification | The authoritative statement of what is to be built | Intent Compiler |
| Decision | A recorded human choice, with rationale | Approval Service |
| Task, Execution | Planned work and what actually happened | Orchestration Engine |
| Agent, Capability, Tool | Who may do what, with which instrument | Agent Runtime, Tool Gateway |
| Policy | The rules that bind all of the above | Policy Engine |
| Artefact | Anything produced: code, schema, manifest, document | Forge roles |
| Evidence, Evaluation | Proof that an artefact satisfies its contract | Evaluation Engine, Witness |
| Approval | The gate decision itself | Approval Service |
| Release, Deployment | What shipped, where, and how to reverse it | Deployment Service |
| Incident | What went wrong and what was done | Platform Operator |
| LearningRecord | What the run teaches, pending a governed gate | Commons Librarian |

## The envelope

Every object carries the same governance envelope, implemented in `domain.Envelope`:

```yaml
id: spec-4c180bd79f6f       # stable identifier
kind: Specification
version: 1.0.0              # bumped on every lifecycle transition
owner: captain
created_at: 2026-07-25T00:49:00+00:00
created_from: intake-9e5daf # provenance, never inferred later
classification: confidential # public | internal | confidential | restricted
lifecycle_state: approved
evidence_refs: [sha256:...]
policy_refs: [constitutional.captain-rule.0]
retention_rule: retain-7y
schema_version: 0.1.0
```

Three properties are non-negotiable.

**Transitions do not mutate.** `transition()` returns a new object at a bumped version. The prior version stays intact, so a reviewer can reconstruct what an object looked like when a decision was taken on it.

**Digests are canonical.** Object digests are computed over sorted, separator-normalised JSON, so two semantically identical objects hash identically regardless of key order.

**Classification travels.** A field classified `restricted` at intake stays restricted through the specification, the generated schema, the masking rules in the generated application and the retention rule on the evidence. Classification that stops at the door is theatre.

## Lifecycle states

```
draft -> proposed -> approved -> executing -> verified -> released
                 \-> rejected            \-> superseded -> archived
```

An object cannot skip to `released` without passing `verified`, and nothing reaches `approved` without a Decision object naming a human.

## Retention

Retention rules are inherited from organisational policy, not chosen per project. The default is seven years for evidence and decisions, aligned with Singapore statutory record-keeping expectations. Personal data carried in intake is retained under the shorter of the project rule and the data-subject purpose limitation, and evidence records reference identifiers rather than payloads so that expiry of the former does not break verification of the latter.
