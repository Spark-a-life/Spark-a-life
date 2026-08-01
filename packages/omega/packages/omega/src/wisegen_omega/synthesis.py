from statistics import mean
from .types import Decision

def synthesise(reviews, cross, evidence, intent):
    risks=[]
    for r in reviews:
        for x in r.risks:
            if x not in risks: risks.append(x)
    missing=[]
    if evidence["coverage"]<0.8: missing.append("Independent evidence covering material claims")
    if intent["assumptions"]: missing.append("Validation of high-impact assumptions")
    confidence=mean(r.confidence for r in reviews)
    confidence*=0.6+0.4*evidence["coverage"]
    if intent["readiness"]=="CONDITIONAL": confidence*=0.9
    recommendation="PROTOTYPE_FIRST" if missing or risks else "PROCEED"
    return Decision(recommendation,round(confidence,3),cross["shared_findings"] or ["Governed execution is preferable to unbounded automation."],
      cross["unresolved_disagreements"],risks[:5],missing,
      "Run the deterministic local example, inspect the decision record, then approve one bounded domain pilot.",
      ["P0 ambiguities are resolved","Captain approval is recorded","Acceptance tests pass"],
      ["A critical assumption is falsified","Evidence integrity fails","Execution exceeds its authority or risk budget"])
