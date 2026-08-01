from __future__ import annotations

from ..models import CircuitState, RiskBudget, RuntimeUsage
from .budget import check_budget


def circuit_state(budget: RiskBudget, usage: RuntimeUsage) -> CircuitState:
    status = check_budget(budget, usage)
    if usage.destructive_tools > budget.maximum_destructive_tools:
        return CircuitState.BLACK
    if not status.within_budget:
        return CircuitState.RED
    if status.ratio >= 0.95:
        return CircuitState.RED
    if status.ratio >= 0.75:
        return CircuitState.AMBER
    return CircuitState.GREEN
