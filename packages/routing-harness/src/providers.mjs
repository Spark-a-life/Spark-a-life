/**
 * Provider adapters behind one contract:
 *   generate({ model, providerConfig, systemPrompt, schema, text, timeoutMs })
 *     -> { rawText, tokensIn, tokensOut, certifiable }
 *
 * Structured outputs are requested wherever the provider supports them, so
 * the harness measures semantic accuracy and cost, not formatting accidents.
 * The mock adapter is scaffolding: its results are marked certifiable:false
 * and the router refuses to certify from them.
 */

async function timedFetch(url, options, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

function apiKey(providerConfig) {
  const key = process.env[providerConfig.api_key_env];
  if (!key) {
    throw new Error(`Missing API key: set ${providerConfig.api_key_env}`);
  }
  return key;
}

/** Anthropic Messages API with forced tool use for schema-enforced output. */
async function anthropicGenerate({ model, providerConfig, systemPrompt, schema, text, timeoutMs }) {
  const res = await timedFetch(providerConfig.base_url, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': apiKey(providerConfig),
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: model.model_id,
      max_tokens: 1024,
      system: systemPrompt,
      messages: [{ role: 'user', content: text }],
      tools: [{
        name: 'emit_extraction',
        description: 'Emit the extraction result as structured JSON.',
        input_schema: schema
      }],
      tool_choice: { type: 'tool', name: 'emit_extraction' }
    })
  }, timeoutMs);

  if (!res.ok) throw new Error(`Anthropic HTTP ${res.status}: ${await res.text()}`);
  const data = await res.json();
  const toolBlock = (data.content || []).find((b) => b.type === 'tool_use');
  return {
    rawText: toolBlock ? JSON.stringify(toolBlock.input) : '',
    tokensIn: data.usage?.input_tokens ?? 0,
    tokensOut: data.usage?.output_tokens ?? 0,
    certifiable: true
  };
}

/** OpenAI-compatible chat completions with json_schema response format (OpenAI, xAI). */
async function openaiGenerate({ model, providerConfig, systemPrompt, schema, text, timeoutMs }) {
  const res = await timedFetch(providerConfig.base_url, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey(providerConfig)}`
    },
    body: JSON.stringify({
      model: model.model_id,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: text }
      ],
      response_format: {
        type: 'json_schema',
        json_schema: { name: 'extraction', strict: false, schema }
      }
    })
  }, timeoutMs);

  if (!res.ok) throw new Error(`OpenAI-compatible HTTP ${res.status}: ${await res.text()}`);
  const data = await res.json();
  return {
    rawText: data.choices?.[0]?.message?.content ?? '',
    tokensIn: data.usage?.prompt_tokens ?? 0,
    tokensOut: data.usage?.completion_tokens ?? 0,
    certifiable: true
  };
}

/**
 * Mock adapter for end-to-end testing without paid APIs.
 * Behaviour is honest scaffolding: it produces plausible variation, including
 * occasional non-compliance for mock-flaky, and every result is marked
 * certifiable:false. Fixtures here can exercise the pipeline; they can never
 * decide a production route.
 */
async function mockGenerate({ model, payload }) {
  const profiles = {
    'mock-fast': { latency: [120, 260], failRate: 0.0, verbosity: 1.0 },
    'mock-verbose': { latency: [280, 520], failRate: 0.0, verbosity: 1.9 },
    'mock-flaky': { latency: [90, 200], failRate: 0.15, verbosity: 1.0 }
  };
  const p = profiles[model.model_id] || profiles['mock-fast'];
  const latency = p.latency[0] + Math.random() * (p.latency[1] - p.latency[0]);
  await new Promise((r) => setTimeout(r, latency));

  const answer = { ...payload.expected, drivers: ['mock-driver-a', 'mock-driver-b'] };
  const body = JSON.stringify(answer);
  const failed = Math.random() < p.failRate;
  const rawText = failed ? '```json\n' + body + '\n```' : body;

  return {
    rawText,
    tokensIn: Math.round(140 * p.verbosity),
    tokensOut: Math.round((body.length / 4) * p.verbosity),
    certifiable: false
  };
}

export async function generate(args) {
  const adapter = args.providerConfig.adapter;
  if (adapter === 'anthropic') return anthropicGenerate(args);
  if (adapter === 'openai') return openaiGenerate(args);
  if (adapter === 'mock') return mockGenerate(args);
  throw new Error(`Unknown adapter: ${adapter}`);
}
