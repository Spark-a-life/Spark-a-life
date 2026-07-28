# Portability

The output must remain operable when WiseGen Forge is removed. This is a design obligation with a test attached, not a marketing claim.

## The export contract

`forge export --run <run> --out bundle.zip` produces:

| Item | Contents |
|---|---|
| `source_code` | The generated application, every candidate |
| `infrastructure_as_code` | Container recipe, compose file, estate manifests |
| `agent_definitions` | The role contracts that produced it |
| `policy_definitions` | The policies that bound it |
| `database_migrations` | Schema and forward or backward migration path |
| `evaluation_records` | Every quality gate result |
| `provenance_history` | The full witness chain |
| `environment_manifest` | Interpreter and platform the run assumed |
| `deployment_runbook` | How to ship and how to reverse |
| `software_bill_of_materials` | What the system is made of |
| `model_substitution_instructions` | How to change model provider without changing behaviour |

## The exit test

Automated in `tests/acceptance/test_portability.py`:

1. Run the full pipeline and export the bundle.
2. Extract it outside the repository.
3. Run the generated application's own test suite in a subprocess with `PYTHONPATH` emptied.
4. Prove, in a second test, that `import wisegen_forge` genuinely fails in that environment, so the first test is not passing by accident.
5. Verify the witness chain with a verifier that imports nothing from the platform.
6. Prove that verifier rejects a tampered chain.

Steps 4 and 6 exist because an exit test that cannot fail proves nothing.

## Model substitution

The specification, the policy decisions, the witness chain, the gate packet shape and the generated application's behaviour under test are all unchanged when the model changes. Only fidelity changes. Substitution is a `ModelSpec` entry declaring capability class, maximum approved risk tier, and cost per thousand tokens in SGD.

## What portability does not promise

The bundle carries the system as it was when exported. It does not carry the factory's ability to regenerate that system from a changed specification, which is the platform's actual product. A customer who exports owns what they built. A customer who stays gets governed regeneration when regulation, dependencies or requirements change.

That distinction is the honest commercial position, and it is better than captivity in both directions: it means the platform has to keep earning the relationship.
