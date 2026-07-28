# ADR-0002: Isolated Chromium over CDP pipe

- Status: Accepted
- Date: 2026-07-28

## Context

A browser adapter is needed for authorised UI-mediated processes without exposing a remote-debugging TCP port or attaching to a user's normal browser profile.

## Decision

Launch a fresh Chrome or Chromium process per execution using `--remote-debugging-pipe` and a temporary non-default user-data directory. Use fixed capability selectors, CDP DOM geometry and CDP Input events. Delete the profile after execution.

## Consequences

- No debugging TCP listener
- Better session isolation and reproducibility
- Chromium-specific implementation
- Process startup overhead for each execution
- Real authenticated workflows require a separate delegated-identity design
