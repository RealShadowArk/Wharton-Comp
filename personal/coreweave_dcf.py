"""CoreWeave capacity DCF (personal, not for the Wharton competition; 23 Nov 2026).

    python personal/coreweave_dcf.py    # writes personal/coreweave_valuation_2026-11-23.md

Why not the standard Round 2 method: it holds 2025's capex/revenue (201%) for ten years. Here capex follows
the capacity the revenue path needs:
  capacity needed at end of year t = revenue in t+1 / r          (r = revenue per $ of gross capacity, one-year lag)
  capex_t = capacity needed - capacity still in service          (vintages retire after L years)
  FCFF_t  = EBITDA_t - 21% tax on positive EBIT - capex_t        (EBIT = EBITDA - straight-line D&A over L years)
Balance sheet at 30 Sep 2026; cash flows from Q4 2026; WACC 12% to 2031, fading to 9.5% by 2036; terminal
growth 3% on FCFF after the fleet reaches a steady state (2043). Tax losses carried forward are ignored (conservative).
Sources (RESEARCH): Yahoo quarterly statements; Q3 2026 10-Q lease note; Q3 2026 results (guidance, backlog);
consensus 2027 (Twelve Data). Scenario inputs are my assumptions (ASSUMPTION), for Pat to change.
"""
from pathlib import Path

DEBT = 46.873          # $bn, 30 Sep 2026: current 10.572 + long-term 36.301 (Yahoo; results: "almost $47bn")
FIN_LEASES = 0.649     # $bn, 10-Q lease note; operating leases 18.697 excluded (rent is inside EBITDA)
CASH = 4.184           # $bn, cash and short-term investments (restricted 1.405 excluded)
SHARES = 554.0         # m, 30 Sep 2026 (dilution from options/RSUs MISSING)
PRICE = 49.06          # $, Yahoo 23 Nov 2026
TAX, G, Y0 = 0.21, 0.03, 0.10   # tax, terminal growth, years from 23 Nov to 31 Dec 2026
REV_2026, REV_Q4 = 13.15, 13.15 - 8.314   # 2026 guidance midpoint 13.0-13.3; Q1-Q3 actual 8.314
CAPEX_Q4 = 38.0 - 30.65                   # 2026 capex guidance midpoint 37-39 less 30.65 to September
# Gross capacity by vintage ($bn, Yahoo gross PP&E): to 2023 4.06, 2024 +11.41, 2025 +26.70, 2026 to Sep +41.31, plus Q4 capex
VINTAGES = {2023: 4.063, 2024: 11.407, 2025: 26.702, 2026: 83.476 - 42.172 + CAPEX_Q4}
LAST = 2042

SCEN = {
    "Bear": dict(rev27=22.50, growth=[0.10, 0.05], fade_to=2030, r=(0.29, 0.29), ebitda=(0.58, 0.50, 2030), life=5,
                 story="2027 at the low analyst estimate; little new business beyond the backlog; renewals at lower GPU prices; GPUs last 5 years"),
    "Base": dict(rev27=26.36, growth=[0.35, 0.20, 0.12], fade_to=2035, r=(0.29, 0.34), ebitda=(0.58, 0.60, 2029), life=7,
                 story="2027 consensus; growth slows to 3% by 2035; capacity turns improve as construction finishes; 6-year GPUs plus longer-lived power and cooling"),
    "Bull": dict(rev27=31.03, growth=[0.45, 0.30, 0.20], fade_to=2035, r=(0.29, 0.40), ebitda=(0.58, 0.65, 2029), life=8,
                 story="2027 at the high estimate; strong renewals and pricing; scale lifts margins; longer useful lives"),
}


def path(start, end, y0, y1, year):
    """Linear from start (year y0) to end (year y1), flat after."""
    return end if year >= y1 else start + (end - start) * (year - y0) / (y1 - y0)


def revenue(s):
    rev, g_last = {2026: REV_2026, 2027: s["rev27"]}, None
    y = 2028
    for g in s["growth"]:
        rev[y] = rev[y - 1] * (1 + g)
        g_last, y = g, y + 1
    first_fade = y
    while y <= LAST + 2:
        g = path(g_last, G, first_fade - 1, s["fade_to"], y) if y <= s["fade_to"] else G
        rev[y] = rev[y - 1] * (1 + g)
        y += 1
    return rev


def wacc(year):
    return 0.12 if year <= 2031 else path(0.12, 0.095, 2031, 2036, year)


def value(s, r_end=None, life=None, wacc_shift=0.0, wacc_const=None):
    W = (lambda y: wacc_const) if wacc_const is not None else (lambda y: wacc(y) + wacc_shift)  # a fixed rate (e.g. from a beta) or the path
    r0, r1 = s["r"]
    r1 = r_end if r_end is not None else r1
    L = life or s["life"]
    e0, e1, ey = s["ebitda"]
    rev = revenue(s)
    vint = dict(VINTAGES)
    r = lambda y: path(r0, r1, 2027, 2031, y)
    # Q4 2026 stub: Q3 2026 EBIT was about zero, so no tax
    pv, df, rows = (REV_Q4 * e0 - CAPEX_Q4) / (1 + W(2026)) ** Y0, (1 + W(2026)) ** Y0, []
    # equipment from one year retires in thirds at ages L-1, L and L+1, so one big purchase year does not echo as one lump
    alive_share = lambda age: 1.0 if age < L - 1 else (2 / 3 if age == L - 1 else (1 / 3 if age == L else 0.0))
    for t in range(2027, LAST + 1):
        alive = sum(c * alive_share(t - y) for y, c in vint.items())
        capex = max(0.0, rev[t + 1] / r(t + 1) - alive)
        da = sum(c / L for y, c in vint.items() if y < t <= y + L)
        vint[t] = capex
        ebitda = rev[t] * path(e0, e1, 2026, ey, t)
        ebit = ebitda - da
        fcff = ebitda - TAX * max(ebit, 0.0) - capex
        df *= 1 + W(t)
        pv += fcff / df
        rows.append((t, rev[t], ebitda / rev[t], ebit / rev[t], capex, fcff))
    # terminal: a fleet growing steadily at G (capex grows at G, so capacity = capex x sum of (1+G)^-k over its life)
    t, R = LAST + 1, rev[LAST + 1]
    K = R * (1 + G) / r1                                    # capacity needed at the end of the terminal year
    life_sum = sum((1 + G) ** -k * (1.0 if k < L - 1 else (2 / 3 if k == L - 1 else 1 / 3)) for k in range(L + 1))
    capex = K / life_sum
    da = capex / (1 + G) * sum((1 + G) ** -k for k in range(L)) / L
    ebitda = R * e1
    fcff = ebitda - TAX * max(ebitda - da, 0.0) - capex
    pv_tv = fcff / (W(t) - G) / df
    ev = pv + pv_tv
    eq = ev - DEBT - FIN_LEASES + CASH
    return dict(ev=ev, pv_tv=pv_tv, eq=eq, ps=eq * 1000 / SHARES, rows=rows, rev=rev)


def solve_r(s, target_ps):
    lo, hi = 0.2, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if value(s, r_end=mid)["ps"] < target_ps else (lo, mid)
    return (lo + hi) / 2


def main():
    implied_ev = PRICE * SHARES / 1000 + DEBT + FIN_LEASES - CASH
    L = ["# CoreWeave: capacity DCF (personal, 23 Nov 2026)", "",
         "Not for the Wharton competition. Generated by `python personal/coreweave_dcf.py`; method in the script's docstring. "
         "All figures in $bn unless stated. Scenario inputs are assumptions; the numbers are not a forecast.", "",
         f"**Price ${PRICE:.2f}** x {SHARES:.0f}m shares = ${PRICE * SHARES / 1000:.1f}bn equity; plus debt {DEBT:.1f}, finance leases {FIN_LEASES:.2f}, "
         f"less cash {CASH:.1f} = **enterprise value ${implied_ev:.1f}bn** implied by the market.", "",
         "## Scenarios", "", "| | Value / share | Equity | Enterprise value | Terminal value share of EV | Story |", "|---|---|---|---|---|---|"]
    res = {k: value(s) for k, s in SCEN.items()}
    for k, s in SCEN.items():
        v = res[k]
        L.append(f"| **{k}** | **${v['ps']:,.0f}** | {v['eq']:,.1f} | {v['ev']:,.1f} | {v['pv_tv'] / v['ev']:.0%} | {s['story']} |" if v["ev"] > 0 else
                 f"| **{k}** | **${v['ps']:,.0f}** | {v['eq']:,.1f} | {v['ev']:,.1f} | n/a | {s['story']} |")
    L += ["", "A negative equity value means the operating business is worth less than the debt: the shares would then be an option on a better outcome, worth something only because shareholders' losses stop at zero.", "",
          "| Input | Bear | Base | Bull |", "|---|---|---|---|",
          "| 2027 revenue | " + " | ".join(f"{s['rev27']:.1f}" for s in SCEN.values()) + " |",
          "| 2030 / 2035 revenue | " + " | ".join(f"{res[k]['rev'][2030]:.1f} / {res[k]['rev'][2035]:.1f}" for k in SCEN) + " |",
          "| Revenue per $ of capacity (r), 2027 to 2031 | " + " | ".join(f"{s['r'][0]:.2f} to {s['r'][1]:.2f}" for s in SCEN.values()) + " |",
          "| EBITDA margin (after rent and stock pay) | " + " | ".join(f"{s['ebitda'][0]:.0%} to {s['ebitda'][1]:.0%} by {s['ebitda'][2]}" for s in SCEN.values()) + " |",
          "| Equipment life (years) | " + " | ".join(str(s["life"]) for s in SCEN.values()) + " |", "",
          "## Base case by year", "", "| Year | Revenue | EBITDA margin | EBIT margin | Capex | FCFF |", "|---|---|---|---|---|---|"]
    for t, rv, em, eb, cx, f in res["Base"]["rows"]:
        if t <= 2036 or t == LAST:
            L.append(f"| {t} | {rv:,.1f} | {em:.0%} | {eb:.0%} | {cx:,.1f} | {f:,.1f} |")
    base = SCEN["Base"]
    L += ["", "## What moves the value (base case, $ per share)", "",
          "Revenue per $ of capacity by 2031 (rows) against equipment life (columns):", "",
          "| r by 2031 | " + " | ".join(f"{l} years" for l in (5, 6, 7, 8)) + " |", "|---|---|---|---|---|"]
    for rr in (0.30, 0.34, 0.38, 0.42, 0.46):
        L.append(f"| {rr:.2f} | " + " | ".join(f"${value(base, r_end=rr, life=l)['ps']:,.0f}" for l in (5, 6, 7, 8)) + " |")
    L += ["", "| WACC | " + " | ".join(f"{d:+.0%}" for d in (-0.01, 0.0, 0.01)) + " |", "|---|---|---|---|",
          "| Base value / share | " + " | ".join(f"${value(base, wacc_shift=d)['ps']:,.0f}" for d in (-0.01, 0.0, 0.01)) + " |", "",
          f"**Reverse:** with everything else at the base case, today's price needs revenue per $ of capacity to reach "
          f"**{solve_r(base, PRICE):.2f}** by 2031 (base 0.34; 2025-27 has run at 0.29-0.33).", "",
          f"**Another way to read the price:** if the bear and base cases are worth nothing to shareholders (their equity value is at or below zero), "
          f"${PRICE:.2f} is {PRICE / res['Bull']['ps']:.0%} of the bull value: the market is paying for roughly that chance of the bull case. That is arithmetic, not a probability estimate.", "",
          "## How r is measured", "",
          "r = revenue in a year / gross PP&E at the end of the year before (Yahoo):", "",
          "| Year | Revenue | Gross PP&E at the end of the year before | r |", "|---|---|---|---|",
          "| 2025 | 5.13 | 15.47 | 0.33 |",
          "| 2026 | 13.15 | 42.17 | 0.31 |",
          f"| 2027 | 26.36 (consensus) | {sum(VINTAGES.values()):.1f} (incl. Q4 capex guidance) | 0.29 |", "",
          "Gross PP&E includes construction still in progress. As building slows, r should rise; how far is the key judgment. "
          "Industry rules of thumb for rented GPUs (about $2 an hour, $45k all-in cost per GPU) also give about 0.33.", "",
          "## Caveats", "",
          "- **Leverage:** equity is a thin slice. Debt of about $47bn means a 10% change in enterprise value moves the share value by about $7-8.",
          "- **Customers:** heavy concentration in Microsoft, OpenAI and Meta. Revenue backlog was $132.5bn at 30 Sep 2026; the model does not value the contracts separately.",
          "- **Left out:**",
          "  - tax losses carried forward (would add value);",
          "  - dilution from options, RSUs and convertible notes (would cut value per share);",
          "  - interest capitalized into PP&E.",
          "- **Life:** equipment life is the most argued input. CoreWeave depreciates GPUs over 6 years; critics argue 4-5. The model's 7 years blends 6-year GPUs with longer-lived power and cooling.",
          "- **Capex:** company-definition capex (includes accrued spending) is used for Q4 2026; gross PP&E history is from Yahoo.", "",
          "## Sources", "",
          "- Yahoo quarterly and annual statements (fetched 23 Nov 2026).",
          "- CoreWeave Q3 2026 10-Q, lease note: finance leases $649m, operating leases $18,697m. https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000465/crwv-20260930.htm",
          "- Q3 2026 results (10 Nov 2026):",
          "  - 2026 revenue guidance $13.0-13.3bn;",
          "  - 2026 capex guidance $37-39bn ($30.65bn to September);",
          "  - backlog $132.5bn;",
          "  - Q4 interest $1.05-1.15bn.",
          "  https://pulse2.com/coreweave-record-q3-revenue-reaches-3-66-billion-as-backlog-grows-to-132-5-billion/",
          "- 2027 revenue estimates (average 26.36, range 22.50-31.03), Twelve Data. https://twelvedata.com/markets/180244/stock/nasdaq/crwv/analysis", ""]
    Path(__file__).with_name("coreweave_valuation_2026-11-23.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
