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
                     who="Universe package 3 (RI and FFO methods)")}


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


def main(key):
    cfg = SETS[key]
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
            if affo is None:
                affo = num(m.get(("Ffo per diluted share", "FY2025")))
                notes.append("AFFO MISSING: FFO per share used, which overstates cash (no maintenance capex)")
            g = [num(v[f"consensus_revenue_growth_y{k}"]) for k in (1, 2, 3)]
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
    L = [f"# Round 2 scorecard: {cfg['who']} (TEST preview, {date.today()})", "",
         "Generated by `python tools/value_financials.py " + key + "`. Methods and defaults: module docstring and "
         "`docs/refined_screen_rules.md`. Values are research estimates, never price targets, returns or position sizes. "
         "Piotroski and Beneish are not applied: their tests (current ratio, gross margin, asset quality) do not fit insurers or REITs.", "",
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
