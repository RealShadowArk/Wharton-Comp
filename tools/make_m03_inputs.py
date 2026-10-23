"""Write the standardized M03 input CSVs for the ten shortlisted companies other than HUBB (run from the repo root: python tools/make_m03_inputs.py). Every assumption is set here and labelled in the CSVs."""
import csv

RF, ERP, BETA, KD, G, RONIC = 0.0513, 0.05, 1.0, 0.056, 0.03, 0.15
PEER = "M12 peer data v0.2 (teammate; FY0 10-K/10-Q figures)"
# ticker: (name, base_year, years_to_first, price, price_src, growth path, growth note,
#          margin override or None, cash, cash_src, debt, debt_src, shares, shares_src)
C = {
 "PYPL": ("PayPal", 2025, 0.19, 55.53, "9 Oct close (M12 peer data; StockAnalysis, Secondary)",
          (0.03, 0.04, 0.04, 0.04, 0.04), "2026 guidance: transaction-margin dollars slightly down, non-GAAP EPS about flat (Feb 2026 outlook); 2022-25 revenue CAGR 6.4% (Calc)",
          None, 14800, "Cash, cash equivalents and investments 31 Dec 2025 (Q4 2025 release, via search)", 11400, PEER, 855.461, "Cover-page shares (M12 data); after 2026 buybacks"),
 "JKHY": ("Jack Henry", 2026, 0.68, 149.31, "9 Oct close (M12 peer data; Secondary)",
          (0.06, 0.06, 0.055, 0.05, 0.05), "FY2027 guidance: GAAP revenue +5.5% to +6.5% (Aug 2026 release); FY2023-26 CAGR 6.9% (Calc)",
          None, 12.1, "Cash 30 Jun 2026 (Q4 FY2026 release, via search)", 40, PEER, 72.03, "Calc: FY2026 net income / diluted EPS"),
 "ZTS": ("Zoetis", 2025, 0.19, 81.92, "22 Oct close (teammate price file, Secondary)",
         (-0.026, 0.03, 0.05, 0.05, 0.05), "2026 revenue guidance cut to $9.12-9.32bn (midpoint -2.6%), organic -3% to -1% (6 Aug 2026 8-K)",
         None, None, "MISSING: 31 Dec 2025 cash not collected", 9049, PEER, 413.224, "Cover-page shares (M12 data)"),
 "LLY": ("Eli Lilly", 2025, 0.19, 1307.12, "22 Oct close (teammate price file, Secondary)",
         (0.319, 0.15, 0.10, 0.08, 0.06), "2026 revenue guidance raised to $85-87bn (midpoint +31.9%) with Q2 2026 results (8-K, 5 Aug 2026)",
         None, None, "MISSING: cash not collected", 42503, PEER + " (borrowings)", 899.35, "Calc: 2025 net income / diluted EPS (cover count includes employee-trust shares)"),
 "ETN": ("Eaton", 2025, 0.19, 369.61, "22 Oct close (teammate price file, Secondary)",
         (0.12, 0.09, 0.07, 0.06, 0.05), "2026 organic growth guidance raised to 11-13% (Q2 2026 release, 31 Jul); Mobility spin-off in Q1 2027 ignored (value goes to holders)",
         None, None, "MISSING: cash not collected", 9895, PEER + " (31 Dec 2025; 2026 acquisitions valued at cost)", 388.4, "Cover-page shares (M12 data)"),
 "AME": ("AMETEK", 2025, 0.19, 236.82, "22 Oct close (teammate price file, Secondary)",
         (0.05, 0.05, 0.05, 0.05, 0.04), "Organic growth assumption; Indicor (closed Aug 2026) valued at cost; 2022-25 CAGR 6.4% (Calc)",
         None, None, "MISSING: cash not collected", 2283.3, PEER + " (31 Dec 2025)", 229.261, "Cover-page shares (M12 data)"),
 "MPWR": ("Monolithic Power Systems", 2025, 0.19, 1210.86, "16 Oct close (teammate price file, Secondary)",
          (0.22, 0.18, 0.15, 0.12, 0.10), "2022-25 revenue CAGR 15.9% (Calc); thesis card: recent growth above 15%",
          None, 1099.3, "Cash and cash equivalents 31 Dec 2025 (10-K via search); investments MISSING", 0, PEER, 49.143, "Cover-page shares (M12 data)"),
 "ADI": ("Analog Devices", 2025, 0.02, 414.68, "13 Oct close (teammate price file, Secondary)",
         (0.30, 0.08, 0.06, 0.06, 0.05), "FY2026: Q3 revenue +40% to $4.02bn, Q4 guide $4.3bn (19 Aug 2026 8-K); cyclical normalisation after",
         None, None, "MISSING: cash not collected", 8591.7, PEER + " (borrowings)", 497.22, "Calc: FY2025 net income / diluted EPS"),
 "BSX": ("Boston Scientific", 2025, 0.19, 46.02, "22 Oct close (teammate price file, Secondary)",
         (0.04, 0.09, 0.09, 0.08, 0.07), "2026 guidance withdrawn after Aug cyberattack (was +5.5-6.5%); 2022-25 CAGR 16.5% (Calc); update due 28 Oct",
         None, None, "MISSING: cash not collected", 11436, PEER, 1449.23, "Cover-page shares (M12 data)"),
 "ISRG": ("Intuitive Surgical", 2025, 0.19, 443.84, "22 Oct close (teammate price file, Secondary)",
          (0.20, 0.15, 0.13, 0.11, 0.09), "Q3 2026 revenue +22%, procedures +15% (20 Oct 2026 8-K)",
          None, 6800, "Cash and investments 30 Sep 2026 (Q3 2026 release via search)", 0, PEER, 353.278, "Cover-page shares (M12 data); Q3 buybacks of 7.8m shares not yet reflected"),
}
rows = {r["ticker"]: r for r in csv.DictReader(open("inputs/m12/M12_peer_data_v02.csv", encoding="utf-8-sig"))}
summary = []
for t, (name, by, ytf, price, psrc, growth, gnote, mo, cash, csrc, debt, dsrc, sh, ssrc) in C.items():
    r = rows[t]; f = lambda k: float(r[k]) if r.get(k) else None
    rev = f("revenue_fy0"); ni = f("net_income_fy0"); pt = f("pretax_income_fy0")
    ebit = f("operating_income_fy0"); cfo = f("cfo_fy0"); capex = f("capex_fy0")
    sw = f("capex_software_fy0") if t in ("PYPL", "JKHY") else 0.0  # R4: Payments only
    capex_all = capex + (sw or 0.0)
    tax = 1 - ni / pt
    if ebit is None:          # R1: no operating income line -> pretax margin
        ebit_basis, ebit, net_int = "pretax margin (R1)", pt, 0.0
    else:
        ebit_basis, net_int = "operating margin", ebit - pt
    margin = ebit / rev
    nopat0 = ebit * (1 - tax)
    fcff0 = cfo - capex_all + net_int * (1 - tax)
    k0 = (fcff0 - nopat0) / rev
    capex_pct = capex_all / rev
    g5 = growth[-1]
    growth = tuple(growth) + tuple(round(g5 + (G - g5) * y / 5, 5) for y in range(1, 6))
    k = [k0 if k0 > 0 else k0 * max(0.0, 1 - y / 5) for y in range(1, 11)]
    da = [round(capex_pct + x, 5) for x in k]
    eq_w = sh * price
    out = [
      ("ticker", t, "", "", "", name), ("valuation_date", "2026-10-23", "date", "", "", ""),
      ("price", price, "USD", "RESEARCH", psrc, "Refresh from WInS before trading"),
      ("base_year", by, "", "", "", "Fiscal year of the latest 10-K"),
      ("base_revenue", rev, "USD m", "RESEARCH", PEER, ""),
      ("growth", ";".join(str(g) for g in growth), "decimal", "ASSUMPTION", "Pat/Claude 23 Oct", gnote + "; years 6-10 fade linearly to 3%"),
      ("ebit_margin", ";".join([str(round(margin, 5))] * 10), "decimal", "ASSUMPTION",
       f"FY0 {ebit_basis} {margin:.1%} held flat (Calc from {PEER})", "Standard method: FY0 margin, no improvement assumed"),
      ("tax_rate", round(tax, 4), "decimal", "RESEARCH", f"Calc: 1 - net income {ni:g} / pretax {pt:g}", "FY0 effective rate"),
      ("da_pct", ";".join(map(str, da)), "decimal", "ASSUMPTION",
       f"D&A not collected for every company. Calibrated to FY0 cash conversion: (CFO - capex + after-tax net interest - NOPAT) / revenue = {k0:+.1%}",
       "A positive gap (non-cash charges such as acquired-intangible amortisation) is held; a negative gap (growth investment) fades to 0 by year 5. Includes stock-compensation add-backs, which flatter heavy payers"),
      ("capex_pct", ";".join([str(round(capex_pct, 5))] * 10), "decimal", "RESEARCH",
       f"FY0 capex {capex:g}" + (f" + capitalised software {sw:g} (R4)" if sw else "") + f" = {capex_pct:.1%} of revenue", ""),
      ("nwc_pct_of_change", 0.0, "decimal", "ASSUMPTION", "Working capital is inside the FY0 cash-conversion calibration", ""),
      ("risk_free", RF, "decimal", "RESEARCH", "10-year Treasury 5.13% on 21 Oct 2026 (FRED DGS10, teammate summary)", ""),
      ("beta", BETA, "", "ASSUMPTION", "Market beta 1.0 for every company: company betas not collected", "Riskier firms (e.g., chips) deserve a higher WACC; see sensitivity"),
      ("equity_premium", ERP, "decimal", "ASSUMPTION", "Student judgment", ""),
      ("pre_tax_cost_of_debt", KD, "decimal", "ASSUMPTION", "10-year Treasury + about 0.5 points", ""),
      ("equity_value_for_weights", round(eq_w, 1), "USD m", "RESEARCH", "Calc: shares x price", ""),
      ("debt_value_for_weights", debt, "USD m", "RESEARCH", dsrc, ""),
      ("terminal_growth", G, "decimal", "ASSUMPTION", "Student judgment", "Below long-run nominal GDP growth"),
      ("terminal_reinvestment_rate", round(G / RONIC, 4), "decimal", "ASSUMPTION",
       f"g / return on new capital = {G} / {RONIC}", "Growth after 2030 must be paid for"),
      ("debt", debt, "USD m", "RESEARCH", dsrc, ""),
      ("non_operating_assets", 0 if cash is None else cash, "USD m", "MISSING" if cash is None else "RESEARCH", csrc,
       "Value excludes cash, so it is understated" if cash is None else ""),
      ("diluted_shares", sh, "m", "RESEARCH", ssrc, ""),
      ("years_to_first_cash_flow", ytf, "years", "ASSUMPTION", "Valuation date to the end of the first forecast fiscal year", ""),
    ]
    with open(f"inputs/m03/{t}_dcf_inputs.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["field", "value", "unit", "label", "source", "note"])
        w.writerows(out)
    print(t, f"margin {margin:.1%} tax {tax:.1%} capex {capex_pct:.1%} k0 {k0:+.1%}")
