import { HttpJsonAdapter } from './http-json-adapter.js';
import { BrowserCdpPipeAdapter } from './browser-cdp-pipe-adapter.js';
import { ValidationError } from '../core/errors.js';

export function createAdapterRegistry(runtimeConfig) {
  const adapters = new Map([
    ['http-json', new HttpJsonAdapter({ timeoutMs: runtimeConfig.executionTimeoutMs })],
    ['browser-cdp-pipe', new BrowserCdpPipeAdapter({
      chromiumPath: process.env.CHROMIUM_PATH,
      timeoutMs: runtimeConfig.browserTimeoutMs
    })]
  ]);
  return {
    get(name) {
      const adapter = adapters.get(name);
      if (!adapter) throw new ValidationError(`No adapter is registered for: ${name}`);
      return adapter;
    }
  };
}
