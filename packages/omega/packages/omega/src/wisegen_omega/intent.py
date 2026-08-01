from .types import Assumption, Clarification

IMPACT={"low":1,"medium":2,"high":3,"critical":4}

def analyse(mission):
    facts=[]; assumptions=[]; unknowns=[]; clarifications=[]
    for key in ("objective","desired_outcome","constraints","success_criteria","stakeholders","deadline"):
        value=mission.get(key)
        if value not in (None,"",[],{}): facts.append({"field":key,"value":value})
        else: unknowns.append(key)
    for i,a in enumerate(mission.get("assumptions",[]),1):
        if isinstance(a,str): a={"statement":a}
        assumptions.append(Assumption(id=a.get("id",f"ASM-{i:03d}"),statement=a["statement"],
            basis=a.get("basis","user-declared"),confidence=float(a.get("confidence",0.5)),
            impact_if_wrong=a.get("impact_if_wrong","medium"),requires_confirmation=bool(a.get("requires_confirmation",False)),
            status=a.get("status","unresolved")))
    required={"objective":"What precise decision or output is required?",
              "success_criteria":"What measurable conditions define an acceptable result?"}
    for field,q in required.items():
        if field in unknowns:
            clarifications.append(Clarification(f"CLR-{len(clarifications)+1:03d}",q,"P0",1.0,True))
    for field in ("constraints","stakeholders","deadline"):
        if field in unknowns:
            clarifications.append(Clarification(f"CLR-{len(clarifications)+1:03d}",f"Please specify {field.replace('_',' ')} if it materially affects the mission.","P2",0.35,False))
    for a in assumptions:
        if a.requires_confirmation or (IMPACT.get(a.impact_if_wrong,2)>=3 and a.confidence<0.75):
            clarifications.append(Clarification(f"CLR-{len(clarifications)+1:03d}",f"Confirm assumption {a.id}: {a.statement}","P1",0.8,True))
    blocking=any(c.blocking for c in clarifications)
    return {"facts":facts,"assumptions":assumptions,"unknowns":unknowns,"clarifications":clarifications,
            "readiness":"BLOCKED" if blocking else ("CONDITIONAL" if unknowns or assumptions else "READY")}
