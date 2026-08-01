#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { loadEnvFile } from './util/env.js';
import { runDemo } from './demo/demo-runner.js';
import { startDemoTarget } from './demo/target-server.js';
import { startControlServer } from './server.js';
import { createRuntime } from './runtime.js';

await loadEnvFile(path.resolve('.env'));

const [command = 'help', ...args] = process.argv.slice(2);

try {
  switch (command) {
    case 'demo':
      await runDemo();
      break;
    case 'serve': {
      const service = await startControlServer();
      const shutdown = async () => {
        await service.close();
        process.exit(0);
      };
      process.once('SIGINT', shutdown);
      process.once('SIGTERM', shutdown);
      break;
    }
    case 'demo-target': {
      const host = process.env.DEMO_TARGET_HOST ?? '127.0.0.1';
      const port = Number(process.env.DEMO_TARGET_PORT ?? 8899);
      const target = await startDemoTarget({ host, port });
      console.log(JSON.stringify({ status: 'started', baseUrl: target.baseUrl }, null, 2));
      const shutdown = async () => {
        await target.close();
        process.exit(0);
      };
      process.once('SIGINT', shutdown);
      process.once('SIGTERM', shutdown);
      break;
    }
    case 'run': {
      const filePath = args[0];
      if (!filePath) throw new Error('Usage: npm run run -- examples/note-create.json');
      const request = JSON.parse(await fs.readFile(path.resolve(filePath), 'utf8'));
      const runtime = await createRuntime();
      const result = await runtime.engine.execute(request);
      console.log(JSON.stringify(result, null, 2));
      process.exitCode = result.disposition === 'SUCCEEDED' ? 0 : 2;
      break;
    }
    case 'approve': {
      const requestPath = args[0];
      const approverPath = args[1];
      if (!requestPath || !approverPath) {
        throw new Error('Usage: npm run approve -- examples/transfer-request.json examples/finance-approver.json');
      }
      const request = JSON.parse(await fs.readFile(path.resolve(requestPath), 'utf8'));
      const approver = JSON.parse(await fs.readFile(path.resolve(approverPath), 'utf8'));
      const runtime = await createRuntime();
      runtime.capabilityRegistry.resolve(request);
      const decision = runtime.policyEngine.evaluate(request);
      if (decision.effect !== 'REQUIRE_APPROVAL') {
        throw new Error(`Policy effect is ${decision.effect}; no approval token can be issued.`);
      }
      const approvalToken = await runtime.approvalService.issue({
        request,
        approver,
        requiredRole: decision.requiredApproverRole,
        ttlSeconds: decision.approvalTtlSeconds
      });
      await runtime.witnessChain.append('APPROVAL_ISSUED', {
        requestId: request.requestId,
        approver,
        requiredRole: decision.requiredApproverRole,
        expiresInSeconds: decision.approvalTtlSeconds
      });
      console.log(JSON.stringify({ requestId: request.requestId, approvalToken }, null, 2));
      break;
    }
    case 'verify-witness': {
      const runtime = await createRuntime();
      const result = await runtime.witnessChain.verify();
      console.log(JSON.stringify(result, null, 2));
      process.exitCode = result.valid ? 0 : 3;
      break;
    }
    case 'help':
    default:
      printHelp();
      process.exitCode = command === 'help' ? 0 : 1;
  }
} catch (error) {
  console.error(JSON.stringify({
    error: error.message,
    code: error.code ?? 'CLI_ERROR'
  }, null, 2));
  process.exitCode = 1;
}

function printHelp() {
  console.log(`WiseGen APE Governed Execution v1.0.0

Commands:
  npm run demo
      Run the complete local demonstration, including HTTP actions, approval,
      policy denial, browser execution, semantic verification and Witness Chain verification.

  npm run serve
      Start the authenticated local control API.

  node src/cli.js demo-target
      Start the bundled demonstration target on 127.0.0.1:8899.

  npm run run -- examples/note-create.json
      Execute one governed action request.

  npm run approve -- examples/transfer-request.json examples/finance-approver.json
      Issue a short-lived, single-use approval token bound to the exact action.

  npm run verify:witness
      Verify the full HMAC-signed hash chain.

  npm test
      Run the automated test suite.
`);
}
