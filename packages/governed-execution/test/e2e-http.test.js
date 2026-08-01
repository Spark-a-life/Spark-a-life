import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { startDemoTarget } from '../src/demo/target-server.js';
import { createRuntime } from '../src/runtime.js';

process.env.RUNTIME_MODE = 'demo';
process.env.CONTROL_API_KEY = 'demo-control-api-key-rotate-before-use';
process.env.WITNESS_HMAC_KEY = 'demo-witness-hmac-key-rotate-before-use-32bytes';
process.env.APPROVAL_HMAC_KEY = 'demo-approval-hmac-key-rotate-before-use-32bytes';


test('HTTP adapter completes an end-to-end action with semantic verification', async () => {
  const target = await startDemoTarget();
  process.env.TARGET_BASE_URL = target.baseUrl;
  process.env.BROWSER_DEMO_ROOT = path.resolve('fixtures');
  process.env.BROWSER_DEMO_FILE = path.resolve('fixtures/browser-demo.html');
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'e2e-http-'));
  const runtime = await createRuntime({
    witnessPath: path.join(directory, 'witness.jsonl'),
    approvalStorePath: path.join(directory, 'approvals.json'),
      stateStorePath: path.join(directory, 'state')
  });
  try {
    const result = await runtime.engine.execute({
      requestId: 'request_e2e_note',
      actor: { id: 'operator.alex', roles: ['operator'] },
      capabilityId: 'notes.create',
      operation: 'create',
      targetBaseUrl: target.baseUrl,
      parameters: { title: 'E2E', body: 'Verified' },
      idempotencyKey: 'idem_e2e_note'
    });
    assert.equal(result.disposition, 'SUCCEEDED');
    assert.equal(result.result.status, 201);
    assert.equal((await runtime.witnessChain.verify()).valid, true);
  } finally {
    await target.close();
    await fs.rm(directory, { recursive: true, force: true });
  }
});
