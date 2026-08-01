import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readJson } from './util/fs.js';
import { CapabilityRegistry } from './core/capability-registry.js';
import { PolicyEngine } from './core/policy-engine.js';
import { ApprovalService } from './core/approval-service.js';
import { WitnessChain } from './core/witness-chain.js';
import { createRedactor } from './security/redaction.js';
import { createAdapterRegistry } from './adapters/index.js';
import { GovernedExecutionEngine } from './core/engine.js';
import { FileStateStore } from './core/state-store.js';
import { ValidationError } from './core/errors.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DEMO_KEYS = [
  'demo-control-api-key-rotate-before-use',
  'demo-witness-hmac-key-rotate-before-use-32bytes',
  'demo-approval-hmac-key-rotate-before-use-32bytes'
];

export async function createRuntime(overrides = {}) {
  normaliseEnvironmentPath('BROWSER_DEMO_ROOT');
  normaliseEnvironmentPath('BROWSER_DEMO_FILE');
  const runtimeConfig = overrides.runtimeConfig ?? await readJson(path.join(ROOT, 'config/runtime.json'));
  const capabilities = overrides.capabilities ?? await readJson(path.join(ROOT, 'config/capabilities.json'));
  const policies = overrides.policies ?? await readJson(path.join(ROOT, 'config/policies.json'));
  const mode = process.env.RUNTIME_MODE ?? 'production';
  const witnessKey = overrides.witnessKey ?? process.env.WITNESS_HMAC_KEY;
  const approvalKey = overrides.approvalKey ?? process.env.APPROVAL_HMAC_KEY;
  const controlApiKey = overrides.controlApiKey ?? process.env.CONTROL_API_KEY;

  if (!witnessKey || !approvalKey) {
    throw new ValidationError('WITNESS_HMAC_KEY and APPROVAL_HMAC_KEY are required. Run npm run keygen.');
  }
  if (mode !== 'demo' && [witnessKey, approvalKey, controlApiKey].some((value) => DEMO_KEYS.includes(value))) {
    throw new ValidationError('Production mode refuses bundled demonstration credentials.');
  }

  const witnessPath = path.resolve(ROOT, overrides.witnessPath ?? process.env.WITNESS_LOG_PATH ?? 'var/witness/witness-chain.jsonl');
  const approvalStorePath = path.resolve(ROOT, overrides.approvalStorePath ?? process.env.APPROVAL_STORE_PATH ?? 'var/approvals/used-nonces.json');
  const stateStorePath = path.resolve(ROOT, overrides.stateStorePath ?? process.env.STATE_STORE_PATH ?? 'var/state');
  const redactor = createRedactor(runtimeConfig.witnessRedaction);
  const witnessChain = new WitnessChain({ filePath: witnessPath, key: witnessKey, redact: redactor });
  const approvalService = new ApprovalService({ key: approvalKey, storePath: approvalStorePath });
  const stateStore = new FileStateStore({ directory: stateStorePath });
  const capabilityRegistry = new CapabilityRegistry(capabilities);
  const policyEngine = new PolicyEngine(policies);
  const adapters = overrides.adapters ?? createAdapterRegistry(runtimeConfig);
  const engine = new GovernedExecutionEngine({
    capabilityRegistry,
    policyEngine,
    approvalService,
    witnessChain,
    stateStore,
    adapters,
    runtimeConfig
  });

  return {
    root: ROOT,
    mode,
    runtimeConfig,
    capabilityRegistry,
    policyEngine,
    approvalService,
    witnessChain,
    stateStore,
    adapters,
    engine,
    controlApiKey
  };
}


function normaliseEnvironmentPath(name) {
  const value = process.env[name];
  if (value && !path.isAbsolute(value)) {
    process.env[name] = path.resolve(ROOT, value);
  }
}
