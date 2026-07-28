import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { WitnessChain } from '../src/core/witness-chain.js';
import { createRedactor } from '../src/security/redaction.js';

async function fixture() {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'witness-test-'));
  const filePath = path.join(directory, 'chain.jsonl');
  const chain = new WitnessChain({
    filePath,
    key: 'w'.repeat(48),
    redact: createRedactor({ sensitiveKeys: ['token'] })
  });
  return { directory, filePath, chain };
}

test('Witness Chain verifies chained hashes and signatures', async () => {
  const { directory, chain } = await fixture();
  await chain.append('REQUEST_RECEIVED', { requestId: 'one', token: 'sensitive' });
  await chain.append('ACTION_COMPLETED', { requestId: 'one' });
  const result = await chain.verify();
  assert.equal(result.valid, true);
  assert.equal(result.records, 2);
  await fs.rm(directory, { recursive: true, force: true });
});

test('Witness Chain detects record tampering', async () => {
  const { directory, filePath, chain } = await fixture();
  await chain.append('REQUEST_RECEIVED', { requestId: 'one' });
  const text = await fs.readFile(filePath, 'utf8');
  await fs.writeFile(filePath, text.replace('REQUEST_RECEIVED', 'REQUEST_CHANGED'));
  const result = await chain.verify();
  assert.equal(result.valid, false);
  assert.match(result.reason, /hash/i);
  await fs.rm(directory, { recursive: true, force: true });
});
