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
PYPL_KEEP = {"diluted_shares": 882, "cash": 8049}  # from the 23 Oct teammate-corrected file
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
    tax = (v["pretax_income"] - v["net_income_common"]) / v["pretax_income"]
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
    debt = v["debt"] + LEASES.get(t, 0)
    cash = ADYEN_CASH if t == "ADYEN" else (PYPL_KEEP["cash"] if t == "PYPL" else v["corporate_cash"])
    shares = PYPL_KEEP["diluted_shares"] if t == "PYPL" else v["diluted_shares_m"]
    erp = 0.05 + (CRP_DLO if t == "DLO" else 0)
    fy_end = "2026-03-31" if cur == "INR" else "2025-12-31"
    first = 0.42 if cur == "INR" else 0.17
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
        ("tax_rate", round(tax, 4), "decimal", "RESEARCH", S, "1 - net income / pretax income"),
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
        ("debt", debt, f"{cur} m", "RESEARCH", S + "; Finalists_DCF_Supplement_Reviewed.xlsx",
         "Debt" + (f" + IFRS/Ind AS lease liabilities {LEASES[t]}" if t in LEASES else "")),
        ("non_operating_assets", round(cash, 3), f"{cur} m", "ASSUMPTION" if t == "ADYEN" else "RESEARCH",
         S, "Gross cash 10,797.401 - merchant/FI payables 6,371.815 (Pat, 3 Nov; EUR 0 shown as the floor)"
         if t == "ADYEN" else ("Corporate cash, 23 Oct teammate-corrected file" if t == "PYPL" else "Corporate cash only; merchant, customer and clearing funds excluded")),
        ("diluted_shares", shares, "m", "RESEARCH", S if t != "PYPL" else "23 Oct teammate-corrected file", ""),
        ("years_to_first_cash_flow", first, "years", "ASSUMPTION", "Valuation date to the end of forecast year 1", ""),
        ("first_year_fraction", 1.0, "", "ASSUMPTION", "Method", "Cash and debt are at the base-year end, so all of forecast year 1 counts"),
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
        extra = ""
        if t == "DLO":
            hi = dict(raw, equity_premium=str(0.05 + CRP_DLO_HIGH))
            extra = f"at {CRP_DLO_HIGH:.1%} country premium: {value(replace(p, wacc=wacc_for(hi, 1.0)))['per_share'] / price:.2f}x"
        if t == "ADYEN":
            extra = f"own cash 0 (floor): {value(replace(p, non_operating_assets=0))['per_share'] / price:.2f}x"
        if t in ("CTSH", "MCO", "ICE", "PYPL"):
            out_sh = val[t]["shares_outstanding_m"]
            extra = f"on {out_sh:,.0f}m shares outstanding (vs {p.diluted_shares:,.0f}m diluted used): {value(replace(p, diluted_shares=out_sh))['per_share'] / price:.2f}x"
        if t == "CME":
            pre = (val[t]["pretax_income"] + val[t]["interest_expense"]) / val[t]["revenue"]
            extra = f"if net clearing-collateral income counts as operating (EBIT margin {pre:.1%}): {value(replace(p, ebit_margin=(pre,) * 10))['per_share'] / price:.2f}x"
        if t == "CTSH":
            extra += f"; at a 25% tax rate instead of {p.tax_rate:.0%}: {value(replace(p, tax_rate=0.25))['per_share'] / price:.2f}x"
        vv = val[t]
        tax = (vv["pretax_income"] - vv["net_income_common"]) / vv["pretax_income"]
        capex = vv["capex"] + (vv["capex_software"] or 0)
        da = vv["d_and_a"] if vv["d_and_a"] is not None else red[(t, "FY0")]["depreciation"]
        sbc = vv["stock_based_comp"] if vv["stock_based_comp"] is not None else 1002  # PYPL: 23 Oct file
        cfo = {"DLO": 227.476, "ADYEN": 1246.157}.get(t, vv["cfo"])
        conv = (vv["operating_income"] * (1 - tax) + da - capex) / (cfo - capex - sbc + (vv["interest_expense"] or 0) * (1 - tax))
        up, down = v["per_share"] / price - 1, bv["per_share"] / price - 1
        ratio = ("no upside" if up <= 0 else ("no downside" if down >= 0 else f"{up / -down:.2f}"))
        res.append(dict(t=t, g=GROUP[t], price=price, cur=val[t]["reporting_currency"], v1=v["per_share"], vm=at_measured,
                        b=b, shift=shift, tv=v["terminal_share_of_ev"], wacc=p.wacc, bear=bv["per_share"],
                        up=up, down=down, ratio=ratio, extra=extra, risk=risk[t], flag=flags[t], conv=conv))
    report(res)


def report(res):
    L = ["# Round 2 scorecard: the nine finalists (TEST preview, 3 Nov 2026)", "",
         "Generated by `python tools/make_round2_dcfs.py`. Inputs: `inputs/m03/<T>_dcf_inputs.csv` (every row labelled and sourced); "
         "reports: `outputs/M03_Valuation_<T>.md`. Rates, currencies and exceptions are Pat's decisions of 3 Nov; the bear cases are a "
         "uniform DRAFT (years 1-3 growth halved, margin x 0.8) for the team to replace or justify in its own words. "
         "Values are research estimates, never price targets, returns or position sizes.", "",
         "## Valuation", "",
         "| Group | Ticker | Price | Value (beta 1.0) | Value / price | At measured beta | Price implies (growth shift) | Bear value | Upside / downside | Check |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        shift = "n/a" if r["shift"] is None else f"{r['shift']:+.1%}"
        L.append(f"| {r['g']} | {r['t']} | {r['price']:,.2f} {r['cur']} | {r['v1']:,.2f} | {r['v1'] / r['price']:.2f} | "
                 f"{r['vm'] / r['price']:.2f} (beta {r['b']:.2f}) | "
                 f"{shift} | {r['bear']:,.2f} ({r['bear'] / r['price']:.2f}) | "
                 f"{r['up']:+.0%} / {r['down']:+.0%} = {r['ratio']} | {r['extra']} |")
    L += ["", "Growth shift: added to every forecast year's revenue growth to match the price (negative = the price assumes less "
          "growth than our base path).", "",
          "## Tests (kit README, 'What makes a buy candidate')", "",
          "| Ticker | 1. M12 top 2 and robust | 2. Value > price at beta 1.0 and measured | 3. Upside/downside >= 1.0 | "
          "4. No red flag (Piotroski, Beneish) | Max position (2% rule) | Beta, volatility | Cash check |",
          "|---|---|---|---|---|---|---|---|"]
    m12 = {"DLO": "Yes: 1st, 32/32", "ADYEN": "Yes: 2nd, 29/32", "PYPL": "No: 3rd, 3/32",
           "CME": "Yes: 1st, 32/32", "ICE": "Yes: 2nd, 32/32",
           "MCO": "No: 3rd (1st in the data-and-ratings split run, 31/32)",
           "INFY": "Yes: 1st, 32/32", "TCS": "Yes: 2nd, 32/32", "CTSH": "No: 3rd"}
    for r in res:
        t2 = "PASS" if min(r["v1"], r["vm"]) > r["price"] else "fail"
        t3 = ("PASS" if r["ratio"] == "no downside" or (r["ratio"] not in ("no upside",) and float(r["ratio"]) >= 1) else "fail")
        f = r["flag"]
        t4 = f"{f['piotroski']}/{f['piotroski_checked']}, {f['beneish_m']}"
        L.append(f"| {r['t']} | {m12[r['t']]} | {t2} | {t3} | {t4} | ${float(r['risk']['max_position_usd']):,.0f} | "
                 f"{float(r['risk']['beta']):.2f}, {float(r['risk']['volatility']):.0%} | {r['conv']:.2f} |")
    L += ["", "Test 1 is from Round 1 (docs/round1_results_2026-11-01.md, official runs after Pat's 1 Nov decisions): "
          "rank in the group and variants (of 32) keeping it in the top 2; 'No' needs a written reason. Tests 5-6 (dip, edge, fit) are the team's written work.", "",
          "Cash check = the model's year-0 free cash flow (EBIT after tax + D&A - capex) / reported cash flow "
          "(CFO, corrected for merchant funds, - capex - stock-based pay + after-tax interest). Above about 1.10 the "
          "model is more generous than the company's actual cash generation."]
    out = ROOT / "outputs" / "round2" / "Round2_scorecard.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
