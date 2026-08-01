import http from 'node:http';
import { createRuntime } from './runtime.js';
import { logger } from './util/log.js';

export async function startControlServer({ host, port, runtimeOverrides = {} } = {}) {
  const runtime = await createRuntime(runtimeOverrides);
  const bindHost = host ?? process.env.CONTROL_HOST ?? '127.0.0.1';
  const bindPort = Number(port ?? process.env.CONTROL_PORT ?? 8787);
  if (!runtime.controlApiKey || runtime.controlApiKey.length < 24) {
    throw new Error('CONTROL_API_KEY must contain at least 24 characters.');
  }

  const rateLimit = new Map();
  const server = http.createServer(async (request, response) => {
    const startedAt = Date.now();
    const requestId = request.headers['x-request-id'] || `http_${cryptoRandomId()}`;
    response.setHeader('x-request-id', requestId);
    response.setHeader('cache-control', 'no-store');
    response.setHeader('x-content-type-options', 'nosniff');
    response.setHeader('content-security-policy', "default-src 'none'; frame-ancestors 'none'");

    try {
      const url = new URL(request.url, `http://${request.headers.host || `${bindHost}:${bindPort}`}`);
      if (request.method === 'GET' && url.pathname === '/health') {
        return sendJson(response, 200, {
          status: 'ok',
          service: runtime.runtimeConfig.serviceName,
          mode: runtime.mode
        });
      }

      authenticate(request, runtime.controlApiKey);
      enforceRateLimit(request, rateLimit);

      if (request.method === 'POST' && url.pathname === '/v1/execute') {
        const body = await readJsonBody(request, runtime.runtimeConfig.requestBodyLimitBytes);
        const result = await runtime.engine.execute(body);
        const status = statusForDisposition(result.disposition);
        return sendJson(response, status, result);
      }

      if (request.method === 'POST' && url.pathname === '/v1/approve') {
        const body = await readJsonBody(request, runtime.runtimeConfig.requestBodyLimitBytes);
        const { request: actionRequest, approver } = body;
        runtime.capabilityRegistry.resolve(actionRequest);
        const decision = runtime.policyEngine.evaluate(actionRequest);
        if (decision.effect !== 'REQUIRE_APPROVAL') {
          return sendJson(response, 409, {
            error: 'The submitted action does not currently require approval.',
            policyDecision: decision
          });
        }
        const approvalToken = await runtime.approvalService.issue({
          request: actionRequest,
          approver,
          requiredRole: decision.requiredApproverRole,
          ttlSeconds: decision.approvalTtlSeconds
        });
        await runtime.witnessChain.append('APPROVAL_ISSUED', {
          requestId: actionRequest.requestId,
          approver,
          requiredRole: decision.requiredApproverRole,
          expiresInSeconds: decision.approvalTtlSeconds
        });
        return sendJson(response, 201, {
          requestId: actionRequest.requestId,
          approvalToken,
          expiresInSeconds: decision.approvalTtlSeconds
        });
      }

      if (request.method === 'GET' && url.pathname === '/v1/witness/verify') {
        const verification = await runtime.witnessChain.verify();
        return sendJson(response, verification.valid ? 200 : 409, verification);
      }

      if (request.method === 'GET' && url.pathname.startsWith('/v1/requests/')) {
        const requestId = decodeURIComponent(url.pathname.slice('/v1/requests/'.length));
        const state = await runtime.stateStore.get(requestId);
        if (!state) return sendJson(response, 404, { error: 'request state not found' });
        return sendJson(response, 200, state);
      }

      return sendJson(response, 404, { error: 'not found' });
    } catch (error) {
      const status = error.statusCode ?? (error.code === 'VALIDATION_ERROR' ? 400 : 500);
      logger.error('Control API request failed.', {
        requestId,
        method: request.method,
        path: request.url,
        error: error.message,
        durationMs: Date.now() - startedAt
      });
      return sendJson(response, status, {
        error: error.message,
        code: error.code ?? 'CONTROL_API_ERROR',
        requestId
      });
    } finally {
      logger.info('Control API request completed.', {
        requestId,
        method: request.method,
        path: request.url,
        statusCode: response.statusCode,
        durationMs: Date.now() - startedAt
      });
    }
  });

  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(bindPort, bindHost, resolve);
  });
  const actualAddress = server.address();
  logger.info('WiseGen governed execution control API started.', {
    host: bindHost,
    port: actualAddress.port,
    mode: runtime.mode
  });
  return {
    server,
    runtime,
    close: () => new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()))
  };
}

function authenticate(request, expectedKey) {
  const header = request.headers.authorization;
  if (header !== `Bearer ${expectedKey}`) {
    const error = new Error('Unauthorised.');
    error.statusCode = 401;
    throw error;
  }
}

function enforceRateLimit(request, store) {
  const source = request.socket.remoteAddress ?? 'unknown';
  const now = Date.now();
  const windowMs = 60_000;
  const limit = 120;
  const current = store.get(source);
  if (!current || now - current.startedAt >= windowMs) {
    store.set(source, { startedAt: now, count: 1 });
    return;
  }
  current.count += 1;
  if (current.count > limit) {
    const error = new Error('Rate limit exceeded.');
    error.statusCode = 429;
    throw error;
  }
}

async function readJsonBody(request, limit) {
  let size = 0;
  const chunks = [];
  for await (const chunk of request) {
    size += chunk.length;
    if (size > limit) {
      const error = new Error('Request body exceeds configured limit.');
      error.statusCode = 413;
      throw error;
    }
    chunks.push(chunk);
  }
  const text = Buffer.concat(chunks).toString('utf8');
  try {
    return JSON.parse(text || '{}');
  } catch {
    const error = new Error('Request body is not valid JSON.');
    error.statusCode = 400;
    throw error;
  }
}

function statusForDisposition(disposition) {
  switch (disposition) {
    case 'SUCCEEDED': return 200;
    case 'AWAITING_APPROVAL':
    case 'STEP_UP_REQUIRED': return 202;
    case 'BLOCKED': return 403;
    case 'REJECTED': return 400;
    case 'STATE_UNCERTAIN': return 409;
    default: return 500;
  }
}

function sendJson(response, status, body) {
  if (response.writableEnded) return;
  const value = JSON.stringify(body);
  response.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(value)
  });
  response.end(value);
}

function cryptoRandomId() {
  return globalThis.crypto.randomUUID();
}
