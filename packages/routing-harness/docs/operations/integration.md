# Ecosystem Integration

## Upstream

**APE Intelligence OS** supplies the constitutional principles, Captain's Gate policy shape and Witness Chain pattern this harness follows. The harness is registered as a GAIE capability and its witness records use the same hash-linked structure, so chains can be reconciled without translation.

**Reference Dataset Builder** discipline governs `payloads/extraction-reference.json`: expert-validated expected values, 10 to 20 examples, quality over volume. Ship at 10 for scaffolding. Extend to 20 before production certification.

## Downstream

**Multi-Model Routing Orchestrator** consumes `var/routing-matrix.json`. The harness answers the question that skill's Layer 2 Model Tier Registry currently answers by assertion: which model actually belongs in which tier, on evidence. Mapping:

| Harness task class | Routing Orchestrator classification |
| --- | --- |
| `extraction` | Tier 2, synthesis and generation, structured output |
| `interactive` | Tier 1 or 2 depending on context dependency, latency-primary |
| `build` | Tier 2 build lane, delegated to Build Lifecycle Orchestrator |

A certified route translates into a Routing Card as follows:

```yaml
routing_card:
  task_id: "TASK-{session}-{n}"
  classification:
    cognitive_load_tier: 2
    context_dependency: MED
    output_sensitivity: GOVERNED
  assigned_model: "{routing-matrix.extraction.primary}"
  evidence_ref: "var/evidence-extraction.json"
  witness_index: "{routing-matrix.extraction.witness_index}"
```

The `evidence_ref` and `witness_index` fields are the addition this harness makes. A Routing Card that carries them can be audited back to the trials that justified the assignment, which is what AI Verify traceability requires and what an assertion-based registry cannot provide.

**Build Lifecycle Orchestrator** owns build-lane adjudication. This harness records `decision: delegated` with the candidate set, then stands aside.

**MAIE capabilities** (for example the HRBP demand scorer) consume certified routes but never certify their own. A capability that selected its own model would breach `capability_self_certification`.

## Adding a provider

1. Add an entry to `providers` in `config/harness.config.json` with `adapter`, `base_url`, `api_key_env`, `certifiable`.
2. If the API shape is OpenAI-compatible, reuse `adapter: "openai"`. Otherwise add one function to `src/providers.mjs` returning `{ rawText, tokensIn, tokensOut, certifiable }`.
3. Add the model to `models` with its `model_id`, structured output mode and verified pricing.
4. Add the alias to the relevant `task_classes[].candidates`.

No other file changes. That is the portability principle working as intended.

## Adding a task class

Define the class in `task_classes` with a candidate list, a `primary_metric` (`cost_per_validated_node`, `latency_p50`, or `external_test_pass_rate` for delegated classes) and a payload set. Metrics beyond these three require a branch in `decideRoute`.
