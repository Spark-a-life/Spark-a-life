from __future__ import annotations

from ..models import MissionBrief, Prospect, ScoreBreakdown

NEGATIVE_TERMS = {"not eligible", "ineligible", "closed", "no unsolicited", "invite only"}
POSITIVE_RELATIONSHIP_TERMS = {"warm", "introduced", "known", "prior", "partner", "existing"}


def score_prospect(brief: MissionBrief, prospect: Prospect) -> ScoreBreakdown:
    reasons: list[str] = []
    risks: list[str] = []
    mission_terms = {term.lower() for term in brief.fundraising.segments}
    focus_terms = {term.lower() for term in prospect.focus_areas}
    overlap = mission_terms.intersection(focus_terms)
    score = 0.25
    if overlap:
        increment = min(0.30, 0.10 * len(overlap))
        score += increment
        reasons.append(f"Focus overlap: {', '.join(sorted(overlap))}")
    if prospect.region.lower() in brief.mission.region.lower() or brief.mission.region.lower() in prospect.region.lower():
        score += 0.12
        reasons.append("Regional fit is aligned.")
    if any(term in prospect.relationship_signal.lower() for term in POSITIVE_RELATIONSHIP_TERMS):
        score += 0.14
        reasons.append("Relationship signal is warm or institutionally relevant.")
    if prospect.estimated_amount >= brief.mission.funding_goal * 0.15:
        score += 0.14
        reasons.append("Potential contribution is material relative to the funding goal.")
    if prospect.giving_history.strip():
        score += 0.08
        reasons.append("Giving history is available for review.")
    lowered_eligibility = prospect.eligibility_notes.lower()
    if any(term in lowered_eligibility for term in NEGATIVE_TERMS):
        score -= 0.35
        risks.append("Eligibility notes contain a negative or restricted access signal.")
    if prospect.restrictions:
        score -= min(0.12, 0.04 * len(prospect.restrictions))
        risks.append("Restrictions require compliance review.")
    score = max(0.0, min(1.0, round(score, 4)))
    if score >= brief.fundraising.minimum_fit_score:
        stage = "qualified"
    elif risks:
        stage = "nurture"
    else:
        stage = "discovered"
    if not reasons:
        reasons.append("Insufficient positive evidence; keep in low-priority research queue.")
    return ScoreBreakdown(prospect.name, score, reasons, risks, stage)


def rank_prospects(brief: MissionBrief) -> list[ScoreBreakdown]:
    return sorted((score_prospect(brief, prospect) for prospect in brief.prospects), key=lambda item: item.score, reverse=True)
