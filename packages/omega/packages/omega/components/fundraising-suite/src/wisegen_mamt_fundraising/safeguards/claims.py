from __future__ import annotations

from ..models import Claim, ComplianceFinding, EvidenceItem

BLOCKED_PHRASES = [
    "guaranteed return",
    "risk-free",
    "assured funding",
    "confirmed grant",
    "automatic approval",
]


def check_claims(claims: list[Claim], evidence: list[EvidenceItem]) -> list[ComplianceFinding]:
    evidence_ids = {item.id for item in evidence}
    findings: list[ComplianceFinding] = []
    for claim in claims:
        lowered = claim.text.lower()
        blocked = next((phrase for phrase in BLOCKED_PHRASES if phrase in lowered), None)
        if blocked:
            findings.append(
                ComplianceFinding(
                    status="block",
                    message=f"Claim uses blocked phrase: {blocked}",
                    severity="high",
                    related_item=claim.text,
                )
            )
        missing = [item for item in claim.evidence_ids if item not in evidence_ids]
        if missing:
            findings.append(
                ComplianceFinding(
                    status="block" if claim.external_use else "revise",
                    message=f"Claim references missing evidence ids: {', '.join(missing)}",
                    severity="high" if claim.external_use else "medium",
                    related_item=claim.text,
                )
            )
        if claim.external_use and not claim.evidence_ids:
            findings.append(
                ComplianceFinding(
                    status="block",
                    message="External claim has no evidence mapping.",
                    severity="high",
                    related_item=claim.text,
                )
            )
    return findings
