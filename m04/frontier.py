"""Efficient frontier and resampled (Michaud) frontier: a DIAGNOSTIC for where our mix sits (20 Nov 2026, TEST).

    python -m m04.frontier          # needs numpy and scipy; writes outputs/m04/

Not used to resize anything: the stock/bond split comes from the floor rule (IPS), and backtests do not
prove future outcomes. Student judgments (Claude's defaults, Pat to confirm):
- Building blocks (monthly USD total returns, Yahoo adjusted closes in inputs/m04/yahoo_monthly/, RESEARCH):
  VOO, VXUS, the four sector tilts (XLI, XLK, XLV, XLF), "Our stocks" (the ten WInS stocks at their 6 Nov
  market-value weights, rebalanced monthly; MediaTek converted with Yahoo TWD=X), IEF as a stand-in for the
  Treasury ladder (ASSUMPTION: a held-to-maturity ladder is less volatile than IEF's market price), BIL for T-bills.
- Our mix = the IPS target: bonds 33.6%, core 17.1% (VOO 70% / VXUS 30%), tilts 9.5% (XLI 3.0, XLK 1.5, XLV 2.5,
  XLF 2.5), individual stocks 39.8% (structure model v4, CLAUDE.md). Growth sleeve = the same without bonds.
- Long-only, fully invested. Annual mean = 12 x monthly mean; covariance = 12 x monthly covariance.
- Windows: 60 months (Nov 2021-Oct 2026, our beta window) and 120 months (Nov 2016-Oct 2026). The Great Depression
  split does not apply: ETF data start in 1998-2011.
- Resampled frontier (Michaud): 200 bootstrap resamples of the months; for each, the frontier at 25 points by
  return rank; weights averaged by rank and evaluated with the full-sample estimates. Risk-free rate 4.00%
  (3-month T-bill, 30 Oct, RESEARCH) for Sharpe ratios.
"""
import csv
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "inputs" / "m04" / "yahoo_monthly"
OUT = ROOT / "outputs" / "m04"
RF = 0.04
SEED = 20261120
B, POINTS = 200, 25
ASSETS = ["VOO", "VXUS", "XLI", "XLK", "XLV", "XLF", "Our stocks", "IEF", "BIL"]
GROWTH = ASSETS[:7]
MIX = {"VOO": 0.171 * 0.7, "VXUS": 0.171 * 0.3, "XLI": 0.030, "XLK": 0.015, "XLV": 0.025, "XLF": 0.025,
       "Our stocks": 0.398, "IEF": 0.336, "BIL": 0.0}
STOCKS = {"NVDA": 35 * 188.10, "2454.TW": 110 * 3390 / 32.0, "ADBE": 46 * 241.86, "WTKWY": 148 * 100.53, "OTEX": 288 * 25.43,
          "TCOM": 233 * 44.60, "EEFT": 131 * 71.45, "DECK": 97 * 87.04, "ADDYY": 119 * 97.21, "SNY": 250 * 46.59}
# 6 Nov WInS quantities x prices (inputs/portfolio/holdings_2026-11-06.csv); MediaTek at about 32 TWD per USD
WINDOWS = {"60 months (Nov 2021-Oct 2026)": "2021-10", "120 months (Nov 2016-Oct 2026)": "2016-10"}


def series(sym):
    out = {}
    for r in csv.DictReader(open(DATA / f"{sym}.csv")):
        if r["Date"].endswith("-01") and r["Adj Close"] not in ("", "None", "null") and r["Date"][:7] <= "2026-10":
            out[r["Date"][:7]] = float(r["Adj Close"])
    return out


def returns(start):
    months = sorted(m for m in series("SPY") if m >= start)
    px = {s: series(s) for s in ["VOO", "VXUS", "XLI", "XLK", "XLV", "XLF", "IEF", "BIL"] + list(STOCKS)}
    fx = series("TWD=X")
    px["2454.TW"] = {m: v / fx[m] for m, v in px["2454.TW"].items() if m in fx}  # USD price
    wts = {s: v / sum(STOCKS.values()) for s, v in STOCKS.items()}
    rows = []
    for a, b in zip(months, months[1:]):
        r = [px[s][b] / px[s][a] - 1 for s in ASSETS[:6]]
        live = [s for s in STOCKS if a in px[s] and b in px[s]]
        r.append(sum(wts[s] * (px[s][b] / px[s][a] - 1) for s in live) / sum(wts[s] for s in live))
        r += [px[s][b] / px[s][a] - 1 for s in ("IEF", "BIL")]
        rows.append(r)
    return np.array(rows)


def min_var(mu, cov, target=None):
    n = len(mu)
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}]
    if target is not None:
        cons.append({"type": "eq", "fun": lambda w: w @ mu - target})
    res = minimize(lambda w: w @ cov @ w, np.full(n, 1 / n), jac=lambda w: 2 * cov @ w, bounds=[(0, 1)] * n,
                   constraints=cons, method="SLSQP", options={"maxiter": 500, "ftol": 1e-12})
    return np.clip(res.x, 0, 1) / np.clip(res.x, 0, 1).sum()


def max_sharpe(mu, cov):
    n = len(mu)
    res = minimize(lambda w: -(w @ mu - RF) / np.sqrt(w @ cov @ w), np.full(n, 1 / n), bounds=[(0, 1)] * n,
                   constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}], method="SLSQP", options={"maxiter": 500})
    return np.clip(res.x, 0, 1) / np.clip(res.x, 0, 1).sum()


def frontier(mu, cov, points=POINTS):
    w0 = min_var(mu, cov)
    lo, hi = w0 @ mu, mu.max()
    return [min_var(mu, cov, t) for t in np.linspace(lo, hi, points)]


def stats(w, mu, cov):
    ret, vol = float(w @ mu), float(np.sqrt(w @ cov @ w))
    return ret, vol, (ret - RF) / vol


def at_vol(curve, mu, cov, vol):
    """Highest frontier return at (or below) a given volatility, by interpolation along the curve."""
    pts = sorted(stats(w, mu, cov)[:2][::-1] for w in curve)  # (vol, ret)
    best = None
    for (v1, r1), (v2, r2) in zip(pts, pts[1:]):
        if v1 <= vol <= v2:
            best = r1 + (r2 - r1) * (vol - v1) / (v2 - v1) if v2 > v1 else max(r1, r2)
    return best if best is not None else (pts[-1][1] if vol > pts[-1][0] else None)


def analyse(R, names, mix, rng):
    mu, cov = R.mean(0) * 12, np.cov(R, rowvar=False) * 12
    classic = frontier(mu, cov)
    sharpe = max_sharpe(mu, cov)
    samples, sharpes = [], []
    for _ in range(B):
        Rb = R[rng.integers(0, len(R), len(R))]
        mb, cb = Rb.mean(0) * 12, np.cov(Rb, rowvar=False) * 12
        samples.append(frontier(mb, cb))
        sharpes.append(max_sharpe(mb, cb))
    resampled = [np.mean([s[k] for s in samples], axis=0) for k in range(POINTS)]
    sharpes = np.array(sharpes)
    w_mix = np.array([mix[n] for n in names]) / sum(mix[n] for n in names)
    return dict(mu=mu, cov=cov, classic=classic, resampled=resampled, sharpe=sharpe, sharpe_resampled=sharpes.mean(0),
                sharpe_p10=np.percentile(sharpes, 10, axis=0), sharpe_p90=np.percentile(sharpes, 90, axis=0), mix=w_mix,
                vol_assets=np.sqrt(np.diag(cov)))


def pct(x):
    return f"{x:.1%}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    L = ["# Efficient frontier and resampled frontier: a diagnostic (TEST, 20 Nov 2026)", "",
         "Generated by `python -m m04.frontier`. Method and defaults: module docstring. **Diagnostic only: our stock/bond split comes from the "
         "floor rule, not from this optimizer, and past returns do not predict future ones.** Mean returns from 5-10 years of data are very "
         "noisy; the resampled frontier shows how much the 'optimal' weights move when the same history is resampled.", ""]
    for wname, start in WINDOWS.items():
        R_all = returns(start)
        L += [f"## {wname}", "", "| Asset | Annual return | Volatility |", "|---|---|---|"]
        mu_all, vol_all = R_all.mean(0) * 12, R_all.std(0, ddof=1) * np.sqrt(12)
        for n, m_, v in zip(ASSETS, mu_all, vol_all):
            L.append(f"| {n} | {pct(m_)} | {pct(v)} |")
        for scope, names in (("Whole portfolio (bonds included)", ASSETS), ("Growth sleeve only (stocks and equity ETFs)", GROWTH)):
            idx = [ASSETS.index(n) for n in names]
            A = analyse(R_all[:, idx], names, MIX, rng)
            mr, mv, ms = stats(A["mix"], A["mu"], A["cov"])
            fc = at_vol(A["classic"], A["mu"], A["cov"], mv)
            fr = at_vol(A["resampled"], A["mu"], A["cov"], mv)
            sr, sv, ss = stats(A["sharpe"], A["mu"], A["cov"])
            rr, rv, rs = stats(A["sharpe_resampled"], A["mu"], A["cov"])
            tag = f"{start}_{'all' if len(names) == len(ASSETS) else 'growth'}"
            with open(OUT / f"frontier_points_{tag}.csv", "w", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["curve", "volatility", "return"] + names)
                for curve, ws in (("classic", A["classic"]), ("resampled", A["resampled"])):
                    for wt in ws:
                        r_, v_, _ = stats(wt, A["mu"], A["cov"])
                        w.writerow([curve, round(v_, 5), round(r_, 5)] + [round(x, 4) for x in wt])
                w.writerow(["our mix", round(mv, 5), round(mr, 5)] + [round(x, 4) for x in A["mix"]])
            L += ["", f"### {scope}", "",
                  f"- **Our mix:** return {pct(mr)}, volatility {pct(mv)}, Sharpe {ms:.2f}.",
                  f"- At the same volatility, the classic frontier reaches {pct(fc) if fc is not None else 'n/a'} and the resampled frontier "
                  f"{pct(fr) if fr is not None else 'n/a'}: a gap of {(fc - mr) * 100 if fc is not None else float('nan'):.1f} and "
                  f"{(fr - mr) * 100 if fr is not None else float('nan'):.1f} percentage points a year.",
                  f"- Classic best-Sharpe portfolio: return {pct(sr)}, volatility {pct(sv)}, Sharpe {ss:.2f}. Resampled: return {pct(rr)}, "
                  f"volatility {pct(rv)}, Sharpe {rs:.2f}.", "",
                  "| Asset | Our mix | Classic best Sharpe | Resampled best Sharpe | Best-Sharpe weight across resamples (p10 to p90) |",
                  "|---|---|---|---|---|"]
            for k, n in enumerate(names):
                L.append(f"| {n} | {pct(A['mix'][k])} | {pct(A['sharpe'][k])} | {pct(A['sharpe_resampled'][k])} | "
                         f"{pct(A['sharpe_p10'][k])} to {pct(A['sharpe_p90'][k])} |")
        L.append("")
    L += ["## How to read this", "",
          "- The classic frontier piles into whatever did best in the sample; the p10-p90 column shows how far those weights swing when the "
          "same months are resampled. That instability is the standard reason not to set weights with an optimizer, and the reason we size by "
          "the floor rule and the 2% worst-year loss instead.",
          "- IEF stands in for the Treasury ladder. The ladder is held to maturity to match the payments, so its market-price swings do not "
          "change what Laura receives; the whole-portfolio view therefore overstates the cost of holding bonds.",
          "- Files: `frontier_points_<start>_<all|growth>.csv` (curves and our mix, for the chart)."]
    (OUT / "frontier_summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
