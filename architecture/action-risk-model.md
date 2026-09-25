# Action Risk Model

Status: Draft  
Version: 1.2.0-alpha  
Canonical source: `governance/AIOS_v1.2.md` §25  
Owner: Human Captain  
Review trigger: Before enabling any consequential external Action

## Purpose

Classify external Actions by consequence, authority, sensitivity, purpose, destination and reversibility rather than by HTTP method or whether an operation is technically read-only.

Read-only does not automatically mean low risk.

Schema enumerations: `GREEN`, `AMBER`, `RED`, `PROHIBITED`.

## Classification

### GREEN

Read-only, low sensitivity, no external commitment.

Examples: authorised retrieval, comparison, internal draft preparation.

Minimum controls:

- Layer 0 boundary, privacy and purpose check;
- authenticated and authorised access;
- data minimisation;
- logging proportionate to risk;
- no onward consequential execution.

An individual Human Captain gate is not required only where purpose, information, privacy, access and retention rules already authorise the retrieval.

### AMBER

Limited external change, normally reversible, bounded consequence.

Examples: calendar invitation, routine CRM update, non-binding correspondence.

Minimum controls:

- AIOS preflight;
- Action Proposal with immutable digest;
- explicit target and intended effect;
- data sensitivity check;
- scoped approval or pre-authorised policy, externally verifiable;
- time-bounded approval bound to the exact proposal;
- execution receipt;
- outcome verification where material.

### RED

Financial, legal, contractual, employment, high-risk disclosure, destructive change, security or credential change, safety-critical execution, autonomous onward delegation, or action with difficult-to-reverse consequences.

Default treatment:

- do not execute unless specifically approved by policy and the Human Captain;
- require enhanced verification and server-side authorisation;
- require explicit rollback or containment plan where feasible;
- require post-execution verification;
- prohibit autonomous chaining.

### PROHIBITED

Must not be executed by this system.

Examples: self-authorisation; unrestricted send-anything; covert data exfiltration; safety-critical plant or clinical control; splitting a prohibited effect into smaller Amber Actions to evade class.

Required treatment:

- refuse;
- do not propose an execution path;
- record the refusal in the Witness Chain;
- do not allow approval to convert Prohibited into executable.

## Decision principle

Action risk is a function of authority, sensitivity, purpose, destination, reversibility and consequence.

Fail closed. Do not silently fall back from Red to Amber, or from Amber to Green, because a control is unimplemented.
