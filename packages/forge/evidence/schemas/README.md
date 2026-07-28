# Evidence schemas

Published so an external auditor can validate a WiseGen Forge evidence bundle without access to this platform. The schemas are JSON Schema draft 2020-12 and describe exactly what the runtime writes.

| Schema | Written by | Where it lands in a run |
|---|---|---|
| `intake-record.schema.json` | Intent Compiler | `objects/intake.json` |
| `specification.schema.json` | Intent Compiler | `objects/specification.json` |
| `evaluation-report.schema.json` | Assurance Engineer | `evidence/evaluation.json` |
| `gate-packet.schema.json` | Gate Steward | `approvals/<id>.json` and `.md` |
| `release-manifest.schema.json` | Release Engineer | `releases/<release>.manifest.json` |
| `witness-entry.schema.json` | Every role | `evidence/witness.jsonl`, one entry per line |

`tests/contract/test_contracts.py` asserts that these schemas keep matching the runtime. If a field is added to an object without being described here, that test fails.
