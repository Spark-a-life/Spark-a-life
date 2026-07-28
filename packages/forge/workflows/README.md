# Workflows

A workflow declares which roles run at which stage, what gates apply, and what each stage must produce. It is documentation the runtime agrees with, not documentation about the runtime.

| Workflow | Status | Purpose |
|---|---|---|
| `spreadsheet-to-application` | reference, implemented | Existing sheet to governed, owned application |
| `document-to-workflow` | defined, deferred | Policy or SOP document to executable approval workflow |
| `intent-to-prototype` | defined, deferred | Conversation to reviewable prototype, no deployment path |
| `application-modernisation` | defined, deferred | Existing repository to specification, then governed regeneration |
| `prototype-to-production` | defined, deferred | Promote a prototype through the full gate set |
| `incident-response` | defined, deferred | Contingency-led recovery with forced human checkpoints |
| `governed-change` | defined, deferred | Change to a deployed system with drift detection |

Deferred workflows have an activation criterion in `docs/decision-records/ADR-0006-scope-boundary.md`. They are not stubs waiting to be filled; they are commitments not yet made.
