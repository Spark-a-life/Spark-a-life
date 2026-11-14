# Spark-a-life repository vision

**Status:** Proposal for Captain ratification  
**Date:** 14 November 2026 (Asia/Singapore)  
**Scope:** Revise, envision, and deliberate an implementable, future-proof, portable public hub

## 1. Situation

`Spark-a-life/Spark-a-life` is a GitHub profile repository. On `main` it currently holds only the default profile README. Three unfinished draft pull requests compete to redefine it:

| PR | Intent | Conflict with profile hub |
| --- | --- | --- |
| Estate front door + 7 packages | Monorepo staging for Forge, OS, Omega, execution, routing, domain overlays | Too heavy; profile README would become a product dump; multi-repo split never completed |
| AIOS v1.2.0-alpha | Docs-only opportunity-evaluation kernel + governed action schemas | Correct as a sibling kernel snapshot; merging to `main` replaces the profile README |
| Portfolio evaluation pack | Coordination playbook stacked on AIOS | Useful; still docs-only; explicitly must not base on `main` |

Separately, November positioning work produced a coherent practice spine that is not yet reflected in any repo layout:

- SOLVE Sensemaking Learning Repo (method teaching)
- Odette-style AI opportunity inquiry (professional deliverable pattern)
- WiseGen Grounded Pilot v0.1.2 + SID / Triple-Check (Captain Gate offline)
- EAA Connected Practice (domain transfer of the decision spine)

**Diagnosis:** the public repo was asked to be four things at once. Future-proof portability requires splitting jobs, not merging more trees onto `main`.

## 2. Objectives

Revise the hub so that it is:

1. **Implementable** — a new contributor can clone, read one map, and run at least one offline pack without secrets or subscriptions.
2. **Future-proof** — model vendors, harnesses (n8n, Claude Code, Cursor), and languages can change without rewriting the practice doctrine.
3. **Portable** — packs travel as checksummed directories or ZIPs; teaching fixtures never require the private estate.

## 3. Deliberation (options considered)

### Option A — Merge the monorepo to `main`

- **For:** One clone shows everything.
- **Against:** Profile README conflict; founder maintenance cost; contradicts SID “do not add an eighth parallel control”; unpublished split plan left packages stranded.
- **Verdict:** Reject for `main`. Keep MULTI_REPO_SETUP as the path for modules that already pass local tests.

### Option B — Merge AIOS docs tree to `main`

- **For:** Canonical governance text becomes visible.
- **Against:** README replacement; AIOS is a decision kernel, not a practice hub; still not a runtime.
- **Verdict:** Reject for `main`. Promote AIOS to a dedicated sibling repository (or private repo) with version pins from this hub.

### Option C — Leave `main` as empty profile forever

- **For:** No accidental overclaim.
- **Against:** Positioning work stays in chat uploads; no portable entry point; org looks unfinished.
- **Verdict:** Insufficient.

### Option D — Thin hub + portable packs + sibling kernels (recommended)

- **For:** Matches Captain Gate doctrine; lands Nov positioning; preserves AIOS and modules without polluting the profile; offline-first; admits estate later without forking witness authority.
- **Against:** Requires discipline not to dump new experiments into the hub; pack curation is ongoing work (founder-effort must be logged).
- **Verdict:** **Adopt.**

## 4. Target architecture

```text
Spark-a-life/Spark-a-life          PUBLIC HUB
├── README.md                      Profile + practice map
├── PACK_MANIFEST.json             Pack versions + SHA-256 pins
├── docs/architecture/             Vision, Captain Gate, ADRs
├── packs/
│   ├── solve-saap/                Method classroom
│   ├── connected-practice/        Reconcile → attest → decide
│   └── grounded-pilot/            Offline 5R Captain fixture
└── .github/                       Pages / release provenance only as needed

Sibling (public or private):
  aios/                            Four-layer evaluation + action lifecycle specs
  wisegen-forge/                   …
  wisegen-ape-intelligence-os/     …
  wisegen-ape-omega/               …
  wisegen-governed-execution/      …
  …

Private estate (never mirrored here):
  wisegen-witness, Beacon, hive envelopes, client corpora, unredacted briefs
```

### Mapping from positioning spine

| Positioning artefact | Hub destination | Estate fate |
| --- | --- | --- |
| Fine-tuned Odette / SOLVE prompt | Method patterns inside `solve-saap` + advanced assignment | TAIE may later ingest redacted inquiry templates |
| Odette Decision Brief | Exemplar under `docs/examples/` only if redacted / concept-case licensed | Not a client engagement record |
| WiseGen Grounded Pilot v0.1.2 | `packs/grounded-pilot` teaching GO | HOLD for witness/Beacon integration until SID D1–D5 ratified |
| EAA Connected Index + routine/offset records | `packs/connected-practice` | Synthetic fixtures only |
| AIOS v1.2 + ADRs | Sibling `aios` repo | Remains decision layer per ADR-001 |
| Seven staged packages | Sibling module repos | Release only after each module’s RELEASE_GATE |

## 5. Future-proofing mechanisms

1. **Truth separation as code contracts** — every pack exposes: inputs, statistical/implementation checks, Captain attestation field, decision enum (`advance` | `hold` | `escalate` | `deny`), next-action handoff.
2. **Evidence labels** — adopt `[V][S][O][I][H][Illus]` (or the five estate evidence states) in every public brief.
3. **Continue / Revise / Stop** — no pack ships without explicit thresholds.
4. **Zero-subscription baseline** — BM25 / static HTML / rules engines first; LLM and SaaS adapters optional and fail-closed.
5. **Single authority rule** — teaching `review_chain.jsonl` is a fixture; `wisegen-witness` remains the only estate backend when admitted.
6. **Harness-agnostic prompts** — SOLVE skill and system instructions are content; execution hosts are interchangeable.

## 6. Implementable milestones

| Milestone | Deliverable | Exit test |
| --- | --- | --- |
| **M0 Hub** | This vision + revised profile README + empty pack stubs + manifest | Clone communicates the practice without overclaim |
| **M1 Packs** | Populate three packs from ratified ZIPs with checksums | `python -m unittest` / browser fixtures / SOLVE facilitator dry-run |
| **M2 Kernel sibling** | AIOS tree moved off this repo’s draft branch into `aios` | Hub links by tagged version; profile README untouched |
| **M3 Module split** | Execute multi-repo publish for modules with green local suites | Each module has CI + provenance release workflow |
| **M4 Estate admit** | SID D1–D5 explicit; witness integration contract filled from real interfaces | Teaching PASS ≠ production PASS documented |

## 7. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Hub becomes a new monorepo by stealth | Pack size budget; refuse new top-level packages on this repo |
| Founder curation burden rises | Log prep / supervision / correction / maintenance before scale claims |
| Novelty or “first” language leaks into README | Novelty only inside dated briefs with search scope |
| Draft PRs confuse contributors | Close or retarget #1–#3 after this proposal is ratified |
| Licence collisions (e.g. noncommercial tools) | Documentation-only until legal reading; pin MIT/Apache modules only |

## 8. Recommendation

Ratify **Option D**. Treat this pull request as M0. Authorise M1 pack population only from checksummed sources already reviewed (SOLVE v0.1.0, WiseGen v0.1.2 candidate, EAA connected-index fixtures). Keep AIOS and the seven modules off `main`. Hold estate integration until Captain Gate decisions in `CAPTAIN_GATE.md` are signed.
