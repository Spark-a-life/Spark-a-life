from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .io import read_json, read_yaml
from .models import MissionBrief

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA = ROOT / "contracts" / "fundraising_mission.schema.json"


class ContractError(ValueError):
    """Raised when a mission contract fails validation."""


def validate_payload(payload: dict[str, Any], schema_path: str | Path = DEFAULT_SCHEMA) -> None:
    schema = read_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.absolute_path))
    if errors:
        rendered = []
        for error in errors:
            location = "/".join(str(part) for part in error.absolute_path) or "root"
            rendered.append(f"{location}: {error.message}")
        raise ContractError("Mission contract validation failed: " + "; ".join(rendered))


def load_brief(path: str | Path, schema_path: str | Path = DEFAULT_SCHEMA) -> MissionBrief:
    payload = read_yaml(path)
    validate_payload(payload, schema_path)
    return MissionBrief.from_dict(payload)
