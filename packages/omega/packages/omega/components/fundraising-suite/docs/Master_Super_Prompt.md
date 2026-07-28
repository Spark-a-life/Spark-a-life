# Master Super Prompt Usage

The repository includes a generator for two delivery routes.

## Route A: Local Zip Route

Use this when portability and reproducibility matter. The model generates a Python scaffolding script that writes the repository locally and creates a zip archive.

```bash
wg-fund prompt --project-name wisegen-mamt-fundraising-suite --route zip
```

## Route B: No-Zip Route

Use this when the environment requires direct text-to-workspace generation. The prompt instructs the model to emit architecture, dependencies, source files and runtime manual in chunks.

```bash
wg-fund prompt --project-name wisegen-mamt-fundraising-suite --route no-zip --chunk-size 5
```

The generated prompt includes a mandatory expert review checkpoint before final code output.
