import fs from 'node:fs/promises';
import path from 'node:path';

export async function ensureParent(filePath) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
}

export async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, 'utf8'));
}

export async function writeJsonAtomic(filePath, value) {
  await ensureParent(filePath);
  const temporary = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  await fs.writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
  await fs.rename(temporary, filePath);
}

export async function appendJsonLine(filePath, value) {
  await ensureParent(filePath);
  await fs.appendFile(filePath, `${JSON.stringify(value)}\n`, { mode: 0o600 });
}

export async function readJsonLines(filePath) {
  try {
    const text = await fs.readFile(filePath, 'utf8');
    return text
      .split('\n')
      .filter(Boolean)
      .map((line, index) => {
        try {
          return JSON.parse(line);
        } catch (error) {
          throw new Error(`Invalid JSON at ${filePath}:${index + 1}: ${error.message}`);
        }
      });
  } catch (error) {
    if (error.code === 'ENOENT') return [];
    throw error;
  }
}

export async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}
