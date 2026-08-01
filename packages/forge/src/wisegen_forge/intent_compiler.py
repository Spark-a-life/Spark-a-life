"""Intent Compiler: human intent to executable specification.

    Human intent -> structured product brief -> executable specification
    -> architecture decision record -> task dependency graph -> verified system

This is the difference between prompt-to-code improvisation and a factory. The
specification is the authoritative artefact: code is derived from it, drift is
measured against it, and regeneration is proposed from it.

The compiler is deliberately deterministic-first. A model may enrich the brief,
but the structure, the acceptance criteria and the constraint set are produced
by rules that can be inspected, tested and defended in an audit.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .domain import ForgeObject, digest
from .model_router import ModelRouter

ACTOR_HINTS = {
    "employee": "employee",
    "staff": "employee",
    "new hire": "new_employee",
    "onboard": "new_employee",
    "manager": "manager",
    "supervisor": "manager",
    "hr": "hr_administrator",
    "human resource": "hr_administrator",
    "people and culture": "hr_administrator",
    "people team": "hr_administrator",
    "admin": "administrator",
    "finance": "finance_officer",
    "auditor": "auditor",
    "student": "learner",
    "clinician": "clinician",
    "patient": "patient",
    "investor": "investor",
    "customer": "customer",
}

CONSTRAINT_HINTS = {
    r"\bpdpa\b|personal data|\bpii\b": "PDPA-aligned handling of personal data",
    r"human approval|sign[- ]off|approval|captain": "Human approval required before any consequential decision",
    r"\bvpc\b|on[- ]prem|air[- ]gap|sovereign|local": "Deployable inside the customer estate without external egress",
    r"audit|evidence|trace|provenance": "Complete audit history retained and exportable",
    r"\brbac\b|role[- ]based|permission": "Role-based access control enforced at the data layer",
    r"\bmom\b|employment act|statutory": "Singapore statutory employment requirements respected",
    r"export|portab|own": "Customer retains export rights over code, data and evidence",
}

OUTCOME_HINTS = {
    r"manual|spreadsheet|email chas|chase": "Reduce manual coordination effort",
    r"delay|slow|turnaround|cycle time": "Shorten turnaround time",
    r"error|mistake|inconsist": "Reduce data entry error and inconsistency",
    r"visib|dashboard|report|status": "Give owners live visibility of status",
    r"complian|audit|evidence": "Preserve approval evidence for compliance review",
    r"onboard|induct": "Complete onboarding without dropped steps",
}

RISK_KEYWORDS = {
    "critical": ("payment", "payroll", "clinical", "medication", "termination", "credential"),
    "high": ("personal data", "pdpa", "employment", "salary", "nric", "health"),
    "medium": ("internal", "workflow", "approval", "dashboard"),
}


@dataclass
class Specification:
    objective: str
    users: list[str]
    outcomes: list[str]
    constraints: list[str]
    acceptance_criteria: list[str]
    data_sources: list[str] = field(default_factory=list)
    risk_tier: str = "medium"
    open_questions: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission": {
                "objective": self.objective,
                "users": self.users,
                "outcomes": self.outcomes,
                "constraints": self.constraints,
                "acceptance_criteria": self.acceptance_criteria,
                "data_sources": self.data_sources,
                "risk_tier": self.risk_tier,
                "open_questions": self.open_questions,
            },
            "provenance": self.provenance,
        }


@dataclass
class IntakeRecord:
    """Immutable record of what the human actually supplied."""

    statement: str
    documents: list[dict[str, Any]] = field(default_factory=list)
    datasets: list[dict[str, Any]] = field(default_factory=list)
    submitted_by: str = "captain"

    @classmethod
    def from_paths(cls, statement: str, paths: list[str | Path], submitted_by: str = "captain") -> "IntakeRecord":
        documents: list[dict[str, Any]] = []
        datasets: list[dict[str, Any]] = []
        for raw in paths:
            path = Path(raw)
            if not path.exists():
                raise FileNotFoundError(path)
            content = path.read_text(encoding="utf-8", errors="replace")
            entry = {
                "name": path.name,
                "path": str(path),
                "bytes": path.stat().st_size,
                "digest": digest(content),
                "excerpt": content[:600],
            }
            (datasets if path.suffix.lower() in (".csv", ".tsv") else documents).append(entry)
        return cls(statement=statement, documents=documents, datasets=datasets, submitted_by=submitted_by)

    def to_object(self) -> ForgeObject:
        return ForgeObject.create(
            "intake",
            {
                "statement": self.statement,
                "documents": self.documents,
                "datasets": self.datasets,
                "submitted_by": self.submitted_by,
            },
            created_from="human_intake",
            classification="confidential",
        )


class IntentCompiler:
    def __init__(self, router: ModelRouter | None = None, actor: str = "gaie.intent-compiler") -> None:
        self.router = router
        self.actor = actor

    def compile(self, intake: IntakeRecord) -> Specification:
        corpus = " ".join(
            [intake.statement]
            + [doc.get("excerpt", "") for doc in intake.documents]
            + [ds.get("excerpt", "") for ds in intake.datasets]
        ).lower()

        objective = self._objective(intake.statement)
        users = self._users(corpus)
        outcomes = self._matched(OUTCOME_HINTS, corpus) or ["Deliver the stated capability with evidence of correctness"]
        constraints = self._matched(CONSTRAINT_HINTS, corpus)
        constraints = self._ensure_floor(constraints)
        risk_tier = self._risk(corpus)
        data_sources = [ds["name"] for ds in intake.datasets] + [doc["name"] for doc in intake.documents]
        acceptance = self._acceptance(objective, users, constraints, intake)
        open_questions = self._open_questions(corpus, intake)

        provenance: dict[str, Any] = {
            "compiler": "wisegen-forge.intent-compiler",
            "method": "deterministic-rules",
            "intake_digest": digest(
                {"statement": intake.statement, "documents": intake.documents, "datasets": intake.datasets}
            ),
        }
        if self.router is not None:
            completion = self.router.complete(
                self.actor,
                self._enrichment_prompt(intake, objective),
                capability="extraction",
                risk_tier=risk_tier,
            )
            provenance["model"] = completion.to_dict()

        return Specification(
            objective=objective,
            users=users,
            outcomes=outcomes,
            constraints=constraints,
            acceptance_criteria=acceptance,
            data_sources=data_sources,
            risk_tier=risk_tier,
            open_questions=open_questions,
            provenance=provenance,
        )

    # ------------------------------------------------------------- helpers
    @staticmethod
    def _objective(statement: str) -> str:
        """First sentence, not first line: intake text wraps, intent does not."""
        flattened = " ".join(part.strip() for part in statement.strip().splitlines() if part.strip())
        if not flattened:
            return "Unstated objective"
        sentence = re.split(r"(?<=[.!?])\s+", flattened)[0].strip().rstrip(".")
        sentence = re.sub(r"^(please|kindly|i want to|we want to|we need to|can you)\s+", "", sentence, flags=re.I)
        return sentence[0].upper() + sentence[1:] if sentence else "Unstated objective"

    @staticmethod
    def _users(corpus: str) -> list[str]:
        found = [role for hint, role in ACTOR_HINTS.items() if hint in corpus]
        ordered: list[str] = []
        for role in found:
            if role not in ordered:
                ordered.append(role)
        return ordered or ["primary_user", "administrator"]

    @staticmethod
    def _matched(table: dict[str, str], corpus: str) -> list[str]:
        out: list[str] = []
        for pattern, value in table.items():
            if re.search(pattern, corpus) and value not in out:
                out.append(value)
        return out

    @staticmethod
    def _ensure_floor(constraints: list[str]) -> list[str]:
        floor = [
            "Human approval required before any consequential decision",
            "Complete audit history retained and exportable",
        ]
        for item in floor:
            if item not in constraints:
                constraints.append(item)
        return constraints

    @staticmethod
    def _risk(corpus: str) -> str:
        for tier in ("critical", "high", "medium"):
            if any(keyword in corpus for keyword in RISK_KEYWORDS[tier]):
                return tier
        return "low"

    @staticmethod
    def _acceptance(objective: str, users: list[str], constraints: list[str], intake: IntakeRecord) -> list[str]:
        criteria = [
            f"A {users[0]} can complete the primary task end to end without manual workarounds",
            "Every record change is written to an immutable audit history with actor, time and prior value",
            "Access is role-based and a user cannot read or write outside their role",
            "All records are exportable in an open format without vendor tooling",
        ]
        if any("PDPA" in item for item in constraints):
            criteria.append("Fields classified as personal data are masked for roles without an explicit need")
        if any("approval" in item.lower() for item in constraints):
            criteria.append("No status may reach a terminal state without a recorded human approval")
        if intake.datasets:
            criteria.append("Every column present in the source dataset is represented or explicitly discarded with reason")
        return criteria

    @staticmethod
    def _open_questions(corpus: str, intake: IntakeRecord) -> list[str]:
        questions: list[str] = []
        if "retention" not in corpus:
            questions.append("What retention period applies to the records this system will hold?")
        if not intake.datasets:
            questions.append("Is there an existing dataset or spreadsheet this system must absorb?")
        if "integrat" not in corpus:
            questions.append("Which existing systems, if any, must this exchange data with?")
        return questions

    @staticmethod
    def _enrichment_prompt(intake: IntakeRecord, objective: str) -> str:
        return (
            "Extract the product brief from the following intake. Return only fields you can "
            "support from the text.\n\n"
            f"OBJECTIVE: {objective}\n"
            f"STATEMENT: {intake.statement}\n"
            f"DATASETS: {[ds['name'] for ds in intake.datasets]}\n"
            f"DOCUMENTS: {[doc['name'] for doc in intake.documents]}\n"
        )
