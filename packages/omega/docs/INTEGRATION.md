# Integration contract

## Control flow

1. Load and validate the Omega mission.
2. Derive a bounded Intelligence OS action request.
3. Evaluate the request through Captain's Gate.
4. Stop on any decision other than `ALLOW`.
5. Execute the Omega state machine.
6. Write Omega's hash-linked audit records.
7. Preserve the derived request and final mission output for review.

## Lane mapping

| Omega domain | Intelligence estate |
|---|---|
| strategy | MAIE |
| market | TAIE |
| personal | PAIE |
| general | GAIE |
| shared | SAIE |

Unknown domains default to MAIE and remain subject to Captain's Gate.

## Authority rule

Omega's Captain decision is necessary but not sufficient. The Intelligence OS gate remains authoritative for runtime, capability, data classification, estate, risk, and side-effect controls.
