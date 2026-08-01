from __future__ import annotations

from ..models import ComplianceFinding, MissionBrief

PUBLIC_DISCLOSURE_TERMS = {"charity portal", "public disclosure", "disclosure regime", "appeal details"}
FOREIGN_PERMIT_TERMS = {"permit", "coc permit", "foreign charitable purpose", "frfcp"}
PERSONAL_DATA_TERMS = {"consent", "pdpa", "personal data", "legitimate use", "notice"}
UNDUE_PRESSURE_TERMS = {
    "pressure",
    "guilt",
    "urgent or you fail",
    "must donate now",
    "shame",
    "fear-based",
}


def _contains_any(values: list[str], terms: set[str]) -> bool:
    joined = "\n".join(values).lower()
    return any(term in joined for term in terms)


def check_fundraising_governance(brief: MissionBrief) -> list[ComplianceFinding]:
    findings: list[ComplianceFinding] = []
    governance = brief.governance
    disclosures = governance.disclosure_requirements
    evidence_sources = [item.source for item in brief.evidence] + [item.title for item in brief.evidence]
    controls = disclosures + evidence_sources + [governance.donor_acceptance_policy]

    if governance.public_appeal and not _contains_any(controls, PUBLIC_DISCLOSURE_TERMS):
        findings.append(
            ComplianceFinding(
                status="revise",
                message=(
                    "Public fundraising appeal is enabled, but no disclosure control is mapped. "
                    "Add jurisdiction-specific disclosure evidence before public egress."
                ),
                severity="medium",
                related_item="governance.public_appeal",
            )
        )

    if governance.foreign_charitable_purpose and not _contains_any(controls, FOREIGN_PERMIT_TERMS):
        findings.append(
            ComplianceFinding(
                status="block",
                message=(
                    "Foreign charitable fundraising is enabled without a mapped permit or equivalent "
                    "jurisdiction-specific control."
                ),
                severity="high",
                related_item="governance.foreign_charitable_purpose",
            )
        )

    if governance.personal_data_used and not _contains_any(controls + brief.organisation.constraints, PERSONAL_DATA_TERMS):
        findings.append(
            ComplianceFinding(
                status="revise",
                message="Personal data use is enabled without an explicit consent, notice or PDPA-equivalent control.",
                severity="medium",
                related_item="governance.personal_data_used",
            )
        )

    if governance.vulnerable_audience and "compliance" not in governance.required_approvals:
        findings.append(
            ComplianceFinding(
                status="block",
                message="Vulnerable-audience fundraising requires compliance approval before outreach.",
                severity="high",
                related_item="governance.required_approvals",
            )
        )

    if "captain" not in governance.required_approvals:
        findings.append(
            ComplianceFinding(
                status="block",
                message="Captain approval is mandatory for all MAMT fundraising missions.",
                severity="high",
                related_item="governance.required_approvals",
            )
        )

    if any(channel in governance.egress_channels for channel in {"email", "linkedin", "data_room", "crm"}):
        if not brief.risk.human_approval_required:
            findings.append(
                ComplianceFinding(
                    status="block",
                    message="External egress channels require human approval to remain enabled.",
                    severity="high",
                    related_item="risk.human_approval_required",
                )
            )

    restricted_terms = [item.lower() for item in governance.restricted_terms]
    for claim in brief.claims:
        claim_lower = claim.text.lower()
        matched_restricted = [term for term in restricted_terms if term in claim_lower]
        if matched_restricted:
            findings.append(
                ComplianceFinding(
                    status="block" if claim.external_use else "revise",
                    message=f"Claim contains restricted governance term(s): {', '.join(matched_restricted)}",
                    severity="high" if claim.external_use else "medium",
                    related_item=claim.text,
                )
            )
        if claim.external_use and any(term in claim_lower for term in UNDUE_PRESSURE_TERMS):
            findings.append(
                ComplianceFinding(
                    status="block",
                    message="External outreach claim may create undue pressure; rewrite before use.",
                    severity="high",
                    related_item=claim.text,
                )
            )

    return findings
