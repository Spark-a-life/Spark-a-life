# Data classes and trust boundaries

## Data classes

Portable enumeration for envelopes that cross adapters. Aligns with AIOS `data_classification` plus Salwise `FICTIONAL`.

| Class | Meaning | May leave the local host? | May be committed to this repository? |
| --- | --- | --- | --- |
| `FICTIONAL` | Invented training or fixture data, labelled as such | Yes, if still labelled fictional | Yes |
| `PUBLIC` | Already public, independently checkable | Yes | Yes, with provenance |
| `INTERNAL` | Practice material not for public profile `main` | Only to authorised private stores | Private-snapshot only |
| `CONFIDENTIAL` | Client, opportunity, or personal evidence | No, unless Layer 0 and Captain authorise a specific channel | No |
| `RESTRICTED` | Heightened access control | No, unless separately authorised | No |
| `REGULATED` | Legal or regulated personal data | No | No |

AIOS action-proposal schema currently enumerates `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`. A future schema revision may add `FICTIONAL` and `REGULATED`. Until then, fictional fixtures stay outside Action Proposal payloads, and regulated data stays out of the repository.

## What must stay local

- LM Studio models, weights, and live endpoints.
- Target-device hardware inventory that is more specific than this brief needs.
- Learner identity and any persistent tutor profile. The skill forbids claiming cross-platform memory; a portable Markdown log is user-exported, not a server store.
- Camera tracking, depth, plates, EXR sequences, and shot metadata.
- Client records, CVs, opportunity corpora, credentials, and `.env` values.
- ChatGPT personal library URLs (`account_id=personal`, `libfile_*`). They are provenance pointers, not secrets, and they are not portable.

## Trust boundaries

```text
[Human acceptance owner]
        |
        v
[Portfolio kernel: envelopes, classes, maturity, UntrustedEvidence]
        |
        +-- AIOS adapter (decision; Action class; Witness)     [Declared]
        +-- Salwise adapter (local task; SAL-Q; SaaP/PaP2)     [Declared; package Verified mechanically]
        +-- Tutor adapter (skill intents; rubric)              [Declared]
        +-- VFX adapter (media job spec)                       [Declared only; not vendored as a runtime]
        +-- Review-prompt adapter (sensemaking meta-prompt)    [Declared]

Host split that must be named on every run:
  orchestrator host  !=  local inference host  !=  DCC/artist workstation  !=  public git remote
```

Localhost belongs to the executor. A remote agent must not describe its own loopback as the owner's desktop.

## Boundary rules

1. No absence of a restriction is permission.
2. Fictional fixtures do not authorise live client work.
3. A checksum authenticates file identity, not factual truth, not approval.
4. Green read-only work on fictional data is the default for this pack.
5. Sending messages, quoting fees, publishing, GPU cluster submission, or Nuke ingestion of unverified AI plates is Red or Prohibited until a real control exists.
6. Secrets, unrestricted tokens, and unnecessary sensitive payloads must not be written into inventories, Witness notes, or tutor logs.
