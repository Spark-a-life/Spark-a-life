from wisegen_pip.io import load_data
from wisegen_pip.pipeline import repository_root
from wisegen_pip.validation import validate_project

def test_example_project_is_valid():
    root = repository_root()
    project = load_data(root / "examples" / "executive-brief" / "project.yaml")
    validate_project(project, root / "schemas" / "project.schema.json")
