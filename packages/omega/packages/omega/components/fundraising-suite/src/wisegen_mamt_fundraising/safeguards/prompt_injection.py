from __future__ import annotations

from ..models import ComplianceFinding, MissionBrief

INJECTION_MARKERS = {
    "ignore previous instructions",
    "ignore all instructions",
    "system prompt",
    "developer message",
    "reveal secrets",
    "exfiltrate",
    "send credentials",
    "tool call",
    "run shell",
    "delete files",
    "disable safeguards",
}


def _scan_text(label: str, text: str) -> list[ComplianceFinding]:
    lowered = text.lower()
    findings: list[ComplianceFinding] = []
    for marker in sorted(INJECTION_MARKERS):
        if marker in lowered:
            findings.append(
                ComplianceFinding(
                    status="block",
                    message=f"Potential prompt-injection marker detected: {marker}",
                    severity="high",
                    related_item=label,
                )
            )
    return findings


def check_prompt_injection_surface(brief: MissionBrief) -> list[ComplianceFinding]:
    findings: list[ComplianceFinding] = []
    for prospect in brief.prospects:
        findings.extend(_scan_text(f"prospect:{prospect.name}:source", prospect.source))
        findings.extend(_scan_text(f"prospect:{prospect.name}:eligibility", prospect.eligibility_notes))
        findings.extend(_scan_text(f"prospect:{prospect.name}:relationship", prospect.relationship_signal))
    for item in brief.evidence:
        findings.extend(_scan_text(f"evidence:{item.id}:title", item.title))
        findings.extend(_scan_text(f"evidence:{item.id}:source", item.source))
    for claim in brief.claims:
        findings.extend(_scan_text("claim", claim.text))
    return findings
