# Validation Report

## Release

- Repository: `wisegen-ape-governed-execution`
- Version: `1.0.0`
- Validation date: 28 July 2026
- Validation host: Linux container
- Node.js used for local validation: `v22.16.0`
- npm used for local validation: `10.9.2`
- Chromium used for browser validation: `144.0.7559.96`
- Declared runtime floor: Node.js 20

## Executed checks

### Static syntax check

```bash
npm run lint
```

Result: **Passed**. All JavaScript files were checked with `node --check`.

### Core and integration tests

```bash
npm test
```

Result: **Passed**.

- 22 tests discovered
- 21 passed
- 1 browser test intentionally skipped in the core suite
- 0 failed

Coverage includes:

- capability entitlement, parameter allowlists and parameter type constraints
- policy precedence and default-deny behaviour
- exact-action approval binding
- self-approval prevention
- approval replay prevention
- semantic outcome verification
- Witness Chain integrity and tamper detection
- durable execution-state persistence and path-traversal prevention
- HTTP adapter end-to-end operation
- authenticated control API and approval workflow

### Browser adapter test

```bash
npm run test:browser
```

Result: **Passed**.

The isolated Chromium adapter successfully:

- launched with a temporary non-default profile
- communicated over CDP pipe
- loaded an allowlisted local fixture
- resolved configured selectors
- inserted text through browser input
- clicked through CDP mouse events
- observed the expected semantic outcome
- removed the temporary profile after execution

### Full demonstration

```bash
npm run demo
```

Result: **Passed**.

Observed dispositions:

| Scenario | Expected | Observed |
|---|---|---|
| Low-consequence note | `SUCCEEDED` | `SUCCEEDED` |
| S$2,500 transfer before approval | `AWAITING_APPROVAL` | `AWAITING_APPROVAL` |
| S$2,500 transfer after bound approval | `SUCCEEDED` | `SUCCEEDED` |
| S$75,000 transfer | `BLOCKED` | `BLOCKED` |
| Governed browser form | `SUCCEEDED` | `SUCCEEDED` |

The generated Witness Chain contained 22 records and verified successfully.

## Packaging checks

- `package-lock.json` generated with zero external packages
- runtime state excluded from the release
- MIT licence included
- CycloneDX SBOM included
- OpenAPI description included
- architecture source register included
- infographic includes a functional QR code pointing readers to `docs/source-register.md`

## Validation boundaries

The local environment did not provide a Docker daemon, so the Docker image was not built during this validation run. The Dockerfile and Compose file were syntax-reviewed, and CI is configured to test Node.js 20 and 22 plus the Chromium browser adapter.

This report does not constitute security certification, legal approval or regulatory compliance. Real deployments require organisation-specific identity integration, secrets management, target-system assurance, data-protection review and operational acceptance.
