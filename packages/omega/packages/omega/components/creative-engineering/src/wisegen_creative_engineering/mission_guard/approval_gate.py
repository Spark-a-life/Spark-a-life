from ..models import EvaluationResult, GateDecision

def captain_gate(evaluation: EvaluationResult, human_approval_required: bool) -> GateDecision:
    if evaluation.decision == GateDecision.BLOCK:
        return GateDecision.BLOCK
    if human_approval_required and evaluation.decision == GateDecision.APPROVE:
        return GateDecision.REVISE
    return evaluation.decision
