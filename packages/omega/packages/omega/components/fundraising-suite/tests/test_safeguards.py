from dataclasses import replace

from wisegen_mamt_fundraising.contracts import load_brief
from wisegen_mamt_fundraising.models import Claim
from wisegen_mamt_fundraising.safeguards.claims import check_claims


def test_blocked_claim_is_caught():
    brief = load_brief("examples/missions/fundraising_500k_programme.yaml")
    claim = Claim("This is a guaranteed return for funders.", [], True)
    findings = check_claims([claim], brief.evidence)
    assert any(item.status == "block" for item in findings)


def test_missing_external_evidence_blocks():
    brief = load_brief("examples/missions/fundraising_500k_programme.yaml")
    claim = replace(brief.claims[0], evidence_ids=["missing"])
    findings = check_claims([claim], brief.evidence)
    assert any("missing evidence" in item.message for item in findings)
