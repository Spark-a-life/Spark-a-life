/**
 * Benchmark runner.
 * Repeated trials per payload per model through a bounded promise pool.
 * worker_threads from v1.0 are gone: model calls are I/O-bound, so a promise
 * pool gives the same concurrency without thread overhead.
 */
import { performance } from 'node:perf_hooks';
import { generate } from './providers.mjs';
import { validate, isStrictJson, countLeafNodes, deepEqual } from './validate.mjs';
import { aggregate, semanticAccuracy } from './metrics.mjs';

async function pool(tasks, concurrency) {
  const results = new Array(tasks.length);
  let next = 0;
  async function worker() {
    while (next < tasks.length) {
      const i = next++;
      results[i] = await tasks[i]();
    }
  }
  await Promise.all(Array.from({ length: Math.min(concurrency, tasks.length) }, worker));
  return results;
}

async function runTrial({ modelAlias, modelConfig, providerConfig, payloadSet, payload, trial, timeoutMs }) {
  const start = performance.now();
  const base = {
    modelAlias,
    payloadId: payload.id,
    trial,
    timestamp: new Date().toISOString()
  };
  try {
    const out = await generate({
      model: modelConfig,
      providerConfig,
      systemPrompt: payloadSet.system_prompt,
      schema: payloadSet.schema,
      text: payload.text,
      payload,
      timeoutMs
    });
    const durationMs = Math.round(performance.now() - start);
    const rawText = (out.rawText || '').trim();
    const strict = isStrictJson(rawText);

    let schemaValid = false;
    let nodeCount = 0;
    let accuracy = null;
    let errorMessage = '';
    try {
      const parsed = JSON.parse(rawText);
      const result = validate(payloadSet.schema, parsed);
      schemaValid = result.valid;
      if (!result.valid) errorMessage = result.errors.join('; ');
      nodeCount = countLeafNodes(parsed);
      accuracy = semanticAccuracy(payload.expected, parsed, deepEqual);
    } catch (parseErr) {
      errorMessage = `JSON parse: ${parseErr.message}`;
    }

    return {
      ...base,
      durationMs,
      tokensIn: out.tokensIn,
      tokensOut: out.tokensOut,
      nodeCount,
      strictJsonValid: strict,
      schemaValid,
      semanticAccuracy: accuracy,
      certifiable: out.certifiable,
      transportError: false,
      errorMessage
    };
  } catch (err) {
    return {
      ...base,
      durationMs: Math.round(performance.now() - start),
      tokensIn: 0,
      tokensOut: 0,
      nodeCount: 0,
      strictJsonValid: false,
      schemaValid: false,
      semanticAccuracy: null,
      certifiable: false,
      transportError: true,
      errorMessage: err.message
    };
  }
}

/**
 * Run the benchmark for one task class.
 * @returns {{ evidence: object[], trials: object[] }}
 */
export async function runBenchmark({ config, taskClass, payloadSet, useMock }) {
  const tc = config.task_classes[taskClass];
  const candidates = useMock ? tc.mock_candidates : tc.candidates;
  if (!candidates || candidates.length === 0) {
    throw new Error(`Task class ${taskClass} has no ${useMock ? 'mock ' : ''}candidates.`);
  }

  const tasks = [];
  for (const modelAlias of candidates) {
    const modelConfig = config.models[modelAlias];
    if (!modelConfig) throw new Error(`Model not in config: ${modelAlias}`);
    const providerConfig = config.providers[modelConfig.provider];
    for (const payload of payloadSet.payloads) {
      for (let trial = 1; trial <= config.execution.trials_per_payload; trial++) {
        tasks.push(() => runTrial({
          modelAlias,
          modelConfig,
          providerConfig,
          payloadSet,
          payload,
          trial,
          timeoutMs: config.execution.request_timeout_ms
        }));
      }
    }
  }

  const trials = await pool(tasks, config.execution.concurrency);
  const evidence = candidates.map((alias) =>
    aggregate(alias, config.models[alias], trials.filter((t) => t.modelAlias === alias))
  );
  return { evidence, trials };
}
