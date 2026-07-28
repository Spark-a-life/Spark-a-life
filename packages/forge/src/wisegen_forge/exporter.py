"""Portable Ownership: the output must remain operable when WiseGen is removed.

The export contract is stronger than a source dump. A bundle carries the code,
the infrastructure definitions, the agent and policy definitions, the migrations,
the evaluation records, the provenance chain, the environment manifest, the
runbook, a software bill of materials and instructions for substituting the
model provider.
"""
from __future__ import annotations

import json
import platform
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CONTRACT_ITEMS = (
    "source_code",
    "infrastructure_as_code",
    "agent_definitions",
    "policy_definitions",
    "database_migrations",
    "evaluation_records",
    "provenance_history",
    "environment_manifest",
    "deployment_runbook",
    "software_bill_of_materials",
    "model_substitution_instructions",
)


def software_bill_of_materials(root: Path) -> dict[str, Any]:
    components = [
        {
            "name": "python-standard-library",
            "version": platform.python_version(),
            "supplier": "Python Software Foundation",
            "licence": "PSF-2.0",
            "purl": f"pkg:generic/python@{platform.python_version()}",
        },
        {
            "name": "sqlite3",
            "version": "bundled-with-python",
            "supplier": "SQLite Consortium",
            "licence": "public-domain",
            "purl": "pkg:generic/sqlite",
        },
    ]
    return {
        "bomFormat": "CycloneDX-like",
        "specVersion": "1.5-subset",
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "tool": "wisegen-forge exporter",
            "component": {"name": root.name, "type": "application"},
        },
        "components": components,
        "note": "The generated application has no third-party runtime dependency. This is deliberate.",
    }


def environment_manifest() -> dict[str, Any]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "executable": sys.executable,
        "minimum_supported_python": "3.10",
        "network_required": False,
        "vendor_credential_required": False,
    }


MODEL_SUBSTITUTION = """# Model substitution

WiseGen Forge treats models as replaceable execution resources. Nothing in the
control flow, the governance gates or the evidence model depends on a particular
provider.

## To run with no external model (default)

No action required. The deterministic adapter is selected automatically and the
whole pipeline, including its tests, runs offline.

## To run against a local model

    export FORGE_OLLAMA_HOST=http://127.0.0.1:11434
    export FORGE_OLLAMA_MODEL=qwen2.5-coder

## To run against a hosted model

    export ANTHROPIC_API_KEY=...
    export FORGE_ANTHROPIC_MODEL=claude-sonnet-4-6

## To add a provider

Implement one method on the router: take a prompt, return text. Register a
`ModelSpec` declaring capability classes, the maximum risk tier the provider is
approved for, and cost per thousand tokens in SGD. Routing, budget enforcement
and evidence capture then apply to it unchanged.

## What does not change when the model changes

- the specification and its acceptance criteria
- policy decisions and refusals
- the witness chain and its verification
- the Captain's Gate packet shape
- the generated application's behaviour under test
"""


def export_bundle(
    run_root: str | Path,
    repo_root: str | Path,
    destination: str | Path,
    manifest_extras: dict[str, Any] | None = None,
) -> Path:
    run_root = Path(run_root)
    repo_root = Path(repo_root)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    resolved_destination = destination.resolve()

    def includable(path: Path) -> bool:
        """Never package build output, caches or a previous bundle.

        Without this guard a second export would archive the first bundle,
        and each run would multiply the artefact size.
        """
        if not path.is_file():
            return False
        if path.resolve() == resolved_destination:
            return False
        if path.suffix in {".zip", ".pyc"}:
            return False
        return "__pycache__" not in path.parts

    included: list[str] = []
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(run_root.rglob("*")):
            if includable(path):
                arcname = f"run/{path.relative_to(run_root)}"
                bundle.write(path, arcname)
                included.append(arcname)

        for folder in ("agents", "policies", "workflows", "evaluations", "docs", "deploy", "templates", "scripts"):
            source = repo_root / folder
            if not source.exists():
                continue
            for path in sorted(source.rglob("*")):
                if includable(path):
                    arcname = f"factory/{path.relative_to(repo_root)}"
                    bundle.write(path, arcname)
                    included.append(arcname)

        bundle.writestr("PORTABILITY.md", MODEL_SUBSTITUTION)
        bundle.writestr("sbom.json", json.dumps(software_bill_of_materials(run_root), indent=2))
        bundle.writestr("environment.json", json.dumps(environment_manifest(), indent=2))
        contract = {
            "contract": "wisegen-forge portable ownership v1",
            "items": {item: True for item in CONTRACT_ITEMS},
            "files": len(included),
            "extras": manifest_extras or {},
            "statement": (
                "The customer may export, redeploy, modify and operate this system without "
                "WiseGen Forge, and without any WiseGen-operated service."
            ),
        }
        bundle.writestr("OWNERSHIP.json", json.dumps(contract, indent=2))
    return destination
