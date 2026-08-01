import { hmacSha256, randomId, sha256, timingSafeEqualHex } from '../security/crypto.js';
import { canonicalJson } from '../util/object.js';
import { appendJsonLine, readJsonLines } from '../util/fs.js';
import { ValidationError } from './errors.js';

export class WitnessChain {
  constructor({ filePath, key, redact = (value) => value }) {
    if (!key || key.length < 32) {
      throw new ValidationError('WITNESS_HMAC_KEY must contain at least 32 characters.');
    }
    this.filePath = filePath;
    this.key = key;
    this.redact = redact;
    this.appendQueue = Promise.resolve();
  }

  append(eventType, payload, occurredAt = new Date().toISOString()) {
    const operation = this.appendQueue.then(() => this.#appendRecord(eventType, payload, occurredAt));
    this.appendQueue = operation.catch(() => {});
    return operation;
  }

  async #appendRecord(eventType, payload, occurredAt) {
    const records = await readJsonLines(this.filePath);
    const previous = records.at(-1);
    const unsigned = {
      recordId: randomId('witness'),
      sequence: records.length + 1,
      previousHash: previous?.recordHash ?? null,
      eventType,
      occurredAt,
      recordedAt: new Date().toISOString(),
      payload: this.redact(payload)
    };
    const recordHash = sha256(canonicalJson(unsigned));
    const signature = hmacSha256(this.key, recordHash);
    const record = { ...unsigned, recordHash, signature };
    await appendJsonLine(this.filePath, record);
    return record;
  }

  async verify() {
    await this.appendQueue;
    const records = await readJsonLines(this.filePath);
    let previousHash = null;
    for (let index = 0; index < records.length; index += 1) {
      const record = records[index];
      if (record.sequence !== index + 1) {
        return failure(index, 'Sequence is discontinuous.');
      }
      if (record.previousHash !== previousHash) {
        return failure(index, 'Previous-hash link is invalid.');
      }
      const { recordHash, signature, ...unsigned } = record;
      const expectedHash = sha256(canonicalJson(unsigned));
      if (recordHash !== expectedHash) {
        return failure(index, 'Record hash is invalid.');
      }
      const expectedSignature = hmacSha256(this.key, recordHash);
      if (!timingSafeEqualHex(signature, expectedSignature)) {
        return failure(index, 'Record signature is invalid.');
      }
      previousHash = recordHash;
    }
    return {
      valid: true,
      records: records.length,
      headHash: previousHash
    };
  }
}

function failure(index, reason) {
  return {
    valid: false,
    failingRecord: index + 1,
    reason
  };
}
