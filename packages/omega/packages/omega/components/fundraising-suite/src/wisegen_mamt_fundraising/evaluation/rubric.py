from __future__ import annotations

from ..models import AdapterResult, ComplianceFinding, EvaluationResult, GateDecision, MissionBrief, ScoreBreakdown

WEIGHTS = {
    "mission_fit": 0.16,
    "funder_fit": 0.16,
    "evidence_integrity": 0.16,
    "financial_logic": 0.12,
    "compliance_safety": 0.16,
    "narrative_quality": 0.12,
    "operational_readiness": 0.12,
}


def evaluate(
    brief: MissionBrief,
    result: AdapterResult,
    scores: list[ScoreBreakdown],
    compliance_findings: list[ComplianceFinding],
) -> EvaluationResult:
    qualified = [item for item in scores if item.score >= brief.fundraising.minimum_fit_score]
    score_values = {
        "mission_fit": 0.86 if brief.mission.objective and brief.fundraising.use_of_funds else 0.55,
        "funder_fit": 0.88 if qualified else 0.45,
        "evidence_integrity": 0.90 if all(claim.evidence_ids for claim in brief.claims if claim.external_use) else 0.50,
        "financial_logic": 0.82 if brief.mission.funding_goal > 0 and brief.fundraising.use_of_funds else 0.50,
        "compliance_safety": 0.90 if not any(item.status == "block" for item in compliance_findings) else 0.30,
        "narrative_quality": 0.84 if "bundle" in result.artefacts else 0.60,
        "operational_readiness": 0.86 if result.execution_mode in {"deterministic", "manual_review"} else 0.62,
    }
    weighted = round(sum(score_values[key] * WEIGHTS[key] for key in WEIGHTS), 4)
    guidance: list[str] = []
    if not qualified:
        guidance.append("No prospect meets the configured minimum fit score; expand sourcing or lower priority assumptions with caution.")
    for finding in compliance_findings:
        if finding.status in {"block", "revise"}:
            guidance.append(f"{finding.severity.upper()}: {finding.message}")
    if weighted >= 0.84 and not any(item.status == "block" for item in compliance_findings):
        decision = GateDecision.APPROVE
    elif weighted >= 0.62 and not any(item.status == "block" for item in compliance_findings):
        decision = GateDecision.REVISE
    else:
        decision = GateDecision.BLOCK
    return EvaluationResult(score_values, weighted, decision, guidance)
