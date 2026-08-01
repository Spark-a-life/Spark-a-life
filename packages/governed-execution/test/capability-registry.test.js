import test from 'node:test';
import assert from 'node:assert/strict';
import { CapabilityRegistry } from '../src/core/capability-registry.js';
import { readJson } from '../src/util/fs.js';

const capabilities = await readJson(new URL('../config/capabilities.json', import.meta.url));

process.env.TARGET_BASE_URL = 'http://127.0.0.1:8899';
process.env.BROWSER_DEMO_ROOT = '/tmp';
process.env.BROWSER_DEMO_FILE = '/tmp/demo.html';

const registry = new CapabilityRegistry(capabilities);

test('capability registry rejects unentitled roles', () => {
  assert.throws(() => registry.resolve({
    requestId: 'request_0001',
    actor: { id: 'user', roles: ['operator'] },
    capabilityId: 'payments.transfer',
    operation: 'submit',
    targetBaseUrl: 'http://127.0.0.1:8899',
    parameters: { amount: 10, currency: 'SGD', beneficiary: 'A', purpose: 'B' },
    idempotencyKey: 'idem_0001'
  }), /not entitled/);
});

test('capability registry rejects undeclared parameters', () => {
  assert.throws(() => registry.resolve({
    requestId: 'request_0002',
    actor: { id: 'operator', roles: ['operator'] },
    capabilityId: 'notes.create',
    operation: 'create',
    targetBaseUrl: 'http://127.0.0.1:8899',
    parameters: { title: 'A', body: 'B', adminOverride: true },
    idempotencyKey: 'idem_0002'
  }), /unauthorised fields/);
});


test('capability registry rejects parameters with the wrong data type', () => {
  assert.throws(() => registry.resolve({
    requestId: 'request_0003',
    actor: { id: 'finance', roles: ['finance_operator'] },
    capabilityId: 'payments.transfer',
    operation: 'submit',
    targetBaseUrl: 'http://127.0.0.1:8899',
    parameters: { amount: '2500', currency: 'SGD', beneficiary: 'A', purpose: 'B' },
    idempotencyKey: 'idem_0003'
  }), /must be a finite number/);
});
