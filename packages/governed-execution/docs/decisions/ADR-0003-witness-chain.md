# ADR-0003: HMAC-signed hash-linked Witness Chain

- Status: Accepted
- Date: 2026-07-28

## Context

Every governance and execution decision needs tamper-evident evidence without requiring a distributed ledger.

## Decision

Store redacted JSON Lines records with sequence numbers, previous-record hashes, canonical record hashes and HMAC signatures.

## Consequences

- Simple local verification and recovery
- Detects modification, deletion and reordering within the retained chain
- Requires one writer per chain file
- Symmetric HMAC does not provide external non-repudiation
- Regulated deployments should export to an independently governed append-only store
