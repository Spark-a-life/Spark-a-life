# STATUS: Claude sensemaking meta-prompt

**Primary lens:** evaluator / red-team.  
**Vendored:** yes, original bytes as `source.md`  
**sha256:** `a2dc1991a82eef9880c15a11e0f8488a010fabd71ad13e5e927f147048855dfe`  
**Size:** 3096 bytes, 31 lines.

## What it actually is

A single-file instruction to an assistant: read `vfx_ai_pipeline_integration_manual.md` and produce an architectural audit (spatial/temporal bounds, colour, Python versus Rust, Kubernetes I/O, QC, fallback, 30-60-90 day plan).

It is not an engine, not an ingestion system, and not evidence that the target manual is production-grade.

## Completeness versus own claims

It names one target file. That file was supplied in this review. It names `k8s-deployment.yaml` as if it were a sibling file; in the upload set it exists only as a section inside the manual.

It asks for edge cases (anamorphic, vertical, NFS bottlenecks, deadlock, SSIM/MSE/optical flow) that the target manual does not implement. That is a fair red-team brief. It is not fair as a preface that calls the target "complete, production-grade".

## Quality

Useful as a review agenda. Damaging as a framing document, because it copies the target's overclaim into the evaluator's starting conditions:

- "complete, production-grade integration manual"
- "zero-liability, highly deterministic VFX AI pipeline"

Those phrases are Declared by Interested Party (the prompt authoring itself) and Contradicted by the target's placeholder QC and missing files.

A 30-60-90 day "shot-bright studio production" matrix would be theatre until claimed paths exist on disk.

## Data

No secrets, no PII, no client shots. No licence.

## Implementability tomorrow

Yes, as a prompt: paste it with the manual into a capable model. The output will only be as honest as the evaluator's willingness to reject the production-grade premise. This evaluation pack is the preferred replacement for that prompt until it is rewritten.

## Fit to AIOS / Spark-a-life

Same genre as an AIOS red-team pass, aimed at a different artefact. Not an AIOS module. Complementary only as a reminder that ingestion prompts must not pre-certify their inputs.

## Publish posture

Private prompt. Rewrite the opening claims before reuse. Do not publish as an "engine".
