from pathlib import Path

from wisegen_mamt_fundraising.engine import run_mission


def test_engine_runs_end_to_end(tmp_path: Path):
    output = tmp_path / "run.json"
    audit = tmp_path / "witness.jsonl"
    result = run_mission("examples/missions/local_ci_mission.yaml", output, audit)
    assert output.exists()
    assert audit.exists()
    assert result["mission_id"] == "ci-fundraising-local"
    assert result["captain_gate"]["decision"] == "approve"
