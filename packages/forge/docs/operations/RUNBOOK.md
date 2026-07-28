# Runbook

Day-two operation. Written for whoever is holding the pager, not for whoever built it.

## Health

```bash
forge doctor                      # interpreter, layout, policies, registry
forge verify --run <run>          # evidence integrity
```

`doctor` exits non-zero on any readiness failure and is the container healthcheck.

## Reading a run

```bash
forge gate --run <run>                    # the packet a reviewer sees
cat <run>/run-summary.json                # machine summary
cat <run>/evidence/witness.jsonl | wc -l  # chain length
```

Start with the gate packet. It is designed to be the first thing read, not the last.

## Common situations

**A run halted on budget.** Expected behaviour, not an incident. The halt is a safe state: no partial side effect, evidence intact. Decide whether the work is worth more budget; if so, raise the project cap deliberately and rerun. Do not raise caps inside a run.

**A quality gate failed.** The packet is not ready and cannot be approved. Read `evidence/evaluation.json` for the failing gate and its detail. Fix the specification or the generator, not the gate.

**Witness verification failed.** Treat as a security incident until disproved. Preserve the run directory unmodified, take a copy, and record the head digest. Determine whether the discrepancy is a code defect in the chain writer or an edit. Do not rerun over the top of it.

**A deployment must be reversed.** Retrieve the manifest from `releases/`, confirm the `rollback_release` target, apply the prior manifest, and record an incident. Target ten minutes.

**An agent is behaving oddly.** Check `tool.refused` and `authority.refused` entries first. Repeated refusals usually mean a contract mismatch, not a compromise: a role is being asked for work it was never granted.

## The kill switch

```bash
export FORGE_NETWORK=deny         # already the default
docker compose down               # stop the estate
```

There is no scenario where a running agent cannot be stopped by stopping the process. The platform holds no long-lived autonomous execution outside a run.

## Incident record

Every incident produces a record carrying: what was observed, when, which run and release, what was done, what evidence was preserved, what the residual risk is, and what changes to policy or specification are proposed. Proposed changes go through the Captain, not through the incident.

## What not to do

- Do not edit the witness chain. Ever. A corrected record is a new entry, not an amended one.
- Do not raise a budget cap mid-run to get past a halt.
- Do not approve a packet that is not ready by editing the evidence.
- Do not deploy from a workspace. Deploy from a manifest.
