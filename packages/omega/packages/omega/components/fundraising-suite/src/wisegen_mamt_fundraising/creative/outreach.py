from __future__ import annotations

from ..models import MissionBrief, ScoreBreakdown


def email_draft(brief: MissionBrief, score: ScoreBreakdown) -> dict[str, str]:
    prospect = next(item for item in brief.prospects if item.name == score.prospect_name)
    subject = f"Potential alignment with {brief.organisation.name}'s programme expansion"
    body = (
        f"Hello,\n\n"
        f"I am reaching out on behalf of {brief.organisation.name}. We are preparing a fundraising "
        f"mission to support {brief.mission.programme_summary}\n\n"
        f"Your focus on {', '.join(prospect.focus_areas)} appears aligned with the programme direction. "
        f"We would value a short conversation to understand whether this fits your current priorities.\n\n"
        f"The current funding goal is {brief.mission.currency} {brief.mission.funding_goal:,.0f}. "
        f"Any formal claim or supporting document will be shared only after internal review and approval.\n\n"
        f"Warm regards,\n{brief.organisation.name}"
    )
    return {"subject": subject, "body": body, "approval_status": "draft_only_not_sent"}


def linkedin_draft(brief: MissionBrief) -> dict[str, str]:
    post = (
        f"We are designing a governed fundraising mission for {brief.mission.programme_summary}\n\n"
        f"The work is not just outreach. It requires prospect research, enrichment, narrative design, "
        f"financial logic, compliance review, evidence discipline, data-room readiness and careful tracking.\n\n"
        f"That is why we are treating fundraising as a Model-Agnostic Mission Team: one operator, specialist roles, "
        f"bounded tools, auditable evidence and human approval before external action."
    )
    return {"channel": "LinkedIn", "post": post, "approval_status": "draft_only_not_published"}


def visual_prompt_pack(brief: MissionBrief) -> dict[str, object]:
    prompt = (
        "Create a premium editorial systems visual showing a governed fundraising AI team. "
        "Include one human operator at the centre, surrounded by specialist role nodes: Sourcer, Enricher, "
        "Outreacher, Memo Writer, Data Room Curator, Tracker, Compliance Reviewer, Creative Director and Safeguard Governor. "
        "Represent Captain Gate, Evidence Layer, Model Router and Witness Chain as clear control layers. "
        "Style: polished strategic consulting diagram, clean typography, restrained visual hierarchy, suitable for LinkedIn."
    )
    return {
        "surface": "manual creative generation or design tool",
        "prompt": prompt,
        "negative_prompt": "No provider logos, no unverifiable statistics, no claims of guaranteed funding, no cluttered interface.",
        "paste_back_required": ["generated_asset_reference", "operator_notes", "approval_decision"],
        "approval_status": "manual_generation_requires_review",
    }
