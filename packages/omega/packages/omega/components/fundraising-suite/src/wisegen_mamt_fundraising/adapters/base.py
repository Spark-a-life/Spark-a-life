from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..models import AdapterResult, MissionBrief


class Adapter(ABC):
    name: str
    execution_mode: str

    @abstractmethod
    def execute(self, brief: MissionBrief, artefacts: dict[str, Any]) -> AdapterResult:
        raise NotImplementedError
