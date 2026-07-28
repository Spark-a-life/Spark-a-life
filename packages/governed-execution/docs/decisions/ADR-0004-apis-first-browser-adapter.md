# ADR-0004: Direct integrations first, browser as governed adapter

- Status: Accepted
- Date: 2026-07-28

## Context

Browser automation can bridge legacy systems but is more sensitive to interface changes, session state and partial completion than supported service interfaces.

## Decision

Prefer authorised APIs, events and typed tools where they provide suitable functionality. Permit browser interaction when the UI is the authorised operating surface or direct integration is unavailable or incomplete.

## Consequences

- Better interoperability and observability for supported interfaces
- Browser use remains available but explicitly bounded
- Capability owners must justify and test UI-mediated workflows
