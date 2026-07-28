from __future__ import annotations

from ..models import MissionBrief


def funding_gap_analysis(brief: MissionBrief, qualified_amount: float) -> dict[str, object]:
    goal = brief.mission.funding_goal
    gap = max(0.0, goal - qualified_amount)
    coverage_ratio = 0.0 if goal == 0 else min(1.0, qualified_amount / goal)
    return {
        "goal": goal,
        "currency": brief.mission.currency,
        "qualified_pipeline_amount": round(qualified_amount, 2),
        "funding_gap": round(gap, 2),
        "coverage_ratio": round(coverage_ratio, 4),
        "use_of_funds": list(brief.fundraising.use_of_funds),
        "financial_note": "Pipeline value is indicative; commitments require human confirmation and funder due diligence.",
    }
