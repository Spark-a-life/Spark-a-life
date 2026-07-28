from __future__ import annotations

from ..models import ComplianceFinding, Prospect


def check_contact_privacy(prospects: list[Prospect]) -> list[ComplianceFinding]:
    findings: list[ComplianceFinding] = []
    for prospect in prospects:
        source_lower = prospect.source.lower()
        if "private inbox" in source_lower or "personal phone" in source_lower:
            findings.append(
                ComplianceFinding(
                    status="revise",
                    message="Prospect source appears to include private contact context; confirm consent before outreach.",
                    severity="medium",
                    related_item=prospect.name,
                )
            )
    return findings
