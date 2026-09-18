# AIOS

**Organisation and Opportunity Intelligence with a specified Governed Action architecture**

Current repository version: **1.2.0-alpha**  
Status: **Docs-only governance snapshot. Private-repo-ready alpha after this alignment. Not a runtime. Not approved for production external execution.**

This branch places the AIOS source tree at the repository root. Merging it to `main` would replace the GitHub profile README currently on `main`. Do not merge unless that replacement is intended.

## What this snapshot is

A labelled design and governance snapshot for private use. Integrity of the original zip/bundle working tree was clean. This branch adds the v1.2 specification as canonical, archives v1.1, and aligns protocol, schemas, tests and docs so they do not contradict v1.2.

### Provenance of `governance/AIOS_v1.2.md`

The original uploaded file `AIOS v1.2.md` (1,886 lines, 63,543 bytes) was read in full during the publish-readiness review. It was not present on the repository agent VM used to create this branch (uploads were not copied across). The file in this tree is therefore a control-complete reconstruction from that review: quoted passages, the §27 / §30 / §31 field lists, the 16-step protocol map, and the packaged v1.1 kernel fragments, including the exact recovered §21–§23 text. It is canonical for derived files in this snapshot. If the Human Captain still holds the original 63,543-byte document, replace `governance/AIOS_v1.2.md` with that file (filename only may change) and re-check derived extracts against it.

`archive/superseded/AIOS_v1.1.md` likewise reconstructs the packaged 1.1 kernel. Sections 21–23 match the recovered original tail exactly. Sections 1–20 are reconstructed from the review description of that kernel.

## What is implemented here

Documents, JSON Schema envelopes, a draft OpenAPI path list with `$ref` bodies, sanitised fictional examples, markdown acceptance specifications, and a v1.2 system instruction.

## What is not implemented

- Action Gateway server
- identity service
- approval service
- Witness Chain store
- policy engine
- runnable tests
- any live host

Do not enable consequential external execution from this repository.

## Purpose

AIOS evaluates employment, executive, advisory, consulting, training, partnership and strategic opportunities using four evaluation layers:

1. Capability Fit
2. Context Fit
3. Opportunity Quality
4. Strategic Position

Layer 0 (initial boundary) and two assurance planes (epistemic; agent security) govern whether that reasoning is evidence-bearing, appropriately authorised and safely executable.

Version 1.2 specifies a governed operational path for external Actions without converting those Actions into independent decision makers. Governed Action is an operational stage, not a fifth evaluation layer.

## Governing flow

`Intent → AIOS Evaluation → Action Risk Classification → Proposal → Preflight → Human Authorisation where required → Execution Integrity Check → Action Gateway (when implemented) → Technical Receipt → Outcome Verification → Witness Chain → Learning`

## Authority

The Human Captain retains final decision rights over claims, disclosure, commitments, risk acceptance and consequential execution.

Possession of an API capability is not authority to use it. There is no self-authorisation. Tool output is untrusted evidence. Prohibited class cannot be executed.

## Canonical sources

1. `governance/AIOS_v1.2.md`
2. `governance/EXTERNAL_ACTION_PROTOCOL.md` (generated from §26; must not diverge)
3. `governance/EVIDENCE_GOVERNANCE_AND_WITNESS_CHAIN.md`
4. `governance/OUTPUT_SCHEMAS_AND_DECISION_REGISTERS.md`

Architecture documents explain implementation but do not silently supersede governing protocols. If a derived file disagrees with v1.2, v1.2 wins.

Superseded v1.1 kernel: `archive/superseded/AIOS_v1.1.md`.

## Repository layout

```text
governance/            Governing protocols, including canonical AIOS v1.2
architecture/          Design notes, risk model, state machine, threat model
architecture/adr/      Architecture Decision Records
actions/openapi/       Draft non-production Action Gateway OpenAPI schema
actions/schemas/       Machine-readable proposal, approval, Witness and receipt schemas
actions/examples/      Sanitised fictional JSON examples only
prompts/               v1.2 GPT instruction (Declared, not Enforced)
tests/regression/      v1.0 Custom-GPT prompt checks (not gateway tests)
tests/action-governance/ Markdown Omega acceptance specifications (not runnable)
tests/adversarial/     Markdown adversarial acceptance specifications (not runnable)
docs/deployment/       Release gate (all boxes unchecked)
archive/superseded/    AIOS v1.1 and the v1.0 system instruction
```

## Release discipline

The repository is the authoritative development and governance source.

`Repository → review → tagged release → deployment package → GPT configuration`

Do not edit deployed copies and later treat them as the source of truth.

## Production gate

Do not enable consequential external execution until all of the following are complete. They are not complete.

- privacy review;
- authority model review;
- threat model review;
- authentication and least-privilege design;
- approval-binding implementation;
- idempotency and reconciliation implementation;
- audit retention/minimisation policy;
- action-governance tests run against an implementation;
- adversarial tests run against an implementation;
- Human Captain release approval.

See `docs/deployment/RELEASE_GATE.md`. Every box is unchecked. That is correct.

## Tests

Markdown files under `tests/` are acceptance specifications and prompt checks. They are not a passing regression suite. They cannot pass without an implementation.

## Data boundary

Personal evidence, client records, CVs, opportunity corpora and per-opportunity confidential material are excluded. Do not add them. Fictional examples use `example.invalid` only.

The v1.2 prompt retains Dr William Siew / Spark-a-life identity because this is the spark-a-life repository.

## Licence

All rights reserved. See `LICENSE`. No licence is granted to use this snapshot for production external execution.
