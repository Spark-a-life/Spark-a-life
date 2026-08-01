import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { ApprovalService } from '../src/core/approval-service.js';

const request = {
  requestId: 'request_transfer_test',
  actor: { id: 'finance.morgan', roles: ['finance_operator'] },
  capabilityId: 'payments.transfer',
  operation: 'submit',
  targetBaseUrl: 'http://127.0.0.1:8899',
  parameters: { amount: 2500, currency: 'SGD', beneficiary: 'Vendor', purpose: 'Test' },
  idempotencyKey: 'idem_transfer_test'
};

test('approval is bound to the exact action and is single use', async () => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'approval-test-'));
  const service = new ApprovalService({
    key: 'a'.repeat(48),
    storePath: path.join(directory, 'nonces.json')
  });
  const token = await service.issue({
    request,
    approver: { id: 'approver.riley', roles: ['finance_approver'] },
    requiredRole: 'finance_approver',
    ttlSeconds: 60
  });
  const payload = await service.validateAndConsume({
    token,
    request,
    requiredRole: 'finance_approver'
  });
  assert.equal(payload.requestId, request.requestId);
  await assert.rejects(
    service.validateAndConsume({ token, request, requiredRole: 'finance_approver' }),
    /already been consumed/
  );
  await fs.rm(directory, { recursive: true, force: true });
});

test('approval cannot be reused after action parameters change', async () => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'approval-test-'));
  const service = new ApprovalService({ key: 'b'.repeat(48), storePath: path.join(directory, 'nonces.json') });
  const token = await service.issue({
    request,
    approver: { id: 'approver.riley', roles: ['finance_approver'] },
    requiredRole: 'finance_approver'
  });
  await assert.rejects(
    service.validateAndConsume({
      token,
      request: { ...request, parameters: { ...request.parameters, amount: 3000 } },
      requiredRole: 'finance_approver'
    }),
    /not bound to this exact action/
  );
  await fs.rm(directory, { recursive: true, force: true });
});

test('self-approval is prohibited', async () => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'approval-test-'));
  const service = new ApprovalService({ key: 'c'.repeat(48), storePath: path.join(directory, 'nonces.json') });
  await assert.rejects(
    service.issue({
      request,
      approver: { id: request.actor.id, roles: ['finance_approver'] },
      requiredRole: 'finance_approver'
    }),
    /cannot approve their own/
  );
  await fs.rm(directory, { recursive: true, force: true });
});
