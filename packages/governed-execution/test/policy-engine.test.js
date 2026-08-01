import test from 'node:test';
import assert from 'node:assert/strict';
import { PolicyEngine, evaluateCondition } from '../src/core/policy-engine.js';
import { readJson } from '../src/util/fs.js';

const policies = await readJson(new URL('../config/policies.json', import.meta.url));

const engine = new PolicyEngine(policies);

function transfer(amount) {
  return {
    capabilityId: 'payments.transfer',
    parameters: { amount, currency: 'SGD' }
  };
}

test('policy precedence blocks transfers above the configured ceiling', () => {
  const decision = engine.evaluate(transfer(75000));
  assert.equal(decision.effect, 'DENY');
  assert.equal(decision.ruleId, 'deny-large-demo-transfer');
});

test('consequential transfer requires independent approval', () => {
  const decision = engine.evaluate(transfer(2500));
  assert.equal(decision.effect, 'REQUIRE_APPROVAL');
  assert.equal(decision.requiredApproverRole, 'finance_approver');
});

test('low-value transfer is allowed', () => {
  assert.equal(engine.evaluate(transfer(250)).effect, 'ALLOW');
});

test('condition evaluator supports numeric and membership operators', () => {
  const source = { amount: 10, roles: ['operator'] };
  assert.equal(evaluateCondition(source, { path: 'amount', operator: 'gte', value: 10 }), true);
  assert.equal(evaluateCondition(source, { path: 'roles', operator: 'contains', value: 'operator' }), true);
});
