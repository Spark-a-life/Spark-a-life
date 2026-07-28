from dataclasses import dataclass

@dataclass(frozen=True)
class RoleAgent:
    name: str
    purpose: str
    allowed_tools: list[str]
    approval_threshold: str
    mission_scope: str

DEFAULT_ROLES = [
    RoleAgent('creative_director','Owns creative intent and coherence',['brief_reader','prompt_compiler'],'medium','mission framing'),
    RoleAgent('brand_steward','Protects brand identity and channel fit',['brand_rules','evaluation_rubric'],'medium','brand and audience'),
    RoleAgent('reference_engineer','Reviews provenance and reference fitness',['asset_registry','provenance_checker'],'high','assets and references'),
    RoleAgent('prompt_compiler','Compiles model-specific prompt packs',['prompt_compiler'],'low','prompt generation'),
    RoleAgent('media_router','Selects eligible adapter',['model_router'],'medium','model routing'),
    RoleAgent('evaluation_agent','Scores outputs and revision guidance',['evaluator'],'medium','quality assessment'),
    RoleAgent('safety_governor','Enforces risk budgets and circuit states',['runtime_governor','circuit_breaker'],'high','operational safety'),
    RoleAgent('provenance_auditor','Writes witness-chain and consent records',['witness_chain','provenance_checker'],'high','audit and provenance'),
    RoleAgent('deployment_agent','Packages approved deliverables',['export_packager'],'high','deployment readiness'),
]
