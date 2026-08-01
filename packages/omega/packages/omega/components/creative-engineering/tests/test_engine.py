from pathlib import Path
from wisegen_creative_engineering.engine import compile_mission, run_mission


def test_compile_mission_contains_prompt_pack():
    compiled = compile_mission('examples/briefs/local_ci_mission.yaml')
    assert compiled['prompt_pack']['adapter'] == 'local_deterministic'
    assert len(compiled['team']) >= 8


def test_run_mission_writes_output_and_witness_chain(tmp_path):
    out = tmp_path / 'run.json'
    result = run_mission('examples/briefs/local_ci_mission.yaml', out)
    assert out.exists()
    assert Path(result['witness_path']).exists()
    assert result['adapter_result']['adapter'] == 'local_deterministic'
    assert result['evaluation']['captain_gate'] in {'approve','revise','block'}
