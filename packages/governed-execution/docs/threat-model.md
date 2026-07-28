# Threat Model

## Scope

This threat model covers the local control API, policy engine, approval service, capability registry, HTTP adapter, Chromium CDP-pipe adapter and Witness Chain.

## Protected assets

- authority to invoke enterprise tools
- approval tokens and signing keys
- target-system credentials and sessions
- action parameters and business data
- evidence records and provenance
- policy and capability definitions
- execution state and idempotency keys

## Principal threats and controls

| Threat | Example | Implemented control | Residual risk |
|---|---|---|---|
| Unauthorised tool use | Actor invokes finance capability | Role entitlement and default-deny policy | Role claims must come from a trusted identity provider in production |
| Parameter smuggling | Request adds `adminOverride` | Per-operation parameter allowlist | Nested parameter schemas require organisation-specific validation |
| Approval substitution | Token used for a different amount | Exact-action digest binding | Compromised approval signing key permits token forgery |
| Approval replay | Same token used twice | Persistent nonce consumption | Multi-instance deployments need a transactional shared store |
| Self-approval | Requester approves own action | Identity comparison and required role | Identity federation must prevent aliases and duplicate identities |
| Unsafe retry | Payment repeated after timeout | Idempotent capability flag and shared idempotency key | Target system must honour idempotency correctly |
| False success | Interface changed but transaction failed | Semantic postconditions | Verification sources may themselves be stale or compromised |
| Browser-profile theft | Agent attaches to personal session | Fresh temporary profile and pipe transport | Real authentication still requires secure delegated identity design |
| Debug port exposure | CDP port reachable over network | `--remote-debugging-pipe`, no TCP endpoint | Browser binary and host remain within the platform trust boundary |
| Arbitrary script execution | Model supplies JavaScript | Fixed adapter implementation and configured selectors | Capability maintainers can still introduce unsafe selectors or plans |
| Evidence tampering | Log line changed after execution | Hash chain and HMAC signatures | HMAC is symmetric and does not provide external non-repudiation |
| Sensitive-data leakage | Token appears in evidence | Recursive redaction and string limits | Content-based secrets not named by a sensitive key may remain |
| Policy rollback | Older permissive rules reintroduced | Policy version in evidence and source control | Runtime does not yet require signed policy bundles |
| Denial of service | Large or repeated API requests | Body limit, timeout and local rate limit | In-memory rate limiting is not distributed |

## Browser-specific assumptions

- Chrome or Chromium is trusted and patched by the operator.
- The browser runs on a controlled host.
- Selectors and plans are reviewed as code.
- Authentication boundaries are respected. MFA is not automated around or bypassed.
- Persisted personal browser state is not used.

## Production hardening priorities

1. Connect actor identity to an enterprise identity provider and verify signed claims.
2. Store keys in an HSM or managed secrets service.
3. Replace file-based nonce storage with a transactional shared database.
4. Send evidence to an independent write-once or append-only store.
5. Sign policy and capability bundles and enforce deployment provenance.
6. Add data classification, field-level schema validation and DLP controls.
7. Add distributed rate limiting, tracing, metrics and alerting.
8. Conduct adversarial testing for prompt injection, tool poisoning and confused-deputy scenarios.
9. Establish incident response, key rotation and evidence-retention procedures.
