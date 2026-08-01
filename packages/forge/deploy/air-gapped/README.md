# Air-gapped

The estate that proves the sovereignty claim. Nothing here is a special build.

## Transfer

1. Export the repository and the portable bundle to removable media.
2. Verify digests on arrival against the SBOM.
3. Run `./scripts/bootstrap.sh`, which performs no network calls.
4. Run `make demo` and `make verify`.

## Model profile

`deterministic` only, or `ollama` against a locally held model. There is no third option inside the boundary, and the platform does not degrade when the hosted profile is unavailable: it simply produces lower-fidelity generation with identical governance.

## Verification without the platform

An auditor inside the boundary can verify any evidence chain with the twenty-line verifier published in `docs/governance/WITNESS-CHAIN.md` and implemented in `tests/acceptance/test_portability.py`. No platform access required.
