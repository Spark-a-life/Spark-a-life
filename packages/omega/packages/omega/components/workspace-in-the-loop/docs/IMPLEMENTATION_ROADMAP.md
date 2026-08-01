# Implementation Roadmap

## Phase 1: Local reference implementation

- Run deterministic CLI workflows.
- Validate lead ranking and media evaluation examples.
- Review witness logs.
- Adjust criteria weights.

## Phase 2: Service layer

- Wrap `run_workspace` in an API endpoint.
- Persist evidence, workspace, and reports in a database.
- Add authentication and role-based access control.
- Add workspace templates for each business vertical.

## Phase 3: LLM adapter layer

- Add model adapters for drafting hypotheses, counterarguments, and rationale summaries.
- Keep ranking, risk, and witness logic outside the LLM.
- Store prompts, model version, temperature, and response hash.

## Phase 4: Outcome feedback

- Add scheduled review of predictions versus actual outcomes.
- Update weights and heuristics only after documented review.
- Track calibration drift.

## Phase 5: Productisation

- Package vertical products:
  - LeadGen Intelligence Workbench
  - Media OS Evaluation Workbench
  - AI Governance Decision Passport
  - Vendor and Model Selection Workbench
