from __future__ import annotations

from typing import Dict, List


def generate_hypotheses(objective: str, constraints: List[str]) -> List[str]:
    joined = "; ".join(constraints) if constraints else "no declared constraints"
    return [
        f"The best option should directly advance the objective: {objective}.",
        f"The best option must remain feasible under constraints: {joined}.",
        "The best option should remain defensible under audit and retrospective review.",
    ]


def summarise_report(report: Dict) -> str:
    return f"{report.get('recommendation', '')} Gate: {report.get('captain_gate', {}).get('status', 'unknown')}."
