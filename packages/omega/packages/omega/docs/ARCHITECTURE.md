# Architecture

## Planes

1. **Mission plane** registers objectives, constraints, authority and acceptance criteria.
2. **SDIA plane** resolves ambiguity, assumptions and evidence readiness.
3. **Deliberation plane** runs isolated advisers, cross-examination and Chair synthesis.
4. **Authority plane** implements Captain's Gate and fail-closed state transitions.
5. **Execution plane** dispatches stable domain plugin contracts.
6. **Verification plane** checks authority, contracts and release readiness.
7. **Witness plane** hash-chains all material events.

The control plane is intentionally separate from domain packages. Model providers and delivery tools can change without changing mission, evidence, authority or audit contracts.

## Reliability boundary

The reference runtime is deterministic and local. It demonstrates orchestration, controls and artefact contracts. It does not prove production availability, factual correctness of arbitrary model outputs, or safety under all adversarial conditions. Those require deployment-specific tests and operational controls.
