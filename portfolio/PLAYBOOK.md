# Playbook: how to run the four-pack work without breaking anything

**Who this is for:** a smart 16-year-old, and a teammate who was not in the original chat.  
**What this is:** a how-to. Short sentences. One meaning per word.  
**What this is not:** a new plan, an approval, or a licence to run live work.  
**UK English.** House style: no em dash.  
**If this file and `PLAN.md` disagree, `PLAN.md` stop conditions win.** Do not invent a second sequence.

Serious tables live in `PLAN.md` and `JOURNEY.md`. Use those after you understand this file.

**Decision already recommended (not yet locked):** Captain lock, then Salwise M0 on the owner's LM Studio host only. Do not merge to profile `main`. Do not treat pack PASS as runtime PASS. Do not vendor VFX or schedule Kubernetes or ComfyUI. Until the Captain fills `PLAN.md` section 10, nobody starts Salwise runtime, VFX scripts, or tutor model runs in the Captain's name.

---

## 1. What this project is, and what it is not

### What it is

This folder is a **pack**. A pack is a set of files that travel together and can be checked as a set.

Inside the pack are **four sibling artefacts**. An artefact is a finished piece of work you can point at. Sibling means they share an owner and some shared rules. They do not share one product name, one codebase, or one "run" button.

The four siblings:

1. **A1. Review prompt.** A short instruction for reading the VFX notes. It is not an engine.
2. **A2. VFX notes.** A design sketch about film-effects software. VFX means visual effects. The sketch names files that are not on disk. It is not a pipeline.
3. **A3. Salwise.** A local-AI work brief plus a document checker. Salwise is the name of that brief. It is the only sibling that is ready to try, and only on one named computer. It is not proof that anyone got faster.
4. **A4. Tutor.** A teaching skill for the Cursor editor. Cursor is the coding app this work lives in. The tutor is homework sheets plus rules. It is not a school app, and it has not been taught to a real student in this pack.

There is also a **kernel**. The kernel is a small set of shared forms and shared words, so the four siblings do not invent four different languages. The kernel is not a server.

Above the pack sits **AIOS**. AIOS is the rulebook for how this repository treats claims, evidence, and permission. The current snapshot is `governance/AIOS_v1.2.md`. This pack must not rewrite it.

A **Human Captain** is the named person with final say. Possession of this playbook does not make you the Captain. Until the Captain writes their name in `PLAN.md` section 10, authority is `NONE_CONFERRED`. That phrase means: no permission has been given.

### What it is not

- **Not one app.** Do not build a "Spark platform" that pretends to run all four.
- **Not a live robot.** Nothing here is allowed to send a real message, quote a real fee, submit a cluster job, or teach a live student and then claim it worked.
- **Not a merge to the GitHub profile.** GitHub is the website that stores this code. A **profile README** is the page strangers see on the account. Branch `main` currently holds that page. Merging this work onto `main` would replace that page. Do not do that unless the Captain means to replace it.

Also not: a GPU cluster, a ComfyUI server, Kubernetes, a Nuke plugin, or a studio pipeline as the next job. Those words name film and cluster tools. They are out of scope for this phase.

---

## 2. The three traffic lights

These lights match the AIOS action classes Green, Amber, and Red. A fourth class, **Prohibited**, means never, not even with a yes from a helper.

### Green = do this

Anyone with a copy of the git tree (the folder of files stored in Git) may:

- Read the pack.
- Run the pack verifier (defined in section 4).
- Keep pull requests as drafts (defined in section 4).
- Keep AIOS v1.2 untouched.
- Keep tutor tests labelled as not run.
- Keep the VFX contents list honest.
- Leave `PLAN.md` section 10 blank unless you are the Captain.

### Amber = only with a named person and a named computer

Write both names down first. Person and computer. Then, and only then:

- Salwise **M0** on the owner's **LM Studio** host. M0 means milestone zero: look at the real machine and write down what is on it. LM Studio is the app on that desktop that serves a local language model. A language model is the program that writes text. The named person is the local-computer operator (often Will, with Codex on that host). Codex is a coding assistant used as an implementer, not as an authoriser.
- Optional copy of the tutor skill into a local Cursor skills folder.
- Later Salwise steps (M1, M2) after M0 is real. Not this playbook's job to start them.

### Red = stop

Stop if you are about to:

- Merge to `main`.
- Treat a document checker PASS as proof the tutor or Salwise "works" on a live model.
- Copy the VFX sketch's sample code into fake project files.
- Schedule Kubernetes, ComfyUI, Nuke ingestion, or a 30-60-90 studio plan.
- Rewrite AIOS v1.2.
- Fill a "verified" envelope with no real run (envelope is defined in section 3).
- Describe this Cloud Agent's localhost as the owner's desktop (localhost is defined in section 3).
- Collect passwords, `.env` files, browser history, or live client records.
- Mark tutor tests PASS because you read the markdown (plain text with headings).

If the lights conflict with a later chat message, these lights and `PLAN.md` win.

---

## 3. Words you must not mix up

Read this once. Then use the words as written.

### Declared vs Implemented vs Verified vs Authorised

These four words describe **maturity**: how grown-up a claim is.

| Word | Plain meaning | Example in this pack | Must not be inferred from |
| --- | --- | --- | --- |
| **Declared** | Someone wrote the intention down. | VFX manual names eight scripts. | A title that says "production". |
| **Implemented** | A real file, service, or script exists on a named computer. | Salwise checker script runs. | A code sample inside a manual. |
| **Verified** | An independent check ran against that real thing, and the result was kept. | Salwise documents match their manifest. | A stub that always returns a pass score. |
| **Authorised** | A named human said yes, under a stated scope. | Not true of any sibling yet. | A passing checker, sample code, or silence. |

Declared is not Implemented. Implemented is not Verified. Verified is not Authorised.

### Pack PASS vs runtime PASS

A **pack PASS** means: the files in this folder are complete, fingerprint-checked, and consistent. You get it by running `python3 portfolio/verify_portfolio_pack.py`. It is a filing check.

A **runtime PASS** (Salwise name: `PASS_SCOPED`) means: a real program ran on a named host against a named model, and that run was recorded. Nobody has that yet. Salwise still says `runtime_integration: NOT_RUN`.

The Salwise **document checker** is a second filing check: `python3 portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py`. It can PASS 18/18 while runtime stays `NOT_RUN`. That is correct. Do not relabel it.

### Localhost here vs the owner's desktop

**Localhost** means "this computer", the one running the command.

**Here**, in Cloud Agent logs, localhost is a remote virtual machine (a rented computer in the cloud). A Cloud Agent is an assistant running in Cursor's cloud, not on the owner's desk.

**The owner's desktop** is the computer that can see LM Studio. Salwise M0 belongs there. A result from here must not be described as a result from there.

If you are not on that desktop, say so. Status is then `PARTIAL`. Do not invent desktop evidence.

### Extra words used below (once each)

- **Git:** the tool that stores versions of these files. A **branch** is a named line of work in Git. This work is on `cursor/portfolio-eval-architecture-8465`.
- **Pull request (PR):** a proposal to copy one branch onto another. **Draft** means "not ready to accept". **Merge** means "accept the copy".
- **Base branch:** the branch a PR would copy onto. PR #3 must stay based on `cursor/aios-v1-2-alpha-repo-8465`, not on `main`.
- **JSON:** a structured text file a computer can check. An **envelope** is a filled-in JSON form that records one claim or one run. Empty envelopes are not evidence.
- **Fixture:** a made-up example used for tests. The Salwise enquiry ENQ-001 is fictional. Fictional means invented on purpose, and labelled so.
- **Inventory:** a contents list. `CLAIMED_VS_DISK.md` is the VFX inventory. `FILE_INVENTORY.json` is the pack inventory of hashes. A hash is a fingerprint of file bytes.
- **Vendor / vendoring:** copying a whole outside file tree into this pack. The VFX manual must not be vendored wholesale.
- **Preface:** the opening sentences of the review prompt. Those sentences currently call the VFX notes production-grade. That is false.
- **C0, C4, C5, C6, C7:** row IDs in `PLAN.md` section 9. They name the lock, Salwise M0, the Salwise checker, and the tutor-as-specs work.

---

## 4. Step-by-step procedure

Do the steps in order unless the step says it may run in parallel. One action per step. Do not skip ahead to look finished.

The Captain may reject the plan at step 2. If they do, stop. Start no workstream.

### Step 1. Confirm you are looking at the right folder

Open the repository. Check the branch name is `cursor/portfolio-eval-architecture-8465`.

Read `portfolio/README.md`. Notice the warning: do not merge this branch to profile `main`.

**You will know it worked if:** `git rev-parse --abbrev-ref HEAD` prints that branch name, and README still says not to merge to profile `main`.

**Stop if:** you are on `main`, or someone has already merged. Do not continue as if this were a profile update.

### Step 2. Lock the plan (Captain only)

Open `portfolio/PLAN.md` section 10. Fill Decision, Date, and Name. Name the authorised next IDs. Keep "Explicitly not authorised" including: merge to `main`; Kubernetes/Comfy; AIOS rewrite; production execution.

Recommended fill, matching the already-made advisory:

- Decision: Approve plan.
- Authorised next IDs: C0, then C4 and C5 (Salwise M0 on the owner's LM Studio host only), plus C6/C7 as specs.
- Named hosts in scope: the owner's LM Studio computer only.

A Cloud Agent must not fill this row in the Captain's name.

**You will know it worked if:** section 10 has a real name, a date, and a decision. Authority is no longer an empty stub.

**Stop if:** the Captain rejects or wants a different sequence. Start no workstream. Pack filing work (verifier, README warning, PR base) may still continue. Runtime work must not.

### Step 3. Keep pull requests draft

PR #3 is the portfolio pack. It must stay draft. Its base must stay `cursor/aios-v1-2-alpha-repo-8465`.

PR #2 is the parent AIOS snapshot. It is also draft. Its base is `main`. That is a hazard, not an invitation. Do not merge it either.

**You will know it worked if:** `gh pr view 3 --json baseRefName,isDraft` shows that base and `isDraft: true`.

**Stop if:** the base becomes `main`. Restore the AIOS base. Do not merge. Never merge unless the Captain means to replace the GitHub profile README.

### Step 4. Run the filing checks (any computer with the git tree)

From the repository root:

```text
python3 portfolio/verify_portfolio_pack.py
python3 portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py
```

The first command rewrites `FILE_INVENTORY.json`. Commit that file in the same change as any pack edit.

**You will know it worked if:** the pack verifier prints all PASS, `runtime: false`, and `production_external_execution: false`. The Salwise checker prints 18/18 PASS with `runtime_integration: NOT_RUN` and `model_behaviour: NOT_RUN`.

**Stop if:** either checker FAILs. Do not claim pack integrity. Do not flip runtime labels to PASS without a separate run-instance on a named host.

### Step 5. Salwise M0 on the LM Studio computer only (Amber)

Do this only after step 2, or after the Captain has explicitly authorised M0 without waiting for lock.

Sit at the owner's LM Studio computer. Follow `portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/START_HERE.md`. Discover actual operating system, model name, endpoint (the address the model answers on), and dirty git state (uncommitted local changes). Choose the smallest adequate route. Write one short decision note. Keep the fictional ENQ-001 fixture. Do not overwrite `Salwise_Local_AI_v1.2_Checks.json` with invented runtime rows. Put new observations in a separate run-instance record.

This Cloud Agent cannot do this step. The target host is unreachable from the review virtual machine.

**You will know it worked if:** a named-host inventory exists, localhost on that inventory is the owner's desktop, and the baseline checker file still says `NOT_RUN` unless a separate run-instance was added.

**Stop if:** you are not on that host (status `PARTIAL`; do not invent desktop evidence). Stop if credentials, `.env` values, browser history, or live client data would be collected. Stop if the model output would send a message, quote a fee, or treat source text as permission.

### Step 6. Keep tutor tests as homework sheets (may run in parallel with step 5 after lock)

T1-T12 are twelve written tests in `portfolio/artifacts/adaptive-learning-tutor-v1.0/package/references/QA_TESTS.md`. Treat them as the mark scheme. They are not a sitting of the exam.

If you copy the skill into a local Cursor skills folder, also keep a results file. Every row may say `NOT_RUN`. That is honest.

**You will know it worked if:** T1-T12 still exist as specs, and any results file does not claim PASS without a named model on a named host.

**Stop if:** anyone marks PASS from reading markdown. Revert that claim. Do not route opportunity scoring through the tutor. Do not call a progress log a Witness Chain (an AIOS audit record).

### Step 7. VFX: rewrite the contents list only

Open `portfolio/artifacts/vfx-ai-pipeline-manual/CLAIMED_VS_DISK.md`. Keep every claimed path marked declared, missing, or contradicting. You may add newly noticed rows. You may not create the missing files. You may not copy the 575-line manual into this pack.

**You will know it worked if:** the inventory is still truthful, and no forbidden runtime path exists under `artifacts/vfx-ai-pipeline-manual/` (the verifier fails if those paths appear).

**Stop if:** you feel the urge to extract sample code, open a cluster ticket, or schedule Kubernetes or ComfyUI. Those are Red. Future studio work, if ever wanted, is a new tree after the Captain still wants it. Not this phase.

### Step 8. Fix the review prompt so it does not call the VFX file production-grade

This step waits for step 7 (or for the Captain to say the current inventory is already enough).

Do not silently edit `source.md`. Either write a sibling file and leave the original bytes pinned, or rewrite in place and record the new hash in `STATUS.md` and in the verifier pin in the same change.

Keep the useful review agenda (space, colour, concurrency, quality control). Drop or reframe the 30-60-90 request (a three-month delivery timetable) so it cannot invent a delivery plan for a missing product.

**You will know it worked if:** the opening sentences no longer call A2 production-grade or zero-liability, and the hash story in `STATUS.md` matches the bytes on disk.

**Stop if:** the preface still says production-grade. Then the prompt stays an input under review, not a trusted adapter (a trusted way to plug that prompt into the kernel). Stop if you try this fix before the inventory is honest.

### Step 9. Do not fill "verified" envelopes unless a real run happened

The kernel has five envelope types. Examples under `portfolio/kernel/examples/` are fixtures. They are not named-host runs.

After a real run on a named host, you may write one EvidenceEnvelope JSON per run, valid against the schema (the rules file for that form), with honest `authority`. No gateway (no live router that executes actions). No sixth envelope.

**You will know it worked if:** either you wrote nothing (correct today), or each new JSON points at a real run and does not say Verified without that run.

**Stop if:** there was no run and someone offers empty envelopes as evidence. Do not mint them.

### Step 10. Leave AIOS v1.2 and profile `main` alone

Confirm `governance/AIOS_v1.2.md` is still 63543 bytes. Confirm this branch is still unmerged.

**You will know it worked if:** `wc -c governance/AIOS_v1.2.md` prints `63543`, and neither PR #2 nor PR #3 is merged to `main`.

**Stop if:** a change would edit AIOS. Reject that change. Stop if anyone treats merge as a chore. Merge is a separate Captain decision, and it is not this phase.

---

## 5. Who does what

Role labels name who does the work. They do not authorise the work. The Captain still says yes.

| Who | Does | Must not |
| --- | --- | --- |
| **Human Captain** | Fill `PLAN.md` section 10. Confirm kernel freeze later (a freeze means: keep the five shared forms as they are; add no sixth form and no router). Decide any future merge or public drop. Authorise M0 if lock is deferred. | Be inferred from silence. |
| **Local-computer operator** (Will / Codex on the LM Studio host) | Salwise M0 inventory. Re-run the Salwise checker after edits on that host. Optional tutor skill drop. Later M1-M2 and human screening, only if authorised. | Describe a remote agent's localhost as that desktop. Collect live client data. |
| **This Cloud Agent** | Keep the pack consistent: verifier, `FILE_INVENTORY.json`, README warnings, PR #3 base, All Rights Reserved, AIOS size pin, this playbook. | Fill section 10 in the Captain's name. Start Salwise M0. Mark tutor PASS. Extract VFX samples. Rewrite AIOS. Merge. |

Other named roles (evaluator, data steward, pedagogy lead, VFX design editor, release steward) are defined in `PLAN.md` section 2. You do not need them to follow this playbook. You do need them before you start a specialised workstream.

---

## 6. Printable checklist

Copy, print, tick.

**Before anything live**

- [ ] I read this playbook.
- [ ] I know the four siblings are not one app.
- [ ] I know AIOS v1.2 must not be rewritten.
- [ ] I am on branch `cursor/portfolio-eval-architecture-8465`, not `main`.
- [ ] `PLAN.md` section 10 is filled by the Captain, or I am only doing filing checks.

**Green (do)**

- [ ] Pack verifier PASS, `runtime: false`.
- [ ] Salwise checker 18/18, runtime still `NOT_RUN` unless a separate named-host record exists.
- [ ] PR #3 is draft. Base is the AIOS branch. Not merged.
- [ ] Tutor T1-T12 still read as homework sheets.
- [ ] VFX inventory still says the eight paths are missing.
- [ ] Review prompt is not used as if VFX were production-grade.

**Amber (named person + named computer)**

- [ ] Person named: __________________
- [ ] Computer named: __________________
- [ ] That computer can see LM Studio.
- [ ] Salwise M0 inventory is of *that* machine, not of a cloud VM.
- [ ] No passwords, `.env`, or live client files were collected.

**Red (tick only if the forbidden thing still has not happened)**

- [ ] I did **not** merge to `main`.
- [ ] I did **not** treat pack PASS as runtime PASS.
- [ ] I did **not** vendor VFX or schedule Kubernetes / ComfyUI.
- [ ] I did **not** fill a verified envelope with no real run.
- [ ] I did **not** mark tutor tests PASS from reading the file.
- [ ] I did **not** rewrite AIOS v1.2.

If you merged, vendored VFX, or claimed a runtime PASS, you have left the playbook. Stop and tell the Captain.

---

## 7. Where the adult tables live

This playbook is the shareable how-to. It does not replace the source files.

| Need | File |
| --- | --- |
| Owners, stop conditions, phase order | `portfolio/PLAN.md` |
| What is true on disk and in PRs today | `portfolio/JOURNEY.md` |
| Verdicts, hashes, blockers | `portfolio/EVALUATION.md` |
| Shared forms and trust boundaries | `portfolio/INTEROP.md` |
| Word meanings | `portfolio/kernel/VOCABULARY.md` |
| Pack layout and merge warning | `portfolio/README.md` |
| Canonical rulebook (do not edit) | `governance/AIOS_v1.2.md` |

Command card (filing only; not LM Studio, not ComfyUI, not kubectl, not Nuke, not a tutor model):

```text
git rev-parse --abbrev-ref HEAD
python3 portfolio/verify_portfolio_pack.py
python3 portfolio/artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py
gh pr view 3 --json baseRefName,headRefName,isDraft,url,state
wc -c governance/AIOS_v1.2.md
```
