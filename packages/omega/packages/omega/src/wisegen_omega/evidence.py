from .types import Claim
ALLOWED={"FACT","STRONG_EVIDENCE","MODERATE_EVIDENCE","EXPERT_JUDGEMENT","HYPOTHESIS","SPECULATION"}
def build_register(mission):
    evidence=[]
    for i,e in enumerate(mission.get("evidence",[]),1):
        if isinstance(e,str): e={"summary":e}
        evidence.append({"id":e.get("id",f"EV-{i:03d}"),"summary":e.get("summary",""),"source":e.get("source","user-provided"),"quality":e.get("quality","unverified")})
    claims=[]
    for i,c in enumerate(mission.get("claims",[]),1):
        classification=c.get("classification","HYPOTHESIS").upper()
        if classification not in ALLOWED: classification="HYPOTHESIS"
        claims.append(Claim(c.get("id",f"CLM-{i:03d}"),c["statement"],classification,float(c.get("confidence",0.5)),c.get("evidence_refs",[]),c.get("limitations",[])))
    coverage=(sum(1 for c in claims if c.evidence_refs)/len(claims)) if claims else (1.0 if evidence else 0.5)
    return {"evidence":evidence,"claims":claims,"coverage":round(coverage,3),"ready":coverage>=0.5 or not claims}
