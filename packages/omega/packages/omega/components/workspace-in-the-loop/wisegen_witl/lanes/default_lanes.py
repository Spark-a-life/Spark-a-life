from __future__ import annotations

from typing import List

from wisegen_witl.core.models import LaneAssessment, WorkspaceState


def professor_lane(workspace: WorkspaceState) -> LaneAssessment:
    weak_evidence = [e.id for e in workspace.evidence if e.reliability < 0.6 or e.relevance < 0.6]
    risks = []
    if weak_evidence:
        risks.append(f"Weak or low-relevance evidence present: {', '.join(weak_evidence)}")
    return LaneAssessment(
        lane="Professor",
        finding="Evidence base is usable if low-quality sources are explicitly caveated.",
        confidence=0.82 if not weak_evidence else 0.66,
        risks=risks,
        recommendations=["Separate observed evidence from assumptions.", "Require citations or provenance for high-impact claims."],
    )


def general_lane(workspace: WorkspaceState) -> LaneAssessment:
    risks = []
    if len(workspace.options) < 2:
        risks.append("Insufficient options for meaningful comparison.")
    if not workspace.constraints:
        risks.append("No operational constraints declared.")
    return LaneAssessment(
        lane="General",
        finding="Execution feasibility depends on constraint clarity and option diversity.",
        confidence=0.78,
        risks=risks,
        recommendations=["Keep workflow steps executable within one operating cycle.", "Define owner, cadence, and fallback path."],
    )


def ceo_shadow_lane(workspace: WorkspaceState) -> LaneAssessment:
    risks = []
    commercial_keys = {"commercial_value", "lifetime_value", "budget_likelihood", "conversion_probability"}
    has_commercial = any(commercial_keys.intersection(o.features.keys()) for o in workspace.options)
    if not has_commercial:
        risks.append("Commercial viability signals are under-specified.")
    return LaneAssessment(
        lane="CEO-Shadow",
        finding="Decision should prioritise viable pathways, not merely technically elegant options.",
        confidence=0.8 if has_commercial else 0.62,
        risks=risks,
        recommendations=["Protect effort against low-value distraction.", "Prefer high-trust entry paths over cold volume."],
    )


def librarian_lane(workspace: WorkspaceState) -> LaneAssessment:
    orphan_options = [o.id for o in workspace.options if not o.evidence_ids]
    risks = []
    if orphan_options:
        risks.append(f"Options without linked evidence: {', '.join(orphan_options)}")
    return LaneAssessment(
        lane="Chief Librarian",
        finding="Traceability is adequate when each option maps to evidence and assumptions.",
        confidence=0.85 if not orphan_options else 0.64,
        risks=risks,
        recommendations=["Attach evidence IDs to every ranked option.", "Store workflow version with every decision."],
    )


def red_team_lane(workspace: WorkspaceState) -> LaneAssessment:
    risks = []
    if "leadgen" in workspace.domain.lower():
        risks.extend([
            "High-intent signals may be gamed by noisy public activity.",
            "Prospecting can become extractive if ethical fit is not scored.",
        ])
    if "media" in workspace.domain.lower() or "video" in workspace.domain.lower():
        risks.extend([
            "Visual appeal can mask factual weakness.",
            "Brand inconsistency may be missed if evaluation focuses only on generation quality.",
        ])
    if not risks:
        risks.append("Ranking metrics may become targets and degrade decision quality over time.")
    return LaneAssessment(
        lane="Red Team",
        finding="Ranking must be abuse-resistant and checked against Goodhart-style metric gaming.",
        confidence=0.88,
        risks=risks,
        recommendations=["Add adversarial review before high-impact execution.", "Review outcomes to detect proxy metric drift."],
    )


def run_default_lanes(workspace: WorkspaceState) -> List[LaneAssessment]:
    return [
        professor_lane(workspace),
        general_lane(workspace),
        ceo_shadow_lane(workspace),
        librarian_lane(workspace),
        red_team_lane(workspace),
    ]
