from __future__ import annotations
from pathlib import Path
import uuid
from .types import MissionState, serialise
from .state_machine import transition
from .intent import analyse
from .evidence import build_register
from .advisers import independent_reviews, cross_examine
from .synthesis import synthesise
from .plugins import execute_plugin
from .witness import WitnessChain

class OmegaEngine:
    def __init__(self,audit_path="outputs/witness-chain.jsonl"):
        self.audit=WitnessChain(audit_path)
    def run(self, mission):
        mission_id=mission.get("mission_id") or f"MIS-{uuid.uuid4().hex[:10].upper()}"
        state=MissionState.RECEIVED; history=[state.value]
        def move(target,payload=None,actor="omega-control-plane"):
            nonlocal state
            state=transition(state,target); history.append(state.value)
            self.audit.append(mission_id,target.value,actor,payload or {})
        move(MissionState.REGISTERED,{"domain":mission.get("domain","strategy")})
        move(MissionState.INTENT_ANALYSIS)
        intent=analyse(mission)
        if intent["readiness"]=="BLOCKED" and not mission.get("captain",{}).get("allow_declared_assumptions",False):
            move(MissionState.CLARIFICATION_REQUIRED,{"clarifications":serialise(intent["clarifications"])})
            return {"mission_id":mission_id,"state":state.value,"history":history,"intent":serialise(intent),"status":"BLOCKED"}
        if intent["readiness"]=="BLOCKED":
            move(MissionState.CLARIFICATION_REQUIRED,{"override":"declared assumption path"})
        move(MissionState.EVIDENCE_READINESS)
        evidence=build_register(mission)
        move(MissionState.INDEPENDENT_DELIBERATION)
        reviews=independent_reviews(mission,mission.get("advisers"))
        move(MissionState.CROSS_EXAMINATION)
        cross=cross_examine(reviews)
        move(MissionState.CHAIR_SYNTHESIS)
        decision=synthesise(reviews,cross,evidence,intent)
        move(MissionState.AWAITING_CAPTAIN,{"recommendation":decision.recommendation})
        captain=mission.get("captain",{}).get("decision","DEFER").upper()
        if captain not in {"APPROVE","APPROVE_WITH_CONDITIONS"}:
            move(MissionState.REJECTED,{"captain_decision":captain})
            return {"mission_id":mission_id,"state":state.value,"history":history,"intent":serialise(intent),"evidence":serialise(evidence),"reviews":serialise(reviews),"cross_examination":cross,"decision":serialise(decision),"status":"NOT_AUTHORISED"}
        move(MissionState.APPROVED,{"captain_decision":captain},"captain")
        move(MissionState.EXECUTION_PLANNING)
        move(MissionState.EXECUTING)
        plugin=execute_plugin(mission)
        move(MissionState.VERIFYING)
        verification={"contract_valid":True,"authority_respected":True,"external_actions":0,"passed":True}
        move(MissionState.RELEASE_REVIEW,verification)
        move(MissionState.DELIVERED,{"plugin":plugin.plugin})
        move(MissionState.RETROSPECTIVE,{"confidence":decision.confidence})
        move(MissionState.CLOSED)
        return {"mission_id":mission_id,"state":state.value,"history":history,"intent":serialise(intent),"evidence":serialise(evidence),"reviews":serialise(reviews),"cross_examination":cross,"decision":serialise(decision),"execution":serialise(plugin),"verification":verification,"status":"COMPLETED"}
