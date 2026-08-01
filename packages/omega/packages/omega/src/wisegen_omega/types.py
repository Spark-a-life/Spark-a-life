from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any

class MissionState(str, Enum):
    RECEIVED="RECEIVED"; REGISTERED="REGISTERED"; INTENT_ANALYSIS="INTENT_ANALYSIS"
    CLARIFICATION_REQUIRED="CLARIFICATION_REQUIRED"; EVIDENCE_READINESS="EVIDENCE_READINESS"
    INDEPENDENT_DELIBERATION="INDEPENDENT_DELIBERATION"; CROSS_EXAMINATION="CROSS_EXAMINATION"
    CHAIR_SYNTHESIS="CHAIR_SYNTHESIS"; AWAITING_CAPTAIN="AWAITING_CAPTAIN"
    APPROVED="APPROVED"; EXECUTION_PLANNING="EXECUTION_PLANNING"; EXECUTING="EXECUTING"
    VERIFYING="VERIFYING"; RELEASE_REVIEW="RELEASE_REVIEW"; DELIVERED="DELIVERED"
    RETROSPECTIVE="RETROSPECTIVE"; CLOSED="CLOSED"; REJECTED="REJECTED"

@dataclass
class Assumption:
    id: str; statement: str; basis: str="unspecified"; confidence: float=0.5
    impact_if_wrong: str="medium"; requires_confirmation: bool=False; status: str="unresolved"

@dataclass
class Clarification:
    id: str; question: str; priority: str; materiality: float; blocking: bool

@dataclass
class Claim:
    id: str; statement: str; classification: str; confidence: float
    evidence_refs: list[str]=field(default_factory=list); limitations: list[str]=field(default_factory=list)

@dataclass
class Review:
    adviser: str; recommendation: str; findings: list[str]; risks: list[str]
    questions: list[str]; confidence: float; evidence_refs: list[str]=field(default_factory=list)

@dataclass
class Decision:
    recommendation: str; confidence: float; consensus: list[str]; disagreements: list[str]
    principal_risks: list[str]; missing_evidence: list[str]; minimum_viable_action: str
    proceed_if: list[str]; stop_if: list[str]


def serialise(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"): return {k: serialise(v) for k,v in asdict(value).items()}
    if isinstance(value, Enum): return value.value
    if isinstance(value, list): return [serialise(v) for v in value]
    if isinstance(value, dict): return {k: serialise(v) for k,v in value.items()}
    return value
