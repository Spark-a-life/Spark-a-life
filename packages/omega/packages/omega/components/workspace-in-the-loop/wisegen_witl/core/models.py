from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Evidence:
    id: str
    source: str
    claim: str
    reliability: float
    relevance: float
    notes: str = ""


@dataclass
class Option:
    id: str
    name: str
    description: str
    features: Dict[str, float]
    evidence_ids: List[str] = field(default_factory=list)


@dataclass
class Criterion:
    id: str
    name: str
    weight: float
    direction: str = "max"  # max or min
    threshold: Optional[float] = None


@dataclass
class LaneAssessment:
    lane: str
    finding: str
    confidence: float
    risks: List[str]
    recommendations: List[str]


@dataclass
class OptionScore:
    option_id: str
    option_name: str
    total_score: float
    criterion_scores: Dict[str, float]
    rationale: str
    confidence: float


@dataclass
class RiskAssessment:
    level: str
    score: float
    risks: List[str]
    gate_required: bool


@dataclass
class WorkspaceState:
    workspace_id: str
    workflow_id: str
    domain: str
    objective: str
    initiator: str
    decision_authority: str
    constraints: List[str]
    evidence: List[Evidence]
    options: List[Option]
    criteria: List[Criterion]
    assumptions: List[str]
    hypotheses: List[str]
    created_at: str = field(default_factory=utc_now)
    lanes: List[LaneAssessment] = field(default_factory=list)
    ranking: List[OptionScore] = field(default_factory=list)
    risk: Optional[RiskAssessment] = None
    captain_gate: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DecisionReport:
    report_id: str
    workspace_id: str
    workflow_id: str
    recommendation: str
    ranked_options: List[OptionScore]
    risk: RiskAssessment
    captain_gate: Dict[str, Any]
    lane_assessments: List[LaneAssessment]
    evidence_summary: Dict[str, Any]
    witness_hash: str
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
