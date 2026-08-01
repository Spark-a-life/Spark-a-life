from __future__ import annotations

from .models import RouteDecision

ROUTING = {
    "strategy": "high_reasoning",
    "sourcing": "retrieval_synthesis",
    "enrichment": "high_reasoning",
    "narrative": "fast_drafting",
    "compliance": "high_reasoning",
    "finance": "high_reasoning",
    "evidence": "local_deterministic",
    "tracker": "local_deterministic",
    "creative": "fast_drafting",
    "audit": "local_deterministic",
    "red_team": "high_reasoning",
    "preflight": "local_deterministic",
}

SENSITIVE_TASKS = {"compliance", "evidence", "audit", "tracker", "preflight"}


class ModelRouter:
    def __init__(self, default_adapter: str = "local_deterministic"):
        self.default_adapter = default_adapter

    def select(self, task_type: str, sensitivity: str = "normal") -> str:
        return self.select_with_policy(task_type, sensitivity).model_class

    def select_with_policy(self, task_type: str, sensitivity: str = "normal") -> RouteDecision:
        normalised = task_type.strip().lower()
        if sensitivity == "high" or normalised in SENSITIVE_TASKS:
            return RouteDecision(
                task_type=normalised,
                model_class="local_deterministic",
                sensitivity=sensitivity,
                rationale="Sensitive, audit-critical or compliance-adjacent task is routed to local deterministic execution.",
                allowed_external_call=False,
            )
        model_class = ROUTING.get(normalised, self.default_adapter)
        external_allowed = model_class not in {"local_deterministic"}
        return RouteDecision(
            task_type=normalised,
            model_class=model_class,
            sensitivity=sensitivity,
            rationale="Route selected by task contract, expected reasoning depth and local-first policy.",
            allowed_external_call=external_allowed,
        )

    def route_table(self, task_types: list[str], sensitivity: str = "normal") -> list[RouteDecision]:
        return [self.select_with_policy(task_type, sensitivity) for task_type in task_types]
