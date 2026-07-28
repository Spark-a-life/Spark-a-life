from ..models import AdapterResult, CreativeBrief, EvaluationResult, GateDecision

WEIGHTS = {
    'fidelity': 0.20,
    'brand_fit': 0.15,
    'audience_fit': 0.15,
    'platform_readiness': 0.10,
    'provenance_integrity': 0.15,
    'safety': 0.15,
    'accessibility': 0.10,
}

def evaluate(brief: CreativeBrief, result: AdapterResult) -> EvaluationResult:
    scores = {k: 0.80 for k in WEIGHTS}
    if all(a.consent in {'owned','licensed','explicit'} for a in brief.assets):
        scores['provenance_integrity'] = 0.95
    else:
        scores['provenance_integrity'] = 0.25
    if 'manual' in result.execution_mode:
        scores['platform_readiness'] = 0.75
    if brief.brand.name.lower() in str(result.artefacts).lower() or brief.brand.name:
        scores['brand_fit'] = 0.85
    weighted = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    guidance = []
    if scores['provenance_integrity'] < 0.6:
        guidance.append('Resolve asset consent and permitted-use gaps before generation or publication.')
    if scores['platform_readiness'] < 0.8:
        guidance.append('Paste generated output reference back into the run record for final approval.')
    if weighted >= 0.82:
        decision = GateDecision.APPROVE
    elif weighted >= 0.60:
        decision = GateDecision.REVISE
    else:
        decision = GateDecision.BLOCK
    return EvaluationResult(scores=scores, weighted_score=round(weighted, 4), decision=decision, revision_guidance=guidance)
