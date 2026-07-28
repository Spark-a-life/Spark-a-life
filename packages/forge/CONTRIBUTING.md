# Contributing

## Ground rules

1. **The specification is authoritative.** Change the specification first, then the code. A pull request that changes behaviour without changing its specification or acceptance criteria will be rejected.
2. **Governance surfaces need the Captain.** Anything under `policies/constitutional/`, `agents/registry.yaml`, `src/wisegen_forge/witness.py`, `approval.py` or `policy.py` requires human sign-off. See `CODEOWNERS`.
3. **No new runtime dependencies.** The core runs on the Python standard library. Optional extras are permitted only behind a graceful fallback, as PyYAML is.
4. **Evidence with every claim.** "Works on my machine" is not evidence. Attach the run summary and witness head.

## Before opening a pull request

```bash
make doctor
make test
make demo
make verify
```

All four must pass. `make lint` and `make typecheck` are advisory and skip silently when the tools are absent.

## Adding a role

See `docs/agent-authoring/AGENT-CONTRACTS.md`. A role needs a distinct stance, a unique exit artefact, an expressible authority boundary and testable evidence requirements. Register it in `agents/registry.yaml` and add its authority tests under `tests/adversarial/`.

## Adding a policy

Policies live in `policies/<scope>/` and are evaluated in scope order: constitutional, organisational, project, data, security, deployment, model-routing, cost, retention. A deny at any scope is final; a later allow cannot overturn an earlier deny. Add the corresponding test in `tests/unit/test_policy.py`.

## Commit and branch conventions

- Branches: `role/<role-id>/<short-topic>`, for example `role/gaie.backend-engineer/schema-migrations`.
- Commits: imperative mood, one concern per commit, and the affected stage in the subject where relevant.
- Every commit that changes generated output must update `CHANGELOG.md`.

## Style

British and Singapore English. Avoid em dashes. Use "craft" rather than "draft" for content creation. Currency defaults to SGD.
