"""Build a team-format Round 2 workbook from Yahoo annual statements (23 Nov 2026).

    python tools/yahoo_round2_workbook.py <folder> TICKER ...

Writes <folder>/yahoo_statements.json (raw, as fetched) and <folder>/Yahoo_Round2_data.xlsx with the
Valuation inputs, Red flags and Risk tabs in the columns tools/round2_team.py reads, so the standard
method runs unchanged. Consensus revenue growth comes from <folder>/consensus.csv (ticker, y1, y2, y3,
source; blank = MISSING), filled by hand from a cited source. Prices: Yahoo's latest quote at fetch time.

Data rules (student judgments, Pat to confirm):
- Statements: Yahoo fundamentals-timeseries, annual, Yahoo's standardized layout (RESEARCH; check the
  10-K before any decision). Values in USD millions.
- Debt = current debt + long-term debt. Lease liabilities are left out: Yahoo does not separate finance
  from operating leases, so finance leases are MISSING. Non-controlling interests are added to debt as a
  senior claim in the equity bridge.
- Cash = cash, equivalents and short-term investments. Shares = ordinary shares at the year-end
  (dilution MISSING). D&A from the cash-flow statement.
"""
import csv
import json
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
from refined_screen import get  # noqa: E402

TS = "https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/"
FIELDS = ["TotalRevenue", "OperatingIncome", "PretaxIncome", "NetIncomeCommonStockholders", "NetIncomeContinuousOperations",
          "CostOfRevenue", "SellingGeneralAndAdministration", "InterestExpense", "InterestIncome",
          "DepreciationAmortizationDepletion", "DepreciationAndAmortization", "CapitalExpenditure", "OperatingCashFlow",
          "StockBasedCompensation", "TotalAssets", "CurrentAssets", "CurrentLiabilities", "AccountsReceivable", "NetPPE",
          "LongTermDebt", "CurrentDebt", "MinorityInterest", "CashCashEquivalentsAndShortTermInvestments",
          "OrdinarySharesNumber"]


def statements(sym):
    url = f"{TS}{sym}?type={','.join('annual' + f for f in FIELDS)}&period1=1420070400&period2=1800000000"
    out = {}
    for r in json.loads(get(url))["timeseries"]["result"]:
        k = r["meta"]["type"][0]
        for x in r.get(k) or []:
            if x and x.get("reportedValue"):
                out.setdefault(x["asOfDate"], {})[k.replace("annual", "")] = x["reportedValue"]["raw"]
    return out


def quote(sym):
    d = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=5d&interval=1d"))["chart"]["result"][0]["meta"]
    return d["regularMarketPrice"], d["regularMarketTime"], d.get("longName") or d.get("shortName") or sym


def m(x):
    return None if x is None else round(x / 1e6, 3)


def main(folder, tickers):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    raw = {t: {"statements": statements(t), "quote": quote(t)} for t in tickers}
    (folder / "yahoo_statements.json").write_text(json.dumps(raw, indent=1, sort_keys=True))
    cons = {r["ticker"]: r for r in csv.DictReader(open(folder / "consensus.csv"))} if (folder / "consensus.csv").exists() else {}
    wb = openpyxl.Workbook()
    vi = wb.active
    vi.title = "Valuation inputs"
    vcols = ["ticker", "company", "reporting_currency", "fiscal_year", "fy_end", "revenue", "operating_income", "pretax_income",
             "net_income_common", "d_and_a", "capex", "capex_software", "cfo", "stock_based_comp", "interest_expense",
             "interest_income", "debt", "corporate_cash", "shares_outstanding_m", "diluted_shares_m", "price_30oct",
             "consensus_revenue_growth_y1", "consensus_revenue_growth_y2", "consensus_revenue_growth_y3", "sources", "notes"]
    vi.append(vcols)
    rf = wb.create_sheet("Red flags")
    rcols = ["ticker", "period", "net_income_continuing", "total_assets", "total_assets_start_of_year", "long_term_debt",
             "current_assets", "current_liabilities", "cost_of_revenue", "revenue", "shares_outstanding_m", "receivables",
             "net_ppe", "depreciation", "sga", "cfo"]
    rf.append(rcols)
    wb.create_sheet("Risk").append(["ticker", "worst_calendar_year", "worst_return"])
    for t in tickers:
        s = raw[t]["statements"]
        years = sorted(d for d in s if s[d].get("TotalRevenue"))
        f0, f1 = s[years[-1]], s[years[-2]]
        da = f0.get("DepreciationAmortizationDepletion", f0.get("DepreciationAndAmortization"))
        nci = f0.get("MinorityInterest") or 0
        debt = (f0.get("CurrentDebt") or 0) + (f0.get("LongTermDebt") or 0) + nci
        c = cons.get(t, {})
        g = [float(c[k]) if c.get(k) not in (None, "") else None for k in ("y1", "y2", "y3")]
        price, when, name = raw[t]["quote"]
        vi.append([t, name, "USD", int(years[-1][:4]), years[-1], m(f0["TotalRevenue"]), m(f0.get("OperatingIncome")),
                   m(f0.get("PretaxIncome")), m(f0.get("NetIncomeCommonStockholders")), m(da), m(-f0.get("CapitalExpenditure", 0)), 0,
                   m(f0.get("OperatingCashFlow")), m(f0.get("StockBasedCompensation")), m(f0.get("InterestExpense")),
                   m(f0.get("InterestIncome")), m(debt), m(f0.get("CashCashEquivalentsAndShortTermInvestments")),
                   m(f0.get("OrdinarySharesNumber")), None, round(price, 2), *g,
                   f"Yahoo fundamentals-timeseries (annual, fiscal year ended {years[-1]}); price: Yahoo quote at {when} (unix time); "
                   f"consensus: {c.get('source') or 'MISSING'}",
                   (f"Debt includes non-controlling interests {m(nci):,.0f}; " if nci else "") + "finance leases MISSING (Yahoo does not separate them)"])
        for label, a, b in (("FY0", f0, f1), ("FY1", f1, s[years[-3]] if len(years) > 2 else {})):
            rf.append([t, label, m(a.get("NetIncomeContinuousOperations")), m(a.get("TotalAssets")), m(b.get("TotalAssets")),
                       m(a.get("LongTermDebt")), m(a.get("CurrentAssets")), m(a.get("CurrentLiabilities")), m(a.get("CostOfRevenue")),
                       m(a.get("TotalRevenue")), m(a.get("OrdinarySharesNumber")), m(a.get("AccountsReceivable")), m(a.get("NetPPE")),
                       m(a.get("DepreciationAmortizationDepletion", a.get("DepreciationAndAmortization"))),
                       m(a.get("SellingGeneralAndAdministration")), m(a.get("OperatingCashFlow"))])
    wb.save(folder / "Yahoo_Round2_data.xlsx")
    for r in vi.iter_rows(min_row=2, values_only=True):
        print(dict(zip(vcols, r)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
