from wisegen_mamt_fundraising.contracts import load_brief
from wisegen_mamt_fundraising.fundraising.scoring import rank_prospects


def test_scoring_prioritises_aligned_prospect():
    brief = load_brief("examples/missions/fundraising_500k_programme.yaml")
    scores = rank_prospects(brief)
    assert scores[0].prospect_name == "Responsible Technology Foundation"
    assert scores[0].score >= brief.fundraising.minimum_fit_score
