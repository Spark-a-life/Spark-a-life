/**
 * Routing decision engine.
 * Consumes aggregated evidence, applies the decision matrix, and emits a
 * routing decision plus a Witness Chain record. Certification guards enforce
 * evidence-before-trust:
 *   - mock evidence can never certify (scaffold decisions are labelled so)
 *   - cost-primary routing without verified pricing falls back with a warning
 *   - below-minimum trial counts cannot certify
 * No one-strike disqualification: eligibility is a compliance RATE against a
 * threshold over repeated trials.
 */

function withinBand(a, b, band) {
  if (a === null || b === null) return false;
  const hi = Math.max(a, b);
  return hi > 0 ? Math.abs(a - b) / hi <= band : true;
}

export function decideRoute({ config, taskClass, evidence, scaffold }) {
  const tc = config.task_classes[taskClass];
  const gov = config.governance;
  const threshold = config.execution.compliance_threshold;
  const warnings = [];

  if (tc.status === 'delegated') {
    return {
      task_class: taskClass,
      decision: 'delegated',
      primary: null,
      fallback: null,
      rationale: tc.note,
      certified: false,
      warnings
    };
  }

  const eligible = evidence.filter((e) => e.complianceRate >= threshold && e.trials > 0);
  if (eligible.length === 0) {
    return {
      task_class: taskClass,
      decision: 'escalate',
      primary: null,
      fallback: null,
      rationale: `No candidate met the compliance threshold of ${threshold} over repeated trials. Escalate to operator; do not route.`,
      certified: false,
      warnings
    };
  }

  // Metric selection
  let metric = tc.primary_metric;
  const costAvailable = eligible.every((e) => e.costPerValidatedNode !== null);
  if (metric === 'cost_per_validated_node' && !costAvailable) {
    warnings.push('Pricing not verified in config: cost basis unavailable, routing on semantic accuracy then latency instead.');
    metric = 'semantic_then_latency';
  }

  let ranked;
  if (metric === 'cost_per_validated_node') {
    ranked = [...eligible].sort((a, b) => a.costPerValidatedNode - b.costPerValidatedNode);
    // Latency tiebreak inside the configured band
    if (ranked.length > 1 &&
        withinBand(ranked[0].costPerValidatedNode, ranked[1].costPerValidatedNode, config.execution.latency_tiebreak_band) &&
        ranked[1].latencyP50 !== null && ranked[0].latencyP50 !== null &&
        ranked[1].latencyP50 < ranked[0].latencyP50) {
      [ranked[0], ranked[1]] = [ranked[1], ranked[0]];
      warnings.push('Cost differential within tiebreak band: lower p50 latency promoted.');
    }
  } else if (metric === 'latency_p50') {
    ranked = [...eligible].sort((a, b) => (a.latencyP50 ?? Infinity) - (b.latencyP50 ?? Infinity));
  } else {
    ranked = [...eligible].sort((a, b) =>
      (b.semanticAccuracy ?? 0) - (a.semanticAccuracy ?? 0) ||
      (a.latencyP50 ?? Infinity) - (b.latencyP50 ?? Infinity));
  }

  const primary = ranked[0];
  const fallback = ranked[1] || evidence.filter((e) => e.modelAlias !== primary.modelAlias)
    .sort((a, b) => b.complianceRate - a.complianceRate)[0] || null;

  // Certification guards
  let certified = true;
  const denials = [];
  if (!primary.certifiable) {
    certified = false;
    denials.push('certify_from_mock_evidence');
  }
  if (primary.trials < gov.minimum_trials_for_certification) {
    certified = false;
    denials.push('certify_below_minimum_trials');
  }
  if (tc.primary_metric === 'cost_per_validated_node' && !costAvailable) {
    certified = false;
    denials.push('certify_without_pricing_for_cost_metric');
  }
  if (scaffold) certified = false;

  const confidence = Math.min(
    primary.complianceRate,
    primary.semanticAccuracy ?? 1,
    primary.trials >= gov.minimum_trials_for_certification ? 1 : 0.5
  );

  return {
    task_class: taskClass,
    decision: certified ? 'certified' : 'scaffold',
    primary: primary.modelAlias,
    fallback: fallback ? fallback.modelAlias : null,
    metric_used: metric,
    rationale: buildRationale(primary, fallback, metric, threshold),
    risk: certified ? 'low' : 'not-for-production',
    confidence: Number(confidence.toFixed(3)),
    certified,
    denials,
    warnings,
    evidence_summary: evidence
  };
}

function buildRationale(primary, fallback, metric, threshold) {
  const parts = [
    `${primary.modelAlias} passed the compliance threshold (${(primary.complianceRate * 100).toFixed(1)}% over ${primary.trials} trials, threshold ${threshold * 100}%).`
  ];
  if (metric === 'cost_per_validated_node') {
    parts.push(`Selected on lowest cost per validated node (${primary.costPerValidatedNode}).`);
  } else if (metric === 'latency_p50') {
    parts.push(`Selected on lowest p50 latency (${primary.latencyP50}ms).`);
  } else {
    parts.push(`Selected on semantic accuracy (${primary.semanticAccuracy}) then latency.`);
  }
  if (primary.semanticAccuracy !== null) {
    parts.push(`Semantic accuracy against the reference dataset: ${(primary.semanticAccuracy * 100).toFixed(1)}%.`);
  }
  if (fallback) parts.push(`Failover: ${fallback.modelAlias}.`);
  return parts.join(' ');
}

/** Persist a routing decision with a witness record. Returns the witness record. */
export function commitRoute({ chain, decision, evidenceRef }) {
  return chain.append('routing-harness', 'routing.update', {
    task_class: decision.task_class,
    decision: decision.decision,
    primary: decision.primary,
    fallback: decision.fallback,
    metric_used: decision.metric_used ?? null,
    rationale: decision.rationale,
    confidence: decision.confidence ?? null,
    certified: decision.certified,
    denials: decision.denials ?? [],
    warnings: decision.warnings ?? [],
    evidence_ref: evidenceRef
  });
}
