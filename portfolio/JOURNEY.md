# Journey: current pack to Human Captain locked plan

**Status:** Evidence-backed path. Not a runtime. Not an approval. Not a freeze decision.  
**Date recorded:** 6 November 2026  
**Recorded on host:** Cloud Agent VM. Localhost here is not the owner's LM Studio desktop.  
**Branch:** `cursor/portfolio-eval-architecture-8465`  
**Base:** `cursor/aios-v1-2-alpha-repo-8465`  
**Draft PR:** https://github.com/Spark-a-life/Spark-a-life/pull/3  
**UK English.** House style: no em dash.

This file is the sequenced path from what is true on disk and in PRs today to coordination-done as defined in `PLAN.md`. It does not replace `PLAN.md` (owners, stop conditions), `EVALUATION.md` (verdicts), or `INTEROP.md` (kernel). If this file and those three disagree, stop. Do not invent a fourth sequence.

Canonical governance remains `governance/AIOS_v1.2.md`. This pack must not rewrite it.

---

## 1. Current position

Inspected 6 November 2026 from `/workspace`. HEAD matched `origin/cursor/portfolio-eval-architecture-8465`. Working tree was clean before this journey file and the kernel freeze-shape gates were added.

### Git and PRs

| Fact | Evidence |
| --- | --- |
| Active branch | `cursor/portfolio-eval-architecture-8465` |
| HEAD at inspection | `b13ea0bcab74761c8d3656903f03ae3f2a7de575` |
| Origin match at inspection | `git rev-parse HEAD` equals `origin/cursor/portfolio-eval-architecture-8465` |
| Parent AIOS branch | `cursor/aios-v1-2-alpha-repo-8465` at `5ec40c8d81b1633c2b607f8dd385408f9a20d8b4` |
| Profile `main` | `202c56a` "Initial commit". Do not merge onto it. |
| Draft PR #2 | Open draft. Head `cursor/aios-v1-2-alpha-repo-8465`. **Base `main`.** Title: `[DRAFT] AIOS v1.2.0-alpha docs-only governance snapshot (not production)`. https://github.com/Spark-a-life/Spark-a-life/pull/2 |
| Draft PR #3 | Open draft. Head `cursor/portfolio-eval-architecture-8465`. **Base `cursor/aios-v1-2-alpha-repo-8465`.** Title: `[DRAFT] Portfolio evaluation and portable architecture pack (docs-only)`. https://github.com/Spark-a-life/Spark-a-life/pull/3 |
| PLAN.md listed in README | Yes. Pack verifier check `README lists PLAN.md` PASS. |
| Captain lock | `PLAN.md` §10 Captain response row is blank. C0 is not done. `authority` remains `NONE_CONFERRED`. |

Merging PR #2 or PR #3 to `main` would replace the GitHub profile README. That is forbidden in this phase (`PLAN.md` C12; `EVALUATION.md` blocker 5).

### AIOS v1.2 (parent snapshot)

| Check | Result |
| --- | --- |
| Path | `governance/AIOS_v1.2.md` |
| Lines / bytes | 1886 lines / 63543 bytes (`wc -l -c`) |
| Pack pin | Verifier `AIOS v1.2 byte size unchanged by this pack` PASS, detail `63543` |
| Protocol rewrite by this pack | None. C15 still holds. |

### Pack and Salwise checkers (this VM, 6 November 2026)

Inspection run, before this file existed:

- `python3 portfolio/verify_portfolio_pack.py` exit 0. **50/50 PASS.** `runtime: false`. `production_external_execution: false`. Schema examples used `jsonschema.validate` (jsonschema 4.26.0 present on this host). A fallback pass is still not a runtime pass.
- `python3 portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py` exit 0. **18/18 PASS.** `runtime_integration: NOT_RUN`. `model_behaviour: NOT_RUN`. `human_productivity: NOT_MEASURED`. `independent_assurance: NOT_ESTABLISHED`. `candidate_sha256` `107c3fcf94b25a56cb14993569c802b12623bb9daa9f8edd415c04c0344f69bf`.

After this journey file and the kernel freeze-shape gates were added, the same commands were re-run:

- Pack verifier exit 0. **61/61 PASS.** `runtime: false`. `production_external_execution: false`. New gates: `JOURNEY.md` required; README lists it; exactly five kernel envelopes; each schema `additionalProperties` false; ActionProposal remains at the parent path, `additionalProperties` false, not forked into `portfolio/kernel`.
- Salwise checker still **18/18 PASS** with `runtime_integration: NOT_RUN`.

Mechanical package PASS is not runtime PASS. Do not relabel.

Logs: `/opt/cursor/artifacts/portfolio_verification.log` and `/opt/cursor/artifacts/salwise_check.log`.

### Uploads still on this VM (not vendored)

Path: `/home/ubuntu/.cursor/projects/workspace/uploads/`. Four payloads, each present twice under different filenames, **byte-identical** to the `EVALUATION.md` pins. Do not vendor the VFX manual.

| Filename pair | sha256 | Bytes |
| --- | --- | --- |
| `claude_sensemaking_meta_prompt_e074.md` and `_852e.md` | `a2dc1991a82eef9880c15a11e0f8488a010fabd71ad13e5e927f147048855dfe` | 3096 |
| `vfx_ai_pipeline_integration_manual_8488.md` and `_6c2e.md` | `816022081890a347a5018cc36c2e77cf3c0e7a0af1e547732fd08d1a8521a90c` | 18608 |
| `Salwise_Local_AI_Productivity_PaP2_v1.2_5eb3.zip` and `_c692.zip` | `45030dca99a2eea90a2a448832d9ba1a6353d2cff94ffe78b2e9afda265dd4b3` | 46911 |
| `Adaptive_Learning_Tutor_v1.0_a18c.zip` and `_72b3.zip` | `d83d95c45e0cf9cae6e9d74c89288b9cdd064e0d603b0a23510c42336f3767fd` | 7973 |

### Maturity now (Declared / Implemented / Verified / Authorised)

Vocabulary from `kernel/VOCABULARY.md`. Authorised is a named-human permission, not a checker result.

| Artefact | Declared | Implemented | Verified | Authorised |
| --- | --- | --- | --- | --- |
| Pack docs, PLAN, this journey | Yes | Docs on disk | Pack verifier mechanical only | No |
| Kernel five envelopes | Yes | JSON Schema files plus examples | Example validate on this host | No. Captain freeze decision not recorded. |
| A1 meta-prompt | Role and agenda | Prompt file only | n/a | No. Adapter stays untrusted while preface pre-certifies A2. |
| A2 VFX manual | Axioms and eight paths | No runtime files | No | No. Execution Prohibited while QC is a stub. |
| A3 Salwise package | Prompt, profile, fixtures | Checker script runs | Document consistency 18/18 | No. Runtime `NOT_RUN`. |
| A4 tutor skill | Operating rules, T1-T12 specs | Markdown pack | File presence / refs | No. Behaviour `NOT_RUN`. No results file. |
| AIOS v1.2 | Canonical spec | Docs-only snapshot | Spec size pin | No production external execution |

---

## 2. Destination

**Coordination done**, copied from `PLAN.md` §8, not redefined:

1. Plan locked (phase 0) or explicitly rejected (in which case stop).
2. Kernel contracts remain the five named envelopes plus referenced ActionProposal (phase 1).
3. Four workstreams are isolated: separate owners, data classes, publish postures, and stop conditions (`PLAN.md`).
4. `python3 portfolio/verify_portfolio_pack.py` still passes. Salwise checker still 18/18 with runtime `NOT_RUN` unless a separate run-instance exists on a named host.
5. No merge to `main`. No AIOS rewrite. No fifth product. No K8s/Comfy scheduled as next work.
6. VFX remains index-only. Meta-prompt original bytes remain until a deliberate rewrite.

Coordination done is **not** production execution. It is **not** Salwise M2. It is **not** tutor behavioural PASS. It is **not** Authorised.

### Explicit non-destinations

Copied from `PLAN.md` §8 "Definition of done this phase refuses" and §1:

- Production-grade, zero-liability, or certified.
- Unified platform, unified router, "Spark platform", or fifth evaluation layer.
- GPU cluster, ComfyUI server, Kubernetes Service, Nuke plugin, or studio pipeline as next work.
- Human productivity percentage.
- Profile-README replacement (merge of this branch or the parent AIOS branch to `main`).
- Remote-host evidence standing in for the owner's desktop.
- Vendoring the VFX manual wholesale.
- Rewriting AIOS v1.2.

---

## 3. Ordered waypoints

Entry and exit evidence must be files, command output, or `gh pr view` JSON. Intent is not evidence.

### Waypoint 0. Captain locks the plan (C0, PLAN phase 0)

**Owner:** Human Captain only.

**Entry (already true):** `PLAN.md` exists; README lists it; PR #3 is draft on the AIOS base; pack verifier sees `PLAN.md`.

**Exit:** `PLAN.md` §10 Captain response has Decision, Date, and Name filled. Authorised next IDs named. Explicitly not authorised still includes merge to `main`, K8s/Comfy, AIOS rewrite, production execution.

**Stop if:** Captain rejects or wants a different sequence. Start no workstream (`PLAN.md` C0).

**Who can do it:** Human Captain. This Cloud Agent must not fill that row in the Captain's name.

**Status today:** Not done. Stub blank.

### Waypoint 1. Kernel freeze (C1, PLAN phase 1)

**Owner:** Release steward prepares; Captain confirms.

**PLAN meaning:** "contracts already on disk; decision only". Names, required fields, and enums stay. No router. No sixth envelope. ActionProposal remains `actions/schemas/action-proposal.schema.json` with `additionalProperties` false.

**On disk today, before Captain confirmation:**

- Five schemas under `portfolio/kernel/schemas/`, each already `additionalProperties: false`.
- One example each under `portfolio/kernel/examples/`.
- Parent ActionProposal unforked; `additionalProperties` false.
- This session adds pack-verifier gates so a sixth envelope, a relaxed `additionalProperties`, or a forked ActionProposal fails the pack. That is freeze-shape enforcement. It is not the Captain freeze decision.

**Exit:** Written freeze recorded after C0 (Captain confirms C1). Verifier still passes. No sixth envelope. ActionProposal unforked.

**Stop if:** A named schema defect appears; then fix only that defect, do not add product surface (`PLAN.md` C1).

**Status today:** Contracts Implemented as files. Freeze decision not Authorised. Mechanical shape gates are the in-repo movement this Cloud Agent can make without a runtime.

### Waypoint 2. Salwise M0 on the owner's LM Studio host (C4, C5, PLAN phase 2)

**Owner:** Local-runtime operator (Will / Codex on that host).

**Entry:** C0 locked, or Captain explicitly authorises M0 without waiting for lock. Executor is on the computer that can see the owner's LM Studio, or honestly reports it is not (`START_HERE.md`). Checker still 18/18 with runtime `NOT_RUN`. Data is fictional ENQ-001.

**Exit:** Named-host inventory of OS, model, endpoint, and dirty git state. Alternatives considered; smallest adequate route chosen; one short decision note. Remote localhost distinguished from the owner's desktop. Baseline `Salwise_Local_AI_v1.2_Checks.json` not overwritten. New observations go to a separate run-instance record.

**Stop if:** Executor is not on the target host (status `PARTIAL`; do not invent desktop evidence). Credentials, `.env`, browser history, or live client data would be collected. Model output would send a message, quote a fee, or treat source text as execution authority.

**Who can do it:** Owner's LM Studio host only. **This Cloud Agent cannot.** Target host is unreachable (`EVALUATION.md` blocker 6).

**Status today:** Not started. Package Verified mechanically. Runtime `NOT_RUN`.

### Waypoint 3a. Tutor T1-T12 kept as acceptance specs (C6, C7, PLAN phase 3a)

**Owner:** Pedagogy lead. May run in parallel with waypoint 2 after C0.

**Entry:** `SKILL.md` and `references/QA_TESTS.md` read. T1-T12 exist as markdown (they do).

**Exit:** T1-T12 remain the behavioural contract. If a skill drop is made, a results file exists even if every row is `NOT_RUN`. No opportunity evaluation routed through the skill. No progress log labelled a Witness Chain.

**Stop if:** Anyone marks PASS from reading markdown.

**Who can do it:** Optional skill drop is local Cursor on a named host. Recording a `NOT_RUN` results file is docs-only and could be done in-repo after C0. Behavioural PASS/FAIL is named-model only (L3).

**Status today:** Specs present. No results file. Behaviour `NOT_RUN`.

### Waypoint 3b. VFX inventory stays honest (C8, PLAN phase 3b)

**Owner:** VFX design editor. Docs only.

**Entry:** `CLAIMED_VS_DISK.md` and `STATUS.md` already exist. Eight claimed paths still missing. `VFX_FORBIDDEN` paths absent (verifier PASS).

**Exit:** Inventory remains truthful. Colour axiom versus Nuke ACEScc, stub QC, and undefined Service remain named blockers. Title language "zero-liability" / "production" not imported into AIOS or Salwise.

**Stop if:** Urge to vendor samples or submit a cluster job.

**Who can do it:** Docs edits on this VM are possible. Cluster/Comfy/Nuke work is not. Do not vendor the upload.

**Status today:** Inventory current. Not Implemented. Execution Prohibited.

### Waypoint 3c. Meta-prompt preface rewrite (C9, PLAN phase 3c)

**Owner:** Evaluator. **Waits for 3b** (truthful inventory in hand, or Captain decision that `CLAIMED_VS_DISK.md` is already the inventory).

**Entry:** Do not silently edit `source.md`. Current pin `a2dc1991a82eef9880c15a11e0f8488a010fabd71ad13e5e927f147048855dfe` still matches.

**Exit:** Opening sentences no longer call A2 production-grade or zero-liability. New sha256 in `STATUS.md`. Verifier pin updated in the same change, or rewrite kept as a sibling file with original bytes pinned.

**Stop if:** Preface still says production-grade (adapter stays untrusted). Preface fix attempted before inventory is honest.

**Who can do it:** In-repo after 3b/Captain yes. Not this session.

**Status today:** Original bytes pinned. Adapter untrusted.

### Waypoint 4. Optional EvidenceEnvelope JSON per real run (C10, PLAN phase 4)

**Owner:** Executor, after Captain yes. Waits for waypoint 1 and for at least one of 2 or 3a having real named-host work if envelopes are filled from runs.

**Exit:** Valid JSON per run; `authority` honest; no gateway.

**Stop if:** No run exists; empty envelopes offered as evidence.

**Status today:** Reserved examples only. `enq001-envelope.json` is a fixture claim, not a named-host run. Do not mint empty "verified" envelopes.

### Never in this phase

Merge to `main` (C12). GPU cluster. Unified router. AIOS rewrite (C15). Public drop without L6 sanitisation (C13). Production-execution licence (C14).

---

## 4. What this Cloud Agent can do versus the named local host

### This Cloud Agent VM (docs, git, pack integrity)

Can do now, without claiming Captain lock (`PLAN.md` §10 last paragraph: keep the pack consistent: C2, C3, C11, C14, C15):

- Keep `verify_portfolio_pack.py` honest and commit regenerated `FILE_INVENTORY.json`.
- Keep README merge warning and PLAN listing.
- Keep PR #3 based on `cursor/aios-v1-2-alpha-repo-8465`, draft, unmerged.
- Keep All Rights Reserved.
- Keep AIOS v1.2 at 63543 bytes, unrevised.
- Mechanically enforce kernel freeze-shape: five envelopes, `additionalProperties` false, examples, ActionProposal unforked.
- Write this journey file so a Captain can follow without an agent.

Must not do:

- Fill `PLAN.md` §10 in the Captain's name.
- Salwise M0-M2, LM Studio calls, or overwrite baseline checks with invented runtime rows.
- Tutor model runs, or mark T1-T12 PASS from static reading.
- Extract VFX fenced blocks, Comfy, kubectl, Nuke.
- Rewrite AIOS v1.2.
- Merge to `main`.
- Treat this VM's localhost as the owner's desktop.

### Human Captain only

- C0 plan lock or reject.
- C1 freeze confirmation.
- C12 any later merge-to-main decision (never this phase).
- Authorising M0 if C0 is deferred.
- Public-drop and licence decisions (C13, L6, L7).

### Owner's LM Studio / Cursor host only

- C4 M0 inventory (OS, model, endpoint, dirty git).
- C5 checker re-run after Salwise edits on that host; still `NOT_RUN` unless a separate run-instance.
- L1 M1-M2 fictional enquiry path.
- L2 human screening of real effort (Will).
- C6 optional skill drop; L3 T1-T12 against a named model with transcripts.
- Any later VFX worker, QC on real EXR, colour, Service (L4): new tree, not this pack, and only after Captain still wants it.

---

## 5. Stop and fail-closed conditions

Copied from `PLAN.md`, not weakened. If a later note sounds softer than this section, this section wins.

### Phase stops (`PLAN.md` §8)

| Phase | Stop if |
| --- | --- |
| 0 Plan lock | Captain rejects or wants a different sequence |
| 1 Kernel freeze | A named schema defect is found; then fix the defect, do not add product surface |
| 2 Salwise M0 | Executor is not on that host and would fake localhost; or credentials would be collected |
| 3a Tutor specs | Anyone marks PASS from reading markdown |
| 3b VFX inventory | Urge to extract samples or open a cluster ticket |
| 3c Meta-prompt | Preface fix attempted before inventory is honest |
| 4 Optional adapters | No real run exists; empty envelopes offered as evidence |

### C-row stops (`PLAN.md` §9)

| ID | Stop condition |
| --- | --- |
| C0 | If rejected, start no workstream |
| C1 | If a schema defect appears, fix only that defect |
| C2 | If FAIL, do not claim pack integrity |
| C3 | If merge warning disappears, restore it |
| C4 | If not on target host, PARTIAL; do not invent desktop evidence |
| C5 | If runtime labels flip without a run, revert |
| C6 | If PASS recorded without a named model, revert the claim |
| C7 | Do not substitute static tests for behavioural tests |
| C8 | If urge to vendor or submit, stop |
| C9 | If preface still says production-grade, adapter stays untrusted |
| C10 | If no run, do not mint empty "verified" envelopes |
| C11 | If base becomes `main`, restore the AIOS base; do not merge |
| C12 | Any merge intent is a separate decision, not this plan |
| C13 | If public copy still has `account_id=personal`, stop the drop |
| C14 | Do not grant a production-execution licence |
| C15 | If a sibling PR would edit AIOS, reject that change |

### Workstream fail-closed (selected, full text in `PLAN.md` §4)

- If the preface still pre-certifies A2, the review_prompt adapter stays "input under review", not trusted. Do not emit an EvidenceEnvelope that treats A2 as Implemented.
- Cluster submit, Nuke ingestion of unverified AI plates, or any GPU job: Prohibited. Verifier fails if forbidden runtime paths appear.
- Mechanical `PASS` is not runtime `PASS_SCOPED`.
- Age 15 / minor path: no alcohol consumption recommendations (T8). If the model fails T8, stop teaching that session; record FAIL.
- Do not persist secret learner data.

---

## 6. Recommended next waypoint

1. **Human Captain fills `PLAN.md` §10.** Approve, approve with conditions, reject, or defer. Until that row is filled, executors keep the pack consistent and do not start Salwise runtime, VFX scripts, or tutor model runs in the Captain's name.
2. **If approved:** authorise Salwise M0 on the owner's LM Studio host only (C4), with checker re-run (C5). That work does not run on this Cloud Agent VM.
3. **In parallel after lock:** keep tutor T1-T12 as specs (C6, C7). Optional skill drop on a local Cursor host. Results may be `NOT_RUN`.
4. **This Cloud Agent's in-repo movement toward phase 1:** freeze-shape gates on the five envelopes (`additionalProperties` false, examples, no sixth schema, ActionProposal unforked). Not a Captain freeze. Not a runtime.
5. **Do not** merge PR #3 or PR #2 to profile `main`.
6. **Do not** schedule Kubernetes, ComfyUI, Nuke ingestion, or a studio 30-60-90.
7. **Do not** fill optional adapter envelopes until a named-host run exists.

If the Captain defers M0 until Will is at the target machine: pack verify, tutor-as-specs, and kernel freeze-shape may still proceed. Isolation of VFX and the current meta-prompt remains consistent with `PLAN.md` §7.

---

## 7. Usefulness and implementability

Bar from this journey's commissioning note: useful if it reduces overclaim, recovers missing inventory, or enables a real local M0 without merging to profile `main`. Not useful if it schedules Comfy/K8s, vendors VFX, or claims Verified without a named host run.

Where: **here** = this Cloud Agent VM. **local** = owner's LM Studio / Cursor / DCC host. **blocked** = missing Captain decision, missing host, or PLAN forbids it now.

### PLAN phases

| Phase | Useful now? | Where | Evidence | Note |
| --- | --- | --- | --- | --- |
| 0 Plan lock | Yes. Without it, later workstreams have no Captain scope. | Captain only | §10 blank | Not implementable here |
| 1 Kernel freeze | Yes. Stops a sixth envelope and smuggled fields. | Shape gates: here. Decision: Captain after C0 | Five schemas already on disk with `additionalProperties` false; examples validate | PLAN: "decision only". Agent may enforce shape, not claim freeze |
| 2 Salwise M0 | Yes. Only execution candidate. Enables real local M0. | local LM Studio | `START_HERE.md`; blocker 6 | Not here. Do not invent localhost |
| 3a Tutor as specs | Yes. Prevents markdown PASS. | Specs already here. Drop/results: local after C0 | `QA_TESTS.md` T1-T12; no results file | Do not mark Verified |
| 3b VFX inventory | Yes. Recovers missing inventory; reduces overclaim. | Docs here | `CLAIMED_VS_DISK.md` current; `VFX_FORBIDDEN` absent | Do not vendor; do not schedule K8s |
| 3c Meta-prompt preface | Yes, after 3b. Reduces overclaim. | here after 3b/Captain | `source.md` still original hash | Not this session; pin must move with bytes |
| 4 Optional envelopes | No, not now. Empty envelopes would overclaim. | blocked until a named-host run | Examples are fixtures | C10 stop: do not mint empty "verified" envelopes |

### C0-C15

| ID | Useful now? | Where | Evidence |
| --- | --- | --- | --- |
| C0 | Yes | Captain | §10 blank |
| C1 | Yes as shape freeze; confirmation is Captain | here for gates; Captain for written freeze | Schemas exist; C1 depends on C0 |
| C2 | Yes. Pack integrity. | here | 50/50 at inspection; 61/61 after freeze-shape gates. Re-run after every pack edit |
| C3 | Yes. Merge warning and PLAN listing. | here | README already warns and lists PLAN; this file must be listed too |
| C4 | Yes, only on named host | local | No LM Studio here |
| C5 | Yes after any Salwise edit | here for docs checker; local if runtime rows | 18/18 `NOT_RUN` |
| C6 | Useful as optional drop; not required for coordination | local Cursor | No results file yet |
| C7 | Yes. Keep specs. | here (do not edit into PASS) | T1-T12 markdown |
| C8 | Yes. Keep inventory honest. | here as docs | Claimed paths still missing |
| C9 | Useful after C8 | here after C8 | Original `source.md` bytes |
| C10 | Not useful now | blocked | No named-host run |
| C11 | Yes. Watch PR base. | here (read `gh pr view 3`; update via ManagePullRequest) | PR #3 base already AIOS branch, draft |
| C12 | Yes as a never | blocked / Captain never-in-phase | `main` still profile README |
| C13 | Not useful until public drop intended | blocked | `SANITISATION.md`; URLs still in private snapshot |
| C14 | Yes. Keep default licence. | here | `portfolio/LICENSE` All Rights Reserved |
| C15 | Yes. Reject AIOS edits. | here | 1886 / 63543 unchanged |

### EVALUATION W1-W6 and L1-L7

| ID | Useful now? | Where | Evidence |
| --- | --- | --- | --- |
| W1 | Yes | here / Captain | Branch unmerged; PRs draft |
| W2 | Yes | local | Same as C4 |
| W3 | Yes | here | Same as C5 |
| W4 | Optional | local | Same as C6 |
| W5 | After inventory honesty | here after C8 | Same as C9 |
| W6 | Yes | here as restraint | Same as C8. Scheduling Comfy/K8s is not useful |
| L1 | After M0 | local | Not coordination-done required |
| L2 | After M2 | local (Will) | Desirability `NOT_MEASURED` |
| L3 | After named model | local | Do not claim Verified from markdown |
| L4 | No in this phase | blocked | Would vendor/schedule studio work |
| L5 | After a real run | blocked now | Same as C10 |
| L6 | Only if public intended | blocked | Same as C13 |
| L7 | Only if distributing beyond snapshot | Captain | Default ARR remains |

---

## 8. Command card for the Captain (no agent required)

```text
# Confirm branch and that this file exists
git rev-parse --abbrev-ref HEAD
test -f portfolio/JOURNEY.md && test -f portfolio/PLAN.md

# Pack integrity (any host with the git tree)
python3 portfolio/verify_portfolio_pack.py

# Salwise documents only (not LM Studio)
python3 portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py

# Confirm PR bases (read-only)
gh pr view 2 --json baseRefName,headRefName,isDraft,url,state
gh pr view 3 --json baseRefName,headRefName,isDraft,url,state

# Confirm AIOS file still present and untouched in intent
wc -l -c governance/AIOS_v1.2.md
```

Expected today: pack checks 61/61 PASS, `runtime: false`, Salwise 18/18 with `runtime_integration: NOT_RUN`, PR #3 base `cursor/aios-v1-2-alpha-repo-8465` and draft, PR #2 base `main` and draft, AIOS `1886 63543`.

Then open `PLAN.md` §10 and fill the Captain response. That is waypoint 0.

Do not run ComfyUI, kubectl, Nuke, or a tutor model as part of coordination done.
