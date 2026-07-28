from __future__ import annotations

from ..models import MissionBrief, ScoreBreakdown


def strategic_narrative(brief: MissionBrief) -> dict[str, object]:
    return {
        "one_line_thesis": (
            f"{brief.organisation.name} is raising {brief.mission.currency} "
            f"{brief.mission.funding_goal:,.0f} to expand: {brief.mission.programme_summary}"
        ),
        "audience": brief.mission.audience,
        "voice": brief.organisation.voice,
        "use_of_funds": list(brief.fundraising.use_of_funds),
        "proof_points": [claim.text for claim in brief.claims if claim.evidence_ids],
        "guardrail": "Use only approved proof points and avoid implying guaranteed funding outcomes.",
    }


def funder_memo(brief: MissionBrief, score: ScoreBreakdown) -> dict[str, object]:
    prospect = next(item for item in brief.prospects if item.name == score.prospect_name)
    return {
        "prospect": prospect.name,
        "type": prospect.type,
        "estimated_amount": prospect.estimated_amount,
        "fit_score": score.score,
        "fit_reasons": score.reasons,
        "risks": score.risks,
        "recommended_ask": min(prospect.estimated_amount, brief.mission.funding_goal),
        "memo": (
            f"Prioritise {prospect.name} if Captain Gate accepts the eligibility reading. "
            f"The strongest fit signals are: {'; '.join(score.reasons)}. "
            f"Restrictions to review: {'; '.join(score.risks) if score.risks else 'none identified in supplied brief'}."
        ),
    }
