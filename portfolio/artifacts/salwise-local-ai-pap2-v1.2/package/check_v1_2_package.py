#!/usr/bin/env python3
"""Check this document package, not a model, device, policy or deployment."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
def main():
    source = json.loads((ROOT / "Salwise_30_Attribute_Source_Extract_v1.2.json").read_text())
    profile = json.loads((ROOT / "Salwise_Local_AI_30_Attribute_Profile_v1.2.json").read_text())
    priorities = json.loads((ROOT / "Salwise_Local_AI_Quality_Crosswalk_v1.2.json").read_text())
    scenarios = json.loads((ROOT / "Salwise_Local_AI_Review_Scenarios_v1.2.json").read_text())
    fixture = json.loads((ROOT / "fixtures/enq001_input.json").read_text())
    oracle = json.loads((ROOT / "references/enq001_frozen_reference.json").read_text())
    path = ROOT / "Salwise_Local_AI_Productivity_PaP2_v1.2.md"
    prompt = path.read_text()
    checks = []
    def check(name, result):
        checks.append({"check": name, "result": "PASS" if result else "FAIL",
                       "scope": "Package structure and declared content only"})
    entries = profile["entries"]
    ids = [x["attribute_id"] for x in entries]
    check("Exactly 30 non-empty source-mapped entries", len(ids) == 30 and len(source) == 30)
    check("Unique IDs retain SAL-Q01 to SAL-Q30",
          ids == [f"SAL-Q{i:02d}" for i in range(1, 31)] and len(set(ids)) == 30)
    check("Original IDs names clusters checks evidence and statuses preserved",
          len(entries) == len(source) and all(all(x[k] == y[k] for k in y)
                                             for x, y in zip(entries, source)))
    clusters = set(x["cluster"] for x in source)
    check("Five source clusters with six entries each",
          len(clusters) == 5 and all(sum(x["cluster"] == c for x in source) == 6 for c in clusters))
    check("No runtime pass or invented result references",
          all(x["local_runtime_status"] == "NOT_ASSESSED" and x["actual_result_ref"] is None
              and x["system_wide_evidence_transfer"] is False for x in entries))
    check("Milestone and applicability fields valid",
          all(x["local_first_required_at"] in profile["milestones"]
              and x["local_applicability"] in {"IN_SCOPE", "PARTIAL_SCOPE", "DEFERRED"} for x in entries))
    check("Eight source overlays retained without corporate-gate import",
          len(profile["overlays"]) == 8
          and all(x["source_corporate_gates_not_imported"] is True for x in profile["overlays"]))
    check("All 15 requested priorities mapped to known standards",
          len(priorities["priorities"]) == 15
          and all(x["related_standard_ids"] and set(x["related_standard_ids"]) <= set(ids)
                  and x["runtime_status"] == "NOT_ASSESSED" for x in priorities["priorities"]))
    check("Prompt includes every assurance ID as a matrix row",
          re.findall(r"^\| (SAL-Q\d{2}) \|", prompt, re.M) == ids)
    check("Goal journey frozen task and stopping conditions explicit",
          all(x in prompt for x in ["### /goal", "### /journey", "ENQ-001",
                                   "M2 is complete", "first relevant milestone"]))
    check("Orchestrator and local task context explicitly separated",
          "Keep this orchestration brief and its assurance annexes with Codex" in prompt)
    check("18 desk-review cases explicitly not agent executions",
          len(scenarios["cases"]) == 18
          and all(x["agent_execution_result"] == "NOT_RUN" for x in scenarios["cases"]))
    check("All scenario standard IDs resolve",
          all(set(x["standards"]) <= set(ids) for x in scenarios["cases"]))
    check("Seven SaaP moves retained as adaptive reasoning checks",
          all(f"| {x} |" in prompt for x in ["Understand", "Organise", "Explore", "Challenge", "Make sense", "Recommend", "Act"])
          and "not mandatory headings" in prompt and "single most important clarifying question" in prompt)
    check("Starter task is distinguished from demonstrated user need",
          "not evidence that enquiries are Will's largest productivity bottleneck" in prompt)
    check("Fictional input and frozen reference identities and core facts agree",
          fixture["fixture_id"] == oracle["fixture_id"] == "ENQ-001"
          and fixture["data_class"] == "FICTIONAL"
          and oracle["known"]["duration_hours"] == 3.5 and oracle["known"]["participants"] == 20
          and len(oracle["constraints"]) == 6 and len(oracle["missing_information"]) == 5
          and all(v is None for v in oracle["missing_information"].values())
          and oracle["model_execution"] == "NOT_RUN")
    task = (ROOT / "Salwise_Local_Model_Task_ENQ001_v1.2.md").read_text()
    check("Minimal local task contains the exact fictional source and no policy annex",
          fixture["source_text"] in task and fixture["source_text"] in prompt
          and len(task.split()) < 500 and "SAL-Q30" not in task)
    check("No prohibited em dash in v1.2 Markdown files",
          all("\u2014" not in p.read_text() for p in ROOT.glob("*v1.2.md")))
    report = {"profile_version": "1.2", "check_type": "MECHANICAL_DOCUMENT_CONSISTENCY",
              "candidate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "checks": checks, "passed": sum(x["result"] == "PASS" for x in checks),
              "total": len(checks), "runtime_integration": "NOT_RUN",
              "model_behaviour": "NOT_RUN", "human_productivity": "NOT_MEASURED",
              "independent_assurance": "NOT_ESTABLISHED"}
    (ROOT / "Salwise_Local_AI_v1.2_Checks.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if checks and all(x["result"] == "PASS" for x in checks) else 1

if __name__ == "__main__":
    raise SystemExit(main())

