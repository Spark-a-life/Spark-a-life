# Changelog

## v1.1.0 (2026-07-28)

Supersedes the v1.0 Model Routing and Benchmarking Playbook harness.

### Changed
- Mock provider quarantined: all mock results carry `certifiable: false` and are blocked from the production routing matrix by the `certify_from_mock_evidence` guard.
- Structured outputs requested per provider (Anthropic forced tool use, OpenAI-compatible `json_schema`) rather than measured as a model differentiator.
- Token Efficiency Index replaced by cost per validated node: output tokens only, weighted by per-provider pricing, denominated in schema-validated nodes from compliant trials.
- One-strike disqualification replaced by a compliance rate threshold over repeated trials.
- `worker_threads` replaced by a bounded promise pool.

### Added
- Semantic accuracy scoring against an expert-validated reference dataset.
- Append-only hash-linked Witness Chain for every routing decision.
- Task-class routing matrix (`extraction`, `interactive`, `build`) with a Codex-class candidate.
- Delegated build lane: routing intent recorded, certification deferred to the Build Lifecycle Orchestrator.
- Certification guards, config advisories, and a 10-test suite.
