"""Approval Service: the Captain's Gate.

AI proposes, the human decides. The gate packet is fixed in shape so that a
reviewer is never asked to approve something they cannot see:

    what changed, why, which agent, which model, which tools, evidence passed,
    evidence failed, residual risk, cost, and how to reverse it.

Available actions: approve, reject, request_revision, approve_with_conditions,
select_branch, combine_branches, escalate.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .domain import digest, new_id, utc_now
from .witness import WitnessChain

ACTIONS = (
    "approve",
    "reject",
    "request_revision",
    "approve_with_conditions",
    "select_branch",
    "combine_branches",
    "escalate",
)


@dataclass
class GatePacket:
    id: str = field(default_factory=lambda: new_id("gate"))
    created_at: str = field(default_factory=utc_now)
    what_changed: list[str] = field(default_factory=list)
    why: str = ""
    agents: list[str] = field(default_factory=list)
    models: list[dict[str, Any]] = field(default_factory=list)
    tools_invoked: list[str] = field(default_factory=list)
    evidence_passed: list[str] = field(default_factory=list)
    evidence_failed: list[str] = field(default_factory=list)
    residual_risks: list[str] = field(default_factory=list)
    cost: dict[str, Any] = field(default_factory=dict)
    reversal: str = ""
    branches: list[dict[str, Any]] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    @property
    def ready(self) -> bool:
        return not self.evidence_failed

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "ready_for_decision": self.ready,
            "what_changed": self.what_changed,
            "why": self.why,
            "which_agents": self.agents,
            "which_models": self.models,
            "which_tools": self.tools_invoked,
            "evidence_passed": self.evidence_passed,
            "evidence_failed": self.evidence_failed,
            "residual_risks": self.residual_risks,
            "cost": self.cost,
            "how_to_reverse": self.reversal,
            "candidate_branches": self.branches,
            "open_questions": self.open_questions,
            "available_actions": list(ACTIONS),
        }

    def to_markdown(self) -> str:
        lines = [
            "# Captain's Gate",
            "",
            f"Packet `{self.id}` created {self.created_at}. "
            + ("**Ready for decision.**" if self.ready else "**Not ready: blocking evidence failed.**"),
            "",
            "## What changed",
        ]
        lines += [f"- {item}" for item in self.what_changed] or ["- nothing recorded"]
        lines += ["", "## Why", self.why or "not stated", "", "## Who and what produced it", ""]
        lines += [f"- agent: {agent}" for agent in self.agents]
        lines += [f"- model: {model.get('model_id')} ({model.get('provider')}, {model.get('tokens')} tokens)" for model in self.models]
        lines += [f"- tool: {tool}" for tool in sorted(set(self.tools_invoked))]
        lines += ["", "## Evidence passed", ""] + [f"- {item}" for item in self.evidence_passed]
        lines += ["", "## Evidence failed", ""] + ([f"- {item}" for item in self.evidence_failed] or ["- none"])
        lines += ["", "## Residual risk", ""] + ([f"- {item}" for item in self.residual_risks] or ["- none recorded"])
        if self.branches:
            lines += ["", "## Candidate branches", "", "| Candidate | Verdict | Cost (SGD) | Note |", "| --- | --- | --- | --- |"]
            for branch in self.branches:
                lines.append(
                    f"| {branch.get('label')} | {branch.get('verdict')} | {branch.get('sgd', 0)} | {branch.get('note', '')} |"
                )
        lines += [
            "",
            "## Cost",
            "",
            f"```json\n{json.dumps(self.cost, indent=2)}\n```",
            "",
            "## How to reverse",
            "",
            self.reversal or "not stated",
            "",
            "## Open questions for the Captain",
            "",
        ]
        lines += [f"- {item}" for item in self.open_questions] or ["- none"]
        lines += ["", "## Decision", "", "Available actions: " + ", ".join(ACTIONS), ""]
        return "\n".join(lines)


@dataclass
class Decision:
    packet_id: str
    action: str
    decided_by: str
    rationale: str
    conditions: list[str] = field(default_factory=list)
    selected_branch: str | None = None
    decided_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "action": self.action,
            "decided_by": self.decided_by,
            "rationale": self.rationale,
            "conditions": self.conditions,
            "selected_branch": self.selected_branch,
            "decided_at": self.decided_at,
        }


class ApprovalService:
    def __init__(self, store: str | Path, witness: WitnessChain) -> None:
        self.store = Path(store)
        self.store.mkdir(parents=True, exist_ok=True)
        self.witness = witness

    def submit(self, packet: GatePacket) -> GatePacket:
        (self.store / f"{packet.id}.json").write_text(json.dumps(packet.to_dict(), indent=2), encoding="utf-8")
        (self.store / f"{packet.id}.md").write_text(packet.to_markdown(), encoding="utf-8")
        self.witness.append(
            "approval-service",
            "gate.submitted",
            {"packet_id": packet.id, "ready": packet.ready, "digest": digest(packet.to_dict())},
        )
        return packet

    def decide(
        self,
        packet: GatePacket,
        action: str,
        decided_by: str,
        rationale: str,
        conditions: list[str] | None = None,
        selected_branch: str | None = None,
    ) -> Decision:
        if action not in ACTIONS:
            raise ValueError(f"unknown gate action: {action}")
        if action in ("approve", "approve_with_conditions", "select_branch") and not packet.ready:
            raise PermissionError("packet is not ready for approval: blocking evidence failed")
        if action == "select_branch" and not selected_branch:
            raise ValueError("select_branch requires a branch label")
        decision = Decision(
            packet_id=packet.id,
            action=action,
            decided_by=decided_by,
            rationale=rationale,
            conditions=list(conditions or []),
            selected_branch=selected_branch,
        )
        (self.store / f"{packet.id}.decision.json").write_text(
            json.dumps(decision.to_dict(), indent=2), encoding="utf-8"
        )
        self.witness.append("captain", "gate.decided", decision.to_dict())
        return decision

    def decision_for(self, packet_id: str) -> Decision | None:
        path = self.store / f"{packet_id}.decision.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return Decision(**data)
