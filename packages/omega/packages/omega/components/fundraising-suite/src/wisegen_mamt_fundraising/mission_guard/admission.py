from __future__ import annotations

from ..models import ComplianceFinding, MissionBrief

APPROVED_ADAPTERS = {"local_deterministic", "manual_bridge"}
APPROVED_CURRENCIES = {"SGD", "USD", "EUR", "GBP", "AUD"}


def admit_mission(brief: MissionBrief) -> list[ComplianceFinding]:
    findings: list[ComplianceFinding] = []
    if brief.output.adapter not in APPROVED_ADAPTERS:
        findings.append(
            ComplianceFinding(
                status="block",
                message=f"Adapter is not approved for this local-first suite: {brief.output.adapter}",
                severity="high",
                related_item="output.adapter",
            )
        )
    if brief.mission.currency not in APPROVED_CURRENCIES:
        findings.append(
            ComplianceFinding(
                status="revise",
                message=f"Currency is outside the default approved set: {brief.mission.currency}",
                severity="medium",
                related_item="mission.currency",
            )
        )
    if brief.risk.maximum_external_calls > 0 and brief.output.adapter == "local_deterministic":
        findings.append(
            ComplianceFinding(
                status="revise",
                message="Local deterministic runs should set maximum_external_calls to 0.",
                severity="medium",
                related_item="risk.maximum_external_calls",
            )
        )
    if brief.fundraising.minimum_fit_score < 0.4:
        findings.append(
            ComplianceFinding(
                status="revise",
                message="Minimum fit score is low; fundraising pipeline may become noisy.",
                severity="medium",
                related_item="fundraising.minimum_fit_score",
            )
        )
    if not brief.evidence:
        findings.append(
            ComplianceFinding(
                status="block",
                message="At least one evidence record is required.",
                severity="high",
                related_item="evidence",
            )
        )
    if not brief.claims:
        findings.append(
            ComplianceFinding(
                status="revise",
                message="No claim register supplied; funder-facing material may lack traceable assertions.",
                severity="medium",
                related_item="claims",
            )
        )
    if not brief.governance.donor_acceptance_policy.strip():
        findings.append(
            ComplianceFinding(
                status="block",
                message="A donor acceptance policy is required before fundraising execution.",
                severity="high",
                related_item="governance.donor_acceptance_policy",
            )
        )
    return findings
