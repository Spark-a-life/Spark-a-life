from wisegen_omega.engine import OmegaEngine

def mission(decision="APPROVE"):
 return {"objective":"Evaluate a bounded pilot","success_criteria":["verified"],"constraints":["local"],"stakeholders":["captain"],"deadline":"2026-08-01","evidence":[{"summary":"test"}],"captain":{"decision":decision,"allow_declared_assumptions":True}}
def test_approved_run_closes(tmp_path):
 r=OmegaEngine(tmp_path/"a.jsonl").run(mission()); assert r["status"]=="COMPLETED"; assert r["state"]=="CLOSED"; assert len(r["reviews"])==8
def test_deferred_run_not_authorised(tmp_path):
 r=OmegaEngine(tmp_path/"a.jsonl").run(mission("DEFER")); assert r["status"]=="NOT_AUTHORISED"; assert r["state"]=="REJECTED"
def test_missing_objective_blocks(tmp_path):
 m={"success_criteria":["x"],"captain":{"decision":"APPROVE","allow_declared_assumptions":False}}
 r=OmegaEngine(tmp_path/"a.jsonl").run(m); assert r["status"]=="BLOCKED"; assert r["state"]=="CLARIFICATION_REQUIRED"
