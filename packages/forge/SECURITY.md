# Security Policy

## Posture

WiseGen Forge treats the language model as an untrusted executor. Every capability is denied until a policy grants it, for a named role, for a named task, within a budget.

Five layers are validated on every run:

1. **Input** - intake is scanned for prompt injection, embedded instructions and re-identification risk before compilation.
2. **Tool** - the tool gateway mediates every external action. There is no direct filesystem, network or process access from an agent.
3. **Credential** - secrets are read from the environment, never persisted to artefacts, evidence or the witness chain. Evidence records reference identifiers, not payloads.
4. **Identity** - agents carry scoped identities. An agent cannot assume another agent's authority, and no agent can assume the Captain's.
5. **Context** - persisted context is hashed into the witness chain, so a rug-pull between runs is detectable rather than silent.

## Defaults

- Network is denied by default. The default model adapter is offline and deterministic.
- Generated code is executed only inside the run workspace, never against the repository.
- Constitutional policy is read-only at run time. Amendment requires a Captain decision recorded outside the run.
- Cost caps halt execution. A halted run is a safe state and produces a partial gate packet, not a silent continuation.

## Reporting a vulnerability

Report privately to the Captain. Do not open a public issue. Include reproduction steps, the run identifier if one exists, and the witness head. Acknowledgement within three working days.

## Out of scope

- Vulnerabilities in generated customer applications after the customer has modified them.
- Findings that require the Captain's signing authority to be compromised first. Compromise of the human principal is outside this threat model and is addressed by organisational controls.

## Compliance touchpoints

Singapore Personal Data Protection Act (data classification and retention), Singapore Model AI Governance Framework including the agentic AI update (human oversight and traceability), EU AI Act Article 14 (human oversight) where applicable. The platform supports compliance; it does not discharge the deploying organisation's obligations.
