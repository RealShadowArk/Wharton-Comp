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
              satellite_share=0.7, account_value=300_000, contribution_1=300_000,
              contribution_2=150_000):
    """The Option 3 target portfolio (WInS_Plan sheet): one target, no stages.

    Shares are set at the start of 2028, after both contributions. Under
    Option 3 the 2027 money alone is below the floor, so it is all in bonds
    and earns the bond yield. Growth = m x cushion (capped); from it come the
    sector tilts, then `satellite_share` of what is left goes to individual
    stocks and the rest to the core index fund.
    """
    portfolio = contribution_1 * (1 + bond_yield) + contribution_2
    floor_2028 = floor(2028, bond_yield, safety_margin)
    cushion = portfolio - floor_2028
    growth = stocks(portfolio, floor_2028, m, max_stock_share) / portfolio
    satellites = (growth - tilts_total) * satellite_share
    target = {"safety": 1 - growth, "tilts": tilts_total,
              "satellites": satellites,
              "core": growth - tilts_total - satellites}
    return {
        "portfolio_2028": portfolio, "floor_2028": floor_2028,
        "cushion_2028": cushion, "growth": growth, "target": target,
        "target_dollars": {k: v * account_value for k, v in target.items()},
    }
