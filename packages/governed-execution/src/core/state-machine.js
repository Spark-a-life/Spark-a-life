import { ValidationError } from './errors.js';

const TRANSITIONS = {
  RECEIVED: ['POLICY_EVALUATED'],
  POLICY_EVALUATED: ['AWAITING_APPROVAL', 'AUTHORISED', 'BLOCKED', 'STEP_UP_REQUIRED'],
  AWAITING_APPROVAL: ['AUTHORISED', 'BLOCKED'],
  AUTHORISED: ['EXECUTING'],
  EXECUTING: ['VERIFYING', 'RETRY_PENDING', 'FAILED'],
  RETRY_PENDING: ['EXECUTING', 'FAILED'],
  VERIFYING: ['SUCCEEDED', 'FAILED', 'STATE_UNCERTAIN'],
  STATE_UNCERTAIN: ['EXECUTING', 'ESCALATED', 'FAILED'],
  STEP_UP_REQUIRED: ['AUTHORISED', 'BLOCKED'],
  BLOCKED: [],
  ESCALATED: [],
  SUCCEEDED: [],
  FAILED: []
};

export class ExecutionStateMachine {
  constructor(requestId) {
    this.requestId = requestId;
    this.state = 'RECEIVED';
    this.history = [{ state: 'RECEIVED', at: new Date().toISOString() }];
  }

  transition(next, details = {}) {
    const allowed = TRANSITIONS[this.state] ?? [];
    if (!allowed.includes(next)) {
      throw new ValidationError(`Invalid execution-state transition: ${this.state} -> ${next}`, {
        requestId: this.requestId,
        currentState: this.state,
        requestedState: next
      });
    }
    this.state = next;
    this.history.push({ state: next, at: new Date().toISOString(), ...details });
    return this.state;
  }

  snapshot() {
    return {
      requestId: this.requestId,
      state: this.state,
      history: [...this.history]
    };
  }
}
