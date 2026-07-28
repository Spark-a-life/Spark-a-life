from ..models import RiskBudget, RuntimeUsage

def budget_ratios(budget: RiskBudget, usage: RuntimeUsage) -> dict[str, float]:
    return {
        'cost': usage.cost_usd / budget.maximum_cost_usd if budget.maximum_cost_usd else 1.0,
        'tokens': usage.tokens / budget.maximum_tokens,
        'runtime': usage.runtime_seconds / budget.maximum_runtime_seconds,
        'external_calls': usage.external_calls / max(1, budget.maximum_external_calls),
        'retries': usage.retries / max(1, budget.maximum_retries),
    }

def highest_budget_ratio(budget: RiskBudget, usage: RuntimeUsage) -> float:
    return max(budget_ratios(budget, usage).values())
