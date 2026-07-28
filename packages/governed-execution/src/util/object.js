export function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

export function canonicalise(value) {
  if (Array.isArray(value)) {
    return value.map(canonicalise);
  }
  if (isPlainObject(value)) {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalise(value[key])])
    );
  }
  return value;
}

export function canonicalJson(value) {
  return JSON.stringify(canonicalise(value));
}

export function getPath(source, path) {
  if (!path) return source;
  return path.split('.').reduce((current, segment) => {
    if (current === null || current === undefined) return undefined;
    return current[segment];
  }, source);
}

export function jsonPointerGet(source, pointer) {
  if (pointer === '') return source;
  if (!pointer.startsWith('/')) return undefined;
  return pointer
    .slice(1)
    .split('/')
    .map((part) => part.replace(/~1/g, '/').replace(/~0/g, '~'))
    .reduce((current, segment) => {
      if (current === null || current === undefined) return undefined;
      return current[segment];
    }, source);
}

export function deepInterpolate(value, variables, { preserveUnresolved = false } = {}) {
  if (typeof value === 'string') {
    return value.replace(/\$\{([^}]+)\}/g, (_, key) => {
      const resolved = getPath(variables, key) ?? process.env[key];
      if (resolved === undefined) {
        if (preserveUnresolved) return `\${${key}}`;
        throw new Error(`Missing interpolation variable: ${key}`);
      }
      return String(resolved);
    });
  }
  if (Array.isArray(value)) {
    return value.map((item) => deepInterpolate(item, variables, { preserveUnresolved }));
  }
  if (isPlainObject(value)) {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, deepInterpolate(item, variables, { preserveUnresolved })])
    );
  }
  return value;
}

export function selectKeys(source, allowedKeys) {
  const result = {};
  for (const key of allowedKeys) {
    if (Object.prototype.hasOwnProperty.call(source, key)) {
      result[key] = source[key];
    }
  }
  return result;
}

export function assertNoExtraKeys(source, allowedKeys, label = 'object') {
  const extras = Object.keys(source).filter((key) => !allowedKeys.includes(key));
  if (extras.length > 0) {
    throw new Error(`${label} contains unauthorised fields: ${extras.join(', ')}`);
  }
}
