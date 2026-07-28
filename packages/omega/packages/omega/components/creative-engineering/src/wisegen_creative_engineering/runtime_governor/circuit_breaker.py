from ..models import CircuitState, RiskBudget, RuntimeUsage
from .budget import highest_budget_ratio

class CircuitBreaker:
    def __init__(self, amber: float = 0.75, red: float = 0.95):
        self.amber = amber
        self.red = red

    def state_for(self, budget: RiskBudget, usage: RuntimeUsage, destructive_violation: bool = False, loop_detected: bool = False) -> CircuitState:
        if destructive_violation:
            return CircuitState.BLACK
        ratio = highest_budget_ratio(budget, usage)
        if loop_detected or ratio >= self.red:
            return CircuitState.RED
        if ratio >= self.amber:
            return CircuitState.AMBER
        return CircuitState.GREEN
