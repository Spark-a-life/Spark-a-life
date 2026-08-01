# Release Checklist

## Code and tests

- [x] No external npm runtime dependencies
- [x] JavaScript syntax check passes
- [x] Core and integration tests pass
- [x] Browser adapter test passes
- [x] Complete demonstration passes
- [x] Durable state retrieval is tested
- [x] Witness Chain tamper detection is tested
- [x] Approval replay and self-approval are tested

## Governance

- [x] Default-deny policy is configured
- [x] Destructive operation is blocked
- [x] Consequential payment threshold requires independent approval
- [x] Approval is bound to the exact action and expires
- [x] Parameter allowlists are enforced
- [x] Semantic postconditions are explicit
- [x] Browser origins, files, selectors and observations are constrained

## Security

- [x] Demonstration credentials are rejected in production mode
- [x] Key-generation script creates restricted local credentials
- [x] Approval tokens are redacted from evidence
- [x] Sensitive-key redaction is configured
- [x] Browser uses a temporary non-default profile
- [x] Browser uses CDP pipe rather than a TCP debugging port
- [x] Runtime state directories are excluded from source control
- [x] Threat model and security policy are included

## Documentation and release assets

- [x] README and quick start
- [x] Architecture and governance model
- [x] Operator runbook
- [x] Adaptation guide
- [x] Control API documentation and OpenAPI file
- [x] Source register in APA 7 format
- [x] Publication infographic and design prompt
- [x] Architecture decision records
- [x] SBOM, licence and changelog
- [x] Validation report
