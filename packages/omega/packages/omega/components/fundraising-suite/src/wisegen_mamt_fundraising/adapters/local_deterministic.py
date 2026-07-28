from __future__ import annotations

from hashlib import sha256
import json
from typing import Any

from ..models import AdapterResult, MissionBrief, RuntimeUsage
from .base import Adapter


class LocalDeterministicAdapter(Adapter):
    name = "local_deterministic"
    execution_mode = "deterministic"

    def execute(self, brief: MissionBrief, artefacts: dict[str, Any]) -> AdapterResult:
        serialised = json.dumps(artefacts, sort_keys=True, ensure_ascii=False)
        digest = sha256(serialised.encode("utf-8")).hexdigest()[:16]
        output = {
            "asset_id": f"fundraising-{brief.mission.id}-{digest}",
            "mission_id": brief.mission.id,
            "artefact_digest": digest,
            "execution_summary": "Deterministic local artefact bundle generated for governance review.",
            "bundle": artefacts,
        }
        return AdapterResult(
            adapter=self.name,
            execution_mode=self.execution_mode,
            artefacts=output,
            usage=RuntimeUsage(tokens=max(1, len(serialised.split())), runtime_seconds=1),
            notes=["No external model call performed."],
        )
