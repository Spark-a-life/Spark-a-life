from .types import MissionState

ALLOWED = {
 MissionState.RECEIVED:{MissionState.REGISTERED}, MissionState.REGISTERED:{MissionState.INTENT_ANALYSIS},
 MissionState.INTENT_ANALYSIS:{MissionState.CLARIFICATION_REQUIRED,MissionState.EVIDENCE_READINESS},
 MissionState.CLARIFICATION_REQUIRED:{MissionState.EVIDENCE_READINESS,MissionState.REJECTED},
 MissionState.EVIDENCE_READINESS:{MissionState.INDEPENDENT_DELIBERATION},
 MissionState.INDEPENDENT_DELIBERATION:{MissionState.CROSS_EXAMINATION},
 MissionState.CROSS_EXAMINATION:{MissionState.CHAIR_SYNTHESIS},
 MissionState.CHAIR_SYNTHESIS:{MissionState.AWAITING_CAPTAIN},
 MissionState.AWAITING_CAPTAIN:{MissionState.APPROVED,MissionState.REJECTED},
 MissionState.APPROVED:{MissionState.EXECUTION_PLANNING}, MissionState.EXECUTION_PLANNING:{MissionState.EXECUTING},
 MissionState.EXECUTING:{MissionState.VERIFYING}, MissionState.VERIFYING:{MissionState.RELEASE_REVIEW},
 MissionState.RELEASE_REVIEW:{MissionState.DELIVERED,MissionState.REJECTED},
 MissionState.DELIVERED:{MissionState.RETROSPECTIVE}, MissionState.RETROSPECTIVE:{MissionState.CLOSED},
 MissionState.CLOSED:set(), MissionState.REJECTED:set(),
}

def transition(current: MissionState, target: MissionState) -> MissionState:
    if target not in ALLOWED[current]:
        raise ValueError(f"Invalid state transition: {current.value} -> {target.value}")
    return target
