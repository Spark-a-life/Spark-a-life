from jsonschema import Draft202012Validator
from .io import load_data

class ProjectValidationError(ValueError):
    pass

def validate_project(project, schema_path):
    schema = load_data(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(project), key=lambda e: list(e.path))
    if errors:
        rendered = []
        for error in errors:
            location = ".".join(str(x) for x in error.path) or "<root>"
            rendered.append(f"{location}: {error.message}")
        raise ProjectValidationError("\n".join(rendered))
