import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { BrowserCdpPipeAdapter } from '../src/adapters/browser-cdp-pipe-adapter.js';

const shouldRun = process.env.RUN_BROWSER_TESTS === '1';

test('isolated CDP-pipe adapter fills, clicks and observes a governed local fixture', { skip: !shouldRun }, async () => {
  const chromiumPath = process.env.CHROMIUM_PATH ?? await findChromium();
  const fixtureRoot = path.resolve('fixtures');
  const fixtureFile = path.join(fixtureRoot, 'browser-demo.html');
  const adapter = new BrowserCdpPipeAdapter({ chromiumPath, timeoutMs: 15000 });
  const result = await adapter.execute({
    request: {
      parameters: { name: 'Browser Test' }
    },
    operation: {
      allowedFilePrefixes: [fixtureRoot],
      plan: [
        { type: 'setContentFile', filePath: fixtureFile },
        { type: 'fill', selector: '#name', valueFrom: 'parameters.name' },
        { type: 'click', selector: '#submit' }
      ],
      observations: [
        { name: 'status', selector: '#status', property: 'textContent' }
      ]
    }
  });
  assert.equal(result.observations.status, 'Submitted for Browser Test');
});

async function findChromium() {
  for (const candidate of ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome']) {
    try {
      await fs.access(candidate);
      return candidate;
    } catch {
      // Continue.
    }
  }
  throw new Error('No Chromium executable found.');
}
