from hashlib import sha256
from ..models import AdapterResult, CreativeBrief, PromptPack, RuntimeUsage
from .base import Adapter

class LocalDeterministicAdapter(Adapter):
    name = 'local_deterministic'
    execution_mode = 'deterministic'

    def execute(self, brief: CreativeBrief, prompt_pack: PromptPack) -> AdapterResult:
        digest = sha256(prompt_pack.prompt.encode('utf-8')).hexdigest()[:16]
        artefact = {
            'asset_id': f"local-{brief.mission.id}-{digest}",
            'creative_direction': prompt_pack.prompt,
            'quality_control': 'Deterministic text artefact for testing, governance rehearsal and CI.'
        }
        return AdapterResult(adapter=self.name, execution_mode=self.execution_mode, artefacts=artefact, usage=RuntimeUsage(tokens=len(prompt_pack.prompt.split()), runtime_seconds=1), notes=['No external model call performed.'])
