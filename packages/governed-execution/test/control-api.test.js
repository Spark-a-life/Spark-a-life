import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { startDemoTarget } from '../src/demo/target-server.js';
import { startControlServer } from '../src/server.js';

const API_KEY = 'demo-control-api-key-rotate-before-use';
process.env.RUNTIME_MODE = 'demo';
process.env.CONTROL_API_KEY = API_KEY;
process.env.WITNESS_HMAC_KEY = 'demo-witness-hmac-key-rotate-before-use-32bytes';
process.env.APPROVAL_HMAC_KEY = 'demo-approval-hmac-key-rotate-before-use-32bytes';

test('control API enforces authentication and completes approval workflow', async () => {
  const target = await startDemoTarget();
  process.env.TARGET_BASE_URL = target.baseUrl;
  process.env.BROWSER_DEMO_ROOT = path.resolve('fixtures');
  process.env.BROWSER_DEMO_FILE = path.resolve('fixtures/browser-demo.html');
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'control-api-test-'));
  const control = await startControlServer({
    host: '127.0.0.1',
    port: 0,
    runtimeOverrides: {
      witnessPath: path.join(directory, 'witness.jsonl'),
      approvalStorePath: path.join(directory, 'approvals.json'),
      stateStorePath: path.join(directory, 'state')
    }
  });
  const address = control.server.address();
  const baseUrl = `http://127.0.0.1:${address.port}`;
  try {
    const health = await fetch(`${baseUrl}/health`);
    assert.equal(health.status, 200);

    const unauthorised = await fetch(`${baseUrl}/v1/witness/verify`);
    assert.equal(unauthorised.status, 401);

    const noteRequest = {
      requestId: 'request_api_note',
      actor: { id: 'operator.alex', roles: ['operator'] },
      capabilityId: 'notes.create',
      operation: 'create',
      targetBaseUrl: target.baseUrl,
      parameters: { title: 'Control API', body: 'Verified' },
      idempotencyKey: 'idem_api_note'
    };
    const note = await post(`${baseUrl}/v1/execute`, noteRequest);
    assert.equal(note.response.status, 200);
    assert.equal(note.body.disposition, 'SUCCEEDED');
    const storedState = await fetch(`${baseUrl}/v1/requests/${noteRequest.requestId}`, {
      headers: { authorization: `Bearer ${API_KEY}` }
    });
    assert.equal(storedState.status, 200);
    assert.equal((await storedState.json()).state, 'SUCCEEDED');

    const transferRequest = {
      requestId: 'request_api_transfer',
      actor: { id: 'finance.morgan', roles: ['finance_operator'] },
      capabilityId: 'payments.transfer',
      operation: 'submit',
      targetBaseUrl: target.baseUrl,
      parameters: {
        amount: 2500,
        currency: 'SGD',
        beneficiary: 'Approved Demonstration Vendor',
        purpose: 'Control API test'
      },
      idempotencyKey: 'idem_api_transfer'
    };
    const pending = await post(`${baseUrl}/v1/execute`, transferRequest);
    assert.equal(pending.response.status, 202);
    assert.equal(pending.body.disposition, 'AWAITING_APPROVAL');

    const approval = await post(`${baseUrl}/v1/approve`, {
      request: transferRequest,
      approver: { id: 'approver.riley', roles: ['finance_approver'] }
    });
    assert.equal(approval.response.status, 201);
    assert.ok(approval.body.approvalToken);

    const completed = await post(`${baseUrl}/v1/execute`, {
      ...transferRequest,
      approvalToken: approval.body.approvalToken
    });
    assert.equal(completed.response.status, 200);
    assert.equal(completed.body.disposition, 'SUCCEEDED');

    const witness = await fetch(`${baseUrl}/v1/witness/verify`, {
      headers: { authorization: `Bearer ${API_KEY}` }
    });
    assert.equal(witness.status, 200);
    assert.equal((await witness.json()).valid, true);
  } finally {
    await control.close();
    await target.close();
    await fs.rm(directory, { recursive: true, force: true });
  }

  async function post(url, body) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        authorization: `Bearer ${API_KEY}`,
        'content-type': 'application/json'
      },
      body: JSON.stringify(body)
    });
    return { response, body: await response.json() };
  }
});
