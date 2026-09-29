"""Facility contribution: where the 2033 portfolio goes (M08).

All amounts are nominal US dollars. The gift share is a decimal between 0
and 1 that P1 chooses; nothing here picks it.
"""

from m05.reserve import TOLERANCE, actual_reserve_transfer, reserve_gap


def check_share(share):
    if not 0 <= share <= 1:
        raise ValueError(f"gift share must be between 0 and 1, got {share}")


def facility_gift(available_2033, reserve_required, share):
    """The 2033 gift under the rule gift = share x leftover.

    Leftover is what remains after the full required reserve. The required
    reserve already includes the immediate 2033 payment, so that payment is
    not subtracted a second time. No leftover means no gift, never a
    negative one.
    """
    check_share(share)
    return share * max(0, available_2033 - reserve_required)


def split_2033(available_2033, reserve_required, share):
    """Every 2033 dollar goes to the reserve, the gift, or retained
    flexibility, in that order."""
    transfer = actual_reserve_transfer(reserve_required, available_2033)
    gap = reserve_gap(reserve_required, transfer)
    leftover = available_2033 - reserve_required
    gift = facility_gift(available_2033, reserve_required, share)
    retained = max(0, leftover) - gift
    return {
        "available_2033": available_2033,
        "reserve_required": reserve_required,
        "actual_reserve_transfer": transfer,
        "reserve_gap": gap,
        "reserve_established": gap <= TOLERANCE,
        "leftover": leftover,
        "facility_gift": gift,
        "retained_flexibility": retained,
        # The gift leaves for good. Only these stay in the portfolio.
        "assets_after_gift": transfer + retained,
    }
