import fs from 'node:fs/promises';
import path from 'node:path';
import { randomSecret } from '../src/security/crypto.js';

const envPath = path.resolve('.env');
const content = `RUNTIME_MODE=production
CONTROL_HOST=127.0.0.1
CONTROL_PORT=8787
CONTROL_API_KEY=${randomSecret(32)}
WITNESS_HMAC_KEY=${randomSecret(48)}
APPROVAL_HMAC_KEY=${randomSecret(48)}
WITNESS_LOG_PATH=var/witness/witness-chain.jsonl
APPROVAL_STORE_PATH=var/approvals/used-nonces.json
STATE_STORE_PATH=var/state
CHROMIUM_PATH=/usr/bin/chromium
TARGET_BASE_URL=http://127.0.0.1:8899
BROWSER_DEMO_ROOT=fixtures
BROWSER_DEMO_FILE=fixtures/browser-demo.html
`;

try {
  await fs.writeFile(envPath, content, { flag: 'wx', mode: 0o600 });
  console.log(`Created ${envPath} with mode 0600.`);
} catch (error) {
  if (error.code === 'EEXIST') {
    console.error('.env already exists. Delete or archive it before generating new keys.');
    process.exitCode = 1;
  } else {
    throw error;
  }
}
