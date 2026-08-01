import test from 'node:test';
import assert from 'node:assert/strict';
import { ExecutionStateMachine } from '../src/core/state-machine.js';

test('execution state machine enforces valid transitions', () => {
  const machine = new ExecutionStateMachine('request_state');
  machine.transition('POLICY_EVALUATED');
  machine.transition('AUTHORISED');
  machine.transition('EXECUTING');
  machine.transition('VERIFYING');
  machine.transition('SUCCEEDED');
  assert.equal(machine.state, 'SUCCEEDED');
  assert.throws(() => machine.transition('EXECUTING'), /Invalid execution-state transition/);
});
