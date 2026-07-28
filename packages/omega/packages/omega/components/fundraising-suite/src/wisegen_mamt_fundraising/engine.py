from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from .adapters.local_deterministic import LocalDeterministicAdapter
from .adapters.manual_bridge import ManualBridgeAdapter
from .audit.witness_chain import WitnessChain
from .contracts import load_brief
from .creative.narrative import funder_memo, strategic_narrative
from .creative.outreach import email_draft, linkedin_draft, visual_prompt_pack
from .evaluation.rubric import evaluate
from .fundraising.data_room import data_room_checklist, evidence_manifest
from .fundraising.donor_due_diligence import review_due_diligence
from .fundraising.financials import funding_gap_analysis
from .fundraising.scoring import rank_prospects
from .io import write_json
from .mamt.mission_team import MissionTeam
from .mission_guard.approval_gate import captain_gate
from .models import AdapterResult, MissionBrief
from .router import ModelRouter
from .runtime_governor.governor import RuntimeGovernor
from .safeguards.review import safeguard_review


def _adapter_for(name: str):
    if name == "local_deterministic":
        return LocalDeterministicAdapter()
    if name == "manual_bridge":
        return ManualBridgeAdapter()
    raise ValueError(f"Unsupported adapter: {name}")


def build_artefacts(brief: MissionBrief) -> dict[str, Any]:
    scores = rank_prospects(brief)
    due_diligence = review_due_diligence(brief)
    qualified = [item for item in scores if item.score >= brief.fundraising.minimum_fit_score]
    qualified_amount = sum(
        prospect.estimated_amount
        for prospect in brief.prospects
        if prospect.name in {item.prospect_name for item in qualified}
    )
    memos = [funder_memo(brief, item) for item in qualified[:5]]
    outreach = [email_draft(brief, item) for item in qualified[:3]]
    route_decisions = _routing_summary()
    return {
        "strategy": strategic_narrative(brief),
        "governance_profile": asdict(brief.governance),
        "prospect_scores": [asdict(item) for item in scores],
        "donor_due_diligence": [asdict(item) for item in due_diligence],
        "shortlist": [item.prospect_name for item in qualified],
        "funder_memos": memos,
        "outreach_drafts": outreach,
        "linkedin_draft": linkedin_draft(brief),
        "visual_prompt_pack": visual_prompt_pack(brief),
        "financials": funding_gap_analysis(brief, qualified_amount),
        "data_room": data_room_checklist(brief),
        "evidence_manifest": evidence_manifest(brief),
        "pipeline_tracker": _pipeline_tracker(brief, scores),
        "model_routing": [asdict(item) for item in route_decisions],
        "egress_policy": _egress_policy(brief),
    }


def _pipeline_tracker(brief: MissionBrief, scores) -> list[dict[str, Any]]:
    rows = []
    for score in scores:
        prospect = next(item for item in brief.prospects if item.name == score.prospect_name)
        requires_compliance = bool(prospect.restrictions) or score.recommended_stage == "qualified"
        rows.append(
            {
                "prospect_name": prospect.name,
                "stage": score.recommended_stage,
                "fit_score": score.score,
                "estimated_amount": prospect.estimated_amount,
                "source": prospect.source,
                "next_action": "Prepare memo" if score.recommended_stage == "qualified" else "Continue research",
                "owner": "tracker_crm_steward",
                "approval_status": "not_sent",
                "compliance_review_required": requires_compliance,
                "data_room_release_allowed": False,
            }
        )
    return rows


def _routing_summary():
    router = ModelRouter()
    return router.route_table(
        [
            "strategy",
            "sourcing",
            "enrichment",
            "narrative",
            "compliance",
            "finance",
            "evidence",
            "tracker",
            "creative",
            "audit",
            "red_team",
        ]
    )


def _egress_policy(brief: MissionBrief) -> dict[str, Any]:
    return {
        "channels": list(brief.governance.egress_channels),
        "human_approval_required": brief.risk.human_approval_required,
        "release_rule": "All external egress requires Captain Gate approval and channel-specific compliance review.",
        "blocked_until_approved": [
            channel for channel in brief.governance.egress_channels if channel in {"email", "linkedin", "deck", "data_room", "crm"}
        ],
    }


def run_mission(
    mission_path: str | Path,
    output_path: str | Path,
    audit_path: str | Path = "outputs/witness_chain.jsonl",
) -> dict[str, Any]:
    brief = load_brief(mission_path)
    chain = WitnessChain(audit_path)
    chain.append("mission_loaded", {"mission_id": brief.mission.id, "source": str(mission_path)})

    team = MissionTeam().compile(brief)
    chain.append("mamt_team_compiled", {"roles": [package.role for package in team]})

    governor = RuntimeGovernor(brief.risk)
    compliance_findings = safeguard_review(brief)
    chain.append("safeguard_review_complete", {"findings": [asdict(item) for item in compliance_findings]})

    artefacts = build_artefacts(brief)
    chain.append(
        "artefacts_built",
        {
            "sections": sorted(artefacts.keys()),
            "qualified_prospects": artefacts["shortlist"],
            "egress_channels": brief.governance.egress_channels,
        },
    )

    adapter = _adapter_for(brief.output.adapter)
    adapter_result: AdapterResult = adapter.execute(brief, artefacts)
    state = governor.record(adapter_result.usage)
    chain.append("adapter_execution_complete", {"adapter": adapter.name, "circuit_state": state.value})

    scores = rank_prospects(brief)
    due_diligence = review_due_diligence(brief)
    evaluation = evaluate(brief, adapter_result, scores, compliance_findings)
    gate = captain_gate(brief, evaluation, compliance_findings)
    chain.append("captain_gate_decision", asdict(gate))

    payload = {
        "mission_id": brief.mission.id,
        "version": "1.5.0",
        "team": [asdict(package) for package in team],
        "compliance_findings": [asdict(item) for item in compliance_findings],
        "donor_due_diligence": [asdict(item) for item in due_diligence],
        "adapter_result": asdict(adapter_result),
        "evaluation": asdict(evaluation),
        "captain_gate": asdict(gate),
        "runtime_status": asdict(governor.status()),
        "audit_path": str(audit_path),
    }
    write_json(output_path, payload)
    return payload
