export class GovernedExecutionError extends Error {
  constructor(message, { code = 'EXECUTION_ERROR', retryable = false, details = {} } = {}) {
    super(message);
    this.name = 'GovernedExecutionError';
    this.code = code;
    this.retryable = retryable;
    this.details = details;
  }
}

export class ValidationError extends GovernedExecutionError {
  constructor(message, details = {}) {
    super(message, { code: 'VALIDATION_ERROR', retryable: false, details });
    this.name = 'ValidationError';
  }
}

export class PolicyDeniedError extends GovernedExecutionError {
  constructor(message, details = {}) {
    super(message, { code: 'POLICY_DENIED', retryable: false, details });
    this.name = 'PolicyDeniedError';
  }
}
