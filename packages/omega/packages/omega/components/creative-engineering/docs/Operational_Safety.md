# Operational Safety

This framework implements operational safety as deterministic engineering controls rather than agent self-policing.

## Controls

- Risk budgets: cost, tokens, runtime, retries and external calls.
- Circuit breaker states: GREEN, AMBER, RED and BLACK.
- Loop detection: repeated tool calls, repeated prompts and stalled progress.
- Credential scoping: capability tokens are issued only for permitted tools and expire automatically.
- Approval gates: high-risk channels and asset classes require explicit human approval.
- Incident records: safety events are written to the witness chain.

## Why this matters

Runaway loops can inflate token spend, misuse tools and create unsafe side effects. The framework assumes agents will optimise towards their objective and therefore limits their operating envelope before execution begins.
