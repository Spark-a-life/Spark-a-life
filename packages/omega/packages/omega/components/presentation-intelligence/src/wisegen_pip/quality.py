def evaluate(project, artefact_text, insights):
    criteria = {
        "intent_alignment": 1.0 if project["intent"]["decision"] in artefact_text else 0.5,
        "evidence_coverage": min(1.0, len(insights) / max(1, len(project["evidence"]))),
        "required_sections": sum(
            1 for heading in [
                "Executive Summary", "Decision Required", "Evidence", "Analysis",
                "Options", "Recommendation", "Risks", "Next Steps"
            ] if f"## {heading}" in artefact_text
        ) / 8.0,
        "governance_readiness": 1.0 if project["workflow"].get("require_human_approval", True) else 0.8,
        "actionability": 1.0 if "## Next Steps" in artefact_text else 0.0
    }
    overall = sum(criteria.values()) / len(criteria)
    remediation = [f"Improve {k.replace('_', ' ')}." for k, v in criteria.items() if v < 0.8]
    return {"criteria": criteria, "overall": round(overall, 4), "remediation": remediation}
