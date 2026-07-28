# Spark-a-life | APE Intelligence

**Control Meets Compassion — AI-enabled consultancy delivery.**

WiseGen is a governed AI operating architecture for organisations that need accountability. It converts human intent into auditable, policy-checked, human-gated pipelines — across any model, any platform, any orchestration harness.

---

## The Problem

Most organisations adopt AI as a tool. They need it as an **accountable work redesign**: decisions traced, evidence recorded, humans in the loop at every gate that matters.

## The Position

**The governed intermediary.** Not raw AI (no accountability). Not legacy BPM (no intelligence). The point where intelligence meets governance, where prompts become pipelines, and where organisations become capable of doing things they could not do before — with humans accountable for every outcome.

---

## The Estate

Seven modules. Two ecosystems. Zero vendor lock-in.

### Core

| Module | What It Does | Ecosystem | Status |
|--------|-------------|-----------|--------|
| [**WiseGen Forge**](packages/forge/) | Governed intent-to-system application factory | Python 3.10+ | v1.0.0 |
| [**APE Intelligence OS**](packages/ape-intelligence-os/) | Governance-native operating architecture — estates, lanes, witness chain | Node.js 20+ | v0.1.0 |
| [**APE Omega**](packages/omega/) | Multi-step governed mission engine with adviser councils | Python 3.10+ | v2.1.0 |

### Execution & Routing

| Module | What It Does | Ecosystem | Status |
|--------|-------------|-----------|--------|
| [**Governed Execution**](packages/governed-execution/) | Policy-checked, authorised, observable enterprise action control plane | Node.js 20+ | v1.0.0 |
| [**Routing Harness**](packages/routing-harness/) | Evidence-based multi-model benchmarking and certification | Node.js 20+ | v1.1.0 |

### Domain Overlays

| Module | What It Does | Ecosystem | Status |
|--------|-------------|-----------|--------|
| [**MAIE HRBP**](packages/maie-hrbp/) | HR demand intelligence and coverage model recommendation | Node.js 20+ | v0.1.0 |
| [**CAF-OS**](packages/caf-os/) | Conversational AI filmmaking operating system | Node.js 20+ | v1.0.0 |

### Documentation

| Document | Description |
|----------|-------------|
| [**Builder's Handbook**](docs/index.html) | From Prompt to Pipeline to Organisation — a builder's guide for non-developers |

---

## Design Principles

- **Captain Rule** — AI proposes, the human decides. Enforced in code, not in prose.
- **Harness-Agnostic** — Claude Code, Cowork, n8n, Make, Zapier, raw API, LangChain. The stack doesn't care.
- **Platform-Agnostic** — Cloud, browser, satellite, edge, air-gapped. Five deployment estates.
- **Model-Agnostic** — Claude, GPT, Gemini, Mistral, Llama, Qwen. The patterns outlast the products.
- **Zero-Dependency Where Possible** — Forge runs on Python stdlib alone. Most Node modules have no npm dependencies.
- **Witness Chain** — Append-only, hash-linked, tamper-evident evidence for every consequential decision.

---

## Quick Start

### Python modules (Forge, Omega)

```bash
cd packages/forge && make doctor && make demo
cd packages/omega && pip install -e ".[dev]" && pytest
```

### Node.js modules

```bash
cd packages/ape-intelligence-os && node --test
cd packages/governed-execution && npm test && npm run demo
cd packages/routing-harness && node --test
cd packages/maie-hrbp && node --test
cd packages/caf-os && npm test && npm run demo
```

---

## Distribution

| Channel | What Ships | Trust Mechanism |
|---------|-----------|-----------------|
| **GitHub Releases** | Versioned zip + SHA256SUMS | Sigstore keyless signing, SLSA L2 provenance |
| **PyPI** (planned) | `wisegen-forge`, `wisegen-ape-omega` | Trusted Publishing (OIDC), Sigstore attestations |
| **npm** (planned) | `@spark-a-life/*` scoped packages | Trusted Publishing (OIDC), `--provenance` flag |

---

## Repository Structure

This is the **estate front door** — the profile README and documentation hub. Each module is staged under `packages/` and designed for individual-repo distribution. See [`MULTI_REPO_SETUP.md`](MULTI_REPO_SETUP.md) for instructions on splitting to independent repositories.

---

<sub>Dr William Siew · Spark-a-life | APE Intelligence · July 2026</sub>
