import pytest
from wisegen_omega.state_machine import transition
from wisegen_omega.types import MissionState

def test_valid_transition(): assert transition(MissionState.RECEIVED,MissionState.REGISTERED)==MissionState.REGISTERED
def test_bypass_fails_closed():
    with pytest.raises(ValueError): transition(MissionState.INTENT_ANALYSIS,MissionState.EXECUTING)
