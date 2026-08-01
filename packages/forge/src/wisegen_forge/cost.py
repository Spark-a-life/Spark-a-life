"""Cost Governor: an agent may not consume unlimited resource merely because it
is still technically active.

Budgets are multi-dimensional (tokens, tool calls, wall time, money) and are
enforced per project and per actor. Default currency is SGD, matching the
operating entity. Breaching a soft threshold raises an escalation; breaching a
hard cap stops execution.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

DIMENSIONS = ("tokens", "tool_calls", "seconds", "sgd")


class BudgetExceeded(RuntimeError):
    def __init__(self, dimension: str, used: float, cap: float, scope: str) -> None:
        super().__init__(
            f"budget exceeded on {dimension} for {scope}: {used:.4f} of {cap:.4f}"
        )
        self.dimension = dimension
        self.used = used
        self.cap = cap
        self.scope = scope


@dataclass
class Budget:
    tokens: float = 250_000
    tool_calls: float = 400
    seconds: float = 900
    sgd: float = 25.0
    escalate_at: float = 0.8

    def cap(self, dimension: str) -> float:
        return float(getattr(self, dimension))


@dataclass
class CostGovernor:
    project_budget: Budget = field(default_factory=Budget)
    actor_budgets: dict[str, Budget] = field(default_factory=dict)
    currency: str = "SGD"
    used: dict[str, dict[str, float]] = field(default_factory=dict)
    escalations: list[dict[str, Any]] = field(default_factory=list)

    def _bucket(self, scope: str) -> dict[str, float]:
        return self.used.setdefault(scope, {dim: 0.0 for dim in DIMENSIONS})

    def charge(self, actor: str, **amounts: float) -> dict[str, Any]:
        for dimension in amounts:
            if dimension not in DIMENSIONS:
                raise ValueError(f"unknown budget dimension: {dimension}")

        project = self._bucket("__project__")
        actor_bucket = self._bucket(actor)
        actor_budget = self.actor_budgets.get(actor, self.project_budget)

        for dimension, amount in amounts.items():
            project[dimension] += float(amount)
            actor_bucket[dimension] += float(amount)
            self._check(dimension, project[dimension], self.project_budget, "project")
            self._check(dimension, actor_bucket[dimension], actor_budget, actor)
        return self.snapshot()

    def _check(self, dimension: str, used: float, budget: Budget, scope: str) -> None:
        cap = budget.cap(dimension)
        if cap <= 0:
            return
        if used > cap:
            raise BudgetExceeded(dimension, used, cap, scope)
        if used >= cap * budget.escalate_at:
            record = {
                "scope": scope,
                "dimension": dimension,
                "used": round(used, 4),
                "cap": cap,
                "level": "escalation",
            }
            if record not in self.escalations:
                self.escalations.append(record)

    def snapshot(self) -> dict[str, Any]:
        project = self._bucket("__project__")
        return {
            "currency": self.currency,
            "project": {dim: round(project[dim], 4) for dim in DIMENSIONS},
            "caps": {dim: self.project_budget.cap(dim) for dim in DIMENSIONS},
            "by_actor": {
                actor: {dim: round(values[dim], 4) for dim in DIMENSIONS}
                for actor, values in self.used.items()
                if actor != "__project__"
            },
            "escalations": list(self.escalations),
        }

    def remaining(self, dimension: str) -> float:
        return self.project_budget.cap(dimension) - self._bucket("__project__")[dimension]
