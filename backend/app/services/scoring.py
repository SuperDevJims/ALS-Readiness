def compute_mps(total_score: int, item_count: int) -> float | None:
    """Mean Percentage Score of one attempt: the share of items answered
    correctly, as a percentage to two decimal places. None when the attempt
    has no items, since there is nothing to take a share of.

    The only place the formula is written. The learner's own result and the
    facilitator's views both call it, so they cannot disagree.
    """
    if item_count == 0:
        return None

    return round(total_score / item_count * 100, 2)
