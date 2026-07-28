/**
 * Aggregates trial records into per-model evidence.
 * Replaces v1.0 TEI with cost per validated node:
 *   - output tokens only (input tokens mostly measure your own prompt)
 *   - weighted by per-provider pricing (tokens are not fungible across vendors)
 *   - denominated in schema-validated leaf nodes from compliant trials only
 * If pricing is null, the cost metric is reported as unavailable rather than
 * silently computed from fiction.
 */

function percentile(sorted, p) {
  if (sorted.length === 0) return null;
  const idx = Math.min(sorted.length - 1, Math.ceil((p / 100) * sorted.length) - 1);
  return sorted[Math.max(0, idx)];
}

export function aggregate(modelAlias, modelConfig, trials) {
  const total = trials.length;
  const compliant = trials.filter((t) => t.schemaValid && t.strictJsonValid && !t.transportError);
  const errored = trials.filter((t) => t.transportError);

  const latencies = compliant.map((t) => t.durationMs).sort((a, b) => a - b);
  const accuracyValues = compliant
    .map((t) => t.semanticAccuracy)
    .filter((v) => v !== null && v !== undefined);

  const validatedNodes = compliant.reduce((n, t) => n + t.nodeCount, 0);
  const outTokens = compliant.reduce((n, t) => n + t.tokensOut, 0);
  const inTokens = compliant.reduce((n, t) => n + t.tokensIn, 0);

  const priceOut = modelConfig.price_per_mtok_out;
  let costPerValidatedNode = null;
  let costBasis = 'unavailable: pricing not set in config';
  if (priceOut !== null && priceOut !== undefined && validatedNodes > 0) {
    costPerValidatedNode = Number(((outTokens * priceOut) / 1e6 / validatedNodes).toPrecision(4));
    costBasis = 'output tokens x configured price / validated nodes';
  }

  return {
    modelAlias,
    trials: total,
    compliantTrials: compliant.length,
    transportErrors: errored.length,
    complianceRate: total > 0 ? Number((compliant.length / total).toFixed(4)) : 0,
    semanticAccuracy: accuracyValues.length
      ? Number((accuracyValues.reduce((a, b) => a + b, 0) / accuracyValues.length).toFixed(4))
      : null,
    latencyP50: percentile(latencies, 50),
    latencyP95: percentile(latencies, 95),
    tokensInTotal: inTokens,
    tokensOutTotal: outTokens,
    validatedNodes,
    costPerValidatedNode,
    costBasis,
    certifiable: trials.length > 0 && trials.every((t) => t.certifiable)
  };
}

/** Semantic accuracy: share of expert-expected fields the output matched. */
export function semanticAccuracy(expected, parsed, deepEqual) {
  if (!expected || !parsed) return null;
  const keys = Object.keys(expected);
  if (keys.length === 0) return null;
  const matched = keys.filter((k) => deepEqual(expected[k], parsed[k])).length;
  return matched / keys.length;
}

export function toCsv(records) {
  const headers = [
    'modelAlias', 'trials', 'compliantTrials', 'transportErrors', 'complianceRate',
    'semanticAccuracy', 'latencyP50', 'latencyP95', 'tokensInTotal', 'tokensOutTotal',
    'validatedNodes', 'costPerValidatedNode', 'certifiable'
  ];
  const rows = records.map((r) => headers.map((h) => r[h] ?? '').join(','));
  return headers.join(',') + '\n' + rows.join('\n') + '\n';
}
