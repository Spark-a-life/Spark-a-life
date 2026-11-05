# Four-artefact coordination plan

**Status:** Coordination specification. Not a runtime. Not production. Not an approval.  
**Version:** 1.0.0-eval (same pack as `README.md`)  
**Date:** 5 November 2026  
**Branch:** `cursor/portfolio-eval-architecture-8465`  
**Base:** `cursor/aios-v1-2-alpha-repo-8465`  
**Draft PR:** https://github.com/Spark-a-life/Spark-a-life/pull/3  
**UK English.** House style: no em dash.

This file is the Human Captain's executable coordination plan for four sibling artefacts. It does not replace `EVALUATION.md` (verdicts and evidence) or `INTEROP.md` (kernel and adapters). If this file and those two disagree, stop. Do not invent a third sequence.

Canonical governance remains `governance/AIOS_v1.2.md`. This pack must not rewrite it.

Vocabulary is already named in `kernel/VOCABULARY.md`. Use it. Do not introduce a parallel lexicon.

---

## 1. Intent and non-goals

### What coordination means

Coordination, in this pack, is three practices:

1. **Shared contracts.** The four artefacts share the kernel envelopes and the maturity / action / data-class words already recorded in `INTEROP.md` and `kernel/`. They do not share a codebase, a router, or a product name.
2. **Sequencing.** Work that can run in parallel does. Work that would manufacture false confidence waits. The order is in §8. It matches `INTEROP.md` "Feasible shared implementation later" and `EVALUATION.md` "Sequenced action items".
3. **Isolation.** Each artefact has its own workstream, owner role, data class, publish posture, and stop condition. A pass in one workstream is not a pass in another.

Coordination also means keeping inventories true. `FILE_INVENTORY.json` and the Salwise `manifest.json` authenticate file identity. They do not authenticate factual truth or confer approval (`kernel/DATA_CLASSES.md` boundary rule 3).

### What coordination does not mean

- One mega-product, unified router, "Spark platform", or fifth evaluation layer. `INTEROP.md` already forbids collapsing the four into one platform.
- A GPU cluster, ComfyUI server, Kubernetes Service, Nuke plugin, or studio pipeline as next work. VFX remains isolated design notes.
- Merging this branch, or the parent AIOS branch, to profile `main`. That would replace the GitHub profile README (`README.md`; `EVALUATION.md` blocker 5).
- Rewriting the AIOS protocol, Action Proposal schema, evidence states, or Action classes. Siblings map at the kernel only.
- Remote-host evidence standing in for the owner's desktop. Localhost belongs to the executor (`kernel/DATA_CLASSES.md`).
- Inferring productivity, mastery, production-grade status, or zero-liability from a checker, a prompt, or a fenced code block.
- Vendoring the VFX manual wholesale. The pack verifier treats extracted runtime paths as a failure (`verify_portfolio_pack.py` `VFX_FORBIDDEN`).
- Public profile publication of Salwise library URLs, learner identity, plates, weights, credentials, or opportunity corpora.
- Conferring authority. Possession of this plan is not Authorised execution (`README.md` Authority; kernel `authority: NONE_CONFERRED` unless a named human is recorded).

---

## 2. Role map

One Human Captain remains final authority. Role labels do not supply independent review. They do not authorise work. They name who does the work when the Human Captain so decides.

Evaluators occupied during the 5 November 2026 review are already listed in `EVALUATION.md`. This map assigns a **best-fit ongoing owner role** per artefact for the coordination phase. It does not invent a live identity service.

| Role | Scope | Best-fit artefact | Must not |
| --- | --- | --- | --- |
| Human Captain | Final decision rights over claims, disclosure, commitments, risk acceptance, consequential execution | All four, plus AIOS, plus this pack | Be inferred from silence (`governance/AIOS_v1.2.md` §29) |
| Evaluator | Honest inventory, overclaim detection, evidence-state labelling | A1 first; A2 as red-team support | Pre-certify a target by copying its title into a prompt |
| Data steward | Classification, sanitisation, what may be committed | A3 (library URLs, fictional ENQ); pack-wide no-secrets | Commit `CONFIDENTIAL` / `RESTRICTED` / `REGULATED` data; treat library URLs as portable |
| Local-runtime operator | Named-host execution of a bounded brief | A3 on the owner's LM Studio machine only | Describe a remote agent's loopback as that desktop |
| Pedagogy lead | Skill drop, T1-T12 as acceptance specs, alcohol/minor safety | A4 | Convert a progress log into a Witness Chain; certify mastery |
| VFX design editor | Inventory rewrite, defect list, colour/QC/Service honesty | A2 (docs only in this phase) | Extract fenced blocks into a fake repo; submit a cluster job |
| Release steward | Branch posture, licence, inventories, verify script, draft PR base | This pack | Merge to `main`; bump AIOS `VERSION`; claim a release gate |

Named people, from existing files:

- Human Captain: AIOS authority term (`kernel/VOCABULARY.md`).
- Will / Dr William Siew: Salwise acceptance owner, already the Spark-a-life identity in this repository. Do not rename Will as Human Captain inside Salwise files. Map at the kernel: both are human acceptance owners in their own scope.
- Codex / executor: implementer of a bounded Salwise brief; not an authoriser.
- Learner: the person being taught by A4; not a Captain analogue.

Roles not faked (from `EVALUATION.md`): there is no live identity service to operate, no production release to sign, and no client-opportunity corpus to steward beyond the named owner already in this repository.

---

## 3. Dependency graph

### Parallel (no wait)

| Work | Why it is independent |
| --- | --- |
| Pack verification on this (or any) git checkout | Docs-only; no model, cluster, or DCC |
| Salwise mechanical checker | Document consistency; already 18/18 PASS with `runtime_integration: NOT_RUN` |
| Salwise M0 on the owner's LM Studio host | Does not depend on VFX, the tutor, or an AIOS Action Gateway |
| Tutor T1-T12 treated as acceptance specs (markdown, `NOT_RUN`) | Product-unrelated to opportunity intelligence; no AIOS engine required |
| Optional tutor skill drop into a local Cursor skills directory | File copy; behaviour remains `NOT_RUN` until a named model is recorded |
| Keeping AIOS v1.2 byte-identical at repository root | Already true; siblings must not touch it |
| Licence All Rights Reserved at pack level | Already true; no per-artefact licence decision is required to stay private |

### Must wait

| Later work | Waits for | Why |
| --- | --- | --- |
| Kernel freeze declaration | Plan lock (§8 phase 0) | Freeze is a Human Captain decision that the on-disk contracts are the contracts |
| Meta-prompt preface rewrite (A1) | A truthful VFX inventory (A2 `CLAIMED_VS_DISK.md` still current, plus any rewrite of claimed-versus-disk) | The prompt's damage is that it pre-certifies A2. Rewriting the preface without an honest inventory leaves the 30-60-90 request pointed at a missing product |
| Optional kernel adapter JSON per run (`EVALUATION.md` L5) | Kernel freeze, plus at least one real run on a named host | Empty envelopes are not evidence |
| Salwise M1-M2 | M0 inventory on the target host | Route choice before configuration (`Salwise_Local_AI_Productivity_PaP2_v1.2.md` /journey) |
| Salwise human-productivity claim | M2 plus Will's screening of real effort, threshold declared first (`EVALUATION.md` L2) | Desirability is `NOT_MEASURED` |
| Tutor behavioural PASS/FAIL | Named model, named host, transcripts (`EVALUATION.md` L3) | Markdown tests are not runs |
| VFX worker, QC, colour path, Kubernetes Service | Human Captain decision that VFX is still desired, plus a new tree, not this manual (`EVALUATION.md` L4) | Current samples are Declared only; execution is Prohibited while QC is a stub |
| AIOS Action Proposal for media | Real worker, real QC, real colour, real Service, `MaturityClaim.implemented_on_disk` true | Cluster submit is Red at minimum and currently Prohibited (`INTEROP.md` vfx adapter; `kernel/INTERFACES.md` MediaJobSpec) |
| Public drop of Salwise | Sanitisation of ChatGPT library URLs (`SANITISATION.md`; `EVALUATION.md` L6) plus a written licence choice | Private-repo-ready is not public-profile-ready |
| Merge to profile `main` | A separate, explicit Human Captain decision that replacing the profile README is intended | Default is never in this phase |

### Explicit non-dependencies (do not invent coupling)

- **Salwise M0 does not depend on VFX.** Local LM Studio enquiry and a fictional GPU/Nuke pipeline are incompatible stacks (`INTEROP.md`).
- **The tutor does not depend on the AIOS opportunity engine.** Do not route opportunity evaluation through the skill. Do not fold four-layer scores into the five-dimension rubric.
- **The meta-prompt depends on a truthful VFX inventory.** Until that inventory is the evaluator's starting condition, A1 is an input under review, not a trusted adapter (`INTEROP.md` review_prompt).
- **The AIOS protocol is not rewritten by any sibling.** `ActionProposal` stays at `actions/schemas/action-proposal.schema.json`. `additionalProperties` remains false. PaP2 is not a fifth AIOS layer. Salwise 30 attributes do not become AIOS evidence states.

### Graph (read down)

```text
[0] Human Captain locks this plan
           |
[1] Kernel freeze (contracts already on disk; decision only)
           |
           +--[2a] Salwise M0 on owner's LM Studio host     (no VFX wait)
           |
           +--[2b] Tutor T1-T12 kept as acceptance specs    (no AIOS wait)
           |         optional: skill drop, results file = NOT_RUN
           |
           +--[2c] VFX inventory rewrite (docs; no K8s/Comfy)
           |         |
           |         +--[3] Meta-prompt preface rewrite
           |
[4] Optional interop adapters (EvidenceEnvelope JSON per real run)
           |
[never in this phase] merge to main; GPU cluster; unified router; AIOS rewrite
```

---

## 4. Per-artefact workstreams

Maturity uses Declared / Implemented / Verified / Authorised from `kernel/VOCABULARY.md`. "This week" means the next bounded increment, not a calendar promise (`EVALUATION.md`).

### 4.1 A1. Sensemaking meta-prompt

**Path:** `portfolio/artifacts/claude-sensemaking-meta-prompt/`  
**Source:** `source.md` (original bytes; sha256 `a2dc1991a82eef9880c15a11e0f8488a010fabd71ad13e5e927f147048855dfe`)  
**Lens:** evaluator / red-team (`EVALUATION.md`; `STATUS.md`)  
**Owner role:** Evaluator. Human Captain remains final authority on reuse.

**What it actually is:** a 31-line review agenda aimed at the VFX manual. Not an engine, not an ingestion system, not evidence that A2 is production-grade.

**Current maturity**

| Claim | State | Basis |
| --- | --- | --- |
| Role and agenda | Declared | File exists; agenda is specific |
| Engine / ingestion | Not claimed honestly | Title overclaims; `STATUS.md` contradicts it |
| Implemented | n/a | Prompt, not a service |
| Verified | n/a | No independent check of outputs |
| Authorised | No | `authority` remains `NONE_CONFERRED` |

Evidence state of the opening frame ("complete, production-grade"; "zero-liability"): Declared by Interested Party, and Contradicted by A2's placeholder QC and missing files (`STATUS.md`).

**Entry criteria**

- `STATUS.md` and `EVALUATION.md` A1 have been read.
- A2 inventory (`CLAIMED_VS_DISK.md`) is in hand. Do not run the prompt as if A2 were a repository.
- Operator accepts that this pack, not the prompt's preface, is the honest evaluation until the preface is rewritten (`EVALUATION.md` A1 Implementability).

**Exit criteria (coordination phase)**

- Preface no longer calls A2 production-grade or zero-liability.
- New sha256 recorded in `STATUS.md`.
- `verify_portfolio_pack.py` pin for the old hash is updated in the same change, or the rewrite is kept as a sibling file and the original bytes remain the pinned source.
- Publish posture remains private.

**Exit criteria this phase does not include:** a 30-60-90 studio production matrix; trusted-adapter status while the preface is unfixed.

**Tasks**

| When | Task | Maps to |
| --- | --- | --- |
| This week | Do not silently edit `source.md`. Keep original bytes so the evaluation remains replayable. | `EVALUATION.md` W5 |
| Next | After A2 inventory rewrite (or an explicit Human Captain decision that `CLAIMED_VS_DISK.md` is already the inventory), rewrite the opening sentences. Keep the spatial / colour / concurrency / QC agenda. Drop or reframe the 30-60-90 request so it cannot manufacture a delivery plan for a missing product. | W5; `STATUS.md` |
| Later | Reuse as a private prompt only. Do not publish as an engine. | Publish posture |

**Blockers**

- Using the current preface as the evaluator's starting condition (overclaim copied from A2's title).
- Treating `k8s-deployment.yaml` as a sibling file. It is a section heading inside A2 (`EVALUATION.md` A1 Completeness).

**Risks**

- A capable model given the current preface will plan a studio rollout for files that are not on disk.
- A rewrite that keeps "production-grade" in a later paragraph reintroduces the same defect.

**Rollback**

- Leave `source.md` byte-identical (current pin). Any rewrite is a new hash and a STATUS update, or a new filename. Do not mix old evaluation hashes with new bytes.

**Fail-closed**

- If the preface still pre-certifies A2, the review_prompt adapter stays "input under review", not trusted (`INTEROP.md`).
- Do not emit an EvidenceEnvelope that treats A2 as Implemented.

**Data class:** `INTERNAL` practice material. No secrets, no PII. Nothing to keep local beyond ordinary editor scratch.

**Publish posture:** Private. Never public as an "engine". Never public without the preface fix.

---

### 4.2 A2. VFX AI pipeline integration manual

**Path:** `portfolio/artifacts/vfx-ai-pipeline-manual/`  
**Source sha256 (upload, not copied):** `816022081890a347a5018cc36c2e77cf3c0e7a0af1e547732fd08d1a8521a90c`  
**Lens:** red-team, feasibility, release-readiness  
**Owner role:** VFX design editor for docs; Human Captain before any later studio work. No studio engineer is scheduled in this phase.

**What it actually is:** a 575-line design sketch with axioms and eight inlined samples. Not a pipeline, not a repository, not a cluster, not deterministic QC, not zero-liability (`STATUS.md`).

**Current maturity**

| Claimed path | On disk | Maturity |
| --- | --- | --- |
| `configs/ic_lora_vfx_production.yaml` | No | Declared |
| `workflows/workflow_ic_lora_api.json` | No (fenced JSON parses; that is not a file) | Declared |
| `scripts/comfy_agentic_worker.py` | No | Declared |
| `orchestrator/Cargo.toml` | No | Declared |
| `orchestrator/src/main.rs` | No | Declared |
| `deploy/Dockerfile` | No | Declared |
| `deploy/k8s-deployment.yaml` | No | Declared |
| `nuke/comfy_nuke_integration.py` | No | Declared |
| ComfyUI Service / PVC | Not even declared as objects | Missing |
| QC `calculate_structural_divergence` | Stub returns `0.021` vs threshold `0.03` | Contradicted as a control |
| Colour axiom vs Nuke `ACES - ACEScc` | Contradiction in the sketch | Declared, internally inconsistent |
| Kernel `MediaJobSpec` example | Reserved, `NOT_IMPLEMENTED` | Declared only |

Implemented: no. Verified: no. Authorised: no. Future execution class if attempted: Prohibited while QC is a stub (`kernel/examples/vfx-media-job-spec-only.json`; `INTEROP.md`).

**Entry criteria**

- `CLAIMED_VS_DISK.md` and `STATUS.md` have been read.
- Operator accepts that section 7's unchecked boxes are the honest deployment line, undercut by the title.
- No intent, in this phase, to vendor a tree or submit a job.

**Exit criteria (coordination phase)**

- Inventory remains truthful. If rewritten, every claimed path is still marked Declared / missing / contradicting, never silently promoted.
- No runtime path from `VFX_FORBIDDEN` exists under `artifacts/vfx-ai-pipeline-manual/`.
- Colour axiom versus Nuke ACEScc, stub QC, and undefined Service remain named blockers, not nits.
- Title language "zero-liability" / "production" is not imported into AIOS or Salwise (`kernel/VOCABULARY.md`).

**Exit criteria this phase does not include:** a worker, a Service, a PVC, ComfyUI, models, tests that can fail, or an AIOS Action Proposal.

**Tasks**

| When | Task | Maps to |
| --- | --- | --- |
| This week | Do not extract fenced blocks into a fake repo. Do not submit anything to a cluster. | `EVALUATION.md` W6 |
| Next | Inventory rewrite only: keep `CLAIMED_VS_DISK.md` as the index; add any newly noticed claimed-versus-disk rows; do not copy the 575-line manual into the pack. | W6; L4 (docs subset) |
| Later | Only if still desired, and only as a new tree: real files, named QC metric on actual EXR pixels, consistent colour (working space, display space, OCIO), graph types fixed, Service/PVC or the cluster claim deleted, tests that can fail, licence, then an AIOS Action Proposal classed Red. | L4 |

**Blockers** (from `EVALUATION.md` and `STATUS.md`; not nits)

1. Title and preface claim production-grade / zero-liability while QC cannot fail and paths are not files.
2. Linear EXR axiom versus Nuke `ACES - ACEScc`.
3. Kubernetes sample is not a deployable manifest (Service undefined; PVC referenced, not specified).
4. Image preprocessor wired as a latent; Rust workflow JSON missing nodes; Dockerfile does not contain ComfyUI; Nuke panel does not submit a job.

**Risks**

- Extracting samples would look like Implemented when maturity is still Declared.
- Scheduling K8s/Comfy next would violate §7 and `INTEROP.md` viability.
- Third-party model licences named in A2 were not legally reviewed (`EVALUATION.md` limitations).

**Rollback**

- The pack never vendored the manual. Rollback is "do not add files". If a later tree is started, it lives outside this index until `MaturityClaim.implemented_on_disk` is true.

**Fail-closed**

- Cluster submit, Nuke ingestion of unverified AI plates, or any GPU job: Prohibited (`kernel/DATA_CLASSES.md` rule 5; MediaJobSpec `action_class_if_executed: PROHIBITED`).
- `verify_portfolio_pack.py` fails if forbidden runtime paths appear.
- Do not emit a MediaJobSpec except the reserved example, and do not treat that example as executable.

**Data class:** `INTERNAL` design notes; inlined samples are `FICTIONAL` placeholders (`input_plate_v01.mov`, `studio-registry.internal`).  
**Must stay local if they ever exist:** camera tracking, depth, plates, EXR sequences, shot metadata, IC-LoRA / Wan weights (`kernel/DATA_CLASSES.md`).

**Publish posture:** Private design notes. Index only. Never public as a pipeline. Wholesale vendoring refused.

---

### 4.3 A3. Salwise Local AI Productivity PaP2 v1.2

**Path:** `portfolio/artifacts/salwise-local-ai-pap2-v1.2/`  
**Package:** `package/` (16 files, original bytes, matching `manifest.json` hashes)  
**Lens:** feasibility / assurance; data steward; interoperability  
**Owner role:** local-runtime operator (Will, with Codex on that host) for M0-M2; data steward for sanitisation; Human Captain for any later live-client or public-drop decision.

**What it actually is:** a reviewed execution brief plus mechanical checker. Best-formed artefact in the set. Not a new operating architecture, not an LM Studio product, not a Pando replica, not a demonstrated productivity gain (`STATUS.md`).

**Current maturity**

| Claim | State | Basis |
| --- | --- | --- |
| Prompt, profile, fixtures, scenarios | Declared | 16 files on disk |
| Package checker | Implemented | `check_v1_2_package.py` runs |
| Document consistency | Verified (mechanical) | 18/18 PASS; `candidate_sha256` `107c3fcf94b25a56cb14993569c802b12623bb9daa9f8edd415c04c0344f69bf` |
| Runtime integration | `NOT_RUN` | Package's own label |
| Model behaviour | `NOT_RUN` | Package's own label |
| Human productivity | `NOT_MEASURED` | Package's own label |
| Independent assurance | `NOT_ESTABLISHED` | Author self-review |
| Authorised production use | No | `Authority: NONE_CONFERRED` |

Do not relabel M0 as AIOS Layer 0 without an explicit mapping (`kernel/VOCABULARY.md`).

**Entry criteria (M0)**

- This plan is locked, or the Human Captain has explicitly authorised M0 without waiting for lock.
- Executor is on the computer that can see the owner's LM Studio, or honestly reports it is not (`START_HERE.md`).
- `python3 package/check_v1_2_package.py` still exits 0, 18/18, with runtime and model labels still `NOT_RUN`.
- Data in use is the fictional ENQ-001 fixture, labelled `FICTIONAL`.
- No new paid usage, no live client records, no credential harvest.

**Exit criteria (M0 only)**

- Inventory of actual OS, model, endpoint, and dirty git state on that named host (`EVALUATION.md` W2).
- Alternatives considered; smallest adequate route chosen; one short decision note.
- Remote localhost, if any, distinguished from the owner's desktop.
- Baseline `Salwise_Local_AI_v1.2_Checks.json` not overwritten with invented runtime rows. Future observations go to a separate run-instance record (`START_HERE.md`).

**Exit criteria this phase does not include:** M1-M2 model execution, human-benefit percentage, independent laboratory assurance, or folding SAL-Q into AIOS.

**Tasks**

| When | Task | Maps to |
| --- | --- | --- |
| This week | On the LM Studio machine, run M0 discovery from `START_HERE.md`. Treat Salwise as the only execution candidate in the four. | W2 |
| This week | Re-run the checker after any edit. | W3 |
| Next | M1-M2: one fictional enquiry path, frozen-reference checks, restart notes. New run-instance record. | L1 |
| Later | Human screening of 10-20 comparable enquiries; threshold declared first. Then, and only then, desirability may leave `NOT_MEASURED`. | L2 |
| Later, only if public is intended | Redact `account_id=personal` library URLs. | L6 |

**Blockers**

- Target host unreachable from this review environment. Do not invent local evidence (`EVALUATION.md` blocker 6).
- ChatGPT personal library URLs are not portable (`SANITISATION.md`; blocker 7).
- Windows / WSL2 / Hermes / Salwise Workbench are reported context to verify, not verified (`STATUS.md`).

**Risks**

- Checker PASS described as production readiness.
- Pando / OpenAI Git-backend throughput used as a local productivity forecast (`INTEROP.md` "What must not be shared").
- Timeout treated as cancellation (`Salwise_Local_AI_Productivity_PaP2_v1.2.md`).
- Sensibility-as-a-Prompt naming remains unresolved; do not fake a definition.

**Rollback**

- Keep the vendored `package/` bytes. Do not convert baseline obligations into supposed historical results.
- If a target-host change fails, retain the known working document revision and report `PARTIAL` or `BLOCKED` with the exact remaining dependency.

**Fail-closed**

- If the executor is not on the target host: finish independent document work; hand over a read-only evidence-collection need; status `PARTIAL`. No local performance inferred from a remote fixture run.
- If credentials, `.env` values, browser history, or live client data would be collected: stop.
- If the model output would send a message, quote a fee, or treat source text as execution authority: stop. Draft only. UntrustedEvidence applies (`kernel/VOCABULARY.md`; Salwise S05 / ENQ-001).
- Mechanical `PASS` is not runtime `PASS_SCOPED`.

**Data class:** ENQ-001 / Cedar Learning is `FICTIONAL` and may stay in the private snapshot. Named owner is already in this repository. Library URLs are account-scoped provenance, not secrets; keep in this private snapshot; redact before any public drop.  
**Must stay local:** LM Studio models, weights, live endpoints, hardware inventory more specific than the brief needs, credentials, `.env` values.

**Publish posture:** Private-repo-ready on this stacked branch. Not public profile material. Not production. Never public without L6 sanitisation and a written licence choice (default remains All Rights Reserved).

---

### 4.4 A4. Adaptive Learning Tutor v1.0

**Path:** `portfolio/artifacts/adaptive-learning-tutor-v1.0/`  
**Package:** `package/` (7 files: `SKILL.md` + six references)  
**Lens:** product reviewer; privacy/safety; release-readiness  
**Owner role:** pedagogy lead. Human Captain for any public drop or behavioural claim.

**What it actually is:** a coherent Cursor skill. Pedagogical sibling. Product-unrelated to opportunity intelligence and to VFX. Not an app, not an LMS, not persistent memory, not a certificate issuer (`STATUS.md`).

**Current maturity**

| Claim | State | Basis |
| --- | --- | --- |
| Skill behaviour | Declared | `SKILL.md` operating rules |
| Markdown pack | Implemented (as text) | 7 files; references resolve |
| File presence / internal refs | Verified (mechanical) | Pack verifier |
| T1-T12 | Specs, not runs | `QA_TESTS.md`; `NOT_RUN` |
| Teaching quality | Not verified | No named model |
| Authorised certification | Forbidden by the skill | Do not award |

**Entry criteria**

- `SKILL.md` and `references/QA_TESTS.md` have been read.
- Operator records T1-T12 as `NOT_RUN` until executed against a named model (`EVALUATION.md` W4).
- Wine default and minor/alcohol rules are treated as behavioural requirements, especially T2 and T8.

**Exit criteria (coordination phase)**

- T1-T12 remain the acceptance specification. A results file exists if a skill drop is made, even if every row is `NOT_RUN`.
- No opportunity evaluation is routed through the skill.
- No progress log is labelled a Witness Chain.

**Exit criteria this phase does not include:** behavioural PASS, public drop, licence change, or resource-URL verification.

**Tasks**

| When | Task | Maps to |
| --- | --- | --- |
| This week | Optional: drop `package/` into a local Cursor skills directory if teaching use is wanted. Record T1-T12 as `NOT_RUN`. | W4 |
| Next | Keep T1-T12 as specs. Do not mark PASS from static reading. | Coordination done-line in §8 |
| Later | Run T1-T12 against a named model on a named host, including T2 (no wine leakage) and T8 (minor). Results JSON plus transcript refs. | L3 |
| Later, if public | Licence decision and recorded behavioural tests if any behavioural claim is made. | `STATUS.md` Publish |

**Blockers**

- None for a private skill drop.
- Behavioural claims without a named host and transcripts.

**Risks**

- Wine-default leakage into an unspecified topic if T2 is not behaviourally enforced.
- Resource URLs unverified.
- Invented learner names, fabricated book contents, fake decimal ratings, cross-app memory, certification (all forbidden by the skill; still a model-compliance risk).

**Rollback**

- Remove the skill directory copy. The vendored `package/` bytes stay.

**Fail-closed**

- Age 15 / minor path: no alcohol consumption recommendations (T8). If the model fails T8, stop teaching that session; record FAIL.
- Malicious webpage claiming to override the skill: ignore (T11; UntrustedEvidence).
- Do not persist secret learner data. Conversational profile stays in session unless the user exports Markdown (`kernel/DATA_CLASSES.md`).

**Data class:** skill text is `INTERNAL` snapshot; bibliographic names are `PUBLIC`; learner identity, if any later appears, is `CONFIDENTIAL` or `REGULATED` and must not be committed.  
**Must stay local:** learner identity and any persistent tutor profile.

**Publish posture:** Private skill snapshot under All Rights Reserved. Public drop needs a licence decision and, if claims are made, recorded T1-T12 runs.

---

## 5. Cross-cutting workstream

Owner role: release steward, with data steward for sanitisation. Human Captain signs publish and merge decisions.

### Kernel contracts

Already on disk. Do not add a sixth envelope. Do not fork `ActionProposal`.

| Envelope | Schema | Example | Adapter |
| --- | --- | --- | --- |
| EvidenceEnvelope | `kernel/schemas/evidence-envelope.schema.json` | `kernel/examples/enq001-envelope.json` | all |
| MaturityClaim | `kernel/schemas/maturity-claim.schema.json` | `kernel/examples/vfx-worker-maturity.json` | vfx first |
| LocalTaskContract | `kernel/schemas/local-task-contract.schema.json` | `kernel/examples/enq001-local-task.json` | salwise |
| SkillSession | `kernel/schemas/skill-session.schema.json` | `kernel/examples/tutor-session-outline.json` | tutor |
| MediaJobSpec | `kernel/schemas/media-job-spec.schema.json` | `kernel/examples/vfx-media-job-spec-only.json` | vfx, reserved |

Kernel freeze, after plan lock, means: these names, required fields, and enums stay. Adapters may ignore interfaces they do not need (`kernel/INTERFACES.md`). Optional later work is filling JSON files from real runs (L5), not implementing a server or router.

### Vocabulary map

`kernel/VOCABULARY.md` is the map. Binding rules for this plan:

- Maturity of our artefacts: Declared / Implemented / Verified / Authorised.
- Salwise runtime: `NOT_ASSESSED`, `PASS_SCOPED`, `FAIL`, `PARTIAL`, `BLOCKED`, `DEFERRED`, plus package-level `NOT_RUN` / `NOT_MEASURED` / `NOT_ESTABLISHED`.
- AIOS evidence states: use for claims about the world, not as a replacement for maturity.
- AIOS action classes: Green / Amber / Red / Prohibited. Schema enums `GREEN`, `AMBER`, `RED`, `PROHIBITED`. Unknown material consequence prevents automatic Green or Amber.
- Shared practice: human acceptance, UntrustedEvidence, status honesty, local-first, UK English.
- Forbidden borrowings: zero-liability, production-grade, PaP2 as a fifth AIOS layer, tutor Skill as an Action, progress log as Witness Chain, Salwise M0 as Layer 0, certified / mastery from a checker.

### FILE_INVENTORY and verify script

- `portfolio/FILE_INVENTORY.json` is regenerated by `verify_portfolio_pack.py`. It is sha256 of tracked pack files except itself.
- After any pack edit, run the verifier and commit the regenerated inventory in the same change.
- Required paths, Salwise manifest hashes, VFX-not-vendored, AIOS v1.2 size `63543`, secret-pattern scan, and em-dash scan are pack gates, not authority.

### Licence

`portfolio/LICENSE`: All Rights Reserved, 2026 Spark-a-life. Source packages that lacked a licence inherit this default. Per-artefact licence change is L7 and is not required to remain private.

### No-secrets

Pattern scan in the verifier is necessary and not sufficient. Data steward still reads `SANITISATION.md` before any wider copy. Do not write secrets, unrestricted tokens, or unnecessary sensitive payloads into inventories, Witness notes, or tutor logs (`kernel/DATA_CLASSES.md` rule 6).

### No false inventories

- Do not list a fenced code block as a file.
- Do not list a remote loopback as the owner's host.
- Do not list a markdown test as a behavioural run.
- Do not list checker PASS as runtime PASS.
- If a byte of an evaluated upload changes, `EVALUATION.md` does not apply until re-run from the new hash.

---

## 6. Reliability and reproducibility

### What another person can re-run, anywhere this pack is checked out

From the repository root:

```text
python3 portfolio/verify_portfolio_pack.py
python3 portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py
```

From `portfolio/`:

```text
python3 verify_portfolio_pack.py
python3 artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py
```

Expected, as of 5 November 2026 on the evaluation host (`/opt/cursor/artifacts/portfolio_verification.log`):

- Pack checks all PASS (then 48/48; the count rises if required-path rows are added).
- `runtime: false`
- `production_external_execution: false`
- Salwise mechanical 18/18 PASS
- `runtime_integration: NOT_RUN`
- `model_behaviour: NOT_RUN`
- VFX manual not vendored wholesale
- AIOS v1.2 size 63543 unchanged
- No high-risk secret patterns in pack text
- No em dash in pack text files

The verifier rewrites `FILE_INVENTORY.json`. A clean re-run should be byte-stable if no files changed.

Upload hashes to repeat the original evaluation (if the uploads are still present):

| File | sha256 |
| --- | --- |
| `claude_sensemaking_meta_prompt_e074.md` | `a2dc1991a82eef9880c15a11e0f8488a010fabd71ad13e5e927f147048855dfe` |
| `vfx_ai_pipeline_integration_manual_8488.md` | `816022081890a347a5018cc36c2e77cf3c0e7a0af1e547732fd08d1a8521a90c` |
| `Salwise_Local_AI_Productivity_PaP2_v1.2_5eb3.zip` | `45030dca99a2eea90a2a448832d9ba1a6353d2cff94ffe78b2e9afda265dd4b3` |
| `Adaptive_Learning_Tutor_v1.0_a18c.zip` | `d83d95c45e0cf9cae6e9d74c89288b9cdd064e0d603b0a23510c42336f3767fd` |

If a byte changes, this evaluation and this plan's hash pins do not apply.

Tutor T1-T12 are acceptance specs. Reading `QA_TESTS.md` is not running them. Record `PASS` / `FAIL` / `NOT RUN` only from a real-model session.

### What cannot be claimed without a named host

| Claim | Named host required | Otherwise |
| --- | --- | --- |
| Salwise runtime integration | Owner's LM Studio machine | `NOT_RUN` |
| Salwise model behaviour | Same, plus model id and endpoint | `NOT_RUN` |
| Human productivity / desirability | Same, plus Will's screening | `NOT_MEASURED` |
| Tutor T1-T12 behavioural result | Cursor (or other) host running the named model | `NOT_RUN` |
| VFX worker / QC / colour / Service | DCC workstation and/or cluster that actually exists | Declared only; execution Prohibited |
| Localhost identity | The executor's machine | Remote review host must not impersonate the desktop |
| Production-grade / Authorised | Release-gate evidence plus Human Captain | Do not apply to any artefact in this set |

jsonschema may be absent. The verifier then uses a required-key fallback and records that limitation in the check detail. A fallback pass is not a full schema-validator pass.

### Honest limitations carried forward from the evaluation

- No LM Studio, Nuke, Kubernetes, or tutor-model session was available on the evaluation host.
- No independent laboratory colour measurement.
- No legal review of third-party model licences named in A2.
- ChatGPT library sources cited by Salwise were not opened.
- Pando / OpenAI Git figures were not re-fetched.
- This pack does not update AIOS `VERSION`, `manifest.json`, or `FILE_INVENTORY.json` at repository root. It is not an AIOS release.

---

## 7. Feasibility, viability, desirability

Keep the table in `EVALUATION.md` "Viability, feasibility, desirability" and `INTEROP.md` "Viability". Restated here only so this plan can be executed without hunting.

| Keep | Why |
| --- | --- |
| Salwise v1.2 package | Specified enough to start M0; honest about what is missing |
| Tutor skill | Small, safe-by-construction text, usable as a drop |
| AIOS v1.2 as canonical governance | Parent snapshot; do not weaken it |
| This kernel | Prevents slogan-level "interop" |

| Isolate | Why |
| --- | --- |
| VFX manual | Overclaim; missing files; stub QC |
| Meta-prompt as currently worded | Pre-certifies A2 |

| Do not do in this coordination phase | Why |
| --- | --- |
| Merge to profile `main` | Would replace the GitHub profile README |
| Build a unified router | Salwise and AIOS both forbid it in this increment |
| Deploy Kubernetes GPUs / schedule Comfy as next work | No Service, no QC, no colour truth |
| Infer productivity or mastery | Explicitly unmeasured |
| Vendor A2 wholesale | Pack gate and evaluation verdict |

Feasibility of Salwise M0: yes, on the owner's machine; no, as verified local result from a remote agent.

Viability of the set: siblings around Spark-a-life, not one product.

Desirability of Salwise: `NOT_MEASURED` until Will screens real effort.  
Desirability of the tutor: plausible for teaching tasks and untested.  
Desirability of VFX-as-written: low; it would create false confidence (`EVALUATION.md`).

Do not schedule K8s or Comfy as next work. Optional interop adapters come only after §8 phases 0-3.

---

## 8. Cadence and definition of done

Realistic sequence. Not a calendar. Each phase has a stop condition. Do not skip forward to manufacture completeness.

| Phase | Name | Owner role | Done when | Stop if |
| --- | --- | --- | --- | --- |
| 0 | Plan lock | Human Captain | This file accepted as the coordination plan; draft PR #3 remains based on the AIOS branch; still not merged to `main` | Captain rejects or wants a different sequence |
| 1 | Kernel freeze | Release steward, Captain confirms | Decision recorded that the five envelopes plus referenced ActionProposal are frozen; no router; no sixth envelope | A named schema defect is found; then fix the defect, do not add product surface |
| 2 | Salwise M0 on target host | Local-runtime operator (Will / Codex on that host) | Host inventory and route decision as in §4.3 | Executor is not on that host and would fake localhost; or credentials would be collected |
| 3a | Tutor acceptance pass as specs | Pedagogy lead | T1-T12 filed as the behavioural contract; results `NOT_RUN` unless a named model was actually used | Anyone marks PASS from reading markdown |
| 3b | VFX inventory rewrite | VFX design editor | `CLAIMED_VS_DISK.md` (and STATUS if needed) still forbids treating A2 as Implemented | Urge to extract samples or open a cluster ticket |
| 3c | Meta-prompt preface fix | Evaluator | Opening sentences no longer call A2 production-grade; new hash or sibling file; STATUS updated | Preface fix attempted before inventory is honest |
| 4 | Optional interop adapters | Executor, after Captain yes | EvidenceEnvelope JSON for each new real run; valid against schema; no gateway | No real run exists; empty envelopes offered as evidence |

3a, 3b, and 3c: 3a may run in parallel with 2. 3c waits for 3b. Phase 4 waits for 1 and for at least one of 2 or 3a having real named-host work if envelopes are to be filled from runs. Inventory-only envelopes that restate `EVALUATION.md` are optional and must keep maturity honest.

### Definition of done: coordination phase

This phase is done when all of the following are true:

1. Plan locked (phase 0) or explicitly rejected (in which case stop).
2. Kernel contracts remain the five named envelopes plus referenced ActionProposal (phase 1).
3. Four workstreams are isolated: separate owners, data classes, publish postures, and stop conditions (this file).
4. `python3 portfolio/verify_portfolio_pack.py` still passes. Salwise checker still 18/18 with runtime `NOT_RUN` unless a separate run-instance exists on a named host.
5. No merge to `main`. No AIOS rewrite. No fifth product. No K8s/Comfy scheduled as next work.
6. VFX remains index-only. Meta-prompt original bytes remain until a deliberate rewrite.

Coordination done is **not** production execution. It is **not** Salwise M2. It is **not** tutor behavioural PASS. It is **not** Authorised.

### Definition of done this phase refuses

- Production-grade, zero-liability, or certified.
- Unified platform.
- GPU cluster.
- Human productivity percentage.
- Profile-README replacement.

---

## 9. Action items

Implementable rows. Owner means the role; the Human Captain may reassign. Stop condition is fail-closed.

| ID | File or artefact | Artefact | Owner role | Dependency | Evidence artefact | Stop condition |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | `portfolio/PLAN.md` | Set | Human Captain | None | Captain decision in §10, or a signed note elsewhere | If rejected, start no workstream |
| C1 | `portfolio/kernel/` | Kernel | Release steward | C0 | Written freeze: no new envelopes; ActionProposal unforked | If a schema defect appears, fix only that defect |
| C2 | `portfolio/verify_portfolio_pack.py` | Pack | Release steward | Any pack edit | Verifier stdout; updated `FILE_INVENTORY.json` | If FAIL, do not claim pack integrity |
| C3 | `portfolio/README.md` | Pack | Release steward | C0 | README lists this plan; still warns not to merge to `main` | If merge warning disappears, restore it |
| C4 | `artifacts/salwise-local-ai-pap2-v1.2/package/START_HERE.md` | A3 | Local-runtime operator | C0; not VFX | Named-host M0 inventory (OS, model, endpoint, dirty git) | If not on target host, PARTIAL; do not invent desktop evidence |
| C5 | `package/check_v1_2_package.py` | A3 | Executor | After any Salwise edit | Exit 0, 18/18, runtime still `NOT_RUN` unless a separate run-instance | If runtime labels flip without a run, revert |
| C6 | `artifacts/adaptive-learning-tutor-v1.0/package/` | A4 | Pedagogy lead | C0; not AIOS engine | Skill visible if dropped; T1-T12 results file exists (`NOT_RUN` allowed) | If PASS recorded without a named model, revert the claim |
| C7 | `package/references/QA_TESTS.md` | A4 | Pedagogy lead | C6 | Specs unchanged; later L3 needs transcripts | Do not substitute static tests for behavioural tests |
| C8 | `artifacts/vfx-ai-pipeline-manual/` | A2 | VFX design editor | C0 | `CLAIMED_VS_DISK.md` current; `VFX_FORBIDDEN` paths absent | If urge to vendor or submit, stop |
| C9 | `artifacts/claude-sensemaking-meta-prompt/source.md` | A1 | Evaluator | C8 (truthful inventory) | New hash + STATUS, or original bytes left pinned | If preface still says production-grade, adapter stays untrusted |
| C10 | `kernel/schemas/evidence-envelope.schema.json` | Kernel | Executor | C1, plus a real run | Valid JSON per run; `authority` honest | If no run, do not mint empty "verified" envelopes |
| C11 | Draft PR #3 base `cursor/aios-v1-2-alpha-repo-8465` | Pack | Release steward | Ongoing | `gh pr view 3` shows that base; PR remains draft | If base becomes `main`, restore the AIOS base; do not merge |
| C12 | Profile `main` | Pack | Human Captain | Never in this phase | Branch remains unmerged | Any merge intent is a separate decision, not this plan |
| C13 | `artifacts/salwise-local-ai-pap2-v1.2/SANITISATION.md` | A3 | Data steward | Only if public drop intended | URLs redacted; titles remain | If public copy still has `account_id=personal`, stop the drop |
| C14 | `portfolio/LICENSE` | Pack | Release steward | None | All Rights Reserved remains default | Do not grant a production-execution licence |
| C15 | `governance/AIOS_v1.2.md` | AIOS | All roles | None | Size 63543; protocol unrevised by siblings | If a sibling PR would edit AIOS, reject that change |

EVALUATION.md W1-W6 and L1-L7 remain the underlying action list. C-rows bind them to files, roles, and stop conditions for this coordination phase. L1-L5 are **not** required for coordination done.

---

## 10. Decision record stub

Not an AIOS Decision Record. Not a Witness Chain. A coordination stub so the Human Captain can accept or reject without waiting for another agent turn.

**Date opened:** 5 November 2026  
**Subject:** Four sibling artefacts under `portfolio/` on `cursor/portfolio-eval-architecture-8465`  
**Decision being supported:** whether to lock this coordination plan and what to authorise next  
**Permitted scope:** plan, contracts, isolated workstreams; no production external execution  
**Prohibited in this decision:** merge to `main`; GPU/K8s/Comfy work; AIOS rewrite; unified router; fifth product  
**Authority:** Human Captain exclusive. This stub confers `NONE_CONFERRED` until the Captain records a choice.

### Recommended next Human Captain decision

1. **Approve this plan** as the coordination-phase lock (C0).  
2. **Then** authorise Salwise M0 on the owner's LM Studio host only (C4), with checker re-run (C5).  
3. **In parallel**, treat tutor T1-T12 as acceptance specs (C6, C7); optional skill drop.  
4. **After** a truthful VFX inventory pass (C8), authorise the meta-prompt preface rewrite (C9).  
5. **Do not** merge PR #3 or the parent AIOS branch to profile `main` (C11, C12).  
6. **Do not** schedule Kubernetes, ComfyUI, Nuke ingestion, or a studio 30-60-90.  
7. **Do not** fill optional adapter envelopes until a named-host run exists (C10).

### Alternatives the Captain may choose instead

- Reject the plan and stop. Workstreams stay isolated by `EVALUATION.md` alone.
- Approve the plan but defer Salwise M0 until Will is at the target machine. Pack verify and tutor-as-specs may still proceed.
- Approve isolation of VFX and the current meta-prompt, and decline any later VFX tree. That is consistent with §7.

### Captain response (leave blank until used)

| Field | Value |
| --- | --- |
| Decision | Approve plan / Approve with conditions / Reject / Defer |
| Conditions | |
| Authorised next IDs | |
| Explicitly not authorised | Merge to `main`; K8s/Comfy; AIOS rewrite; production execution |
| Named hosts in scope | |
| Date | |
| Name | |

Until that row is filled, executors may keep the pack consistent (C2, C3, C11, C14, C15) and must not start Salwise runtime, VFX scripts, or tutor model runs in the Captain's name.

---

## Annex A. Command card

```text
# Pack integrity (any host with the git tree)
python3 portfolio/verify_portfolio_pack.py

# Salwise documents only (not LM Studio)
python3 portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py

# Confirm PR base (read-only)
gh pr view 3 --json baseRefName,headRefName,isDraft,url

# Confirm AIOS file still present and untouched in intent
wc -c governance/AIOS_v1.2.md
```

Do not run ComfyUI, kubectl, Nuke, or a tutor model as part of coordination done.

## Annex B. Pointers (do not duplicate)

| Need | File |
| --- | --- |
| Verdicts, upload hashes, blockers, W/L actions | `portfolio/EVALUATION.md` |
| Kernel, adapters, trust boundaries | `portfolio/INTEROP.md` |
| Term meanings | `portfolio/kernel/VOCABULARY.md` |
| Envelope fields | `portfolio/kernel/INTERFACES.md` |
| Data classes, what stays local | `portfolio/kernel/DATA_CLASSES.md` |
| A1 status | `portfolio/artifacts/claude-sensemaking-meta-prompt/STATUS.md` |
| A2 status and defects | `portfolio/artifacts/vfx-ai-pipeline-manual/STATUS.md` |
| A2 claimed vs disk | `portfolio/artifacts/vfx-ai-pipeline-manual/CLAIMED_VS_DISK.md` |
| A3 status | `portfolio/artifacts/salwise-local-ai-pap2-v1.2/STATUS.md` |
| A3 sanitisation | `portfolio/artifacts/salwise-local-ai-pap2-v1.2/SANITISATION.md` |
| A3 start | `portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/START_HERE.md` |
| A4 status | `portfolio/artifacts/adaptive-learning-tutor-v1.0/STATUS.md` |
| A4 tests as specs | `portfolio/artifacts/adaptive-learning-tutor-v1.0/package/references/QA_TESTS.md` |
| Pack licence | `portfolio/LICENSE` |
| Canonical governance | `governance/AIOS_v1.2.md` |
