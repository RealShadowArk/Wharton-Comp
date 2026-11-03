"""Round 2: build the nine finalists' DCF and bear-case input files, run them,
and write outputs/round2/Round2_scorecard.md.

Run from the repo root: python tools/make_round2_dcfs.py
Reads Pat's completed workbook, his DCF supplement (leases, corrected CFO) and
outputs/round2/M_round2_risk.csv (measured betas, sizing, red flags).
Writes inputs/m03/<T>_dcf_inputs.csv and <T>bear_dcf_inputs.csv (PYPL's file is
updated to 30 Oct; its 23 Oct version is in git), outputs/M03_Valuation_<T>.*.

Pat's decisions (3 Nov 2026):
1. US 10-year 4.94% (Treasury par CMT, 30 Oct; research compilation).
2. Local-currency rates: Adyen EUR, German 10-year 3.34%; Infosys and TCS INR,
   Indian 10-year 7.3977%, ERP 5%, no extra country premium; dLocal country
   premium 3.0% (named countries only) with 5.4% shown.
3. Adyen own cash = gross cash 10,797.401 - merchant/FI payables 6,371.815.
4. Exceptions: dLocal year-1 margin from operating-profit guidance; Infosys
   and TCS year-1 growth from the rupee consensus (guidance is constant currency).
5. Bear cases: a uniform DRAFT (growth halved, margin x 0.8) for the team to
   replace or justify in its own words.
Consistency choice (ASSUMPTION): local terminal growth = (1.03)(1 + rf_local) /
(1 + rf_US) - 1, so euro and rupee growth match their discount rates.
"""
import csv
import sys
from dataclasses import replace
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from m03.dcf import value  # noqa: E402
from m03.run import load, run, wacc_for  # noqa: E402

R2 = ROOT / "inputs" / "round2_2026-11-01"
RF_US = 0.0494
RF = {"EUR": 0.0334, "INR": 0.073977, "USD": RF_US}
RF_SRC = {"USD": "US Treasury 10-year par CMT, 30 Oct 2026 (research compilation, 2 Nov; Pat chose it 3 Nov)",
          "EUR": "German 10-year Federal-bond reference yield, 30 Oct 2026 (Bundesbank, via research compilation)",
          "INR": "India benchmark 10-year YTM, 30 Oct 2026 (CCIL, via research compilation)"}
CRP_DLO, CRP_DLO_HIGH = 0.0299, 0.0534
LEASES = {"DLO": 3.385, "ADYEN": 252.366, "INFY": 91760, "TCS": 112830}  # IFRS/Ind AS totals; US GAAP finance leases are already in debt
ADYEN_CASH = 10797.401 - 6371.815
# Honest-review corrections (3 Nov): PayPal's bridge at 30 Sep 2026 (Q3 2026 release, 27 Oct):
# cash, cash equivalents and investments 7,160 + 3,120 + 4,785; debt 2,533 + 10,939; diluted shares 858.
PYPL_Q3 = {"cash": 15065, "debt": 13472, "shares": 858}
CTSH_TAX = 0.25  # 2026 adjusted ETR guidance ~25%; 2025 GAAP 36% includes a one-off $390m OBBBA deferred-tax charge
CME_FLOAT, CME_EQUITY = 5253.6 - 4833.8, 371.7  # 2025 10-K: clearing-collateral earnings less distributions; equity earnings (S&P DJI, OSTTRA)
TICKERS = ["DLO", "ADYEN", "PYPL", "CME", "ICE", "MCO", "INFY", "TCS", "CTSH"]
GROUP = {"DLO": "Payments", "ADYEN": "Payments", "PYPL": "Payments", "CME": "Exchanges and data",
         "ICE": "Exchanges and data", "MCO": "Exchanges and data", "INFY": "IT services",
         "TCS": "IT services", "CTSH": "IT services"}


def workbook():
    wb = openpyxl.load_workbook(R2 / "Pat_Round2_data_completed.xlsx", data_only=True)
    rows = [r for r in wb["Valuation inputs"].iter_rows(values_only=True) if any(v not in (None, "") for v in r)]
    val = {r[1]: dict(zip(rows[0], r)) for r in rows[1:]}
    rows = [r for r in wb["Red flags"].iter_rows(values_only=True) if any(v not in (None, "") for v in r)]
    red = {(r[0], r[1]): dict(zip(rows[0], r)) for r in rows[1:]}
    return val, red


def fade(g1, g2, g3, terminal):
    return [g1, g2, g3] + [g3 + (terminal - g3) * k / 7 for k in range(1, 8)]


def build(t, v, red, beta_measured):
    cur = v["reporting_currency"]
    rf = RF[cur]
    g_term = 1.03 * (1 + rf) / (1 + RF_US) - 1
    rev = v["revenue"]
    tax = CTSH_TAX if t == "CTSH" else (v["pretax_income"] - v["net_income_common"]) / v["pretax_income"]
    margin = v["operating_income"] / rev
    da = (v["d_and_a"] if v["d_and_a"] is not None else red[(t, "FY0")]["depreciation"]) / rev
    capex = (v["capex"] + (v["capex_software"] or 0)) / rev
    g1 = v["guidance_next_fy_revenue_growth"] if t in ("ADYEN", "CTSH") else v["consensus_revenue_growth_y1"]
    growth = fade(g1, v["consensus_revenue_growth_y2"], v["consensus_revenue_growth_y3"], g_term)
    margins = [margin] * 10
    notes = {"growth": "Year 1 " + ("guidance midpoint" if t in ("ADYEN", "CTSH") else "consensus")
             + "; years 2-3 consensus; linear fade to terminal growth by year 10"}
    if t == "DLO":  # exception: operating-profit guidance +27.5% to +32.5% for FY2026
        m1 = v["operating_income"] * 1.30 / (rev * (1 + g1))
        margins = [m1] * 10
        notes["ebit_margin"] = f"Exception (Pat, 3 Nov): FY2026 operating profit +30% (guidance midpoint) / consensus revenue = {m1:.4f}, then held"
    if t in ("INFY", "TCS"):
        notes["growth"] += "; year 1 is the rupee consensus (Pat, 3 Nov: guidance is constant currency)"
    debt = PYPL_Q3["debt"] if t == "PYPL" else v["debt"] + LEASES.get(t, 0)
    cash = ADYEN_CASH if t == "ADYEN" else (PYPL_Q3["cash"] if t == "PYPL" else v["corporate_cash"])
    # Shares at the same date as cash and debt (Red flags tab, FY0 shares outstanding), so buybacks are
    # not counted twice; PayPal's bridge is 30 Sep 2026. Dilutive options/RSUs are not added (MISSING).
    shares = PYPL_Q3["shares"] if t == "PYPL" else red[(t, "FY0")]["shares_outstanding_m"]
    if t == "DLO":  # dilution is material for dLocal: 7.83m dilutive shares (Q2 2026 6-K, 13 Aug 2026)
        shares += 7.83
    erp = 0.05 + (CRP_DLO if t == "DLO" else 0)
    fy_end = "2026-03-31" if cur == "INR" else "2025-12-31"
    first = 0.42 if cur == "INR" else 0.17
    fraction = 0.25 if t == "PYPL" else 1.0  # PayPal: Q1-Q3 2026 cash flow is already in the 30 Sep cash
    S = "Pat_Round2_data_completed.xlsx (Valuation inputs; sources listed there)"
    rows = [
        ("ticker", t, "", "RESEARCH", S, GROUP[t]),
        ("valuation_date", "2026-10-30", "date", "CASE", "Price date", ""),
        ("price", v["price_30oct"], cur, "RESEARCH", S, "30 Oct 2026 close, local listing"),
        ("base_year", v["fiscal_year"], "", "RESEARCH", S, f"Fiscal year ended {fy_end}"),
        ("base_revenue", rev, f"{cur} m", "RESEARCH", S, ""),
        ("growth", ";".join(f"{g:.4f}" for g in growth), "decimal", "ASSUMPTION", "Standard method (Pat, 3 Nov)", notes["growth"]),
        ("ebit_margin", ";".join(f"{m:.5f}" for m in margins), "decimal", "ASSUMPTION",
         "Standard method: base-year operating margin held flat", notes.get("ebit_margin", f"Operating income / revenue = {margin:.4f}")),
        ("tax_rate", round(tax, 4), "decimal", "RESEARCH", S if t != "CTSH" else "Cognizant Q3 2025 10-Q and 2026 guidance (8-K, 29 Oct 2026)",
         "Normal rate: 2026 adjusted guidance about 25%; 2025 GAAP 36% includes a one-off $390m tax charge" if t == "CTSH" else "1 - net income / pretax income"),
        ("da_pct", ";".join([f"{da:.5f}"] * 10), "decimal", "RESEARCH", S, "Reported D&A / revenue (true D&A, so stock pay stays inside EBIT: sbc_pct 0)"),
        ("capex_pct", ";".join([f"{capex:.5f}"] * 10), "decimal", "RESEARCH", S,
         "Capex" + (" + capitalized software (R4)" if GROUP[t] == "Payments" else "") + " / revenue"),
        ("nwc_pct_of_change", 0.0, "decimal", "ASSUMPTION", "Kit default", ""),
        ("risk_free", rf, "decimal", "RESEARCH", RF_SRC[cur], f"{cur} cash flows, {cur} rate"),
        ("beta", 1.0, "", "ASSUMPTION", "Standard method", ""),
        ("beta_measured", round(beta_measured, 3), "", "RESEARCH", "60 monthly USD returns vs SPY, Nov 2021-Oct 2026 (outputs/round2/M_round2_risk.csv)", ""),
        ("equity_premium", round(erp, 4), "decimal", "ASSUMPTION",
         "Kit default 5%" + (f" + dLocal country premium {CRP_DLO:.2%} (named countries only; {CRP_DLO_HIGH:.2%} shown)" if t == "DLO" else ""), ""),
        ("pre_tax_cost_of_debt", round(rf + 0.005, 6), "decimal", "ASSUMPTION", "Kit default: 10-year + 0.5 points", ""),
        ("equity_value_for_weights", round(v["price_30oct"] * v["shares_outstanding_m"], 2), f"{cur} m", "RESEARCH", "Price x shares outstanding", ""),
        ("debt_value_for_weights", debt, f"{cur} m", "RESEARCH", S, "Book debt"),
        ("terminal_growth", round(g_term, 5), "decimal", "ASSUMPTION",
         "3% in USD, converted by the rate gap: 1.03 x (1 + rf local) / (1 + rf US) - 1", ""),
        ("return_on_new_capital", 0.15, "decimal", "ASSUMPTION", "Kit default", ""),
        ("debt", debt, f"{cur} m", "RESEARCH", "PayPal Q3 2026 release (27 Oct 2026)" if t == "PYPL" else S + "; Finalists_DCF_Supplement_Reviewed.xlsx",
         "Short-term 2,533 + long-term 10,939 at 30 Sep 2026" if t == "PYPL" else "Debt" + (f" + IFRS/Ind AS lease liabilities {LEASES[t]}" if t in LEASES else "")),
        ("non_operating_assets", round(cash, 3), f"{cur} m", "ASSUMPTION" if t == "ADYEN" else "RESEARCH",
         S, "Gross cash 10,797.401 - merchant/FI payables 6,371.815 (Pat, 3 Nov; EUR 0 shown as the floor)"
         if t == "ADYEN" else ("Cash, cash equivalents and investments 7,160 + 3,120 + 4,785 at 30 Sep 2026 (PayPal's measure excludes customer funds)" if t == "PYPL" else "Corporate cash only; merchant, customer and clearing funds excluded")),
        ("diluted_shares", shares, "m", "RESEARCH", "PayPal Q3 2026 release: diluted shares, Q3" if t == "PYPL" else "Pat_Round2_data_completed.xlsx (Red flags, FY0 shares outstanding)",
         ("Year-end shares 294.93 + 7.83 dilutive shares (Q2 2026 6-K)" if t == "DLO" else "Shares at the cash-and-debt date so buybacks are not double counted; dilution not added (MISSING)") if t != "PYPL" else "Matches the 30 Sep 2026 bridge"),
        ("years_to_first_cash_flow", first, "years", "ASSUMPTION", "Valuation date to the end of forecast year 1", ""),
        ("first_year_fraction", fraction, "", "ASSUMPTION", "Method", "PayPal: bridge at 30 Sep 2026, so only Q4 of 2026 counts" if t == "PYPL" else "Cash and debt are at the base-year end, so all of forecast year 1 counts"),
        ("sbc_pct", 0, "decimal", "ASSUMPTION", "Method", "0 because da_pct is reported D&A"),
    ]
    return rows, growth, margins, g_term


def bear(rows, growth, margins, g_term):
    out = []
    for r in rows:
        r = list(r)
        if r[0] == "growth":
            bg = [g / 2 for g in growth[:3]] + [growth[2] / 2 + (g_term - growth[2] / 2) * k / 7 for k in range(1, 8)]
            r[1], r[3], r[5] = ";".join(f"{g:.4f}" for g in bg), "ASSUMPTION", "DRAFT bear: years 1-3 growth halved, then fade to terminal growth. The team must replace or justify it"
        if r[0] == "ebit_margin":
            r[1], r[5] = ";".join(f"{m * 0.8:.5f}" for m in margins), "DRAFT bear: margin x 0.8 (a 20% cut). The team must replace or justify it"
        out.append(r)
    return out


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["field", "value", "unit", "label", "source", "note"])
        w.writerows(rows)


def main():
    val, red = workbook()
    risk = {r["ticker"]: r for r in csv.DictReader(open(ROOT / "outputs" / "round2" / "M_round2_risk.csv"))}
    flags = {r["ticker"]: r for r in csv.DictReader(open(ROOT / "outputs" / "round2" / "M_round2_redflags.csv"))}
    m3 = ROOT / "inputs" / "m03"
    sys.path.insert(0, str(ROOT / "tools"))
    from round2_risk_redflags import usd_prices
    prices = usd_prices()
    res = []
    for t in TICKERS:
        rows, growth, margins, g_term = build(t, val[t], red, float(risk[t]["beta_measured"] if "beta_measured" in risk[t] else risk[t]["beta"]))
        write(m3 / f"{t}_dcf_inputs.csv", rows)
        write(m3 / f"{t}bear_dcf_inputs.csv", bear(rows, growth, margins, g_term))
        p, v, shift, price = run(t)
        _, raw, _ = load(t)
        b = float(raw["beta_measured"])
        at_measured = value(replace(p, wacc=wacc_for(raw, b)))["per_share"]
        _, bv, _, _ = run(t + "bear")
        b_full, n_full = long_beta(prices, t)
        at_full = value(replace(p, wacc=wacc_for(raw, b_full)))["per_share"]
        vv = val[t]
        capex = vv["capex"] + (vv["capex_software"] or 0)
        da = vv["d_and_a"] if vv["d_and_a"] is not None else red[(t, "FY0")]["depreciation"]
        sbc = vv["stock_based_comp"] if vv["stock_based_comp"] is not None else 1002  # PYPL: 23 Oct file (secondary)
        cfo = {"DLO": 227.476, "ADYEN": 1246.157}.get(t, vv["cfo"])
        model_cash = vv["operating_income"] * (1 - p.tax_rate) + da - capex
        reported_cash = cfo - capex - sbc + (vv["interest_expense"] or 0) * (1 - p.tax_rate)
        conv = model_cash / reported_cash
        da_rep = p.da_pct[0] + (reported_cash - model_cash) / vv["revenue"]
        at_reported = value(replace(p, da_pct=(da_rep,) * 10))["per_share"]
        extra = ""
        if t == "DLO":
            hi = dict(raw, equity_premium=str(0.05 + CRP_DLO_HIGH))
            extra = f"at {CRP_DLO_HIGH:.1%} country premium: {value(replace(p, wacc=wacc_for(hi, 1.0)))['per_share'] / price:.2f}x"
        if t == "ADYEN":
            extra = f"own cash 0 (floor): {value(replace(p, non_operating_assets=0))['per_share'] / price:.2f}x"
        if t == "CME":
            m_adj = (vv["operating_income"] + CME_FLOAT + CME_EQUITY) / vv["revenue"]
            adj = value(replace(p, ebit_margin=(m_adj,) * 10))["per_share"]
            extra = (f"with net clearing float {CME_FLOAT:,.0f} and S&P DJI/OSTTRA equity earnings {CME_EQUITY:,.0f} "
                     f"in EBIT (margin {m_adj:.1%}): {adj / price:.2f}x at beta 1.0, "
                     f"{value(replace(p, ebit_margin=(m_adj,) * 10, wacc=wacc_for(raw, b_full)))['per_share'] / price:.2f}x at beta {b_full:.2f}")
        up, down = v["per_share"] / price - 1, bv["per_share"] / price - 1
        ratio = ("no upside" if up <= 0 else ("no downside" if down >= 0 else f"{up / -down:.2f}"))
        res.append(dict(t=t, g=GROUP[t], price=price, cur=val[t]["reporting_currency"], v1=v["per_share"], vm=at_measured,
                        b=b, shift=shift, tv=v["terminal_share_of_ev"], wacc=p.wacc, bear=bv["per_share"],
                        up=up, down=down, ratio=ratio, extra=extra, risk=risk[t], flag=flags[t], conv=conv,
                        b_full=b_full, n_full=n_full, at_full=at_full, at_reported=at_reported))
    report(res)


def long_beta(prices, t):
    """Beta on every monthly USD return available (up to Oct 2026) versus SPY."""
    ms = [m for m in sorted(prices) if m <= "2026-10" and prices[m].get(t) and prices[m].get("SPY")]
    s = [prices[b][t] / prices[a][t] - 1 for a, b in zip(ms, ms[1:])]
    m = [prices[b]["SPY"] / prices[a]["SPY"] - 1 for a, b in zip(ms, ms[1:])]
    sb, mb = sum(s) / len(s), sum(m) / len(m)
    return (sum((x - sb) * (y - mb) for x, y in zip(s, m)) / sum((y - mb) ** 2 for y in m), len(s))


def report(res):
    L = ["# Round 2 scorecard: the nine finalists (TEST preview, 3 Nov 2026)", "",
         "Generated by `python tools/make_round2_dcfs.py`. Inputs: `inputs/m03/<T>_dcf_inputs.csv` (every row labelled and sourced); "
         "reports: `outputs/M03_Valuation_<T>.md`. Rates, currencies and exceptions are Pat's decisions of 3 Nov; the bear cases are a "
         "uniform DRAFT (years 1-3 growth halved, margin x 0.8) for the team to replace or justify in its own words. "
         "Values are research estimates, never price targets, returns or position sizes.", "",
         "## Valuation", "",
         "| Group | Ticker | Price | Value (beta 1.0) | Value / price | At 5-year beta | At full-history beta | On reported cash flow | Price implies (growth shift) | Bear value | Upside / downside | Other checks |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        shift = "n/a" if r["shift"] is None else f"{r['shift']:+.1%}"
        L.append(f"| {r['g']} | {r['t']} | {r['price']:,.2f} {r['cur']} | {r['v1']:,.2f} | {r['v1'] / r['price']:.2f} | "
                 f"{r['vm'] / r['price']:.2f} (beta {r['b']:.2f}) | {r['at_full'] / r['price']:.2f} (beta {r['b_full']:.2f}, {r['n_full']} months) | "
                 f"{r['at_reported'] / r['price']:.2f} | {shift} | {r['bear']:,.2f} ({r['bear'] / r['price']:.2f}) | "
                 f"{r['up']:+.0%} / {r['down']:+.0%} = {r['ratio']} | {r['extra']} |")
    L += ["", "Growth shift: added to every forecast year's revenue growth to match the price (negative = the price assumes less "
          "growth than our base path). Full-history beta: every monthly USD return since listing (or 1993) to Oct 2026 versus SPY. "
          "On reported cash flow: D&A recalibrated so year-1 free cash flow matches the company's reported cash generation "
          "(CFO corrected for merchant funds, less capex, less stock-based pay, plus after-tax interest).", "",
          "## Honest-review corrections (3 Nov)", "",
          "| Item | Before | Now | Source |", "|---|---|---|---|",
          "| PayPal cash, debt, shares | 8,049 / 11,583 / 882m (mixed dates) | 15,065 / 13,472 / 858m at 30 Sep 2026; only Q4 2026 cash flow added | [Q3 2026 release](https://s205.q4cdn.com/875401827/files/content_files/PYPL-3Q-26-Earnings-Release.pdf) |",
          "| Share counts (other eight) | FY2025 average diluted shares (counts 2025 buybacks twice) | Shares outstanding at the cash-and-debt date (dilution not added) | Pat's Red flags tab |",
          "| Cognizant tax rate | 36.1% (2025 GAAP) | 25% | [Q3 2025 10-Q: $390m one-off charge](https://www.sec.gov/Archives/edgar/data/1058290/000105829025000341/ctsh-20250930.htm); [2026 guidance](https://www.sec.gov/Archives/edgar/data/0001058290/000105829026000039/exhibit9939302026.htm) |",
          "| CME and Adyen betas | 5-year only (0.15, 2.35) | Full-history beta shown for all nine | Pat's Yahoo file |",
          "| CME earnings | Operating income only | Clearing float and S&P DJI earnings shown as a variant | [2025 10-K](https://www.sec.gov/Archives/edgar/data/1156375/000115637526000009/cme-20251231.htm) |", "",
          "## Tests (kit README, 'What makes a buy candidate')", "",
          "| Ticker | 1. M12 top 2 and robust | 2. Value > price at beta 1.0, 5-year and full-history beta | 3. Upside/downside >= 1.0 | "
          "4. No red flag (Piotroski, Beneish) | Max position (2% rule) | Beta, volatility | Cash check |",
          "|---|---|---|---|---|---|---|---|"]
    m12 = {"DLO": "Yes: 1st, 32/32", "ADYEN": "Yes: 2nd, 29/32", "PYPL": "No: 3rd, 3/32",
           "CME": "Yes: 1st, 32/32", "ICE": "Yes: 2nd, 32/32",
           "MCO": "No: 3rd (1st in the data-and-ratings split run, 31/32)",
           "INFY": "Yes: 1st, 32/32", "TCS": "Yes: 2nd, 32/32", "CTSH": "No: 3rd"}
    for r in res:
        t2 = "PASS" if min(r["v1"], r["vm"], r["at_full"]) > r["price"] else "fail"
        t3 = ("PASS" if r["ratio"] == "no downside" or (r["ratio"] not in ("no upside",) and float(r["ratio"]) >= 1) else "fail")
        f = r["flag"]
        t4 = f"{f['piotroski']}/{f['piotroski_checked']}, {f['beneish_m']}"
        L.append(f"| {r['t']} | {m12[r['t']]} | {t2} | {t3} | {t4} | ${float(r['risk']['max_position_usd']):,.0f} | "
                 f"{float(r['risk']['beta']):.2f}, {float(r['risk']['volatility']):.0%} | {r['conv']:.2f} |")
    L += ["", "Test 1 is from Round 1 (docs/round1_results_2026-11-01.md, official runs after Pat's 1 Nov decisions): "
          "rank in the group and variants (of 32) keeping it in the top 2; 'No' needs a written reason. Tests 5-6 (dip, edge, fit) are the team's written work.", "",
          "Cash check = the model's year-0 free cash flow (EBIT after tax + D&A - capex) / reported cash flow "
          "(CFO, corrected for merchant funds, - capex - stock-based pay + after-tax interest). Above about 1.10 the "
          "model is more generous than the company's actual cash generation.", "",
          "## Caveats that still matter", "",
          "- **dLocal:** shares include 7.83m dilutive shares from its Q2 2026 6-K (294.9m + 7.8m); without them the "
          "upside/downside ratio would be 1.06, so test 3 is a near miss, not a clear fail.",
          "- **PayPal:** the bridge counts all $15.1bn of corporate cash and investments as spare, although some supports its credit "
          "book and regulated entities; and the uniform draft bear (no downside) is far milder than the team's 23 Oct bear ($34-39). "
          "Its price implies revenue shrinking about 4-5% a year for a decade.",
          "- **Cognizant:** passes every valuation test, but was 3rd in M12 (needs a written reason).",
          "- **Adyen:** passes at beta 1.0 and on reported cash flow, fails at its measured betas (2.35 over 5 years, 1.82 since 2018).",
          "- **CME:** below the price under every reasonable input; only the 5-year beta of 0.15 (cost of equity barely above the "
          "Treasury yield) made it look cheap.",
          "- Bear cases are still the uniform draft: the team must replace or justify them in its own words."]
    out = ROOT / "outputs" / "round2" / "Round2_scorecard.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
