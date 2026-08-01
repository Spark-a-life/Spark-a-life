from wisegen_omega.advisers import independent_reviews, cross_examine

def test_full_council():
 r=independent_reviews({"objective":"test"}); assert len(r)==8; assert len({x.adviser for x in r})==8; assert cross_examine(r)["review_count"]==8
