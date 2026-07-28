# Verification Record

Verified on Node.js v22.16.0 on 27 July 2026.

Commands executed successfully:

```bash
npm run lint
npm run test
npm run build
npm run demo
```

Results:

- syntax checks passed
- 3 of 3 automated tests passed
- distributable build generated
- end-to-end demo created a project, routed a shot, completed a deterministic mock render, registered the asset, recorded approval and wrote a hash-linked witness chain

Production provider boundary:

The included generic HTTP adapter is executable but cannot be truthfully certified against proprietary platforms without authorised, current vendor API specifications and credentials. Mock mode is the default and provides complete local execution. Vendor onboarding requirements are defined in `docs/operations.md`.
