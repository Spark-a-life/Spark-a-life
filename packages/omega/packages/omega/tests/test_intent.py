from wisegen_omega.intent import analyse

def test_missing_objective_blocks():
    r=analyse({"success_criteria":["x"]}); assert r["readiness"]=="BLOCKED"; assert any(c.blocking for c in r["clarifications"])
def test_complete_mission_ready_or_conditional():
    r=analyse({"objective":"Decide a bounded pilot","success_criteria":["pass"],"constraints":[],"stakeholders":[],"deadline":"2026-01-01"}); assert r["readiness"] in {"READY","CONDITIONAL"}
