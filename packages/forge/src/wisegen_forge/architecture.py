"""Architecture and Risk Engine (Stage 3).

Produces the artefacts that must exist before a single line of code is generated:
system architecture, threat model, data classification, model selection, tool
permissions, deployment model, cost envelope, test strategy and rollback plan.

Each decision is emitted as an Architecture Decision Record so that the reason
survives the person who made it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .intent_compiler import Specification
from .spreadsheet_compiler import SheetModel

STRIDE = ("spoofing", "tampering", "repudiation", "information_disclosure", "denial_of_service", "elevation_of_privilege")


@dataclass
class ArchitectureDecision:
    id: str
    title: str
    status: str
    context: str
    decision: str
    consequences: list[str]
    alternatives: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "context": self.context,
            "decision": self.decision,
            "consequences": self.consequences,
            "alternatives_considered": self.alternatives,
        }

    def to_markdown(self) -> str:
        lines = [
            f"# {self.id}: {self.title}",
            "",
            f"**Status:** {self.status}",
            "",
            "## Context",
            self.context,
            "",
            "## Decision",
            self.decision,
            "",
            "## Consequences",
        ]
        lines += [f"- {item}" for item in self.consequences]
        if self.alternatives:
            lines += ["", "## Alternatives considered"] + [f"- {item}" for item in self.alternatives]
        return "\n".join(lines) + "\n"


@dataclass
class ArchitecturePlan:
    components: list[dict[str, Any]]
    data_classification: dict[str, str]
    threat_model: list[dict[str, Any]]
    deployment: dict[str, Any]
    cost_envelope: dict[str, Any]
    test_strategy: list[str]
    rollback: dict[str, Any]
    decisions: list[ArchitectureDecision]

    def to_dict(self) -> dict[str, Any]:
        return {
            "components": self.components,
            "data_classification": self.data_classification,
            "threat_model": self.threat_model,
            "deployment": self.deployment,
            "cost_envelope": self.cost_envelope,
            "test_strategy": self.test_strategy,
            "rollback": self.rollback,
            "decisions": [decision.to_dict() for decision in self.decisions],
        }


def design(spec: Specification, sheet: SheetModel | None, target_estate: str = "customer-vpc") -> ArchitecturePlan:
    restricted = []
    confidential = []
    classification: dict[str, str] = {}
    if sheet is not None:
        for column in sheet.columns:
            classification[column.slug] = column.classification
            if column.classification == "restricted":
                restricted.append(column.slug)
            elif column.classification == "confidential":
                confidential.append(column.slug)

    components = [
        {"name": "web_ui", "responsibility": "role-scoped forms, lists and status transitions", "technology": "stdlib HTTP + server-rendered HTML"},
        {"name": "api", "responsibility": "record CRUD, transitions, approvals, export", "technology": "Python stdlib http.server"},
        {"name": "store", "responsibility": "authoritative records plus append-only audit table", "technology": "SQLite (portable) or PostgreSQL (institutional)"},
        {"name": "authz", "responsibility": "role-based access, field masking by classification", "technology": "in-process policy check on every request"},
        {"name": "audit", "responsibility": "immutable change history with actor, time and prior value", "technology": "append-only table with hash chain"},
        {"name": "export", "responsibility": "open-format extraction of records and evidence", "technology": "CSV and JSON, no vendor tooling required"},
    ]

    threats = [
        {
            "category": "spoofing",
            "threat": "A caller asserts a role it does not hold",
            "mitigation": "Role is resolved from a signed session token, never from a client-supplied field alone",
            "residual": "low",
        },
        {
            "category": "tampering",
            "threat": "A record is edited without trace",
            "mitigation": "Every write appends to the audit table before the row is updated; audit rows are never updated",
            "residual": "low",
        },
        {
            "category": "repudiation",
            "threat": "An approver denies having approved",
            "mitigation": "Approvals carry actor, timestamp and payload digest in the witness chain",
            "residual": "low",
        },
        {
            "category": "information_disclosure",
            "threat": f"Personal data exposed to roles without need to know ({len(restricted) + len(confidential)} sensitive fields)",
            "mitigation": "Field masking driven by data classification, enforced server side",
            "residual": "medium" if restricted else "low",
        },
        {
            "category": "denial_of_service",
            "threat": "Unbounded export or query exhausts the host",
            "mitigation": "Page size caps and per-role rate limits",
            "residual": "medium",
        },
        {
            "category": "elevation_of_privilege",
            "threat": "An agent deploys to production without human approval",
            "mitigation": "Deployment requires a signed manifest referencing an approval record; constitutional policy denies otherwise",
            "residual": "low",
        },
    ]

    deployment = {
        "primary_estate": target_estate,
        "supported_estates": ["managed-cloud", "customer-vpc", "on-premises", "local-workstation", "air-gapped"],
        "egress": "denied by default",
        "artefacts": ["container image", "compose file", "kubernetes manifests", "terraform module", "portable bundle"],
        "data_residency": "Singapore unless the customer specifies otherwise",
    }

    cost_envelope = {
        "currency": "SGD",
        "generation_ceiling": 25.0,
        "monthly_run_estimate_low": 0.0,
        "monthly_run_estimate_high": 60.0,
        "assumption": "Single small instance plus object storage; no hosted model calls in the default deterministic profile",
    }

    test_strategy = [
        "unit: schema, classification and transition rules",
        "contract: API request and response shapes against the specification",
        "integration: create, transition, approve, export round trip",
        "policy: a prohibited action is refused and the refusal is witnessed",
        "adversarial: role escalation attempt, path traversal, audit tamper",
        "acceptance: one criterion per line in the approved specification",
    ]

    rollback = {
        "strategy": "immutable releases with previous release retained",
        "data": "forward-only migrations with a tested down path for the last release",
        "trigger": "failed acceptance evaluation, policy breach, or Captain instruction",
        "max_time_to_reverse_minutes": 10,
    }

    decisions = [
        ArchitectureDecision(
            id="ADR-0001",
            title="Specification is the authoritative artefact",
            status="accepted",
            context="Generated code drifts. Chat history is not an artefact that survives a staffing change.",
            decision="The approved specification is authoritative. Code, tests and deployment are derived from it, and drift is measured against it.",
            consequences=[
                "Regeneration is a governed operation rather than a rewrite",
                "Every acceptance criterion must map to at least one executable check",
            ],
            alternatives=["Treat the repository as the source of truth", "Treat the conversation as the source of truth"],
        ),
        ArchitectureDecision(
            id="ADR-0002",
            title="Deterministic offline model adapter is the default",
            status="accepted",
            context="The factory must run in air-gapped estates and in CI with no vendor credential.",
            decision="The default model adapter is deterministic and local. Hosted and local-runtime adapters are opt-in and change fidelity, never control flow.",
            consequences=["The full pipeline and its tests run offline", "Model output quality varies by adapter; governance behaviour does not"],
            alternatives=["Require a hosted model for all stages", "Mock the model only in tests"],
        ),
        ArchitectureDecision(
            id="ADR-0003",
            title="Evidence gates completion",
            status="accepted",
            context="An agent reporting completion has no standing on its own.",
            decision="A task is complete only when its evidence bundle satisfies the acceptance contract. Failing evidence blocks the Captain's Gate packet from being marked ready.",
            consequences=["Slower nominal throughput", "Auditable completion claims"],
            alternatives=["Trust agent self-report with sampling"],
        ),
        ArchitectureDecision(
            id="ADR-0004",
            title=f"Primary deployment estate is {target_estate}",
            status="proposed",
            context="Data residency and sovereignty requirements dominate hosting convenience for institutional customers.",
            decision=f"Target {target_estate} first, with an unchanged portable bundle for the other four estates.",
            consequences=["Higher operational burden on the customer", "No platform captivity"],
            alternatives=["Managed cloud first", "Local workstation first"],
        ),
    ]
    if restricted:
        decisions.append(
            ArchitectureDecision(
                id="ADR-0005",
                title="Restricted fields are masked by default",
                status="accepted",
                context=f"The source dataset carries restricted fields: {', '.join(restricted)}.",
                decision="Restricted fields are masked server side unless the requesting role holds an explicit need-to-know grant.",
                consequences=["Some operational roles will need an explicit grant", "Reduces disclosure blast radius"],
                alternatives=["Mask in the client", "Rely on role separation alone"],
            )
        )

    return ArchitecturePlan(
        components=components,
        data_classification=classification,
        threat_model=threats,
        deployment=deployment,
        cost_envelope=cost_envelope,
        test_strategy=test_strategy,
        rollback=rollback,
        decisions=decisions,
    )
