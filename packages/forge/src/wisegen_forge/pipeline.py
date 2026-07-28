"""The runtime spine: intake to operational learning, in nine governed stages.

    1 intake            5 branchable execution      9 operational learning
    2 intent compile    6 continuous verification
    3 architecture      7 Captain's Gate
    4 mission planning  8 deployment

Every stage writes to the witness chain, charges the cost governor and asks the
policy engine before it acts. Nothing here needs a network connection or a
vendor credential to complete.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import mini_yaml
from .agent_runtime import AgentContext, AgentRegistry, AgentRuntime
from .approval import ApprovalService, GatePacket
from .architecture import ArchitecturePlan, design
from .cost import Budget, CostGovernor
from .deployment import DeploymentService
from .domain import ForgeObject, utc_now
from .evaluation import EvaluationEngine, EvaluationReport
from .exporter import export_bundle
from .generators import webapp
from .intent_compiler import IntakeRecord, IntentCompiler, Specification
from .model_router import ModelRouter
from .orchestrator import MissionGraph, Orchestrator, Task
from .policy import PolicyEngine
from .spreadsheet_compiler import SheetModel, compile_sheet
from .tool_gateway import ToolGateway
from .witness import WitnessChain

DEFAULT_CANDIDATES = ("conservative", "performance")


@dataclass
class RunResult:
    run_root: Path
    specification: Specification | None = None
    sheet: SheetModel | None = None
    plan: ArchitecturePlan | None = None
    graph: MissionGraph | None = None
    execution: dict[str, Any] = field(default_factory=dict)
    report: EvaluationReport | None = None
    packet: GatePacket | None = None
    decision: dict[str, Any] | None = None
    deployment: dict[str, Any] | None = None
    bundle: Path | None = None
    cost: dict[str, Any] = field(default_factory=dict)
    witness: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        return {
            "run_root": str(self.run_root),
            "objective": self.specification.objective if self.specification else None,
            "risk_tier": self.specification.risk_tier if self.specification else None,
            "candidates": [task.candidate_label for task in (self.graph.tasks.values() if self.graph else []) if task.candidate_label],
            "execution": self.execution,
            "evaluation": self.report.to_dict() if self.report else None,
            "gate_ready": self.packet.ready if self.packet else None,
            "decision": self.decision,
            "deployment": self.deployment,
            "bundle": str(self.bundle) if self.bundle else None,
            "cost": self.cost,
            "witness": self.witness,
        }


class ForgeRun:
    """One governed run of the factory."""

    def __init__(
        self,
        repo_root: str | Path,
        run_root: str | Path,
        project: str = "demo",
        target_estate: str = "customer-vpc",
        allow_network: bool = False,
        budget: Budget | None = None,
    ) -> None:
        self.repo_root = Path(repo_root)
        self.run_root = Path(run_root)
        self.run_root.mkdir(parents=True, exist_ok=True)
        self.project = project
        self.target_estate = target_estate

        self.witness = WitnessChain(self.run_root / "evidence" / "witness.jsonl")
        self.governor = CostGovernor(project_budget=budget or Budget())
        self.policy = PolicyEngine(self.repo_root / "policies")
        self.router = ModelRouter.from_policy_file(self.governor, self.repo_root / "policies" / "model-routing" / "routing.yaml")
        self.tools = ToolGateway(self.run_root / "workspace", self.policy, self.witness, self.governor, allow_network)
        self.registry = AgentRegistry(self.repo_root / "agents" / "registry.yaml")
        self.runtime = AgentRuntime(self.registry, self.policy, self.tools, self.router, self.witness, self.governor)
        self.evaluator = EvaluationEngine(self.run_root / "workspace")
        self.approvals = ApprovalService(self.run_root / "approvals", self.witness)
        self.deployer = DeploymentService(self.run_root, self.witness)
        self.result = RunResult(run_root=self.run_root)
        self._register_handlers()
        self.witness.append("forge", "run.started", {"project": project, "estate": target_estate, "at": utc_now()})

    # ------------------------------------------------------ stage 1 and 2
    def intake(self, statement: str, paths: list[str | Path] | None = None, submitted_by: str = "captain") -> IntakeRecord:
        record = IntakeRecord.from_paths(statement, list(paths or []), submitted_by)
        obj = record.to_object()
        self._persist("intake", obj)
        self.witness.append("forge", "intake.recorded", {"object_id": obj.id, "digest": obj.digest()})
        return record

    def compile_intent(self, record: IntakeRecord) -> Specification:
        spec = IntentCompiler(self.router).compile(record)
        self.result.specification = spec
        obj = ForgeObject.create("specification", spec.to_dict(), created_from="intent_compiler", classification="confidential")
        self._persist("specification", obj)
        self.witness.append("gaie.intent-compiler", "specification.compiled", {"object_id": obj.id, "risk_tier": spec.risk_tier})
        return spec

    def compile_datasets(self, record: IntakeRecord) -> SheetModel | None:
        if not record.datasets:
            return None
        sheet = compile_sheet(record.datasets[0]["path"])
        self.result.sheet = sheet
        obj = ForgeObject.create("data_model", sheet.to_dict(), created_from="spreadsheet_compiler", classification="confidential")
        self._persist("data_model", obj)
        self.witness.append(
            "gaie.data-engineer",
            "dataset.compiled",
            {"entity": sheet.entity, "rows": sheet.row_count, "quality": sheet.quality["verdict"]},
        )
        return sheet

    # ---------------------------------------------------------- stage 3
    def design_architecture(self, spec: Specification, sheet: SheetModel | None) -> ArchitecturePlan:
        plan = design(spec, sheet, self.target_estate)
        self.result.plan = plan
        obj = ForgeObject.create("architecture", plan.to_dict(), created_from="architecture_engine")
        self._persist("architecture", obj)
        decisions_dir = self.run_root / "decisions"
        decisions_dir.mkdir(parents=True, exist_ok=True)
        for decision in plan.decisions:
            (decisions_dir / f"{decision.id}.md").write_text(decision.to_markdown(), encoding="utf-8")
        self.witness.append("kaie.architect", "architecture.designed", {"decisions": [d.id for d in plan.decisions]})
        return plan

    # ---------------------------------------------------- stages 4 and 5
    def plan_mission(self, spec: Specification, sheet: SheetModel, candidates: tuple[str, ...] = DEFAULT_CANDIDATES) -> MissionGraph:
        graph = MissionGraph()
        schema = graph.add("generate_schema", "gaie.data-engineer", capability="generate_schema")
        base = graph.add("generate_application", "gaie.backend-engineer", [schema.id], capability="generate_application")
        graph.tasks.pop(base.id)
        forks = graph.branch(base, list(candidates))
        verify_ids: list[str] = []
        for fork in forks:
            verify = graph.add(
                f"verify [{fork.candidate_label}]",
                "kaie.assurance-engineer",
                [fork.id],
                capability="verify_candidate",
                candidate=fork.candidate_label,
            )
            verify_ids.append(verify.id)
        review = graph.add("security_review", "kaie.security-auditor", verify_ids, capability="security_review")
        graph.add("package_release", "paie.release-engineer", [review.id], capability="package_release")
        self.result.graph = graph
        self.witness.append("paie.orchestrator", "mission.planned", graph.to_dict())
        return graph

    def execute(self, graph: MissionGraph) -> dict[str, Any]:
        orchestrator = Orchestrator(
            runner=self.runtime.run,
            on_event=lambda event, payload: self.witness.append("paie.orchestrator", event, payload),
        )
        summary = orchestrator.execute(graph, stop_on_error=False)
        self.result.execution = summary
        return summary

    # ---------------------------------------------------------- stage 6
    def evaluate(self, spec: Specification, sheet: SheetModel, graph: MissionGraph) -> EvaluationReport:
        report = EvaluationReport()
        candidates = [task for task in graph.tasks.values() if task.candidate_label and task.name.startswith("generate_application")]
        chosen = next((task for task in candidates if task.state == "completed"), None)
        prefix = f"app_{chosen.candidate_label}" if chosen else "app"

        report.add(self.evaluator.gate_artefacts_present([f"{prefix}/app.py", f"{prefix}/test_app.py", "schema.sql", f"{prefix}/openapi.json"]))
        report.add(self.evaluator.gate_compiles([f"{prefix}/app.py", f"{prefix}/test_app.py"]))

        verify_tasks = [task for task in graph.tasks.values() if task.name.startswith("verify") and task.result]
        test_result = next(
            (task.result["evidence"]["tests"] for task in verify_tasks if chosen and task.payload.get("candidate") == chosen.candidate_label),
            {"ok": False, "summary": "no test evidence"},
        )
        report.add(self.evaluator.gate_tests(test_result))

        test_source = (self.run_root / "workspace" / prefix / "test_app.py")
        report.add(
            self.evaluator.gate_acceptance_coverage(
                spec.acceptance_criteria, test_source.read_text(encoding="utf-8") if test_source.exists() else ""
            )
        )
        report.add(self.evaluator.gate_data_quality(sheet.quality))

        seen = [entry.event for entry in self.witness.entries()]
        report.add(
            self.evaluator.gate_provenance(
                self.witness.verify(),
                ["intake.recorded", "specification.compiled", "mission.planned", "agent.completed"],
                seen,
            )
        )
        refusals = [entry.payload for entry in self.witness.entries() if entry.event in ("tool.refused", "policy.refused", "authority.refused")]
        report.add(self.evaluator.gate_policy(refusals, expect_refusals=False))
        report.add(self.evaluator.gate_cost(self.governor.snapshot()))

        self.result.report = report
        (self.run_root / "evidence").mkdir(parents=True, exist_ok=True)
        (self.run_root / "evidence" / "evaluation.json").write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
        self.witness.append("kaie.assurance-engineer", "evaluation.completed", {"passed": report.passed, "failed": [r.gate for r in report.failures]})
        return report

    # ---------------------------------------------------------- stage 7
    def build_gate_packet(self, spec: Specification, plan: ArchitecturePlan, graph: MissionGraph, report: EvaluationReport) -> GatePacket:
        written = sorted(self.tools._fs_list("."))
        models = [spec.provenance.get("model")] if spec.provenance.get("model") else []
        branches = []
        for task in graph.tasks.values():
            if not task.candidate_label or not task.name.startswith("generate_application"):
                continue
            verify = next((t for t in graph.tasks.values() if t.name == f"verify [{task.candidate_label}]"), None)
            verdict = "passed" if verify and verify.state == "completed" and verify.result and verify.result["evidence"]["tests"]["ok"] else "failed"
            branches.append(
                {
                    "label": task.candidate_label,
                    "verdict": verdict,
                    "sgd": self.governor.snapshot()["by_actor"].get("gaie.backend-engineer", {}).get("sgd", 0.0),
                    "note": task.result.get("note", "") if task.result else task.error or "",
                }
            )

        packet = GatePacket(
            what_changed=[f"created {len(written)} artefact(s) in the run workspace"] + [f"- {name}" for name in written[:12]],
            why=spec.objective,
            agents=sorted({task.agent for task in graph.tasks.values()}),
            models=models,
            tools_invoked=[entry.payload.get("tool", "") for entry in self.witness.entries() if entry.event == "tool.invoked"],
            evidence_passed=[result.gate for result in report.results if result.passed],
            evidence_failed=[f"{result.gate}: {result.detail}" for result in report.failures],
            residual_risks=[f"{threat['category']}: {threat['threat']} (residual {threat['residual']})" for threat in plan.threat_model if threat["residual"] != "low"],
            cost=self.governor.snapshot(),
            reversal=f"Delete release artefacts and redeploy {plan.rollback['strategy']}; maximum time to reverse {plan.rollback['max_time_to_reverse_minutes']} minutes.",
            branches=branches,
            open_questions=spec.open_questions,
        )
        self.approvals.submit(packet)
        self.result.packet = packet
        return packet

    def decide(self, packet: GatePacket, action: str, decided_by: str, rationale: str, selected_branch: str | None = None) -> dict[str, Any]:
        decision = self.approvals.decide(packet, action, decided_by, rationale, selected_branch=selected_branch)
        self.result.decision = decision.to_dict()
        return self.result.decision

    # ------------------------------------------------------ stages 8 and 9
    def deploy(self, packet: GatePacket, release: str, environment: str = "production", dry_run: bool = True) -> dict[str, Any]:
        decision = self.approvals.decision_for(packet.id)
        if decision is None or decision.action not in ("approve", "approve_with_conditions", "select_branch"):
            raise PermissionError("no approving Captain's Gate decision for this packet")
        manifest = self.deployer.prepare(
            release=release,
            target_estate=self.target_estate,
            environment=environment,
            artefact_root=self.run_root / "workspace",
            approvals=[packet.id],
            evidence_bundle=str((self.run_root / "evidence" / "evaluation.json").relative_to(self.run_root)),
            rollback_release=self.deployer.previous_release(exclude=release),
        )
        outcome = self.deployer.apply(manifest, dry_run=dry_run)
        self.result.deployment = outcome
        return outcome

    def export(self, destination: str | Path | None = None) -> Path:
        target = Path(destination or self.run_root / "portable-bundle.zip")
        bundle = export_bundle(self.run_root, self.repo_root, target, {"project": self.project, "estate": self.target_estate})
        self.result.bundle = bundle
        self.witness.append("forge", "bundle.exported", {"path": str(bundle)})
        return bundle

    def learning_record(self) -> dict[str, Any]:
        """Stage 9. Production evidence feeds back, but never automatically."""
        report = self.result.report
        record = {
            "at": utc_now(),
            "project": self.project,
            "gates_failed": [result.gate for result in (report.failures if report else [])],
            "cost": self.governor.snapshot(),
            "candidate_outcomes": [branch for branch in (self.result.packet.branches if self.result.packet else [])],
            "proposed_updates": [
                "promote the selected candidate's generator settings to the template library",
                "raise the data-quality minimum if remediation was required",
            ],
            "applied": False,
            "note": "Updates pass through a governed learning gate. Nothing here retrains or alters production behaviour automatically.",
        }
        path = self.run_root / "evidence" / "learning-record.json"
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        self.witness.append("saie.librarian", "learning.recorded", {"gates_failed": record["gates_failed"], "applied": False})
        return record

    # ------------------------------------------------------------ helpers
    def _persist(self, name: str, obj: ForgeObject) -> None:
        directory = self.run_root / "objects"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / f"{name}.json").write_text(json.dumps(obj.to_dict(), indent=2), encoding="utf-8")

    def finalise(self) -> RunResult:
        self.result.cost = self.governor.snapshot()
        self.result.witness = self.witness.verify()
        (self.run_root / "run-summary.json").write_text(json.dumps(self.result.summary(), indent=2), encoding="utf-8")
        self.witness.append("forge", "run.finalised", {"passed": self.result.report.passed if self.result.report else None})
        return self.result

    # --------------------------------------------------------- handlers
    def _register_handlers(self) -> None:
        run = self

        @run.runtime.handler("generate_schema")
        def generate_schema(context: AgentContext) -> dict[str, Any]:
            config = run._config("conservative")
            written = context.tools.invoke(context.agent.id, "fs_write", path="schema.sql", content=webapp.render_schema_sql(config))
            return {"evidence": {"files_written": [written["path"]]}, "artefacts": [written["path"]]}

        @run.runtime.handler("generate_application")
        def generate_application(context: AgentContext) -> dict[str, Any]:
            candidate = str(context.task.candidate_label or "conservative")
            config = run._config(candidate)
            folder = f"app_{candidate}"
            files = {
                f"{folder}/app.py": webapp.render_app(config),
                f"{folder}/test_app.py": webapp.render_tests(config),
                f"{folder}/openapi.json": webapp.render_openapi(config),
                f"{folder}/README.md": webapp.render_readme(config, run.result.specification),
                f"{folder}/Dockerfile": webapp.render_dockerfile(config),
            }
            written = [context.tools.invoke(context.agent.id, "fs_write", path=path, content=body)["path"] for path, body in files.items()]
            syntax = context.tools.invoke(context.agent.id, "py_compile", path=f"{folder}/app.py")
            return {
                "evidence": {"files_written": written, "syntax_check": syntax},
                "note": f"{candidate} profile, page cap {config['page_size_cap']}",
            }

        @run.runtime.handler("verify_candidate")
        def verify_candidate(context: AgentContext) -> dict[str, Any]:
            candidate = str(context.payload.get("candidate") or "conservative")
            folder = f"app_{candidate}"
            syntax = context.tools.invoke(context.agent.id, "py_compile", path=f"{folder}/test_app.py")
            tests = context.tools.invoke(context.agent.id, "run_tests", path=f"{folder}/test_app.py")
            return {"evidence": {"syntax_check": syntax, "tests": tests}, "candidate": candidate}

        @run.runtime.handler("security_review")
        def security_review(context: AgentContext) -> dict[str, Any]:
            findings: list[dict[str, str]] = []
            for name in context.tools.invoke(context.agent.id, "fs_list", path="."):
                if not name.endswith(".py"):
                    continue
                source = context.tools.invoke(context.agent.id, "fs_read", path=name)
                for pattern, issue, severity in (
                    ("eval(", "dynamic evaluation of input", "high"),
                    ("subprocess", "process execution in generated code", "medium"),
                    ("urllib.request", "outbound network call in generated code", "high"),
                    ("verify=False", "TLS verification disabled", "critical"),
                ):
                    if pattern in source:
                        findings.append({"file": name, "issue": issue, "severity": severity, "pattern": pattern})
            return {"evidence": {"static_analysis": {"files_scanned": len(context.tools.invoke(context.agent.id, "fs_list", path=".")), "findings": findings}}}

        @run.runtime.handler("package_release")
        def package_release(context: AgentContext) -> dict[str, Any]:
            files = context.tools.invoke(context.agent.id, "fs_list", path=".")
            manifest = {"files": files, "packaged_at": utc_now(), "estate": run.target_estate}
            written = context.tools.invoke(
                context.agent.id, "fs_write", path="release-contents.json", content=json.dumps(manifest, indent=2)
            )
            return {"evidence": {"package_manifest": written, "file_count": len(files)}}

    def _config(self, candidate: str) -> dict[str, Any]:
        if self.result.specification is None or self.result.sheet is None:
            raise RuntimeError("specification and data model must exist before generation")
        return webapp.build_config(self.result.specification, self.result.sheet, candidate)


def run_full_pipeline(
    repo_root: str | Path,
    run_root: str | Path,
    statement: str,
    inputs: list[str | Path],
    project: str = "demo",
    target_estate: str = "customer-vpc",
    auto_decide: bool = True,
    release: str = "1.0.0",
) -> RunResult:
    """Stages 1 to 9 in order. Used by `forge demo` and by the acceptance tests."""
    run = ForgeRun(repo_root, run_root, project=project, target_estate=target_estate)
    record = run.intake(statement, inputs)
    spec = run.compile_intent(record)
    sheet = run.compile_datasets(record)
    if sheet is None:
        raise ValueError("this workflow requires at least one dataset in the intake")
    plan = run.design_architecture(spec, sheet)
    graph = run.plan_mission(spec, sheet)
    run.execute(graph)
    report = run.evaluate(spec, sheet, graph)
    packet = run.build_gate_packet(spec, plan, graph, report)

    if auto_decide and packet.ready:
        winner = next((branch["label"] for branch in packet.branches if branch["verdict"] == "passed"), None)
        run.decide(
            packet,
            "select_branch" if winner else "request_revision",
            decided_by="captain (unattended demo profile)",
            rationale="Demo profile records an explicit decision so the deployment path is exercised. "
            "In an attended run this decision belongs to a named human.",
            selected_branch=winner,
        )
        if winner:
            run.deploy(packet, release=release, dry_run=True)
    run.export()
    run.learning_record()
    return run.finalise()
