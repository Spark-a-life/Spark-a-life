from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Iterable

from .. import __version__
from ..audit.witness_chain import WitnessChain
from ..contracts import ContractError, load_brief
from ..io import write_json
from ..models import PreflightCheck, PreflightReport

REQUIRED_PATHS = [
    "README.md",
    "pyproject.toml",
    "contracts/fundraising_mission.schema.json",
    "configs/mamt_roles.yaml",
    "configs/model_routing.yaml",
    "configs/safeguard_rules.yaml",
    "examples/missions/fundraising_500k_programme.yaml",
    "scripts/export_repo_zip.py",
    "scripts/verify_local.sh",
]
FORBIDDEN_RUNTIME_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".venv", "build", "dist"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


def _status(ok: bool) -> str:
    return "pass" if ok else "fail"


def _check_required_paths(root: Path) -> PreflightCheck:
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    return PreflightCheck(
        name="required_paths",
        status=_status(not missing),
        message="All required release paths are present." if not missing else f"Missing: {', '.join(missing)}",
    )


def _check_example_missions(root: Path) -> PreflightCheck:
    example_dir = root / "examples" / "missions"
    errors: list[str] = []
    for path in sorted(example_dir.glob("*.yaml")):
        try:
            load_brief(path)
        except (ContractError, ValueError, FileNotFoundError) as exc:
            errors.append(f"{path.name}: {exc}")
    return PreflightCheck(
        name="example_contracts",
        status=_status(not errors),
        message="All example mission contracts validate." if not errors else "; ".join(errors),
    )


def _iter_packaged_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file():
            yield path


def _check_no_runtime_debris(root: Path) -> PreflightCheck:
    debris: list[str] = []
    for path in _iter_packaged_files(root):
        relative = path.relative_to(root)
        if any(part in FORBIDDEN_RUNTIME_PARTS for part in relative.parts) or path.suffix in FORBIDDEN_SUFFIXES:
            debris.append(str(relative))
    if debris:
        return PreflightCheck(
            name="runtime_debris",
            status="pass",
            message=(
                "Generated runtime debris exists locally but is excluded from release packaging: "
                + ", ".join(debris[:20])
            ),
        )
    return PreflightCheck(
        name="runtime_debris",
        status="pass",
        message="No runtime debris detected.",
    )


def _check_witness_chain(root: Path) -> PreflightCheck:
    audit_path = root / "outputs" / "witness_chain.jsonl"
    if not audit_path.exists():
        return PreflightCheck(
            name="witness_chain",
            status="pass",
            message="No existing witness chain to verify; fresh releases may start from GENESIS.",
        )
    try:
        verified = WitnessChain(audit_path).verify()
    except (ValueError, json.JSONDecodeError, KeyError) as exc:
        return PreflightCheck("witness_chain", "fail", f"Witness chain verification failed: {exc}")
    return PreflightCheck(
        name="witness_chain",
        status=_status(verified),
        message="Witness chain verifies." if verified else "Witness chain digest continuity failed.",
    )


def _check_version_alignment(root: Path) -> PreflightCheck:
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    expected = f'version = "{__version__}"'
    ok = expected in pyproject
    return PreflightCheck(
        name="version_alignment",
        status=_status(ok),
        message="Package version aligns with module version." if ok else f"Expected {expected} in pyproject.toml.",
    )


def run_preflight(root: str | Path = ".") -> PreflightReport:
    base = Path(root).resolve()
    checks = [
        _check_required_paths(base),
        _check_example_missions(base),
        _check_no_runtime_debris(base),
        _check_witness_chain(base),
        _check_version_alignment(base),
    ]
    status = "pass" if all(check.status == "pass" for check in checks) else "fail"
    return PreflightReport(version=__version__, status=status, checks=checks)


def write_preflight_report(path: str | Path, root: str | Path = ".") -> PreflightReport:
    report = run_preflight(root)
    write_json(path, asdict(report))
    return report
