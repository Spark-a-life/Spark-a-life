import hashlib, uuid
from datetime import datetime, timezone

def create_witness(project, project_path, artefact_text, quality_report):
    return {
        "witness_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project_id": project["project"]["id"],
        "workflow_template": project["workflow"]["template"],
        "source": {"path": str(project_path), "sha256": hashlib.sha256(project_path.read_bytes()).hexdigest()},
        "artefact": {"sha256": hashlib.sha256(artefact_text.encode("utf-8")).hexdigest()},
        "quality": quality_report,
        "assumptions": [x for x in project["evidence"] if x["type"] == "assumption"],
        "human_approval_required": project["workflow"].get("require_human_approval", True)
    }

def release_status(project, quality_score):
    if quality_score < float(project["workflow"]["release_threshold"]):
        return "blocked"
    if project["workflow"].get("require_human_approval", True):
        return "review_required"
    return "approved"
