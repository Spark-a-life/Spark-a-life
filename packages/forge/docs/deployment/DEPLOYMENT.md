# Deployment

## Four estates, one artefact

| Estate | Use when | Command |
|---|---|---|
| Local workstation | Development, demonstration, sovereign single-user work | `make demo` |
| Docker | Reproducible local or single-host institutional runs | `docker compose up` |
| Kubernetes | Institutional deployment with scaling and rotation | `kubectl apply -k deploy/kubernetes` |
| Customer VPC | Data residency and sovereignty requirements dominate | `deploy/customer-vpc/README.md` |
| Air-gapped | No egress permitted at all | `deploy/air-gapped/README.md` |

The same portable bundle serves all five. Nothing is estate-specific except the infrastructure wrapper.

## Non-negotiables in every estate

1. **Egress denied by default.** `FORGE_NETWORK=deny`. Enabling network access is a policy change, recorded, not a flag someone flips.
2. **Non-root execution.** The container runs as uid 10001 with `no-new-privileges`.
3. **Signed manifests.** Deployment applies a manifest, never a conversational instruction.
4. **Named rollback.** A release with no reversal target is refused unless it is a genuine first release, and it must say so.
5. **Evidence travels.** The evidence bundle reference is part of the manifest, not an attachment.

## Release procedure

```bash
./scripts/verify-release.sh        # the gate: doctor, tests, demo, verify, export, licence, changelog
git tag -a v1.0.0 -m "..."         # only after the gate passes
git push origin v1.0.0             # release workflow crafts bundle and SBOM
```

The gate passing is necessary, not sufficient. Captain sign-off is still required, and the release workflow does not deploy.

## Rollback

```bash
forge gate --run <run> --show                     # confirm what shipped
# apply the prior release manifest from releases/
```

Target time to reverse is ten minutes. If a change cannot be reversed within that window, it needed a different deployment strategy, not a faster runbook.

## Data residency

Default residency is Singapore unless the customer specifies otherwise. Residency is recorded in the architecture plan at stage 3, carried into the manifest, and is part of what the Captain approves. It is not an operational detail discovered at deployment time.

## Model estates

| Profile | Adapter | Network | Use |
|---|---|---|---|
| `deterministic` | built in | none | default, CI, air-gapped, reproducibility tests |
| `ollama` | local runtime | localhost only | sovereign estates wanting model fidelity without egress |
| `anthropic` | hosted API | allow-listed egress | highest fidelity, where policy permits egress |

Changing the profile changes fidelity. It does not change control flow, policy evaluation, evidence capture or the gate. That separation is the point of `ADR-0002`.
