# Claimed layout versus disk

Source file: uploaded `vfx_ai_pipeline_integration_manual_8488.md`  
sha256: `816022081890a347a5018cc36c2e77cf3c0e7a0af1e547732fd08d1a8521a90c`  
This pack does not copy that file.

Heading form in the manual is `### \`path\``. Those paths were searched on the extract root `/tmp/portfolio-review`. None existed as files.

The fenced `workflows/workflow_ic_lora_api.json` block parses as JSON. Parsing a citation is not the same as a file on disk.

## Graph defects visible in the fenced JSON

- Node `22` `DepthAnythingPreprocessor` output is wired to `KSamplerAdvanced.latent_image`.
- Node `20` `LoadVideo` `frame_load_cap` 33; node `18` pads to `16:9`; training YAML bucket is `960x544x33`, which is not 16:9.
- Checkpoint name `wan_2_1_14b_bf16.safetensors` is loaded via `CheckpointLoaderSimple`.

## Checklist in section 7

Every production audit box is unchecked. That is the only honest line in the deployment story, and it is undercut by the title.
