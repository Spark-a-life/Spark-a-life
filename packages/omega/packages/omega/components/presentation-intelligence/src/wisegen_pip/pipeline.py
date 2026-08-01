from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from .adapters import LocalDeterministicAdapter
from .governance import create_witness, release_status
from .io import dump_json, load_data
from .models import RunResult
from .quality import evaluate
from .validation import validate_project

def repository_root():
    return Path(__file__).resolve().parents[2]

def run_project(project_path, adapter=None):
    project_path = Path(project_path).resolve()
    root = repository_root()
    project = load_data(project_path)
    validate_project(project, root / "schemas" / "project.schema.json")
    adapter = adapter or LocalDeterministicAdapter()
    context = {"project": project}
    context.update(adapter.generate("reasoning", context))
    context.update(adapter.generate("generation", context))

    env = Environment(
        loader=FileSystemLoader(root / "templates"),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True
    )
    artefact_text = env.get_template("executive-brief.md.j2").render(
        project=project["project"],
        intent=project["intent"],
        audience=project["audience"],
        evidence=project["evidence"],
        insights=context["insights"],
        sections=context["sections"]
    )

    build_dir = root / "build" / project["project"]["id"]
    build_dir.mkdir(parents=True, exist_ok=True)
    (build_dir / "artefact.md").write_text(artefact_text, encoding="utf-8")

    quality = evaluate(project, artefact_text, context["insights"])
    dump_json(build_dir / "quality-report.json", quality)
    witness = create_witness(project, project_path, artefact_text, quality)
    dump_json(build_dir / "witness-record.json", witness)
    status = release_status(project, quality["overall"])
    dump_json(build_dir / "release-manifest.json", {
        "project_id": project["project"]["id"],
        "release_status": status,
        "quality_score": quality["overall"],
        "release_threshold": project["workflow"]["release_threshold"],
        "human_approval_required": project["workflow"].get("require_human_approval", True),
        "files": ["artefact.md", "quality-report.json", "witness-record.json"]
    })
    return RunResult(str(build_dir), status, quality["overall"], witness["witness_id"])
