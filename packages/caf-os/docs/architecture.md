# Reference Architecture

```mermaid
flowchart TD
  H[Human Creative Director] --> V[Conversational Director]
  V --> P[Production Intelligence]
  P --> R[Capability Router]
  R --> K[Kling-style provider]
  R --> S[Seedance-style provider]
  R --> L[LoRA / local pipeline]
  R --> A[Avatar provider]
  R --> M[Mock provider]
  K --> AR[Asset Registry]
  S --> AR
  L --> AR
  A --> AR
  M --> AR
  AR --> Q[Media QA]
  Q --> G[Captain's Gate]
  G --> W[Witness Chain]
```

## Trust boundaries

- Human authority is external to the generation providers.
- Provider output is untrusted until registered and reviewed.
- Local writes are restricted to configured project roots.
- Rights records are mandatory for real likeness and cloned voice use.
- Release requires explicit approval events.
