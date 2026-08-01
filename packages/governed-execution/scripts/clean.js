import fs from 'node:fs/promises';
import path from 'node:path';

for (const directory of ['var/witness', 'var/approvals', 'var/state', 'var/browser-profiles']) {
  const absolute = path.resolve(directory);
  await fs.rm(absolute, { recursive: true, force: true });
  await fs.mkdir(absolute, { recursive: true });
  await fs.writeFile(path.join(absolute, '.gitkeep'), '');
}
console.log('Removed generated runtime state.');
