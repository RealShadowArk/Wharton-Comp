"""TEST stress rerun of Pat's final list after the 5 Nov sell-off.

Values come from the Round 2 DCF inputs (inputs/m03/<T>[bear]_dcf_inputs.csv). Only the price and the
scenario change. Prices are the latest seen in WInS or the 4 Nov red-flag reports (dates in PRICES).
Scenarios (TEST, the same shocks for every company):
  recession: revenue -15%, 0%, +5% in years 1-3, then a linear fade to terminal growth; margin x0.8 in years 1-3
  deep:      revenue -30%, 0%, +5%; margin x0.6 in years 1-3
Run from the repo root: python tools/stress_final_list_2026-11-05.py
"""
import dataclasses, sys
sys.path.insert(0, ".")
from m03.run import load, wacc_for
from m03.dcf import value

FULL_BETA = {"NVDA": 2.05, "ADBE": 1.38, "2454.TW": 1.26, "9961.HK": 1.11, "EEFT": 1.36, "DECK": 0.94,
             "WKL.AS": 0.85, "ADS.DE": 1.20, "SAN.PA": 0.64, "OTEX": 1.17, "005930.KS": 1.22}  # Round 2 scorecards
PRICES = {  # local currency, (price, date and source)
    "NVDA": (203.12, "4 Nov, WInS"), "ADBE": (249.58, "4 Nov, WInS"), "2454.TW": (3715, "4 Nov, WInS"),
    "9961.HK": (43.79 * 6.718, "5 Nov TCOM $43.79 x CNY 6.718 (SAFE 4 Nov)"), "EEFT": (69.70, "5 Nov, WInS"),
    "DECK": (87.44, "5 Nov, Yahoo"), "WKL.AS": (85.44, "3 Nov close"), "ADS.DE": (168.10, "3 Nov close"),
    "SAN.PA": (80.98, "3 Nov close"), "OTEX": (25.76, "3 Nov close"), "005930.KS": (212000, "4 Nov intraday")}

def per_share(t, beta=None, **chg):
    p, raw, _ = load(t)
    if beta is not None:
        p = dataclasses.replace(p, wacc=wacc_for(raw, beta))
    return value(dataclasses.replace(p, **chg))["per_share"]

def shock(t, g123, mk):
    p, raw, _ = load(t); term = float(raw["terminal_growth"])
    g = list(g123) + [g123[-1] + (term - g123[-1]) * k / 7 for k in range(1, 8)]
    return {"growth": tuple(g), "ebit_margin": tuple(x * mk if i < 3 else x for i, x in enumerate(p.ebit_margin))}

rows = []
for t, (px, src) in PRICES.items():
    raw = load(t)[1]
    betas = [1.0, FULL_BETA[t]] + ([] if t == "9961.HK" else [float(raw["beta_measured"])])  # Trip.com 5-yr beta ~0, unusable
    base = [per_share(t, b) / px for b in betas]
    bear = per_share(t + "bear") / px
    rec = [per_share(t, b, **shock(t, (-0.15, 0.0, 0.05), 0.8)) / px for b in betas]
    deep = [per_share(t, b, **shock(t, (-0.30, 0.0, 0.05), 0.6)) / px for b in betas]
    rows.append((t, px, src, base[0], min(base), bear, rec[0], min(rec), deep[0], min(deep)))
print("| Stock | Price used | Base b1 | Base, lowest beta | Bear | Recession b1 | Recession, lowest beta | Deep b1 | Deep, lowest beta |")
print("|---|---|---|---|---|---|---|---|---|")
for t, px, src, b1, bmin, bear, r1, rmin, d1, dmin in rows:
    print(f"| {t} | {px:,.2f} ({src}) | {b1:.2f} | {bmin:.2f} | {bear:.2f} | {r1:.2f} | {rmin:.2f} | {d1:.2f} | {dmin:.2f} |")
