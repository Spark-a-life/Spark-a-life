from __future__ import annotations

from ..mission_guard.admission import admit_mission
from ..models import ComplianceFinding, MissionBrief
from .claims import check_claims
from .fundraising_compliance import check_fundraising_governance
from .privacy import check_contact_privacy
from .prompt_injection import check_prompt_injection_surface


def safeguard_review(brief: MissionBrief) -> list[ComplianceFinding]:
    findings: list[ComplianceFinding] = []
    findings.extend(admit_mission(brief))
    findings.extend(check_claims(brief.claims, brief.evidence))
    findings.extend(check_contact_privacy(brief.prospects))
    findings.extend(check_fundraising_governance(brief))
    findings.extend(check_prompt_injection_surface(brief))
    return findings
