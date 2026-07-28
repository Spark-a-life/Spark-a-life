from __future__ import annotations

from typing import Any

from ..models import AdapterResult, MissionBrief, RuntimeUsage
from .base import Adapter


class ManualBridgeAdapter(Adapter):
    name = "manual_bridge"
    execution_mode = "manual_review"

    def execute(self, brief: MissionBrief, artefacts: dict[str, Any]) -> AdapterResult:
        instructions = {
            "mission_id": brief.mission.id,
            "operator_steps": [
                "Review compliance findings and Captain Gate status.",
                "Copy only approved drafts into the chosen email, CRM, design or data-room surface.",
                "Do not send, publish or share until human approval is recorded.",
                "Paste resulting external references back into the run record for audit continuity.",
            ],
            "approved_for_external_egress": False,
            "artefacts_for_review": artefacts,
        }
        return AdapterResult(
            adapter=self.name,
            execution_mode=self.execution_mode,
            artefacts=instructions,
            usage=RuntimeUsage(tokens=len(str(artefacts).split()), runtime_seconds=1),
            notes=["Manual bridge used to avoid unsupported automation claims."],
        )
