from __future__ import annotations

from ..models import CaptainGateResult, ComplianceFinding, EvaluationResult, GateDecision, MissionBrief


def captain_gate(
    brief: MissionBrief,
    evaluation: EvaluationResult,
    compliance_findings: list[ComplianceFinding],
) -> CaptainGateResult:
    reasons: list[str] = []
    required_actions: list[str] = []
    if any(item.status == "block" for item in compliance_findings):
        reasons.extend(item.message for item in compliance_findings if item.status == "block")
        return CaptainGateResult(GateDecision.BLOCK, reasons, False, ["Resolve blocking compliance findings."])
    if evaluation.decision == GateDecision.BLOCK:
        return CaptainGateResult(GateDecision.BLOCK, evaluation.revision_guidance, False, ["Revise failed output set."])
    if brief.risk.human_approval_required:
        reasons.append("Human approval is required before external egress or CRM write.")
        required_actions.append("Review outreach drafts, claim register and data-room manifest.")
        return CaptainGateResult(GateDecision.PENDING_HUMAN_REVIEW, reasons, False, required_actions)
    if evaluation.decision == GateDecision.REVISE:
        return CaptainGateResult(GateDecision.REVISE, evaluation.revision_guidance, False, ["Revise and rerun QA evaluation."])
    return CaptainGateResult(GateDecision.APPROVE, ["All automated checks passed."], True, [])
