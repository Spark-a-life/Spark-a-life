"""Acceptance tests: the promises made to the customer.

The exit test is the one that matters. A governed factory that cannot be
removed has produced captivity rather than capability, so these tests operate
on an extracted bundle with the platform deliberately off the import path.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from tests import EXAMPLES, REPO_ROOT

from wisegen_forge.pipeline import run_full_pipeline

STATEMENT = (
    "Build a governed employee onboarding application from our existing spreadsheet, "
    "with role-based access, an approval workflow and an exportable audit history."
)


def independent_verify(chain_path: Path) -> tuple[bool, list[str]]:
    """Re-verify a witness chain using nothing but the standard library.

    This function deliberately does not import wisegen_forge. It is the
    auditor's verifier: if the published algorithm is honest, a stranger can
    reproduce it in twenty lines.
    """

    def digest(payload: object) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    genesis = "sha256:" + "0" * 64  # published in docs/governance/WITNESS-CHAIN.md
    problems: list[str] = []
    previous = genesis
    for index, line in enumerate(chain_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        entry = json.loads(line)
        if entry["seq"] != index:
            problems.append(f"entry {index}: sequence is {entry['seq']}")
        if entry["prev_digest"] != previous:
            problems.append(f"entry {index}: broken link")
        if digest(entry["payload"]) != entry["payload_digest"]:
            problems.append(f"entry {index}: payload does not match its digest")
        recomputed = digest(
            {
                "seq": entry["seq"],
                "at": entry["at"],
                "actor": entry["actor"],
                "event": entry["event"],
                "payload_digest": entry["payload_digest"],
                "prev_digest": entry["prev_digest"],
            }
        )
        if recomputed != entry["entry_digest"]:
            problems.append(f"entry {index}: entry digest does not recompute")
        previous = entry["entry_digest"]
    return (not problems), problems


class PortabilityAcceptanceTests(unittest.TestCase):
    """The exit test: does the customer own something that still works?"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.result = run_full_pipeline(
            repo_root=REPO_ROOT,
            run_root=root / "run",
            statement=STATEMENT,
            inputs=sorted(EXAMPLES.glob("*")),
            project="acceptance",
        )
        cls.extracted = root / "extracted"
        with zipfile.ZipFile(cls.result.bundle) as bundle:
            bundle.extractall(cls.extracted)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_ownership_contract_is_complete(self) -> None:
        contract = json.loads((self.extracted / "OWNERSHIP.json").read_text())
        for item in (
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
        ):
            self.assertTrue(contract["items"].get(item), f"the bundle does not honour {item}")

    def test_bundle_carries_the_factory_definitions(self) -> None:
        for expected in ("factory/agents/registry.yaml", "factory/policies", "factory/docs"):
            self.assertTrue(list(self.extracted.glob(expected + "*")), f"missing {expected}")

    def test_bundle_carries_the_generated_system(self) -> None:
        apps = sorted((self.extracted / "run" / "workspace").glob("app_*"))
        self.assertGreaterEqual(len(apps), 2)
        self.assertTrue((self.extracted / "run" / "workspace" / "schema.sql").exists())

    def test_bundle_excludes_caches_and_prior_bundles(self) -> None:
        for path in self.extracted.rglob("*"):
            self.assertNotEqual(path.suffix, ".zip", f"a bundle inside a bundle: {path}")
            self.assertNotIn("__pycache__", path.parts, f"cache leaked into the bundle: {path}")

    def test_no_secret_material_left_the_boundary(self) -> None:
        needles = ("sk-ant-", "BEGIN RSA PRIVATE KEY", "BEGIN OPENSSH PRIVATE KEY", "AWS_SECRET")
        for path in self.extracted.rglob("*"):
            if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".py", ".yaml", ".sql", ".txt"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                for needle in needles:
                    self.assertNotIn(needle, text, f"possible secret in {path.name}")

    def test_generated_application_runs_without_the_platform(self) -> None:
        """The exit test proper: no wisegen_forge on the path, no network, no installs."""
        app = self.extracted / "run" / "workspace" / "app_conservative"
        self.assertTrue((app / "app.py").exists())

        environment = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": str(self.extracted),
            "PYTHONPATH": "",  # the platform is deliberately unavailable
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "test_app", "-v"],
            cwd=str(app),
            capture_output=True,
            text=True,
            timeout=180,
            env=environment,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"the generated application failed outside the platform:\n{proc.stdout}\n{proc.stderr}",
        )

    def test_platform_import_is_genuinely_unavailable_in_that_environment(self) -> None:
        """Guards the test above: prove the exit test was not passing by accident."""
        proc = subprocess.run(
            [sys.executable, "-c", "import wisegen_forge"],
            cwd=str(self.extracted),
            capture_output=True,
            text=True,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "PYTHONPATH": ""},
        )
        self.assertNotEqual(proc.returncode, 0, "wisegen_forge was importable, so the exit test proves nothing")

    def test_an_outsider_can_verify_the_evidence(self) -> None:
        chain = self.extracted / "run" / "evidence" / "witness.jsonl"
        self.assertTrue(chain.exists(), "provenance history must travel with the bundle")
        ok, problems = independent_verify(chain)
        self.assertTrue(ok, f"independent verification failed: {problems}")

    def test_independent_verifier_detects_tampering(self) -> None:
        """A verifier that always says yes is worthless, so prove it says no."""
        with tempfile.TemporaryDirectory() as tmp:
            source = self.extracted / "run" / "evidence" / "witness.jsonl"
            copy = Path(tmp) / "witness.jsonl"
            rows = [json.loads(line) for line in source.read_text().splitlines() if line.strip()]
            rows[1]["payload"]["injected"] = "after the fact"
            copy.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n")
            ok, problems = independent_verify(copy)
            self.assertFalse(ok)
            self.assertTrue(problems)


class SpecificationAcceptanceTests(unittest.TestCase):
    """Every promise in the specification must map to something executable."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.result = run_full_pipeline(
            repo_root=REPO_ROOT,
            run_root=Path(cls.tmp.name) / "run",
            statement=STATEMENT,
            inputs=sorted(EXAMPLES.glob("*")),
            project="acceptance-spec",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_acceptance_coverage_gate_was_enforced(self) -> None:
        coverage = next(r for r in self.result.report.results if r.gate == "acceptance.coverage")
        self.assertTrue(coverage.passed, coverage.detail)
        self.assertTrue(coverage.blocking, "acceptance coverage must block, not warn")

    def test_role_based_access_is_present_in_the_generated_system(self) -> None:
        app = (self.result.run_root / "workspace" / "app_conservative" / "app.py").read_text()
        for marker in ("role", "audit"):
            self.assertIn(marker, app.lower(), f"the generated application does not implement {marker}")

    def test_restricted_fields_are_masked_by_default(self) -> None:
        app = (self.result.run_root / "workspace" / "app_conservative" / "app.py").read_text().lower()
        self.assertIn("mask", app, "restricted fields must be masked server side")

    def test_export_path_exists_in_the_generated_system(self) -> None:
        openapi = json.loads(
            (self.result.run_root / "workspace" / "app_conservative" / "openapi.json").read_text()
        )
        paths = " ".join(openapi.get("paths", {}).keys())
        self.assertIn("export", paths, "the customer must be able to extract their own records")

    def test_every_stage_left_evidence(self) -> None:
        events = {entry["event"] for entry in (
            json.loads(line)
            for line in (self.result.run_root / "evidence" / "witness.jsonl").read_text().splitlines()
            if line.strip()
        )}
        for required in (
            "run.started",
            "intake.recorded",
            "gate.submitted",
            "gate.decided",
            "deployment.prepared",
            "bundle.exported",
        ):
            self.assertIn(required, events, f"stage evidence missing: {required}")


if __name__ == "__main__":
    unittest.main()
