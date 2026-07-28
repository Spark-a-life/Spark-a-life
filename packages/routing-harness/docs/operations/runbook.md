# Runbook

## Scaffold run (no credentials, no cost)

```bash
node --test            # 10 tests
node src/cli.mjs demo  # mock bench, scaffold route, verify
```

Expected: three mock candidates benchmarked, a `SCAFFOLD` routing decision with guard `certify_from_mock_evidence`, the build lane reported as `DELEGATED`, three config advisories about unverified pricing, and a valid witness chain. Nothing is written to `var/routing-matrix.json`. That is the correct outcome, not a failure.

## Live certification run

**Preconditions**

- [ ] `model_id` set for every candidate (placeholders begin `VERIFY-` and are deliberately invalid)
- [ ] `price_per_mtok_in` and `price_per_mtok_out` set from each provider's current price list
- [ ] Reference dataset extended to 20 expert-validated payloads
- [ ] `trials_per_payload` x payload count is at least 30 per candidate
- [ ] API keys exported

**Sequence**

```bash
node src/cli.mjs verify              # expect: config clean
node src/cli.mjs bench extraction    # repeated trials, live providers
node src/cli.mjs route extraction    # decision + witness record
node src/cli.mjs witness             # confirm the chain
```

A `CERTIFIED` decision writes `var/routing-matrix.json`. Anything else does not.

## Reading the outcome

| Decision | Meaning | Action |
| --- | --- | --- |
| `certified` | Candidate met compliance, trial count and metric requirements on live evidence | Route is live. Downstream skills may consume it. |
| `scaffold` | Pipeline ran, but a guard blocked certification | Read `guards`. Usually mock mode or unverified pricing. |
| `escalate` | No candidate met the compliance threshold | Do not route. Investigate schema, prompt or provider status, then re-run. |
| `delegated` | Task class is adjudicated elsewhere | Hand to the Build Lifecycle Orchestrator. |

## Re-certification cadence

Re-run `bench` and `route` when any of the following change: provider pricing, a candidate model version, the reference dataset, or the extraction schema. Each re-run appends to the witness chain, so the history of why a route changed is preserved rather than overwritten.

## Failure modes

**All candidates escalate.** Usually a schema or prompt problem rather than a model problem. Inspect `var/trials-<class>.json` for the recorded `errorMessage` values before concluding a model is unfit.

**Transport errors dominate.** Check credentials and `request_timeout_ms`. Transport errors count against compliance rate by design: a model that times out is not routable, whatever its accuracy would have been.

**Cost metric unavailable.** Pricing is `null` somewhere. The harness falls back to semantic accuracy then latency and refuses certification. Set the prices.

**Witness chain reports INVALID.** The chain has been edited outside the harness. Do not repair it in place. Preserve the file, investigate, and start a new chain deliberately.
