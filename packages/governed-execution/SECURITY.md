# Security Policy

## Supported version

Security fixes are applied to the current `1.x` line.

## Reporting a vulnerability

Do not open a public issue containing credentials, exploit details, personal data or evidence records. Report the issue privately to the repository owner through the organisation's established security contact channel.

A useful report includes:

- affected version and commit
- deployment mode and operating system
- minimal reproduction steps
- expected and observed behaviour
- security impact
- relevant logs with secrets removed
- suggested mitigation, where known

## Security assumptions

This reference implementation assumes:

- a trusted operating-system host
- one writer per Witness Chain file
- signing keys stored outside source control
- a private control-plane network boundary
- trusted capability and policy maintainers
- reviewed target-system contracts

## Non-goals

The repository does not provide:

- external non-repudiation
- distributed consensus
- a hardware security module
- enterprise identity federation
- a distributed approval datastore
- automatic compliance certification
- safe persistence of personal browser sessions

Review [Threat Model](docs/threat-model.md) before deployment.
