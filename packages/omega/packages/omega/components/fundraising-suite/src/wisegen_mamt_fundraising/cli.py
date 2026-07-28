from __future__ import annotations

from dataclasses import asdict
import argparse
import json
from pathlib import Path
from typing import Sequence

from .audit.witness_chain import WitnessChain
from .contracts import ContractError, load_brief
from .engine import run_mission
from .prompting.master_prompt import generate_master_prompt
from .release.manifest import write_release_manifest
from .release.preflight import run_preflight, write_preflight_report
from .safeguards.review import safeguard_review


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wg-fund", description="WiseGen MAMT Fundraising Suite")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate a fundraising mission YAML contract")
    validate.add_argument("mission")

    run = sub.add_parser("run", help="Run a fundraising mission locally")
    run.add_argument("mission")
    run.add_argument("--output", default="outputs/fundraising_run.json")
    run.add_argument("--audit", default="outputs/witness_chain.jsonl")

    inspect = sub.add_parser("inspect", help="Inspect a generated run JSON")
    inspect.add_argument("run_json")

    prompt = sub.add_parser("prompt", help="Generate the WiseGen Master Super Prompt")
    prompt.add_argument("--project-name", default="wisegen-mamt-fundraising-suite")
    prompt.add_argument("--route", choices=["zip", "no-zip"], default="zip")
    prompt.add_argument("--chunk-size", type=int, default=5)

    review = sub.add_parser("review", help="Run safeguard review without executing the mission")
    review.add_argument("mission")

    audit = sub.add_parser("verify-audit", help="Verify a witness-chain JSONL file")
    audit.add_argument("audit_jsonl")

    preflight = sub.add_parser("preflight", help="Run client-shipment preflight checks")
    preflight.add_argument("--root", default=".")
    preflight.add_argument("--output", default="")

    manifest = sub.add_parser("manifest", help="Write a deterministic release manifest")
    manifest.add_argument("--root", default=".")
    manifest.add_argument("--output", default="outputs/release_manifest.json")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            brief = load_brief(args.mission)
            print(f"valid: {brief.mission.id}")
            return 0
        if args.command == "run":
            result = run_mission(args.mission, args.output, args.audit)
            print(json.dumps({"mission_id": result["mission_id"], "output": args.output}, indent=2))
            return 0
        if args.command == "inspect":
            path = Path(args.run_json)
            data = json.loads(path.read_text(encoding="utf-8"))
            summary = {
                "mission_id": data["mission_id"],
                "version": data.get("version", "unknown"),
                "decision": data["captain_gate"]["decision"],
                "egress_allowed": data["captain_gate"]["egress_allowed"],
                "weighted_score": data["evaluation"]["weighted_score"],
                "compliance_findings": len(data["compliance_findings"]),
                "donor_due_diligence_items": len(data.get("donor_due_diligence", [])),
            }
            print(json.dumps(summary, indent=2))
            return 0
        if args.command == "prompt":
            print(generate_master_prompt(args.project_name, args.route, args.chunk_size))
            return 0
        if args.command == "review":
            brief = load_brief(args.mission)
            findings = safeguard_review(brief)
            print(json.dumps([asdict(item) for item in findings], indent=2, ensure_ascii=False))
            return 1 if any(item.status == "block" for item in findings) else 0
        if args.command == "verify-audit":
            verified = WitnessChain(args.audit_jsonl).verify()
            print(json.dumps({"audit": args.audit_jsonl, "verified": verified}, indent=2))
            return 0 if verified else 1
        if args.command == "preflight":
            if args.output:
                report = write_preflight_report(args.output, args.root)
            else:
                report = run_preflight(args.root)
            print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
            return 0 if report.status == "pass" else 1
        if args.command == "manifest":
            manifest = write_release_manifest(args.output, args.root)
            print(json.dumps({"output": args.output, "file_count": manifest["file_count"]}, indent=2))
            return 0
    except (ContractError, ValueError, FileNotFoundError, PermissionError, json.JSONDecodeError) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
