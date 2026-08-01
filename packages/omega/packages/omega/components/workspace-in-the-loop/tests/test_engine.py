from pathlib import Path

from wisegen_witl.core.engine import run_workspace
from wisegen_witl.storage.json_store import read_json


def test_engine_produces_decision_report(tmp_path: Path):
    case = read_json("examples/leadgen_case.json")
    workflow = read_json("workflows/leadgen_workflow.json")
    report = run_workspace(case, workflow, witness_path=tmp_path / "witness.jsonl")
    assert report.recommendation.startswith("Prioritise")
    assert report.ranked_options
    assert report.witness_hash
    assert report.captain_gate["status"] in {"requires_human_approval", "approved_for_low_risk_execution"}
