from dataclasses import asdict
from pathlib import Path
from .contracts import parse_brief
from .io import load_yaml, write_json
from .mamt.mission_team import MissionTeam
from .mission_guard.admission import assert_admissible
from .prompting import compile_prompt_pack
from .runtime_governor.governor import RuntimeGovernor
from .router import get_adapter
from .evaluation.rubric import evaluate
from .mission_guard.approval_gate import captain_gate
from .audit.witness_chain import WitnessChain


def compile_mission(path: str | Path) -> dict:
    brief = parse_brief(load_yaml(path))
    team = MissionTeam().compile(brief)
    prompt_pack = compile_prompt_pack(brief)
    return {'brief': brief.to_dict(), 'team': team, 'prompt_pack': asdict(prompt_pack)}


def run_mission(path: str | Path, output_path: str | Path = 'outputs/run.json') -> dict:
    brief = parse_brief(load_yaml(path))
    assert_admissible(brief)
    witness_path = Path(output_path).with_suffix('.jsonl')
    witness = WitnessChain(witness_path)
    witness.append('mission_admitted', {'mission_id': brief.mission.id, 'adapter': brief.output.adapter})
    team = MissionTeam().compile(brief)
    witness.append('mamt_compiled', {'roles': [r['role'] for r in team]})
    prompt_pack = compile_prompt_pack(brief)
    witness.append('prompt_pack_compiled', {'title': prompt_pack.title, 'adapter': prompt_pack.adapter})
    governor = RuntimeGovernor(brief.risk)
    adapter = get_adapter(brief.output.adapter)
    governor.record_action(f"adapter:{adapter.name}:execute")
    governor.assert_executable()
    adapter_result = adapter.execute(brief, prompt_pack)
    state = governor.record_action(f"adapter:{adapter.name}:complete", adapter_result.usage)
    witness.append('adapter_executed', {'adapter': adapter_result.adapter, 'state': state.value, 'usage': asdict(adapter_result.usage)})
    evaluation = evaluate(brief, adapter_result)
    gate = captain_gate(evaluation, brief.risk.human_approval_required)
    evaluation_payload = asdict(evaluation)
    evaluation_payload['captain_gate'] = gate.value
    witness.append('evaluation_completed', evaluation_payload)
    result = {
        'brief': brief.to_dict(),
        'team': team,
        'prompt_pack': asdict(prompt_pack),
        'adapter_result': asdict(adapter_result),
        'evaluation': evaluation_payload,
        'circuit_state': state.value,
        'witness_path': str(witness_path),
    }
    write_json(output_path, result)
    return result
