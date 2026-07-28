from __future__ import annotations

from ..models import CircuitState, RiskBudget, RuntimeUsage
from .budget import BudgetStatus, check_budget
from .circuit_breaker import circuit_state


class RuntimeGovernor:
    def __init__(self, budget: RiskBudget):
        self.budget = budget
        self.usage = RuntimeUsage()

    def record(self, usage: RuntimeUsage) -> CircuitState:
        self.usage = RuntimeUsage(
            cost_usd=self.usage.cost_usd + usage.cost_usd,
            tokens=self.usage.tokens + usage.tokens,
            runtime_seconds=self.usage.runtime_seconds + usage.runtime_seconds,
            external_calls=self.usage.external_calls + usage.external_calls,
            retries=self.usage.retries + usage.retries,
            consecutive_similar_actions=max(
                self.usage.consecutive_similar_actions,
                usage.consecutive_similar_actions,
            ),
            destructive_tools=self.usage.destructive_tools + usage.destructive_tools,
        )
        return circuit_state(self.budget, self.usage)

    def status(self) -> BudgetStatus:
        return check_budget(self.budget, self.usage)
