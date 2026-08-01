from __future__ import annotations
from .roles import DEFAULT_ROLES, RoleAgent
from ..models import CreativeBrief

class MissionTeam:
    def __init__(self, roles: list[RoleAgent] | None = None):
        self.roles = roles or DEFAULT_ROLES

    def compile(self, brief: CreativeBrief) -> list[dict]:
        return [
            {
                'role': role.name,
                'purpose': role.purpose,
                'allowed_tools': role.allowed_tools,
                'approval_threshold': role.approval_threshold,
                'mission_scope': role.mission_scope,
                'mission_id': brief.mission.id,
                'handoff_contract': f"{role.name} must produce auditable output for {brief.output.adapter} without exceeding mission risk budget."
            }
            for role in self.roles
        ]
