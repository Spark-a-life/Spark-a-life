/**
 * Zero-dependency JSON Schema subset validator.
 * Supports: type, properties, required, items, enum, minimum, maximum.
 * Sufficient for harness reference schemas. Not a full draft implementation:
 * extend deliberately, or substitute Ajv in environments where dependencies
 * are permitted.
 */

/** @returns {{ valid: boolean, errors: string[] }} */
export function validate(schema, value, path = '$') {
  const errors = [];
  check(schema, value, path, errors);
  return { valid: errors.length === 0, errors };
}

function typeOf(v) {
  if (v === null) return 'null';
  if (Array.isArray(v)) return 'array';
  const t = typeof v;
  if (t === 'number') return Number.isInteger(v) ? 'integer' : 'number';
  return t;
}

function typeMatches(expected, actual) {
  if (expected === actual) return true;
  if (expected === 'number' && actual === 'integer') return true;
  return false;
}

function check(schema, value, path, errors) {
  if (!schema || typeof schema !== 'object') return;

  if (schema.type) {
    const actual = typeOf(value);
    if (!typeMatches(schema.type, actual)) {
      errors.push(`${path}: expected ${schema.type}, got ${actual}`);
      return;
    }
  }

  if (schema.enum && !schema.enum.some((e) => deepEqual(e, value))) {
    errors.push(`${path}: value not in enum [${schema.enum.join(', ')}]`);
  }

  if (typeof value === 'number') {
    if (schema.minimum !== undefined && value < schema.minimum) {
      errors.push(`${path}: ${value} below minimum ${schema.minimum}`);
    }
    if (schema.maximum !== undefined && value > schema.maximum) {
      errors.push(`${path}: ${value} above maximum ${schema.maximum}`);
    }
  }

  if (schema.type === 'object' && value && typeof value === 'object' && !Array.isArray(value)) {
    for (const key of schema.required || []) {
      if (!(key in value)) errors.push(`${path}.${key}: required property missing`);
    }
    for (const [key, sub] of Object.entries(schema.properties || {})) {
      if (key in value) check(sub, value[key], `${path}.${key}`, errors);
    }
  }

  if (schema.type === 'array' && Array.isArray(value) && schema.items) {
    value.forEach((item, i) => check(schema.items, item, `${path}[${i}]`, errors));
  }
}

export function deepEqual(a, b) {
  if (a === b) return true;
  if (typeof a === 'number' && typeof b === 'number') return Math.abs(a - b) < 1e-9;
  if (typeof a !== 'object' || typeof b !== 'object' || a === null || b === null) return false;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  const ka = Object.keys(a);
  const kb = Object.keys(b);
  if (ka.length !== kb.length) return false;
  return ka.every((k) => deepEqual(a[k], b[k]));
}

/** Strict output test: bare JSON object, no fences, no preamble. */
export function isStrictJson(rawText) {
  const t = rawText.trim();
  return t.startsWith('{') && t.endsWith('}') && !t.includes('```');
}

/** Count scalar leaf nodes of a parsed JSON value. */
export function countLeafNodes(obj) {
  if (typeof obj !== 'object' || obj === null) return 1;
  const values = Array.isArray(obj) ? obj : Object.values(obj);
  if (values.length === 0) return 1;
  return values.reduce((n, v) => n + countLeafNodes(v), 0);
}
