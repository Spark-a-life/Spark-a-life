from __future__ import annotations
from pathlib import Path
import json
from jsonschema import Draft202012Validator
from .models import AssetRecord, BrandSpec, CreativeBrief, CreativeSpec, Mission, OutputSpec, RiskBudget

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / 'contracts' / 'mission.schema.json'

def validate_contract(data: dict) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    return [f"{'.'.join(str(x) for x in error.path)}: {error.message}" for error in errors]

def parse_brief(data: dict) -> CreativeBrief:
    errors = validate_contract(data)
    if errors:
        raise ValueError('Invalid mission contract: ' + '; '.join(errors))
    m = data['mission']; b = data['brand']; c = data['creative']; r = data['risk']; o = data['output']
    return CreativeBrief(
        mission=Mission(m['id'], m['objective'], m['audience'], m['channel'], m.get('industry')),
        brand=BrandSpec(b['name'], b['voice'], list(b['constraints'])),
        creative=CreativeSpec(c['format'], c['style'], c['message'], list(c['references'])),
        assets=[AssetRecord(a['id'], a['type'], a['source'], a['consent'], list(a['permitted_use'])) for a in data['assets']],
        risk=RiskBudget(
            maximum_cost_usd=float(r['maximum_cost_usd']), maximum_tokens=int(r['maximum_tokens']),
            maximum_runtime_seconds=int(r['maximum_runtime_seconds']), maximum_external_calls=int(r['maximum_external_calls']),
            maximum_retries=int(r['maximum_retries']), human_approval_required=bool(r.get('human_approval_required', True)),
            maximum_consecutive_similar_actions=int(r.get('maximum_consecutive_similar_actions', 3))
        ),
        output=OutputSpec(o['adapter'], list(o['deliverables'])), raw=data
    )
