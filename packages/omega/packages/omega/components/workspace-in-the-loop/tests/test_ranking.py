from wisegen_witl.core.models import Criterion, Option
from wisegen_witl.core.ranking import rank_options


def test_rank_options_orders_by_weighted_score():
    criteria = [Criterion(id="fit", name="Fit", weight=0.7), Criterion(id="risk", name="Risk", weight=0.3, direction="min")]
    options = [
        Option(id="a", name="A", description="", features={"fit": 0.8, "risk": 0.2}),
        Option(id="b", name="B", description="", features={"fit": 0.7, "risk": 0.8}),
    ]
    ranked = rank_options(options, criteria)
    assert ranked[0].option_id == "a"
    assert ranked[0].total_score > ranked[1].total_score
