from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip"}


def should_include(path: Path) -> bool:
    if any(part in EXCLUDED_PARTS or part.endswith(".egg-info") for part in path.parts):
        return False
    if path.parts and path.parts[0] == "outputs" and path.name != ".gitkeep":
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return True


def export_zip(root: Path, output: Path) -> Path:
    root = root.resolve()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if path == output or not path.is_file() or not should_include(relative):
                continue
            archive.write(path, path.relative_to(root.parent))
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Export the repository as a portable zip archive.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="outputs/wisegen-mamt-fundraising-suite.zip")
    args = parser.parse_args()
    output = export_zip(Path(args.root), Path(args.output))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
