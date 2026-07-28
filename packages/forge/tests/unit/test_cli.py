"""Smoke tests for the command line interface.

The CLI is the documented surface. If a flag in the README stops working, the
documentation becomes a liability, so the interface is tested rather than
described.
"""

from __future__ import annotations

import io
import contextlib
import tempfile
import unittest
from pathlib import Path

from tests import REPO_ROOT

from wisegen_forge.cli import build_parser, main, resolve_chain


def run_cli(*argv: str) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(list(argv))
    return code, buffer.getvalue()


class ParserTests(unittest.TestCase):
    def test_every_documented_command_exists(self) -> None:
        parser = build_parser()
        actions = [a for a in parser._actions if getattr(a, "choices", None) and "doctor" in a.choices]
        commands = set(actions[0].choices)
        for expected in ("doctor", "roles", "compile-sheet", "plan", "run", "demo", "gate", "verify", "export"):
            self.assertIn(expected, commands)

    def test_run_flag_is_accepted_and_aliased(self) -> None:
        parser = build_parser()
        canonical = parser.parse_args(["verify", "--run", "somewhere"])
        legacy = parser.parse_args(["verify", "--run-root", "somewhere"])
        self.assertEqual(canonical.run_root, legacy.run_root)


class CommandTests(unittest.TestCase):
    def test_doctor_reports_readiness(self) -> None:
        code, output = run_cli("--repo", str(REPO_ROOT), "doctor")
        self.assertEqual(code, 0, output)
        self.assertIn("checks passed", output)

    def test_roles_lists_the_full_roster(self) -> None:
        code, output = run_cli("--repo", str(REPO_ROOT), "roles")
        self.assertEqual(code, 0)
        for role_id in ("kaie.captain", "gaie.intent-compiler", "paie.release-engineer", "saie.librarian",
                        "taie.solution-lead"):
            self.assertIn(role_id, output)

    def test_compile_sheet_reports_classification(self) -> None:
        sheet = REPO_ROOT / "examples" / "employee-onboarding" / "onboarding.csv"
        code, output = run_cli("--repo", str(REPO_ROOT), "compile-sheet", str(sheet))
        self.assertEqual(code, 0)
        self.assertIn("restricted", output)


class VersionTests(unittest.TestCase):
    def test_package_and_project_versions_agree(self) -> None:
        import wisegen_forge

        declared = [
            line.split("=", 1)[1].strip().strip('"')
            for line in (REPO_ROOT / "pyproject.toml").read_text().splitlines()
            if line.startswith("version = ")
        ][0]
        self.assertEqual(wisegen_forge.__version__, declared)

    def test_changelog_documents_the_current_version(self) -> None:
        import wisegen_forge

        changelog = (REPO_ROOT / "CHANGELOG.md").read_text()
        self.assertIn(f"[{wisegen_forge.__version__}]", changelog)


class ChainResolutionTests(unittest.TestCase):
    def test_a_run_directory_resolves_to_its_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chain = Path(tmp) / "evidence" / "witness.jsonl"
            chain.parent.mkdir(parents=True)
            chain.write_text("")
            self.assertEqual(resolve_chain(tmp), chain)

    def test_a_file_path_is_returned_unchanged(self) -> None:
        self.assertEqual(resolve_chain("some/chain.jsonl"), Path("some/chain.jsonl"))

    def test_a_directory_without_a_chain_fails_loudly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                resolve_chain(tmp)


if __name__ == "__main__":
    unittest.main()
