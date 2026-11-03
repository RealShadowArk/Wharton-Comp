"""Round 2 for a teammate's workbook: risk, red flags, DCF, draft bear, scorecard.

Run: python tools/round2_team.py akshajp
Same method as Pat's nine (tools/round2_risk_redflags.py, tools/make_round2_dcfs.py):
- 60 monthly USD returns (Nov 2021-Oct 2026) vs SPY; also the full-history beta;
  worst complete calendar year through 2025; max position = $6,000 / worst loss.
- Piotroski and Beneish per the kit README (leverage test passes with zero debt both years).
- DCF: rates by currency (US 4.94%), year 1 = numeric guidance midpoint else
  consensus, years 2-3 consensus, fade to terminal growth; FY0 margin flat; reported
  D&A (sbc_pct 0); cash, debt and shares at the same date; first forecast year
  timed from the fiscal year-end.
- Bear = uniform DRAFT (years 1-3 growth halved, margin x 0.8) for Pat to replace.
"""
import csv
import math
import re
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from m03.dcf import value  # noqa: E402
from m03.run import load, run, wacc_for  # noqa: E402

RF = {"USD": 0.0494, "EUR": 0.0334, "INR": 0.073977, "CNY": 0.016266,  # CNY: China 10-year, 30 Oct 2026 (Akshat's source)
      "HKD": 0.03855, "GBP": 0.052917,  # HK and UK 10-year, 30 Oct 2026 (new-candidates Round 2 workbook, local_10y_yield)
      "DKK": 0.0315,  # Denmark 10-year, 30 Oct 2026 (groups 3-4 Round 2 workbook, local_10y_yield)
      "JPY": 0.02817,  # Japan 10-year, 30 Oct 2026 (wave 3 group 3 workbook, local_10y_yield)
      "TWD": 0.0203, "KRW": 0.04008}  # Taiwan and Korea 10-year, 30 Oct 2026 (wave 3 group 1 workbook, local_10y_yield)
RF_US, T_BILL = 0.0494, 0.04
VAL_DATE = date(2026, 10, 30)
TEAM = ROOT / "context" / "teammates_2026-11-03"
SETS = {
    "akshajp": dict(
        workbook=TEAM / "akshaj_p_final" / "Team_Round2_Akshaj_P.xlsx",
        yahoo=TEAM / "akshaj_p_final" / "Yahoo original CSVs",
        m12=[TEAM / "akshaj_p_final" / "Software.csv", TEAM / "akshaj_p_final" / "M12_peer_data.csv"],
        who="Akshaj P",
        notes={"KO": "2025 operating cash flow is low next to profit; check for one-off payments before trusting the cash check",
               "NKE": "FY2026 margin (8.2%) is held flat; Nike's margin is depressed, so the base case is a low-margin case",
               "NOW": "Year-1 growth is consensus (guidance covers subscription revenue only)"}),
    "akshat": dict(
        workbook=TEAM / "akshat_final" / "Akshat_Round2_updated.xlsx",
        yahoo=TEAM / "akshat_final" / "Yahoo Max",
        m12=[TEAM / "akshat_final" / "pharma_m12_research_inputs.csv", TEAM / "Akshat_digital_m12_research_inputs.csv"],
        alias={"9961": "9961.HK", "SNY": "SAN.PA"},
        series={"9961.HK": ("TCOM", None)},             # risk from the TCOM ADR (1 ADS = 1 share), USD
        fx={"SAN.PA": ("EURUSD=X", "mul")},             # EUR price x USD per EUR
        crp={"9961.HK": 0.0091},                         # China CRP (Damodaran 1 Jan 2026, secondary mirror; Pat 3 Nov)
        who="Akshat",
        notes={"9961.HK": "Valued in RMB (China 10-year 1.63% + China CRP 0.91%); 2025 profit includes RMB 19.4bn of one-off gains (M12 rank holds without them); risk from TCOM",
               "META": "VOO top-10 holding", "BKNG": "Own cash = cash - deferred merchant bookings (team convention)",
               "SAN.PA": "Valued in EUR; risk in USD", "NVS": "Year-1 consensus +1.3% (patent expiries)"}),
    "akshajk": dict(
        workbook=TEAM / "akshaj_k_final" / "Akshaj_Seven_Companies_Round2.xlsx",
        yahoo=TEAM / "akshaj_k_final" / "monthly_from_seven_workbook",  # his Yahoo Max monthly closes (ASML = USD ADR)
        m12=[ROOT / "outputs/new_candidates/M12_Semiconductors.csv", ROOT / "outputs/new_candidates/M12_Aerospace_and_defence.csv"],
        fy_end={"NVDA": "2026-01-25", "LRCX": "2026-06-28", "ASML": "2025-12-31", "GD": "2025-12-31",
                "HII": "2025-12-31", "ESLT": "2025-12-31", "QCOM": "2025-09-28"},
        rf_bounds={"ASML": {"FY0": (2709.0, 2725.5), "FY1": (3677.3, 3694.2)}},  # noncurrent borrowings 2,709 / 3,677.3 + finance leases 16.5 / 16.9 (split not disclosed)
        tax_override={"QCOM": (1 - (5541 + 5724) / 12663, "1 - (net income + one-off 5,724m deferred-tax valuation allowance) / pretax income (reversed in FY2026 per the July 2026 10-Q)")},
        who="Akshaj K (Akshaj R)",
        notes={"GD": "SG&A = reported G&A (no separate selling line, verified)", "HII": "SG&A = reported G&A (no separate selling line, verified)",
               "ASML": "Noncurrent debt 2,709 excl. finance leases (16.5 total, split not disclosed): red flags run at both ends; risk from the USD ADR",
               "NVDA": "VOO top-10 holding; consensus growth 91% / 68% / 30%",
               "ESLT": "Israel war exposure (see the Kenon note); interest expense MISSING (43.6 interest lines, 71.6 with factoring)",
               "QCOM": "Tied 2nd in Akshaj's six-company M12; FY2025 tax excludes the one-off 5,724m valuation allowance"}),
    "akshajr_new": dict(
        workbook=TEAM / "akshaj_k_final/CW_ASM_round2/CW_and_ASM_Round2.xlsx",
        yahoo=TEAM / "akshaj_k_final/CW_ASM_round2/Yahoo_Max_monthly",
        series={t: (f"{t}_Max_monthly_original", None) for t in ("CW", "ASM.AS", "SPY")},
        fx={"ASM.AS": ("EURUSD=X_Max_monthly_original", "mul")},
        m12=[ROOT / "outputs/new_candidates/M12_Semiconductors.csv", ROOT / "outputs/new_candidates/M12_Aerospace_and_defence.csv"],
        val_override={"ASM.AS": {"capex_software": 205.1 + 44.7}},  # capitalized development + intangible purchases (cash-flow statement)
        who="Akshaj R (new candidates CW, ASM International)",
        notes={"ASM.AS": "Valued in EUR; capex includes capitalized development 205.1 and intangible purchases 44.7 (IFRS capitalizes development; its amortization is in D&A), total 468.3",
               "CW": "Interest income MISSING (inside other income); no separate software capex"}),
    "aryu": dict(
        workbook=TEAM / "aryu_round2_pat/Aryu_Round2_2026-11-03" / "Aryu_Round2_filled.xlsx",
        yahoo=TEAM / "aryu_round2_pat/Aryu_Round2_2026-11-03" / "Yahoo_Max_Monthly_Originals",
        m12=[ROOT / "outputs/new_candidates/M12_Medtech.csv"],
        group={"CEG": "Power", "NRG": "Power"},
        m12_text={"CEG": "Not scored (EPS growth undefined: 2022 loss); power group not released",
                   "NRG": "No (power group not released; complete-only diagnostic 5 of 6, 0/32)"},
        fy_end={"CEG": "2025-12-31", "NRG": "2025-12-31"},
        val_override={"CEG": {"fiscal_year": 2025, "debt": 21543, "capex": 2949 + 1149, "d_and_a": 1957 + (2601 - 985)},  # D&A + nuclear-fuel amortization (capex includes nuclear fuel)  # borrowings (finance leases not quantified, R8); CEG + Calpine reported capex
                      "NRG": {"fiscal_year": 2025, "capex": round(1147 / 30713 * 33471, 1)},  # NRG's own capex / revenue on the pro forma revenue
                      "RMD": {"fiscal_year": 2026}, "ALC": {"fiscal_year": 2025}, "EW": {"fiscal_year": 2025}},
        g1_override={"CEG": (35850 / 36812 - 1, "consensus FY2026 revenue 35.85bn / 2025 pro forma 36,812"),
                     "NRG": (35310 / 33471 - 1, "consensus FY2026 revenue 35.31bn / 2025 pro forma 33,471")},
        who="Aryu (power, medtech; data filled by Pat)",
        notes={"CEG": "2025 pro forma with Calpine; debt = borrowings 21,543 (finance leases not quantified); capex = CEG 2,949 + Calpine 1,149 reported (no pro forma cash-flow statement); D&A 3,573 = pro forma 1,957 + CEG nuclear-fuel amortization 1,616 (cash-flow D&A 2,601 - income-statement 985), because capex includes nuclear fuel (Aryu's treatment); no losing calendar year (listed 2022)",
                "NRG": "2025 pro forma with the LS Power plants; debt includes 650 preferred; capex = NRG's 2025 capex ratio (3.7%) on pro forma revenue (ASSUMPTION); D&A 1,866 includes amortization of customer-acquisition costs whose cash cost sits in operating costs (generous)",
                "RMD": "Year 1 = midpoint of 5-7% core constant-currency guidance", "ALC": "Year 1 = midpoint of 5-7% constant-currency guidance; debt excludes 509 leases",
                "EW": "Year 1 = midpoint of 10-11% constant-currency guidance; continuing figures"}),
    "dxcm": dict(
        workbook=TEAM / "round2_groups34" / "Medtech_and_Software_Round2.xlsx",
        yahoo=TEAM / "round2_groups34" / "Medtech_and_Software_Yahoo_Max_Monthly",
        m12=[ROOT / "outputs/new_candidates/M12_Medtech.csv"],
        who="Group 3 (Dexcom)", notes={"DXCM": "Year 1 = midpoint of 12-13% guidance"}),
    "consumer_pharma": dict(
        workbook=TEAM / "round2_groups34" / "Consumer_Brands_and_Pharma_Round2.xlsx",
        yahoo=TEAM / "round2_groups34" / "Consumer_Brands_and_Pharma_Yahoo_Max_Monthly",
        m12=[ROOT / "outputs/new_candidates/M12_Consumer_brands.csv", ROOT / "outputs/new_candidates/M12_Pharmaceuticals_and_Biotechnology.csv"],
        fx={"ADS.DE": ("EURUSD=X", "mul")},  # HLN and NVO risk from their USD ADRs
        who="Group 4 (Lululemon, Haleon, Novo Nordisk, adidas)",
        notes={"LULU": "Fiscal year ended 1 Feb 2026; year 1 = midpoint of the -5% to -7% guidance",
                "HLN": "Valued in GBP (UK 10-year 5.29%); year 1 = organic guidance about 2.5%; risk from the USD ADR",
                "NVO": "Valued in DKK (Denmark 10-year 3.15%); dilution MISSING (outstanding shares used); capex 19.5% of revenue (capacity build) held for ten years; risk from the USD ADR",
                "ADS.DE": "Valued in EUR; dilution and stock pay MISSING (outstanding shares used); worst year from 2004 only (EURUSD history)"}),
    "wave3_g3": dict(
        workbook=ROOT / "inputs/m12/wave3_2026-11-03/return1" / "New_Companies_Round2.xlsx",
        yahoo=ROOT / "inputs/m12/wave3_2026-11-03/return1" / "Yahoo Finance Max Monthly",
        m12=[ROOT / "outputs/new_candidates/M12_Exchanges_and_data.csv", ROOT / "outputs/new_candidates/M12_IT_services.csv",
             ROOT / "outputs/new_candidates/M12_Internet_and_Digital_Platforms.csv"],
        skip={"B3SA3.SA", "BABA"},  # B3: bank-like and no operating income; Alibaba: negative free cash flow
        fx={"8697.T": ("JPY=X", "div"), "WKL.AS": ("EURUSD=X", "mul"), "WIPRO.NS": ("INR=X", "div"), "0700.HK": ("HKD=X", "div")},
        crp={"0700.HK": 0.0091, "PDD": 0.0091},  # China country risk premium, as for Trip.com (Pat 3 Nov)
        fy_end={"0700.HK": "2025-12-31", "PDD": "2025-12-31"},
        group={"0700.HK": "Internet and Digital Platforms", "PDD": "Internet and Digital Platforms"},
        m12_text={"0700.HK": "Screened out (bank-like: loan receivables inside operating cash flow) unless Pat overrules",
                  "PDD": "Screened out (bank-like per the researcher: merchant deposits inside operating cash flow) unless Pat overrules"},
        val_override={"WKL.AS": {"capex": 303}, "TRU": {"capex": 326.0},
                      "PDD": {"capex": 1145.077, "cfo": None},  # cash check skipped: CFO includes merchant payables +15,328 and deposits +1,248
                      "WIPRO.NS": {"d_and_a": 29107 - 851}, "DOX": {"d_and_a": 128.799 + 61.469}},
        who="Wave 3, group 3 (exchanges, IT services, internet)",
        notes={"8697.T": "Valued in JPY (Japan 10-year 2.82%); clearing balances excluded from cash",
                "WKL.AS": "Capex 303 = total net capital expenditure (combined line); D&A includes impairments",
                "TRU": "Capex 326 = reported capital expenditures (combined)",
                "WIPRO.NS": "Valued in INR; D&A = 29,107 less the disclosed 851 intangible impairment",
                "DOX": "D&A = depreciation 128.8 + purchased-intangible amortization 61.5",
                "0700.HK": "Valued in RMB (China 10-year + 0.91% CRP); bank-like flag: Pat decides",
                "PDD": "Valued in RMB per ADS (China 10-year + 0.91% CRP); capex = combined line; screened out as bank-like by the researcher (merchant deposits in CFO): Pat decides",
                "MTCH": "Year 1 = midpoint of the -2.2% to +1.4% guidance"}),
    "wave3_g1": dict(
        workbook=ROOT / "inputs/m12/wave3_2026-11-03/return2/New_companies" / "New_companies_Round2.xlsx",
        yahoo=ROOT / "inputs/m12/wave3_2026-11-03/return2/New_companies" / "Yahoo_Max_monthly",
        series={t: (f"{t}_Max_monthly_original", None) for t in ("NXPI", "2454.TW", "005930.KS", "8035.T", "TXT", "AIR.PA", "LDO.MI", "HO.PA", "SPY")},
        fx={"2454.TW": ("TWD=X_Max_monthly_original", "div"), "005930.KS": ("KRW=X_Max_monthly_original", "div"),
             "8035.T": ("JPY=X_Max_monthly_original", "div"), "AIR.PA": ("EURUSD=X_Max_monthly_original", "mul"),
             "LDO.MI": ("EURUSD=X_Max_monthly_original", "mul"), "HO.PA": ("EURUSD=X_Max_monthly_original", "mul")},
        m12=[ROOT / "outputs/new_candidates/M12_Semiconductors.csv", ROOT / "outputs/new_candidates/M12_Aerospace_and_defence.csv"],
        skip={"TXT"},  # bank-like (Textron Financial) and no operating-income line or classified balance sheet
        fx_fix={"KRW=X_Max_monthly_original": ROOT / "inputs/m12/wave3_2026-11-03/return2/New_companies" / "Federal_Reserve_DEXKOUS_original.csv", "TWD=X_Max_monthly_original": ROOT / "inputs/m12/wave3_2026-11-03/return2/New_companies" / "Federal_Reserve_DEXTAUS_original.csv", "JPY=X_Max_monthly_original": ROOT / "inputs/m12/wave3_2026-11-03/return2/New_companies" / "Federal_Reserve_DEXJPUS_original.csv", "EURUSD=X_Max_monthly_original": ROOT / "inputs/m12/wave3_2026-11-03/return2/New_companies" / "Federal_Reserve_DEXUSEU_original.csv"},  # Yahoo FX glitches (e.g. KRW 0.11 in 2015-16)
        fy_end={"AIR.PA": "2025-12-31"}, group={"AIR.PA": "Aerospace and defence"},
        m12_text={"AIR.PA": "Screened out (bank-like: Airbus Bank) unless Pat overrules"},
        val_override={"AIR.PA": {"capex": 3964, "corporate_cash": 17221},  # combined capex; cash INCLUDES Airbus Bank (scope unverified: upper bound)
                      "LDO.MI": {"capex": 1016}, "HO.PA": {"capex": 756.7, "pretax_income": 2036.8}},
        who="Wave 3, group 1 (semiconductors, aerospace and defence)",
        notes={"2454.TW": "Valued in TWD; consensus growth 15% / 77% / 69% (check before relying)",
                "005930.KS": "Valued in KRW; consensus growth 117% / 40% / 11% (check before relying); preferred shares in the share count; stock pay MISSING",
                "8035.T": "Valued in JPY; year 1 = FY Mar 2027 guidance midpoint 51%; dilution and stock pay MISSING",
                "AIR.PA": "Valued in EUR; capex = combined line; cash 17,221 includes Airbus Bank (upper bound); bank-like flag: Pat decides",
                "LDO.MI": "Valued in EUR; capex = combined line", "HO.PA": "Valued in EUR; capex = combined line; pretax = net income + tax"}),
    "newcands": dict(
        workbook=ROOT / "inputs/m12/new_candidates_2026-11-03/final_2026-11-03/Wharton_Candidates_Missing_Audit/Wharton_Candidates_Round2_Missing_Audit.xlsx",
        yahoo=ROOT / "inputs/m12/new_candidates_2026-11-03/final_2026-11-03/Wharton_Candidates_Missing_Audit/Yahoo_Max_Monthly",
        m12=[ROOT / "outputs/new_candidates/M12_Exchanges_and_data.csv"],
        fx={"0388.HK": ("HKD=X", "div"), "AUTO.L": ("GBPUSD=X", "mul")},  # HKD per USD; USD per GBP (pence scale cancels in returns)
        fy_end={"AUTO.L": "2026-03-31"}, group={"AUTO.L": "Internet and Digital Platforms"},
        m12_text={"AUTO.L": "No (group not released; complete-only diagnostic 6 of 10, 2/32)"},
        val_override={"0388.HK": {"capex": 1733}},  # ex the one-off HK$3,148m headquarters purchase (ASSUMPTION, see note)
        tax_continuing={"TW"},  # Up-C: tax from net income before non-controlling interests (LLC units are in the share count)
        who="New candidates (HKEX, Tradeweb, Auto Trader)",
        notes={"0388.HK": "Valued in HKD (HK 10-year 3.855%). Capex 1,733 excludes the one-off HK$3,148m headquarters purchase (with it, capex is 20.6% of revenue held for ten years); operating cash flow includes clearing and margin-fund movements, so the cash check is not meaningful",
               "TW": "Tax 21.6% from net income before non-controlling interests (Up-C); capex includes capitalized software 62.5",
               "AUTO.L": "Valued in GBP (UK 10-year 5.29%); shares at 31 Mar 2026 (buybacks since: 760.6m on 19 Oct)"}),
}
TEXT = {"ticker", "company", "peer_group", "reporting_currency", "guidance_next_fy_revenue_growth", "guidance_basis",
        "cash_note", "long_term_target", "sources", "notes", "period", "guidance_fy2026_revenue_growth_numeric", "source", "listing_used_for_prices", "price_currency"}


def clean(d):
    """Numeric fields: numbers (or numbers stored as text) stay; other text (MISSING, N/A ...) becomes None."""
    def num(v):
        if isinstance(v, (int, float)) or v is None:
            return v
        try:
            return float(str(v).replace(",", ""))
        except ValueError:
            return None
    return {k: (v if k in TEXT else num(v)) for k, v in d.items()}


def num_guidance(v):
    """Numeric guidance midpoint, or None (proxy, approximate or one-sided)."""
    if isinstance(v, (int, float)):
        return float(v)
    if not v or any(s in str(v) for s in ("proxy", "≈", "≥", "≤", "~")):
        return None
    pcts = [float(x) / 100 for x in re.findall(r"[-+]?\d+(?:\.\d+)?(?=%)", str(v))]
    return sum(pcts) / len(pcts) if len(pcts) == 2 else None


def read_series(path):
    out = {}
    for r in csv.DictReader(open(path)):
        m = r["Date"][:7]
        if r["Date"].endswith("-01") and r.get("Adj Close") not in (None, "", "null") and m <= "2026-10":
            out[m] = float(r["Adj Close"])
    return out


def fed_month_end(path):
    """Federal Reserve daily FX (H.10 / FRED CSV) -> {YYYY-MM: last value in that month}."""
    out = {}
    for r in csv.reader(open(path, encoding="utf-8-sig")):
        if len(r) == 2 and r[1] not in ("", ".") and r[0][:4].isdigit():
            out[r[0][:7]] = float(r[1])
    return out


def monthly(folder, tickers, series=None, fx=None, fx_fix=None):
    """Monthly USD adjusted closes: {month: {ticker: price}}. series maps a ticker to another file
    (e.g. an ADR); fx converts a local-currency series with a Yahoo FX file ('mul' for USD per unit).
    fx_fix maps a Yahoo FX file to a Federal Reserve file in the same units: a Yahoo month more than
    20% away from the Fed month-end value is a known Yahoo glitch and is replaced by the Fed value."""
    series, fx, fx_fix = series or {}, fx or {}, fx_fix or {}
    out = {}
    for t in ["SPY"] + tickers:
        src = read_series(folder / f"{series.get(t, (t,))[0]}.csv")
        if t in fx:
            rate = read_series(folder / f"{fx[t][0]}.csv")
            if fx[t][0] in fx_fix:
                fed = fed_month_end(fx_fix[fx[t][0]])
                rate = {m: (fed[m] if m in fed and abs(v / fed[m] - 1) > 0.2 else v) for m, v in rate.items()}
            src = {m: v * rate[m] if fx[t][1] == "mul" else v / rate[m] for m, v in src.items() if m in rate}
        for m, v in src.items():
            out.setdefault(m, {})[t] = v
    return out


def beta_stats(p, t, start):
    ms = [m for m in sorted(p) if m >= start and t in p[m] and "SPY" in p[m]]
    s = [p[b][t] / p[a][t] - 1 for a, b in zip(ms, ms[1:])]
    m = [p[b]["SPY"] / p[a]["SPY"] - 1 for a, b in zip(ms, ms[1:])]
    sb, mb = sum(s) / len(s), sum(m) / len(m)
    beta = sum((x - sb) * (y - mb) for x, y in zip(s, m)) / sum((y - mb) ** 2 for y in m)
    vol = math.sqrt(sum((x - sb) ** 2 for x in s) / (len(s) - 1)) * math.sqrt(12)
    years = len(s) / 12
    cagr = (p[ms[-1]][t] / p[ms[0]][t]) ** (1 / years) - 1
    rm = (p[ms[-1]]["SPY"] / p[ms[0]]["SPY"]) ** (1 / years) - 1
    return beta, vol, cagr, rm, len(s)


def worst_year(p, t):
    best = (None, 9.0)
    for y in range(1986, 2026):
        a, b = p.get(f"{y - 1}-12", {}).get(t), p.get(f"{y}-12", {}).get(t)
        if a and b and b / a - 1 < best[1]:
            best = (y, b / a - 1)
    return best


def red_flags(a, b, cfo):
    roa = lambda x: x["net_income_continuing"] / x["total_assets_start_of_year"]
    lev = lambda x: (x["long_term_debt"] or 0) / ((x["total_assets"] + x["total_assets_start_of_year"]) / 2)
    cr = lambda x: x["current_assets"] / x["current_liabilities"]
    gm = lambda x: None if x["cost_of_revenue"] is None else (x["revenue"] - x["cost_of_revenue"]) / x["revenue"]
    turn = lambda x: x["revenue"] / x["total_assets_start_of_year"]
    tests = {"1 ROA > 0": roa(a) > 0, "2 CFO > 0": None if cfo is None else cfo > 0, "3 ROA up": roa(a) > roa(b),
             "4 CFO > net income": None if cfo is None else cfo > a["net_income_continuing"],
             "5 leverage down": lev(a) < lev(b) or lev(a) == lev(b) == 0,
             "6 current ratio up": cr(a) > cr(b), "7 no new shares": a["shares_outstanding_m"] <= b["shares_outstanding_m"],
             "8 gross margin up": None if gm(a) is None else gm(a) > gm(b), "9 asset turnover up": turn(a) > turn(b)}
    def safe(f):
        try:
            return f()
        except (TypeError, ZeroDivisionError):
            return None
    idx = {"DSRI": lambda: (a["receivables"] / a["revenue"]) / (b["receivables"] / b["revenue"]),
           "GMI": lambda: None if gm(a) is None else gm(b) / gm(a),
           "AQI": lambda: (1 - (a["current_assets"] + a["net_ppe"]) / a["total_assets"]) / (1 - (b["current_assets"] + b["net_ppe"]) / b["total_assets"]),
           "SGI": lambda: a["revenue"] / b["revenue"],
           "DEPI": lambda: (b["depreciation"] / (b["depreciation"] + b["net_ppe"])) / (a["depreciation"] / (a["depreciation"] + a["net_ppe"])),
           "SGAI": lambda: (a["sga"] / a["revenue"]) / (b["sga"] / b["revenue"]),
           "TATA": lambda: (a["net_income_continuing"] - cfo) / a["total_assets"],
           "LVGI": lambda: ((a["current_liabilities"] + (a["long_term_debt"] or 0)) / a["total_assets"])
                   / ((b["current_liabilities"] + (b["long_term_debt"] or 0)) / b["total_assets"])}
    idx = {k: safe(f) for k, f in idx.items()}
    coef = {"DSRI": 0.920, "GMI": 0.528, "AQI": 0.404, "SGI": 0.892, "DEPI": 0.115, "SGAI": -0.172, "TATA": 4.679, "LVGI": -0.327}
    missing = [k for k, v in idx.items() if v is None]
    m = None if missing else -4.84 + sum(coef[k] * v for k, v in idx.items())
    checked = [v for v in tests.values() if v is not None]
    return sum(checked), len(checked), [k for k, v in tests.items() if v is False], (m, missing)


def fade(g1, g2, g3, term):
    return [g1, g2, g3] + [g3 + (term - g3) * k / 7 for k in range(1, 8)]


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["field", "value", "unit", "label", "source", "note"])
        w.writerows(rows)


def main(key):
    cfg = SETS[key]
    wb = openpyxl.load_workbook(cfg["workbook"], data_only=True)
    sheet = lambda n: [r for r in wb[n].iter_rows(values_only=True) if any(v not in (None, "") for v in r)]
    vr, rr, kr = sheet("Valuation inputs"), sheet("Red flags"), sheet("Risk")
    val = {r[vr[0].index("ticker")]: clean(dict(zip(vr[0], r))) for r in vr[1:]
           if isinstance(r[vr[0].index("ticker")], str) and isinstance(r[vr[0].index("revenue")], (int, float))}
    red = {(r[0], {"FY-1": "FY1"}.get(r[1], r[1])): clean(dict(zip(rr[0], r))) for r in rr[1:]}
    for k, extra in cfg.get("rf_proxies", {}).items():
        red[k].update(extra)
    risk_tab = {r[0]: dict(zip(kr[0], r)) for r in kr[1:]}
    for t, extra in cfg.get("val_override", {}).items():
        val[t].update(extra)
    tickers = [t for t in val if t not in cfg.get("skip", ())]
    fy_end, group, m12 = {}, {}, {}
    from m12.score import load as m12load, score_all, stability
    fy_end.update({t: date.fromisoformat(d) for t, d in cfg.get("fy_end", {}).items()})
    group.update(cfg.get("group", {}))
    m12.update(cfg.get("m12_text", {}))
    for f in cfg.get("m12", []):
        rows = m12load(f)
        alias = cfg.get("alias", {})
        for r in rows:
            r["ticker"] = alias.get(r["ticker"], r["ticker"])
            if r.get("fy_end_date"):
                fy_end[r["ticker"]] = date.fromisoformat(str(r["fy_end_date"])[:10])
        for g, res in score_all(rows).items():
            st = stability(res) if res["released"] else {}
            ranked = [t for _, t in sorted(((v, t) for t, v in res["totals"].items() if v is not None), reverse=True)]
            for t in res["raw"]:
                group[t] = g
                if t in ranked:
                    k = st.get(t, (0, 32))[0]
                    ok = t in res["shortlist"] and k >= 24
                    m12[t] = f"{'Yes' if ok else 'No'}: {ranked.index(t) + 1} of {len(ranked)}, {k}/32"
    p = monthly(Path(cfg["yahoo"]), tickers, cfg.get("series"), cfg.get("fx"), cfg.get("fx_fix")) if cfg.get("yahoo") else None
    m3 = ROOT / "inputs" / "m03"
    res = []
    for t in tickers:
        v = val[t]
        cur = v["reporting_currency"]
        rf = RF[cur]
        g_term = 1.03 * (1 + rf) / (1 + RF_US) - 1
        rev = v["revenue"]
        tax = (v["pretax_income"] - v["net_income_common"]) / v["pretax_income"]
        tax_note = "1 - net income / pretax income"
        if t in cfg.get("tax_continuing", ()):
            tax = 1 - red[(t, "FY0")]["net_income_continuing"] / v["pretax_income"]
            tax_note = "1 - net income before non-controlling interests / pretax income"
        if t in cfg.get("tax_override", {}):
            tax, tax_note = cfg["tax_override"][t]
        if not 0 <= tax < 1:  # e.g. a discontinued-operations gain: use continuing net income
            tax = 1 - red[(t, "FY0")]["net_income_continuing"] / v["pretax_income"]
            tax_note = "1 - continuing net income / pretax income (net income includes discontinued operations)"
        if not 0 <= tax < 1:
            raise ValueError(f"{t}: no valid tax rate; needs a decision")
        margin = v["operating_income"] / rev
        g_guid = num_guidance(v.get("guidance_next_fy_revenue_growth", v.get("guidance_fy2026_revenue_growth_numeric")))
        if g_guid is None and v.get("guidance_growth_low") is not None and v.get("guidance_growth_high") is not None:
            g_guid = (v["guidance_growth_low"] + v["guidance_growth_high"]) / 2  # midpoint of the published range (team method)
        g1 = g_guid if g_guid is not None else v["consensus_revenue_growth_y1"]
        g1_note = ""
        if t in cfg.get("g1_override", {}):
            g1, g1_note = cfg["g1_override"][t]
        if v["consensus_revenue_growth_y3"] is None:  # year-3 consensus MISSING: fade starts after year 2
            g2 = v["consensus_revenue_growth_y2"]
            growth = [g1, g2] + [g2 + (g_term - g2) * k / 8 for k in range(1, 9)]
            g1_note += ("; " if g1_note else "") + "year-3 consensus MISSING: fade to terminal growth starts after year 2"
        else:
            growth = fade(g1, v["consensus_revenue_growth_y2"], v["consensus_revenue_growth_y3"], g_term)
        fy1_end = fy_end[t].replace(year=fy_end[t].year + 1)
        to_first = round((fy1_end - VAL_DATE).days / 365.25, 2)
        rolled = ""
        if to_first <= 0:  # next fiscal year already ended before 30 Oct (e.g. Qualcomm, September year-end)
            rev = rev * (1 + growth[0])
            growth = growth[1:] + [g_term]
            fy1_end = fy1_end.replace(year=fy1_end.year + 1)
            to_first = round((fy1_end - VAL_DATE).days / 365.25, 2)
            rolled = (f"; FY{v['fiscal_year'] + 1} ended before the valuation date: base revenue = FY{v['fiscal_year']} x (1 + year-1 consensus), "
                      "its cash flow treated as already paid out (cash and debt at the FY0 year-end)")
        da, capex = v["d_and_a"] / rev, (v["capex"] + (v["capex_software"] or 0)) / rev
        S = f"{cfg['workbook'].name} (Valuation inputs; source ledger 'Round 2 sources.csv')"
        rows = [
            ("ticker", t, "", "RESEARCH", S, group.get(t, "")),
            ("valuation_date", "2026-10-30", "date", "CASE", "Price date", ""),
            ("price", v["price_30oct"], cur, "RESEARCH", S, "30 Oct 2026 close, checked in WInS by the teammate"),
            ("base_year", v["fiscal_year"], "", "RESEARCH", S, f"Fiscal year ended {fy_end[t]}"),
            ("base_revenue", round(rev, 3), f"{cur} m", "RESEARCH" if not rolled else "ASSUMPTION", S, rolled.lstrip("; ")),
            ("growth", ";".join(f"{g:.4f}" for g in growth), "decimal", "ASSUMPTION", "Standard method (Pat, 3 Nov)",
             ("Year 1 guidance midpoint" if g_guid is not None and t not in cfg.get("g1_override", {}) else "Year 1 consensus") + "; years 2-3 consensus; fade to terminal growth"
             + (f" ({g1_note})" if g1_note else "")),
            ("ebit_margin", ";".join([f"{margin:.5f}"] * 10), "decimal", "ASSUMPTION", "Standard method: FY0 operating margin held flat", ""),
            ("tax_rate", round(tax, 4), "decimal", "RESEARCH", S, tax_note),
            ("da_pct", ";".join([f"{da:.5f}"] * 10), "decimal", "RESEARCH", S, "Reported D&A / revenue; stock pay stays in EBIT (sbc_pct 0)"),
            ("capex_pct", ";".join([f"{capex:.5f}"] * 10), "decimal", "RESEARCH", S, ""),
            ("nwc_pct_of_change", 0.0, "decimal", "ASSUMPTION", "Kit default", ""),
            ("risk_free", rf, "decimal", "RESEARCH", "US Treasury 10-year par CMT, 30 Oct 2026" if cur == "USD" else "Local 10-year, 30 Oct 2026", ""),
            ("beta", 1.0, "", "ASSUMPTION", "Standard method", ""),
            ("beta_measured", round(beta_stats(p, t, "2021-10")[0] if p else cfg["betas"][t][0], 3), "", "RESEARCH",
             "60 monthly USD returns vs SPY, Nov 2021-Oct 2026" + ("" if p else " (teammate's calculation; recompute from the Yahoo CSVs)"), ""),
            ("equity_premium", 0.05 + cfg.get("crp", {}).get(t, 0), "decimal", "ASSUMPTION",
             "Kit default 5%" + (f" + country risk premium {cfg['crp'][t]:.2%}" if t in cfg.get("crp", {}) else ""), ""),
            ("pre_tax_cost_of_debt", round(rf + 0.005, 6), "decimal", "ASSUMPTION", "Kit default: 10-year + 0.5 points", ""),
            ("equity_value_for_weights", round(v["price_30oct"] * v["shares_outstanding_m"], 2), f"{cur} m", "RESEARCH", "Price x shares", ""),
            ("debt_value_for_weights", v["debt"], f"{cur} m", "RESEARCH", S, ""),
            ("terminal_growth", round(g_term, 5), "decimal", "ASSUMPTION", "3% in USD, converted by the rate gap", ""),
            ("return_on_new_capital", 0.15, "decimal", "ASSUMPTION", "Kit default", ""),
            ("debt", v["debt"], f"{cur} m", "RESEARCH", S, ""),
            ("non_operating_assets", v["corporate_cash"], f"{cur} m", "RESEARCH", S, "Corporate cash"),
            ("diluted_shares", v["diluted_shares_m"] or v["shares_outstanding_m"], "m", "RESEARCH", S,
             "Shares at the cash-and-debt date plus dilution (teammate's ledger)" if v["diluted_shares_m"] else "Dilution MISSING: shares outstanding used (understates the share count slightly)"),
            ("years_to_first_cash_flow", to_first, "years", "ASSUMPTION", f"Valuation date to the end of FY{v['fiscal_year'] + 1} ({fy1_end})", ""),
            ("first_year_fraction", 1.0, "", "ASSUMPTION", "Method", "Cash and debt at the FY0 year-end"),
            ("sbc_pct", 0, "decimal", "ASSUMPTION", "Method", "0 because da_pct is reported D&A"),
        ]
        write(m3 / f"{t}_dcf_inputs.csv", rows)
        bear = []
        for r in rows:
            r = list(r)
            if r[0] == "growth":
                r[1] = ";".join(f"{g:.4f}" for g in [x / 2 for x in growth[:3]] + [growth[2] / 2 + (g_term - growth[2] / 2) * k / 7 for k in range(1, 8)])
                r[5] = "DRAFT bear: years 1-3 growth halved. Pat replaces or justifies it"
            if r[0] == "ebit_margin":
                r[1], r[5] = ";".join([f"{margin * 0.8:.5f}"] * 10), "DRAFT bear: margin x 0.8"
            bear.append(r)
        write(m3 / f"{t}bear_dcf_inputs.csv", bear)
        pp, vv, shift, price = run(t)
        _, raw, _ = load(t)
        if p:
            b5, vol, cagr, rm, _ = beta_stats(p, t, "2021-10")
            bf, _, _, _, nf = beta_stats(p, t, "1900-01")
        else:
            (b5, bf, nf), vol, cagr, rm = cfg["betas"][t], None, None, None
        at = lambda b: value(replace(pp, wacc=wacc_for(raw, b)))["per_share"]
        _, bv, _, _ = run(t + "bear")
        wy = worst_year(p, t) if p else (risk_tab[t]["worst_calendar_year"], risk_tab[t]["worst_return"])
        a, b = red[(t, "FY0")], red[(t, "FY1")]
        bounds = cfg.get("rf_bounds", {}).get(t)
        if bounds:
            outs = [red_flags(dict(a, long_term_debt=bounds["FY0"][i]), dict(b, long_term_debt=bounds["FY1"][i]), a["cfo"]) for i in (0, 1)]
            pio, pio_n, fails, mscore = outs[0]
            if (outs[0][0], round(outs[0][3][0], 2)) != (outs[1][0], round(outs[1][3][0], 2)):
                fails = fails + [f"bounds differ: {outs[1][0]}/{outs[1][1]}, M {outs[1][3][0]:.2f} at the upper bound"]
        else:
            pio, pio_n, fails, mscore = red_flags(a, b, a["cfo"])
        model_cash = v["operating_income"] * (1 - tax) + v["d_and_a"] - v["capex"]
        if v["cfo"] is None or v["stock_based_comp"] is None:  # cash check needs both
            rep_cash = None
        else:
            rep_cash = v["cfo"] - v["capex"] - v["stock_based_comp"] + (v["interest_expense"] or 0) * (1 - tax)
        da_rep = None if rep_cash is None else pp.da_pct[0] + (rep_cash - model_cash) / rev
        up, down = vv["per_share"] / price - 1, bv["per_share"] / price - 1
        res.append(dict(t=t, g=group.get(t, ""), price=price, cur=cur, v1=vv["per_share"], v5=at(b5), vf=at(bf), b5=b5, bf=bf, nf=nf,
                        rep=None if da_rep is None else value(replace(pp, da_pct=(da_rep,) * 10))["per_share"], shift=shift, bear=bv["per_share"], up=up, down=down,
                        ratio="no upside" if up <= 0 else ("no downside" if down >= 0 else f"{up / -down:.2f}"),
                        conv=None if rep_cash is None else model_cash / rep_cash, vol=vol, cagr=cagr, rm=rm, sharpe=None if vol is None else (cagr - T_BILL) / vol,
                        wy=wy, maxpos=6000 / -wy[1] if wy[1] < 0 else None, pio=f"{pio}/{pio_n}", fails="; ".join(fails),
                        m=f"NOT CHECKED ({', '.join(mscore[1])} MISSING)" if mscore[0] is None else f"{mscore[0]:.2f}", m12=m12.get(t, "MISSING"),
                        note=cfg["notes"].get(t, "")))
    report(key, cfg, res)


def report(key, cfg, res):
    L = [f"# Round 2 scorecard: {cfg['who']} (TEST preview, {date.today()})", "",
         "Generated by `python tools/round2_team.py " + key + "` with the same method as Pat's nine. Bear cases are a uniform DRAFT "
         "(years 1-3 growth halved, margin x 0.8) for Pat to replace. Values are research estimates, never price targets, returns or position sizes.", "",
         "| Group | Ticker | Price | Value (beta 1.0) | Value / price | At 5-year beta | At full-history beta | On reported cash flow | Price implies (growth shift) | Bear / price | Upside / downside |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        sh = "n/a" if r["shift"] is None else f"{r['shift']:+.1%}"
        L.append(f"| {r['g']} | {r['t']} | {r['price']:,.2f} {r['cur']} | {r['v1']:,.2f} | {r['v1'] / r['price']:.2f} | "
                 f"{r['v5'] / r['price']:.2f} (beta {r['b5']:.2f}) | {r['vf'] / r['price']:.2f} (beta {r['bf']:.2f}, {r['nf']} months) | "
                 + ("MISSING" if r["rep"] is None else f"{r['rep'] / r['price']:.2f}") + f" | {sh} | {r['bear'] / r['price']:.2f} | {r['up']:+.0%} / {r['down']:+.0%} = {r['ratio']} |")
    L += ["", "## Tests", "",
          "| Ticker | 1. M12 top 2 and robust | 2. Value > price at beta 1.0, 5-year and full-history beta | 3. Upside/downside >= 1.0 | "
          "4. Piotroski, Beneish | Worst year (max position) | 5-year return a year, volatility, Sharpe | Cash check | Note |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        t2 = "PASS" if min(r["v1"], r["v5"], r["vf"]) > r["price"] else "fail"
        t3 = "PASS" if r["ratio"] == "no downside" or (r["ratio"] != "no upside" and float(r["ratio"]) >= 1) else "fail"
        mp = "no losing year" if r["maxpos"] is None else f"${r['maxpos']:,.0f}"
        L.append(f"| {r['t']} | {r['m12']} | {t2} | {t3} | {r['pio']} (fails: {r['fails'] or 'none'}), {r['m']} | "
                 f"{r['wy'][0]}: {r['wy'][1]:.1%} ({mp}) | "
                 + ("MISSING until the Yahoo CSVs arrive" if r["vol"] is None else f"{r['cagr']:+.1%}, {r['vol']:.0%}, {r['sharpe']:.2f}")
                 + f" | {'MISSING' if r['conv'] is None else format(r['conv'], '.2f')} | {r['note']} |")
    L += ["", (f"S&P 500 (SPY) compound return over the same window: {res[0]['rm']:+.1%} a year; " if res[0]["rm"] is not None
               else "Betas and worst years are the teammate's own calculations until the Yahoo CSVs arrive; ") + "risk-free 4.00% (3-month T-bill, 30 Oct).",
          "Cash check = model year-0 free cash flow / reported cash flow (CFO - capex - stock-based pay + after-tax interest); above about 1.10 the model is generous."]
    out = ROOT / "outputs" / "round2" / f"Round2_scorecard_{key}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1])
