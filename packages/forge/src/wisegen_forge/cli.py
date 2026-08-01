"""`forge` command line interface.

    forge doctor                     environment and repository readiness
    forge roles                      the role roster that runs an engagement
    forge intake                     record intent and inputs, stages 1 to 2
    forge compile-sheet              inspect a spreadsheet before committing
    forge plan                       show the mission graph without executing
    forge run                        stages 1 to 9, honouring the gate
    forge demo                       the reference Spreadsheet-to-Application run
    forge gate                       show or decide an open Captain's Gate packet
    forge verify                     verify a witness chain
    forge export                     produce a portable ownership bundle
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from . import __version__, mini_yaml
from .agent_runtime import AgentRegistry
from .approval import ApprovalService, GatePacket
from .cost import Budget
from .pipeline import ForgeRun, run_full_pipeline
from .policy import PolicyEngine
from .spreadsheet_compiler import compile_sheet
from .witness import WitnessChain

REPO_ROOT = Path(__file__).resolve().parents[2]


def _print(payload) -> None:
    print(json.dumps(payload, indent=2, default=str))


def cmd_doctor(args: argparse.Namespace) -> int:
    repo = Path(args.repo)
    checks = []
    checks.append(("python >= 3.10", sys.version_info >= (3, 10), f"found {sys.version.split()[0]}"))
    for folder in ("agents", "policies", "workflows", "examples", "docs", "tests"):
        checks.append((f"{folder}/ present", (repo / folder).exists(), str(repo / folder)))
    try:
        registry = AgentRegistry(repo / "agents" / "registry.yaml")
        checks.append(("agent registry loads", len(registry) > 0, f"{len(registry)} agents, v{registry.version}"))
    except Exception as exc:  # noqa: BLE001
        checks.append(("agent registry loads", False, str(exc)))
    try:
        policy = PolicyEngine(repo / "policies")
        checks.append(("policy engine loads", len(policy.rules) > 0, f"{len(policy.rules)} rules"))
        denial = policy.evaluate({"actor": "gaie.backend-engineer", "action": "capability:deploy_production", "resource": "prod"})
        checks.append(("constitutional deny works", not denial.allowed, denial.reason))
    except Exception as exc:  # noqa: BLE001
        checks.append(("policy engine loads", False, str(exc)))
    checks.append(("yaml backend", True, "PyYAML" if mini_yaml._pyyaml else "built-in subset parser"))
    checks.append(("network required", True, "no"))

    width = max(len(name) for name, _, _ in checks)
    failed = 0
    for name, ok, detail in checks:
        failed += 0 if ok else 1
        print(f"[{'ok ' if ok else 'FAIL'}] {name.ljust(width)}  {detail}")
    print(f"\n{len(checks) - failed} of {len(checks)} checks passed")
    return 0 if failed == 0 else 1


def cmd_roles(args: argparse.Namespace) -> int:
    registry = AgentRegistry(Path(args.repo) / "agents" / "registry.yaml")
    layers: dict[str, list] = {}
    for agent in registry.agents.values():
        layers.setdefault(agent.layer, []).append(agent)
    for layer in sorted(layers):
        print(f"\n== {layer} ==")
        for agent in sorted(layers[layer], key=lambda a: a.id):
            print(f"  {agent.id:<32} v{agent.version:<8} {agent.role}")
            print(f"  {'':<32} mandate: {agent.mandate}")
            print(f"  {'':<32} exit artefact: {agent.exit_artefact}")
    print(f"\n{len(registry)} roles, registry v{registry.version}")
    return 0


def cmd_compile_sheet(args: argparse.Namespace) -> int:
    _print(compile_sheet(args.path).to_dict())
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    run = ForgeRun(args.repo, args.run_root, project=args.project, target_estate=args.estate)
    record = run.intake(args.statement, args.input or [])
    spec = run.compile_intent(record)
    sheet = run.compile_datasets(record)
    if sheet is None:
        print("no dataset supplied: nothing to plan against", file=sys.stderr)
        return 2
    run.design_architecture(spec, sheet)
    graph = run.plan_mission(spec, sheet)
    _print({"specification": spec.to_dict(), "mission": graph.to_dict()})
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    result = run_full_pipeline(
        repo_root=args.repo,
        run_root=args.run_root,
        statement=args.statement,
        inputs=args.input or [],
        project=args.project,
        target_estate=args.estate,
        auto_decide=not args.hold_at_gate,
        release=args.release,
    )
    _print(result.summary())
    return 0 if (result.report and result.report.passed) else 1


def cmd_demo(args: argparse.Namespace) -> int:
    repo = Path(args.repo)
    run_root = Path(args.run_root)
    if run_root.exists() and not args.keep:
        # A run root holds one run. Appending a second run's evidence over the
        # first one's artefacts would leave the chain pointing at files that no
        # longer exist. Pass --keep to accumulate deliberately.
        shutil.rmtree(run_root)
    example = repo / "examples" / "employee-onboarding"
    statement = (example / "requirement.md").read_text(encoding="utf-8")
    inputs = [example / "onboarding.csv", example / "hr-policy.md", example / "org-chart.csv"]
    result = run_full_pipeline(
        repo_root=repo,
        run_root=args.run_root,
        statement=statement,
        inputs=inputs,
        project="employee-onboarding",
        target_estate=args.estate,
        auto_decide=True,
        release="1.0.0",
    )
    summary = result.summary()
    _print(summary)
    print("\nGate packet:", result.packet.id if result.packet else "none")
    print("Workspace:", Path(args.run_root) / "workspace")
    print("Bundle:", result.bundle)
    return 0 if (result.report and result.report.passed) else 1


def cmd_gate(args: argparse.Namespace) -> int:
    store = Path(args.run_root) / "approvals"
    witness = WitnessChain(Path(args.run_root) / "evidence" / "witness.jsonl")
    service = ApprovalService(store, witness)
    packets = sorted(path for path in store.glob("*.json") if ".decision" not in path.name)
    if not packets:
        print("no gate packets found", file=sys.stderr)
        return 2
    latest = json.loads(packets[-1].read_text(encoding="utf-8"))
    if not args.action:
        print((store / f"{latest['id']}.md").read_text(encoding="utf-8"))
        return 0
    packet = GatePacket(
        id=latest["id"],
        what_changed=latest["what_changed"],
        why=latest["why"],
        evidence_passed=latest["evidence_passed"],
        evidence_failed=latest["evidence_failed"],
        branches=latest["candidate_branches"],
    )
    decision = service.decide(packet, args.action, args.by, args.rationale, selected_branch=args.branch)
    _print(decision.to_dict())
    return 0


def resolve_chain(target: str) -> Path:
    """Accept a run directory or a chain file, so operators need not remember the layout."""
    path = Path(target)
    if path.is_dir():
        candidate = path / "evidence" / "witness.jsonl"
        if candidate.exists():
            return candidate
        found = sorted(path.rglob("witness*.jsonl"))
        if found:
            return found[0]
        raise SystemExit(f"no witness chain found under {path}")
    return path


def cmd_verify(args: argparse.Namespace) -> int:
    chain = resolve_chain(args.chain or args.run_root)
    verification = WitnessChain(chain).verify()
    verification["chain"] = str(chain)
    _print(verification)
    return 0 if verification["ok"] else 1


def cmd_export(args: argparse.Namespace) -> int:
    from .exporter import export_bundle

    bundle = export_bundle(args.run_root, args.repo, args.out)
    print(bundle)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="forge", description="WiseGen Forge: governed intent-to-system application factory")
    parser.add_argument("--version", action="version", version=f"wisegen-forge {__version__}")
    parser.add_argument("--repo", default=str(REPO_ROOT), help="repository root holding agents, policies and workflows")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="check environment and repository readiness")
    doctor.set_defaults(func=cmd_doctor)

    roles = subparsers.add_parser("roles", help="print the role roster")
    roles.set_defaults(func=cmd_roles)

    sheet = subparsers.add_parser("compile-sheet", help="inspect a spreadsheet: schema, classification, workflow, quality")
    sheet.add_argument("path")
    sheet.set_defaults(func=cmd_compile_sheet)

    for name, handler, help_text in (("plan", cmd_plan, "plan without executing"), ("run", cmd_run, "run the full pipeline")):
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("statement")
        command.add_argument("--input", action="append", help="path to a document or dataset (repeatable)")
        command.add_argument("--run", "--run-root", dest="run_root", default="./.forge/run")
        command.add_argument("--project", default="adhoc")
        command.add_argument("--estate", default="customer-vpc")
        command.add_argument("--release", default="1.0.0")
        command.add_argument("--hold-at-gate", action="store_true", help="stop at the Captain's Gate for a human decision")
        command.set_defaults(func=handler)

    demo = subparsers.add_parser("demo", help="run the reference Spreadsheet-to-Application demonstrator")
    demo.add_argument("--run", "--run-root", dest="run_root", default="./.forge/demo")
    demo.add_argument("--estate", default="customer-vpc")
    demo.add_argument("--keep", action="store_true", help="append to an existing run root instead of starting fresh")
    demo.set_defaults(func=cmd_demo)

    gate = subparsers.add_parser("gate", help="show or decide the latest Captain's Gate packet")
    gate.add_argument("--run", "--run-root", dest="run_root", default="./.forge/demo")
    gate.add_argument("--action", choices=["approve", "reject", "request_revision", "approve_with_conditions", "select_branch", "combine_branches", "escalate"])
    gate.add_argument("--by", default="captain")
    gate.add_argument("--rationale", default="reviewed at the Captain's Gate")
    gate.add_argument("--branch")
    gate.set_defaults(func=cmd_gate)

    verify = subparsers.add_parser("verify", help="verify a witness chain")
    verify.add_argument("chain", nargs="?", help="a run directory or a witness chain file")
    verify.add_argument("--run", "--run-root", dest="run_root", default="./.forge/demo")
    verify.set_defaults(func=cmd_verify)

    export = subparsers.add_parser("export", help="produce a portable ownership bundle")
    export.add_argument("--run", "--run-root", dest="run_root", default="./.forge/demo")
    export.add_argument("--out", default="./portable-bundle.zip")
    export.set_defaults(func=cmd_export)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except BrokenPipeError:
        # Operators pipe into head and less routinely. A closed pipe is not an
        # error, and a traceback here would look like a failed governed run.
        # Redirect the descriptor before the interpreter flushes on exit.
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 1)
        return 0
    except KeyboardInterrupt:
        print("\ninterrupted: the run halted at a safe point, evidence is intact", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
