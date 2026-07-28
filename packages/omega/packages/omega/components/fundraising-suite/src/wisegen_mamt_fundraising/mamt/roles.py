from __future__ import annotations

from ..models import RoleAgent


DEFAULT_ROLES = [
    RoleAgent("captain_strategist", "Owns mission intent, thesis and final decision logic", ["mission_reader", "strategy_planner", "approval_gate"], "high", "strategy and authority"),
    RoleAgent("prospect_researcher_sourcer", "Finds and qualifies prospects", ["prospect_registry", "source_capture"], "medium", "sourcing"),
    RoleAgent("enricher_intelligence_analyst", "Adds fit and relationship intelligence", ["prospect_registry", "evidence_register", "scoring_engine"], "medium", "enrichment"),
    RoleAgent("narrative_architect", "Builds evidence-grounded fundraising narrative", ["narrative_builder", "evidence_register"], "medium", "narrative"),
    RoleAgent("memo_writer", "Produces funder briefs and internal memos", ["memo_builder", "evidence_register"], "medium", "synthesis"),
    RoleAgent("financial_analyst", "Checks budget and sustainability logic", ["budget_checker", "risk_register"], "high", "financial logic"),
    RoleAgent("compliance_reviewer", "Checks eligibility, privacy, claims and restrictions", ["claim_checker", "safeguard_rules"], "high", "compliance"),
    RoleAgent("outreach_drafter", "Drafts outreach and follow-up sequences", ["outreach_builder", "evidence_register"], "high", "external communication"),
    RoleAgent("data_room_curator", "Organises due diligence evidence", ["data_room_manifest", "evidence_register"], "high", "evidence operations"),
    RoleAgent("tracker_crm_steward", "Maintains pipeline status and next actions", ["pipeline_tracker"], "medium", "operations"),
    RoleAgent("creative_director", "Creates channel creative and visual prompt packs", ["creative_pack", "brand_rules"], "medium", "creative engineering"),
    RoleAgent("safeguard_governor", "Enforces runtime and egress boundaries", ["runtime_governor", "circuit_breaker", "credential_broker"], "high", "safeguards"),
    RoleAgent("evidence_librarian", "Maintains claim-source traceability", ["evidence_register", "witness_chain"], "high", "evidence integrity"),
    RoleAgent("qa_evaluator", "Scores outputs against rubrics", ["rubric_evaluator", "approval_gate"], "medium", "evaluation"),
]
