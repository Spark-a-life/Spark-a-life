import { ValidationError } from './errors.js';

export function validateAgainstSchema(value, schema, path = '$') {
  if (!schema) return;
  if (schema.enum && !schema.enum.some((candidate) => Object.is(candidate, value))) {
    fail(path, `must equal one of: ${schema.enum.map(String).join(', ')}`);
  }

  switch (schema.type) {
    case 'object':
      if (value === null || typeof value !== 'object' || Array.isArray(value)) fail(path, 'must be an object');
      for (const required of schema.required ?? []) {
        if (!Object.prototype.hasOwnProperty.call(value, required)) fail(`${path}.${required}`, 'is required');
      }
      for (const [key, item] of Object.entries(value)) {
        const propertySchema = schema.properties?.[key];
        if (!propertySchema) {
          if (schema.additionalProperties === false) fail(`${path}.${key}`, 'is not allowed');
          continue;
        }
        validateAgainstSchema(item, propertySchema, `${path}.${key}`);
      }
      break;
    case 'array':
      if (!Array.isArray(value)) fail(path, 'must be an array');
      if (schema.minItems !== undefined && value.length < schema.minItems) fail(path, `must contain at least ${schema.minItems} items`);
      if (schema.maxItems !== undefined && value.length > schema.maxItems) fail(path, `must contain at most ${schema.maxItems} items`);
      value.forEach((item, index) => validateAgainstSchema(item, schema.items, `${path}[${index}]`));
      break;
    case 'string':
      if (typeof value !== 'string') fail(path, 'must be a string');
      if (schema.minLength !== undefined && value.length < schema.minLength) fail(path, `must contain at least ${schema.minLength} characters`);
      if (schema.maxLength !== undefined && value.length > schema.maxLength) fail(path, `must contain at most ${schema.maxLength} characters`);
      if (schema.pattern && !new RegExp(schema.pattern).test(value)) fail(path, `must match ${schema.pattern}`);
      break;
    case 'number':
      if (typeof value !== 'number' || !Number.isFinite(value)) fail(path, 'must be a finite number');
      numericBounds(value, schema, path);
      break;
    case 'integer':
      if (!Number.isInteger(value)) fail(path, 'must be an integer');
      numericBounds(value, schema, path);
      break;
    case 'boolean':
      if (typeof value !== 'boolean') fail(path, 'must be a boolean');
      break;
    case undefined:
      break;
    default:
      throw new ValidationError(`Unsupported schema type at ${path}: ${schema.type}`);
  }
}

function numericBounds(value, schema, path) {
  if (schema.minimum !== undefined && value < schema.minimum) fail(path, `must be at least ${schema.minimum}`);
  if (schema.maximum !== undefined && value > schema.maximum) fail(path, `must be at most ${schema.maximum}`);
  if (schema.exclusiveMinimum !== undefined && value <= schema.exclusiveMinimum) fail(path, `must be greater than ${schema.exclusiveMinimum}`);
  if (schema.exclusiveMaximum !== undefined && value >= schema.exclusiveMaximum) fail(path, `must be less than ${schema.exclusiveMaximum}`);
}

function fail(path, message) {
  throw new ValidationError(`Schema validation failed: ${path} ${message}.`, { path, message });
}
