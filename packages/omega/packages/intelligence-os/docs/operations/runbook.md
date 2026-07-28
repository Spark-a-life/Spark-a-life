# Operations Runbook

## Preflight

```bash
node --version
node src/cli.mjs verify
node --test
```

## Run a governed workflow

```bash
node src/cli.mjs run examples/action-request.json examples/task.json
node src/cli.mjs witness
```

## Reset demonstration evidence

```bash
node src/cli.mjs reset
```

## Add a runtime

1. Add its definition to `config/runtimes.json` with `enabled: false`.
2. Implement a runtime adapter.
3. Register the adapter in the runtime factory.
4. Add runtime-specific tests and a threat assessment.
5. Declare permitted capabilities and data classes.
6. Obtain accountable approval.
7. Enable the runtime only after verification passes.

## Incident response

1. Disable the affected runtime or capability.
2. Preserve the Witness Chain and relevant host logs.
3. Stop external side effects.
4. Identify affected estates and data classes.
5. Reproduce the workflow using recorded inputs.
6. Record the incident, decision and remediation.
7. Re-enable only after re-evaluation and approval.
