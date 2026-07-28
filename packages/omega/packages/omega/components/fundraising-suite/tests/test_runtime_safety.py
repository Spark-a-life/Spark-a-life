from wisegen_mamt_fundraising.models import RiskBudget, RuntimeUsage
from wisegen_mamt_fundraising.runtime_governor.circuit_breaker import circuit_state
from wisegen_mamt_fundraising.runtime_governor.loop_detector import LoopDetector


def test_circuit_breaker_turns_red_on_budget_excess():
    budget = RiskBudget(1, 100, 10, 0, 1, human_approval_required=False)
    assert circuit_state(budget, RuntimeUsage(cost_usd=2)).value == "red"


def test_loop_detector_flags_repetition():
    detector = LoopDetector(window=4, maximum_repeats=3)
    assert detector.observe("same action") is False
    assert detector.observe("same action") is False
    assert detector.observe("same action") is True
