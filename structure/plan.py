"""Option 3 (floor rule) and the WInS plan from the structure model.

A Python port of Laura_Gao_Portfolio_Structure_Model_v4.xlsx: sheets Inputs
(rows 38-44), Step5_Scenarios and WInS_Plan. All amounts are nominal US
dollars; rates are decimals.

Option 3: every year, stocks = m x cushion (capped at a maximum share of
wealth), where cushion = wealth - floor and the floor is the cost of bonds
that cover all ten payments. Everything else is in bonds earning the
locked-in bond yield.
"""

from m05.reserve import FIRST_PAYMENT_YEAR, required_reserve

FIRST_YEAR = 2027
CONTRIBUTIONS = {2027: 300_000, 2028: 150_000}


def reserve_with_margin(bond_yield, safety_margin):
    """Reserve needed at the start of 2033 (Inputs!B44): the present value
    of the ten payments at the bond yield, plus the safety margin."""
    return required_reserve(bond_yield) * (1 + safety_margin)


def floor(year, bond_yield, safety_margin):
    """Dollars that, invested at the bond yield from the start of `year`,
    grow into the 2033 reserve (Inputs row 40)."""
    return (reserve_with_margin(bond_yield, safety_margin)
            / (1 + bond_yield) ** (FIRST_PAYMENT_YEAR - year))


def stocks(wealth, floor_value, m, max_stock_share):
    """Option 3's stock holding: m x cushion, capped, never below zero."""
    return min(m * max(0.0, wealth - floor_value), max_stock_share * wealth)


def scenario_path(returns, bond_yield, safety_margin, m, max_stock_share,
                  contributions=CONTRIBUTIONS):
    """Wealth at the start of each year 2027-2033 under Option 3, for one
    stock-return path (one return per year, 2027-2032). Matches a row of
    Step5_Scenarios, columns I-O."""
    wealth = [contributions.get(FIRST_YEAR, 0)]
    for k, ret in enumerate(returns):
        year = FIRST_YEAR + k
        w = wealth[-1]
        s = stocks(w, floor(year, bond_yield, safety_margin), m,
                   max_stock_share)
        wealth.append(s * (1 + ret) + (w - s) * (1 + bond_yield)
                      + contributions.get(year + 1, 0))
    return wealth


def wins_plan(bond_yield, safety_margin, m, max_stock_share, tilts_total,
              m_lowest=1, account_value=300_000, contribution_1=300_000,
              contribution_2=150_000):
    """Stage 1 and Stage 2 shares and amounts (WInS_Plan sheet).

    Shares are set at the start of 2028, after both contributions. Under
    Option 3 the 2027 money alone is below the floor, so it is all in bonds
    and earns the bond yield. Stage 1 holds what every m from `m_lowest` up
    to the chosen `m` agrees on: the bond share the chosen m needs and the
    stock share the lowest m holds; the rest waits in T-bills. Stage 2 is
    the full target at the chosen m.
    """
    portfolio = contribution_1 * (1 + bond_yield) + contribution_2
    floor_2028 = floor(2028, bond_yield, safety_margin)
    cushion = portfolio - floor_2028

    def growth(mult):
        return stocks(portfolio, floor_2028, mult, max_stock_share) / portfolio

    g_low, g_target = growth(m_lowest), growth(m)
    stage1 = {"safety": min(1 - g_low, 1 - g_target),
              "growth_core": min(g_low, g_target)}
    stage1["parked"] = 1 - stage1["safety"] - stage1["growth_core"]
    stage2 = {"safety": 1 - g_target, "growth_core": g_target - tilts_total,
              "tilts": tilts_total}

    def dollars(shares):
        return {k: v * account_value for k, v in shares.items()}

    return {
        "portfolio_2028": portfolio, "floor_2028": floor_2028,
        "cushion_2028": cushion, "growth_lowest_m": g_low,
        "growth_target": g_target,
        "stage1": stage1, "stage1_dollars": dollars(stage1),
        "stage2": stage2, "stage2_dollars": dollars(stage2),
    }
