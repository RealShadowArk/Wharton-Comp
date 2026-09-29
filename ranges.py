"""Contribution ranges and funding results from M07's simulated paths.

A state is a declared 2031 starting point. Every path M07 ran from it
counts, including zero gifts and failed payments.
"""

import math

from m05.reserve import TOLERANCE
from m08.gift import facility_gift, split_2033

RANGE_METHODS = ("equal_tail", "one_sided_minimum")


def quantile(values, p):
    """The smallest modeled value with at least a share p of all values at
    or below it. Bounds are always values that actually occurred."""
    if not values:
        raise ValueError("no values")
    if not 0 <= p <= 1:
        raise ValueError(f"p must be between 0 and 1, got {p}")
    ordered = sorted(values)
    # Rounding first stops 0.07 * 100 = 7.000000000000001 from moving up
    # a whole position.
    index = max(0, math.ceil(round(p * len(ordered), 9)) - 1)
    return ordered[index]


def gift_range(gifts, method, coverage):
    """Bounds for the gift, and the share of modeled gifts that actually
    fall inside them.

    equal_tail cuts the same share off each end. one_sided_minimum gives a
    floor only, for a claim like "at least $X".
    """
    if not 0 < coverage < 1:
        raise ValueError(f"coverage must be between 0 and 1, got {coverage}")
    if method == "equal_tail":
        tail = (1 - coverage) / 2
        lower, upper = quantile(gifts, tail), quantile(gifts, 1 - tail)
    elif method == "one_sided_minimum":
        lower, upper = quantile(gifts, 1 - coverage), None
    else:
        raise ValueError(f"range method must be one of {RANGE_METHODS}")
    inside = [g for g in gifts
              if g >= lower and (upper is None or g <= upper)]
    return {
        "lower_bound": lower,
        "upper_bound": upper,
        "target_coverage": coverage,
        "achieved_coverage": len(inside) / len(gifts),
        "zero_gift_frequency":
            sum(1 for g in gifts if g <= TOLERANCE) / len(gifts),
        "n_paths": len(gifts),
    }


def payment_success_rate(paths):
    """Share of paths that funded all ten payments. Reported separately
    from the gift range; one never stands in for the other."""
    return sum(1 for p in paths if p["all_payments_success"]) / len(paths)


def check_state(paths, state_id, value_2031):
    """Every path in a state must start from the declared 2031 balance."""
    for p in paths:
        if abs(p["value_2031"] - value_2031) > 0.01:
            raise ValueError(
                f"path {p['path_id']} in state {state_id} starts at "
                f"{p['value_2031']:.2f}, not the declared {value_2031:.2f}")


def policy_outcomes(paths, share):
    """How one gift share did across a set of paths."""
    gifts = [p["facility_gift"] for p in paths]
    retained = [split_2033(p["value_2033"], p["reserve_required"],
                           share)["retained_flexibility"] for p in paths]
    mismatches = sum(
        1 for p in paths
        if abs(p["facility_gift"] - facility_gift(
            p["value_2033"], p["reserve_required"], share)) > 0.01)
    return {
        "n_paths": len(paths),
        "reserve_not_established_rate":
            sum(1 for p in paths if p["reserve_gap"] > TOLERANCE)
            / len(paths),
        "gift_mean": sum(gifts) / len(gifts),
        "gift_p10": quantile(gifts, 0.10),
        "gift_median": quantile(gifts, 0.50),
        "gift_p90": quantile(gifts, 0.90),
        "retained_median": quantile(retained, 0.50),
        "all_payments_success_rate": payment_success_rate(paths),
        "mean_total_shortfall":
            sum(p["total_nominal_shortfall"] for p in paths) / len(paths),
        "worst_single_shortfall":
            max(p["worst_single_shortfall"] for p in paths),
        # Paths where M07's gift differs from this rule. Should be zero.
        "gift_rule_mismatches": mismatches,
    }
