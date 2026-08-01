from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from wisegen_witl.core.models import Criterion, DecisionReport, Evidence, Option, WorkspaceState
from wisegen_witl.core.ranking import rank_options
from wisegen_witl.core.risk import assess_risk, captain_gate_decision
from wisegen_witl.core.witness import WitnessChain
from wisegen_witl.lanes.default_lanes import run_default_lanes


def _build_evidence(rows: List[Dict[str, Any]]) -> List[Evidence]:
    return [Evidence(**row) for row in rows]


def _build_options(rows: List[Dict[str, Any]]) -> List[Option]:
    return [Option(**row) for row in rows]


def _build_criteria(rows: List[Dict[str, Any]]) -> List[Criterion]:
    return [Criterion(**row) for row in rows]


def run_workspace(case: Dict[str, Any], workflow: Dict[str, Any], witness_path: str = "audit/witness-chain.jsonl") -> DecisionReport:
    workspace = WorkspaceState(
        workspace_id=f"witl-{uuid4().hex[:12]}",
        workflow_id=workflow["workflow_id"],
        domain=workflow["domain"],
        objective=case["objective"],
        initiator=case.get("initiator", "unknown"),
        decision_authority=case.get("decision_authority", workflow.get("default_decision_authority", "Captain")),
        constraints=case.get("constraints", []),
        evidence=_build_evidence(case.get("evidence", [])),
        options=_build_options(case.get("options", [])),
        criteria=_build_criteria(workflow.get("criteria", [])),
        assumptions=case.get("assumptions", []),
        hypotheses=case.get("hypotheses", []),
    )

    witness = WitnessChain(witness_path)
    witness.record("workspace_created", workspace.to_dict())

    workspace.lanes = run_default_lanes(workspace)
    witness.record("lane_deliberation_completed", {"workspace_id": workspace.workspace_id, "lanes": [x.__dict__ for x in workspace.lanes]})

    workspace.ranking = rank_options(workspace.options, workspace.criteria)
    witness.record("ranking_completed", {"workspace_id": workspace.workspace_id, "ranking": [x.__dict__ for x in workspace.ranking]})

    threshold = float(workflow.get("captain_gate", {}).get("risk_threshold", 0.34))
    workspace.risk = assess_risk(workspace.ranking, workspace.lanes, threshold)
    workspace.captain_gate = captain_gate_decision(workspace.risk, workspace.decision_authority)

    top = workspace.ranking[0] if workspace.ranking else None
    recommendation = "No recommendation because no options were provided."
    if top:
        recommendation = f"Prioritise {top.option_name} with score {top.total_score}. {top.rationale}"

    evidence_summary = {
        "evidence_count": len(workspace.evidence),
        "average_reliability": round(sum(e.reliability for e in workspace.evidence) / max(1, len(workspace.evidence)), 4),
        "average_relevance": round(sum(e.relevance for e in workspace.evidence) / max(1, len(workspace.evidence)), 4),
    }

    pre_report = {
        "workspace": workspace.to_dict(),
        "recommendation": recommendation,
        "evidence_summary": evidence_summary,
    }
    witness_hash = witness.record("decision_report_created", pre_report)

    return DecisionReport(
        report_id=f"report-{uuid4().hex[:12]}",
        workspace_id=workspace.workspace_id,
        workflow_id=workspace.workflow_id,
        recommendation=recommendation,
        ranked_options=workspace.ranking,
        risk=workspace.risk,
        captain_gate=workspace.captain_gate,
        lane_assessments=workspace.lanes,
        evidence_summary=evidence_summary,
        witness_hash=witness_hash,
    )
