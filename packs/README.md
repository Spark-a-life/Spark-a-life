# Portable packs

Packs are the implementable unit of the Spark-a-life public hub.

Each pack must:

1. Run offline (or on paper) without API keys.
2. Declare its truth boundary (what is statistical / implementation vs Captain judgement).
3. Ship a README with Continue / Revise / Stop criteria.
4. Appear in `/PACK_MANIFEST.json` with a SHA-256 once populated.
5. Use synthetic or teaching fixtures only unless the Captain authorises otherwise.

| Pack | Role | Status |
| --- | --- | --- |
| [`solve-saap`](solve-saap/) | Method: SOLVE sensemaking classroom | Stub — awaiting G2 |
| [`connected-practice`](connected-practice/) | Decision demo: reconcile → attest → decide | Stub — awaiting G2 |
| [`grounded-pilot`](grounded-pilot/) | Captain training: offline 5R review | Stub — awaiting G2 |

Do not add a fourth pack until one of the first three has a ratified checksum and an exit test in CI or a documented manual protocol.
