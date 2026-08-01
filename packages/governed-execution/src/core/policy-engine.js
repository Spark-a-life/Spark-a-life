import { getPath } from '../util/object.js';
import { ValidationError } from './errors.js';

const EFFECTS = new Set(['ALLOW', 'DENY', 'REQUIRE_APPROVAL', 'REQUIRE_STEP_UP']);

export class PolicyEngine {
  constructor(document) {
    if (!document || !Array.isArray(document.rules)) {
      throw new ValidationError('Policy document must contain a rules array.');
    }
    this.version = document.version ?? 'unversioned';
    this.defaultEffect = document.defaultEffect ?? 'DENY';
    this.rules = [...document.rules].sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0));
    if (!EFFECTS.has(this.defaultEffect)) {
      throw new ValidationError(`Invalid default policy effect: ${this.defaultEffect}`);
    }
  }

  evaluate(request) {
    for (const rule of this.rules) {
      if ((rule.all ?? []).every((condition) => evaluateCondition(request, condition))) {
        if (!EFFECTS.has(rule.effect)) {
          throw new ValidationError(`Invalid policy effect in rule ${rule.id}: ${rule.effect}`);
        }
        return {
          policyVersion: this.version,
          ruleId: rule.id,
          effect: rule.effect,
          reason: rule.reason ?? rule.description ?? 'Policy rule matched.',
          requiredApproverRole: rule.requiredApproverRole,
          approvalTtlSeconds: rule.approvalTtlSeconds
        };
      }
    }
    return {
      policyVersion: this.version,
      ruleId: 'default',
      effect: this.defaultEffect,
      reason: 'No explicit allow rule matched.'
    };
  }
}

export function evaluateCondition(source, condition) {
  const actual = getPath(source, condition.path);
  const expected = condition.value;
  switch (condition.operator) {
    case 'equals': return actual === expected;
    case 'notEquals': return actual !== expected;
    case 'in': return Array.isArray(expected) && expected.includes(actual);
    case 'contains': return Array.isArray(actual)
      ? actual.includes(expected)
      : typeof actual === 'string' && actual.includes(String(expected));
    case 'gt': return Number(actual) > Number(expected);
    case 'gte': return Number(actual) >= Number(expected);
    case 'lt': return Number(actual) < Number(expected);
    case 'lte': return Number(actual) <= Number(expected);
    case 'exists': return expected ? actual !== undefined : actual === undefined;
    case 'prefix': return typeof actual === 'string' && actual.startsWith(String(expected));
    default: throw new ValidationError(`Unsupported policy operator: ${condition.operator}`);
  }
}
