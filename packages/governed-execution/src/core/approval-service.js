import { base64urlDecodeJson, base64urlEncodeJson, hmacSha256, randomId, sha256, timingSafeEqualHex } from '../security/crypto.js';
import { canonicalise } from '../util/object.js';
import { readJson, writeJsonAtomic } from '../util/fs.js';
import { ValidationError } from './errors.js';

export function actionDigest(request) {
  const boundAction = canonicalise({
    requestId: request.requestId,
    actor: request.actor,
    capabilityId: request.capabilityId,
    operation: request.operation,
    targetBaseUrl: request.targetBaseUrl,
    parameters: request.parameters,
    idempotencyKey: request.idempotencyKey
  });
  return sha256(boundAction);
}

export class ApprovalService {
  constructor({ key, storePath }) {
    if (!key || key.length < 32) {
      throw new ValidationError('APPROVAL_HMAC_KEY must contain at least 32 characters.');
    }
    this.key = key;
    this.storePath = storePath;
    this.consumeQueue = Promise.resolve();
  }

  async issue({ request, approver, requiredRole, ttlSeconds = 300 }) {
    if (!approver?.id || !Array.isArray(approver.roles)) {
      throw new ValidationError('Approver identity and roles are required.');
    }
    if (!approver.roles.includes(requiredRole)) {
      throw new ValidationError(`Approver lacks required role: ${requiredRole}`);
    }
    if (approver.id === request.actor.id) {
      throw new ValidationError('The requester cannot approve their own consequential action.');
    }
    const issuedAt = new Date();
    const expiresAt = new Date(issuedAt.getTime() + ttlSeconds * 1000);
    const payload = {
      version: 1,
      nonce: randomId('approval'),
      actionDigest: actionDigest(request),
      requestId: request.requestId,
      approver,
      requiredRole,
      issuedAt: issuedAt.toISOString(),
      expiresAt: expiresAt.toISOString()
    };
    const encoded = base64urlEncodeJson(payload);
    const signature = hmacSha256(this.key, encoded);
    return `${encoded}.${signature}`;
  }

  validateAndConsume({ token, request, requiredRole }) {
    const operation = this.consumeQueue.then(() => this.#validateAndConsume({ token, request, requiredRole }));
    this.consumeQueue = operation.catch(() => {});
    return operation;
  }

  async #validateAndConsume({ token, request, requiredRole }) {
    if (typeof token !== 'string' || !token.includes('.')) {
      throw new ValidationError('A valid bound approval token is required.');
    }
    const [encoded, signature, extra] = token.split('.');
    if (extra !== undefined) throw new ValidationError('Malformed approval token.');
    const expectedSignature = hmacSha256(this.key, encoded);
    if (!timingSafeEqualHex(signature, expectedSignature)) {
      throw new ValidationError('Approval token signature is invalid.');
    }
    const payload = base64urlDecodeJson(encoded);
    if (payload.version !== 1) throw new ValidationError('Unsupported approval token version.');
    if (payload.requiredRole !== requiredRole) throw new ValidationError('Approval role does not match policy.');
    if (payload.actionDigest !== actionDigest(request)) throw new ValidationError('Approval is not bound to this exact action.');
    if (Date.parse(payload.expiresAt) <= Date.now()) throw new ValidationError('Approval token has expired.');
    if (payload.approver.id === request.actor.id) throw new ValidationError('Self-approval is prohibited.');

    const used = await this.#readUsedNonces();
    if (used[payload.nonce]) throw new ValidationError('Approval token has already been consumed.');
    used[payload.nonce] = {
      requestId: request.requestId,
      consumedAt: new Date().toISOString(),
      approverId: payload.approver.id
    };
    await writeJsonAtomic(this.storePath, used);
    return payload;
  }

  async #readUsedNonces() {
    try {
      return await readJson(this.storePath);
    } catch (error) {
      if (error.code === 'ENOENT') return {};
      throw error;
    }
  }
}
