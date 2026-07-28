import test from 'node:test';
import assert from 'node:assert/strict';
import { verifyPostconditions } from '../src/core/verifier.js';

const request = { parameters: { title: 'Expected', name: 'Will' } };

test('semantic postconditions pass only when all expected outcomes are observed', () => {
  const result = verifyPostconditions([
    { type: 'httpStatus', equals: 201 },
    { type: 'jsonPointerExists', pointer: '/id' },
    { type: 'jsonPointerEqualsFromRequest', pointer: '/title', requestPath: 'parameters.title' }
  ], {
    status: 201,
    body: { id: 'note_1', title: 'Expected' }
  }, request);
  assert.equal(result.verified, true);
});

test('semantic verification reports a mismatch rather than treating change as success', () => {
  const result = verifyPostconditions([
    { type: 'jsonPointerEquals', pointer: '/status', equals: 'ACCEPTED' }
  ], {
    body: { status: 'REJECTED' }
  }, request);
  assert.equal(result.verified, false);
  assert.equal(result.checks[0].actual, 'REJECTED');
});
