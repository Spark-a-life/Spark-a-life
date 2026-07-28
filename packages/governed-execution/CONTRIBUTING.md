# Contributing

## Change discipline

Every change to an adapter, capability, policy, verifier or evidence record must include:

1. A clear operating purpose
2. Positive and negative tests
3. Failure and partial-completion analysis
4. Security and data-protection impact
5. Documentation updates
6. A backwards-compatibility assessment

## Pull-request gate

Run:

```bash
npm run check
npm run test:browser
```

A policy change must show which rule has precedence and why. A browser change must show how selectors, origins, profiles and authentication state remain constrained. A verifier change must include a test proving that an incorrect outcome fails.

## Coding conventions

- Use Node.js built-ins where practical.
- Use ESM modules and two-space indentation.
- Prefer explicit types and result objects over implicit booleans.
- Fail closed on unknown capability, policy, adapter and postcondition types.
- Do not log raw approval tokens, credentials or browser state.
- Use UK English in documentation.
