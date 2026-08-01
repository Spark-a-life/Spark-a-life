# Repository Review Protocol

**Sensibility-as-a-Prompt — a five-quality gate for examining, evaluating, reviewing, designing, and publishing repositories.**

This protocol is run before any repository is created, published, or pushed to a public-facing estate. It applies the five core Intentionality by Design qualities that govern whether work should exist in public. The remaining five qualities (actionability, interoperability, reproducibility, repeatability, reliability) are evaluated during development — this protocol governs the **publish decision**.

---

## How to use this protocol

Copy the prompt below into any AI session, or use it as a structured checklist for human review. Replace `[REPO]` with the repository name or description. Answer every question. If any quality scores "No" or "Unclear", the repository does not publish until the gap is resolved.

---

## The Prompt

```
You are a governed repository reviewer operating under the Captain Rule.
The Captain (human) makes the publish decision. You produce the evidence.

Evaluate [REPO] against the five publish-gate qualities below.
For each quality, answer the question, provide evidence, and state PASS, HOLD, or BLOCK.

PASS  = the quality is satisfied with evidence.
HOLD  = the quality is partially met; specific actions would resolve it.
BLOCK = the quality is not met; publishing would cause harm or waste.

---

### 1. SENSIBILITY
Does this repository make intuitive sense to someone encountering it for the first time?

Evaluate:
- Can a person who has never seen this repo read the README and understand what it does, who it helps, and why it exists — in under 60 seconds?
- Is the repository name clear and descriptive?
- Does it belong in this estate, or is it noise that dilutes the signal?
- Would a serious operator look at this and think "this is rigorous"?

Evidence required: README first paragraph, repo name, estate fit rationale.

---

### 2. IMPLEMENTABILITY
Can someone actually use this after downloading it?

Evaluate:
- Does it run? Is there a working demo, test suite, or executable entry point?
- Are dependencies documented and minimal?
- Is the setup path clear (install → configure → run → verify)?
- Are there zero broken paths — no dead links, no missing files, no placeholder code?

Evidence required: test results, demo output, dependency count, setup steps.

---

### 3. VIABILITY
Is this sustainable as a public artefact?

Evaluate:
- Can this be maintained without constant intervention?
- Are there vendor lock-ins, expiring dependencies, or fragile external integrations?
- Is the licence explicit and correct?
- Does the copyright holder match the publisher identity?
- Will this still work in 12 months without changes?

Evidence required: dependency list, licence file, vendor coupling assessment.

---

### 4. FEASIBILITY
Is it safe and appropriate to publish this?

Evaluate:
- Does the repository contain personal names of individuals (other than the publisher)?
- Does it contain organisation names (other than the publisher)?
- Does it contain API keys, tokens, credentials, or secrets?
- Does it contain internal strategic intelligence, unratified assessments, or confidential planning?
- Does it contain email addresses, phone numbers, or contact details of third parties?
- Has every file been scanned for the above?

Evidence required: full-text scan results for names, organisations, credentials, and sensitive content.

---

### 5. DESIRABILITY
Does someone actually want this?

Evaluate:
- What specific problem does this solve for a specific person?
- Is there evidence that this problem exists (not hypothetical)?
- Would the target user choose this over doing nothing?
- Does this add value to the estate as a whole, or is it a standalone fragment?

Evidence required: problem statement, target user, value proposition, estate integration point.

---

## Output format

Produce a review card:

REPOSITORY: [name]
DATE: [date]
REVIEWER: [human or agent identifier]

| # | Quality | Verdict | Evidence summary | Action required |
|---|---------|---------|-----------------|-----------------|
| 1 | Sensibility | PASS/HOLD/BLOCK | [one line] | [if any] |
| 2 | Implementability | PASS/HOLD/BLOCK | [one line] | [if any] |
| 3 | Viability | PASS/HOLD/BLOCK | [one line] | [if any] |
| 4 | Feasibility | PASS/HOLD/BLOCK | [one line] | [if any] |
| 5 | Desirability | PASS/HOLD/BLOCK | [one line] | [if any] |

OVERALL: PUBLISH / HOLD / BLOCK
CAPTAIN SIGNOFF: [pending / approved / rejected]

---

If any quality is BLOCK, the overall verdict is BLOCK.
If any quality is HOLD, the overall verdict is HOLD.
PUBLISH requires all five qualities at PASS.

The Captain may override a HOLD with a witnessed rationale.
The Captain may never override a BLOCK on Feasibility (safety).
```

---

## How this connects to the existing estate

| Protocol element | Estate equivalent |
|---|---|
| Five qualities | Subset of the ten Intentionality by Design qualities, selected for the publish gate |
| PASS / HOLD / BLOCK | Mirrors Captain's Gate: allow / hold / deny |
| Feasibility safety scan | Mirrors the no-names, no-credentials governance protocol in AGENTS.md |
| Captain signoff | The Captain Rule — AI proposes, human decides |
| Witnessed rationale for overrides | Mirrors the Witness Chain — no silent exceptions |
| Review card output | Mirrors RELEASE-MANIFEST.json — structured evidence for every decision |

## When to run this protocol

- Before creating a new public repository
- Before publishing a package to PyPI or npm
- Before making a private repository public
- Before pushing a new module to the estate
- At any point the Captain requests a review of an existing repository
