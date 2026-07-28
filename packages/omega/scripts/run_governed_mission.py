#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
OS = ROOT / 'packages' / 'intelligence-os'
OMEGA = ROOT / 'packages' / 'omega'

def load(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f) if path.suffix.lower() in {'.yaml','.yml'} else json.load(f)

def derive_request(mission: dict) -> dict:
    captain = mission.get('captain', {})
    decision = str(captain.get('decision','DEFER')).upper()
    approved = decision in {'APPROVE','APPROVE_WITH_CONDITIONS'}
    domain = str(mission.get('domain','strategy')).lower()
    estate = {'strategy':'MAIE','market':'TAIE','personal':'PAIE','general':'GAIE','shared':'SAIE'}.get(domain,'MAIE')
    return {
      'request_id': mission.get('mission_id','mission-unassigned'),
      'estate': estate,
      'actor': 'omega-control-plane',
      'purpose': mission.get('objective','Execute governed mission'),
      'action': 'internal_assessment',
      'risk_tier': 'medium',
      'capability_id': 'research.source-verification',
      'data_classification': 'internal',
      'external_side_effect': False,
      'human_approved': approved,
      'approval_reference': f"captain:{decision}" if approved else '',
      'runtime_id': 'local-deterministic'
    }

def main():
    p=argparse.ArgumentParser(description='Run an Omega mission through WiseGen Intelligence OS Captain\'s Gate')
    p.add_argument('mission')
    p.add_argument('--output', default=str(ROOT/'outputs'/'governed-mission.json'))
    p.add_argument('--audit', default=str(ROOT/'outputs'/'omega-witness-chain.jsonl'))
    a=p.parse_args()
    mission_path=Path(a.mission).resolve(); mission=load(mission_path)
    req=derive_request(mission)
    req_path=ROOT/'outputs'/'derived-action-request.json'; req_path.parent.mkdir(parents=True,exist_ok=True)
    req_path.write_text(json.dumps(req,indent=2),encoding='utf-8')
    gate=subprocess.run(['node','src/cli.mjs','gate',str(req_path)],cwd=OS,text=True,capture_output=True)
    if gate.returncode != 0:
        sys.stderr.write(gate.stderr); return gate.returncode
    gate_result=json.loads(gate.stdout)
    if str(gate_result.get('decision','')).upper() != 'ALLOW':
        Path(a.output).write_text(json.dumps({'status':'BLOCKED_BY_CAPTAINS_GATE','gate':gate_result},indent=2),encoding='utf-8')
        print(json.dumps({'status':'BLOCKED_BY_CAPTAINS_GATE','output':a.output},indent=2)); return 2
    cmd=[sys.executable,'-m','wisegen_omega.cli','run',str(mission_path),'--output',str(Path(a.output).resolve()),'--audit',str(Path(a.audit).resolve())]
    env=dict(__import__('os').environ); env['PYTHONPATH']=str(OMEGA/'src')
    run=subprocess.run(cmd,cwd=OMEGA,env=env)
    if run.returncode==0:
        print(json.dumps({'governance_gate':'ALLOW','omega_output':str(Path(a.output).resolve()),'derived_request':str(req_path)},indent=2))
    return run.returncode
if __name__=='__main__': raise SystemExit(main())
