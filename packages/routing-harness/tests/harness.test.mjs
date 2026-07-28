import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import { validate, isStrictJson, countLeafNodes } from '../src/validate.mjs';
import { WitnessChain } from '../src/witness.mjs';
import { aggregate } from '../src/metrics.mjs';
import { decideRoute } from '../src/route.mjs';

const schema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    score: { type: 'number' },
    tier: { type: 'string', enum: ['low', 'high'] },
    tags: { type: 'array', items: { type: 'string' } }
  },
  required: ['name', 'score']
};

test('validator accepts conforming objects and rejects violations', () => {
  assert.equal(validate(schema, { name: 'x', score: 4.2, tier: 'low', tags: ['a'] }).valid, true);
  assert.equal(validate(schema, { name: 'x' }).valid, false);
  assert.equal(validate(schema, { name: 'x', score: 'high' }).valid, false);
  assert.equal(validate(schema, { name: 'x', score: 1, tier: 'mid' }).valid, false);
  assert.equal(validate(schema, { name: 'x', score: 1, tags: ['a', 2] }).valid, false);
});

test('strict JSON test rejects fences and preambles', () => {
  assert.equal(isStrictJson('{"a":1}'), true);
  assert.equal(isStrictJson('```json\n{"a":1}\n```'), false);
  assert.equal(isStrictJson('Here is the JSON: {"a":1}'), false);
});

test('leaf node counting', () => {
  assert.equal(countLeafNodes({ a: 1, b: { c: 2, d: [3, 4] } }), 4);
});

test('witness chain appends, verifies, and detects tampering', () => {
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'wc-')), 'chain.jsonl');
  const chain = new WitnessChain(file);
  chain.append('test', 'routing.update', { primary: 'a', certified: false });
  chain.append('test', 'routing.update', { primary: 'b', certified: true });
  assert.equal(chain.verify().valid, true);

  const lines = fs.readFileSync(file, 'utf8').trim().split('\n');
  const tampered = JSON.parse(lines[0]);
  tampered.payload.primary = 'evil';
  fs.writeFileSync(file, [JSON.stringify(tampered), lines[1]].join('\n') + '\n');
  assert.equal(chain.verify().valid, false);
});

function fakeTrials(n, { compliant = n, certifiable = true, tokensOut = 40, nodes = 8 } = {}) {
  return Array.from({ length: n }, (_, i) => ({
    schemaValid: i < compliant,
    strictJsonValid: i < compliant,
    transportError: false,
    durationMs: 200 + i,
    semanticAccuracy: i < compliant ? 1 : null,
    nodeCount: i < compliant ? nodes : 0,
    tokensOut: i < compliant ? tokensOut : 0,
    tokensIn: 120,
    certifiable
  }));
}

test('aggregate computes compliance rate and cost per validated node', () => {
  const e = aggregate('m', { price_per_mtok_out: 10 }, fakeTrials(50, { compliant: 49 }));
  assert.equal(e.complianceRate, 0.98);
  assert.ok(e.costPerValidatedNode > 0);
  const unpriced = aggregate('m', { price_per_mtok_out: null }, fakeTrials(10));
  assert.equal(unpriced.costPerValidatedNode, null);
});

const baseConfig = {
  execution: { compliance_threshold: 0.98, latency_tiebreak_band: 0.1 },
  governance: { minimum_trials_for_certification: 30 },
  task_classes: {
    extraction: { primary_metric: 'cost_per_validated_node' },
    build: { status: 'delegated', note: 'delegated to Build Lifecycle Orchestrator' }
  }
};

test('router refuses to certify from mock evidence', () => {
  const evidence = [aggregate('mock-fast', { price_per_mtok_out: 4 }, fakeTrials(50, { certifiable: false }))];
  const d = decideRoute({ config: baseConfig, taskClass: 'extraction', evidence, scaffold: false });
  assert.equal(d.certified, false);
  assert.ok(d.denials.includes('certify_from_mock_evidence'));
});

test('router refuses to certify below minimum trials', () => {
  const evidence = [aggregate('m', { price_per_mtok_out: 4 }, fakeTrials(10))];
  const d = decideRoute({ config: baseConfig, taskClass: 'extraction', evidence, scaffold: false });
  assert.equal(d.certified, false);
  assert.ok(d.denials.includes('certify_below_minimum_trials'));
});

test('router certifies live evidence above thresholds and prefers lower cost', () => {
  const cheap = aggregate('cheap', { price_per_mtok_out: 2 }, fakeTrials(50));
  const dear = aggregate('dear', { price_per_mtok_out: 20 }, fakeTrials(50));
  const d = decideRoute({ config: baseConfig, taskClass: 'extraction', evidence: [dear, cheap], scaffold: false });
  assert.equal(d.certified, true);
  assert.equal(d.primary, 'cheap');
  assert.equal(d.fallback, 'dear');
});

test('router escalates when no candidate meets the compliance threshold', () => {
  const evidence = [aggregate('m', { price_per_mtok_out: 4 }, fakeTrials(50, { compliant: 40 }))];
  const d = decideRoute({ config: baseConfig, taskClass: 'extraction', evidence, scaffold: false });
  assert.equal(d.decision, 'escalate');
  assert.equal(d.primary, null);
});

test('build lane is delegated, never routed by this harness', () => {
  const d = decideRoute({ config: baseConfig, taskClass: 'build', evidence: [], scaffold: false });
  assert.equal(d.decision, 'delegated');
  assert.equal(d.certified, false);
});
