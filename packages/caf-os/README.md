# WiseGen CAF-OS v1.0

**Conversational AI Filmmaking Operating System**

A governance-first, voice-ready, model-agnostic production control plane for AI filmmaking. It turns human creative intent into structured production decisions, capability routing, render jobs, asset records, approvals and an append-only witness chain.

## What is executable

- TypeScript CLI for project creation, shot routing, render submission, approval and audit inspection
- Express API for orchestration and external clients
- MCP stdio server exposing governed production tools
- deterministic model router covering Kling-style, Seedance-style, LoRA, avatar and local/mock execution profiles
- local project, asset, character, shot, rights, approval and witness registries
- asynchronous mock provider for safe end-to-end testing without paid APIs
- generic HTTP provider contract for authorised vendor or internal endpoints
- Zod validation and Vitest coverage

## Deliberate boundary

Vendor API shapes change and may not be publicly stable. CAF-OS therefore does not invent proprietary Kling, Higgsfield or ElevenLabs endpoints. Production integrations use an explicit `HttpGenerationProvider` contract configured against an authorised endpoint you control or are licensed to call. The repository is fully executable in `mock` mode and ready for verified provider adapters.

## Start

```bash
npm install
npm run verify
npm run demo
npm run api
npm run mcp
```

API: `http://localhost:8787/health`

## Core commands

```bash
npm run init-project -- --id biopic-trailer --title "Biopic Trailer"
npm run route -- --project biopic-trailer --shot examples/shots/dialogue-closeup.json
npm run demo
```

## Intentionality-by-design lanes

1. **Intent lane**: purpose, audience, desired effect and non-negotiables
2. **Narrative lane**: story state, scene logic, paper edit and continuity
3. **Identity lane**: character, voice, costume and authorised likeness binding
4. **Production lane**: shot specifications, audio-first timing and model routing
5. **Execution lane**: asynchronous provider calls and asset registration
6. **Assurance lane**: technical QA, rights, accessibility and release checks
7. **Governance lane**: Captain's Gate approvals and Witness Chain provenance
8. **Learning lane**: reusable decisions, presets, failure patterns and routing evidence

See `docs/goal-and-journey.md` and `prompts/sensemaking-as-a-prompt.md`.
