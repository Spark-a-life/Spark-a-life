class LocalDeterministicAdapter:
    def generate(self, stage, context):
        project = context["project"]
        if stage == "reasoning":
            insights = []
            for item in project["evidence"]:
                if item["type"] in {"fact", "metric", "source"}:
                    insights.append({
                        "claim": item["title"],
                        "evidence_ids": [item["id"]],
                        "implication": item["content"],
                        "confidence": float(item.get("confidence", 0.7)),
                        "limitation": "Derived from one supplied evidence item."
                    })
            return {"insights": insights}
        if stage == "generation":
            intent = project["intent"]
            return {"sections": {
                "executive_summary": (
                    f"The artefact supports the decision: {intent['decision']} "
                    f"It uses {len(project['evidence'])} supplied evidence items and preserves "
                    "assumptions, quality scores and release status."
                ),
                "options": [
                    "Proceed with the proposed governed workflow.",
                    "Run a limited pilot with defined evaluation criteria.",
                    "Pause pending additional evidence or stakeholder validation."
                ],
                "recommendation": (
                    "Run a controlled pilot, measure quality against the declared success criteria, "
                    "and require human approval before external release."
                ),
                "next_steps": [
                    "Confirm the accountable owner and reviewer.",
                    "Execute the pilot workflow.",
                    "Review the quality report and witness record.",
                    "Approve, revise or reject through the Captain's Gate."
                ]
            }}
        return {}
