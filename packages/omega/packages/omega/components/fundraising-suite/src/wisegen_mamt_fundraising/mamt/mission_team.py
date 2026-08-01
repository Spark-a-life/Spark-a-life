from __future__ import annotations

from ..models import MissionBrief, RoleAgent, WorkPackage
from .roles import DEFAULT_ROLES


class MissionTeam:
    def __init__(self, roles: list[RoleAgent] | None = None):
        self.roles = roles or DEFAULT_ROLES

    def compile(self, brief: MissionBrief) -> list[WorkPackage]:
        packages: list[WorkPackage] = []
        for role in self.roles:
            packages.append(
                WorkPackage(
                    role=role.name,
                    purpose=role.purpose,
                    allowed_tools=list(role.allowed_tools),
                    approval_threshold=role.approval_threshold,
                    mission_scope=role.mission_scope,
                    mission_id=brief.mission.id,
                    output_contract=(
                        f"{role.name} must produce bounded, auditable output for "
                        f"mission {brief.mission.id} using only approved tools."
                    ),
                    escalation_rule="Escalate to Captain Gate on evidence gaps, egress, compliance ambiguity or budget breach.",
                )
            )
        return packages
