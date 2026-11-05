# STATUS: VFX AI pipeline integration manual

**Primary lens:** red-team, with feasibility and release-readiness.  
**Vendored wholesale:** no  
**Reason:** overclaim plus incomplete layout. The document presents itself as a production integration manual. On disk it is one markdown file. Claimed runtime paths do not exist as files.

Source sha256 (uploaded file):

```text
816022081890a347a5018cc36c2e77cf3c0e7a0af1e547732fd08d1a8521a90c
```

Original size: 18608 bytes, 575 lines. See `CLAIMED_VS_DISK.md`.

## What it actually is

A design sketch. Axioms plus inlined samples for a ComfyUI-oriented clean-plate workflow, a Python WebSocket worker, a Rust orchestrator, a Dockerfile, a partial Kubernetes manifest, and a Nuke panel.

It is not a repository, not a cluster, not a deterministic QC system, and not zero-liability.

## Completeness versus own claims

| Claimed path | On disk | Maturity |
| --- | --- | --- |
| `configs/ic_lora_vfx_production.yaml` | No | Declared |
| `workflows/workflow_ic_lora_api.json` | No (JSON parses as a fenced block) | Declared |
| `scripts/comfy_agentic_worker.py` | No | Declared |
| `orchestrator/Cargo.toml` | No | Declared |
| `orchestrator/src/main.rs` | No | Declared |
| `deploy/Dockerfile` | No | Declared |
| `deploy/k8s-deployment.yaml` | No | Declared |
| `nuke/comfy_nuke_integration.py` | No | Declared |
| ComfyUI server Service | Not in manifest | Missing even as a declaration |
| PVC `nfs-exr-storage-pvc` | Referenced, not defined | Missing |
| IC-LoRA weights / Wan 14B | Not included | Expected absence |

## Quality blockers (not nits)

1. `calculate_structural_divergence` is a placeholder that returns `0.021`. With threshold `0.03`, QC always passes. "Zero-liability QC" is therefore Contradicted by the supplied code.
2. Axiom 2 requires 16-bit half-float linear ACES. The Nuke Read uses `ACES - ACEScc` (log). CLIP prompt text "16-bit float linear" does not perform colour management.
3. `KSamplerAdvanced` takes `latent_image` from `DepthAnythingPreprocessor` (an image preprocessor). Type mismatch.
4. Rust `build_workflow` emits JSON that references nodes `22`, `35`, and `36` without defining them, and uses a different sampler node than the Python workflow.
5. Dockerfile installs `websocket-client` and `numpy` only. It does not install ComfyUI, models, or a VAE. ENTRYPOINT runs the worker, which expects an already running server.
6. Kubernetes Deployment points at `comfyui-service.vfx-pipeline.svc.cluster.local:8188` with no Service, no ComfyUI Deployment, and no PVC spec. Four GPU replicas would contend on a shared NFS path that is not defined here.
7. Nuke `dispatch_and_ingest` starts a thread and immediately builds a tree on the main thread without submitting a job or waiting for EXRs. `register_nuke_menu()` is commented out.
8. Custom nodes (`ICLoRALoader`, `SaveEXR`, `LoadVideo`, `ImagePadForAspectRatio`) are assumed without a node pack inventory.
9. Temporal rule `(F-1) mod 8 == 0` is encoded as 33 frames. Anamorphic and vertical plates are forced toward 16:9 padding. That can destroy spatial conditioning.
10. Seed mutation `+= 1337` is not a structural-alignment strategy.

## Data

No secrets, no PII, no client plates. `studio-registry.internal` is a fictional registry name. Input plate `input_plate_v01.mov` is a placeholder filename. No licence.

Copyright: sample code appears original to the manual; third-party models (Wan, Depth Anything, LTX) are named, not bundled.

## Implementability tomorrow

No. A competent engineer could start from the axioms, not from these samples as a deployable system. Running the inlined worker as written would exercise a stub QC path, not a studio pipeline.

## Fit to AIOS / Spark-a-life

Unrelated product domain. If ever implemented, cluster submission and Nuke ingestion of generated plates would be AIOS Red (production consequence) and currently Prohibited because QC, colour, and services are not real.

Do not place this manual beside AIOS as if it were an implemented Action surface.

## What would have to change before vendoring a tree

- Extract each fenced block to a real path whose hash is inventoried.
- Replace stub QC with a named metric computed from actual EXR pixels against a named reference.
- Make colourspace explicit and consistent (working space, display space, OCIO config).
- Fix graph types (image versus latent).
- Add the missing Kubernetes Service, ComfyUI server, and PVC, or delete the cluster claim.
- Add tests that can fail.
- Remove "zero-liability" and "production" from the title until a release gate exists.
- Add a licence.
