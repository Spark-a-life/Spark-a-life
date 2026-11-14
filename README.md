# Spark-a-life

**Control Meets Compassion** — AI-enabled consultancy delivery through governed practice, not raw tooling.

This repository is the **public practice hub**: a thin profile front door, a map of the method, and versioned portable packs that run offline. It is not a production Action Gateway, not the private estate, and not a monorepo of every module.

## Positioning in one line

> AI proposes. Evidence informs. Captains verify. Humans decide.

Statistical or implementation signals never become Expert Truth. A named Captain retains authority over commitments, disclosure, dietary/allergen-class decisions in domain work, and any external effect.

## Practice spine

| Stage | Pack | What you can do offline |
| --- | --- | --- |
| **Method** | `packs/solve-saap` | Run SOLVE sensemaking: separate facts from hypotheses; compare process-only vs AI; design a small test |
| **Decision demo** | `packs/connected-practice` | Reconcile synthetic evidence → attest → Advance / Hold / Escalate with a downloadable handoff |
| **Captain training** | `packs/grounded-pilot` | Index approved sources, draft a 5R review, practice human approval without live side effects |

Domain cases (fine dining inquiry, SME analytics coaching, and others) are **overlays** on this spine. They do not create parallel authority systems.

## What lives where

| Surface | Role |
| --- | --- |
| **This repo (`Spark-a-life/Spark-a-life`)** | Profile README, architecture docs, portable pack index |
| **Sibling module repos** | Publishable runtimes (Forge, Intelligence OS, Omega, execution, routing, domain overlays) |
| **AIOS sibling (planned)** | Opportunity-evaluation kernel: four layers + governed action lifecycle (docs/schemas until implemented) |
| **Private estate** | Authoritative witness, identity, client corpora — never mirrored here |

See [`docs/architecture/REPO_VISION.md`](docs/architecture/REPO_VISION.md) for the full deliberation and [`docs/architecture/CAPTAIN_GATE.md`](docs/architecture/CAPTAIN_GATE.md) for held decisions.

## Design principles

1. **One job per repo** — hub ≠ kernel ≠ modules ≠ private estate.
2. **Portable packs first** — stdlib Python / static HTML / checksummed fixtures before any subscription dependency.
3. **Captain Gate everywhere** — allow / hold / deny with recorded rationale; no self-authorisation.
4. **Process before AI** — if a matrix, rule, or reconciliation closes the gap, stop.
5. **Contracts over frameworks** — schemas and ADRs outlive vendors and harnesses.
6. **Admit, do not fork authority** — teaching review chains never become estate witness truth.

## Quick start (when packs are populated)

```sh
# Method classroom (any chat or paper)
open packs/solve-saap/README.md

# Connected Practice browser demo
open packs/connected-practice/index.html

# Grounded Pilot offline CLI (Python 3.10+, SQLite FTS5)
cd packs/grounded-pilot && python pilot.py index && python pilot.py check
```

Until pack directories are filled from ratified sources, treat this hub as **architecture + profile only**.

## Honest limits

- No consequential external execution is authorised from this repository.
- Pack PASS is not estate PASS.
- Novelty and readiness claims require dated search scope and Continue / Revise / Stop criteria.
- Draft historical branches that staged a seven-package monorepo or an AIOS tree at the repo root are **not** the target shape for `main`.

## Related public modules

See the [Spark-a-life organisation](https://github.com/Spark-a-life) for craft utilities (design quality, readability, integration screening, and related tools). Publishable WiseGen modules are intended as separate repositories once their local release gates pass.

---

Spark-a-life · APE Intelligence · Practice hub revision 2026-11-14
