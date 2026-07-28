import http from 'node:http';
import { randomUUID } from 'node:crypto';

export async function startDemoTarget({ host = '127.0.0.1', port = 0 } = {}) {
  const notesByIdempotencyKey = new Map();
  const transfersByIdempotencyKey = new Map();
  const server = http.createServer(async (request, response) => {
    try {
      const url = new URL(request.url, `http://${request.headers.host}`);
      if (request.method === 'GET' && url.pathname === '/health') {
        return sendJson(response, 200, { status: 'ok' });
      }
      if (request.method === 'GET' && url.pathname === '/browser-demo') {
        return sendHtml(response, browserDemoHtml());
      }
      if (request.method === 'POST' && url.pathname === '/api/notes') {
        const idempotencyKey = requireIdempotencyKey(request);
        if (notesByIdempotencyKey.has(idempotencyKey)) {
          return sendJson(response, 201, notesByIdempotencyKey.get(idempotencyKey));
        }
        const body = await readJsonBody(request);
        if (typeof body.title !== 'string' || typeof body.body !== 'string') {
          return sendJson(response, 400, { error: 'title and body are required' });
        }
        const note = {
          id: `note_${randomUUID()}`,
          title: body.title,
          body: body.body,
          createdAt: new Date().toISOString()
        };
        notesByIdempotencyKey.set(idempotencyKey, note);
        return sendJson(response, 201, note);
      }
      if (request.method === 'POST' && url.pathname === '/api/transfers') {
        const idempotencyKey = requireIdempotencyKey(request);
        if (transfersByIdempotencyKey.has(idempotencyKey)) {
          return sendJson(response, 201, transfersByIdempotencyKey.get(idempotencyKey));
        }
        const body = await readJsonBody(request);
        if (!Number.isFinite(body.amount) || body.amount <= 0 || body.currency !== 'SGD') {
          return sendJson(response, 400, { error: 'A positive SGD amount is required.' });
        }
        const transfer = {
          transactionId: `txn_${randomUUID()}`,
          status: 'ACCEPTED',
          amount: body.amount,
          currency: body.currency,
          beneficiary: body.beneficiary,
          purpose: body.purpose,
          acceptedAt: new Date().toISOString()
        };
        transfersByIdempotencyKey.set(idempotencyKey, transfer);
        return sendJson(response, 201, transfer);
      }
      if (request.method === 'DELETE' && url.pathname.startsWith('/api/accounts/')) {
        return sendJson(response, 501, { error: 'This route exists only to prove that policy blocks it before invocation.' });
      }
      return sendJson(response, 404, { error: 'not found' });
    } catch (error) {
      return sendJson(response, error.statusCode ?? 500, { error: error.message });
    }
  });

  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(port, host, resolve);
  });
  const address = server.address();
  const baseUrl = `http://${host}:${address.port}`;
  return {
    baseUrl,
    close: () => new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()))
  };
}

function requireIdempotencyKey(request) {
  const value = request.headers['idempotency-key'];
  if (typeof value !== 'string' || value.length < 8) {
    const error = new Error('idempotency-key header is required');
    error.statusCode = 400;
    throw error;
  }
  return value;
}

async function readJsonBody(request, limit = 1024 * 1024) {
  let size = 0;
  const chunks = [];
  for await (const chunk of request) {
    size += chunk.length;
    if (size > limit) {
      const error = new Error('request body too large');
      error.statusCode = 413;
      throw error;
    }
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
}

function sendJson(response, status, body) {
  const value = JSON.stringify(body);
  response.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(value),
    'cache-control': 'no-store'
  });
  response.end(value);
}

function sendHtml(response, body) {
  response.writeHead(200, {
    'content-type': 'text/html; charset=utf-8',
    'content-length': Buffer.byteLength(body),
    'content-security-policy': "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; object-src 'none'; base-uri 'none'",
    'cache-control': 'no-store'
  });
  response.end(body);
}

function browserDemoHtml() {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WiseGen Governed Browser Demo</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 40rem; margin: 4rem auto; padding: 0 1rem; }
    label, input, button, output { display: block; margin: 0.75rem 0; }
    input { padding: 0.6rem; width: 100%; box-sizing: border-box; }
    button { padding: 0.7rem 1rem; }
    output { font-weight: 700; }
  </style>
</head>
<body>
  <main>
    <h1>Governed Browser Adapter Demonstration</h1>
    <label for="name">Name</label>
    <input id="name" name="name" autocomplete="off">
    <button id="submit" type="button">Submit</button>
    <output id="status" aria-live="polite">Not submitted</output>
  </main>
  <script>
    document.querySelector('#submit').addEventListener('click', () => {
      const name = document.querySelector('#name').value.trim();
      document.querySelector('#status').textContent = name ? 'Submitted for ' + name : 'Name required';
    });
  </script>
</body>
</html>`;
}
