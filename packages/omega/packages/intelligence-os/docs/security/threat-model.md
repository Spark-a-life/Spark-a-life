# Threat Model

## Protected assets

- Constitutional and policy configuration
- Estate boundaries
- Capability certifications
- Sensitive context and organisational knowledge
- Witness Chain integrity
- Human approval records

## Principal threats

1. Prompt or context injection that attempts to alter authority
2. Runtime self-escalation or unauthorised tool use
3. Sensitive-data overexposure
4. Capability substitution or version drift
5. Memory poisoning and unreviewed knowledge promotion
6. Witness record deletion, reordering or modification
7. External side effects without accountable approval
8. Cross-estate data leakage

## Baseline mitigations

- Fail-closed Captain's Gate
- Explicit runtime enablement
- Certified capability allow-lists
- Risk and data ceilings
- Human approval for medium and high risk
- No network access or external side effects in the baseline
- Hash-linked Witness Chain
- Separation between candidate memory and canonical knowledge
- Deterministic tests and CI

## Residual risks

The local Witness Chain is tamper-evident, not independently immutable. Production deployment should add signed records, append-only remote replication, key management, access control, encrypted storage and external time attestation.
