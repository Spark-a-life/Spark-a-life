import argparse
import json
from .io import load_data, write_json
from .validation import validate_mission
from .engine import OmegaEngine
from .witness import verify


def main():
    parser = argparse.ArgumentParser(prog="wisegen-omega")
    sub = parser.add_subparsers(dest="command", required=True)
    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("mission")
    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("mission")
    run_cmd.add_argument("--output", required=True)
    run_cmd.add_argument("--audit", default="outputs/witness-chain.jsonl")
    inspect_cmd = sub.add_parser("inspect")
    inspect_cmd.add_argument("result")
    audit_cmd = sub.add_parser("verify-audit")
    audit_cmd.add_argument("path")
    args = parser.parse_args()

    if args.command == "validate":
        errors = validate_mission(load_data(args.mission))
        print("VALID" if not errors else "\n".join(errors))
        raise SystemExit(1 if errors else 0)

    if args.command == "run":
        mission = load_data(args.mission)
        errors = validate_mission(mission)
        if errors:
            print("\n".join(errors))
            raise SystemExit(1)
        result = OmegaEngine(args.audit).run(mission)
        write_json(args.output, result)
        print(json.dumps({"status": result["status"], "state": result["state"], "output": args.output}, indent=2))
    elif args.command == "inspect":
        data = load_data(args.result)
        print(json.dumps({k: data.get(k) for k in ("mission_id", "status", "state", "decision", "verification")}, indent=2, ensure_ascii=False))
    elif args.command == "verify-audit":
        ok, count = verify(args.path)
        print(json.dumps({"valid": ok, "records": count}, indent=2))
        raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
