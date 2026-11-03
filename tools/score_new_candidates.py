"""Score the 67 new candidates against each industry's existing peers (M12, TEST preview, 3 Nov 2026).

Run: python tools/score_new_candidates.py
Writes outputs/new_candidates/M12_<industry>.csv (inputs as scored) and
outputs/new_candidates/M12_new_candidates_summary.md.

Screens applied to new names before scoring (team rules, 1-3 Nov):
  not_being_acquired = N -> out; bank_like = Y -> out (Pat may overrule);
  operating cash flow - capex <= 0 -> out; market cap below $2bn -> out.
Combined capex lines (PP&E + software in one cash line) are accepted (Pat's
exception); in Payments (rule R4) their software field is set to 0 so the
same spending is not added twice.

"Complete-only" ranks every complete company even when the group gate
(5 complete and 80% coverage) fails. It is a DIAGNOSTIC, labelled as such.
M12 is a research filter, never a value, a return or a weight.
"""
import csv
import sys
import zipfile
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from m12.score import MEASURES, score_group, stability  # noqa: E402

NC = ROOT / "inputs" / "m12" / "new_candidates_2026-11-03"
FIN = NC / "final_2026-11-03"
T3 = ROOT / "context" / "teammates_2026-11-03"
OUT = ROOT / "outputs" / "new_candidates"
COLS = ["peer_group", "ticker", "company", "reporting_currency", "fiscal_year", "fy_end_date",
        "revenue_fy0", "revenue_fy3", "operating_income_fy0", "pretax_income_fy0",
        "total_assets_fy0", "total_assets_fy1", "total_debt_fy0", "current_assets_fy0",
        "current_liabilities_fy0", "inventory_fy0", "total_equity_fy0", "eps_diluted_fy0",
        "eps_diluted_fy3", "eps_cont_fy0", "eps_cont_fy3", "earnings_common_fy0", "cfo_fy0",
        "capex_fy0", "capex_software_fy0", "shares_outstanding_m", "price",
        "market_cap_cutoff_proxy_m", "source", "new"]
# Combined cash purchases of PP&E and intangibles/software, used where the PP&E-only line is not reported
# (Pat's combined-capex exception; values verified by the researcher and recorded in the MISSING notes).
COMBINED_CAPEX = {"OR.PA": (1495.3, "L'Oreal combined PP&E + intangibles purchases (Consumer_Brands_and_Pharma MISSING.csv)"),
                  "GE": (1273, "GE combined PP&E + internal-use software (6_Semiconductors_and_Aerospace Missing fields)"),
                  # wave 3 (group 3 return, 3 Nov)
                  "WKL.AS": (303, "Wolters Kluwer total net capital expenditure (PP&E + intangibles), notes"),
                  "TRU": (326.0, "TransUnion capital expenditures as reported (PP&E + software)"),
                  "PDD": (1145.077, "PDD combined purchases of property, equipment, software and intangibles")}
# Facts that fill an EPS blank: the issuer reports no potential shares, so diluted EPS = basic EPS.
EPS_FACTS = {"8697.T": (76.81, 44.02, "JPX omits diluted EPS (no potential shares): basic EPS, split-adjusted")}
# Approximate 30 Oct 2026 USD per unit, ONLY for the $2bn size screen (never used in scores).
USD_PER = {"USD": 1, "EUR": 1.1163, "GBP": 1.33, "CHF": 1.25, "DKK": 0.15, "HKD": 0.1286,
           "INR": 0.0113, "TWD": 0.031, "JPY": 0.0066, "CAD": 1 / 1.396, "BRL": 0.18}

INDUSTRIES = [  # canonical name, base loader, new-data tab, new-data workbook
    ("Payments", "pat:Payments", "Payments", NC / "Round1_Four_Industries.xlsx"),
    ("Exchanges and data", "pat:Exchanges_and_data", "Exchanges and data", [FIN / "Wharton_Candidates_Missing_Audit" / "Wharton_Candidates_Round1_Missing_Audit.xlsx", ROOT / "inputs/m12/wave3_2026-11-03/return1/New_Companies_Round1.xlsx"]),
    ("IT services", "pat:IT_services", "IT services", [FIN / "Wharton_Candidates_Missing_Audit" / "Wharton_Candidates_Round1_Missing_Audit.xlsx", ROOT / "inputs/m12/wave3_2026-11-03/return1/New_Companies_Round1.xlsx"]),
    ("Power", "csv:context/teammates_2026-11-02/aryu_m12/Power.csv", "Power", NC / "Round1_Four_Industries.xlsx"),
    ("Medtech", "csv:context/teammates_2026-11-02/aryu_m12/Medtech.csv", "Medtech", NC / "Round1_Four_Industries.xlsx"),
    ("Software", "csv:context/teammates_2026-11-03/akshaj_p_final/Software.csv", "Software", NC / "Round1_Four_Industries.xlsx"),
    ("Consumer brands", "csv:context/teammates_2026-11-03/akshaj_p_final/M12_peer_data.csv", "Consumer brands", FIN / "Consumer_Brands_and_Pharma_Research_Package" / "Consumer_Brands_and_Pharma_Round1.xlsx"),
    ("Pharmaceuticals and Biotechnology", "csv:context/teammates_2026-11-03/akshat_final/pharma_m12_research_inputs.csv", "Pharmaceuticals and Biotechnolo", FIN / "Consumer_Brands_and_Pharma_Research_Package" / "Consumer_Brands_and_Pharma_Round1.xlsx"),
    ("Internet and Digital Platforms", "csv:context/teammates_2026-11-03/Akshat_digital_m12_research_inputs.csv", "Internet and Digital Platforms", [FIN / "Wharton_Candidates_Missing_Audit" / "Wharton_Candidates_Round1_Missing_Audit.xlsx", ROOT / "inputs/m12/wave3_2026-11-03/return1/New_Companies_Round1.xlsx"]),
    ("Semiconductors", "akshajk:Akshaj_Semiconductors_Revised.xlsx", "Semiconductors", FIN / "6_Semiconductors_and_Aerospace_Round1_filled.xlsx"),
    ("Aerospace and defence", "akshajk:Akshaj_Aerospace_Defence_Revised.xlsx", "Aerospace and defence", FIN / "6_Semiconductors_and_Aerospace_Round1_filled.xlsx"),
]


def s(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer() and abs(v) > 1e6:
        return str(int(v))
    return str(v).strip()


def isnum(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def base_rows(spec, group):
    kind, path = spec.split(":", 1)
    if kind == "pat":
        rows = list(csv.DictReader(open(ROOT / "inputs/m12/round1_2026-10-31" / f"{path}.csv", encoding="utf-8-sig")))
        src = f"Pat round 1 ({path}.csv)"
    elif kind == "csv":
        rows = list(csv.DictReader(open(ROOT / path, encoding="utf-8-sig")))
        src = path.split("/")[-2] + "/" + path.split("/")[-1]
    else:
        rows, src = akshajk_rows(T3 / "akshaj_k_final" / path), f"Akshaj K {path} (Annual inputs + Review)"
    out = []
    for r in rows:
        d = {k: s(r.get(k)) for k in COLS}
        d.update(peer_group=group, source=src, new="")
        for k in ("total_debt_fy0",):  # R8 fallback field, if the teammate used it
            if not d[k] and isnum(r.get("borrowing_debt_original_fy0")):
                d[k] = s(r["borrowing_debt_original_fy0"])
        if not isnum(d["market_cap_cutoff_proxy_m"]) and isnum(d["price"]) and isnum(d["shares_outstanding_m"]):
            d["market_cap_cutoff_proxy_m"] = str(float(d["price"]) * float(d["shares_outstanding_m"]))
        out.append(d)
    return out


def akshajk_rows(path):
    """Convert Akshaj K's long-format Annual inputs + Review tab to M12 columns."""
    wb = openpyxl.load_workbook(path, data_only=True)
    long = {}
    for r in wb["Annual inputs"].iter_rows(min_row=5, values_only=True):
        if r[0] and r[1] and r[0] != "Ticker":
            long[(r[0], r[1])] = {"FY0": r[3], "FY-1": r[4], "FY-3": r[6]}
    review = {}
    hdr = None
    for r in wb["Review"].iter_rows(values_only=True):
        if r[0] == "Ticker" and r[3] == "Price":
            hdr = r
            continue
        if hdr and r[0] and isnum(r[3]):
            review[r[0]] = dict(zip(hdr, r))
        elif hdr and r[0] == "Ticker":
            hdr = None
    def g(t, m, p="FY0"):
        v = long.get((t, m), {}).get(p)
        return s(v) if isnum(v) else ""
    rows = []
    for t in sorted({k[0] for k in long}):
        rv = review.get(t, {})
        rows.append({
            "ticker": t, "company": t, "reporting_currency": s(rv.get("Currency")),
            "revenue_fy0": g(t, "Revenue"), "revenue_fy3": g(t, "Revenue", "FY-3"),
            "operating_income_fy0": g(t, "Operating income"), "pretax_income_fy0": g(t, "Pretax income"),
            "total_assets_fy0": g(t, "Total assets"), "total_assets_fy1": g(t, "Total assets", "FY-1"),
            "total_debt_fy0": g(t, "Debt used: quantified leases or R8"),
            "current_assets_fy0": g(t, "Current assets"), "current_liabilities_fy0": g(t, "Current liabilities"),
            "inventory_fy0": g(t, "Inventory"), "total_equity_fy0": g(t, "Common equity"),
            "eps_diluted_fy0": g(t, "Diluted EPS (total)"), "eps_diluted_fy3": g(t, "Diluted EPS (total)", "FY-3"),
            "earnings_common_fy0": g(t, "Net income to common"), "cfo_fy0": g(t, "Operating cash flow (total)"),
            "capex_fy0": g(t, "Cash capital spending"),
            "shares_outstanding_m": s(rv.get("Valuation shares m")), "price": s(rv.get("Price")),
            "market_cap_cutoff_proxy_m": s(rv.get("Market cap m")),
        })
    return rows


def new_rows(path, tab, group):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[tab]
    hdr = [c.value for c in ws[1]]
    rows, screened = [], []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[1]:
            continue
        raw = dict(zip(hdr, r))
        d = {k: s(raw.get(k)) for k in COLS}
        d.update(peer_group=group, source=f"{path.name} / {tab}", new="Y")
        if not isnum(d["market_cap_cutoff_proxy_m"]) and isnum(d["price"]) and isnum(d["shares_outstanding_m"]):
            d["market_cap_cutoff_proxy_m"] = str(float(d["price"]) * float(d["shares_outstanding_m"]))
        if not d["capex_fy0"] and d["ticker"] in COMBINED_CAPEX:
            d["capex_fy0"] = str(COMBINED_CAPEX[d["ticker"]][0])
            d["source"] += "; capex = combined line (exception)"
        if d["ticker"] in EPS_FACTS and not d["eps_diluted_fy0"]:
            d["eps_diluted_fy0"], d["eps_diluted_fy3"] = (str(x) for x in EPS_FACTS[d["ticker"]][:2])
            d["source"] += "; EPS = basic (no potential shares)"
        notes = s(raw.get("notes")).lower()
        if group == "Payments" and isnum(d["capex_fy0"]) and ("combined line" in notes or "overlaps" in notes):
            d["capex_software_fy0"] = "0"  # combined line already includes software (Pat's exception)
        why = []
        if s(raw.get("not_being_acquired")).upper() == "N":
            why.append("being acquired")
        if s(raw.get("bank_like")).upper() == "Y":
            why.append("bank-like")
        if isnum(d["cfo_fy0"]) and isnum(d["capex_fy0"]) and float(d["cfo_fy0"]) - float(d["capex_fy0"]) <= 0:
            why.append("free cash flow not positive")
        elif isnum(d["cfo_fy0"]) and float(d["cfo_fy0"]) <= 0:
            why.append("operating cash flow negative")
        fx = USD_PER.get(d["reporting_currency"].upper())
        if fx and isnum(d["market_cap_cutoff_proxy_m"]) and float(d["market_cap_cutoff_proxy_m"]) * fx < 2000:
            why.append(f"market cap about ${float(d['market_cap_cutoff_proxy_m']) * fx:,.0f}m")
        (screened if why else rows).append((d, why))
    return [d for d, _ in rows], [(d["ticker"], "; ".join(w)) for d, w in screened]


def ranked(res, kw):
    stab = stability(res, **kw) if len(res["complete"]) >= 2 else {}
    order = sorted(res["complete"], key=lambda t: -res["totals"][t])
    return order, stab


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines = ["# New candidates: M12 by industry (TEST preview, 3 Nov 2026)", "",
             "Generated by `python tools/score_new_candidates.py`. Existing peers plus the new names that pass the screens. "
             "**M12 is a research filter, never a value, return or weight.** \"x/32\" = variants (of 32) keeping the company in the top 2. "
             "Where a group is not released (fewer than 5 complete or under 80% coverage), the ranking of its complete companies is a DIAGNOSTIC.", ""]
    summary = []
    for group, base, tab, wbpath in INDUSTRIES:
        b = base_rows(base, group)
        n, out = [], []
        for path in (wbpath if isinstance(wbpath, list) else [wbpath]):
            n1, o1 = new_rows(path, tab, group)
            n += n1
            out += o1
        rows = b + n
        with open(OUT / f"M12_{group.replace(' ', '_')}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            w.writerows(rows)
        res = score_group(rows)
        order, stab = ranked(res, {})
        newset = {d["ticker"] for d in n}
        lines += [f"## {group}", "",
                  f"Released: **{'yes' if res['released'] else 'no'}** ({len(res['complete'])} of {len(rows)} complete, {res['coverage']:.0%}). "
                  + ("" if res["released"] else "Ranking below is the complete-only DIAGNOSTIC."), ""]
        lines += ["| Rank | Ticker | New? | TFS | Top-2 in variants | Worst rank |", "|---|---|---|---|---|---|"]
        for i, t in enumerate(order, 1):
            k = stab.get(t, ("", "", ""))
            lines.append(f"| {i} | {t} | {'NEW' if t in newset else ''} | {res['totals'][t]:.1f} | {k[0]}/{k[1]} | {k[2]} |")
        inc = [t for t in res["raw"] if t not in res["complete"]]
        if inc:
            lines.append("")
            lines.append("Not scored (incomplete): " + "; ".join(
                f"{t}{' (NEW)' if t in newset else ''}: " + ", ".join(f"{m} {res['raw'][t][m][1]}" for m, _, _ in MEASURES if res["raw"][t][m][0] is None)
                for t in inc) + ".")
        if out:
            lines.append("")
            lines.append("Screened out before scoring: " + "; ".join(f"{t} ({w})" for t, w in out) + ".")
        lines.append("")
        top_new = [(order.index(t) + 1, t) for t in order if t in newset]
        summary.append((group, res["released"], order[:3], top_new, len(order)))
    head = ["## Summary", "", "| Industry | Released? | Top 3 (complete companies) | Best new names (rank) |", "|---|---|---|---|"]
    for g, rel, top, tn, n in summary:
        head.append(f"| {g} | {'yes' if rel else 'no (diagnostic)'} | {', '.join(top)} | {', '.join(f'{t} ({r}/{n})' for r, t in tn[:3]) or 'none scored'} |")
    lines[5:5] = head + [""]
    (OUT / "M12_new_candidates_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(head))


if __name__ == "__main__":
    main()
