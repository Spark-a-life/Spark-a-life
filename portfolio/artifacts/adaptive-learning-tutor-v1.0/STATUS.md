# STATUS: Adaptive Learning Tutor v1.0

**Primary lens:** product reviewer, with privacy/safety and release-readiness.  
**Vendored:** yes, original bytes, under `package/`  
**Behavioural tests:** `NOT_RUN`

## What it actually is

A Cursor skill: `SKILL.md` plus six reference files. It instructs an assistant to build curricula, 30-day plans, Socratic assessment, and a portable Markdown progress log. Default topic is wine appreciation when the learner specifies none and context is already about wine.

It is not an app, not a learning-management system, not persistent memory, and not a certificate issuer.

## Completeness versus own claims

`SKILL.md` lists six reference files. All six exist:

- `references/CURRICULUM.md`
- `references/ASSESSMENT.md`
- `references/PLAN.md`
- `references/RESOURCE_POLICY.md`
- `references/WINE_EXAMPLE.md`
- `references/QA_TESTS.md`

No extra files. No missing files. No LICENSE in the zip.

T1-T12 in `QA_TESTS.md` are human-in-the-loop acceptance tests. They say local static tests do not substitute for real-model behavioural tests. That is correct and observed: this review did not run them against a model.

## Quality

Small and coherent. Safety rules for minors, alcohol, copyright, fabricated book contents, and fake decimal ratings are explicit.

Limits:

- Wine-default trigger can leak into an unspecified topic if the model ignores T2. That is a behavioural risk, not a file defect.
- Resource URLs are home domains to verify, not verified in this session.
- No version file, no owner field, no licence.

## Data

No secrets. No learner PII. Named works (MacNeil, Johnson, Robinson, WSET) are public bibliographic references. Invented learner names are forbidden by the skill itself.

## Implementability tomorrow

Yes, as a skill drop: copy `package/` to a Cursor skills directory and invoke it. Repeatability of teaching quality is unproven until T1-T12 are run and recorded.

Declared: skill behaviour.  
Implemented: markdown only.  
Verified: file presence and internal references.  
Not verified: model compliance.

## Fit to AIOS / Spark-a-life

Unrelated as a product; complementary as pedagogy for the same practice. Do not route opportunity evaluation through it. Do not treat a progress log as a Witness Chain.

## Publish posture

Fine as a private skill snapshot under All Rights Reserved. Public drop would still need a licence decision and a recorded T1-T12 run if any behavioural claim is made.
