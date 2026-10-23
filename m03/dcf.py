"""M03 company valuation: free cash flow to the firm (FCFF) discounted at WACC.

Spec (P3 role PDF, see CLAUDE.md):
- FCFF = EBIT(1 - t) + D&A - capex - change in net working capital.
- Discount with WACC, never an equity rate.
- TV_N = FCFF_{N+1} / (WACC - g); WACC must exceed g, otherwise an error.
- Equity = EV + non-operating assets - debt and senior claims, divided by
  diluted shares.
- Sensitivities: discount rate, terminal growth and one operating driver.

All amounts are nominal US dollars in millions unless stated; rates are
decimals. A valuation is a research estimate, never an annual return,
a price target or a position size.
"""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Inputs:
    base_revenue: float          # last reported fiscal year
    growth: tuple                # revenue growth for each forecast year
    ebit_margin: tuple           # EBIT / revenue for each forecast year
    tax_rate: float
    da_pct: tuple                # D&A / revenue for each forecast year
    capex_pct: tuple             # capex / revenue for each forecast year
    nwc_pct_of_change: float     # change in NWC / change in revenue
    wacc: float
    terminal_growth: float
    debt: float                  # debt and senior claims
    non_operating_assets: float  # cash and other non-operating assets
    diluted_shares: float        # millions
    years_to_first_cash_flow: float = 1.0  # discount time of forecast year 1

    def __post_init__(self):
        n = len(self.growth)
        for name in ("ebit_margin", "da_pct", "capex_pct"):
            if len(getattr(self, name)) != n:
                raise ValueError(f"{name} needs {n} values, one per forecast year")


def wacc(risk_free, beta, equity_premium, pre_tax_cost_of_debt, tax_rate,
         equity_value, debt_value):
    """Weighted average cost of capital from CAPM and market-value weights."""
    cost_of_equity = risk_free + beta * equity_premium
    weight_debt = debt_value / (equity_value + debt_value)
    return ((1 - weight_debt) * cost_of_equity
            + weight_debt * pre_tax_cost_of_debt * (1 - tax_rate))


def forecast(p):
    """Year-by-year rows: revenue, EBIT, NOPAT, D&A, capex, change in NWC, FCFF."""
    rows, revenue = [], p.base_revenue
    for k, g in enumerate(p.growth):
        new_revenue = revenue * (1 + g)
        ebit = new_revenue * p.ebit_margin[k]
        nopat = ebit * (1 - p.tax_rate)
        da = new_revenue * p.da_pct[k]
        capex = new_revenue * p.capex_pct[k]
        d_nwc = (new_revenue - revenue) * p.nwc_pct_of_change
        rows.append({"year": k + 1, "revenue": new_revenue, "ebit": ebit,
                     "nopat": nopat, "da": da, "capex": capex, "d_nwc": d_nwc,
                     "fcff": nopat + da - capex - d_nwc})
        revenue = new_revenue
    return rows


def terminal_value(fcff_next, wacc_rate, g):
    """Gordon growth value at the end of the forecast."""
    if wacc_rate <= g:
        raise ValueError(f"WACC ({wacc_rate:.4f}) must exceed terminal growth ({g:.4f})")
    return fcff_next / (wacc_rate - g)


def value(p):
    """Enterprise value, equity value and value per diluted share."""
    rows = forecast(p)
    last = rows[-1]
    # Year N+1: revenue grows at g; margins and ratios stay at year-N levels.
    rev_next = last["revenue"] * (1 + p.terminal_growth)
    fcff_next = (rev_next * p.ebit_margin[-1] * (1 - p.tax_rate)
                 + rev_next * (p.da_pct[-1] - p.capex_pct[-1])
                 - (rev_next - last["revenue"]) * p.nwc_pct_of_change)
    tv = terminal_value(fcff_next, p.wacc, p.terminal_growth)
    pv = 0.0
    for r in rows:
        t = p.years_to_first_cash_flow + r["year"] - 1
        r["discount_factor"] = (1 + p.wacc) ** -t
        r["pv_fcff"] = r["fcff"] * r["discount_factor"]
        pv += r["pv_fcff"]
    pv_tv = tv * rows[-1]["discount_factor"]
    ev = pv + pv_tv
    equity = ev + p.non_operating_assets - p.debt
    return {"rows": rows, "fcff_next": fcff_next, "terminal_value": tv,
            "pv_forecast": pv, "pv_terminal": pv_tv, "ev": ev,
            "terminal_share_of_ev": pv_tv / ev, "equity": equity,
            "per_share": equity / p.diluted_shares}


def sensitivity(p, field, values):
    """Value per share as one input changes; NOT DEFINED when WACC <= g."""
    out = {}
    for v in values:
        if field in ("growth", "ebit_margin"):
            base = getattr(p, field)
            shifted = tuple(x + v for x in base)
            q = replace(p, **{field: shifted})
        else:
            q = replace(p, **{field: v})
        try:
            out[v] = value(q)["per_share"]
        except ValueError:
            out[v] = None
    return out


def grid(p, field_a, values_a, field_b, values_b):
    """Two-way table of value per share (rows field_a, columns field_b)."""
    return {a: sensitivity(replace(p, **{field_a: a}), field_b, values_b)
            for a in values_a}


def implied_growth_shift(p, price, lo=-0.5, hi=0.5, tol=1e-6):
    """Parallel shift to every forecast-year growth rate that makes the value
    per share equal the market price (a reverse DCF). None if no solution."""
    def gap(shift):
        q = replace(p, growth=tuple(g + shift for g in p.growth))
        return value(q)["per_share"] - price
    if gap(lo) > 0 or gap(hi) < 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if gap(mid) > 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2
