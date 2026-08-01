import path from 'node:path';
import fs from 'node:fs/promises';
import { writeJsonAtomic, readJson } from '../util/fs.js';
import { ValidationError } from './errors.js';

export class FileStateStore {
  constructor({ directory }) {
    this.directory = directory;
  }

  async save(snapshot) {
    validateRequestId(snapshot.requestId);
    await writeJsonAtomic(this.#path(snapshot.requestId), snapshot);
    return snapshot;
  }

  async get(requestId) {
    validateRequestId(requestId);
    try {
      return await readJson(this.#path(requestId));
    } catch (error) {
      if (error.code === 'ENOENT') return null;
      throw error;
    }
  }

  async remove(requestId) {
    validateRequestId(requestId);
    await fs.rm(this.#path(requestId), { force: true });
  }

  #path(requestId) {
    return path.join(this.directory, `${requestId}.json`);
  }
}

function validateRequestId(requestId) {
  if (typeof requestId !== 'string' || !/^[A-Za-z0-9._-]{8,128}$/.test(requestId)) {
    throw new ValidationError('requestId contains characters that are unsafe for durable state storage.');
  }
}
