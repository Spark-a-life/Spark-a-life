# Operating Handbook

## Standard cadence

1. Draft or select a mission brief under `examples/briefs`.
2. Validate the brief: `wcef validate <brief.yaml>`.
3. Compile the mission team: `wcef compile <brief.yaml>`.
4. Run the mission: `wcef run <brief.yaml> --output outputs/run.json`.
5. Inspect the result: `wcef inspect outputs/run.json`.
6. Apply Captain's Gate decision: approve, revise or block.
7. Archive witness events for audit.

## Production expectations

- Use manual adapters only when public APIs are unavailable or unsuitable.
- Never expose raw credentials to role agents.
- Treat all reference assets as governed inputs with ownership, consent and permitted-use metadata.
- Require human approval for client work, faces, brands, public profiles, financial services, healthcare, education, government and regulated material.
- Use evaluation scores as decision support, not as a substitute for accountable judgement.
