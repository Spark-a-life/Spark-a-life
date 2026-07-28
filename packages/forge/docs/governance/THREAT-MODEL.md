# Threat Model

The model is an untrusted executor. Everything below follows from that single premise.

## Assets

| Asset | Why it matters |
|---|---|
| The approval authority | Whoever holds it can ship anything |
| Constitutional policy | Whoever can amend it can grant themselves authority |
| The witness chain | Whoever can rewrite it can make anything unfalsifiable |
| Customer data in intake | Personal data under PDPA, often HR or clinical |
| Signing key | Whoever holds it can forge a release manifest |
| The generated system | It becomes production infrastructure at the customer |

## Adversaries

1. **The compromised model.** Producing output shaped by injected instructions in intake content.
2. **The overreaching agent.** Attempting actions beyond its contract, often plausibly framed as helpfulness.
3. **The malicious insider.** Holding legitimate credentials but not legitimate authority.
4. **The supply chain.** A dependency, template or connector carrying hostile code.
5. **The careless operator.** No malice, high blast radius.

The human principal's own compromise is out of scope and is addressed by organisational controls.

## Five layers, and what each stops

| Layer | Control | Test |
|---|---|---|
| Input | Intake is data, never instruction. Content is digested and stored, never executed | `PromptInjectionTests` |
| Tool | Deny by default, no direct filesystem or network, path traversal refused, refusals witnessed | `SandboxTests` |
| Credential | Secrets read from environment only, never written to artefacts or evidence | bundle secret scan |
| Identity | Scoped role identities, no assumption of another role's authority, no wildcard grants | `SeparationOfDutiesTests` |
| Context | Persisted context hashed into the chain, so a rug-pull between runs is detectable | witness verification |

## STRIDE on the platform

| Category | Threat | Mitigation | Residual |
|---|---|---|---|
| Spoofing | An agent claims the Captain's identity | Approval requires a decision record; agents cannot write it | low |
| Tampering | Evidence quietly rewritten | Hash chain with published verification | low, and detectable rather than prevented |
| Repudiation | An approver denies approving | Decision carries actor, time, rationale and digest, all witnessed | low |
| Information disclosure | Restricted fields leak into generated code or evidence | Classification travels; server-side masking; evidence stores references | medium |
| Denial of service | An agent loops and exhausts budget | Cost governor halts at cap; halt is a safe state | low |
| Elevation of privilege | An agent deploys without approval | Constitutional deny plus signed manifest requiring an approval reference | low |

## Known limitations, stated plainly

- **Local signing key.** Version 1 signs manifests with an HMAC key derived from the local environment. This detects accidental corruption and casual tampering. It does not withstand an attacker with host access. Substitute an organisational key or Cosign before institutional deployment.
- **Single-writer chain.** See `WITNESS-CHAIN.md`. Anchor the head externally for stronger guarantees.
- **Generated code is not formally verified.** It is compiled, tested, statically checked and adversarially probed. That is assurance, not proof.
- **Deterministic adapter is not a safety property.** It bounds variability; it does not make output correct.

Stating these is part of the control. A threat model that lists only what is solved is a brochure.
