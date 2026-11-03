"""Round 2 risk measures and red flags for the nine finalists (kit README formulas).

Run: python tools/round2_risk_redflags.py
Reads inputs/round2_2026-11-01/Pat_Round2_data_completed.xlsx (Red flags tab) and
yahoo_monthly_adjclose_max.csv (Yahoo Adj Close, max history, from Pat's 2 Nov file).
Writes outputs/round2/M_round2_risk.csv and M_round2_redflags.csv.

Choices (labelled; Pat can change them):
- Window: 60 monthly returns, Nov 2021 to Oct 2026 (prices Oct 2021 to Oct 2026),
  matching Aryu's window and the 30 Oct valuation date.
- Adyen and TCS in US dollars: ADYEN.AS x EURUSD=X, TCS.NS / INR=X (M04 rule).
- Annual return = compound (geometric) annual return over the window.
- rf = 4.00%: 3-month T-bill, FRED DTB3, 30 Oct 2026 (read by Pat).
- Piotroski test 5: leverage "lower than last year", or zero debt in both years.
- dLocal and Adyen FY0 CFO use Pat's merchant-funds correction (supplement, 2 Nov).
"""
import csv
import math
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
R2 = ROOT / "inputs" / "round2_2026-11-01"
OUT = ROOT / "outputs" / "round2"
RF = 0.04
START, END = "2021-10", "2026-10"
TICKERS = ["DLO", "ADYEN", "PYPL", "CME", "ICE", "MCO", "INFY", "TCS", "CTSH"]
CFO_CORRECTED = {"DLO": 227.476, "ADYEN": 1246.157}  # Finalists_DCF_Supplement_Reviewed.xlsx


def usd_prices():
    rows = list(csv.DictReader(open(R2 / "yahoo_monthly_adjclose_max.csv")))
    num = lambda v: None if v in ("", "NA") else float(v)
    out = {}
    for r in rows:
        eur, inr = num(r["EURUSD=X"]), num(r["INR=X"])
        a, t = num(r["ADYEN.AS"]), num(r["TCS.NS"])
        out[r["month"]] = {
            "SPY": num(r["SPY"]), "DLO": num(r["DLO"]), "PYPL": num(r["PYPL"]),
            "CME": num(r["CME"]), "ICE": num(r["ICE"]), "MCO": num(r["MCO"]),
            "INFY": num(r["INFY"]), "CTSH": num(r["CTSH"]),
            "ADYEN": a * eur if a is not None and eur is not None else None,
            "TCS": t / inr if t is not None and inr is not None else None,
            "ADYEN_local": a, "TCS_local": t}
    return out


def risk(prices):
    months = [m for m in sorted(prices) if START <= m <= END]
    rets = lambda k: [prices[b][k] / prices[a][k] - 1 for a, b in zip(months, months[1:])]
    cagr = lambda k: (prices[months[-1]][k] / prices[months[0]][k]) ** (12 / (len(months) - 1)) - 1
    m = rets("SPY")
    mbar = sum(m) / len(m)
    rm = cagr("SPY")
    res = []
    for t in TICKERS:
        s = rets(t)
        sbar = sum(s) / len(s)
        cov = sum((x - sbar) * (y - mbar) for x, y in zip(s, m)) / (len(s) - 1)
        beta = cov / (sum((y - mbar) ** 2 for y in m) / (len(m) - 1))
        vol = math.sqrt(sum((x - sbar) ** 2 for x in s) / (len(s) - 1)) * math.sqrt(12)
        r = cagr(t)
        worst = worst_year(prices, t)
        ytd = prices["2026-10"][t] / prices["2025-12"][t] - 1
        res.append({"ticker": t, "returns": len(s), "beta": round(beta, 3), "volatility": round(vol, 4),
                    "annual_return": round(r, 4), "sharpe": round((r - RF) / vol, 3),
                    "treynor": round((r - RF) / beta, 4) if beta > 0 else "NOT DEFINED",
                    "alpha": round(r - (RF + beta * (rm - RF)), 4),
                    "worst_year": worst[0], "worst_return_usd": round(worst[1], 4),
                    "max_position_usd": round(6000 / -worst[1]) if worst[1] < 0 else "no losing year",
                    "ytd_2026_to_oct": round(ytd, 4)})
    return res, rm


def worst_year(prices, t):
    years = sorted({m[:4] for m in prices})
    best = (None, 9.0)
    for y in years:
        a, b = prices.get(f"{int(y) - 1}-12", {}).get(t), prices.get(f"{y}-12", {}).get(t)
        if a and b and int(y) <= 2025 and b / a - 1 < best[1]:
            best = (int(y), b / a - 1)
    return best


def red_flags():
    ws = openpyxl.load_workbook(R2 / "Pat_Round2_data_completed.xlsx", data_only=True)["Red flags"]
    rows = [r for r in ws.iter_rows(values_only=True) if any(v not in (None, "") for v in r)]
    hdr = rows[0]
    data = {(r[0], r[1]): dict(zip(hdr, r)) for r in rows[1:]}
    out = []
    for t in TICKERS:
        a, b = data[(t, "FY0")], data[(t, "FY1")]  # a = year t, b = year t-1
        cfo = CFO_CORRECTED.get(t, a["cfo"])
        roa = lambda x: x["net_income_continuing"] / x["total_assets_start_of_year"]
        lev = lambda x: (x["long_term_debt"] or 0) / ((x["total_assets"] + x["total_assets_start_of_year"]) / 2)
        cr = lambda x: x["current_assets"] / x["current_liabilities"]
        gm = lambda x: None if x["cost_of_revenue"] is None else (x["revenue"] - x["cost_of_revenue"]) / x["revenue"]
        turn = lambda x: x["revenue"] / x["total_assets_start_of_year"]
        tests = {
            "1 ROA > 0": roa(a) > 0,
            "2 CFO > 0": cfo > 0,
            "3 ROA up": roa(a) > roa(b),
            "4 CFO > net income": cfo > a["net_income_continuing"],
            "5 leverage down": lev(a) < lev(b) or (lev(a) == 0 and lev(b) == 0),
            "6 current ratio up": cr(a) > cr(b),
            "7 no new shares": a["shares_outstanding_m"] <= b["shares_outstanding_m"],
            "8 gross margin up": None if gm(a) is None else gm(a) > gm(b),
            "9 asset turnover up": turn(a) > turn(b),
        }
        checked = [v for v in tests.values() if v is not None]
        idx = {
            "DSRI": (a["receivables"] / a["revenue"]) / (b["receivables"] / b["revenue"]),
            "GMI": None if gm(a) is None else gm(b) / gm(a),
            "AQI": (1 - (a["current_assets"] + a["net_ppe"]) / a["total_assets"])
                   / (1 - (b["current_assets"] + b["net_ppe"]) / b["total_assets"]),
            "SGI": a["revenue"] / b["revenue"],
            "DEPI": (b["depreciation"] / (b["depreciation"] + b["net_ppe"]))
                    / (a["depreciation"] / (a["depreciation"] + a["net_ppe"])),
            "SGAI": (a["sga"] / a["revenue"]) / (b["sga"] / b["revenue"]),
            "TATA": (a["net_income_continuing"] - cfo) / a["total_assets"],
            "LVGI": ((a["current_liabilities"] + (a["long_term_debt"] or 0)) / a["total_assets"])
                    / ((b["current_liabilities"] + (b["long_term_debt"] or 0)) / b["total_assets"]),
        }
        coef = {"DSRI": 0.920, "GMI": 0.528, "AQI": 0.404, "SGI": 0.892, "DEPI": 0.115,
                "SGAI": -0.172, "TATA": 4.679, "LVGI": -0.327}
        m = None if idx["GMI"] is None else -4.84 + sum(coef[k] * v for k, v in idx.items())
        rec = {"ticker": t, "piotroski": sum(checked), "piotroski_checked": len(checked),
               "piotroski_fails": "; ".join(k for k, v in tests.items() if v is False),
               "piotroski_not_checked": "; ".join(k for k, v in tests.items() if v is None),
               "beneish_m": "NOT CHECKED (GMI MISSING)" if m is None else round(m, 2),
               "beneish_flag": "" if m is None else ("FLAG" if m > -1.78 else "pass"),
               "cfo_used": cfo}
        rec.update({k: "MISSING" if v is None else round(v, 3) for k, v in idx.items()})
        out.append(rec)
    return out


def write(path, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    p = usd_prices()
    rk, rm = risk(p)
    rf_ = red_flags()
    write(OUT / "M_round2_risk.csv", rk)
    write(OUT / "M_round2_redflags.csv", rf_)
    print(f"S&P 500 (SPY) compound return {rm:.1%} a year, Nov 2021-Oct 2026; rf {RF:.2%}")
    for r in rk:
        print(r)
    for r in rf_:
        print(r)
    for t, k in (("ADYEN", "ADYEN_local"), ("TCS", "TCS_local")):
        print(t, "worst year in local currency:", tuple(round(x, 4) if isinstance(x, float) else x
                                                         for x in worst_year(p, k)))
