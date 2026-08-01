"""Integration tests for the nine-stage governed runtime.

One pipeline run is shared across the class because the run is deterministic
and the assertions are read-only. Determinism is itself part of what is under
test: an ungoverned factory that produces a different system each time cannot
be audited.
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tests import EXAMPLES, REPO_ROOT

from wisegen_forge.pipeline import run_full_pipeline

STATEMENT = (
    "Build a governed employee onboarding application from our existing spreadsheet, "
    "with role-based access, an approval workflow and an exportable audit history."
)


class PipelineTests(unittest.TestCase):
    tmp: tempfile.TemporaryDirectory

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.result = run_full_pipeline(
            repo_root=REPO_ROOT,
            run_root=Path(cls.tmp.name) / "run",
            statement=STATEMENT,
            inputs=sorted(EXAMPLES.glob("*")),
            project="integration",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    # ------------------------------------------------ stages 1 to 3
    def test_specification_carries_acceptance_criteria(self) -> None:
        spec = self.result.specification
        self.assertIsNotNone(spec)
        self.assertTrue(spec.objective)
        self.assertTrue(spec.acceptance_criteria, "generation must never proceed on unstated acceptance criteria")
        self.assertTrue(spec.constraints)
        self.assertTrue(spec.users)

    def test_dataset_is_compiled_with_classification(self) -> None:
        sheet = self.result.sheet
        self.assertIsNotNone(sheet)
        self.assertGreater(len(sheet.columns), 3)
        classifications = {column.classification for column in sheet.columns}
        self.assertTrue(
            classifications & {"confidential", "restricted", "personal"},
            "an HR dataset must raise at least one sensitive classification",
        )

    def test_architecture_plan_names_risk_and_reversal(self) -> None:
        plan = self.result.plan
        self.assertIsNotNone(plan)
        as_dict = plan.to_dict()
        for key in ("threat_model", "rollback", "cost_envelope", "test_strategy", "data_classification", "decisions"):
            self.assertIn(key, as_dict, f"the architecture plan must carry {key}")

    # ------------------------------------------------ stages 4 and 5
    def test_mission_graph_is_acyclic_and_wave_ordered(self) -> None:
        graph = self.result.graph
        waves = graph.waves()
        self.assertGreater(len(waves), 2, "a real mission has sequential dependencies")
        seen: set[str] = set()
        for wave in waves:
            for task in wave:
                for dependency in task.depends_on:
                    self.assertIn(dependency, seen, "a task was scheduled before its dependency")
            seen.update(task.id for task in wave)

    def test_branchable_execution_produced_competing_candidates(self) -> None:
        labels = {task.candidate_label for task in self.result.graph.tasks.values() if task.candidate_label}
        self.assertGreaterEqual(len(labels), 2, "material choices must produce parallel candidates")

    def test_generated_application_exists_per_candidate(self) -> None:
        workspace = self.result.run_root / "workspace"
        apps = sorted(workspace.glob("app_*"))
        self.assertGreaterEqual(len(apps), 2)
        for app in apps:
            for expected in ("app.py", "test_app.py", "openapi.json", "Dockerfile", "README.md"):
                self.assertTrue((app / expected).exists(), f"{app.name} is missing {expected}")

    # ------------------------------------------------ stages 6 and 7
    def test_quality_gates_ran_and_passed(self) -> None:
        report = self.result.report
        self.assertIsNotNone(report)
        self.assertTrue(report.passed, f"quality gates failed: {[g.name for g in report.failures]}")
        names = {result.gate for result in report.results}
        for required in ("artefacts.present", "code.compiles", "tests.pass", "provenance.complete",
                         "acceptance.coverage", "policy.enforced", "cost.within_envelope"):
            self.assertIn(required, names)

    def test_gate_packet_answers_the_reviewer_questions(self) -> None:
        packet = self.result.packet
        markdown = packet.to_markdown().lower()
        for question in ("what changed", "evidence", "cost", "revers"):
            self.assertIn(question, markdown, f"the gate packet must address: {question}")
        self.assertTrue(packet.branches, "the reviewer must be able to compare candidates")

    def test_decision_was_recorded_by_a_named_authority(self) -> None:
        decision = self.result.decision
        self.assertIsNotNone(decision, "a run that deploys must carry a recorded decision")
        self.assertTrue(decision["decided_by"])
        self.assertTrue(decision["rationale"])

    # ------------------------------------------------ stages 8 and 9
    def test_release_manifest_is_signed_and_reversible(self) -> None:
        deployment = self.result.deployment
        self.assertIsNotNone(deployment)
        manifest = deployment["manifest"]
        self.assertTrue(manifest["signature"], "deployment happens through signed manifests")
        self.assertTrue(manifest["artefact_digest"].startswith("sha256:"))
        self.assertTrue(manifest["rollback_release"], "no deployment without a named rollback target")
        self.assertIn("rollback_to", deployment)

    def test_witness_chain_verifies_and_covers_every_stage(self) -> None:
        witness = self.result.witness
        self.assertTrue(witness["ok"], witness.get("problems"))
        self.assertGreater(witness["length"], 20)

    def test_cost_was_metered_per_actor(self) -> None:
        cost = self.result.cost
        self.assertIn("by_actor", cost)
        self.assertGreater(len(cost["by_actor"]), 3, "cost must be attributable to roles, not just to the project")

    def test_portable_bundle_is_produced_and_bounded(self) -> None:
        bundle = self.result.bundle
        self.assertTrue(bundle.exists())
        size_mb = bundle.stat().st_size / (1024 * 1024)
        self.assertLess(size_mb, 50, "the bundle must not accumulate prior bundles or caches")

    def test_run_is_deterministic(self) -> None:
        """A second run over identical inputs must produce identical artefacts."""
        with tempfile.TemporaryDirectory() as second:
            other = run_full_pipeline(
                repo_root=REPO_ROOT,
                run_root=Path(second) / "run",
                statement=STATEMENT,
                inputs=sorted(EXAMPLES.glob("*")),
                project="integration",
            )
            first_app = (self.result.run_root / "workspace" / "app_conservative" / "app.py").read_text()
            second_app = (other.run_root / "workspace" / "app_conservative" / "app.py").read_text()
            self.assertEqual(first_app, second_app, "generation must be reproducible for the same specification")
            self.assertEqual(
                self.result.specification.acceptance_criteria,
                other.specification.acceptance_criteria,
            )


class MissingDatasetTests(unittest.TestCase):
    def test_workflow_refuses_without_a_dataset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            statement_only = Path(tmp) / "requirement.md"
            statement_only.write_text("Build something useful for the HR team.")
            with self.assertRaises(ValueError):
                run_full_pipeline(
                    repo_root=REPO_ROOT,
                    run_root=Path(tmp) / "run",
                    statement="Build something useful",
                    inputs=[statement_only],
                    project="negative",
                )


if __name__ == "__main__":
    unittest.main()
