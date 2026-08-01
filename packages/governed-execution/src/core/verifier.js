import { getPath, jsonPointerGet, deepInterpolate } from '../util/object.js';
import { ValidationError } from './errors.js';

export function verifyPostconditions(postconditions, result, request) {
  const checks = postconditions.map((condition) => evaluatePostcondition(condition, result, request));
  return {
    verified: checks.every((check) => check.passed),
    checks
  };
}

export function evaluatePostcondition(condition, result, request) {
  let actual;
  let expected;
  let passed = false;
  switch (condition.type) {
    case 'httpStatus':
      actual = result.status;
      expected = condition.equals;
      passed = actual === expected;
      break;
    case 'jsonPointerExists':
      actual = jsonPointerGet(result.body, condition.pointer);
      expected = 'defined';
      passed = actual !== undefined;
      break;
    case 'jsonPointerEquals':
      actual = jsonPointerGet(result.body, condition.pointer);
      expected = condition.equals;
      passed = actual === expected;
      break;
    case 'jsonPointerEqualsFromRequest':
      actual = jsonPointerGet(result.body, condition.pointer);
      expected = getPath(request, condition.requestPath);
      passed = actual === expected;
      break;
    case 'urlPrefix':
      actual = result.finalUrl;
      expected = deepInterpolate(condition.value, { ...process.env, parameters: request.parameters });
      passed = typeof actual === 'string' && actual.startsWith(expected);
      break;
    case 'observationEquals':
      actual = result.observations?.[condition.observation];
      expected = condition.equals;
      passed = actual === expected;
      break;
    case 'observationEqualsTemplate':
      actual = result.observations?.[condition.observation];
      expected = deepInterpolate(condition.template, { parameters: request.parameters });
      passed = actual === expected;
      break;
    default:
      throw new ValidationError(`Unsupported postcondition type: ${condition.type}`);
  }
  return {
    type: condition.type,
    passed,
    actual,
    expected
  };
}
