"""TEST reruns prompted by the 4 Nov macro and red-flag reports (Amdocs guidance, Wolters Kluwer disposal gain, Trip.com cash check).

Run from the repo root: python tools/retest_redflags_2026-11-04.py. Results are TEST values for Pat to review, not official outputs."""
import sys, dataclasses, re, openpyxl
sys.path.insert(0, ".")
from m03.run import load, wacc_for
from m03.dcf import value
def ps(t, beta=None, **chg):
    p, raw, rows = load(t)
    if beta is not None: p = dataclasses.replace(p, wacc=wacc_for(raw, beta))
    return value(dataclasses.replace(p, **chg))["per_share"], raw
def full_beta(t, sc):
    for line in open(sc):
        if line.startswith(f"| {t} "): return line
    return ""
# ---- Amdocs: FY2027 guidance (3 Nov) revenue -14.3% to -17.9% reported -> midpoint -16.1%
for t in ("DOX", "DOXbear"):
    p, raw, _ = load(t); g = list(p.growth); m = list(p.ebit_margin)
    b5 = float(load("DOX")[1]["beta_measured"])
    for label, chg in [("as run (old year 1 %.1f%%)" % (g[0]*100), {}),
                       ("year 1 = -16.1%", {"growth": tuple([-0.161] + g[1:]) if t == "DOX" else tuple([-0.161/2] + g[1:])}),
                       ("year 1 = -16.1%, margin x 19.5/21.6", {"growth": tuple([-0.161] + g[1:]) if t == "DOX" else tuple([-0.161/2] + g[1:]),
                                                               "ebit_margin": tuple(x * 19.5 / 21.6 for x in m)})]:
        v1, _ = ps(t, **chg); v5, _ = ps(t, beta=b5, **chg)
        print(f"{t:8s} {label:38s} value b1 ${v1:6.2f} (x{v1/62.83:.2f} at $62.83, x{v1/34.58:.2f} at $34.58) | 5y beta ${v5:6.2f} (x{v5/62.83:.2f} / x{v5/34.58:.2f})")
# ---- Wolters Kluwer: FY2025 IFRS operating profit 1,735 includes a 232 FRR disposal gain
for t in ("WKL.AS", "WKL.ASbear"):
    p, raw, _ = load(t); m = list(p.ebit_margin); base = float(raw["base_revenue"])
    b5 = float(load("WKL.AS")[1]["beta_measured"])
    new = tuple(x * (1735 - 232) / 1735 for x in m)
    for label, chg in [("as run", {}), ("ex 232 gain", {"ebit_margin": new})]:
        v1, _ = ps(t, **chg); v5, _ = ps(t, beta=b5, **chg)
        print(f"{t:10s} {label:12s} margin {(chg.get('ebit_margin') or m)[0]:.4f} value b1 EUR {v1:6.2f} (x{v1/87.00:.2f}) | 5y beta EUR {v5:6.2f} (x{v5/87.00:.2f})")
# ---- Trip.com cash check: Valuation inputs CFO 19,625 is FY2024; FY2025 is 14,379
wb = openpyxl.load_workbook("context/teammates_2026-11-03/akshat_final/Akshat_Round2_updated.xlsx", data_only=True)
rows = list(wb["Valuation inputs"].iter_rows(values_only=True)); h = rows[0]
v = next(dict(zip(h, r)) for r in rows[1:] if r and r[h.index("ticker")] == "9961.HK")
p, raw, _ = load("9961.HK"); tax = float(raw["tax_rate"])
rep = lambda cfo: cfo - v["capex"] - (v["stock_based_comp"] or 0) + (v["interest_expense"] or 0) * (1 - tax)
print("TCOM fields:", {k: v[k] for k in ("cfo", "capex", "stock_based_comp", "interest_expense")}, "tax", tax)
print(f"TCOM reported-cash base: old {rep(19625):,.0f}  new {rep(14379):,.0f}; cash check 0.80 -> {0.80*rep(19625)/rep(14379):.2f} (from the rounded 0.80)")
print("---- full-history betas")
p, raw, _ = load("DOX"); g = list(p.growth); m = list(p.ebit_margin)
pb, rawb, _ = load("DOXbear"); gb = list(pb.growth); mb = list(pb.ebit_margin)
for label, chg, chgb in [("year 1 -16.1%", {"growth": tuple([-0.161] + g[1:])}, {"growth": tuple([-0.161/2] + gb[1:])}),
                         ("year 1 -16.1%, margin cut", {"growth": tuple([-0.161] + g[1:]), "ebit_margin": tuple(x*19.5/21.6 for x in m)},
                          {"growth": tuple([-0.161/2] + gb[1:]), "ebit_margin": tuple(x*19.5/21.6 for x in mb)})]:
    v, _ = ps("DOX", beta=1.16, **chg); vb, _ = ps("DOXbear", **chgb)
    print(f"DOX {label}: full beta 1.16 ${v:.2f} (x{v/62.83:.2f} / x{v/34.58:.2f}); bear b1 ${vb:.2f}")
v, _ = ps("WKL.AS", beta=0.85, ebit_margin=tuple(x*1503/1735 for x in load("WKL.AS")[0].ebit_margin))
print(f"WKL ex gain full beta 0.85: EUR {v:.2f} (x{v/87:.2f})")
# WKL upside/downside ex gain (beta 1.0)
v1, _ = ps("WKL.AS", ebit_margin=tuple(x*1503/1735 for x in load("WKL.AS")[0].ebit_margin))
vb, _ = ps("WKL.ASbear", ebit_margin=tuple(x*1503/1735 for x in load("WKL.ASbear")[0].ebit_margin))
print(f"WKL ex gain upside/downside: +{v1/87-1:.0%} / -{1-vb/87:.0%} = {(v1/87-1)/(1-vb/87):.2f}")
print(f"TCOM SAMR penalty per share: RMB {5180/690.208:.2f} vs price 265.17 ({5180/690.208/265.17:.1%})")
print("---- Reckitt: FY2025 operating income 4,217 includes the 1,245 Essential Home disposal gain (teammate's own note)")
f = (4217 - 1245) / 4217
pr, rawr, _ = load("RKT.L"); b5r = float(rawr["beta_measured"])
rows_ = []
for label, k in (("as run", 1.0), ("ex 1,245 gain", f)):
    v1, _ = ps("RKT.L", ebit_margin=tuple(x * k for x in load("RKT.L")[0].ebit_margin))
    v5, _ = ps("RKT.L", beta=b5r, ebit_margin=tuple(x * k for x in load("RKT.L")[0].ebit_margin))
    vf, _ = ps("RKT.L", beta=0.51, ebit_margin=tuple(x * k for x in load("RKT.L")[0].ebit_margin))
    vb, _ = ps("RKT.Lbear", ebit_margin=tuple(x * k for x in load("RKT.Lbear")[0].ebit_margin))
    up, dn = v1 / 54.08 - 1, 1 - vb / 54.08
    print(f"RKT {label:14s} margin {load('RKT.L')[0].ebit_margin[0]*k:.4f}: b1 GBP {v1:.2f} (x{v1/54.08:.2f}) | 5y x{v5/54.08:.2f} | full 0.51 x{vf/54.08:.2f} | bear x{vb/54.08:.2f} | up/down {up:+.0%}/{-dn:+.0%}" + (f" = {up/dn:.2f}" if dn > 0 else " = no downside"))
