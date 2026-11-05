# Kernel interfaces

These are contracts. They are not implementations. Adapters may ignore interfaces they do not need. No adapter becomes a decision maker for another product.

When an adapter later causes material external effect, it must emit an AIOS Action Proposal and stop. The kernel does not execute.

## 1. EvidenceEnvelope

JSON Schema: `schemas/evidence-envelope.schema.json`

Use for any portable claim about an artefact, run, or finding.

Required: `claim`, `evidence_state`, `maturity`, `data_class`, `authority`, `source_ref`, `recorded_at`.

`evidence_state` uses the AIOS v1.2 set.  
`maturity` uses Declared / Implemented / Verified / Authorised.  
`authority` is `NONE_CONFERRED` unless a named human is recorded.

## 2. MaturityClaim

JSON Schema: `schemas/maturity-claim.schema.json`

Separates "the document says X exists" from "X exists on disk" from "X was run".

Example: VFX `scripts/comfy_agentic_worker.py` is Declared (inlined in a manual), not Implemented (no file on disk), not Verified.

## 3. LocalTaskContract

JSON Schema: `schemas/local-task-contract.schema.json`

Salwise ENQ-style work. Known facts, missing fields, constraints, `draft_only`, `model_execution`.

The local model receives this compact contract, not the orchestration policy. Codex or another executor retains policy.

## 4. SkillSession

JSON Schema: `schemas/skill-session.schema.json`

Tutor intents: `outline`, `expand`, `resources`, `plan`, `assess`, `answer-key`, `case-study`, `track`.

Progress is conversational unless the user asks for a Markdown log. No cross-app memory. Scores are not certificates.

## 5. MediaJobSpec

JSON Schema: `schemas/media-job-spec.schema.json`

Reserved for a future VFX worker. Fields exist so a later implementation does not invent a private vocabulary. This snapshot contains no worker.

A MediaJobSpec is not executable. Submitting frames to a diffusion cluster would be an AIOS Red Action at minimum (production media consequence) and is Prohibited while QC is a stub.

## 6. ActionProposal (existing, do not fork)

Canonical schema: `actions/schemas/action-proposal.schema.json` on the parent AIOS branch.

The kernel references it. It does not copy or relax it. `additionalProperties` remains false.

## Adapter responsibilities

| Adapter | Owns | Emits | Must not |
| --- | --- | --- | --- |
| `aios` | Four-layer evaluation, Layer 0, action class, Witness | Decision record; Action Proposal when execution is contemplated | Execute |
| `salwise` | /goal, /journey, SAL-Q local profile, ENQ fixtures | LocalTaskContract; run-instance record (future) | Import corporate gates; claim productivity |
| `tutor` | Curriculum, rubric, safety for alcohol and minors | SkillSession notes | Persist secret learner data; certify |
| `vfx` | Future media job fields | MediaJobSpec only after files exist on disk | Claim zero-liability or production |
| `review_prompt` | Sensemaking review procedure | EvidenceEnvelope list | Treat a target manual as production-grade without inventory |

## Sequencing rule

Reuse before build. Configuration before code. Independent work before blocked host work. Human acceptance before benefit claims.
