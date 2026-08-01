import fs from 'node:fs/promises';
import path from 'node:path';
import { startDemoTarget } from './target-server.js';
import { createRuntime } from '../runtime.js';
import { randomId } from '../security/crypto.js';

const DEMO_ENV = {
  RUNTIME_MODE: 'demo',
  CONTROL_API_KEY: 'demo-control-api-key-rotate-before-use',
  WITNESS_HMAC_KEY: 'demo-witness-hmac-key-rotate-before-use-32bytes',
  APPROVAL_HMAC_KEY: 'demo-approval-hmac-key-rotate-before-use-32bytes'
};

export async function runDemo() {
  for (const [key, value] of Object.entries(DEMO_ENV)) {
    if (!process.env[key]) process.env[key] = value;
  }
  const target = await startDemoTarget();
  process.env.TARGET_BASE_URL = target.baseUrl;
  process.env.BROWSER_DEMO_ROOT = path.resolve('fixtures');
  process.env.BROWSER_DEMO_FILE = path.resolve('fixtures/browser-demo.html');
  process.env.CHROMIUM_PATH = process.env.CHROMIUM_PATH ?? await findChromium();

  const runId = `${Date.now()}_${process.pid}`;
  const witnessPath = path.resolve(`var/witness/demo-${runId}.jsonl`);
  const approvalStorePath = path.resolve(`var/approvals/demo-${runId}.json`);
  const stateStorePath = path.resolve(`var/state/demo-${runId}`);
  const runtime = await createRuntime({ witnessPath, approvalStorePath, stateStorePath });

  try {
    const noteRequest = {
      requestId: randomId('request'),
      actor: { id: 'operator.alex', roles: ['operator'] },
      capabilityId: 'notes.create',
      operation: 'create',
      targetBaseUrl: target.baseUrl,
      parameters: { title: 'Governed execution', body: 'A verified low-consequence action.' },
      idempotencyKey: randomId('idem')
    };
    const noteResult = await runtime.engine.execute(noteRequest);

    const transferRequest = {
      requestId: randomId('request'),
      actor: { id: 'finance.morgan', roles: ['finance_operator'] },
      capabilityId: 'payments.transfer',
      operation: 'submit',
      targetBaseUrl: target.baseUrl,
      parameters: {
        amount: 2500,
        currency: 'SGD',
        beneficiary: 'Approved Demonstration Vendor',
        purpose: 'Governed execution demonstration'
      },
      idempotencyKey: randomId('idem')
    };
    const pendingResult = await runtime.engine.execute(transferRequest);
    const approvalToken = await runtime.approvalService.issue({
      request: transferRequest,
      approver: { id: 'approver.riley', roles: ['finance_approver'] },
      requiredRole: pendingResult.policyDecision.requiredApproverRole,
      ttlSeconds: pendingResult.policyDecision.approvalTtlSeconds
    });
    const transferResult = await runtime.engine.execute({ ...transferRequest, approvalToken });

    const blockedResult = await runtime.engine.execute({
      ...transferRequest,
      requestId: randomId('request'),
      idempotencyKey: randomId('idem'),
      parameters: { ...transferRequest.parameters, amount: 75000 }
    });

    const browserResult = await runtime.engine.execute({
      requestId: randomId('request'),
      actor: { id: 'operator.alex', roles: ['operator'] },
      capabilityId: 'demo.browser-form',
      operation: 'submit',
      parameters: { name: 'WiseGen APE Intelligence' },
      idempotencyKey: randomId('idem')
    });

    const witnessVerification = await runtime.witnessChain.verify();
    const summary = {
      target: target.baseUrl,
      witnessPath,
      results: {
        note: noteResult.disposition,
        transferBeforeApproval: pendingResult.disposition,
        transferAfterApproval: transferResult.disposition,
        oversizedTransfer: blockedResult.disposition,
        browserForm: browserResult.disposition
      },
      witnessVerification
    };
    console.log(JSON.stringify(summary, null, 2));

    const expected = {
      note: 'SUCCEEDED',
      transferBeforeApproval: 'AWAITING_APPROVAL',
      transferAfterApproval: 'SUCCEEDED',
      oversizedTransfer: 'BLOCKED',
      browserForm: 'SUCCEEDED'
    };
    for (const [key, value] of Object.entries(expected)) {
      if (summary.results[key] !== value) {
        throw new Error(`Demonstration assertion failed for ${key}: expected ${value}, received ${summary.results[key]}`);
      }
    }
    if (!witnessVerification.valid) throw new Error('Witness Chain verification failed.');
    return summary;
  } finally {
    await target.close();
    await fs.rm(approvalStorePath, { force: true });
    await fs.rm(stateStorePath, { recursive: true, force: true });
  }
}

async function findChromium() {
  const candidates = [
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/usr/bin/google-chrome',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  ];
  for (const candidate of candidates) {
    try {
      await fs.access(candidate);
      return candidate;
    } catch {
      // Continue.
    }
  }
  throw new Error('Chromium was not found. Set CHROMIUM_PATH to a Chrome or Chromium executable.');
}
