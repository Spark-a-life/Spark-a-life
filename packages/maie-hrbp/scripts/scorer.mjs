/**
 * Deterministic HRBP demand scorer.
 *
 * Implements config/demand-rubric.json. Deliberately deterministic: the
 * scoring arithmetic is not a model task. A model's role in this capability is
 * extracting structured signals from unit briefs, which is what the GAIE
 * routing harness certifies. Scoring itself must be reproducible and
 * inspectable, so it lives here.
 */

const PROHIBITED_FIELDS = [
  'employee_id',
  'employee_name',
  'case_narrative',
  'performance_rating',
  'medical_or_leave_reason',
  'protected_characteristics'
];

export class GuardViolation extends Error {
  constructor(message, details) {
    super(message);
    this.name = 'GuardViolation';
    this.details = details;
  }
}

/** Reject individual-level or prohibited data before any scoring occurs. */
export function assertIngestable(unit, rubricMinCellSize = 20) {
  const found = PROHIBITED_FIELDS.filter((f) => f in unit);
  if (found.length) {
    throw new GuardViolation('Prohibited individual-level fields present in unit record', { fields: found });
  }
  if (typeof unit.headcount !== 'number' || unit.headcount < rubricMinCellSize) {
    throw new GuardViolation('Unit below minimum cell size; reported as insufficient rather than scored', {
      headcount: unit.headcount ?? null,
      minimum_cell_size: rubricMinCellSize
    });
  }
  return true;
}

function clamp(v, lo, hi) {
  return Math.min(hi, Math.max(lo, v));
}

function populationModifier(headcount, medianUnitSize, range) {
  if (!headcount || !medianUnitSize) return 0;
  const ratio = Math.log(headcount / medianUnitSize) / Math.log(4);
  return Number(clamp(ratio * 0.5, range[0], range[1]).toFixed(3));
}

function confidenceFor(unit, rubric) {
  const present = rubric.dimensions.filter((d) => typeof unit.scores?.[d.id] === 'number').length;
  const completeness = present / rubric.dimensions.length;
  const quarters = unit.evidence_age_quarters ?? 0;
  const freshness = quarters <= 1 ? 1.0 : quarters <= 2 ? 0.85 : 0.6;
  return Number(clamp(completeness * freshness, 0.2, 0.95).toFixed(3));
}

function bandFor(index, rubric) {
  return rubric.bands.find((b) => index >= b.min && index <= b.max) || rubric.bands[rubric.bands.length - 1];
}

function alternativeFor(index, band, rubric) {
  const distances = rubric.bands
    .filter((b) => b.id !== band.id)
    .map((b) => ({ band: b, d: Math.min(Math.abs(index - b.min), Math.abs(index - b.max)) }))
    .sort((a, b) => a.d - b.d);
  return distances[0]?.band ?? null;
}

/**
 * Score one unit.
 * @returns recommendation, alternative, rationale, risk, confidence, drivers
 */
export function scoreUnit(unit, rubric) {
  assertIngestable(unit, rubric.dimensions ? 20 : 20);

  const contributions = rubric.dimensions.map((d) => {
    const raw = unit.scores?.[d.id];
    const value = typeof raw === 'number' ? clamp(raw, 0, 10) : 0;
    return {
      dimension: d.id,
      name: d.name,
      value,
      weight: d.weight,
      contribution: Number((value * d.weight).toFixed(4)),
      evidence_present: typeof raw === 'number'
    };
  });

  const weighted = contributions.reduce((sum, c) => sum + c.contribution, 0);
  const modifier = populationModifier(
    unit.headcount,
    unit.median_unit_size,
    rubric.population_modifier.range
  );
  const demandIndex = Number(clamp(weighted + modifier, 0, 10).toFixed(2));

  const band = bandFor(demandIndex, rubric);
  const alternative = alternativeFor(demandIndex, band, rubric);
  const confidence = confidenceFor(unit, rubric);

  const drivers = [...contributions]
    .filter((c) => c.evidence_present)
    .sort((a, b) => b.contribution - a.contribution)
    .slice(0, 3)
    .map((c) => `${c.name} (${c.value}/10)`);

  const cautions = [];
  const operationalShare = unit.operational_share;
  if (typeof operationalShare === 'number' && operationalShare > rubric.leakage_check.caution_threshold) {
    cautions.push(rubric.leakage_check.caution_text);
  }
  const missing = contributions.filter((c) => !c.evidence_present).map((c) => c.name);
  if (missing.length) {
    cautions.push(`Evidence missing for: ${missing.join(', ')}. Absent dimensions scored zero, which biases the index downward.`);
  }

  const risk = confidence < 0.5 || cautions.length > 1
    ? 'high'
    : cautions.length === 1 ? 'medium' : 'low';

  return {
    unit_name: unit.unit_name,
    headcount: unit.headcount,
    demand_index: demandIndex,
    weighted_subtotal: Number(weighted.toFixed(3)),
    population_modifier: modifier,
    coverage_recommendation: band.recommendation,
    alternative: alternative ? alternative.recommendation : null,
    drivers,
    rationale: buildRationale(unit, demandIndex, band, drivers, modifier),
    cautions,
    risk,
    confidence,
    contributions,
    rubric_version: rubric.rubric_version,
    rubric_status: rubric.status
  };
}

function buildRationale(unit, index, band, drivers, modifier) {
  const parts = [
    `Demand index ${index} places ${unit.unit_name} in the ${band.recommendation} band.`,
    band.description
  ];
  if (drivers.length) parts.push(`Principal drivers: ${drivers.join(', ')}.`);
  parts.push(`Headcount of ${unit.headcount} contributed a bounded modifier of ${modifier >= 0 ? '+' : ''}${modifier}, by design a secondary influence rather than the basis of the recommendation.`);
  return parts.join(' ');
}

/** Score a portfolio and surface cross-unit distribution. */
export function scorePortfolio(units, rubric) {
  const scored = [];
  const excluded = [];
  for (const unit of units) {
    try {
      scored.push(scoreUnit(unit, rubric));
    } catch (err) {
      if (err instanceof GuardViolation) {
        excluded.push({ unit_name: unit.unit_name ?? 'unnamed', reason: err.message, details: err.details });
      } else throw err;
    }
  }
  const counts = scored.reduce((acc, s) => {
    acc[s.coverage_recommendation] = (acc[s.coverage_recommendation] || 0) + 1;
    return acc;
  }, {});
  return {
    scored,
    excluded,
    distribution: counts,
    units_scored: scored.length,
    units_excluded: excluded.length,
    portfolio_caution: scored.some((s) => s.cautions.length)
      ? 'One or more units carry cautions. Read unit-level cautions before treating this distribution as a sizing basis.'
      : null
  };
}
