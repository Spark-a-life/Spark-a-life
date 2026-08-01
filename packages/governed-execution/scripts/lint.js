import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';

const roots = ['src', 'scripts', 'test'];
const files = [];
for (const root of roots) await collect(path.resolve(root), files);

for (const file of files.filter((value) => value.endsWith('.js'))) {
  await run(process.execPath, ['--check', file]);
}
console.log(`Syntax checked ${files.filter((value) => value.endsWith('.js')).length} JavaScript files.`);

async function collect(directory, output) {
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) await collect(fullPath, output);
    else output.push(fullPath);
  }
}

function run(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: 'inherit' });
    child.once('exit', (code) => code === 0 ? resolve() : reject(new Error(`${command} exited with ${code}`)));
  });
}
