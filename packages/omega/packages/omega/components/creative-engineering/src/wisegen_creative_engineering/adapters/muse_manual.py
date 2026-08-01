from ..models import AdapterResult, CreativeBrief, PromptPack, RuntimeUsage
from .base import Adapter

class MuseManualAdapter(Adapter):
    name = 'muse_manual'
    execution_mode = 'manual_bridge'

    def execute(self, brief: CreativeBrief, prompt_pack: PromptPack) -> AdapterResult:
        instructions = {
            'surface': 'Meta AI, Instagram or WhatsApp, depending on availability',
            'operator_steps': [
                'Open the selected Meta surface.',
                'Attach only approved reference assets listed in the mission contract.',
                'Paste the prompt pack exactly as compiled.',
                'Apply the negative prompt as constraints where the interface supports it.',
                'Save generated media and paste the output reference back into the run record.'
            ],
            'prompt': prompt_pack.prompt,
            'negative_prompt': prompt_pack.negative_prompt,
            'paste_back_required': prompt_pack.paste_back_required,
        }
        return AdapterResult(adapter=self.name, execution_mode=self.execution_mode, artefacts=instructions, usage=RuntimeUsage(tokens=len(prompt_pack.prompt.split()) * 2, runtime_seconds=1), notes=['Manual bridge used because no public Muse API is assumed.'])
