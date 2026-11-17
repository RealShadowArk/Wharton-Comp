"""Refined stock screen (17 Nov 2026): our Round 2 tests at today's prices, plus the
checks adapted from the 2023 winner (Zhou, n.d.): country grades, alpha/beta vs the
industry, and a hand-graded management score. Adding checks only narrows the list,
so everything that passes here also passes the old screen. Defaults are student
judgments (Pat, 17 Nov), listed in docs/refined_screen_rules.md.

    python tools/refined_screen.py            # needs Yahoo, FRED and api.worldbank.org

Universe: every company with a Round 2 scorecard row (outputs/round2/*.md).
Outputs: outputs/screen/refined_screen_<date>.md and .csv, country_grades_<date>.csv,
and inputs/screen/management_grades.csv (template rows for Pat to grade).
"""
import csv
import json
import math
import re
import subprocess
import time
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/screen"
INP = ROOT / "inputs/screen"
UA = {"User-Agent": "Mozilla/5.0"}

# ---------- defaults (student judgments) ----------
GRADES = [(80, "A"), (65, "B"), (50, "C"), (35, "D"), (0, "F")]
FAIL_GRADES = {"F"}                   # D is flagged, not removed
MGMT_PASS = 3.0                       # average of four 1-5 items
INDUSTRY_ETF = {                      # iShares global sector ETFs (USD)
    "Semiconductors": "IXN", "Software": "IXN", "IT services": "IXN",
    "Payments": "IXG", "Exchanges and data": "IXG",
    "Medtech": "IXJ", "Pharmaceuticals and Biotechnology": "IXJ",
    "Aerospace and defence": "EXI", "Power": "JXI",
    "Consumer brands": "RXI", "Internet and Digital Platforms": "IXP"}
ETF_OVERRIDE = {t: "KXI" for t in ("PEP", "KO", "GIS", "HLN", "RKT.L")}           # staples
ETF_OVERRIDE.update({t: "RXI" for t in ("BKNG", "9961.HK", "PDD")})                # travel, e-commerce
YAHOO = {"ADYEN": "ADYEN.AS", "ASML": "ASML.AS", "TCS": "TCS.NS", "INFY": "INFY.NS"}
AB_RULES = ("both", "beta")           # winner's rule (alpha above AND beta below the industry), and beta only
COUNTRY_SUFFIX = {".KS": "KOR", ".TW": "TWN", ".T": "JPN", ".L": "GBR", ".PA": "FRA",
                  ".DE": "DEU", ".AS": "NLD", ".MI": "ITA", ".NS": "IND", ".HK": "HKG"}
COUNTRY = {"0700.HK": "CHN", "9961.HK": "CHN", "PDD": "CHN", "DLO": "URY", "INFY": "IND",
           "TCS": "IND", "NVO": "DNK", "NVS": "CHE", "ALC": "CHE", "AZN": "GBR", "HLN": "GBR",
           "CHKP": "ISR", "ESLT": "ISR", "OTEX": "CAN", "LULU": "CAN", "ADYEN": "NLD",
           "ASML": "NLD"}
FX = {"EUR": ("EURUSD=X", False), "GBP": ("GBPUSD=X", False), "GBp": ("GBPUSD=X", False),
      "JPY": ("JPY=X", True), "KRW": ("KRW=X", True), "TWD": ("TWD=X", True),
      "HKD": ("HKD=X", True), "INR": ("INR=X", True), "CHF": ("CHF=X", True),
      "CNY": ("CNY=X", True), "DKK": ("DKK=X", True)}
WB_ISO = ["USA", "KOR", "CHN", "HKG", "TWN", "JPN", "GBR", "FRA", "DEU", "NLD", "ITA", "IND",
          "URY", "DNK", "CHE", "ISR", "CAN"]


def get(url, headers=UA, timeout=60):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers),
                                        timeout=timeout) as r:
                return r.read().decode()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def monthly(symbol):
    """Month-start -> adjusted close (Yahoo), plus the latest price and currency."""
    d = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                       "?range=6y&interval=1mo"))["chart"]["result"][0]
    ts, adj = d["timestamp"], d["indicators"]["adjclose"][0]["adjclose"]
    off = d["meta"].get("gmtoffset", 0)       # bars are stamped at local midnight
    series = {}
    for t, p in zip(ts, adj):
        if p:
            m = datetime.fromtimestamp(t + off + 43200, tz=timezone.utc)   # noon: immune to DST shifts
            series[(m.year, m.month)] = p
    time.sleep(0.3)
    return series, d["meta"]["regularMarketPrice"], d["meta"].get("currency", "")


def returns(series, months):
    return [series[b] / series[a] - 1 for a, b in zip(months, months[1:])
            if a in series and b in series] if all(m in series for m in months) else None


def window():
    """61 month-starts ending with the last complete month (60 monthly returns)."""
    y, m = date.today().year, date.today().month
    out = []
    for k in range(61, 0, -1):
        mm = m - k
        out.append((y + (mm - 1) // 12, (mm - 1) % 12 + 1))
    return out


def usd_per(ccy, cache):
    """USD per one unit of a currency, from Yahoo's latest FX quote."""
    if ccy == "USD":
        return 1.0
    if ccy in ("GBp", "GBX"):
        return usd_per("GBP", cache) / 100
    if ccy not in cache:
        sym, inv = FX[ccy]
        _, rate, _ = monthly(sym)
        cache[ccy] = 1 / rate if inv else rate
    return cache[ccy]


def alpha_beta(rs, rm, rf):
    xs = [a - f for a, f in zip(rm, rf)]
    ys = [a - f for a, f in zip(rs, rf)]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    var = sum((x - mx) ** 2 for x in xs)
    beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / var
    return 12 * (my - beta * mx), beta          # annualized Jensen alpha, beta


def tbill(months):
    rows = [r.split(",") for r in get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=TB3MS",
                                      headers={"User-Agent": "curl/8"}).splitlines()[1:]]
    m = {(int(d[:4]), int(d[5:7])): float(v) / 1200 for d, v in rows if v not in ("", ".")}
    last = m[max(m)]
    return [m.get(k, last) for k in months[1:]]


# ---------- country grades ----------
def wb(indicator, source=None):
    url = (f"https://api.worldbank.org/v2/country/{';'.join(WB_ISO)}/indicator/{indicator}"
           f"?format=json&mrnev=1&per_page=100" + (f"&source={source}" if source else ""))
    out = {}
    for r in json.loads(get(url, timeout=120))[1] or []:
        iso = "TWN" if "Taiwan" in r["country"]["value"] else r["countryiso3code"]
        out[iso] = (r["value"], r["date"])
    return out


RATING_SCORE = {"AAA": 100, "AA+": 95, "AA": 90, "AA-": 85, "A+": 80, "A": 75, "A-": 70,
                "BBB+": 65, "BBB": 60, "BBB-": 55, "BB+": 45, "BB": 40, "BB-": 35, "B+": 25,
                "B": 20, "B-": 15}


def country_grades():
    pv, rq = wb("GOV_WGI_PV.SC", 3), wb("GOV_WGI_RQ.SC", 3)
    infl, gini = wb("FP.CPI.TOTL.ZG"), wb("SI.POV.GINI")
    ratings_file = INP / "sovereign_ratings.csv"
    if not ratings_file.exists():
        with ratings_file.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["iso3", "sp_rating", "source", "as_of"])
            w.writerows([[c, "", "", ""] for c in WB_ISO])
    ratings = {r["iso3"]: r for r in csv.DictReader(ratings_file.open())}
    grades = {}
    for c in WB_ISO:
        parts, notes = [], []
        for name, data, f in (
                ("political stability", pv, lambda v: v),
                ("regulatory quality", rq, lambda v: v),
                ("inflation", infl, lambda v: max(0.0, 100 - 12.5 * abs(v - 2))),
                ("inequality", gini, lambda v: min(100.0, max(0.0, (55 - v) / 30 * 100)))):
            v = data.get(c, (None, None))
            if v[0] is None:
                notes.append(f"{name} MISSING")
            else:
                parts.append(f(v[0]))
        rt = ratings.get(c, {}).get("sp_rating", "").strip()
        if rt in RATING_SCORE:
            parts.append(RATING_SCORE[rt])
        else:
            notes.append("credit rating MISSING")
        score = sum(parts) / len(parts)
        grade = next(g for cut, g in GRADES if score >= cut)
        grades[c] = dict(iso3=c, score=round(score, 1), grade=grade, criteria=len(parts),
                         provisional="yes" if notes else "no", missing="; ".join(notes),
                         pol_stab=pv.get(c, (None,))[0], reg_quality=rq.get(c, (None,))[0],
                         inflation=infl.get(c, (None,))[0], gini=gini.get(c, (None,))[0],
                         rating=rt or "MISSING")
    return grades


# ---------- Round 2 scorecards ----------
def num(cell):
    m = re.search(r"-?[\d,]+\.?\d*", cell or "")
    return float(m.group().replace(",", "")) if m else None


def scorecards():
    rows = {}
    files = sorted(ROOT.glob("outputs/round2/Round2_scorecard*.md"),
                   key=lambda p: subprocess.run(["git", "log", "-1", "--format=%ct", "--", str(p)],
                                                capture_output=True, text=True, cwd=ROOT).stdout)
    for f in files:                          # later commits override earlier ones
        header = None
        for line in f.read_text().splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0] == "Group":
                header = cells
                continue
            if not header or len(cells) != len(header) or set(line) <= set("|- "):
                continue
            r = dict(zip(header, cells))
            if "Value / price" not in r:
                continue
            price = num(r["Price"])
            ccy = r["Price"].split()[-1]
            bear = num(r.get("Bear / price")) if "Bear / price" in r else (
                (num(r["Bear value"]) or 0) / price if num(r.get("Bear value")) else None)
            rows[r["Ticker"]] = dict(
                ticker=r["Ticker"], group=r["Group"], price_then=price, ccy=ccy,
                r_b1=num(r["Value / price"]), r_5y=num(r["At 5-year beta"]),
                r_full=num(r["At full-history beta"]), bear=bear, source=f.name)
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    INP.mkdir(parents=True, exist_ok=True)
    today = date.today()
    months = window()
    rf = tbill(months)
    grades = country_grades()
    bench, _, _ = monthly("ACWI")
    rm = returns(bench, months)
    etf_ab, fx_ret, fx_spot = {}, {}, {}
    mgmt_file = INP / "management_grades.csv"
    mgmt = {r["ticker"]: r for r in csv.DictReader(mgmt_file.open())} if mgmt_file.exists() else {}

    results = []
    for t, s in sorted(scorecards().items()):
        sym = YAHOO.get(t, t)
        row = dict(ticker=t, group=s["group"], source=s["source"])
        try:
            series, px, ccy = monthly(sym)
        except Exception as e:
            row.update(status=f"no Yahoo data ({type(e).__name__})")
            results.append(row)
            continue
        px_s = px * usd_per(ccy, fx_spot) / usd_per(s["ccy"], fx_spot)   # in the scorecard's currency
        k = s["price_then"] / px_s
        r = {n: (s[n] * k if s[n] is not None else None) for n in ("r_b1", "r_5y", "r_full", "bear")}
        up, down = r["r_b1"] - 1, (r["bear"] - 1) if r["bear"] is not None else None
        updown = float("inf") if down is not None and down >= 0 else (
            up / -down if down else None)
        old = all(v is not None and v > 1 for v in (r["r_b1"], r["r_5y"], r["r_full"])) and (
            updown is not None and updown >= 1)
        # alpha/beta in USD vs ACWI, and the industry ETF's own alpha/beta
        rs = returns(series, months)
        if rs and ccy in FX:                 # convert local returns to USD
            fsym, inv = FX[ccy]
            if fsym not in fx_ret:
                fs, _, _ = monthly(fsym)
                fr = returns(fs, months)
                fx_ret[fsym] = [(1 / (1 + x) - 1) if inv else x for x in fr] if fr else None
            fr = fx_ret[fsym]
            rs = [(1 + a) * (1 + b) - 1 for a, b in zip(rs, fr)] if fr else None
        etf = ETF_OVERRIDE.get(t, INDUSTRY_ETF.get(s["group"]))
        if etf not in etf_ab:
            es, _, _ = monthly(etf)
            etf_ab[etf] = alpha_beta(returns(es, months), rm, rf)
        ea, eb = etf_ab[etf]
        if rs:
            a, b = alpha_beta(rs, rm, rf)
            ab_pass = {"both": a > ea and b < eb, "beta": b < eb}
        else:
            a = b = None                     # under 60 months of history: not testable
            ab_pass = {"both": None, "beta": None}
        iso = COUNTRY.get(t) or next((c for suf, c in COUNTRY_SUFFIX.items() if t.endswith(suf)), "USA")
        g = grades[iso]
        country_pass = g["grade"] not in FAIL_GRADES
        m = mgmt.get(t, {})
        items = [num(m.get(k)) for k in ("capital_allocation", "guidance_record",
                                         "governance", "controversies")]
        mg = sum(items) / 4 if all(v is not None for v in items) else None
        def refined(rule):
            ok = old and country_pass and bool(ab_pass[rule]) and (mg is None or mg >= MGMT_PASS)
            return "yes, management pending" if ok and mg is None else "yes" if ok else "no"
        row.update(price_now=round(px_s, 2), ccy=s["ccy"], r_b1=round(r["r_b1"], 2),
                   r_5y=round(r["r_5y"], 2) if r["r_5y"] else None,
                   r_full=round(r["r_full"], 2) if r["r_full"] else None,
                   bear=round(r["bear"], 2) if r["bear"] else None,
                   updown="no downside" if updown == float("inf") else (round(updown, 2) if updown else None),
                   old_pass=old, country=iso, grade=g["grade"] + ("*" if g["provisional"] == "yes" else ""),
                   alpha=round(a * 100, 1) if a is not None else None,
                   beta=round(b, 2) if b is not None else None, etf=etf,
                   etf_alpha=round(ea * 100, 1) if ea is not None else None,
                   etf_beta=round(eb, 2) if eb is not None else None,
                   alpha_above=(a > ea) if a is not None else None,
                   beta_below=ab_pass["beta"],
                   mgmt=round(mg, 2) if mg is not None else "pending",
                   refined_pass=refined("both"), refined_beta_only=refined("beta"), status="ok")
        results.append(row)

    # outputs
    keys = ["ticker", "group", "price_now", "ccy", "r_b1", "r_5y", "r_full", "bear", "updown",
            "old_pass", "country", "grade", "alpha", "beta", "etf", "etf_alpha", "etf_beta",
            "alpha_above", "beta_below", "mgmt", "refined_pass", "refined_beta_only", "status",
            "source"]
    with (OUT / f"refined_screen_{today}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)
    with (OUT / f"country_grades_{today}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(next(iter(grades.values())).keys()))
        w.writeheader()
        w.writerows(grades.values())
    # management template for the names that pass everything else
    need = [r for r in results if r.get("refined_beta_only", "").startswith("yes")]
    if not mgmt_file.exists() or need:
        rows = {r["ticker"]: r for r in csv.DictReader(mgmt_file.open())} if mgmt_file.exists() else {}
        for r in need:
            rows.setdefault(r["ticker"], dict(ticker=r["ticker"], capital_allocation="",
                                              guidance_record="", governance="", controversies="",
                                              evidence=""))
        with mgmt_file.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["ticker", "capital_allocation", "guidance_record",
                                              "governance", "controversies", "evidence"])
            w.writeheader()
            w.writerows(rows.values())
    ok = [r for r in results if r.get("status") == "ok"]
    L = [f"# Refined screen, {today} (TEST)", "",
         "Generated by `python tools/refined_screen.py`. Rules: `docs/refined_screen_rules.md`. "
         "Value ratios are the Round 2 DCF values at today's price (values unchanged). Alpha and "
         "beta: 60 monthly USD returns vs ACWI, T-bill adjusted; the industry is the iShares global "
         "sector ETF. A * grade is provisional (criteria missing). Past alpha does not predict "
         "future returns.", "",
         f"**Funnel:** {len(results)} Round 2 companies → {len(ok)} with data → "
         f"{sum(r['old_pass'] for r in ok)} pass the old value tests today → "
         f"{sum(r['old_pass'] and r['grade'][0] not in FAIL_GRADES for r in ok)} also pass the country grade → "
         f"{sum(r['refined_pass'] != 'no' for r in ok)} also pass the winner's alpha AND beta rule, "
         f"{sum(r['refined_beta_only'] != 'no' for r in ok)} pass with beta only "
         "(management grades pending).", "",
         "| Ticker | Group | Value/price b1, 5y, full | Bear | Up/down | Old | Country | Alpha % (ETF) | Beta (ETF) | Mgmt | Refined: alpha+beta | Refined: beta only |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(ok, key=lambda r: (not r["old_pass"], r["refined_beta_only"] == "no", r["ticker"])):
        L.append(f"| {r['ticker']} | {r['group']} | {r['r_b1']}, {r['r_5y']}, {r['r_full']} | {r['bear']} | "
                 f"{r['updown']} | {'pass' if r['old_pass'] else 'fail'} | {r['country']} {r['grade']} | "
                 f"{r['alpha']} ({r['etf_alpha']} {r['etf']}) | {r['beta']} ({r['etf_beta']}) | {r['mgmt']} | "
                 f"{r['refined_pass']} | {r['refined_beta_only']} |")
    bad = [r for r in results if r.get("status") != "ok"]
    if bad:
        L += ["", "No data: " + ", ".join(f"{r['ticker']} ({r['status']})" for r in bad)]
    L += ["", "## Country grades", "",
          "| Country | Score | Grade | Pol. stability | Reg. quality | Inflation % | Gini | S&P rating | Missing |",
          "|---|---|---|---|---|---|---|---|---|"]
    for g in sorted(grades.values(), key=lambda g: -g["score"]):
        L.append(f"| {g['iso3']} | {g['score']} | {g['grade']} | {fmt(g['pol_stab'])} | {fmt(g['reg_quality'])} | "
                 f"{fmt(g['inflation'])} | {fmt(g['gini'])} | {g['rating']} | {g['missing']} |")
    (OUT / f"refined_screen_{today}.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def fmt(v):
    return "MISSING" if v is None else f"{v:.1f}"


if __name__ == "__main__":
    main()
