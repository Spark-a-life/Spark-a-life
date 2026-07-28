#!/usr/bin/env node
/**
 * WiseGen Model Routing Harness v1.1 CLI
 *
 * Commands:
 *   verify                       Config sanity + witness chain integrity
 *   bench <task_class> [--mock]  Run repeated-trial benchmark, write evidence
 *   route <task_class> [--mock] [--scaffold]
 *                                Decide route from latest evidence, witness it
 *   demo                         Mock bench + scaffold route, end to end
 *   witness                      Show witness chain verification summary
 */
import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';
import { runBenchmark } from './harness.mjs';
import { decideRoute, commitRoute } from './route.mjs';
import { WitnessChain } from './witness.mjs';
import { toCsv } from './metrics.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONFIG_PATH = path.join(ROOT, 'config', 'harness.config.json');
const OUT_DIR = path.join(ROOT, 'var');
const WITNESS_PATH = path.join(ROOT, 'var', 'witness', 'routing-witness.jsonl');

function loadConfig() {
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function loadPayloadSet(config, taskClass) {
  const rel = config.task_classes[taskClass]?.payload_set;
  if (!rel) return null;
  return JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
}

function evidencePath(taskClass, useMock) {
  return path.join(OUT_DIR, `evidence-${taskClass}${useMock ? '-mock' : ''}.json`);
}

async function cmdBench(taskClass, useMock) {
  const config = loadConfig();
  if (!config.task_classes[taskClass]) throw new Error(`Unknown task class: ${taskClass}`);
  if (config.task_classes[taskClass].status === 'delegated') {
    console.log(`Task class '${taskClass}' is delegated: ${config.task_classes[taskClass].note}`);
    return;
  }
  const payloadSet = loadPayloadSet(config, taskClass);
  console.log(`[bench] ${taskClass} | mode=${useMock ? 'MOCK (non-certifiable scaffolding)' : 'LIVE'} | trials/payload=${config.execution.trials_per_payload}`);

  const { evidence, trials } = await runBenchmark({ config, taskClass, payloadSet, useMock });

  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(evidencePath(taskClass, useMock), JSON.stringify({
    generated_at: new Date().toISOString(),
    task_class: taskClass,
    mode: useMock ? 'mock' : 'live',
    payload_set: payloadSet.set_id,
    evidence,
    trial_count: trials.length
  }, null, 2));
  fs.writeFileSync(path.join(OUT_DIR, `evidence-${taskClass}${useMock ? '-mock' : ''}.csv`), toCsv(evidence));
  fs.writeFileSync(path.join(OUT_DIR, `trials-${taskClass}${useMock ? '-mock' : ''}.json`), JSON.stringify(trials, null, 2));

  for (const e of evidence) {
    console.log(`  ${e.modelAlias.padEnd(14)} compliance=${(e.complianceRate * 100).toFixed(1)}% accuracy=${e.semanticAccuracy ?? 'n/a'} p50=${e.latencyP50}ms cost/node=${e.costPerValidatedNode ?? 'unpriced'} certifiable=${e.certifiable}`);
  }
  console.log(`[bench] Evidence written to ${evidencePath(taskClass, useMock)}`);
}

function cmdRoute(taskClass, useMock, scaffold) {
  const config = loadConfig();
  const tc = config.task_classes[taskClass];
  if (!tc) throw new Error(`Unknown task class: ${taskClass}`);

  let evidence = [];
  let evidenceRef = null;
  if (tc.status !== 'delegated') {
    const p = evidencePath(taskClass, useMock);
    if (!fs.existsSync(p)) throw new Error(`No evidence at ${p}. Run bench first.`);
    const file = JSON.parse(fs.readFileSync(p, 'utf8'));
    evidence = file.evidence;
    evidenceRef = path.relative(ROOT, p);
  }

  const decision = decideRoute({ config, taskClass, evidence, scaffold: scaffold || useMock });
  const chain = new WitnessChain(WITNESS_PATH);
  const record = commitRoute({ chain, decision, evidenceRef });

  if (decision.decision === 'certified') {
    const matrixPath = path.join(OUT_DIR, 'routing-matrix.json');
    const matrix = fs.existsSync(matrixPath) ? JSON.parse(fs.readFileSync(matrixPath, 'utf8')) : {};
    matrix[taskClass] = {
      primary: decision.primary,
      fallback: decision.fallback,
      certified_at: record.timestamp,
      witness_index: record.index
    };
    fs.writeFileSync(matrixPath, JSON.stringify(matrix, null, 2));
    console.log(`[route] CERTIFIED ${taskClass}: primary=${decision.primary} fallback=${decision.fallback}`);
  } else {
    console.log(`[route] ${decision.decision.toUpperCase()} ${taskClass}: primary=${decision.primary ?? '-'} (not written to production matrix)`);
    if (decision.denials?.length) console.log(`  guards: ${decision.denials.join(', ')}`);
  }
  for (const w of decision.warnings ?? []) console.log(`  warning: ${w}`);
  console.log(`  rationale: ${decision.rationale}`);
  console.log(`  witness record #${record.index} appended (${record.hash.slice(0, 12)}...)`);
}

function cmdVerify() {
  const config = loadConfig();
  const issues = [];
  for (const [alias, m] of Object.entries(config.models)) {
    if (config.providers[m.provider]?.certifiable && (m.price_per_mtok_out === null || String(m.model_id).startsWith('VERIFY'))) {
      issues.push(`${alias}: model_id or pricing unverified (certification will be blocked for cost-primary routing).`);
    }
  }
  const chain = new WitnessChain(WITNESS_PATH);
  const result = chain.verify();
  console.log(`[verify] config: ${issues.length === 0 ? 'clean' : issues.length + ' advisories'}`);
  issues.forEach((i) => console.log(`  advisory: ${i}`));
  console.log(`[verify] witness chain: ${result.valid ? `valid (${result.length} records)` : `INVALID at #${result.at}: ${result.reason}`}`);
  if (!result.valid) process.exitCode = 1;
}

function cmdWitness() {
  const chain = new WitnessChain(WITNESS_PATH);
  const result = chain.verify();
  const records = chain.read();
  console.log(`[witness] ${result.valid ? 'valid' : 'INVALID'} | records=${records.length}`);
  for (const r of records.slice(-5)) {
    console.log(`  #${r.index} ${r.timestamp} ${r.action} ${r.payload.task_class ?? ''} -> ${r.payload.primary ?? '-'} certified=${r.payload.certified}`);
  }
}

async function main() {
  const [cmd, arg] = process.argv.slice(2);
  const useMock = process.argv.includes('--mock');
  const scaffold = process.argv.includes('--scaffold');

  if (cmd === 'bench' && arg) return cmdBench(arg, useMock);
  if (cmd === 'route' && arg) return cmdRoute(arg, useMock, scaffold);
  if (cmd === 'verify') return cmdVerify();
  if (cmd === 'witness') return cmdWitness();
  if (cmd === 'demo') {
    await cmdBench('extraction', true);
    cmdRoute('extraction', true, true);
    cmdRoute('build', true, true);
    return cmdVerify();
  }
  console.log('Usage: node src/cli.mjs <verify|bench <class> [--mock]|route <class> [--mock] [--scaffold]|witness|demo>');
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
