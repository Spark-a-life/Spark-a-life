from __future__ import annotations


def handoff_record(from_role: str, to_role: str, artefact: str, checks: list[str]) -> dict[str, object]:
    if not from_role or not to_role or not artefact:
        raise ValueError("from_role, to_role and artefact are required")
    return {
        "from": from_role,
        "to": to_role,
        "artefact": artefact,
        "required_checks": checks,
        "status": "ready_for_review",
    }
