def handoff_record(from_role: str, to_role: str, artefact: str, checks: list[str]) -> dict:
    return {'from': from_role, 'to': to_role, 'artefact': artefact, 'required_checks': checks, 'status': 'ready'}
