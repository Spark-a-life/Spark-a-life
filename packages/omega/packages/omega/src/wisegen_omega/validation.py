from pathlib import Path
import json
from jsonschema import Draft202012Validator

def validate_mission(mission, schema_path=None):
    schema_path=Path(schema_path or Path(__file__).resolve().parents[2]/"schemas"/"mission.schema.json")
    schema=json.loads(schema_path.read_text(encoding="utf-8"))
    errors=sorted(Draft202012Validator(schema).iter_errors(mission),key=lambda e:list(e.path))
    return [f"{'/'.join(map(str,e.path)) or '<root>'}: {e.message}" for e in errors]
