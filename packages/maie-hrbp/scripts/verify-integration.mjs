#!/usr/bin/env node
/**
 * Integration verifier.
 *
 * Merges this overlay into a working copy of the WiseGen APE Intelligence OS
 * and exercises the real CaptainsGate and CapabilityRegistry against the
 * example action requests. Proves the manifest entries are governed correctly
 * by the actual OS code, not by a restatement of it.
 *
 * Usage:
 *   node scripts/verify-integration.mjs <path-to-ape-intelligence-os>
 */
import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';

const OVERLAY = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const osSource = process.argv[2];

if (!osSource || !fs.existsSync(path.join(osSource, 'src', 'governance', 'captains-gate.mjs'))) {
  console.error('Usage: node scripts/verify-integration.mjs <path-to-ape-intelligence-os>');
  console.error('The path must contain src/governance/captains-gate.mjs');
  process.exit(2);
}

const work = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'maie-integration-'));
fs.cpSync(osSource, work, { recursive: true });

// --- Merge the capability overlay -----------------------------------------
const registryPath = path.join(work, 'config', 'capabilities.json');
const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
const overlay = JSON.parse(fs.readFileSync(path.join(OVERLAY, 'config', 'capabilities.maie.json'), 'utf8'));
const existingIds = new Set(registry.capabilities.map((c) => c.id));
const added = overlay.capabilities.filter((c) => !existingIds.has(c.id));
registry.capabilities.push(...added);
fs.writeFileSync(registryPath, JSON.stringify(registry, null, 2));

// --- Merge the denial addendum --------------------------------------------
const policyPath = path.join(work, 'config', 'policies', 'captains-gate.json');
const policy = JSON.parse(fs.readFileSync(policyPath, 'utf8'));
const addendum = JSON.parse(fs.readFileSync(path.join(OVERLAY, 'config', 'policies', 'captains-gate.maie-addendum.json'), 'utf8'));
for (const denial of addendum.automatic_denials_add) {
  if (!policy.automatic_denials.includes(denial)) policy.automatic_denials.push(denial);
}
fs.writeFileSync(policyPath, JSON.stringify(policy, null, 2));

console.log(`[merge] ${added.length} capabilities added, ${addendum.automatic_denials_add.length} denials merged`);
console.log(`[merge] working copy: ${work}\n`);

// --- Schema conformance ----------------------------------------------------
const capSchema = JSON.parse(fs.readFileSync(path.join(work, 'schemas', 'capability.schema.json'), 'utf8'));
const reqSchema = JSON.parse(fs.readFileSync(path.join(work, 'schemas', 'action-request.schema.json'), 'utf8'));

function conforms(schema, obj, label) {
  const problems = [];
  for (const key of schema.required || []) {
    if (!(key in obj)) problems.push(`missing required field '${key}'`);
  }
  for (const [key, spec] of Object.entries(schema.properties || {})) {
    if (!(key in obj)) continue;
    if (spec.enum && !spec.enum.includes(obj[key])) problems.push(`'${key}' value '${obj[key]}' not in enum`);
    if (spec.type === 'string' && typeof obj[key] !== 'string') problems.push(`'${key}' must be string`);
    if (spec.type === 'boolean' && typeof obj[key] !== 'boolean') problems.push(`'${key}' must be boolean`);
    if (spec.type === 'array' && !Array.isArray(obj[key])) problems.push(`'${key}' must be array`);
  }
  console.log(`  ${problems.length === 0 ? 'PASS' : 'FAIL'}  ${label}${problems.length ? ': ' + problems.join('; ') : ''}`);
  return problems.length === 0;
}

let ok = true;
console.log('[schema] capability entries against schemas/capability.schema.json');
for (const c of overlay.capabilities) ok = conforms(capSchema, c, c.id) && ok;

const exampleFiles = fs.readdirSync(path.join(OVERLAY, 'examples')).filter((f) => f.startsWith('action-request'));
console.log('\n[schema] action requests against schemas/action-request.schema.json');
const requests = {};
for (const f of exampleFiles) {
  const req = JSON.parse(fs.readFileSync(path.join(OVERLAY, 'examples', f), 'utf8'));
  requests[f] = req;
  ok = conforms(reqSchema, req, f) && ok;
}

// --- Live Captain's Gate evaluation ---------------------------------------
const { CapabilityRegistry } = await import(pathToFileURL(path.join(work, 'src', 'governance', 'registry.mjs')));
const { CaptainsGate } = await import(pathToFileURL(path.join(work, 'src', 'governance', 'captains-gate.mjs')));

const estates = fs.readdirSync(path.join(work, 'config', 'estates'))
  .map((f) => JSON.parse(fs.readFileSync(path.join(work, 'config', 'estates', f), 'utf8')));
const runtimes = JSON.parse(fs.readFileSync(path.join(work, 'config', 'runtimes.json'), 'utf8'));

const gate = new CaptainsGate({
  policy,
  registry: new CapabilityRegistry(registry),
  runtimeRegistry: runtimes,
  estates
});

const expected = {
  'action-request-harvest.json': 'allow',
  'action-request-recommend.json': 'allow',
  'action-request-denied.json': 'deny',
  'action-request-unapproved.json': 'hold',
  'action-request-ceiling-breach.json': 'deny'
};

console.log('\n[gate] live evaluation through the real CaptainsGate');
for (const [file, req] of Object.entries(requests)) {
  const result = gate.evaluate(req);
  const want = expected[file];
  const pass = result.decision === want;
  if (!pass) ok = false;
  console.log(`  ${pass ? 'PASS' : 'FAIL'}  ${file.padEnd(38)} -> ${result.decision.padEnd(5)} (expected ${want})`);
  console.log(`         ${result.reason}`);
}

// --- OS self-verification --------------------------------------------------
console.log('\n[os] running the OS own verify and test commands with the overlay merged');
try {
  const verifyOut = execFileSync('node', ['src/cli.mjs', 'verify'], { cwd: work, encoding: 'utf8' });
  console.log(verifyOut.trim().split('\n').map((l) => '  ' + l).join('\n'));
} catch (err) {
  ok = false;
  console.log('  FAIL  OS verify failed: ' + (err.stdout || err.message));
}
try {
  execFileSync('node', ['--test'], { cwd: work, encoding: 'utf8', stdio: 'pipe' });
  console.log('  PASS  OS test suite passes with the overlay merged');
} catch (err) {
  ok = false;
  console.log('  FAIL  OS test suite failed with the overlay merged');
}

fs.rmSync(work, { recursive: true, force: true });
console.log(`\n[result] ${ok ? 'INTEGRATION VERIFIED' : 'INTEGRATION FAILED'}`);
process.exit(ok ? 0 : 1);
