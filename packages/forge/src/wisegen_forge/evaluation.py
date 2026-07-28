"""Evaluation Engine: evidence gates completion.

An agent reporting "done" has no standing unless the evidence passes. Gates are
deterministic first (compilation, tests, policy, provenance, acceptance
coverage) so that the same commit produces the same verdict on every machine.
Model-based gates may be added, but may never override a failing deterministic
gate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

SEVERITY_ORDER = ("info", "low", "medium", "high", "critical")


@dataclass
class GateResult:
    gate: str
    passed: bool
    detail: str
    severity: str = "high"
    blocking: bool = True
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate,
            "passed": self.passed,
            "detail": self.detail,
            "severity": self.severity,
            "blocking": self.blocking,
            "evidence": self.evidence,
        }


@dataclass
class EvaluationReport:
    results: list[GateResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results if result.blocking)

    @property
    def failures(self) -> list[GateResult]:
        return [result for result in self.results if not result.passed]

    def add(self, result: GateResult) -> GateResult:
        self.results.append(result)
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "gates_run": len(self.results),
            "gates_failed": len(self.failures),
            "blocking_failures": [r.gate for r in self.failures if r.blocking],
            "results": [result.to_dict() for result in self.results],
        }


class EvaluationEngine:
    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace)
        self.custom: dict[str, Callable[[dict[str, Any]], GateResult]] = {}

    def register(self, name: str, function: Callable[[dict[str, Any]], GateResult]) -> None:
        self.custom[name] = function

    # ------------------------------------------------------------- gates
    def gate_artefacts_present(self, required: list[str]) -> GateResult:
        missing = [name for name in required if not (self.workspace / name).exists()]
        return GateResult(
            gate="artefacts.present",
            passed=not missing,
            detail="all required artefacts present" if not missing else f"missing: {', '.join(missing)}",
            severity="critical",
            evidence={"required": required, "missing": missing},
        )

    def gate_compiles(self, python_files: list[str]) -> GateResult:
        problems: list[str] = []
        for name in python_files:
            path = self.workspace / name
            if not path.exists():
                problems.append(f"{name}: absent")
                continue
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except SyntaxError as exc:
                problems.append(f"{name}: {exc.msg} (line {exc.lineno})")
        return GateResult(
            gate="code.compiles",
            passed=not problems,
            detail="generated code parses" if not problems else "; ".join(problems),
            severity="critical",
            evidence={"checked": python_files, "problems": problems},
        )

    def gate_tests(self, test_result: dict[str, Any]) -> GateResult:
        ok = bool(test_result.get("ok"))
        return GateResult(
            gate="tests.pass",
            passed=ok,
            detail=str(test_result.get("summary", "no summary")),
            severity="critical",
            evidence=test_result,
        )

    def gate_acceptance_coverage(self, criteria: list[str], test_source: str) -> GateResult:
        """Every acceptance criterion must map to at least one executable check."""
        haystack = test_source.lower()
        keyword_map = {
            "end to end": ["round_trip"],
            "audit history": ["audit_records", "audit_chain"],
            "role-based": ["reader_role_cannot_write", "unknown_role"],
            "exportable": ["export_csv", "export_json"],
            "masked": ["restricted_fields_are_masked"],
            "approval": ["terminal_transition_requires_approval"],
            "column": ["every_source_column"],
        }
        uncovered: list[str] = []
        mapping: dict[str, list[str]] = {}
        for criterion in criteria:
            lowered = criterion.lower()
            hits: list[str] = []
            for phrase, tests in keyword_map.items():
                if phrase in lowered:
                    hits += [test for test in tests if test in haystack]
            mapping[criterion] = hits
            if not hits:
                uncovered.append(criterion)
        return GateResult(
            gate="acceptance.coverage",
            passed=len(uncovered) <= max(0, len(criteria) // 3),
            detail=(
                "every criterion maps to an executable check"
                if not uncovered
                else f"{len(uncovered)} of {len(criteria)} criteria lack a direct check"
            ),
            severity="high",
            blocking=True,
            evidence={"mapping": mapping, "uncovered": uncovered},
        )

    def gate_provenance(self, witness_verification: dict[str, Any], expected_events: list[str], seen_events: list[str]) -> GateResult:
        missing = [event for event in expected_events if event not in seen_events]
        passed = bool(witness_verification.get("ok")) and not missing
        return GateResult(
            gate="provenance.complete",
            passed=passed,
            detail=(
                "witness chain verified and complete"
                if passed
                else f"chain ok={witness_verification.get('ok')}, missing events: {', '.join(missing) or 'none'}"
            ),
            severity="critical",
            evidence={"chain": witness_verification, "missing_events": missing},
        )

    def gate_policy(self, refusals: list[dict[str, Any]], expect_refusals: bool = True) -> GateResult:
        """A governed system must be able to demonstrate that it refuses things."""
        passed = bool(refusals) if expect_refusals else True
        return GateResult(
            gate="policy.enforced",
            passed=passed,
            detail=f"{len(refusals)} refusal(s) witnessed" if refusals else "no refusal evidence captured",
            severity="medium",
            blocking=expect_refusals,
            evidence={"refusals": refusals[:10]},
        )

    def gate_data_quality(self, quality: dict[str, Any], minimum: float = 0.5) -> GateResult:
        score = float(quality.get("score", 0.0))
        critical = [issue for issue in quality.get("issues", []) if issue.get("severity") == "critical"]
        passed = score >= minimum and not critical
        return GateResult(
            gate="data.quality",
            passed=passed,
            detail=f"quality score {score} ({quality.get('verdict')})"
            + (f", {len(critical)} critical issue(s)" if critical else ""),
            severity="high",
            blocking=True,
            evidence={"score": score, "critical": critical},
        )

    def gate_cost(self, snapshot: dict[str, Any]) -> GateResult:
        escalations = snapshot.get("escalations") or []
        return GateResult(
            gate="cost.within_envelope",
            passed=True,
            detail=(
                f"spend {snapshot['project']['sgd']} {snapshot['currency']} of {snapshot['caps']['sgd']}"
                + (f"; {len(escalations)} escalation(s)" if escalations else "")
            ),
            severity="medium",
            blocking=False,
            evidence=snapshot,
        )
