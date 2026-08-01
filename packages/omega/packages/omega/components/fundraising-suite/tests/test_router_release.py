from wisegen_mamt_fundraising.release.manifest import build_release_manifest
from wisegen_mamt_fundraising.release.preflight import run_preflight
from wisegen_mamt_fundraising.router import ModelRouter


def test_sensitive_tasks_route_locally():
    router = ModelRouter()
    decision = router.select_with_policy("compliance")
    assert decision.model_class == "local_deterministic"
    assert decision.allowed_external_call is False


def test_release_preflight_passes_for_current_repo():
    report = run_preflight(".")
    assert report.status == "pass"
    assert {item.name for item in report.checks} >= {"required_paths", "example_contracts", "version_alignment"}


def test_release_manifest_includes_hashes():
    manifest = build_release_manifest(".")
    assert manifest["version"] == "1.5.0"
    assert manifest["file_count"] > 0
    assert all("sha256" in item and len(item["sha256"]) == 64 for item in manifest["files"])
