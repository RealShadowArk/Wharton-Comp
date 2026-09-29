"""WInS plan: the Stage 1 and Stage 2 shares from the structure model.

A Python port of Laura_Gao_Portfolio_Structure_Model_v1.xlsx, sheets Inputs
(rows 38-45) and WInS_Plan. All amounts are nominal US dollars; rates are
decimals. Target shares are set at the start of 2028, after both
contributions, and then applied to the WInS account.
"""

from m05.reserve import FIRST_PAYMENT_YEAR, required_reserve

GLIDE_START, GLIDE_END = 2027, 2032
OPTIONS = ("Option 1", "Option 2", "Option 3")


def reserve_with_margin(bond_yield, safety_margin):
    """Reserve needed at the start of 2033 (Inputs!B44): the present value
    of the ten payments at the bond yield, plus the safety margin."""
    return required_reserve(bond_yield) * (1 + safety_margin)


def floor(year, bond_yield, safety_margin):
    """Dollars that, invested at the bond yield from the start of `year`,
    grow into the 2033 reserve (Inputs row 40)."""
    return (reserve_with_margin(bond_yield, safety_margin)
            / (1 + bond_yield) ** (FIRST_PAYMENT_YEAR - year))


def glide_share(year, share_2027, share_2032):
    """Option 2's stock share, in a straight line from 2027 to 2032
    (Inputs row 41)."""
    return share_2027 + (share_2032 - share_2027) * (
        (year - GLIDE_START) / (GLIDE_END - GLIDE_START))


def wins_plan(bond_yield, safety_margin, m, max_stock_share,
              glide_2027, glide_2032, tilts_total, option="Option 3",
              account_value=300_000, contribution_1=300_000,
              contribution_2=150_000):
    """Stage 1 and Stage 2 shares and amounts (WInS_Plan sheet).

    The 2028 portfolio assumes a neutral 2027: everything earns the bond
    yield for one year. Stage 1 takes the smallest safety share and the
    smallest growth share across the three options, so every option agrees
    with it; the rest is parked in T-bills until Stage 2.
    """
    portfolio = contribution_1 * (1 + bond_yield) + contribution_2
    floor_2028 = floor(2028, bond_yield, safety_margin)
    cushion = portfolio - floor_2028

    growth = {
        "Option 1": cushion / portfolio,
        "Option 2": glide_share(2028, glide_2027, glide_2032),
        "Option 3": min(m * cushion, max_stock_share * portfolio) / portfolio,
    }
    safety = {k: 1 - v for k, v in growth.items()}

    stage1_safety = min(safety.values())
    stage1_growth = min(growth.values())
    stage1 = {"safety": stage1_safety, "growth_core": stage1_growth,
              "parked": 1 - stage1_safety - stage1_growth}

    stage2 = {"safety": safety[option],
              "growth_core": growth[option] - tilts_total,
              "tilts": tilts_total}

    def dollars(shares):
        return {k: v * account_value for k, v in shares.items()}

    return {
        "portfolio_2028": portfolio, "floor_2028": floor_2028,
        "cushion_2028": cushion, "growth_by_option": growth,
        "stage1": stage1, "stage1_dollars": dollars(stage1),
        "stage2": stage2, "stage2_dollars": dollars(stage2),
    }
