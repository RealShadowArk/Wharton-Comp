"""Universe screen (17 Nov 2026), modelled on the 2023 winner's funnel (Zhou, n.d.):
S&P 500 constituents → price ≥ $5 → country grade (not F) → alpha/beta vs the
industry average → M12 score within peer groups → top 3 per group.

Both alpha/beta versions are reported:
  winner's rule: alpha above AND beta below the industry average;
  refined rule (binding, Pat 17 Nov): beta below the industry average.

Banks, insurers and REITs are kept, with their own M12 metric sets (the FCFF metrics
do not fit balance-sheet businesses); see docs/refined_screen_rules.md.

    python tools/universe_screen.py        # needs Wikipedia, Yahoo, FRED, World Bank
Cache: scratchpad-style folder outputs/screen/.cache (git-ignored); delete it to refresh.
"""
import csv
import hashlib
import html
import importlib.util
import json
import re
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/screen"
CACHE = OUT / ".cache"
spec = importlib.util.spec_from_file_location("rs", ROOT / "tools/refined_screen.py")
rs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rs)

_raw_get = rs.get


def cached_get(url, headers=rs.UA, timeout=60):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".txt")
    if f.exists():
        return f.read_text()
    text = _raw_get(url, headers=headers, timeout=timeout)
    f.write_text(text)
    return text


rs.get = cached_get
rs.time.sleep = lambda s: None          # the cache makes the polite pause unnecessary on reruns

STATES = set("""Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware Florida
Georgia Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts
Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada New_Hampshire New_Jersey New_Mexico
New_York North_Carolina North_Dakota Ohio Oklahoma Oregon Pennsylvania Rhode_Island South_Carolina
South_Dakota Tennessee Texas Utah Vermont Virginia Washington West_Virginia Wisconsin Wyoming
D.C. Washington_D.C. District_of_Columbia Puerto_Rico""".replace("_", " ").split()) | {
    "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
    "Rhode Island", "South Carolina", "South Dakota", "West Virginia", "Washington, D.C.",
    "District of Columbia", "Puerto Rico"}
ISO = {"United States": "USA", "South Korea": "KOR", "China": "CHN", "Hong Kong": "HKG",
       "Taiwan": "TWN", "Japan": "JPN", "United Kingdom": "GBR", "England": "GBR", "France": "FRA",
       "Germany": "DEU", "Netherlands": "NLD", "Italy": "ITA", "India": "IND", "Uruguay": "URY",
       "Denmark": "DNK", "Switzerland": "CHE", "Israel": "ISR", "Canada": "CAN", "Ireland": "IRL",
       "Bermuda": "BMU", "Luxembourg": "LUX", "Singapore": "SGP", "Jersey": "GBR", "Guernsey": "GBR",
       "Ontario": "CAN", "Quebec": "CAN", "British Columbia": "CAN", "Alberta": "CAN"}
BANKLIKE = ("Bank", "Insurance", "Reinsurance", "Consumer Finance", "Multi-Sector Holdings",
            "Mortgage")


def table_rows(page):
    tabs = re.findall(r'(?s)<table[^>]*class="[^"]*wikitable[^"]*"[^>]*>.*?</table>', page)
    out = []
    for tab in tabs:
        rows = []
        for tr in re.findall(r"(?s)<tr.*?</tr>", tab):
            rows.append([html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                         for c in re.findall(r"(?s)<t[hd][^>]*>(.*?)</t[hd]>", tr)])
        out.append(rows)
    return out


def sp500():
    page = cached_get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    rows = table_rows(page)[0]
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:] if len(r) >= 5]


HQ_OVERRIDE = {"XYZ": "USA"}   # Block, Inc.: Wikipedia lists no HQ; Oakland, California (company 10-K)


def country_of(hq):
    hq = re.sub(r"\[\d+\]", "", hq)                     # drop footnote markers
    last = hq.split(",")[-1].strip()
    if last in STATES or hq.strip() in STATES:
        return "USA"
    return ISO.get(last, "MISSING")


def fill_ratings(isos):
    """S&P foreign-currency sovereign ratings from Wikipedia's table (which cites S&P)."""
    page = cached_get("https://en.wikipedia.org/wiki/List_of_countries_by_credit_rating")
    sp = table_rows(page)[0]
    names = {v: k for k, v in ISO.items() if k not in ("England", "Jersey", "Guernsey", "Ontario",
                                                      "Quebec", "British Columbia", "Alberta")}
    found = {}
    for r in sp[1:]:
        m = re.search(r"(AAA|AA\+|AA−|AA-|AA|A\+|A−|A-|A|BBB\+|BBB−|BBB-|BBB|BB\+|BB−|BB-|BB|B\+|B−|B-|B)$", r[1])
        if m:
            found[r[0].strip()] = (m.group(1).replace("−", "-"), r[3] if len(r) > 3 else "")
    path = ROOT / "inputs/screen/sovereign_ratings.csv"
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["iso3", "sp_rating", "source", "as_of"])
        for iso in sorted(isos):
            name = names.get(iso, "")
            rt, when = found.get(name, ("", ""))
            w.writerow([iso, rt, "Wikipedia, 'List of countries by credit rating', S&P table "
                        f"(citing S&P Global Ratings), accessed {date.today()}" if rt else
                        "MISSING: not in the S&P table", when])


def fundamentals(sym):
    types = ["TotalRevenue", "OperatingIncome", "PretaxIncome", "NetIncomeCommonStockholders",
             "DilutedEPS", "TotalAssets", "TotalDebt", "CurrentAssets", "CurrentLiabilities",
             "StockholdersEquity", "OperatingCashFlow", "CapitalExpenditure", "OrdinarySharesNumber",
             "ReconciledDepreciation", "InterestExpense"]
    url = ("https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/"
           f"{sym}?type={','.join('annual' + t for t in types)}&period1=1483228800"
           f"&period2={int(time.time())}")
    data = {}
    for res in json.loads(cached_get(url))["timeseries"]["result"]:
        t = res["meta"]["type"][0].replace("annual", "")
        pts = [p for p in res.get(res["meta"]["type"][0], []) if p]
        data[t] = [p["reportedValue"]["raw"] for p in sorted(pts, key=lambda p: p["asOfDate"])]
    return data


def m12_metrics(d, price, kind):
    """The eight M12 metrics (or the bank-like / REIT variants). None = MISSING."""
    def last(k, n=1):
        v = d.get(k, [])
        return v[-n] if len(v) >= n else None

    def cagr(series):
        v = d.get(series, [])
        if len(v) < 4 or v[-4] is None or v[-1] is None or v[-4] <= 0 or v[-1] <= 0:
            return None
        return (v[-1] / v[-4]) ** (1 / 3) - 1

    def div(a, b):
        return a / b if a is not None and b not in (None, 0) else None
    shares = last("OrdinarySharesNumber")
    mcap = price * shares if shares else None
    rev, ni = last("TotalRevenue"), last("NetIncomeCommonStockholders")
    assets = [last("TotalAssets"), last("TotalAssets", 2)]
    avg_assets = sum(assets) / 2 if None not in assets else None
    cfo, capex = last("OperatingCashFlow"), last("CapitalExpenditure")
    m = {"G1": cagr("TotalRevenue"), "G2": cagr("DilutedEPS"), "V1": div(ni, mcap)}
    if kind == "banklike":
        m.update(Q1=div(last("PretaxIncome"), rev), Q2=div(ni, avg_assets),
                 B1=div(last("TotalDebt") or 0, last("StockholdersEquity")),
                 B2=div(last("StockholdersEquity"), last("TotalAssets")),
                 V2=div(last("StockholdersEquity"), mcap))
    elif kind == "reit":
        dep = last("ReconciledDepreciation")
        ffo = ni + dep if ni is not None and dep is not None else None
        m.update(Q1=div(last("OperatingIncome"), rev), Q2=div(rev, avg_assets),
                 B1=div(last("TotalDebt"), last("TotalAssets")),
                 B2=div(last("OperatingIncome"), abs(last("InterestExpense") or 0) or None),
                 V1=div(ffo, mcap), V2=div(cfo, mcap))
    else:
        m.update(Q1=div(last("OperatingIncome"), rev), Q2=div(rev, avg_assets),
                 B1=div(last("TotalDebt") or 0, last("TotalAssets")),
                 B2=div(last("CurrentAssets"), last("CurrentLiabilities")),
                 V2=div(cfo + capex if cfo is not None and capex is not None else None, mcap))
    return m


DIRECTION = {"Q1": 1, "Q2": 1, "B1": -1, "B2": 1, "G1": 1, "G2": 1, "V1": 1, "V2": 1}


def m12_score(group):
    """M12: rank each metric within the peer group (RANK.AVG), s = 100 (r-1)/(n-1), equal weights.
    Only complete companies are ranked; groups need at least 5 of them."""
    complete = [c for c in group if all(c["m"][k] is not None for k in DIRECTION)]
    if len(complete) < 5:
        return
    for k, sgn in DIRECTION.items():
        vals = sorted(sgn * c["m"][k] for c in complete)
        n = len(vals)
        for c in complete:
            x = sgn * c["m"][k]
            lo = vals.index(x) + 1
            hi = n - vals[::-1].index(x)
            c.setdefault("s", {})[k] = 100 * ((lo + hi) / 2 - 1) / (n - 1)
    for c in complete:
        c["tfs"] = round(sum(c["s"].values()) / 8, 1)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ".gitignore").write_text(".cache/\n")
    today = date.today()
    uni, seen = [], set()
    for c in sp500():                                   # one row per company: drop extra share classes
        if c.get("CIK") in seen:
            continue
        seen.add(c.get("CIK"))
        uni.append(c)
    for c in uni:
        c["country"] = HQ_OVERRIDE.get(c["Symbol"]) or country_of(c["Headquarters Location"])
    isos = sorted(set(rs.WB_ISO) | {c["country"] for c in uni if c["country"] != "MISSING"})
    fill_ratings(isos)
    rs.WB_ISO = isos
    grades = rs.country_grades()
    months = rs.window()
    rf = rs.tbill(months)
    bench, _, _ = rs.monthly("ACWI")
    rm = rs.returns(bench, months)

    for c in uni:
        c["sym"] = c["Symbol"].replace(".", "-")
        sub = c["GICS Sub-Industry"]
        c["kind"] = ("banklike" if any(w in sub for w in BANKLIKE) else
                     "reit" if "REIT" in sub else "standard")
        try:
            series, px, ccy = rs.monthly(c["sym"])
            c["price"] = px
            r = rs.returns(series, months)
            c["alpha"], c["beta"] = rs.alpha_beta(r, rm, rf) if r else (None, None)
        except Exception as e:
            c["price"], c["alpha"], c["beta"], c["err"] = None, None, None, type(e).__name__

    # industry average: sub-industry when it has 5+ measured members, else the sector
    def peers_key(c):
        n = sum(1 for o in uni if o["GICS Sub-Industry"] == c["GICS Sub-Industry"] and o["beta"] is not None)
        return ("sub", c["GICS Sub-Industry"]) if n >= 5 else ("sector", c["GICS Sector"])
    avg = {}
    for c in uni:
        c["ind"] = peers_key(c)
    for key in {c["ind"] for c in uni}:
        mem = [o for o in uni if o["ind"] == key and o["beta"] is not None]
        avg[key] = (sum(o["alpha"] for o in mem) / len(mem), sum(o["beta"] for o in mem) / len(mem))

    for c in uni:
        g = grades.get(c["country"], {"grade": "MISSING", "provisional": "yes"})
        c["grade"] = g["grade"] + ("*" if g.get("provisional") == "yes" else "")
        c["price_ok"] = c["price"] is not None and c["price"] >= 5
        c["country_ok"] = not c["grade"].startswith("MISSING") and c["grade"][0] not in rs.FAIL_GRADES
        ia, ib = avg[c["ind"]]
        c["ind_alpha"], c["ind_beta"] = ia, ib
        c["beta_ok"] = c["beta"] is not None and c["beta"] < ib
        c["alpha_ok"] = c["alpha"] is not None and c["alpha"] > ia
        c["refined"] = c["price_ok"] and c["country_ok"] and c["beta_ok"]
        c["winner"] = c["refined"] and c["alpha_ok"]
        c["m"] = {k: None for k in DIRECTION}
        if c["refined"]:
            try:
                c["m"] = m12_metrics(fundamentals(c["sym"]), c["price"], c["kind"])
            except Exception as e:
                c["err"] = "fundamentals " + type(e).__name__

    # M12 peer groups: GICS sector, with bank-like and REIT businesses in their own groups
    def group(c):
        return {"banklike": "Financials: banks and insurers", "reit": "Real Estate: REITs"}.get(
            c["kind"], c["GICS Sector"] + ("" if c["GICS Sector"] != "Financials" else ": other"))
    for gname in {group(c) for c in uni}:
        m12_score([c for c in uni if group(c) == gname and c["refined"]])

    def shortlist(flag, top=3):
        picks = []
        for gname in sorted({group(c) for c in uni}):
            mem = sorted([c for c in uni if group(c) == gname and c[flag] and c.get("tfs") is not None],
                         key=lambda c: -c["tfs"])
            if mem:
                cut = mem[min(top, len(mem)) - 1]["tfs"]
                picks += [c for c in mem if c["tfs"] >= cut]       # keep ties
        return picks

    keys = ["Symbol", "Security", "GICS Sector", "GICS Sub-Industry", "country", "grade", "kind",
            "price", "alpha", "beta", "ind_alpha", "ind_beta", "alpha_ok", "beta_ok", "refined",
            "winner", "tfs", "err"]
    with (OUT / f"universe_screen_{today}.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(keys + list(DIRECTION))
        for c in uni:
            w.writerow([round(c[k], 4) if isinstance(c.get(k), float) else c.get(k, "") for k in keys] +
                       [round(c["m"][k], 4) if c["m"][k] is not None else "MISSING" for k in DIRECTION])
    n = len(uni)
    priced = sum(c["price_ok"] for c in uni)
    ctry = sum(c["price_ok"] and c["country_ok"] for c in uni)
    ref = [c for c in uni if c["refined"]]
    win = [c for c in uni if c["winner"]]
    L = [f"# Universe screen, {today} (TEST)", "",
         "Generated by `python tools/universe_screen.py`. Universe: S&P 500 constituents (Wikipedia). "
         "Alpha and beta: 60 monthly returns vs ACWI, T-bill adjusted, compared with the average of the "
         "GICS sub-industry (5+ members) or sector. M12: eight metrics ranked within peer groups (bank-like "
         "and REIT variants), equal weights, Yahoo annual statements. A score is a research filter, never a "
         "value or a weight; past alpha does not predict returns. Next step for the shortlist: the DCF and "
         "red-flag work (team packages).", "",
         f"**Funnel:** {n} companies → {priced} priced ≥ $5 → {ctry} pass the country grade → "
         f"**{len(ref)} beta below the industry (refined, binding)** → "
         f"{sum(c.get('tfs') is not None for c in ref)} with complete M12 data; "
         f"winner's rule (alpha above as well): **{len(win)}** → "
         f"{sum(c.get('tfs') is not None for c in win)} with complete M12 data.", ""]
    for title, flag in (("Shortlist: winner's rule (alpha above and beta below the industry), top 3 M12 per group", "winner"),
                        ("Shortlist: refined rule (beta below the industry), top 3 M12 per group", "refined")):
        L += [f"## {title}", "", "| Group | Ticker | Company | Sub-industry | Country | M12 | Alpha % (ind.) | Beta (ind.) |",
              "|---|---|---|---|---|---|---|---|"]
        for c in shortlist(flag):
            L.append(f"| {group(c)} | {c['Symbol']} | {c['Security']} | {c['GICS Sub-Industry']} | "
                     f"{c['country']} {c['grade']} | {c['tfs']} | {c['alpha'] * 100:.1f} ({c['ind_alpha'] * 100:.1f}) | "
                     f"{c['beta']:.2f} ({c['ind_beta']:.2f}) |")
        L.append("")
    errs = [c for c in uni if c.get("err")]
    if errs:
        L.append("Data gaps: " + ", ".join(f"{c['Symbol']} ({c['err']})" for c in errs))
    (OUT / f"universe_screen_{today}.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
