"""ETF tilt review, 16 Oct 2026: look-through sector weights, one-year crash
replays and the M02 stress paths. Run from the repo root: python tools/etf_review.py"""
import csv, sys
sys.path.insert(0, ".")
from structure.plan import scenario_path, floor, reserve_with_margin

ACCOUNT = 300_000
BONDS = 100_704.41          # ladder cost incl. accrued (Bond_Ladder F16)
BOND_COMM = 175.0
PRICES = {"VOO": 707.43, "VXUS": 83.58, "XLI": 167.04, "XLK": 190.43,
          "XLV": 173.96, "XLC": 110.82, "XLF": 54.83}   # WInS 14 Oct (XLF older)
CORE = {"VOO": 35_844, "VXUS": 15_362}
SECTOR_OF = {"XLI": "Industrials", "XLK": "Information Technology",
             "XLV": "Health Care", "XLC": "Communication Services",
             "XLF": "Financials"}
# VOO GICS weights, Vanguard 31 Aug 2026 [V1]
VOO_W = {"Information Technology": .3787, "Financials": .1229,
         "Communication Services": .0950, "Health Care": .0928,
         "Consumer Discretionary": .0914, "Industrials": .0831,
         "Consumer Staples": .0450, "Energy": .0348, "Utilities": .0198,
         "Materials": .0183, "Real Estate": .0180}
OPTIONS = {
    "A locked": {"XLI": .030, "XLK": .024, "XLV": .018, "XLC": .013, "XLF": .015},
    "B reweight": {"XLI": .025, "XLK": .015, "XLV": .030, "XLC": .010, "XLF": .020},
    "C proposed": {"XLI": .030, "XLK": .015, "XLV": .030, "XLC": 0, "XLF": .025}, "FINAL": {"XLI": .030, "XLK": .015, "XLV": .025, "XLC": 0, "XLF": .025},
}
WORST = {"XLI": -.387, "XLK": -.419, "XLV": -.233, "XLC": -.376, "XLF": -.549}
STOCKS = 119_481
# shortlist groups -> GICS sector (equal split is an ASSUMPTION)
STOCK_GROUPS = ["Financials", "Health Care", "Industrials",
                "Information Technology", "Health Care"]


def positions(opt):
    pos = {}
    for t, d in {**CORE, **{k: v * ACCOUNT for k, v in OPTIONS[opt].items()}}.items():
        n = int(d // PRICES[t])
        if n:
            pos[t] = n * PRICES[t]
    return pos


def lookthrough(pos, with_stocks=False):
    s = {k: 0.0 for k in VOO_W}
    for sec, w in VOO_W.items():
        s[sec] += pos["VOO"] * w
    for t, sec in SECTOR_OF.items():
        s[sec] += pos.get(t, 0)
    s["International (VXUS, split not collected)"] = pos["VXUS"]
    if with_stocks:
        for sec in STOCK_GROUPS:
            s[sec] += STOCKS / len(STOCK_GROUPS)
    return s


print("== Positions ==")
for o in OPTIONS:
    p = positions(o)
    cost = sum(p.values())
    print(o, {k: round(v) for k, v in p.items()}, "ETF total", round(cost),
          "cash left", round(ACCOUNT - BONDS - BOND_COMM - cost - 25 * len(p)))
    for t, w in OPTIONS[o].items():
        if w:
            print(f"   2% rule {t}: {w*abs(WORST[t])*100:.2f}% of portfolio")

print("\n== Look-through, ETFs only (% of ETF money | % of $300k) and VOO market weight ==")
for o in OPTIONS:
    p = positions(o); lt = lookthrough(p); tot = sum(p.values())
    us = tot - p["VXUS"]
    print("--", o, "ETF money", round(tot), "US ETF money", round(us))
    print("   US-only shares vs S&P 500:", {k[:12]: f"{lt[k]/us*100:.1f} vs {VOO_W[k]*100:.1f}" for k in list(VOO_W)[:6]})
    for k, v in sorted(lt.items(), key=lambda x: -x[1]):
        mk = VOO_W.get(k)
        print(f"  {k:45s} ${v:9,.0f} {v/tot*100:5.1f}% {v/ACCOUNT*100:5.2f}%"
              + (f"   market {mk*100:4.1f}%  ratio {v/tot/mk:4.2f}x" if mk else ""))

print("\n== Look-through incl. stock sleeve, equal split ASSUMPTION (% of all stock money | % of $300k) ==")
for o in OPTIONS:
    p = positions(o); lt = lookthrough(p, True); tot = sum(p.values()) + STOCKS
    print("--", o)
    for k, v in sorted(lt.items(), key=lambda x: -x[1])[:7]:
        print(f"  {k:45s} ${v:9,.0f} {v/tot*100:5.1f}% {v/ACCOUNT*100:5.2f}%")

# one-year replays. Sources: IVV/IXUS NAV (core research), MSCI ACWI ex USA
# IMI 2008 (secondary), sector SPDR NAV calendar returns (industry research);
# ALL-WORST = each fund's own worst year at once (TEST).
R = {
    "2008": {"VOO": -.3694, "VXUS": -.460, "XLI": -.3892, "XLK": -.4142,
             "XLV": -.2315, "XLC": None, "XLF": -.5527},
    "2018": {"VOO": -.0443, "VXUS": -.1454, "XLI": -.1310, "XLK": -.0156,
             "XLV": .0630, "XLC": None, "XLF": -.1309},
    "2020": {"VOO": .1840, "VXUS": .1114, "XLI": .1100, "XLK": .4367,
             "XLV": .1333, "XLC": .2685, "XLF": -.0168},
    "2022": {"VOO": -.1813, "VXUS": -.1635, "XLI": -.0555, "XLK": -.2771,
             "XLV": -.0204, "XLC": -.3764, "XLF": -.1056},
    "ALL-WORST": {"VOO": -.3694, "VXUS": -.460, **WORST},
}
print("\n== One-year replays: gain/loss in $ and % of $300k (bonds and cash held flat) ==")
for o in OPTIONS:
    p = positions(o)
    print("--", o)
    for y, r in R.items():
        known = sum(v * r[t] for t, v in p.items() if r.get(t) is not None)
        tilts = sum(v * r[t] for t, v in p.items() if t in SECTOR_OF and r.get(t) is not None)
        miss = [t for t in p if r.get(t) is None]
        # after stocks are bought: each stock group earns its sector fund's return (proxy)
        stock_r = None
        if all(r.get(t) is not None for t in ("XLI", "XLK", "XLV", "XLF")):
            proxy = {"Financials": r["XLF"], "Health Care": r["XLV"],
                     "Industrials": r["XLI"], "Information Technology": r["XLK"]}
            stock_r = sum(STOCKS / 5 * proxy[s] for s in STOCK_GROUPS)
        extra = f" missing {miss}" if miss else ""
        print(f"  {y:9s} ETFs ${known:9,.0f} ({known/ACCOUNT*100:5.1f}%)  tilts only ${tilts:8,.0f}"
              f" ({tilts/ACCOUNT*100:4.2f}%)"
              + (f"  | +stocks(proxy) ${known+stock_r:9,.0f} ({(known+stock_r)/ACCOUNT*100:5.1f}%)" if stock_r is not None else "")
              + extra)

# bond ladder mark-to-market for parallel yield shifts (ASSUMPTION: funds
# modelled as par bonds maturing 15 Dec of their year)
from datetime import date
T0 = date(2026, 10, 8)
LADDER = [  # (cost, coupon, maturity, ytm)
    (12775.41, .049, date(2032, 12, 15), .049), (12147.60, .05, date(2033, 12, 15), .05),
    (11534.38, .05, date(2034, 12, 15), .05), (10884.72, .051, date(2035, 12, 15), .051),
    (10292.94, .0515, date(2036, 12, 15), .0515), (9690.67, .0475, date(2037, 2, 15), .05228),
    (9399.12, .045, date(2038, 5, 15), .053), (8275.17, .04375, date(2039, 11, 15), .05428),
    (8066.84, .0425, date(2040, 11, 15), .05488), (7637.56, .03125, date(2041, 11, 15), .05583)]


def price(c, mat, y):
    t = (mat - T0).days / 365.25
    n = int(t * 2) + 1
    times = [t - 0.5 * k for k in range(n) if t - 0.5 * k > 0]
    return sum((c / 2) / (1 + y / 2) ** (2 * s) for s in times) + 1 / (1 + y / 2) ** (2 * t)


print("\n== Bond ladder market value for an immediate parallel yield shift ==")
for dy in (-0.015, -0.01, 0.01, 0.025):
    v = sum(cost * price(c, m, y + dy) / price(c, m, y) for cost, c, m, y in LADDER)
    print(f"  {dy*100:+.1f} pts: ${v:,.0f} ({(v/BONDS-1)*100:+.1f}%, {(v-BONDS)/ACCOUNT*100:+.2f}% of $300k)")

# M02 stress paths through Option 3 (whole plan, case cash flows)
paths = {}
for row in csv.DictReader(open("inputs/M02_assumptions.csv")):
    if row["assumption_id"].startswith("SCN-S") and row["asset_id"] == "growth_core":
        paths.setdefault(row["scenario_id"], {})[int(row["measure"][-4:])] = float(row["value"])
reserve = reserve_with_margin(0.0524, 0.0)
print(f"\n== Option 3, M02 paths S1-S8 (reserve needed at start of 2033: ${reserve:,.0f}) ==")
for s in sorted(paths):
    ret = [paths[s][y] for y in range(2027, 2033)]
    w = scenario_path(ret, 0.0524, 0.0, 2, 1.0)
    print(f"  {s}: wealth 2033 ${w[-1]:,.0f}  above reserve ${w[-1]-reserve:,.0f}  "
          f"covered={'yes' if w[-1] >= reserve - 1 else 'NO'}")
