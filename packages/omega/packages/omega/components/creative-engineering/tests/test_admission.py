import pytest
from copy import deepcopy
from wisegen_creative_engineering.io import load_yaml
from wisegen_creative_engineering.contracts import parse_brief
from wisegen_creative_engineering.mission_guard.admission import assert_admissible


def test_admission_rejects_unverified_public_asset():
    data = load_yaml('examples/briefs/local_ci_mission.yaml')
    bad = deepcopy(data)
    bad['assets'][0]['consent'] = 'public_unverified'
    brief = parse_brief(bad)
    with pytest.raises(ValueError):
        assert_admissible(brief)
