# Four-artefact evaluation

**Date:** 5 November 2026  
**Environment:** remote review host. Localhost here is not the owner's desktop.  
**UK English.** No production claims.

Evaluators occupied, by artefact:

| Artefact | Primary lens | Also used |
| --- | --- | --- |
| Sensemaking meta-prompt | Evaluator / red-team | Product reviewer |
| VFX integration manual | Red-team | Feasibility, release-readiness |
| Salwise PaP2 v1.2 | Feasibility / assurance | Data steward, interoperability |
| Adaptive Learning Tutor v1.0 | Product reviewer | Privacy/safety, release-readiness |
| The set | Interoperability architect | Delivery lead |

Roles not faked: there is no live identity service to operate, no production release to sign, and no client-opportunity corpus to steward beyond the named owner already in this repository.

## Verdicts

| ID | Artefact | What it is | Verdict | Vendor | Publish |
| --- | --- | --- | --- | --- | --- |
| A1 | `claude_sensemaking_meta_prompt.md` | Review prompt for A2 | Keep as a private prompt. Rewrite the production-grade premise before reuse. | Source only | Private |
| A2 | `vfx_ai_pipeline_integration_manual.md` | Design sketch with inlined samples | Do not treat as a pipeline. Do not vendor wholesale. | Index only | Private design notes |
| A3 | Salwise Local AI Productivity PaP2 v1.2 | Reviewed execution brief + mechanical checker | Best-formed artefact. Execution candidate. Runtime not assessed. | Yes, original bytes | Private-repo-ready |
| A4 | Adaptive Learning Tutor v1.0 | Cursor skill pack | Coherent skill. Behaviour not run. | Yes, original bytes | Private skill snapshot |

Set verdict: sibling practice materials around Spark-a-life, not one product. Share the kernel in `INTEROP.md`. Do not merge this branch or the parent AIOS branch to profile `main`.

## Method

1. Read both markdown uploads in full.
2. Extract both zips to `/tmp/portfolio-review/`.
3. Inventory every file. sha256 every payload. Compare claimed layouts with disk.
4. Parse every JSON file. Re-run `check_v1_2_package.py` (18/18 PASS, mechanical only).
5. Pattern-scan for secrets, PII, client records, licence gaps, overclaim.
6. Compare vocabulary and authority with canonical `governance/AIOS_v1.2.md` on this branch's parent snapshot.

Upload hashes:

| File | sha256 | Bytes |
| --- | --- | --- |
| `claude_sensemaking_meta_prompt_e074.md` | `a2dc1991a82eef9880c15a11e0f8488a010fabd71ad13e5e927f147048855dfe` | 3096 |
| `vfx_ai_pipeline_integration_manual_8488.md` | `816022081890a347a5018cc36c2e77cf3c0e7a0af1e547732fd08d1a8521a90c` | 18608 |
| `Salwise_Local_AI_Productivity_PaP2_v1.2_5eb3.zip` | `45030dca99a2eea90a2a448832d9ba1a6353d2cff94ffe78b2e9afda265dd4b3` | 46911 |
| `Adaptive_Learning_Tutor_v1.0_a18c.zip` | `d83d95c45e0cf9cae6e9d74c89288b9cdd064e0d603b0a23510c42336f3767fd` | 7973 |

Repeat from those hashes. If a byte changes, this evaluation does not apply.

---

## A1. Sensemaking meta-prompt

### What it actually is

Thirty-one lines of instruction. It tells an assistant it is a VFX systems architect receiving a "complete, production-grade" manual, then asks for spatial, colour, concurrency, QC, and 30-60-90 day production planning.

### Completeness

Depends on A2. A2 was supplied. Referenced `k8s-deployment.yaml` is not a sibling file; it is a section heading inside A2.

### Quality

The review agenda is specific and usable. The opening frame is overclaim copied from A2's title. Asking for a 30-60-90 production matrix before inventorying files would manufacture a delivery plan for a missing product.

### Data

None sensitive.

### Implementability

Usable tomorrow as a prompt. This pack replaces it as the honest evaluation until the preface is rewritten.

Declared: role and agenda. Implemented: n/a. Verified: n/a.

### Fit

Review procedure, same genre as AIOS red-team, different target. Not an AIOS module.

### Publish

Private. Not an engine.

---

## A2. VFX AI pipeline integration manual

### What it actually is

One markdown file, 575 lines. Axioms plus eight inlined samples. See `artifacts/vfx-ai-pipeline-manual/STATUS.md`.

### Completeness

Claimed eight runtime paths. Disk has zero of them. Kubernetes Service, PVC, ComfyUI server, models, and tests are absent even as files. Section 7 checkboxes are unchecked.

### Quality and contradictions

Blockers:

- Placeholder QC returns `0.021` against a `0.03` threshold, so the closed loop cannot fail.
- Linear EXR axiom versus Nuke `ACES - ACEScc`.
- Image preprocessor wired as a latent.
- Rust workflow JSON is missing nodes it references.
- Dockerfile does not contain ComfyUI.
- Kubernetes workers target a Service that is not defined.
- Nuke panel does not submit a job and builds a tree immediately.
- Training bucket `960x544x33` versus workflow 16:9 pad.
- "Zero-liability" in the title is marketing language, not a control.

Nits:

- `register_nuke_menu()` commented out.
- Hardcoded `127.0.0.1:8188` and seed `1337`.
- `rucomfyui` crate version and API not verified in this session.
- Mixed Python worker and Rust orchestrator without a stated failover contract.

### Data

No secrets, plates, or people. No licence.

### Implementability

Not runnable as a pipeline tomorrow. Extracting fenced blocks would produce starting samples, not a studio system.

Declared: axioms and samples. Implemented: no. Verified: no.

### Fit

Unrelated domain. Future execution would be an AIOS Red or Prohibited Action, not a local Salwise task.

### Publish

Private design notes only. Wholesale vendoring refused.

---

## A3. Salwise Local AI Productivity PaP2 v1.2

### What it actually is

A 16-file document package: execution prompt, author review, Pando research note, source map, 30-attribute local profile, source extract, 15-priority crosswalk, 18 desk scenarios, compact local-model task, fictional fixture, frozen reference, checker, check results, check history, manifest, start-here.

### Completeness

Manifest bytes and sha256 values match disk for every listed file. Checker 18/18 PASS on this host, same `candidate_sha256` as the review document (`107c3fcf94b25a56cb14993569c802b12623bb9daa9f8edd415c04c0344f69bf`). Runtime integration `NOT_RUN`. Model behaviour `NOT_RUN`. Human productivity `NOT_MEASURED`. Independent assurance `NOT_ESTABLISHED`. Those labels match the files.

v1.1 is superseded and not bundled. That is declared.

### Quality

This is the only artefact that already applies the honesty bar used for AIOS: checkers are not authority, remote localhost is not the target, a demo is not a diagnosed bottleneck, timeout is not cancellation, a short context is not a Hermes 64k agent, Pando throughput is not local speed.

Known limits, owned by the package itself:

- Author self-review.
- Target machine unknown.
- ChatGPT personal library URLs are not portable.
- Sensibility-as-a-Prompt naming remains unresolved and is correctly not faked.

No version mix inside v1.2 files. Em dash check is part of the mechanical suite.

### Data

Fictional enquiry. Named owner Dr William Siew, already the Spark-a-life identity in this repository. No live client data. Library URLs: see `artifacts/salwise-local-ai-pap2-v1.2/SANITISATION.md`. No licence in the zip; All Rights Reserved applied at pack level.

### Implementability

Tomorrow, on the owner's LM Studio machine, M0 can start. Tomorrow, on this remote host, only the document checker can run. That distinction is the package's own rule.

Declared: prompt, profile, scenarios. Implemented: checker. Verified: package consistency. Not verified: inference, human benefit.

### Fit

Complementary sibling to AIOS. Closest in spirit. Do not fold Salwise 30 attributes into AIOS four layers. Do not fold AIOS Action classes into SAL-Q rows. Map at the kernel only.

### Publish

Private-repo-ready. Not public profile material. Not production.

---

## A4. Adaptive Learning Tutor v1.0

### What it actually is

Seven files, 12878 bytes uncompressed. A skill with intent routing, a five-dimension rubric, and a wine example pack.

### Completeness

All six referenced files exist. QA tests T1-T12 exist as markdown. No runtime harness.

### Quality

Tight operating rules. Explicit bans on invented book contents, fake ratings, cross-app memory, certification, invented learner names, and alcohol exercises for minors.

Residual risk: wine default and topic leakage if T2 is not behaviourally enforced. Resource URLs unverified. No owner or licence field.

### Data

No PII, no secrets. Public bibliographic names only.

### Implementability

Tomorrow as a Cursor skill file drop. Teaching quality unverified.

Declared: skill. Implemented: markdown. Verified: references resolve. Not verified: T1-T12.

### Fit

Pedagogical sibling, product-unrelated to opportunity intelligence and to VFX. Keep isolated.

### Publish

Private skill snapshot. Public drop needs a licence decision and, if claims are made, recorded behavioural tests.

---

## Set

### Interoperability

Shared: human acceptance, untrusted inputs, status honesty, local-first data, UK English.

Incompatible stacks: opportunity governance; local LM Studio enquiry; conversational tutor; fictional GPU/Nuke pipeline; a review prompt.

See `INTEROP.md` for kernel, adapters, data classes, and trust boundaries.

### Portable architecture

Implemented in this pack as documents and JSON Schema, not as a server.

Kernel envelopes: EvidenceEnvelope, MaturityClaim, LocalTaskContract, SkillSession, MediaJobSpec.  
ActionProposal remains the AIOS schema at repository root. Do not fork it.

Trust boundary: orchestrator host, local inference host, DCC workstation, and public git remote are different machines. Localhost is the executor's.

What stays local: weights, plates, learner identity, credentials, opportunity corpora, personal ChatGPT library.

### Viability, feasibility, desirability

| Keep | Why |
| --- | --- |
| Salwise v1.2 package | Specified enough to start M0; honest about what is missing |
| Tutor skill | Small, safe-by-construction text, usable as a drop |
| AIOS v1.2 as canonical governance | Already the parent snapshot; do not weaken it |
| This kernel | Prevents slogan-level "interop" |

| Isolate | Why |
| --- | --- |
| VFX manual | Overclaim; missing files; stub QC |
| Meta-prompt as currently worded | Pre-certifies A2 |

| Do not do | Why |
| --- | --- |
| Merge to profile `main` | Would replace the GitHub profile README |
| Build a unified router | Salwise and AIOS both forbid it in this increment |
| Deploy Kubernetes GPUs | No Service, no QC, no colour truth |
| Infer productivity or mastery | Explicitly unmeasured |

Desirability of Salwise is `NOT_MEASURED` until Will screens real effort. Desirability of the tutor is plausible for teaching tasks and untested. Desirability of VFX-as-written is low: it would create false confidence.

---

## Blockers versus nits

### Blockers

1. VFX title and meta-prompt preface claim production-grade / zero-liability while QC cannot fail and paths are not files.
2. VFX colour axiom contradicts the Nuke sample.
3. VFX Kubernetes sample is not a deployable manifest.
4. No artefact in this set, including AIOS, is a runtime. Do not enable consequential external execution.
5. Merging this work to `main` would replace the profile README.
6. Salwise target host is unreachable from this review environment. Do not invent local evidence.
7. ChatGPT personal library URLs are not portable; redact before any public drop.

### Nits

1. Tutor zip has no LICENSE or VERSION.
2. Salwise zip has no LICENSE.
3. VFX and meta-prompt have no licence.
4. Tutor resource URLs unverified.
5. Meta-prompt 30-60-90 request is the wrong deliverable shape for A2's maturity.
6. Salwise source-register wording still mentions Stage/Studio; local rows correctly replace those checks, but readers can misread the extract JSON in isolation.

---

## Sequenced action items

Owner means the Human Captain unless another name is listed. "This week" means the next bounded increment, not a calendar promise.

### This week

| ID | Action | File or artefact | Owner | Done when |
| --- | --- | --- | --- | --- |
| W1 | Keep this pack on a stacked branch. Do not merge to `main`. | `portfolio/README.md` | Human Captain | Branch remains unmerged |
| W2 | Treat Salwise as the only execution candidate. On the LM Studio machine, run M0 discovery from `START_HERE.md`. | `artifacts/salwise-local-ai-pap2-v1.2/package/START_HERE.md` | Will / Codex on that host | Inventory of actual OS, model, endpoint, dirty git state |
| W3 | Re-run the Salwise checker after any edit. | `package/check_v1_2_package.py` | Executor | Exit 0, 18/18, runtime still `NOT_RUN` unless a separate run-instance is added |
| W4 | Drop the tutor skill into a local Cursor skills directory if teaching use is wanted. Record T1-T12 as NOT_RUN until executed. | `artifacts/adaptive-learning-tutor-v1.0/package/` | Operator | Skill visible; results file exists |
| W5 | Rewrite A1's opening sentences so they do not call A2 production-grade. | `artifacts/claude-sensemaking-meta-prompt/source.md` (future revision, not silently edited here) | Evaluator | New hash; STATUS updated |
| W6 | Do not extract VFX samples into a fake repo. If work continues, start from axioms and `CLAIMED_VS_DISK.md`. | `artifacts/vfx-ai-pipeline-manual/` | Red-team | No cluster submit |

### Later

| ID | Action | File or artefact | Owner | Done when |
| --- | --- | --- | --- | --- |
| L1 | Salwise M1-M2: one fictional enquiry path, frozen-reference checks, restart notes. | ENQ-001 files; new run-instance record (do not overwrite baseline) | Will | `model_execution` not `NOT_RUN`; human_acceptance still separately recorded |
| L2 | Human screening of 10-20 comparable enquiries, threshold declared first. | Salwise human-pilot sheet (not in zip; to be created then) | Will | Desirability no longer `NOT_MEASURED` |
| L3 | Tutor T1-T12 against a named model, including T2 (no wine leakage) and T8 (minor). | `package/references/QA_TESTS.md` plus a results JSON | Operator | Each case PASS/FAIL with transcript refs |
| L4 | If VFX is still desired: real files, real QC, real colour, real Service, tests that can fail, licence, then an AIOS Action Proposal classed Red. | New tree, not this manual | Studio engineer + Human Captain | `MaturityClaim.implemented_on_disk` true; stub QC gone |
| L5 | Optional kernel implementation: write EvidenceEnvelope JSON for each new run. | `kernel/schemas/evidence-envelope.schema.json` | Executor | Valid JSON per run; no gateway |
| L6 | Public-drop sanitisation of Salwise library URLs, if public is ever intended. | `SANITISATION.md` | Data steward | URLs gone; titles remain |
| L7 | Licence decision per artefact if distribution beyond this snapshot is intended. | Each STATUS | Human Captain | Written choice; default remains All Rights Reserved |

---

## Honest limitations of this evaluation

- No LM Studio, Nuke, Kubernetes, or tutor-model session was available here.
- No independent laboratory colour measurement.
- No legal review of third-party model licences named in A2.
- ChatGPT library sources cited by Salwise were not opened; they are account-scoped.
- Pando / OpenAI Git figures were not re-fetched; Salwise already records a 403 on The New Stack URL and relies on the OpenAI engineering page.
- This pack does not update AIOS `VERSION`, `manifest.json`, or `FILE_INVENTORY.json`. It is not an AIOS release.

Reproduction command:

```text
python3 portfolio/verify_portfolio_pack.py
python3 portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py
```
