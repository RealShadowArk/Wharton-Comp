"""Value tests for balance-sheet businesses (17-19 Nov 2026; extension of M03, TEST).

FCFF at WACC does not fit insurers or REITs, so (student judgments, docs/refined_screen_rules.md):
- RI method (insurers, banks): value = book value per share + PV of residual income
  (ROE - cost of equity) x opening book value. ROE starts at the 3-year average and fades
  linearly to the cost of equity by year 10 (no excess return after that). Book value
  grows by retained earnings (1 - 3-year average payout).
- FFO method (REITs): AFFO per diluted share (FFO if AFFO is MISSING) is the cash flow to
  shareholders. Years 1-3 grow at consensus revenue growth, then fade to 3% by year 10,
  plus a terminal value at the cost of equity.
Cost of equity = 4.94% (US 10-year, 30 Oct) + beta x 5%, at beta 1.0, the 5-year beta and the
full-history beta (vs SPY, from the teammate's Yahoo files). Terminal growth 3%.
Bear (uniform DRAFT, as for the DCFs): ROE x 0.8; AFFO x 0.8 with years 1-3 growth halved.
Same tests as Round 2: value above price at all three betas; upside/downside at least 1.0.

    python tools/value_financials.py pkg3
"""
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import round2_team as r2  # noqa: E402

RF, ERP, G = 0.0494, 0.05, 0.03
SETS = {"pkg3": dict(workbook=r2.SETS["pkg3"]["workbook"], yahoo=r2.SETS["pkg3"]["yahoo"],
                     who="Universe package 3 (RI and FFO methods)",
                     # Part A top-ups (19 Nov): Kimco publishes FAD (its AFFO-type measure), not AFFO; Realty Income year-1 consensus
                     affo_override={"KIM": (1.26, "FAD per diluted share FY2025 (Kimco's AFFO-type measure, Q4 2025 supplement p. 9)")},
                     g1_override={"O": (0.091, "FY2026 consensus +9.1% (QDD Research, 19 Nov; Part A top-ups)")}),
        "utilities": dict(  # TEST preview for Pat's option (b): residual income for regulated utilities
            workbook=ROOT / "context/teammates_2026-11-19/partB/Wharton_Package_5_Part_B_Round_2.xlsx",
            yahoo=ROOT / "context/teammates_2026-11-19/partB/yahoo_monthly", kind="utility",
            tickers=["PEG", "EXC", "ED", "ATO", "AEP"], px30={**{t: r2.PX_30OCT[t] for t in ("PEG", "EXC", "ED")}},
            who="Regulated utilities, residual income (TEST preview for option b)")}


def long_block(wb):
    rows = list(wb["Valuation inputs"].iter_rows(values_only=True))
    i = next(k for k, r in enumerate(rows) if r[0] == "Ticker" and r[1] == "Method")
    d = defaultdict(dict)
    for r in rows[i + 1:]:
        if r[0] and r[2]:
            d[r[0]][(r[2], str(r[3]))] = r[4]
    return d


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def ri_value(bv0, roe, payout, ke, years=10):
    bv, total = bv0, bv0
    for t in range(1, years + 1):
        roe_t = roe + (ke - roe) * (t - 1) / (years - 1)
        total += (roe_t - ke) * bv / (1 + ke) ** t
        bv *= 1 + roe_t * max(0.0, 1 - payout)
    return total


def ffo_value(cf0, g123, ke):
    gs = list(g123) + [g123[2] + (G - g123[2]) * k / 7 for k in range(1, 8)]
    cf, total = cf0, 0.0
    for t, g in enumerate(gs, 1):
        cf *= 1 + g
        total += cf / (1 + ke) ** t
    return total + cf * (1 + G) / (ke - G) / (1 + ke) ** len(gs)


def utility(key):
    """Residual income for regulated utilities: same as the insurer RI method, from the Part B long block.
    ROE = 3-year average of net income / average common equity; payout = dividends per share x current
    diluted shares / net income (ASSUMPTION: today's share count); book value per share at 30 Sep 2026."""
    cfg = SETS[key]
    wb = openpyxl.load_workbook(cfg["workbook"], data_only=True)
    rows = list(wb["Valuation inputs"].iter_rows(values_only=True))
    head = rows[0]
    val = {r[1]: dict(zip(head, r)) for r in rows[1:] if r[1] in cfg["tickers"] and isinstance(r[5], (int, float))}
    i = next(k for k, r in enumerate(rows) if r[0] == "Ticker" and r[1] == "Method")
    lb = defaultdict(list)
    for r in rows[i + 1:]:
        if r[0] in cfg["tickers"] and r[2]:
            lb[r[0]].append((str(r[2]), str(r[3]), r[4]))
    p = r2.monthly(Path(cfg["yahoo"]), cfg["tickers"])
    year = lambda per: int(next(x for x in str(per).replace("FY", " ").replace("-", " ").split() if len(x) == 4 and x.isdigit()))
    out = []
    for t in cfg["tickers"]:
        v, items = val[t], lb[t]
        pick = lambda pre: {year(per): num(x) for m, per, x in items if m.startswith(pre) and num(x) is not None}
        ni, eq, dps = pick("Net income to common"), pick("Common equity"), pick("Dividends")
        bv0 = next(num(x) for m, per, x in items if m.startswith("Book value per"))
        ys = sorted(ni)[-3:]
        roes = [ni[y] / ((eq[y - 1] + eq[y]) / 2) for y in ys]
        sh = num(v["diluted_shares_m"])
        pays = [dps[y] * sh / ni[y] for y in ys]
        roe, payout = sum(roes) / 3, sum(pays) / 3
        allowed = sorted(num(x) for m, per, x in items if "llowed" in m and num(x) is not None)
        b5 = r2.beta_stats(p, t, "2021-10")[0]
        bf, _, _, _, nf = r2.beta_stats(p, t, "1900-01")
        wy = r2.worst_year(p, t)
        vals = {b: ri_value(bv0, roe, payout, RF + b * ERP) for b in (1.0, b5, bf)}
        bear = ri_value(bv0, roe * 0.8, payout, RF + ERP)
        px30 = cfg["px30"].get(t) or num(v.get("price_30oct_close"))
        for label, price in (("30 Oct", px30), ("19 Nov WInS", num(v["wins_price_usd"]))):
            r = [vals[b] / price for b in (1.0, b5, bf)]
            up, down = vals[1.0] / price - 1, bear / price - 1
            ud = "no downside" if down >= 0 else ("no upside" if up <= 0 else f"{up / -down:.2f}")
            ok = all(x > 1 for x in r) and (ud == "no downside" or (ud != "no upside" and float(ud) >= 1))
            out.append(dict(t=t, method="RI (utility)", when=label, price=price, v1=vals[1.0], r=r, b5=b5, bf=bf, nf=nf, bear=bear / price, ud=ud, ok=ok, wy=wy,
                            basis=(f"book value {bv0:.2f} (30 Sep 2026, {price / bv0:.2f}x book), ROE {roe:.1%} (FY{ys[0]}-FY{ys[-1]}: {', '.join(f'{x:.1%}' for x in roes)}), "
                                   f"payout {payout:.0%}, allowed ROE {allowed[0]:.2%}-{allowed[-1]:.2%}"), notes=""))
    write_report(key, cfg, out, "Residual income on book value, as for the insurers (TEST preview for Pat's option b, not adopted). "
                 "Cost of equity = 4.94% + beta x 5%; at beta 1.0 it is 9.94%, about the allowed returns, so value is close to book value.")


def main(key):
    cfg = SETS[key]
    if cfg.get("kind") == "utility":
        return utility(key)
    wb = openpyxl.load_workbook(cfg["workbook"], data_only=True)
    vr = [r for r in wb["Valuation inputs"].iter_rows(values_only=True)]
    head = vr[0]
    val = {r[1]: dict(zip(head, r)) for r in vr[1:] if r[1] and r[0] in ("RI method", "FFO method")}
    lb = long_block(wb)
    p = r2.monthly(Path(cfg["yahoo"]), list(val))
    out = []
    for t, v in val.items():
        m = lb[t]
        b5 = r2.beta_stats(p, t, "2021-10")[0]
        bf, _, _, _, nf = r2.beta_stats(p, t, "1900-01")
        wy = r2.worst_year(p, t)
        notes = []
        if v["peer_group"] == "RI method":
            roes = [num(m.get(("Return on average common equity", f"FY{y}"))) for y in (2023, 2024, 2025)]
            roe = sum(roes) / 3
            bv0 = num(m.get(("Book value per share", "2026-09-30")))
            sh = num(v["diluted_shares_m"]) or num(v["shares_outstanding_m"])
            if not num(v["diluted_shares_m"]):
                notes.append("diluted shares MISSING: shares outstanding used for EPS")
            pays = []
            for y in (2023, 2024, 2025):
                ni, dps = num(m.get(("Net income to common", f"FY{y}"))), num(m.get(("Dividends per share", f"FY{y}")))
                pays.append(dps / (ni / sh))
            payout = sum(pays) / 3
            f = lambda b, k=1.0: ri_value(bv0, roe * k, payout, RF + b * ERP)
            basis = f"book value {bv0:.2f} (30 Sep 2026), ROE {roe:.1%} (3-year average: {', '.join(f'{x:.1%}' for x in roes)}), payout {payout:.0%}"
            vals = {b: f(b) for b in (1.0, b5, bf)}
            bear = f(1.0, 0.8)
        else:
            affo = num(m.get(("Affo per diluted share", "FY2025")))
            if t in cfg.get("affo_override", {}):
                affo, why = cfg["affo_override"][t]
                notes.append(why)
            if affo is None:
                affo = num(m.get(("Ffo per diluted share", "FY2025")))
                notes.append("AFFO MISSING: FFO per share used, which overstates cash (no maintenance capex)")
            g = [num(v[f"consensus_revenue_growth_y{k}"]) for k in (1, 2, 3)]
            if t in cfg.get("g1_override", {}):
                g[0], why = cfg["g1_override"][t]
                notes.append(why)
            if g[0] is None:
                g[0] = g[1]
                notes.append("year-1 consensus MISSING: year-2 consensus used")
            f = lambda b, k=1.0, h=1.0: ffo_value(affo * k, [x * h for x in g], RF + b * ERP)
            basis = f"AFFO/share {affo:.2f} (FY2025), growth {', '.join(f'{x:+.1%}' for x in g)} then fade to 3%"
            vals = {b: f(b) for b in (1.0, b5, bf)}
            bear = f(1.0, 0.8, 0.5)
        for label, price in (("30 Oct", num(v["price_30oct"])), ("19 Nov", num(v["collection_date_price_usd"]))):
            r = [vals[b] / price for b in (1.0, b5, bf)]
            up, down = vals[1.0] / price - 1, bear / price - 1
            ud = "no downside" if down >= 0 else ("no upside" if up <= 0 else f"{up / -down:.2f}")
            ok = all(x > 1 for x in r) and (ud == "no downside" or (ud != "no upside" and float(ud) >= 1))
            out.append(dict(t=t, method=v["peer_group"], when=label, price=price, v1=vals[1.0], r=r, b5=b5, bf=bf, nf=nf,
                            bear=bear / price, ud=ud, ok=ok, wy=wy, basis=basis, notes="; ".join(notes)))
    write_report(key, cfg, out, "Piotroski and Beneish are not applied: their tests (current ratio, gross margin, asset quality) do not fit insurers or REITs.")


def write_report(key, cfg, out, extra):
    L = [f"# Round 2 scorecard: {cfg['who']} (TEST preview, {date.today()})", "",
         "Generated by `python tools/value_financials.py " + key + "`. Methods and defaults: module docstring and "
         "`docs/refined_screen_rules.md`. Values are research estimates, never price targets, returns or position sizes. " + extra, "",
         "| Ticker | Method | Price | Value (beta 1.0) | Value / price at beta 1.0, 5-year, full | Bear / price | Upside / downside | Value tests | Worst year (max position) | Basis |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for o in out:
        L.append(f"| {o['t']} | {o['method']} | {o['price']:.2f} ({o['when']}) | {o['v1']:.2f} | "
                 f"{o['r'][0]:.2f}, {o['r'][1]:.2f} (beta {o['b5']:.2f}), {o['r'][2]:.2f} (beta {o['bf']:.2f}, {o['nf']} months) | "
                 f"{o['bear']:.2f} | {o['ud']} | {'PASS' if o['ok'] else 'fail'} | {o['wy'][0]}: {o['wy'][1]:.1%} "
                 f"(${6000 / -o['wy'][1]:,.0f}) | {o['basis']}{'; ' + o['notes'] if o['notes'] else ''} |")
    path = ROOT / "outputs" / "round2" / f"Round2_scorecard_{key}_financials.md"
    path.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1])
