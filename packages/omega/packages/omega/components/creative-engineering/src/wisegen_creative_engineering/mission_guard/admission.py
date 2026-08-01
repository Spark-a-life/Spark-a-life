from ..models import CreativeBrief

REGULATED_CHANNEL_TERMS = {'government','healthcare','finance','financial','education','public service'}

def admission_checks(brief: CreativeBrief) -> list[str]:
    issues: list[str] = []
    for asset in brief.assets:
        if asset.consent in {'none','public_unverified'}:
            issues.append(f"Asset {asset.id} has insufficient consent status: {asset.consent}")
    joined = f"{brief.mission.channel} {brief.mission.industry or ''}".lower()
    if any(term in joined for term in REGULATED_CHANNEL_TERMS) and not brief.risk.human_approval_required:
        issues.append('Regulated or sensitive domain requires human approval.')
    return issues

def assert_admissible(brief: CreativeBrief) -> None:
    issues = admission_checks(brief)
    if issues:
        raise ValueError('Mission not admissible: ' + '; '.join(issues))
