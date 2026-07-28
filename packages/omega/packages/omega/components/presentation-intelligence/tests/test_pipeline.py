from pathlib import Path
from wisegen_pip.pipeline import repository_root, run_project

def test_pipeline_generates_outputs():
    root = repository_root()
    result = run_project(root / "examples" / "executive-brief" / "project.yaml")
    build = Path(result.build_dir)
    for name in ["artefact.md", "quality-report.json", "witness-record.json", "release-manifest.json"]:
        assert (build / name).exists()
    assert result.release_status == "review_required"
    assert result.quality_score >= 0.8
