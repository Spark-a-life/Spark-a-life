from .types import Review
ROLES=("sceptic","first_principles","opportunity_strategist","outsider","execution_lead","risk_governance","systems_architect","economist")

def _base(mission, role):
    objective=mission.get("objective","unspecified objective")
    constraints=mission.get("constraints",[]) or []
    patterns={
      "sceptic":(["The proposal may fail if its key assumptions are not validated."],["False confidence from deterministic-looking outputs."],["What evidence would falsify the proposal?"]),
      "first_principles":(["Separate the desired outcome from the proposed implementation."],["Inherited constraints may be conventions rather than necessities."],["Which causal mechanism makes the proposal work?"]),
      "opportunity_strategist":(["Consider a smaller platform capability that serves multiple domains."],["Over-specialisation may reduce reuse."],["Which adjacent use case increases leverage without increasing risk?"]),
      "outsider":(["The user journey and decision rights must be understandable without specialist knowledge."],["Complex governance may become ceremony."],["Can a new operator explain what happens when the system refuses to proceed?"]),
      "execution_lead":(["Begin with a deterministic acceptance-tested vertical slice."],["Scope expansion can prevent delivery."],["What can be completed and verified in one working day?"]),
      "risk_governance":(["External actions must remain behind explicit authority gates."],["Sensitive data, prompt injection and credential leakage require controls."],["Who bears accountability when a recommendation is wrong?"]),
      "systems_architect":(["Use stable contracts between the control plane and domain plugins."],["Tight coupling between models and workflows threatens portability."],["Which interfaces must remain versioned and backwards compatible?"]),
      "economist":(["Measure deliberation cost against avoided rework and risk."],["More agents can create coordination cost without decision value."],["What threshold justifies the full council rather than a streamlined path?"]),
    }
    f,r,q=patterns[role]
    rec="PROTOTYPE_FIRST" if role in {"sceptic","execution_lead","risk_governance"} else "PROCEED_CAREFULLY"
    confidence=max(0.45,min(0.9,0.72-0.02*len(constraints)))
    return Review(role,rec,[f"Objective reviewed: {objective}"]+f,r,q,confidence)

def independent_reviews(mission, selected=None):
    return [_base(mission,r) for r in (selected or ROLES)]

def cross_examine(reviews):
    recommendations={r.recommendation for r in reviews}
    shared=[]
    if any("assumption" in " ".join(r.findings+r.risks).lower() for r in reviews): shared.append("Validate assumptions before irreversible execution.")
    return {"recommendation_diversity":sorted(recommendations),"shared_findings":shared,
            "unresolved_disagreements":["Council differs on whether to proceed directly or prototype first."] if len(recommendations)>1 else [],
            "review_count":len(reviews)}
