import { isPlainObject } from '../util/object.js';

const DEFAULT_SENSITIVE = [
  'authorization',
  'cookie',
  'set-cookie',
  'password',
  'secret',
  'token',
  'accesstoken',
  'refreshtoken',
  'apikey'
];

export function createRedactor(options = {}) {
  const sensitiveKeys = new Set(
    (options.sensitiveKeys ?? DEFAULT_SENSITIVE).map((key) => String(key).toLowerCase())
  );
  const maxStringLength = options.maxStringLength ?? 2048;

  function redact(value, keyHint = '') {
    if (sensitiveKeys.has(String(keyHint).toLowerCase())) {
      return '[REDACTED]';
    }
    if (typeof value === 'string') {
      return value.length > maxStringLength
        ? `${value.slice(0, maxStringLength)}...[TRUNCATED]`
        : value;
    }
    if (Array.isArray(value)) {
      return value.map((item) => redact(item));
    }
    if (isPlainObject(value)) {
      return Object.fromEntries(
        Object.entries(value).map(([key, item]) => [key, redact(item, key)])
      );
    }
    return value;
  }

  return redact;
}
