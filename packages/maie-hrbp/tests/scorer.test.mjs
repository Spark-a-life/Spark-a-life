import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';
import { scoreUnit, scorePortfolio, assertIngestable, GuardViolation } from '../scripts/scorer.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const rubric = JSON.parse(fs.readFileSync(path.join(ROOT, 'config', 'demand-rubric.json'), 'utf8'));
const portfolio = JSON.parse(fs.readFileSync(path.join(ROOT, 'examples', 'sample-portfolio.json'), 'utf8'));

const unit = (over = {}) => ({
  unit_name: 'Test unit',
  headcount: 300,
  median_unit_size: 340,
  evidence_age_quarters: 1,
  operational_share: 0.3,
  scores: {
    change_load: 5, manager_capability_gap: 5, er_intensity: 5,
    structural_ambiguity: 5, workforce_volatility: 5, industrial_relations_load: 5
  },
  ...over
});

test('prohibited individual-level fields are rejected before scoring', () => {
  for (const field of ['employee_id', 'employee_name', 'case_narrative', 'performance_rating']) {
    assert.throws(() => assertIngestable(unit({ [field]: 'x' })), GuardViolation);
  }
});

test('units below minimum cell size are excluded, not scored', () => {
  assert.throws(() => assertIngestable(unit({ headcount: 14 })), GuardViolation);
  const result = scorePortfolio(portfolio.units, rubric);
  const legal = result.excluded.find((e) => e.unit_name === 'Corporate legal');
  assert.ok(legal, 'sub-threshold unit must appear in excluded');
  assert.equal(result.scored.some((s) => s.unit_name === 'Corporate legal'), false);
});

test('band assignment follows the demand index', () => {
  const high = scoreUnit(unit({ scores: { change_load: 9, manager_capability_gap: 9, er_intensity: 8, structural_ambiguity: 8, workforce_volatility: 7, industrial_relations_load: 7 } }), rubric);
  assert.equal(high.coverage_recommendation, 'dedicated');

  const low = scoreUnit(unit({ scores: { change_load: 1, manager_capability_gap: 1, er_intensity: 1, structural_ambiguity: 1, workforce_volatility: 2, industrial_relations_load: 1 } }), rubric);
  assert.equal(low.coverage_recommendation, 'shared-services');

  const mid = scoreUnit(unit(), rubric);
  assert.equal(mid.coverage_recommendation, 'pooled');
});

test('a small unit in crisis outranks a large stable unit', () => {
  const smallCrisis = scoreUnit(unit({
    unit_name: 'Small crisis', headcount: 120,
    scores: { change_load: 9, manager_capability_gap: 9, er_intensity: 8, structural_ambiguity: 8, workforce_volatility: 7, industrial_relations_load: 6 }
  }), rubric);
  const largeStable = scoreUnit(unit({
    unit_name: 'Large stable', headcount: 900,
    scores: { change_load: 2, manager_capability_gap: 2, er_intensity: 2, structural_ambiguity: 1, workforce_volatility: 2, industrial_relations_load: 3 }
  }), rubric);

  assert.ok(smallCrisis.demand_index > largeStable.demand_index,
    'demand, not headcount, must drive the index');
  assert.equal(smallCrisis.coverage_recommendation, 'dedicated');
  assert.equal(largeStable.coverage_recommendation, 'shared-services');
});

test('population modifier stays inside its bounds', () => {
  const tiny = scoreUnit(unit({ headcount: 25 }), rubric);
  const huge = scoreUnit(unit({ headcount: 9000 }), rubric);
  const [lo, hi] = rubric.population_modifier.range;
  assert.ok(tiny.population_modifier >= lo && tiny.population_modifier <= hi);
  assert.ok(huge.population_modifier >= lo && huge.population_modifier <= hi);
});

test('leakage caution fires above the operational share threshold', () => {
  const leaky = scoreUnit(unit({ operational_share: 0.68 }), rubric);
  assert.ok(leaky.cautions.some((c) => c.includes('tiering leakage')));
  const clean = scoreUnit(unit({ operational_share: 0.3 }), rubric);
  assert.equal(clean.cautions.some((c) => c.includes('tiering leakage')), false);
});

test('missing evidence lowers confidence and raises a caution', () => {
  const partial = scoreUnit(unit({ scores: { change_load: 8, manager_capability_gap: 7 } }), rubric);
  assert.ok(partial.confidence < 0.6);
  assert.ok(partial.cautions.some((c) => c.includes('Evidence missing')));
});

test('confidence is capped below certainty while the rubric is provisional', () => {
  const complete = scoreUnit(unit({ evidence_age_quarters: 0 }), rubric);
  assert.ok(complete.confidence <= 0.95);
  assert.equal(rubric.status, 'provisional');
});

test('stale evidence reduces confidence', () => {
  const fresh = scoreUnit(unit({ evidence_age_quarters: 1 }), rubric);
  const stale = scoreUnit(unit({ evidence_age_quarters: 4 }), rubric);
  assert.ok(stale.confidence < fresh.confidence);
});

test('every scored unit carries an alternative, rationale, risk and confidence', () => {
  const result = scorePortfolio(portfolio.units, rubric);
  for (const s of result.scored) {
    assert.ok(s.alternative, `${s.unit_name} missing alternative`);
    assert.ok(s.rationale.length > 0);
    assert.ok(['low', 'medium', 'high'].includes(s.risk));
    assert.ok(s.confidence > 0 && s.confidence <= 0.95);
    assert.equal(s.rubric_status, 'provisional');
  }
});

test('scoring is deterministic', () => {
  const a = scoreUnit(unit(), rubric);
  const b = scoreUnit(unit(), rubric);
  assert.deepEqual(a, b);
});
