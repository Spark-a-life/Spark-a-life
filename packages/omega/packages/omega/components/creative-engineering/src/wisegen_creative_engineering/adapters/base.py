from abc import ABC, abstractmethod
from ..models import AdapterResult, CreativeBrief, PromptPack

class Adapter(ABC):
    name: str
    execution_mode: str

    @abstractmethod
    def execute(self, brief: CreativeBrief, prompt_pack: PromptPack) -> AdapterResult:
        raise NotImplementedError
