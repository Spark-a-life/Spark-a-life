from __future__ import annotations
import argparse, json
from .contracts import validate_contract
from .io import load_yaml, read_json
from .engine import compile_mission, run_mission


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='wcef', description='WiseGen Creative Engineering Framework CLI')
    sub = parser.add_subparsers(dest='cmd', required=True)
    p_val = sub.add_parser('validate'); p_val.add_argument('brief')
    p_compile = sub.add_parser('compile'); p_compile.add_argument('brief')
    p_run = sub.add_parser('run'); p_run.add_argument('brief'); p_run.add_argument('--output', default='outputs/run.json')
    p_inspect = sub.add_parser('inspect'); p_inspect.add_argument('run_json')
    args = parser.parse_args(argv)
    if args.cmd == 'validate':
        errors = validate_contract(load_yaml(args.brief))
        if errors:
            print('\n'.join(errors)); return 1
        print('valid'); return 0
    if args.cmd == 'compile':
        print(json.dumps(compile_mission(args.brief), indent=2, ensure_ascii=False)); return 0
    if args.cmd == 'run':
        result = run_mission(args.brief, args.output)
        print(json.dumps({'output': args.output, 'decision': result['evaluation']['captain_gate'], 'witness_path': result['witness_path']}, indent=2)); return 0
    if args.cmd == 'inspect':
        result = read_json(args.run_json)
        print(json.dumps({'mission_id': result['brief']['mission']['id'], 'adapter': result['adapter_result']['adapter'], 'score': result['evaluation']['weighted_score'], 'decision': result['evaluation']['captain_gate'], 'circuit_state': result['circuit_state']}, indent=2)); return 0
    return 2

if __name__ == '__main__':
    raise SystemExit(main())
