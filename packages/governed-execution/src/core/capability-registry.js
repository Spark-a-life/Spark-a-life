import { deepInterpolate, assertNoExtraKeys } from '../util/object.js';
import { ValidationError } from './errors.js';
import { validateAgainstSchema } from './schema-validator.js';

export class CapabilityRegistry {
  constructor(document) {
    if (!document || !Array.isArray(document.capabilities)) {
      throw new ValidationError('Capability registry must contain a capabilities array.');
    }
    this.version = document.version ?? 'unversioned';
    this.capabilities = new Map();
    for (const capability of document.capabilities) {
      if (!capability.id || this.capabilities.has(capability.id)) {
        throw new ValidationError(`Capability identifier is missing or duplicated: ${capability.id}`);
      }
      this.capabilities.set(capability.id, capability);
    }
  }

  resolve(request) {
    validateBaseRequest(request);
    const capability = this.capabilities.get(request.capabilityId);
    if (!capability) {
      throw new ValidationError(`Unknown capability: ${request.capabilityId}`);
    }
    const operation = capability.operations?.[request.operation];
    if (!operation) {
      throw new ValidationError(`Unknown operation ${request.operation} for ${request.capabilityId}`);
    }
    const roles = new Set(request.actor.roles);
    if (!(capability.allowedRoles ?? []).some((role) => roles.has(role))) {
      throw new ValidationError('Actor is not entitled to invoke this capability.', {
        capabilityId: request.capabilityId,
        actorId: request.actor.id
      });
    }
    const allowedParameters = operation.parameterAllowlist ?? [];
    assertNoExtraKeys(request.parameters, allowedParameters, 'parameters');
    validateAgainstSchema(request.parameters, operation.parameterSchema, 'parameters');
    const variables = {
      ...process.env,
      parameters: request.parameters,
      request
    };
    const resolvedOperation = deepInterpolate(operation, variables);
    return {
      registryVersion: this.version,
      capability: { ...capability, operations: undefined },
      operation: resolvedOperation
    };
  }
}

export function validateBaseRequest(request) {
  if (!request || typeof request !== 'object') {
    throw new ValidationError('Action request must be an object.');
  }
  const allowed = [
    'requestId',
    'actor',
    'capabilityId',
    'operation',
    'targetBaseUrl',
    'parameters',
    'idempotencyKey',
    'approvalToken',
    'metadata'
  ];
  assertNoExtraKeys(request, allowed, 'action request');
  for (const field of ['requestId', 'capabilityId', 'operation', 'idempotencyKey']) {
    if (typeof request[field] !== 'string' || request[field].length < 1) {
      throw new ValidationError(`Missing or invalid field: ${field}`);
    }
  }
  if (request.requestId.length < 8 || request.idempotencyKey.length < 8) {
    throw new ValidationError('requestId and idempotencyKey must contain at least eight characters.');
  }
  if (!request.actor || typeof request.actor.id !== 'string' || !Array.isArray(request.actor.roles)) {
    throw new ValidationError('actor.id and actor.roles are required.');
  }
  if (!request.parameters || typeof request.parameters !== 'object' || Array.isArray(request.parameters)) {
    throw new ValidationError('parameters must be an object.');
  }
}
