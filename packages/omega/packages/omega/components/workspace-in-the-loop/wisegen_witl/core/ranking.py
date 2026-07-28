from __future__ import annotations

from typing import Dict, List

from wisegen_witl.core.models import Criterion, Option, OptionScore


def _normalise(value: float, direction: str) -> float:
    clipped = max(0.0, min(1.0, float(value)))
    if direction == "min":
        return 1.0 - clipped
    return clipped


def rank_options(options: List[Option], criteria: List[Criterion]) -> List[OptionScore]:
    if not criteria:
        raise ValueError("Ranking requires at least one criterion.")
    total_weight = sum(c.weight for c in criteria)
    if total_weight <= 0:
        raise ValueError("Total criteria weight must be greater than zero.")

    results: List[OptionScore] = []
    for option in options:
        criterion_scores: Dict[str, float] = {}
        weighted_total = 0.0
        missing = []
        for criterion in criteria:
            raw = option.features.get(criterion.id)
            if raw is None:
                raw = 0.0
                missing.append(criterion.id)
            score = _normalise(raw, criterion.direction)
            criterion_scores[criterion.id] = round(score, 4)
            weighted_total += score * criterion.weight
        total = weighted_total / total_weight
        confidence = max(0.1, 1.0 - (0.08 * len(missing)))
        rationale = f"Weighted score {total:.3f} across {len(criteria)} criteria."
        if missing:
            rationale += f" Missing feature values treated as zero: {', '.join(missing)}."
        results.append(OptionScore(
            option_id=option.id,
            option_name=option.name,
            total_score=round(total, 4),
            criterion_scores=criterion_scores,
            rationale=rationale,
            confidence=round(confidence, 4),
        ))
    return sorted(results, key=lambda x: x.total_score, reverse=True)
