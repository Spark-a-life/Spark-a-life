import argparse, sys
from .io import load_data
from .pipeline import repository_root, run_project
from .validation import ProjectValidationError, validate_project

def main():
    parser = argparse.ArgumentParser(prog="wisegen-pip")
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate")
    v.add_argument("project")
    r = sub.add_parser("run")
    r.add_argument("project")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            validate_project(load_data(args.project), repository_root() / "schemas" / "project.schema.json")
            print("VALID")
        else:
            result = run_project(args.project)
            print(f"build_dir={result.build_dir}")
            print(f"release_status={result.release_status}")
            print(f"quality_score={result.quality_score:.4f}")
            print(f"witness_id={result.witness_id}")
    except (ProjectValidationError, ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
