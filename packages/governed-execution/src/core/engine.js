import { ExecutionStateMachine } from './state-machine.js';
import { verifyPostconditions } from './verifier.js';
import { actionDigest } from './approval-service.js';
import { GovernedExecutionError, ValidationError } from './errors.js';

export class GovernedExecutionEngine {
  constructor({ capabilityRegistry, policyEngine, approvalService, witnessChain, stateStore, adapters, runtimeConfig }) {
    this.capabilityRegistry = capabilityRegistry;
    this.policyEngine = policyEngine;
    this.approvalService = approvalService;
    this.witnessChain = witnessChain;
    this.stateStore = stateStore ?? { save: async () => {} };
    this.adapters = adapters;
    this.runtimeConfig = runtimeConfig;
  }

  async execute(request) {
    const machine = new ExecutionStateMachine(request.requestId ?? 'unvalidated');
    const startedAt = Date.now();
    try {
      const resolved = this.capabilityRegistry.resolve(request);
      await this.stateStore.save(machine.snapshot());
      await this.witnessChain.append('REQUEST_RECEIVED', {
        request: sanitisedRequest(request),
        capabilityRegistryVersion: resolved.registryVersion,
        state: machine.snapshot()
      });

      const decision = this.policyEngine.evaluate(request);
      await this.#transition(machine, 'POLICY_EVALUATED', { ruleId: decision.ruleId, effect: decision.effect });
      await this.witnessChain.append('POLICY_DECIDED', {
        requestId: request.requestId,
        actionDigest: actionDigest(request),
        decision,
        state: machine.snapshot()
      });

      if (decision.effect === 'DENY') {
        await this.#transition(machine, 'BLOCKED', { reason: decision.reason });
        await this.witnessChain.append('ACTION_BLOCKED', {
          requestId: request.requestId,
          decision,
          state: machine.snapshot()
        });
        return resultEnvelope(request, machine, startedAt, {
          disposition: 'BLOCKED',
          policyDecision: decision
        });
      }

      if (decision.effect === 'REQUIRE_STEP_UP') {
        await this.#transition(machine, 'STEP_UP_REQUIRED', { reason: decision.reason });
        await this.witnessChain.append('STEP_UP_REQUIRED', {
          requestId: request.requestId,
          decision,
          state: machine.snapshot()
        });
        return resultEnvelope(request, machine, startedAt, {
          disposition: 'STEP_UP_REQUIRED',
          policyDecision: decision
        });
      }

      let approval;
      if (decision.effect === 'REQUIRE_APPROVAL') {
        await this.#transition(machine, 'AWAITING_APPROVAL', { requiredRole: decision.requiredApproverRole });
        if (!request.approvalToken) {
          await this.witnessChain.append('APPROVAL_REQUIRED', {
            requestId: request.requestId,
            actionDigest: actionDigest(request),
            requiredApproverRole: decision.requiredApproverRole,
            expiresInSeconds: decision.approvalTtlSeconds,
            state: machine.snapshot()
          });
          return resultEnvelope(request, machine, startedAt, {
            disposition: 'AWAITING_APPROVAL',
            policyDecision: decision,
            actionDigest: actionDigest(request)
          });
        }
        approval = await this.approvalService.validateAndConsume({
          token: request.approvalToken,
          request,
          requiredRole: decision.requiredApproverRole
        });
        await this.#transition(machine, 'AUTHORISED', { approverId: approval.approver.id });
        await this.witnessChain.append('APPROVAL_CONSUMED', {
          requestId: request.requestId,
          actionDigest: approval.actionDigest,
          approver: approval.approver,
          requiredRole: approval.requiredRole,
          issuedAt: approval.issuedAt,
          expiresAt: approval.expiresAt,
          state: machine.snapshot()
        });
      } else {
        await this.#transition(machine, 'AUTHORISED', { ruleId: decision.ruleId });
      }

      const adapter = this.adapters.get(resolved.capability.adapter);
      const maxRetries = Math.min(
        resolved.operation.maxRetries ?? 0,
        this.runtimeConfig.maxRetries ?? 0
      );
      let adapterResult;
      let attempt = 0;
      while (true) {
        attempt += 1;
        await this.#transition(machine, 'EXECUTING', { attempt });
        await this.witnessChain.append('EXECUTION_STARTED', {
          requestId: request.requestId,
          capabilityId: request.capabilityId,
          operation: request.operation,
          adapter: resolved.capability.adapter,
          attempt,
          state: machine.snapshot()
        });
        try {
          adapterResult = await adapter.execute({
            request,
            capability: resolved.capability,
            operation: resolved.operation
          });
          break;
        } catch (error) {
          const retryable = error instanceof GovernedExecutionError && error.retryable;
          const canRetry = retryable && resolved.operation.idempotent && attempt <= maxRetries;
          await this.witnessChain.append('EXECUTION_ATTEMPT_FAILED', {
            requestId: request.requestId,
            attempt,
            error: serialiseError(error),
            canRetry
          });
          if (canRetry) {
            await this.#transition(machine, 'RETRY_PENDING', { reason: error.message, nextAttempt: attempt + 1 });
            await delay(Math.min(250 * (2 ** (attempt - 1)), 2000));
            continue;
          }
          await this.#transition(machine, 'FAILED', { reason: error.message });
          await this.witnessChain.append('EXECUTION_FAILED', {
            requestId: request.requestId,
            error: serialiseError(error),
            state: machine.snapshot()
          });
          return resultEnvelope(request, machine, startedAt, {
            disposition: 'FAILED',
            policyDecision: decision,
            error: serialiseError(error)
          });
        }
      }

      await this.#transition(machine, 'VERIFYING');
      const verification = verifyPostconditions(
        resolved.operation.postconditions ?? [],
        adapterResult,
        request
      );
      await this.witnessChain.append('OUTCOME_VERIFIED', {
        requestId: request.requestId,
        verification,
        result: adapterResult,
        state: machine.snapshot()
      });

      if (!verification.verified) {
        await this.#transition(machine, 'STATE_UNCERTAIN', { reason: 'One or more semantic postconditions failed.' });
        await this.witnessChain.append('STATE_UNCERTAIN', {
          requestId: request.requestId,
          verification,
          state: machine.snapshot()
        });
        return resultEnvelope(request, machine, startedAt, {
          disposition: 'STATE_UNCERTAIN',
          policyDecision: decision,
          verification,
          result: adapterResult
        });
      }

      await this.#transition(machine, 'SUCCEEDED');
      await this.witnessChain.append('ACTION_COMPLETED', {
        requestId: request.requestId,
        verification,
        state: machine.snapshot()
      });
      return resultEnvelope(request, machine, startedAt, {
        disposition: 'SUCCEEDED',
        policyDecision: decision,
        verification,
        result: adapterResult
      });
    } catch (error) {
      if (machine.state === 'RECEIVED') {
        await this.witnessChain.append('REQUEST_REJECTED', {
          request: sanitisedRequest(request),
          error: serialiseError(error)
        });
      }
      return resultEnvelope(request, machine, startedAt, {
        disposition: error instanceof ValidationError ? 'REJECTED' : 'FAILED',
        error: serialiseError(error)
      });
    }
  }

  async #transition(machine, next, details = {}) {
    machine.transition(next, details);
    await this.stateStore.save(machine.snapshot());
    return machine.state;
  }
}

function resultEnvelope(request, machine, startedAt, fields) {
  return {
    requestId: request.requestId,
    durationMs: Date.now() - startedAt,
    ...fields,
    execution: machine.snapshot()
  };
}

function sanitisedRequest(request) {
  if (!request || typeof request !== 'object') return request;
  const { approvalToken, ...safe } = request;
  return {
    ...safe,
    approvalTokenPresent: Boolean(approvalToken)
  };
}

function serialiseError(error) {
  return {
    name: error.name ?? 'Error',
    code: error.code ?? 'UNEXPECTED_ERROR',
    message: error.message ?? String(error),
    retryable: Boolean(error.retryable),
    details: error.details ?? {}
  };
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
