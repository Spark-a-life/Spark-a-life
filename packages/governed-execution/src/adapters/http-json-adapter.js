import { GovernedExecutionError, ValidationError } from '../core/errors.js';

export class HttpJsonAdapter {
  constructor({ timeoutMs = 15000 } = {}) {
    this.timeoutMs = timeoutMs;
  }

  async execute({ request, operation }) {
    if (!request.targetBaseUrl) {
      throw new ValidationError('targetBaseUrl is required for an HTTP capability.');
    }
    const base = new URL(request.targetBaseUrl);
    if (!['http:', 'https:'].includes(base.protocol)) {
      throw new ValidationError(`Unsupported target protocol: ${base.protocol}`);
    }
    const url = new URL(operation.path, base);
    if (url.origin !== base.origin) {
      throw new ValidationError('Resolved HTTP operation escaped the authorised target origin.');
    }

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const response = await fetch(url, {
        method: operation.method,
        headers: {
          'content-type': 'application/json',
          'accept': 'application/json',
          'idempotency-key': request.idempotencyKey,
          'x-wisegen-request-id': request.requestId
        },
        body: ['GET', 'HEAD'].includes(operation.method)
          ? undefined
          : JSON.stringify(request.parameters),
        signal: controller.signal,
        redirect: 'error'
      });
      const contentType = response.headers.get('content-type') ?? '';
      const body = contentType.includes('application/json')
        ? await response.json()
        : await response.text();
      if (response.status >= 500) {
        throw new GovernedExecutionError(`Target service returned ${response.status}.`, {
          code: 'TARGET_SERVICE_ERROR',
          retryable: true,
          details: { status: response.status, url: url.toString() }
        });
      }
      return {
        adapter: 'http-json',
        status: response.status,
        body,
        finalUrl: response.url,
        headers: {
          'content-type': response.headers.get('content-type'),
          'x-request-id': response.headers.get('x-request-id')
        }
      };
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new GovernedExecutionError('HTTP operation timed out.', {
          code: 'TARGET_TIMEOUT',
          retryable: true,
          details: { url: url.toString(), timeoutMs: this.timeoutMs }
        });
      }
      if (error instanceof GovernedExecutionError || error instanceof ValidationError) throw error;
      throw new GovernedExecutionError(`HTTP operation failed: ${error.message}`, {
        code: 'TARGET_CONNECTION_ERROR',
        retryable: true,
        details: { url: url.toString() }
      });
    } finally {
      clearTimeout(timeout);
    }
  }
}
