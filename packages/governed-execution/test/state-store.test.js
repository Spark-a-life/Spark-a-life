import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { FileStateStore } from '../src/core/state-store.js';


test('durable state store persists and retrieves execution snapshots atomically', async () => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'state-store-test-'));
  const store = new FileStateStore({ directory });
  const snapshot = {
    requestId: 'request_state_store',
    state: 'SUCCEEDED',
    history: [{ state: 'SUCCEEDED', at: new Date().toISOString() }]
  };
  await store.save(snapshot);
  assert.deepEqual(await store.get(snapshot.requestId), snapshot);
  await store.remove(snapshot.requestId);
  assert.equal(await store.get(snapshot.requestId), null);
  await fs.rm(directory, { recursive: true, force: true });
});

test('durable state store rejects path traversal in request identifiers', async () => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'state-store-test-'));
  const store = new FileStateStore({ directory });
  await assert.rejects(
    store.save({ requestId: '../../escape', state: 'RECEIVED', history: [] }),
    /unsafe for durable state storage/
  );
  await fs.rm(directory, { recursive: true, force: true });
});
