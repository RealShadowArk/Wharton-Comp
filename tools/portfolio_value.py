"""Value the frozen WInS portfolio (6 Nov 2026) at newer prices.

    python tools/portfolio_value.py                     # 6 Nov WInS prices (check: reproduces the freeze)
    python tools/portfolio_value.py --prices p.csv      # manual prices: columns id,price (TWD for 2454; per $1000 face for bonds)
    python tools/portfolio_value.py --yahoo --fred      # live: Yahoo closes + FRED yields (needs the wharton-comp environment)

Holdings: inputs/portfolio/holdings_2026-11-06.csv (WInS positions at the freeze).
The portfolio is frozen for the competition, so this is tracking only (TEST).
Bonds without a price are repriced from the change in FRED's 10- and 20-year
Treasury yields since 6 Nov (--fred), or held at their 6 Nov price (STALE).
"""
import argparse
import csv
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOLDINGS = ROOT / "inputs/portfolio/holdings_2026-11-06.csv"
START = 300_000.0          # CASE: WInS account at the start
TWD_6NOV = 33.097          # RESEARCH: backed out of WInS 6 Nov (110 x 3,390 / $11,266.84)
TWD_COST = 32.833          # RESEARCH: WInS rate at the MediaTek fill (4-5 Nov)
FREEZE = date(2026, 11, 6)
UA = {"User-Agent": "wharton-comp portfolio tracker"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return r.read().decode()


def yahoo(symbol):
    meta = json.loads(get("https://query1.finance.yahoo.com/v8/finance/chart/"
                          f"{symbol}?range=5d&interval=1d"))["chart"]["result"][0]["meta"]
    return float(meta["regularMarketPrice"])


def fred_change(series):
    """Latest value minus the 6 Nov value (percentage points)."""
    rows = [r.split(",") for r in get(
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}").splitlines()[1:]]
    rows = [(date.fromisoformat(d), float(v)) for d, v in rows if v not in ("", ".")]
    at_freeze = [v for d, v in rows if d <= FREEZE][-1]
    return rows[-1][1] - at_freeze, rows[-1][0]


def bond_price(coupon, maturity, y, today):
    """Clean-ish price per 100 face: semiannual coupons, fractional first period."""
    n_years = (maturity - today).days / 365.25
    periods = n_years * 2
    k = int(periods)
    frac = periods - k
    pv = sum(coupon / 2 / (1 + y / 2) ** (frac + i) for i in range(k + 1))
    return pv + 100 / (1 + y / 2) ** periods


def solve_yield(coupon, maturity, price, today):
    lo, hi = 0.0, 0.2
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if bond_price(coupon, maturity, mid, today) > price else (lo, mid)
    return (lo + hi) / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices")
    ap.add_argument("--yahoo", action="store_true")
    ap.add_argument("--fred", action="store_true")
    ap.add_argument("--twd", type=float, help="TWD per USD (default: Yahoo with --yahoo, else 6 Nov)")
    a = ap.parse_args()

    rows = list(csv.DictReader(HOLDINGS.open()))
    manual = {}
    if a.prices:
        manual = {r["id"]: float(r["price"]) for r in csv.DictReader(open(a.prices))}
    twd = a.twd or (yahoo("TWD=X") if a.yahoo else TWD_6NOV)
    d10 = d20 = 0.0
    if a.fred:
        (d10, asof), (d20, _) = fred_change("DGS10"), fred_change("DGS20")
        print(f"FRED yield change since 6 Nov to {asof}: 10y {d10:+.2f}, 20y {d20:+.2f} points")

    total = cost_total = 0.0
    groups = {}
    print(f"{'id':20s} {'qty':>6s} {'price':>10s} {'value $':>11s} {'P/L %':>7s}  source")
    for r in rows:
        qty, p6, paid = float(r["qty"]), float(r["price_6nov"]), float(r["price_paid"])
        src = "6 Nov WInS"
        if r["id"] in manual:
            price, src = manual[r["id"]], "manual"
        elif a.yahoo and r["yahoo"]:
            price, src = yahoo(r["yahoo"]), "Yahoo"
        elif r["id"].startswith("T") and a.fred:
            cpn, mat = float(r["id"][1:6]), date.fromisoformat(r["id"][7:17])
            y6 = solve_yield(cpn, mat, p6 / 10, FREEZE)
            w = min(max(((mat - date.today()).days / 365.25 - 10) / 10, 0), 1)
            price = 10 * bond_price(cpn, mat, y6 + ((1 - w) * d10 + w * d20) / 100, date.today())
            src = "FRED reprice (TEST)"
        else:
            price = p6
            if src == "6 Nov WInS" and (a.yahoo or a.prices):
                src = "STALE (6 Nov)"
        fx = twd if r["currency"] == "TWD" else 1.0
        fx_cost = TWD_COST if r["currency"] == "TWD" else 1.0
        value, cost = qty * price / fx, qty * paid / fx_cost
        total += value
        cost_total += cost
        groups[r["group"]] = groups.get(r["group"], 0.0) + value
        pl = (value / cost - 1) * 100 if r["group"] != "Cash" else 0.0
        print(f"{r['id']:20s} {qty:6.0f} {price:10.2f} {value:11,.2f} {pl:+6.1f}%  {src}")

    print("\nBy group:")
    for g, v in sorted(groups.items(), key=lambda kv: -kv[1]):
        print(f"  {g:15s} {v:11,.0f}  {v / total:6.1%}")
    print(f"\nTotal value ${total:,.2f}   vs $300,000 start: {total / START - 1:+.2%}"
          f"   (TWD {twd:.3f} per USD; cash is an estimate until confirmed)")


if __name__ == "__main__":
    sys.exit(main())
