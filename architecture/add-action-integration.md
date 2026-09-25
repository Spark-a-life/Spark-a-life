# Weaving AIOS v1.2 into Add Action

## Executive verdict

**CONDITIONALLY PURSUE as a design.** Assuming "Add Action" means the Add Action section of a Custom GPT builder, AIOS v1.2 must not be moved into the Action itself. AIOS remains the governance and reasoning layer that decides whether an Action is allowed to progress. The Action, when implemented, is a tightly bounded execution interface.

This is a docs-only snapshot. There is no implemented Action Gateway, identity service or approval service in this repository. Consequential external execution is not enabled.

## Recommended architecture

**Human intent → AIOS evaluation → Action risk classification → Proposal → Preflight → Human authorisation where required → Execution integrity check → Action Gateway (when implemented) → Technical receipt → Outcome verification → Witness Chain → Learning**

| Stage | Responsibility |
|---|---|
| AIOS v1.2 four layers | Decide whether the proposed commitment makes sense |
| Layer 0 | Purpose, privacy, access, retention and practice boundary |
| Evidence protocol | Establish what is known, uncertain or contradicted using v1.2 evidence states |
| Opportunity Quality | Test mandate, authority, sponsor, resources and downside |
| Circuit breakers | Stop progression when structural conditions fail |
| Action class | Green / Amber / Red / Prohibited |
| External Action Protocol | `governance/AIOS_v1.2.md` §26, extracted as `governance/EXTERNAL_ACTION_PROTOCOL.md` |
| Add Action / API | Perform only the authorised operation, if a gateway exists |
| Witness Chain | Record what was proposed, authorised, executed, observed and reconciled |
| Learning loop | Compare intended, authorised and observed effects |

This is stronger than giving a GPT direct access to email, CRM, calendars or document systems and relying on prompting alone to keep it disciplined.

Governed Action is an operational stage, not a fifth evaluation layer. The four layers answer "Should we?". The operational stage answers "Having decided, how do we act without losing control and provenance?".

## What to put behind Add Action

Rather than exposing dozens of business-system operations directly, the specified **AIOS Action Gateway** has four operations:

| Operation | Purpose | Side effect? |
|---|---|---:|
| `preflightAction` | Test whether an intended external action is sufficiently evidenced, scoped and authorised | No |
| `proposeAction` | Create an immutable proposal and return a `proposal_id` | No external commitment |
| `executeApprovedAction` | Execute exactly the approved proposal | Yes, only if implemented and authorised |
| `getActionReceipt` | Retrieve execution result and Witness Chain information | No |

The draft schema is `actions/openapi/aios-action-gateway.yaml`. It is non-functional until implemented. Server: `https://example.invalid`.

The gateway, when built, is the controlled interface between the GPT and whatever sits behind it: CRM, email, calendar, document repository, workflow engine or another API. Opportunity databases and client corpora must not live in this repository.

## The action envelope

Every consequential action carries the §27.1 envelope. Canonical binding field is `proposal_digest`.

The model must not be able to manufacture `human_authorisation=true` and thereby authorise itself. Authorisation is enforced by a future Action service, not merely expressed in the prompt. This snapshot is Declared, not Enforced.

## How AIOS v1.2 governs an Action

Suppose the GPT concludes that a hiring manager should be sent a proposal committing to an enterprise programme.

Without AIOS, that may become an unbound send operation.

With AIOS, the system first asks:

**Capability:** Is the proposed contribution evidenced?

**Context:** Does the evidence transfer into this organisational environment?

**Opportunity Quality:** Is mandate, authority, sponsorship, access and resourcing sufficient?

**Strategic Position:** Is this commitment the right way to position the Human Captain?

**Layer 0 and circuit breakers:** Are purpose, privacy, access, IP and window-dressing conditions satisfied?

**Class:** Green, Amber, Red or Prohibited?

Only then may it formulate an Action Proposal. Prohibited stops. Amber and Red require externally verifiable approval bound to the digest.

The system does not merely ask "May I send this?". It asks whether this is the right commitment, supported by adequate evidence, within mandate, authority and risk boundaries, and whether the Human Captain has authorised this exact external consequence.

## Canonical protocol

The governing protocol is `governance/AIOS_v1.2.md` §26. The extracted copy is `governance/EXTERNAL_ACTION_PROTOCOL.md`. This architecture note must not duplicate or independently modify that protocol.

## First implementation: record before act

Phase 1 should persist:

Opportunity Case → Finding Register → Unknowns → Opportunity Quality Register → Decision → Gate and Layer 0 results → Witness Chain

Only in a later phase, after RELEASE_GATE.md is complete, should a gateway execute external commitments.

Do not initially expose generic endpoints such as send-anything, update-anything or run-workflow. Narrow operation boundaries make governance materially easier.

Platform-level user approval is an additional safety control, not a replacement for the External Action Protocol and server-side policy enforcement.

## Recommended design

AIOS v1.2 = intelligence and constitutional layer.  
External Action Protocol = authority and execution-integrity layer.  
Add Action = execution adapter, when implemented.  
Witness Chain = accountability and learning layer.

Do not let "agentic" become "autonomous".

## Suggested next artefact (not in this snapshot)

An implemented Action Gateway with identity, approval, policy, idempotency, reconciliation and verified Omega tests. That is a different artefact class.

## Source basis

Files that exist in this repository:

- `governance/AIOS_v1.2.md`
- `governance/EXTERNAL_ACTION_PROTOCOL.md`
- `governance/EVIDENCE_GOVERNANCE_AND_WITNESS_CHAIN.md`
- `governance/OUTPUT_SCHEMAS_AND_DECISION_REGISTERS.md`
- `actions/openapi/aios-action-gateway.yaml`
- `actions/schemas/action-proposal.schema.json`
- `actions/schemas/approval.schema.json`
- `actions/schemas/witness-event.schema.json`
- `archive/superseded/AIOS_v1.1.md`
- `prompts/system-instructions/CreateGPT_System_Instruction_v1.2.txt`
