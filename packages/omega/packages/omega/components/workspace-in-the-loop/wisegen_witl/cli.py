from __future__ import annotations

import argparse
import json
from pathlib import Path

from wisegen_witl.core.engine import run_workspace
from wisegen_witl.core.witness import WitnessChain
from wisegen_witl.storage.json_store import read_json, write_json


def cmd_run(args: argparse.Namespace) -> int:
    case = read_json(args.case)
    workflow = read_json(args.workflow)
    report = run_workspace(case, workflow, witness_path=args.witness)
    write_json(args.out, report.to_dict())
    print(f"Decision report written to {args.out}")
    print(f"Recommendation: {report.recommendation}")
    print(f"Captain Gate: {report.captain_gate['status']}")
    print(f"Witness hash: {report.witness_hash}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    chain = WitnessChain(args.log)
    rows = chain.read()
    print(json.dumps({"log": str(Path(args.log)), "events": len(rows), "last_hash": rows[-1]["hash"] if rows else None}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wisegen-witl", description="WiseGen Workspace-in-the-Loop CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run a governed workspace decision")
    run.add_argument("--case", required=True)
    run.add_argument("--workflow", required=True)
    run.add_argument("--out", default="outputs/decision_report.json")
    run.add_argument("--witness", default="audit/witness-chain.jsonl")
    run.set_defaults(func=cmd_run)

    audit = sub.add_parser("audit", help="Inspect witness chain")
    audit.add_argument("--log", default="audit/witness-chain.jsonl")
    audit.set_defaults(func=cmd_audit)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
