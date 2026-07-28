import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { CapabilityRegistry } from '../src/core/capability-registry.js';
import { PolicyEngine } from '../src/core/policy-engine.js';
import { ApprovalService } from '../src/core/approval-service.js';
import { WitnessChain } from '../src/core/witness-chain.js';
import { GovernedExecutionEngine } from '../src/core/engine.js';
import { createRedactor } from '../src/security/redaction.js';
import { readJson } from '../src/util/fs.js';

const capabilities = await readJson(new URL('../config/capabilities.json', import.meta.url));
const policies = await readJson(new URL('../config/policies.json', import.meta.url));
process.env.TARGET_BASE_URL = 'http://127.0.0.1:8899';
process.env.BROWSER_DEMO_ROOT = '/tmp';
process.env.BROWSER_DEMO_FILE = '/tmp/demo.html';

async function createFixture() {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'engine-test-'));
  const witness = new WitnessChain({
    filePath: path.join(directory, 'witness.jsonl'),
    key: 'w'.repeat(48),
    redact: createRedactor()
  });
  const approval = new ApprovalService({
    storePath: path.join(directory, 'approvals.json'),
    key: 'a'.repeat(48)
  });
  const adapter = {
    async execute({ request }) {
      if (request.capabilityId === 'notes.create') {
        return { status: 201, body: { id: 'note_1', title: request.parameters.title } };
      }
      return { status: 201, body: { transactionId: 'txn_1', status: 'ACCEPTED' } };
    }
  };
  const engine = new GovernedExecutionEngine({
    capabilityRegistry: new CapabilityRegistry(capabilities),
    policyEngine: new PolicyEngine(policies),
    approvalService: approval,
    witnessChain: witness,
    adapters: { get: () => adapter },
    runtimeConfig: { maxRetries: 1 }
  });
  return { directory, witness, approval, engine };
}

test('engine verifies a low-consequence action', async () => {
  const fixture = await createFixture();
  const result = await fixture.engine.execute({
    requestId: 'request_note_test',
    actor: { id: 'operator.alex', roles: ['operator'] },
    capabilityId: 'notes.create',
    operation: 'create',
    targetBaseUrl: 'http://127.0.0.1:8899',
    parameters: { title: 'Verified', body: 'Test' },
    idempotencyKey: 'idem_note_test'
  });
  assert.equal(result.disposition, 'SUCCEEDED');
  assert.equal(result.verification.verified, true);
  assert.equal((await fixture.witness.verify()).valid, true);
  await fs.rm(fixture.directory, { recursive: true, force: true });
});

test('engine holds consequential action until bound approval is supplied', async () => {
  const fixture = await createFixture();
  const request = {
    requestId: 'request_transfer_test',
    actor: { id: 'finance.morgan', roles: ['finance_operator'] },
    capabilityId: 'payments.transfer',
    operation: 'submit',
    targetBaseUrl: 'http://127.0.0.1:8899',
    parameters: { amount: 2500, currency: 'SGD', beneficiary: 'Vendor', purpose: 'Test' },
    idempotencyKey: 'idem_transfer_test'
  };
  const pending = await fixture.engine.execute(request);
  assert.equal(pending.disposition, 'AWAITING_APPROVAL');
  const token = await fixture.approval.issue({
    request,
    approver: { id: 'approver.riley', roles: ['finance_approver'] },
    requiredRole: 'finance_approver'
  });
  const completed = await fixture.engine.execute({ ...request, approvalToken: token });
  assert.equal(completed.disposition, 'SUCCEEDED');
  await fs.rm(fixture.directory, { recursive: true, force: true });
});
