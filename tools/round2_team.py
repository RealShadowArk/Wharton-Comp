"""Round 2 for a teammate's workbook: risk, red flags, DCF, draft bear, scorecard.

Run: python tools/round2_team.py akshajp
Same method as Pat's nine (tools/round2_risk_redflags.py, tools/make_round2_dcfs.py):
- 60 monthly USD returns (Nov 2021-Oct 2026) vs SPY; also the full-history beta;
  worst complete calendar year through 2025; max position = $6,000 / worst loss.
- Piotroski and Beneish per the kit README (leverage test passes with zero debt both years).
- DCF: rates by currency (US 4.94%), year 1 = numeric guidance midpoint else
  consensus, years 2-3 consensus, fade to terminal growth; FY0 margin flat; reported
  D&A (sbc_pct 0); cash, debt and shares at the same date; first forecast year
  timed from the fiscal year-end.
- Bear = uniform DRAFT (years 1-3 growth halved, margin x 0.8) for Pat to replace.
"""
import csv
import math
import re
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from m03.dcf import value  # noqa: E402
from m03.run import load, run, wacc_for  # noqa: E402

RF = {"USD": 0.0494, "EUR": 0.0334, "INR": 0.073977}
RF_US, T_BILL = 0.0494, 0.04
VAL_DATE = date(2026, 10, 30)
TEAM = ROOT / "context" / "teammates_2026-11-03"
SETS = {
    "akshajp": dict(
        workbook=TEAM / "akshaj_p_final" / "Team_Round2_Akshaj_P.xlsx",
        yahoo=TEAM / "akshaj_p_final" / "Yahoo original CSVs",
        m12=[TEAM / "akshaj_p_final" / "Software.csv", TEAM / "akshaj_p_final" / "M12_peer_data.csv"],
        who="Akshaj P",
        notes={"KO": "2025 operating cash flow is low next to profit; check for one-off payments before trusting the cash check",
               "NKE": "FY2026 margin (8.2%) is held flat; Nike's margin is depressed, so the base case is a low-margin case",
               "NOW": "Year-1 growth is consensus (guidance covers subscription revenue only)"}),
    "akshajk": dict(
        workbook=TEAM / "akshaj_k_final" / "Akshaj_Six_Picks_Round2.xlsx",
        yahoo=None,  # Max monthly CSVs not yet received: teammate's betas used, labelled
        betas={"NVDA": (2.2046, 2.047, 333), "LRCX": (1.9653, 1.968, 405), "ASML": (1.6979, 1.314, 274),
               "GD": (0.3024, 0.792, 405), "HII": (0.1705, 0.7922, 187), "ESLT": (0.092, 0.6357, 359)},
        fy_end={"NVDA": "2026-01-25", "LRCX": "2026-06-28", "ASML": "2025-12-31", "GD": "2025-12-31",
                "HII": "2025-12-31", "ESLT": "2025-12-31"},
        group={"NVDA": "Semiconductors", "LRCX": "Semiconductors", "ASML": "Semiconductors",
               "GD": "Aerospace and defence", "HII": "Aerospace and defence", "ESLT": "Aerospace and defence"},
        m12_text={"NVDA": "1 of 6 (90); stability not given", "LRCX": "2 of 6, tied with ASML and QCOM (45); stability not given",
                  "ASML": "2 of 6, tied with LRCX and QCOM (45); stability not given", "GD": "1 of 6 (65); stability not given",
                  "HII": "2 of 6 (57.5); stability not given", "ESLT": "3 of 6 (52.5); stability not given"},
        rf_proxies={("GD", "FY0"): {"sga": 2595}, ("GD", "FY1"): {"sga": 2568},
                    ("HII", "FY0"): {"sga": 977}, ("HII", "FY1"): {"sga": 973}},
        rf_bounds={"ASML": {"FY0": (2709.0, 2725.5), "FY1": (3677.3, 3694.2)}},
        who="Akshaj K",
        notes={"GD": "Beneish uses reported G&A as SG&A (NOT FULLY VERIFIED)", "HII": "Beneish uses reported G&A as SG&A (NOT FULLY VERIFIED)",
               "ASML": "Long-term debt known only within tight bounds; red flags run at both ends",
               "NVDA": "VOO top-10 holding; consensus growth 91% / 68% / 30%",
               "ESLT": "Israel war exposure (see the Kenon note)"}),
}
TEXT = {"ticker", "company", "peer_group", "reporting_currency", "guidance_next_fy_revenue_growth", "guidance_basis",
        "cash_note", "long_term_target", "sources", "notes", "period", "source", "listing_used_for_prices", "price_currency"}


def clean(d):
    """Numeric fields: numbers stay; any text (MISSING, N/A ...) becomes None."""
    return {k: (v if k in TEXT or isinstance(v, (int, float)) or v is None else None) for k, v in d.items()}


def num_guidance(v):
    """Numeric guidance midpoint, or None (proxy, approximate or one-sided)."""
    if isinstance(v, (int, float)):
        return float(v)
    if not v or any(s in str(v) for s in ("proxy", "≈", "≥", "≤", "~")):
        return None
    pcts = [float(x) / 100 for x in re.findall(r"[-+]?\d+(?:\.\d+)?(?=%)", str(v))]
    return sum(pcts) / len(pcts) if len(pcts) == 2 else None


def monthly(folder, tickers):
    out = {}
    for t in ["SPY"] + tickers:
        for r in csv.DictReader(open(folder / f"{t}.csv")):
            m = r["Date"][:7]
            if r["Date"].endswith("-01") and r["Adj Close"] not in ("", "null") and m <= "2026-10":
                out.setdefault(m, {})[t] = float(r["Adj Close"])
    return out


def beta_stats(p, t, start):
    ms = [m for m in sorted(p) if m >= start and t in p[m] and "SPY" in p[m]]
    s = [p[b][t] / p[a][t] - 1 for a, b in zip(ms, ms[1:])]
    m = [p[b]["SPY"] / p[a]["SPY"] - 1 for a, b in zip(ms, ms[1:])]
    sb, mb = sum(s) / len(s), sum(m) / len(m)
    beta = sum((x - sb) * (y - mb) for x, y in zip(s, m)) / sum((y - mb) ** 2 for y in m)
    vol = math.sqrt(sum((x - sb) ** 2 for x in s) / (len(s) - 1)) * math.sqrt(12)
    years = len(s) / 12
    cagr = (p[ms[-1]][t] / p[ms[0]][t]) ** (1 / years) - 1
    rm = (p[ms[-1]]["SPY"] / p[ms[0]]["SPY"]) ** (1 / years) - 1
    return beta, vol, cagr, rm, len(s)


def worst_year(p, t):
    best = (None, 9.0)
    for y in range(1986, 2026):
        a, b = p.get(f"{y - 1}-12", {}).get(t), p.get(f"{y}-12", {}).get(t)
        if a and b and b / a - 1 < best[1]:
            best = (y, b / a - 1)
    return best


def red_flags(a, b, cfo):
    roa = lambda x: x["net_income_continuing"] / x["total_assets_start_of_year"]
    lev = lambda x: (x["long_term_debt"] or 0) / ((x["total_assets"] + x["total_assets_start_of_year"]) / 2)
    cr = lambda x: x["current_assets"] / x["current_liabilities"]
    gm = lambda x: None if x["cost_of_revenue"] is None else (x["revenue"] - x["cost_of_revenue"]) / x["revenue"]
    turn = lambda x: x["revenue"] / x["total_assets_start_of_year"]
    tests = {"1 ROA > 0": roa(a) > 0, "2 CFO > 0": cfo > 0, "3 ROA up": roa(a) > roa(b),
             "4 CFO > net income": cfo > a["net_income_continuing"],
             "5 leverage down": lev(a) < lev(b) or lev(a) == lev(b) == 0,
             "6 current ratio up": cr(a) > cr(b), "7 no new shares": a["shares_outstanding_m"] <= b["shares_outstanding_m"],
             "8 gross margin up": None if gm(a) is None else gm(a) > gm(b), "9 asset turnover up": turn(a) > turn(b)}
    idx = {"DSRI": (a["receivables"] / a["revenue"]) / (b["receivables"] / b["revenue"]),
           "GMI": None if gm(a) is None else gm(b) / gm(a),
           "AQI": (1 - (a["current_assets"] + a["net_ppe"]) / a["total_assets"]) / (1 - (b["current_assets"] + b["net_ppe"]) / b["total_assets"]),
           "SGI": a["revenue"] / b["revenue"],
           "DEPI": (b["depreciation"] / (b["depreciation"] + b["net_ppe"])) / (a["depreciation"] / (a["depreciation"] + a["net_ppe"])),
           "SGAI": (a["sga"] / a["revenue"]) / (b["sga"] / b["revenue"]),
           "TATA": (a["net_income_continuing"] - cfo) / a["total_assets"],
           "LVGI": ((a["current_liabilities"] + (a["long_term_debt"] or 0)) / a["total_assets"])
                   / ((b["current_liabilities"] + (b["long_term_debt"] or 0)) / b["total_assets"])}
    coef = {"DSRI": 0.920, "GMI": 0.528, "AQI": 0.404, "SGI": 0.892, "DEPI": 0.115, "SGAI": -0.172, "TATA": 4.679, "LVGI": -0.327}
    m = None if idx["GMI"] is None else -4.84 + sum(coef[k] * v for k, v in idx.items())
    checked = [v for v in tests.values() if v is not None]
    return sum(checked), len(checked), [k for k, v in tests.items() if v is False], m


def fade(g1, g2, g3, term):
    return [g1, g2, g3] + [g3 + (term - g3) * k / 7 for k in range(1, 8)]


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["field", "value", "unit", "label", "source", "note"])
        w.writerows(rows)


def main(key):
    cfg = SETS[key]
    wb = openpyxl.load_workbook(cfg["workbook"], data_only=True)
    sheet = lambda n: [r for r in wb[n].iter_rows(values_only=True) if any(v not in (None, "") for v in r)]
    vr, rr, kr = sheet("Valuation inputs"), sheet("Red flags"), sheet("Risk")
    val = {r[vr[0].index("ticker")]: clean(dict(zip(vr[0], r))) for r in vr[1:]}
    red = {(r[0], {"FY-1": "FY1"}.get(r[1], r[1])): clean(dict(zip(rr[0], r))) for r in rr[1:]}
    for k, extra in cfg.get("rf_proxies", {}).items():
        red[k].update(extra)
    risk_tab = {r[0]: dict(zip(kr[0], r)) for r in kr[1:]}
    tickers = list(val)
    fy_end, group, m12 = {}, {}, {}
    from m12.score import load as m12load, score_all, stability
    fy_end.update({t: date.fromisoformat(d) for t, d in cfg.get("fy_end", {}).items()})
    group.update(cfg.get("group", {}))
    m12.update(cfg.get("m12_text", {}))
    for f in cfg.get("m12", []):
        rows = m12load(f)
        for r in rows:
            fy_end[r["ticker"]] = date.fromisoformat(r["fy_end_date"])
        for g, res in score_all(rows).items():
            st = stability(res) if res["released"] else {}
            ranked = [t for _, t in sorted(((v, t) for t, v in res["totals"].items() if v is not None), reverse=True)]
            for t in res["raw"]:
                group[t] = g
                if t in ranked:
                    k = st.get(t, (0, 32))[0]
                    ok = t in res["shortlist"] and k >= 24
                    m12[t] = f"{'Yes' if ok else 'No'}: {ranked.index(t) + 1} of {len(ranked)}, {k}/32"
    p = monthly(Path(cfg["yahoo"]), tickers) if cfg.get("yahoo") else None
    m3 = ROOT / "inputs" / "m03"
    res = []
    for t in tickers:
        v = val[t]
        cur = v["reporting_currency"]
        rf = RF[cur]
        g_term = 1.03 * (1 + rf) / (1 + RF_US) - 1
        rev = v["revenue"]
        tax = (v["pretax_income"] - v["net_income_common"]) / v["pretax_income"]
        margin = v["operating_income"] / rev
        g_guid = num_guidance(v["guidance_next_fy_revenue_growth"])
        g1 = g_guid if g_guid is not None else v["consensus_revenue_growth_y1"]
        growth = fade(g1, v["consensus_revenue_growth_y2"], v["consensus_revenue_growth_y3"], g_term)
        fy1_end = fy_end[t].replace(year=fy_end[t].year + 1)
        to_first = round((fy1_end - VAL_DATE).days / 365.25, 2)
        da, capex = v["d_and_a"] / rev, (v["capex"] + (v["capex_software"] or 0)) / rev
        S = f"{cfg['workbook'].name} (Valuation inputs; source ledger 'Round 2 sources.csv')"
        rows = [
            ("ticker", t, "", "RESEARCH", S, group.get(t, "")),
            ("valuation_date", "2026-10-30", "date", "CASE", "Price date", ""),
            ("price", v["price_30oct"], cur, "RESEARCH", S, "30 Oct 2026 close, checked in WInS by the teammate"),
            ("base_year", v["fiscal_year"], "", "RESEARCH", S, f"Fiscal year ended {fy_end[t]}"),
            ("base_revenue", rev, f"{cur} m", "RESEARCH", S, ""),
            ("growth", ";".join(f"{g:.4f}" for g in growth), "decimal", "ASSUMPTION", "Standard method (Pat, 3 Nov)",
             ("Year 1 guidance midpoint" if g_guid is not None else "Year 1 consensus") + "; years 2-3 consensus; fade to terminal growth"),
            ("ebit_margin", ";".join([f"{margin:.5f}"] * 10), "decimal", "ASSUMPTION", "Standard method: FY0 operating margin held flat", ""),
            ("tax_rate", round(tax, 4), "decimal", "RESEARCH", S, "1 - net income / pretax income"),
            ("da_pct", ";".join([f"{da:.5f}"] * 10), "decimal", "RESEARCH", S, "Reported D&A / revenue; stock pay stays in EBIT (sbc_pct 0)"),
            ("capex_pct", ";".join([f"{capex:.5f}"] * 10), "decimal", "RESEARCH", S, ""),
            ("nwc_pct_of_change", 0.0, "decimal", "ASSUMPTION", "Kit default", ""),
            ("risk_free", rf, "decimal", "RESEARCH", "US Treasury 10-year par CMT, 30 Oct 2026" if cur == "USD" else "Local 10-year, 30 Oct 2026", ""),
            ("beta", 1.0, "", "ASSUMPTION", "Standard method", ""),
            ("beta_measured", round(beta_stats(p, t, "2021-10")[0] if p else cfg["betas"][t][0], 3), "", "RESEARCH",
             "60 monthly USD returns vs SPY, Nov 2021-Oct 2026" + ("" if p else " (teammate's calculation; recompute from the Yahoo CSVs)"), ""),
            ("equity_premium", 0.05, "decimal", "ASSUMPTION", "Kit default", ""),
            ("pre_tax_cost_of_debt", round(rf + 0.005, 6), "decimal", "ASSUMPTION", "Kit default: 10-year + 0.5 points", ""),
            ("equity_value_for_weights", round(v["price_30oct"] * v["shares_outstanding_m"], 2), f"{cur} m", "RESEARCH", "Price x shares", ""),
            ("debt_value_for_weights", v["debt"], f"{cur} m", "RESEARCH", S, ""),
            ("terminal_growth", round(g_term, 5), "decimal", "ASSUMPTION", "3% in USD, converted by the rate gap", ""),
            ("return_on_new_capital", 0.15, "decimal", "ASSUMPTION", "Kit default", ""),
            ("debt", v["debt"], f"{cur} m", "RESEARCH", S, ""),
            ("non_operating_assets", v["corporate_cash"], f"{cur} m", "RESEARCH", S, "Corporate cash"),
            ("diluted_shares", v["diluted_shares_m"], "m", "RESEARCH", S, "Shares at the cash-and-debt date plus dilution (teammate's ledger)"),
            ("years_to_first_cash_flow", to_first, "years", "ASSUMPTION", f"Valuation date to the end of FY{v['fiscal_year'] + 1} ({fy1_end})", ""),
            ("first_year_fraction", 1.0, "", "ASSUMPTION", "Method", "Cash and debt at the FY0 year-end"),
            ("sbc_pct", 0, "decimal", "ASSUMPTION", "Method", "0 because da_pct is reported D&A"),
        ]
        write(m3 / f"{t}_dcf_inputs.csv", rows)
        bear = []
        for r in rows:
            r = list(r)
            if r[0] == "growth":
                r[1] = ";".join(f"{g:.4f}" for g in [x / 2 for x in growth[:3]] + [growth[2] / 2 + (g_term - growth[2] / 2) * k / 7 for k in range(1, 8)])
                r[5] = "DRAFT bear: years 1-3 growth halved. Pat replaces or justifies it"
            if r[0] == "ebit_margin":
                r[1], r[5] = ";".join([f"{margin * 0.8:.5f}"] * 10), "DRAFT bear: margin x 0.8"
            bear.append(r)
        write(m3 / f"{t}bear_dcf_inputs.csv", bear)
        pp, vv, shift, price = run(t)
        _, raw, _ = load(t)
        if p:
            b5, vol, cagr, rm, _ = beta_stats(p, t, "2021-10")
            bf, _, _, _, nf = beta_stats(p, t, "1900-01")
        else:
            (b5, bf, nf), vol, cagr, rm = cfg["betas"][t], None, None, None
        at = lambda b: value(replace(pp, wacc=wacc_for(raw, b)))["per_share"]
        _, bv, _, _ = run(t + "bear")
        wy = worst_year(p, t) if p else (risk_tab[t]["worst_calendar_year"], risk_tab[t]["worst_return"])
        a, b = red[(t, "FY0")], red[(t, "FY1")]
        bounds = cfg.get("rf_bounds", {}).get(t)
        if bounds:
            outs = [red_flags(dict(a, long_term_debt=bounds["FY0"][i]), dict(b, long_term_debt=bounds["FY1"][i]), a["cfo"]) for i in (0, 1)]
            pio, pio_n, fails, mscore = outs[0]
            if (outs[0][0], round(outs[0][3], 2)) != (outs[1][0], round(outs[1][3], 2)):
                fails = fails + [f"bounds differ: {outs[1][0]}/{outs[1][1]}, M {outs[1][3]:.2f} at the upper bound"]
        else:
            pio, pio_n, fails, mscore = red_flags(a, b, a["cfo"])
        model_cash = v["operating_income"] * (1 - tax) + v["d_and_a"] - v["capex"]
        rep_cash = v["cfo"] - v["capex"] - v["stock_based_comp"] + (v["interest_expense"] or 0) * (1 - tax)
        da_rep = pp.da_pct[0] + (rep_cash - model_cash) / rev
        up, down = vv["per_share"] / price - 1, bv["per_share"] / price - 1
        res.append(dict(t=t, g=group.get(t, ""), price=price, cur=cur, v1=vv["per_share"], v5=at(b5), vf=at(bf), b5=b5, bf=bf, nf=nf,
                        rep=value(replace(pp, da_pct=(da_rep,) * 10))["per_share"], shift=shift, bear=bv["per_share"], up=up, down=down,
                        ratio="no upside" if up <= 0 else ("no downside" if down >= 0 else f"{up / -down:.2f}"),
                        conv=model_cash / rep_cash, vol=vol, cagr=cagr, rm=rm, sharpe=None if vol is None else (cagr - T_BILL) / vol,
                        wy=wy, maxpos=6000 / -wy[1] if wy[1] < 0 else None, pio=f"{pio}/{pio_n}", fails="; ".join(fails),
                        m="NOT CHECKED (GMI MISSING)" if mscore is None else f"{mscore:.2f}", m12=m12.get(t, "MISSING"),
                        note=cfg["notes"].get(t, "")))
    report(key, cfg, res)


def report(key, cfg, res):
    L = [f"# Round 2 scorecard: {cfg['who']} (TEST preview, {date.today()})", "",
         "Generated by `python tools/round2_team.py " + key + "` with the same method as Pat's nine. Bear cases are a uniform DRAFT "
         "(years 1-3 growth halved, margin x 0.8) for Pat to replace. Values are research estimates, never price targets, returns or position sizes.", "",
         "| Group | Ticker | Price | Value (beta 1.0) | Value / price | At 5-year beta | At full-history beta | On reported cash flow | Price implies (growth shift) | Bear / price | Upside / downside |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        sh = "n/a" if r["shift"] is None else f"{r['shift']:+.1%}"
        L.append(f"| {r['g']} | {r['t']} | {r['price']:,.2f} {r['cur']} | {r['v1']:,.2f} | {r['v1'] / r['price']:.2f} | "
                 f"{r['v5'] / r['price']:.2f} (beta {r['b5']:.2f}) | {r['vf'] / r['price']:.2f} (beta {r['bf']:.2f}, {r['nf']} months) | "
                 f"{r['rep'] / r['price']:.2f} | {sh} | {r['bear'] / r['price']:.2f} | {r['up']:+.0%} / {r['down']:+.0%} = {r['ratio']} |")
    L += ["", "## Tests", "",
          "| Ticker | 1. M12 top 2 and robust | 2. Value > price at beta 1.0, 5-year and full-history beta | 3. Upside/downside >= 1.0 | "
          "4. Piotroski, Beneish | Worst year (max position) | 5-year return a year, volatility, Sharpe | Cash check | Note |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        t2 = "PASS" if min(r["v1"], r["v5"], r["vf"]) > r["price"] else "fail"
        t3 = "PASS" if r["ratio"] == "no downside" or (r["ratio"] != "no upside" and float(r["ratio"]) >= 1) else "fail"
        mp = "no losing year" if r["maxpos"] is None else f"${r['maxpos']:,.0f}"
        L.append(f"| {r['t']} | {r['m12']} | {t2} | {t3} | {r['pio']} (fails: {r['fails'] or 'none'}), {r['m']} | "
                 f"{r['wy'][0]}: {r['wy'][1]:.1%} ({mp}) | "
                 + ("MISSING until the Yahoo CSVs arrive" if r["vol"] is None else f"{r['cagr']:+.1%}, {r['vol']:.0%}, {r['sharpe']:.2f}")
                 + f" | {r['conv']:.2f} | {r['note']} |")
    L += ["", (f"S&P 500 (SPY) compound return over the same window: {res[0]['rm']:+.1%} a year; " if res[0]["rm"] is not None
               else "Betas and worst years are the teammate's own calculations until the Yahoo CSVs arrive; ") + "risk-free 4.00% (3-month T-bill, 30 Oct).",
          "Cash check = model year-0 free cash flow / reported cash flow (CFO - capex - stock-based pay + after-tax interest); above about 1.10 the model is generous."]
    out = ROOT / "outputs" / "round2" / f"Round2_scorecard_{key}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1])
