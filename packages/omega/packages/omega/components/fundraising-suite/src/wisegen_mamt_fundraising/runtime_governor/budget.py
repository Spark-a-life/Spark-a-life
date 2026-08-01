from __future__ import annotations

from dataclasses import dataclass

from ..models import RiskBudget, RuntimeUsage


@dataclass(frozen=True)
class BudgetStatus:
    within_budget: bool
    ratio: float
    messages: list[str]


def check_budget(budget: RiskBudget, usage: RuntimeUsage) -> BudgetStatus:
    checks = {
        "cost": (usage.cost_usd, budget.maximum_cost_usd),
        "tokens": (usage.tokens, budget.maximum_tokens),
        "runtime_seconds": (usage.runtime_seconds, budget.maximum_runtime_seconds),
        "external_calls": (usage.external_calls, budget.maximum_external_calls),
        "retries": (usage.retries, budget.maximum_retries),
        "consecutive_similar_actions": (
            usage.consecutive_similar_actions,
            budget.maximum_consecutive_similar_actions,
        ),
        "destructive_tools": (usage.destructive_tools, budget.maximum_destructive_tools),
    }
    ratios: list[float] = []
    messages: list[str] = []
    for name, (used, allowed) in checks.items():
        if allowed == 0:
            ratio = 1.0 if used == 0 else 999.0
        else:
            ratio = float(used) / float(allowed)
        ratios.append(ratio)
        if ratio > 1:
            messages.append(f"{name} exceeded: used {used}, allowed {allowed}")
    return BudgetStatus(within_budget=not messages, ratio=max(ratios), messages=messages)
