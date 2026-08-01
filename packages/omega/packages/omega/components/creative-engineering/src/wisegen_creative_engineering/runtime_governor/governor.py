from ..models import CircuitState, RiskBudget, RuntimeUsage
from .circuit_breaker import CircuitBreaker
from .loop_detector import LoopDetector

class RuntimeGovernor:
    def __init__(self, budget: RiskBudget):
        self.budget = budget
        self.usage = RuntimeUsage()
        self.loop_detector = LoopDetector(budget.maximum_consecutive_similar_actions)
        self.circuit_breaker = CircuitBreaker()
        self.state = CircuitState.GREEN

    def record_action(self, signature: str, usage_delta: RuntimeUsage | None = None, destructive_violation: bool = False) -> CircuitState:
        if usage_delta:
            self.usage.cost_usd += usage_delta.cost_usd
            self.usage.tokens += usage_delta.tokens
            self.usage.runtime_seconds += usage_delta.runtime_seconds
            self.usage.external_calls += usage_delta.external_calls
            self.usage.retries += usage_delta.retries
        loop = self.loop_detector.observe(signature)
        self.state = self.circuit_breaker.state_for(self.budget, self.usage, destructive_violation, loop)
        return self.state

    def assert_executable(self) -> None:
        if self.state in {CircuitState.RED, CircuitState.BLACK}:
            raise RuntimeError(f"Mission halted by runtime governor: {self.state.value}")
