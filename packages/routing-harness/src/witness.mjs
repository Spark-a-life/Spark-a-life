/**
 * Append-only, hash-linked Witness Chain.
 * Pattern-compatible with the APE Intelligence OS chain: each record carries
 * prev_hash and hash = sha256(prev_hash + canonical(record body)).
 */
import { createHash } from 'node:crypto';
import * as fs from 'node:fs';
import * as path from 'node:path';

const GENESIS = 'wisegen-routing-harness-genesis';

function canonical(obj) {
  if (obj === null || typeof obj !== 'object') return JSON.stringify(obj);
  if (Array.isArray(obj)) return `[${obj.map(canonical).join(',')}]`;
  return `{${Object.keys(obj).sort().map((k) => `${JSON.stringify(k)}:${canonical(obj[k])}`).join(',')}}`;
}

export class WitnessChain {
  constructor(filePath) {
    this.filePath = filePath;
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
  }

  read() {
    if (!fs.existsSync(this.filePath)) return [];
    return fs.readFileSync(this.filePath, 'utf8')
      .split('\n')
      .filter(Boolean)
      .map((line) => JSON.parse(line));
  }

  append(actor, action, payload) {
    const records = this.read();
    const prevHash = records.length ? records[records.length - 1].hash : GENESIS;
    const body = {
      index: records.length,
      timestamp: new Date().toISOString(),
      actor,
      action,
      estate: 'GAIE',
      payload,
      prev_hash: prevHash
    };
    const record = { ...body, hash: sha256(prevHash + canonical(body)) };
    fs.appendFileSync(this.filePath, JSON.stringify(record) + '\n', 'utf8');
    return record;
  }

  verify() {
    const records = this.read();
    let prevHash = GENESIS;
    for (const record of records) {
      const { hash, ...body } = record;
      if (body.prev_hash !== prevHash) {
        return { valid: false, at: record.index, reason: 'broken link' };
      }
      if (sha256(prevHash + canonical(body)) !== hash) {
        return { valid: false, at: record.index, reason: 'hash mismatch' };
      }
      prevHash = hash;
    }
    return { valid: true, length: records.length };
  }
}

function sha256(text) {
  return createHash('sha256').update(text, 'utf8').digest('hex');
}
