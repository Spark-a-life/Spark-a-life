from __future__ import annotations

from typing import List

from wisegen_witl.core.models import LaneAssessment, OptionScore, RiskAssessment


def assess_risk(ranking: List[OptionScore], lanes: List[LaneAssessment], gate_threshold: float) -> RiskAssessment:
    risks: List[str] = []
    for lane in lanes:
        risks.extend(lane.risks)

    top_confidence = ranking[0].confidence if ranking else 0.0
    uncertainty_penalty = max(0.0, 1.0 - top_confidence)
    risk_density = min(1.0, len(risks) / 10.0)
    risk_score = round((0.55 * risk_density) + (0.45 * uncertainty_penalty), 4)

    if risk_score >= 0.67:
        level = "high"
    elif risk_score >= 0.34:
        level = "medium"
    else:
        level = "low"

    return RiskAssessment(
        level=level,
        score=risk_score,
        risks=risks,
        gate_required=risk_score >= gate_threshold,
    )


def captain_gate_decision(risk: RiskAssessment, decision_authority: str) -> dict:
    if risk.gate_required:
        return {
            "status": "requires_human_approval",
            "authority": decision_authority,
            "reason": f"Risk level {risk.level} with score {risk.score} exceeds configured gate threshold.",
            "auto_execute": False,
        }
    return {
        "status": "approved_for_low_risk_execution",
        "authority": decision_authority,
        "reason": "Risk is within configured threshold.",
        "auto_execute": True,
    }
