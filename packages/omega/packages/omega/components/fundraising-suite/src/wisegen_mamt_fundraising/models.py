from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class GateDecision(str, Enum):
    APPROVE = "approve"
    REVISE = "revise"
    BLOCK = "block"
    PENDING_HUMAN_REVIEW = "pending_human_review"


class CircuitState(str, Enum):
    GREEN = "green"
    AMBER = "amber"
    RED = "red"
    BLACK = "black"


@dataclass(frozen=True)
class Mission:
    id: str
    objective: str
    programme_summary: str
    funding_goal: float
    currency: str
    audience: str
    region: str
    timeframe: str = "not specified"


@dataclass(frozen=True)
class Organisation:
    name: str
    voice: str
    constraints: list[str]


@dataclass(frozen=True)
class GovernanceProfile:
    jurisdiction: str
    fundraising_mode: str
    public_appeal: bool
    foreign_charitable_purpose: bool
    personal_data_used: bool
    vulnerable_audience: bool
    egress_channels: list[str]
    donor_acceptance_policy: str
    required_approvals: list[str]
    disclosure_requirements: list[str] = field(default_factory=list)
    restricted_terms: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class FundraisingPlan:
    segments: list[str]
    minimum_fit_score: float
    use_of_funds: list[str]


@dataclass(frozen=True)
class Prospect:
    name: str
    type: str
    region: str
    focus_areas: list[str]
    eligibility_notes: str
    estimated_amount: float
    source: str
    giving_history: str = ""
    relationship_signal: str = ""
    restrictions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EvidenceItem:
    id: str
    title: str
    source: str
    kind: str
    confidence: str
    permitted_use: list[str]


@dataclass(frozen=True)
class Claim:
    text: str
    evidence_ids: list[str]
    external_use: bool


@dataclass(frozen=True)
class RiskBudget:
    maximum_cost_usd: float
    maximum_tokens: int
    maximum_runtime_seconds: int
    maximum_external_calls: int
    maximum_retries: int
    maximum_consecutive_similar_actions: int = 3
    maximum_destructive_tools: int = 0
    human_approval_required: bool = True


@dataclass(frozen=True)
class OutputSpec:
    adapter: str
    deliverables: list[str]


@dataclass(frozen=True)
class MissionBrief:
    mission: Mission
    organisation: Organisation
    governance: GovernanceProfile
    fundraising: FundraisingPlan
    prospects: list[Prospect]
    evidence: list[EvidenceItem]
    claims: list[Claim]
    risk: RiskBudget
    output: OutputSpec
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MissionBrief":
        mission = Mission(**data["mission"])
        organisation = Organisation(**data["organisation"])
        governance = GovernanceProfile(**data["governance"])
        fundraising = FundraisingPlan(**data["fundraising"])
        prospects = [Prospect(**item) for item in data.get("prospects", [])]
        evidence = [EvidenceItem(**item) for item in data.get("evidence", [])]
        claims = [Claim(**item) for item in data.get("claims", [])]
        risk = RiskBudget(**data["risk"])
        output = OutputSpec(**data["output"])
        return cls(mission, organisation, governance, fundraising, prospects, evidence, claims, risk, output, data)


@dataclass(frozen=True)
class RoleAgent:
    name: str
    purpose: str
    allowed_tools: list[str]
    approval_threshold: str
    mission_scope: str


@dataclass(frozen=True)
class WorkPackage:
    role: str
    purpose: str
    allowed_tools: list[str]
    approval_threshold: str
    mission_scope: str
    mission_id: str
    output_contract: str
    escalation_rule: str


@dataclass(frozen=True)
class RuntimeUsage:
    cost_usd: float = 0
    tokens: int = 0
    runtime_seconds: int = 0
    external_calls: int = 0
    retries: int = 0
    consecutive_similar_actions: int = 0
    destructive_tools: int = 0


@dataclass(frozen=True)
class ScoreBreakdown:
    prospect_name: str
    score: float
    reasons: list[str]
    risks: list[str]
    recommended_stage: str


@dataclass(frozen=True)
class DonorDueDiligenceResult:
    prospect_name: str
    risk_level: str
    acceptance_recommendation: str
    flags: list[str]
    required_actions: list[str]


@dataclass(frozen=True)
class RouteDecision:
    task_type: str
    model_class: str
    sensitivity: str
    rationale: str
    allowed_external_call: bool


@dataclass(frozen=True)
class AdapterResult:
    adapter: str
    execution_mode: str
    artefacts: dict[str, Any]
    usage: RuntimeUsage
    notes: list[str]


@dataclass(frozen=True)
class ComplianceFinding:
    status: str
    message: str
    severity: str
    related_item: str


@dataclass(frozen=True)
class EvaluationResult:
    scores: dict[str, float]
    weighted_score: float
    decision: GateDecision
    revision_guidance: list[str]


@dataclass(frozen=True)
class CaptainGateResult:
    decision: GateDecision
    reasons: list[str]
    egress_allowed: bool
    required_human_actions: list[str]


@dataclass(frozen=True)
class PreflightCheck:
    name: str
    status: str
    message: str


@dataclass(frozen=True)
class PreflightReport:
    version: str
    status: str
    checks: list[PreflightCheck]
