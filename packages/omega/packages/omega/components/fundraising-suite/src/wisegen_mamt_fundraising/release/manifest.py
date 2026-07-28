from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

from .. import __version__
from ..io import write_json
from .preflight import run_preflight

EXCLUDED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "build", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip"}


def _included(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if relative.parts and relative.parts[0] == "outputs" and path.name != ".gitkeep":
        return False
    return path.is_file() and path.suffix not in EXCLUDED_SUFFIXES


def file_digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_release_manifest(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root).resolve()
    files = []
    for path in sorted(base.rglob("*")):
        if _included(path, base):
            files.append(
                {
                    "path": str(path.relative_to(base)),
                    "sha256": file_digest(path),
                    "bytes": path.stat().st_size,
                }
            )
    preflight = run_preflight(base)
    return {
        "name": "wisegen-mamt-fundraising-suite",
        "version": __version__,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "preflight_status": preflight.status,
        "file_count": len(files),
        "files": files,
        "preflight": asdict(preflight),
    }


def write_release_manifest(path: str | Path, root: str | Path = ".") -> dict[str, Any]:
    manifest = build_release_manifest(root)
    write_json(path, manifest)
    return manifest
