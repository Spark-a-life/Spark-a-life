from wisegen_creative_engineering.models import RiskBudget, RuntimeUsage, CircuitState
from wisegen_creative_engineering.runtime_governor.governor import RuntimeGovernor


def test_governor_moves_to_red_on_repeated_actions():
    budget = RiskBudget(1, 1000, 100, 10, 2, False, maximum_consecutive_similar_actions=3)
    gov = RuntimeGovernor(budget)
    gov.record_action('same-tool-call')
    gov.record_action('same-tool-call')
    state = gov.record_action('same-tool-call')
    assert state == CircuitState.RED


def test_governor_moves_to_amber_on_budget_pressure():
    budget = RiskBudget(10, 1000, 100, 10, 2, False)
    gov = RuntimeGovernor(budget)
    state = gov.record_action('expensive-call', RuntimeUsage(cost_usd=8))
    assert state == CircuitState.AMBER
