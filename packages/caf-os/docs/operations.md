# Operations Runbook

## Local assurance

```bash
npm ci
npm run verify
npm run demo
```

## API production posture

Run behind an authenticated reverse proxy. Restrict `CAF_PROJECT_ROOT` to a dedicated volume. Do not expose vendor API keys to clients. Use separate service accounts for generation and publishing. Back up project registries and witness logs. Send logs to an append-only or WORM-capable store for regulated deployments.

## Provider onboarding

1. Obtain documented and authorised API access.
2. Confirm submission, status, cancellation and output-download contracts.
3. Implement a provider-specific adapter conforming to `GenerationProvider`.
4. Add contract tests using recorded non-sensitive responses.
5. Add capability metadata and routing evidence.
6. Pass security, rights and cost controls before enabling production traffic.

## Release gates

- story and intent lock
- identity and consent approval
- audio master approval
- technical render review
- editorial lock
- accessibility and captions approval
- rights clearance
- export validation
- publication authorisation
