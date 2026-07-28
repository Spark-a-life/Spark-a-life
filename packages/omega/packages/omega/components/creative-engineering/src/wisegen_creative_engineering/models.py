from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any

class CircuitState(str, Enum):
    GREEN = "GREEN"
    AMBER = "AMBER"
    RED = "RED"
    BLACK = "BLACK"

class GateDecision(str, Enum):
    APPROVE = "approve"
    REVISE = "revise"
    BLOCK = "block"

@dataclass(frozen=True)
class RiskBudget:
    maximum_cost_usd: float
    maximum_tokens: int
    maximum_runtime_seconds: int
    maximum_external_calls: int
    maximum_retries: int
    human_approval_required: bool = True
    maximum_consecutive_similar_actions: int = 3

@dataclass(frozen=True)
class AssetRecord:
    id: str
    type: str
    source: str
    consent: str
    permitted_use: list[str]

@dataclass(frozen=True)
class Mission:
    id: str
    objective: str
    audience: str
    channel: str
    industry: str | None

@dataclass(frozen=True)
class CreativeSpec:
    format: str
    style: str
    message: str
    references: list[str]

@dataclass(frozen=True)
class BrandSpec:
    name: str
    voice: str
    constraints: list[str]

@dataclass(frozen=True)
class OutputSpec:
    adapter: str
    deliverables: list[str]

@dataclass(frozen=True)
class CreativeBrief:
    mission: Mission
    brand: BrandSpec
    creative: CreativeSpec
    assets: list[AssetRecord]
    risk: RiskBudget
    output: OutputSpec
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data

@dataclass
class RuntimeUsage:
    cost_usd: float = 0.0
    tokens: int = 0
    runtime_seconds: int = 0
    external_calls: int = 0
    retries: int = 0

@dataclass(frozen=True)
class PromptPack:
    adapter: str
    title: str
    prompt: str
    negative_prompt: str
    paste_back_required: list[str]
    governance_notes: list[str]

@dataclass(frozen=True)
class AdapterResult:
    adapter: str
    execution_mode: str
    artefacts: dict[str, Any]
    usage: RuntimeUsage
    notes: list[str]

@dataclass(frozen=True)
class EvaluationResult:
    scores: dict[str, float]
    weighted_score: float
    decision: GateDecision
    revision_guidance: list[str]

@dataclass(frozen=True)
class MissionRunResult:
    brief: dict[str, Any]
    team: list[dict[str, Any]]
    prompt_pack: dict[str, Any]
    adapter_result: dict[str, Any]
    evaluation: dict[str, Any]
    circuit_state: str
    witness_path: str
