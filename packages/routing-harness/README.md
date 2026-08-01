# WiseGen Model Routing Harness v1.1

**Owner estate:** GAIE (capability evaluation, no direct production authority)
**Capability:** `capability.evaluate.routing`
**Design rule:** Evidence before trust. Mock evidence can exercise the pipeline. It can never decide a production route.

The harness benchmarks candidate models per task class, aggregates repeated-trial evidence, and produces witnessed routing decisions consumable by the Multi-Model Routing Orchestrator as Routing Card inputs.

## What changed from the v1.0 playbook

1. **Mock mode is quarantined, not disguised.** The v1.0 harness hardcoded both model responses and scripted one candidate to fail, then called the output a benchmark. v1.1 keeps a mock provider for end-to-end testing, but every mock result carries `certifiable: false` and the router's automatic denial `certify_from_mock_evidence` blocks it from the production matrix.

2. **Structured outputs are requested, not tested for.** Anthropic routes through forced tool use; OpenAI and xAI route through `json_schema` response format. Formatting compliance is a configuration matter. The benchmark now differentiates on what matters: semantic accuracy against an expert reference dataset, cost, and latency.

3. **TEI is replaced by cost per validated node.** Output tokens only (input tokens mostly measure your own prompt), weighted by per-provider pricing (tokens are not fungible across vendors), denominated in schema-validated nodes from compliant trials only. Pricing ships as `null`: the harness reports the cost metric as unavailable and blocks cost-primary certification until you set verified prices. It will not compute money from fiction.

4. **No one-strike disqualification.** Eligibility is a compliance rate (default 98 percent) over repeated trials (default 5 per payload across 10 reference payloads). Certification additionally requires a minimum of 30 trials per candidate. Extend the reference set to 20 payloads before production certification, per Reference Dataset Builder discipline.

5. **Route changes are witnessed.** Every routing decision, certified or scaffold, appends a hash-linked record to an append-only witness chain: primary, fallback, metric, rationale, confidence, denials, and the evidence file reference. Self-tuning routing stays auditable. Governance tier: low (no human approval for route flips, witness chain mandatory), consistent with the Captain's Gate policy.

6. **Codex enters through the task-class matrix, not as a third worker.** The router is keyed by task class. `extraction` and `interactive` compare Grok, Sonnet and the Codex-class model directly. `build` is declared but delegated: build-lane routing between Sonnet and Codex is scored on test-pass rate against a Task Specification Card by the Build Lifecycle Orchestrator, which this harness records but does not adjudicate.

7. **worker_threads removed.** Model calls are I/O-bound; a bounded promise pool provides the same concurrency without thread overhead or the `__filename` re-entry pattern.

## Requirements

Node.js 20 or newer. No npm dependencies.

## Run

```bash
node src/cli.mjs demo                      # mock bench + scaffold route + verify
node src/cli.mjs verify                    # config advisories + witness integrity
node --test                                # test suite (10 tests)

# Live certification run (after setting model ids, pricing, API keys):
export ANTHROPIC_API_KEY=... OPENAI_API_KEY=... XAI_API_KEY=...
node src/cli.mjs bench extraction
node src/cli.mjs route extraction
node src/cli.mjs witness
```

## Before any live certification run

- Set current `model_id` values in `config/harness.config.json` for the Codex and Grok entries (placeholders are deliberately invalid).
- Set `price_per_mtok_in` and `price_per_mtok_out` from each provider's current price list.
- Extend `payloads/extraction-reference.json` to 20 expert-validated payloads.
- Confirm `trials_per_payload` gives at least `minimum_trials_for_certification` (30) trials per candidate.
- Note on strict schema modes: OpenAI's `strict: true` requires `additionalProperties: false` and all properties required. The harness uses `strict: false` by default so arbitrary reference schemas work; tighten per schema when you certify.

## Outputs

- `var/evidence-<class>[-mock].json` and `.csv`: aggregated per-model evidence
- `var/trials-<class>[-mock].json`: raw trial records
- `var/routing-matrix.json`: certified routes only
- `var/witness/routing-witness.jsonl`: append-only decision chain

Start with the work. Keep the human accountable.

## Repository map

```
config/harness.config.json      candidates, thresholds, pricing, task classes, guards
payloads/extraction-reference.json  expert-validated reference dataset (10, extend to 20)
src/cli.mjs                     verify | bench | route | witness | demo
src/harness.mjs                 repeated-trial runner, bounded promise pool
src/providers.mjs               Anthropic / OpenAI-compatible / quarantined mock adapters
src/metrics.mjs                 compliance rate, semantic accuracy, cost per validated node
src/route.mjs                   decision matrix, certification guards, witness emission
src/validate.mjs                zero-dependency schema subset validator
tests/harness.test.mjs          10 tests incl. tamper detection and guard enforcement
docs/governance/posture.md      estate placement, constitutional alignment, denials
docs/operations/runbook.md      scaffold and live certification procedures
docs/operations/integration.md  Routing Card mapping and ecosystem wiring
```

## Documentation

- Governance posture: `docs/governance/posture.md`
- Operator runbook: `docs/operations/runbook.md`
- Ecosystem integration: `docs/operations/integration.md`
