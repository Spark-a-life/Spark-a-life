# Interoperability architecture

**Status:** Docs-only kernel. Not a runtime.  
**Decision:** Keep four artefacts as siblings. Share a small kernel. Do not collapse them into one platform.

Primary lens: interoperability architect.

## Why a kernel plus adapters

The artefacts share a practice, not a codebase.

Shared practice, observed on disk:

- Honest status labels in Salwise and AIOS.
- Untrusted source/tool text.
- Human acceptance before benefit or certification claims.
- Local-first for personal and client data.
- UK English in Salwise, the tutor, and AIOS-facing docs.
- Salwise forbids the em dash in its v1.2 Markdown; AIOS house style is in play for AIOS-facing docs.

Incompatible stacks, also observed on disk:

- AIOS is opportunity intelligence and governed Action. It has no GPU, Nuke, or tutor runtime.
- Salwise is one local LM Studio enquiry path. It forbids a new router, Git backend, or model fleet.
- The tutor is a conversational Cursor skill with a wine default.
- The VFX manual describes ComfyUI, Rust/Tokio, Kubernetes GPUs, and Foundry Nuke.
- The meta-prompt is an evaluation procedure aimed at that VFX manual.

A single "Spark platform" that pretended to run all four would violate Salwise's smallest-adequate-route rule, AIOS's "not a runtime" snapshot, and the VFX manual's own missing files.

## Kernel

Named in `kernel/INTERFACES.md`. Five envelopes:

1. `EvidenceEnvelope`
2. `MaturityClaim`
3. `LocalTaskContract`
4. `SkillSession`
5. `MediaJobSpec`

Plus a reference, not a fork, to AIOS `ActionProposal`.

The kernel owns vocabulary (`kernel/VOCABULARY.md`) and data classes (`kernel/DATA_CLASSES.md`). It does not own models, clusters, or skills.

## Adapters

```text
                    +------------------+
                    | Human acceptance |
                    +--------+---------+
                             |
                    +--------v---------+
                    | Portfolio kernel |
                    +--------+---------+
           +---------+---------+---------+---------+
           v         v         v         v         v
         aios     salwise    tutor      vfx    review_prompt
```

Each adapter may run alone. Coupling is optional and explicit.

### aios

Canonical files stay at repository root: `governance/AIOS_v1.2.md` and friends. This pack must not rewrite them.

If Salwise later proposes a live message, fee, or calendar hold, that proposal belongs on the AIOS Action path. Class at least Amber, likely Red. This snapshot has no gateway, so the only legal output is a draft proposal file.

### salwise

Vendored under `artifacts/salwise-local-ai-pap2-v1.2/package/`. Next executable candidate for a target-host M0. Emits `LocalTaskContract`. Maps SAL-Q statuses onto kernel maturity; does not map them onto AIOS evidence states.

### tutor

Vendored under `artifacts/adaptive-learning-tutor-v1.0/package/`. Drop-in Cursor skill. Emits `SkillSession`. Not an opportunity evaluator. Wine is a default topic, not a Salwise or AIOS domain.

### vfx

Not vendored as a tree. Index and defects only. A future worker would emit `MediaJobSpec` and, before any cluster submit, an AIOS Action Proposal classed Red (production media) or Prohibited (stub QC, colour contradiction, missing services).

### review_prompt

Vendored as `artifacts/claude-sensemaking-meta-prompt/source.md`. It is a procedure for reading the VFX manual. It currently overclaims that manual as production-grade. Until rewritten, it is not a trusted adapter; it is an input under review.

## Vocabulary intersections worth keeping

| Concept | AIOS | Salwise | Tutor | VFX sketch |
| --- | --- | --- | --- | --- |
| Human stays in charge | Human Captain | Will owns acceptance | Learner directs; no invented name | Artist review after failed retries (Declared, unimplemented) |
| Untrusted inputs | ADR-006 | ENQ source is data | T11 malicious page | None stated; prompt injection via CLIP text is unaddressed |
| Status honesty | Declared vs Enforced | NOT_ASSESSED / NOT_RUN | Record PASS/FAIL/NOT RUN | Title says production; QC is a stub |
| Local-first data | Corpus excluded | Fictional ENQ; local model | Conversational profile | Plates would stay on NFS if it existed |
| Checkers are not authority | Release gate unchecked | Package PASS is not runtime PASS | Static tests are not behavioural tests | Checklist boxes are empty |

## What must not be shared

- VFX "zero-liability" language.
- Tutor wine defaults leaking into Salwise or AIOS.
- AIOS four-layer scores leaking into a tutor rubric or a structural-divergence number.
- Salwise 30-attribute corporate source checks imported back as if this local profile certified the original register.
- Pando/OpenAI Git-backend throughput numbers as local productivity forecasts.

## Feasible shared implementation later

If a later increment implements anything, implement the envelopes first, as JSON files written by humans or scripts. Do not implement a router.

Suggested order:

1. Keep using Salwise `check_v1_2_package.py` and this pack's `verify_portfolio_pack.py`.
2. On the target LM Studio host, fill a `LocalTaskContract` run-instance for ENQ-001.
3. Drop the tutor skill into a Cursor skill directory and run T1-T12 against a real model, recording NOT_RUN until then.
4. Do not start VFX files until `MaturityClaim.implemented_on_disk` is true for a real worker, a real QC metric, and a real colour path.
5. Any external effect still requires AIOS Action Proposal fields and Human Captain approval.

## Viability

Worth keeping: Salwise package, tutor skill, AIOS as canonical governance, this kernel.

Worth isolating: VFX manual (design notes), meta-prompt (rewrite before reuse).

Worth sequencing, not merging: Salwise M0-M2 on the owner's machine, then a decision to continue, simplify, or stop. Tutor behavioural tests in parallel. No GPU cluster work in this increment.
