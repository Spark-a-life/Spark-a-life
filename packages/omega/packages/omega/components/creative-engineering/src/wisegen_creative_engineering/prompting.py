from .models import CreativeBrief, PromptPack

def compile_prompt_pack(brief: CreativeBrief) -> PromptPack:
    governance = [
        'Use only assets with declared consent and permitted use.',
        'Do not imitate private individuals or unverified public-profile assets.',
        'Preserve brand constraints and channel suitability.',
    ] + brief.brand.constraints
    prompt = f"""
Objective: {brief.mission.objective}
Audience: {brief.mission.audience}
Channel: {brief.mission.channel}
Brand: {brief.brand.name}
Brand voice: {brief.brand.voice}
Format: {brief.creative.format}
Creative style: {brief.creative.style}
Core message: {brief.creative.message}
References to consider: {', '.join(brief.creative.references) or 'None'}
Deliverables: {', '.join(brief.output.deliverables)}
Governance: {'; '.join(governance)}
Produce a polished creative direction that is usable for the specified platform and does not rely on undeclared assets.
""".strip()
    negative = 'No unauthorised likeness, no unlicensed logos, no misleading claims, no unreadable text, no invented endorsements.'
    return PromptPack(adapter=brief.output.adapter, title=f"{brief.mission.id} prompt pack", prompt=prompt, negative_prompt=negative, paste_back_required=['generated_asset_reference','model_notes','human_reviewer'], governance_notes=governance)
