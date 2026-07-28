import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { GovernedExecutionError, ValidationError } from '../core/errors.js';
import { getPath } from '../util/object.js';

class CdpPipeTransport {
  constructor(processHandle, timeoutMs) {
    this.process = processHandle;
    this.timeoutMs = timeoutMs;
    this.nextId = 1;
    this.pending = new Map();
    this.waiters = new Set();
    this.buffer = '';

    processHandle.stdio[4].setEncoding('utf8');
    processHandle.stdio[4].on('data', (chunk) => this.#onData(chunk));
    processHandle.on('exit', (code, signal) => {
      const error = new GovernedExecutionError('Chromium process exited.', {
        code: 'BROWSER_EXITED',
        retryable: true,
        details: { code, signal }
      });
      for (const { reject, timer } of this.pending.values()) {
        clearTimeout(timer);
        reject(error);
      }
      this.pending.clear();
    });
  }

  send(method, params = {}, sessionId) {
    const id = this.nextId++;
    const message = { id, method, params };
    if (sessionId) message.sessionId = sessionId;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new GovernedExecutionError(`CDP command timed out: ${method}`, {
          code: 'CDP_TIMEOUT',
          retryable: true,
          details: { method, timeoutMs: this.timeoutMs }
        }));
      }, this.timeoutMs);
      this.pending.set(id, { resolve, reject, timer, method });
      this.process.stdio[3].write(`${JSON.stringify(message)}\0`);
    });
  }

  waitForEvent(method, { sessionId, predicate = () => true, timeoutMs = this.timeoutMs } = {}) {
    return new Promise((resolve, reject) => {
      const waiter = { method, sessionId, predicate, resolve, reject, timer: null };
      waiter.timer = setTimeout(() => {
        this.waiters.delete(waiter);
        reject(new GovernedExecutionError(`CDP event timed out: ${method}`, {
          code: 'CDP_EVENT_TIMEOUT',
          retryable: true,
          details: { method, timeoutMs }
        }));
      }, timeoutMs);
      this.waiters.add(waiter);
    });
  }

  #onData(chunk) {
    this.buffer += chunk;
    let separator;
    while ((separator = this.buffer.indexOf('\0')) >= 0) {
      const raw = this.buffer.slice(0, separator);
      this.buffer = this.buffer.slice(separator + 1);
      if (!raw) continue;
      let message;
      try {
        message = JSON.parse(raw);
      } catch {
        continue;
      }
      if (message.id) {
        const pending = this.pending.get(message.id);
        if (!pending) continue;
        clearTimeout(pending.timer);
        this.pending.delete(message.id);
        if (message.error) {
          pending.reject(new GovernedExecutionError(`CDP command failed: ${pending.method}`, {
            code: 'CDP_COMMAND_ERROR',
            retryable: false,
            details: message.error
          }));
        } else {
          pending.resolve(message.result ?? {});
        }
        continue;
      }
      if (message.method) {
        for (const waiter of [...this.waiters]) {
          if (waiter.method !== message.method) continue;
          if (waiter.sessionId && waiter.sessionId !== message.sessionId) continue;
          if (!waiter.predicate(message.params ?? {})) continue;
          clearTimeout(waiter.timer);
          this.waiters.delete(waiter);
          waiter.resolve(message.params ?? {});
        }
      }
    }
  }
}

export class BrowserCdpPipeAdapter {
  constructor({ chromiumPath, timeoutMs = 15000 } = {}) {
    this.chromiumPath = chromiumPath ?? process.env.CHROMIUM_PATH ?? 'chromium';
    this.timeoutMs = timeoutMs;
  }

  async execute({ request, operation }) {
    const allowedOrigins = new Set((operation.allowedOrigins ?? []).map((value) => new URL(value).origin));
    const allowedUrlPrefixes = operation.allowedUrlPrefixes ?? [];
    const allowedFilePrefixes = (operation.allowedFilePrefixes ?? []).map((value) => path.resolve(value));
    if (allowedOrigins.size === 0 && allowedUrlPrefixes.length === 0 && allowedFilePrefixes.length === 0) {
      throw new ValidationError('Browser capability must declare an allowed origin, URL prefix or file prefix.');
    }

    const profileDirectory = await fs.mkdtemp(path.join(os.tmpdir(), 'wisegen-browser-'));
    const args = [
      '--headless=new',
      '--remote-debugging-pipe',
      `--user-data-dir=${profileDirectory}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-background-networking',
      '--disable-component-update',
      '--disable-default-apps',
      '--disable-extensions',
      '--disable-sync',
      '--disable-translate',
      '--metrics-recording-only',
      '--mute-audio',
      'about:blank'
    ];
    if ((typeof process.getuid === 'function' && process.getuid() === 0) || process.env.BROWSER_NO_SANDBOX === '1') {
      args.push('--no-sandbox');
    }

    const browser = spawn(this.chromiumPath, args, {
      stdio: ['ignore', 'ignore', 'pipe', 'pipe', 'pipe']
    });
    let browserExited = false;
    browser.once('exit', () => { browserExited = true; });
    let stderr = '';
    browser.stderr.setEncoding('utf8');
    browser.stderr.on('data', (chunk) => {
      stderr = `${stderr}${chunk}`.slice(-4096);
    });

    const transport = new CdpPipeTransport(browser, this.timeoutMs);
    try {
      await transport.send('Browser.getVersion');
      const { targetId } = await transport.send('Target.createTarget', { url: 'about:blank' });
      const { sessionId } = await transport.send('Target.attachToTarget', { targetId, flatten: true });
      await Promise.all([
        transport.send('Page.enable', {}, sessionId),
        transport.send('DOM.enable', {}, sessionId),
        transport.send('Runtime.enable', {}, sessionId)
      ]);

      for (const step of operation.plan ?? []) {
        if (step.type === 'navigate') {
          const destination = new URL(step.url);
          const allowedByOrigin = allowedOrigins.has(destination.origin);
          const allowedByPrefix = allowedUrlPrefixes.some((prefix) => destination.toString().startsWith(prefix));
          if (!allowedByOrigin && !allowedByPrefix) {
            throw new ValidationError(`Browser navigation is not allowlisted: ${destination.toString()}`);
          }
          const loaded = transport.waitForEvent('Page.loadEventFired', { sessionId });
          const navigation = await transport.send('Page.navigate', { url: destination.toString() }, sessionId);
          if (navigation.errorText) {
            loaded.catch(() => {});
            throw new GovernedExecutionError(`Browser navigation failed: ${navigation.errorText}`, {
              code: 'BROWSER_NAVIGATION_ERROR',
              retryable: true
            });
          }
          await loaded;
        } else if (step.type === 'setContentFile') {
          const resolvedFile = path.resolve(step.filePath);
          const allowed = allowedFilePrefixes.some((prefix) => resolvedFile === prefix || resolvedFile.startsWith(`${prefix}${path.sep}`));
          if (!allowed) {
            throw new ValidationError(`Browser content file is not allowlisted: ${resolvedFile}`);
          }
          const html = await fs.readFile(resolvedFile, 'utf8');
          const { frameTree } = await transport.send('Page.getFrameTree', {}, sessionId);
          await transport.send('Page.setDocumentContent', {
            frameId: frameTree.frame.id,
            html
          }, sessionId);
        } else if (step.type === 'fill') {
          const value = getPath(request, step.valueFrom);
          if (typeof value !== 'string') {
            throw new ValidationError(`Browser fill value must be a string: ${step.valueFrom}`);
          }
          const nodeId = await querySelector(transport, sessionId, step.selector);
          await transport.send('DOM.focus', { nodeId }, sessionId);
          await selectAllAndClear(transport, sessionId);
          await transport.send('Input.insertText', { text: value }, sessionId);
        } else if (step.type === 'click') {
          const nodeId = await querySelector(transport, sessionId, step.selector);
          await transport.send('DOM.scrollIntoViewIfNeeded', { nodeId }, sessionId);
          const { model } = await transport.send('DOM.getBoxModel', { nodeId }, sessionId);
          const quad = model?.content;
          if (!Array.isArray(quad) || quad.length !== 8) {
            throw new GovernedExecutionError(`Unable to resolve click geometry for ${step.selector}.`, {
              code: 'BROWSER_GEOMETRY_ERROR',
              retryable: false
            });
          }
          const x = (quad[0] + quad[2] + quad[4] + quad[6]) / 4;
          const y = (quad[1] + quad[3] + quad[5] + quad[7]) / 4;
          await transport.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }, sessionId);
          await transport.send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }, sessionId);
          await transport.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }, sessionId);
        } else {
          throw new ValidationError(`Unsupported browser-plan step: ${step.type}`);
        }
      }

      const observations = {};
      for (const observation of operation.observations ?? []) {
        if (!['textContent', 'value', 'checked'].includes(observation.property)) {
          throw new ValidationError(`Unsupported browser observation property: ${observation.property}`);
        }
        const expression = `(() => { const element = document.querySelector(${JSON.stringify(observation.selector)}); return element ? element[${JSON.stringify(observation.property)}] : null; })()`;
        const evaluated = await transport.send('Runtime.evaluate', {
          expression,
          returnByValue: true,
          awaitPromise: true
        }, sessionId);
        observations[observation.name] = evaluated.result?.value ?? null;
      }
      const urlResult = await transport.send('Runtime.evaluate', {
        expression: 'window.location.href',
        returnByValue: true
      }, sessionId);
      return {
        adapter: 'browser-cdp-pipe',
        status: 200,
        finalUrl: urlResult.result?.value,
        observations
      };
    } catch (error) {
      if (error instanceof ValidationError || error instanceof GovernedExecutionError) throw error;
      throw new GovernedExecutionError(`Browser operation failed: ${error.message}`, {
        code: 'BROWSER_OPERATION_ERROR',
        retryable: false,
        details: { stderr }
      });
    } finally {
      if (!browserExited) browser.kill('SIGTERM');
      await Promise.race([
        browserExited ? Promise.resolve() : new Promise((resolve) => browser.once('exit', resolve)),
        new Promise((resolve) => setTimeout(resolve, 1000))
      ]);
      if (!browserExited) browser.kill('SIGKILL');
      await fs.rm(profileDirectory, { recursive: true, force: true });
    }
  }
}

async function querySelector(transport, sessionId, selector) {
  const { root } = await transport.send('DOM.getDocument', { depth: 1, pierce: true }, sessionId);
  const { nodeId } = await transport.send('DOM.querySelector', { nodeId: root.nodeId, selector }, sessionId);
  if (!nodeId) {
    throw new GovernedExecutionError(`Browser selector did not match: ${selector}`, {
      code: 'BROWSER_SELECTOR_NOT_FOUND',
      retryable: false
    });
  }
  return nodeId;
}

async function selectAllAndClear(transport, sessionId) {
  const modifier = process.platform === 'darwin' ? 4 : 2;
  await transport.send('Input.dispatchKeyEvent', {
    type: 'keyDown',
    key: 'a',
    code: 'KeyA',
    windowsVirtualKeyCode: 65,
    nativeVirtualKeyCode: 65,
    modifiers: modifier
  }, sessionId);
  await transport.send('Input.dispatchKeyEvent', {
    type: 'keyUp',
    key: 'a',
    code: 'KeyA',
    windowsVirtualKeyCode: 65,
    nativeVirtualKeyCode: 65,
    modifiers: modifier
  }, sessionId);
  await transport.send('Input.dispatchKeyEvent', {
    type: 'keyDown',
    key: 'Backspace',
    code: 'Backspace',
    windowsVirtualKeyCode: 8,
    nativeVirtualKeyCode: 8
  }, sessionId);
  await transport.send('Input.dispatchKeyEvent', {
    type: 'keyUp',
    key: 'Backspace',
    code: 'Backspace',
    windowsVirtualKeyCode: 8,
    nativeVirtualKeyCode: 8
  }, sessionId);
}
