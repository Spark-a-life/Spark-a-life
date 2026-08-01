import crypto from 'node:crypto';
import { canonicalJson } from '../util/object.js';

export function sha256(value) {
  const data = typeof value === 'string' ? value : canonicalJson(value);
  return crypto.createHash('sha256').update(data).digest('hex');
}

export function hmacSha256(key, value) {
  const data = typeof value === 'string' ? value : canonicalJson(value);
  return crypto.createHmac('sha256', key).update(data).digest('hex');
}

export function timingSafeEqualHex(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  return crypto.timingSafeEqual(Buffer.from(a, 'hex'), Buffer.from(b, 'hex'));
}

export function randomId(prefix = 'id') {
  return `${prefix}_${crypto.randomUUID()}`;
}

export function randomSecret(bytes = 32) {
  return crypto.randomBytes(bytes).toString('base64url');
}

export function base64urlEncodeJson(value) {
  return Buffer.from(canonicalJson(value), 'utf8').toString('base64url');
}

export function base64urlDecodeJson(value) {
  return JSON.parse(Buffer.from(value, 'base64url').toString('utf8'));
}
