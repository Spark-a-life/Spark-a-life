from __future__ import annotations

from ..models import DonorDueDiligenceResult, MissionBrief, Prospect

HIGH_RISK_TERMS = {
    "sanction",
    "bribery",
    "corruption",
    "money laundering",
    "fraud",
    "political condition",
    "conflict of interest",
    "undisclosed beneficial owner",
}
MEDIUM_RISK_TERMS = {
    "restricted use",
    "brand activation",
    "naming rights",
    "exclusive rights",
    "sensitive sector",
    "requires consent",
}


def review_prospect_due_diligence(brief: MissionBrief, prospect: Prospect) -> DonorDueDiligenceResult:
    flags: list[str] = []
    required_actions: list[str] = []
    combined = " ".join(
        [
            prospect.name,
            prospect.type,
            prospect.region,
            prospect.eligibility_notes,
            prospect.giving_history,
            prospect.relationship_signal,
            prospect.source,
            " ".join(prospect.restrictions),
        ]
    ).lower()

    for term in sorted(HIGH_RISK_TERMS):
        if term in combined:
            flags.append(f"High-risk donor signal: {term}")
    for term in sorted(MEDIUM_RISK_TERMS):
        if term in combined:
            flags.append(f"Review donor condition: {term}")

    if not prospect.source.strip():
        flags.append("Missing source trace")
    if "cold" in prospect.relationship_signal.lower():
        flags.append("Cold relationship signal")
    if prospect.estimated_amount <= 0:
        flags.append("No estimated amount supplied")
    if prospect.estimated_amount >= brief.mission.funding_goal * 0.5:
        flags.append("Concentration risk: prospect could represent 50 percent or more of funding goal")

    if any(flag.startswith("High-risk") for flag in flags):
        risk_level = "high"
        recommendation = "escalate_before_acceptance"
        required_actions.extend(["Compliance review", "Captain review", "Document acceptance rationale"])
    elif flags:
        risk_level = "medium"
        recommendation = "accept_with_conditions"
        required_actions.extend(["Review restrictions", "Confirm fit with donor acceptance policy"])
    else:
        risk_level = "low"
        recommendation = "eligible_for_standard_review"
        required_actions.append("Proceed through standard Captain Gate")

    if brief.governance.foreign_charitable_purpose:
        required_actions.append("Confirm foreign charitable purpose permit or equivalent approval")
    if brief.governance.personal_data_used:
        required_actions.append("Confirm lawful personal-data basis before outreach")

    return DonorDueDiligenceResult(
        prospect_name=prospect.name,
        risk_level=risk_level,
        acceptance_recommendation=recommendation,
        flags=flags,
        required_actions=sorted(set(required_actions)),
    )


def review_due_diligence(brief: MissionBrief) -> list[DonorDueDiligenceResult]:
    return [review_prospect_due_diligence(brief, prospect) for prospect in brief.prospects]
