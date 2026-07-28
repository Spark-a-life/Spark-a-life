# Witness Chain

An append-only hash chain over every action, refusal and failure in a run. It exists so that a stranger, months later, without access to this platform, can establish what happened.

## The algorithm

Published in full, because a verification scheme that only the vendor can run is not evidence.

```
genesis      = "sha256:" + "0" * 64

payload_digest = sha256(canonical_json(payload))
entry_digest   = sha256(canonical_json({
                   seq, at, actor, event, payload_digest, prev_digest
                 }))
```

`canonical_json` is `json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)`. Digests are prefixed `sha256:`. Entries are stored one JSON object per line in `evidence/witness.jsonl`, in sequence order starting at 1.

## Verification

```bash
forge verify --run .forge/demo
```

Verification recomputes every payload digest and every entry digest, and checks that each entry's `prev_digest` equals its predecessor's `entry_digest`. This detects:

| Attack | Detected by |
|---|---|
| Rewriting a payload | payload digest mismatch |
| Deleting an entry | broken link and sequence gap |
| Reordering entries | broken link |
| Appending a forged entry | link mismatch at the join |
| Truncating the tail | head digest differs from the published head |

`tests/unit/test_core.py` proves each of these fails closed.

## Independent verification

`tests/acceptance/test_portability.py` contains a twenty-line verifier that imports nothing from this platform, and a second test proving that verifier rejects a tampered chain. An auditor can copy that function. That is the point.

## What the chain is not

It is not a blockchain, and it makes no distributed-consensus claim. A party holding both the chain and write access to it can rewrite it wholesale. The chain defends against selective, silent edits, which is the realistic failure mode: an agent or an operator quietly adjusting one record. For stronger guarantees, anchor the head externally, which is what the estate's `wisegen-witness` cross-anchoring exists for. Record the head digest at release time in a system the run cannot write to.

## Recording discipline

Three rules keep the chain honest.

1. **Refusals are recorded.** A denied tool call, a policy refusal, an authority refusal and a budget halt all produce entries. A trail of successes only is a marketing artefact.
2. **Failures are recorded.** Handler exceptions are witnessed as `tool.failed` before they propagate.
3. **Secrets are never recorded.** Payloads carry references, digests and summaries. Credentials, personal data payloads and full file contents stay out. `tests/acceptance` scans the exported bundle for secret material.
