#!/usr/bin/env python3
"""Verify this docs-only portfolio pack. Not a model, cluster, or production gate."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INVENTORY_NAME = "FILE_INVENTORY.json"
SECRET_RE = re.compile(
    r"(BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY"
    r"|AKIA[0-9A-Z]{16}"
    r"|sk-[A-Za-z0-9]{20,}"
    r"|xox[baprs]-[A-Za-z0-9-]{10,}"
    r"|Bearer [A-Za-z0-9._\-]{20,})",
    re.I,
)
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt", ".yaml", ".yml"}
REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "EVALUATION.md",
    "INTEROP.md",
    "PLAN.md",
    "JOURNEY.md",
    "kernel/VOCABULARY.md",
    "kernel/DATA_CLASSES.md",
    "kernel/INTERFACES.md",
    "kernel/schemas/evidence-envelope.schema.json",
    "kernel/schemas/maturity-claim.schema.json",
    "kernel/schemas/local-task-contract.schema.json",
    "kernel/schemas/skill-session.schema.json",
    "kernel/schemas/media-job-spec.schema.json",
    "artifacts/salwise-local-ai-pap2-v1.2/STATUS.md",
    "artifacts/salwise-local-ai-pap2-v1.2/package/manifest.json",
    "artifacts/salwise-local-ai-pap2-v1.2/package/check_v1_2_package.py",
    "artifacts/adaptive-learning-tutor-v1.0/STATUS.md",
    "artifacts/adaptive-learning-tutor-v1.0/package/SKILL.md",
    "artifacts/vfx-ai-pipeline-manual/STATUS.md",
    "artifacts/vfx-ai-pipeline-manual/CLAIMED_VS_DISK.md",
    "artifacts/claude-sensemaking-meta-prompt/STATUS.md",
    "artifacts/claude-sensemaking-meta-prompt/source.md",
]
SCHEMA_EXAMPLES = [
    ("kernel/schemas/evidence-envelope.schema.json", "kernel/examples/enq001-envelope.json"),
    ("kernel/schemas/maturity-claim.schema.json", "kernel/examples/vfx-worker-maturity.json"),
    ("kernel/schemas/local-task-contract.schema.json", "kernel/examples/enq001-local-task.json"),
    ("kernel/schemas/skill-session.schema.json", "kernel/examples/tutor-session-outline.json"),
    ("kernel/schemas/media-job-spec.schema.json", "kernel/examples/vfx-media-job-spec-only.json"),
]
KERNEL_SCHEMA_FILES = [
    "evidence-envelope.schema.json",
    "maturity-claim.schema.json",
    "local-task-contract.schema.json",
    "skill-session.schema.json",
    "media-job-spec.schema.json",
]
ACTION_PROPOSAL_REL = Path("actions") / "schemas" / "action-proposal.schema.json"
VFX_FORBIDDEN = [
    "artifacts/vfx-ai-pipeline-manual/vfx_ai_pipeline_integration_manual.md",
    "artifacts/vfx-ai-pipeline-manual/scripts/comfy_agentic_worker.py",
    "artifacts/vfx-ai-pipeline-manual/deploy/k8s-deployment.yaml",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_files() -> list[Path]:
    files = [p for p in ROOT.rglob("*") if p.is_file() and p.name != INVENTORY_NAME]
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check(name: str, result: bool, detail: str = "") -> dict:
    row = {"check": name, "result": "PASS" if result else "FAIL"}
    if detail:
        row["detail"] = detail
    return row


def try_jsonschema(schema: dict, instance: dict) -> tuple[bool, str]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        missing = [k for k in schema.get("required", []) if k not in instance]
        extra = []
        if schema.get("additionalProperties") is False:
            extra = [k for k in instance if k not in schema.get("properties", {})]
        ok = not missing and not extra
        detail = "jsonschema unavailable; required-key fallback"
        if missing:
            detail += f"; missing={missing}"
        if extra:
            detail += f"; extra={extra}"
        return ok, detail
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return True, "jsonschema.validate"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def main() -> int:
    checks: list[dict] = []
    files = tracked_files()

    for rel in REQUIRED_PATHS:
        path = ROOT / rel
        checks.append(check(f"required path exists: {rel}", path.is_file()))

    for rel in VFX_FORBIDDEN:
        path = ROOT / rel
        checks.append(check(f"VFX runtime path not vendored: {rel}", not path.exists()))

    json_ok = True
    json_fail = []
    for path in files:
        if path.suffix == ".json":
            try:
                load_json(path)
            except Exception as exc:  # noqa: BLE001
                json_ok = False
                json_fail.append(f"{path.relative_to(ROOT)}: {exc}")
    checks.append(check("all JSON files parse", json_ok, "; ".join(json_fail)))

    schema_dir = ROOT / "kernel" / "schemas"
    found_schemas = {p.name for p in schema_dir.glob("*.json")} if schema_dir.is_dir() else set()
    expected_schemas = set(KERNEL_SCHEMA_FILES)
    checks.append(check(
        "exactly five kernel envelopes; no sixth schema file",
        found_schemas == expected_schemas,
        "found=" + ",".join(sorted(found_schemas)),
    ))
    for name in KERNEL_SCHEMA_FILES:
        schema_path = schema_dir / name
        if not schema_path.is_file():
            checks.append(check(f"kernel schema additionalProperties false: {name}", False, "missing"))
            continue
        schema = load_json(schema_path)
        checks.append(check(
            f"kernel schema additionalProperties false: {name}",
            schema.get("additionalProperties") is False,
        ))

    for schema_rel, example_rel in SCHEMA_EXAMPLES:
        schema = load_json(ROOT / schema_rel)
        instance = load_json(ROOT / example_rel)
        ok, detail = try_jsonschema(schema, instance)
        checks.append(check(f"schema example: {example_rel}", ok, detail))

    action_proposal = ROOT.parent / ACTION_PROPOSAL_REL
    checks.append(check("ActionProposal remains at parent AIOS path", action_proposal.is_file()))
    if action_proposal.is_file():
        ap_schema = load_json(action_proposal)
        checks.append(check(
            "ActionProposal additionalProperties remains false",
            ap_schema.get("additionalProperties") is False,
        ))
    forked_action_proposal = schema_dir / "action-proposal.schema.json"
    checks.append(check(
        "ActionProposal not forked into portfolio kernel",
        not forked_action_proposal.exists(),
    ))

    secret_hits = []
    emdash_hits = []
    for path in files:
        if path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if SECRET_RE.search(text):
            secret_hits.append(path.relative_to(ROOT).as_posix())
        if "\u2014" in text:
            emdash_hits.append(path.relative_to(ROOT).as_posix())
    checks.append(check("no high-risk secret patterns in pack text", not secret_hits, ", ".join(secret_hits)))
    checks.append(check("no em dash in pack text files", not emdash_hits, ", ".join(emdash_hits)))

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    checks.append(check("README warns not to merge to profile main", "Do not merge this branch to profile" in readme))
    checks.append(check("README states docs-only", "Docs-only" in readme))
    checks.append(check("README lists PLAN.md", "PLAN.md" in readme))
    checks.append(check("README lists JOURNEY.md", "JOURNEY.md" in readme))

    aios_v12 = ROOT.parent / "governance" / "AIOS_v1.2.md"
    checks.append(check("parent AIOS v1.2 remains at repository root", aios_v12.is_file()))
    if aios_v12.is_file():
        checks.append(check(
            "AIOS v1.2 byte size unchanged by this pack",
            aios_v12.stat().st_size == 63543,
            str(aios_v12.stat().st_size),
        ))

    salwise_manifest = load_json(ROOT / "artifacts/salwise-local-ai-pap2-v1.2/package/manifest.json")
    salwise_root = ROOT / "artifacts/salwise-local-ai-pap2-v1.2/package"
    manifest_hash_ok = True
    mismatch = []
    for row in salwise_manifest["files"]:
        path = salwise_root / row["path"]
        if not path.is_file():
            manifest_hash_ok = False
            mismatch.append(f"missing {row['path']}")
            continue
        digest = sha256(path)
        size = path.stat().st_size
        if digest != row["sha256"] or size != row["bytes"]:
            manifest_hash_ok = False
            mismatch.append(row["path"])
    checks.append(check("Salwise manifest hashes match vendored package", manifest_hash_ok, ", ".join(mismatch)))

    checker = subprocess.run(
        [sys.executable, str(salwise_root / "check_v1_2_package.py")],
        cwd=salwise_root,
        capture_output=True,
        text=True,
        check=False,
    )
    checks.append(check("Salwise package checker exit 0", checker.returncode == 0, checker.stderr[-500:]))
    if checker.returncode == 0:
        report = json.loads(checker.stdout)
        checks.append(check(
            "Salwise checker 18/18 mechanical only",
            report.get("passed") == 18 and report.get("total") == 18
            and report.get("runtime_integration") == "NOT_RUN"
            and report.get("model_behaviour") == "NOT_RUN",
        ))

    skill = (ROOT / "artifacts/adaptive-learning-tutor-v1.0/package/SKILL.md").read_text(encoding="utf-8")
    for ref in [
        "references/CURRICULUM.md",
        "references/ASSESSMENT.md",
        "references/PLAN.md",
        "references/RESOURCE_POLICY.md",
        "references/WINE_EXAMPLE.md",
        "references/QA_TESTS.md",
    ]:
        checks.append(check(
            f"tutor reference exists: {ref}",
            (ROOT / "artifacts/adaptive-learning-tutor-v1.0/package" / ref).is_file() and ref in skill,
        ))

    vfx_hash_file = (ROOT / "artifacts/vfx-ai-pipeline-manual/SOURCE_SHA256.txt").read_text().strip()
    checks.append(check(
        "VFX source hash recorded",
        vfx_hash_file == "816022081890a347a5018cc36c2e77cf3c0e7a0af1e547732fd08d1a8521a90c",
        vfx_hash_file,
    ))
    prompt_hash = sha256(ROOT / "artifacts/claude-sensemaking-meta-prompt/source.md")
    checks.append(check(
        "meta-prompt source hash unchanged",
        prompt_hash == "a2dc1991a82eef9880c15a11e0f8488a010fabd71ad13e5e927f147048855dfe",
        prompt_hash,
    ))

    inventory = {
        "package": "Spark-a-life portfolio evaluation and architecture pack",
        "version": "1.0.0-eval",
        "generated": "2026-11-05",
        "note": "sha256 of every tracked file under portfolio/ except this inventory",
        "runtime": False,
        "production_external_execution": False,
        "files": [
            {"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)}
            for p in files
        ],
    }
    (ROOT / INVENTORY_NAME).write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    checks.append(check("FILE_INVENTORY.json written", (ROOT / INVENTORY_NAME).is_file()))

    report = {
        "check_type": "PORTFOLIO_PACK_VERIFICATION",
        "passed": sum(x["result"] == "PASS" for x in checks),
        "total": len(checks),
        "runtime": False,
        "production_external_execution": False,
        "checks": checks,
    }
    print(json.dumps(report, indent=2))
    return 0 if checks and all(x["result"] == "PASS" for x in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
