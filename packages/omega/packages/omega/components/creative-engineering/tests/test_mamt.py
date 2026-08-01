from wisegen_creative_engineering.io import load_yaml
from wisegen_creative_engineering.contracts import parse_brief
from wisegen_creative_engineering.mamt.mission_team import MissionTeam


def test_mamt_compiles_role_agents():
    brief = parse_brief(load_yaml('examples/briefs/local_ci_mission.yaml'))
    team = MissionTeam().compile(brief)
    roles = {r['role'] for r in team}
    assert {'creative_director','safety_governor','provenance_auditor','deployment_agent'} <= roles
    assert all(r['mission_id'] == brief.mission.id for r in team)
