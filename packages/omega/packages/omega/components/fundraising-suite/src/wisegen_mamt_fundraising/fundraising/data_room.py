from __future__ import annotations

from ..models import EvidenceItem, MissionBrief

REQUIRED_SECTIONS = [
    "Organisation Profile",
    "Programme Design",
    "Impact Evidence",
    "Financials and Budget",
    "Governance and Policies",
    "Case Studies",
    "Funder-Specific Packs",
    "Audit Trail",
]


def evidence_manifest(brief: MissionBrief) -> list[dict[str, object]]:
    return [
        {
            "id": item.id,
            "title": item.title,
            "kind": item.kind,
            "confidence": item.confidence,
            "permitted_use": item.permitted_use,
            "source": item.source,
        }
        for item in brief.evidence
    ]


def data_room_checklist(brief: MissionBrief) -> dict[str, object]:
    mapped: dict[str, list[EvidenceItem]] = {section: [] for section in REQUIRED_SECTIONS}
    for item in brief.evidence:
        kind = item.kind.lower()
        if "impact" in kind:
            mapped["Impact Evidence"].append(item)
        elif "budget" in kind or "financial" in kind:
            mapped["Financials and Budget"].append(item)
        elif "policy" in kind or "governance" in kind:
            mapped["Governance and Policies"].append(item)
        elif "case" in kind:
            mapped["Case Studies"].append(item)
        elif "programme" in kind or "program" in kind:
            mapped["Programme Design"].append(item)
        else:
            mapped["Organisation Profile"].append(item)
    return {
        "root": f"data_room/{brief.mission.id}",
        "sections": [
            {
                "section": section,
                "status": "ready" if records else "needs_input",
                "evidence_ids": [record.id for record in records],
            }
            for section, records in mapped.items()
        ],
        "release_rule": "No data-room release without Captain Gate approval and funder-specific access review.",
    }
