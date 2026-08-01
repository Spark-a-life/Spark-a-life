"""Agent Runtime: agent-as-policy-bound-software, not agent-as-prompt.

Each agent is a versioned contract declaring its mandate, its allowed and
prohibited authorities, its model policy, the evidence it must produce and the
gate it reports to. The runtime refuses any capability the contract does not
grant, refuses again if the Policy Engine disagrees, and witnesses both the
refusal and the execution.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from . import mini_yaml
from .cost import CostGovernor
from .model_router import ModelRouter
from .orchestrator import Task
from .policy import PolicyEngine
from .tool_gateway import ToolGateway
from .witness import WitnessChain


class AuthorityError(PermissionError):
    pass


@dataclass
class AgentDefinition:
    id: str
    version: str
    role: str
    mandate: str
    layer: str = "forge"
    allowed: list[str] = field(default_factory=list)
    prohibited: list[str] = field(default_factory=list)
    model_capability: str = "reasoning"
    evidence_requirements: list[str] = field(default_factory=list)
    approval_gate: str = "captain"
    exit_artefact: str = "unspecified"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentDefinition":
        authority = data.get("authority") or {}
        model_policy = data.get("model_policy") or {}
        return cls(
            id=str(data["id"]),
            version=str(data.get("version", "0.1.0")),
            role=str(data.get("role", data["id"])),
            mandate=str(data.get("mandate", "")),
            layer=str(data.get("layer", "forge")),
            allowed=list(authority.get("allowed") or []),
            prohibited=list(authority.get("prohibited") or []),
            model_capability=str(model_policy.get("capability", "reasoning")),
            evidence_requirements=list(data.get("evidence_requirements") or []),
            approval_gate=str(data.get("approval_gate", "captain")),
            exit_artefact=str(data.get("exit_artefact", "unspecified")),
        )

    def may(self, capability: str) -> bool:
        if capability in self.prohibited:
            return False
        return capability in self.allowed or "*" in self.allowed


@dataclass
class AgentContext:
    task: Task
    agent: AgentDefinition
    tools: ToolGateway
    router: ModelRouter
    witness: WitnessChain
    governor: CostGovernor
    state: dict[str, Any]

    @property
    def payload(self) -> dict[str, Any]:
        return self.task.payload


class AgentRegistry:
    def __init__(self, path: str | Path) -> None:
        document = mini_yaml.load_file(path) or {}
        self.version = str(document.get("version", "0.0.0"))
        self.agents: dict[str, AgentDefinition] = {}
        for entry in document.get("agents", []) or []:
            definition = AgentDefinition.from_dict(entry)
            self.agents[definition.id] = definition

    def get(self, agent_id: str) -> AgentDefinition:
        if agent_id not in self.agents:
            raise KeyError(f"agent not in registry: {agent_id}")
        return self.agents[agent_id]

    def by_layer(self, layer: str) -> list[AgentDefinition]:
        return [agent for agent in self.agents.values() if agent.layer == layer]

    def all(self) -> list[AgentDefinition]:
        return list(self.agents.values())

    def __len__(self) -> int:
        return len(self.agents)


class AgentRuntime:
    def __init__(
        self,
        registry: AgentRegistry,
        policy: PolicyEngine,
        tools: ToolGateway,
        router: ModelRouter,
        witness: WitnessChain,
        governor: CostGovernor,
    ) -> None:
        self.registry = registry
        self.policy = policy
        self.tools = tools
        self.router = router
        self.witness = witness
        self.governor = governor
        self.handlers: dict[str, Callable[[AgentContext], dict[str, Any]]] = {}
        self.state: dict[str, Any] = {}

    def handler(self, capability: str) -> Callable[[Callable[[AgentContext], dict[str, Any]]], Callable]:
        def decorator(function: Callable[[AgentContext], dict[str, Any]]):
            self.handlers[capability] = function
            return function

        return decorator

    def run(self, task: Task) -> dict[str, Any]:
        capability = str(task.payload.get("capability", task.name))
        agent = self.registry.get(task.agent)

        if not agent.may(capability):
            self.witness.append(agent.id, "authority.refused", {"capability": capability, "task": task.name})
            raise AuthorityError(f"{agent.id} v{agent.version} is not authorised for {capability}")

        decision = self.policy.evaluate(
            {"actor": agent.id, "action": f"capability:{capability}", "resource": task.name, "classification": "internal"}
        )
        if not decision.allowed:
            self.witness.append(agent.id, "policy.refused", {"capability": capability, "reason": decision.reason})
            raise AuthorityError(f"policy refused {agent.id} -> {capability}: {decision.reason}")

        handler = self.handlers.get(capability)
        if handler is None:
            raise KeyError(f"no handler registered for capability {capability}")

        self.witness.append(
            agent.id,
            "agent.started",
            {
                "capability": capability,
                "task": task.name,
                "agent_version": agent.version,
                "candidate": task.candidate_label,
                "rule_id": decision.rule_id,
            },
        )
        context = AgentContext(
            task=task,
            agent=agent,
            tools=self.tools,
            router=self.router,
            witness=self.witness,
            governor=self.governor,
            state=self.state,
        )
        result = handler(context)
        missing = [item for item in agent.evidence_requirements if item not in (result.get("evidence") or {})]
        self.witness.append(
            agent.id,
            "agent.completed",
            {
                "capability": capability,
                "task": task.name,
                "candidate": task.candidate_label,
                "evidence_provided": sorted((result.get("evidence") or {}).keys()),
                "evidence_missing": missing,
            },
        )
        if missing:
            result.setdefault("warnings", []).append(f"missing required evidence: {', '.join(missing)}")
        return result
