"""Convert the filled Round 1 workbook into M12 peer files (one CSV per group).

Usage: python tools/round1_xlsx_to_csv.py <workbook.xlsx> <out_dir>
Rows marked in_wins_at_5_plus = N are left out (rule 0.1). Market cap = price x shares.
"""
import csv
import sys
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook

GROUPS = ["Payments", "Exchanges and data", "IT services"]
REQUIRED = ["revenue_fy0", "revenue_fy3", "total_assets_fy0", "total_assets_fy1", "total_debt_fy0",
            "current_assets_fy0", "current_liabilities_fy0", "eps_diluted_fy0", "eps_diluted_fy3",
            "earnings_common_fy0", "cfo_fy0", "capex_fy0", "price", "shares_outstanding_m"]


def cell(v):
    if isinstance(v, (datetime, date)):
        return v.strftime("%Y-%m-%d")
    return "" if v is None else v


def main(book, out_dir):
    wb = load_workbook(book, data_only=True)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    groups = [ws.title for ws in wb.worksheets if ws.cell(1, 1).value == "peer_group"] or GROUPS
    for g in groups:
        ws = wb[g]
        hdr = [c.value for c in ws[1]]
        rows, dropped = [], []
        for vals in ws.iter_rows(min_row=2, values_only=True):
            r = {h: cell(v) for h, v in zip(hdr, vals)}
            if not r.get("ticker"):
                continue
            if str(r.get("in_wins_at_5_plus", "")).strip().upper() == "N":
                dropped.append(r["ticker"])
                continue
            if r["price"] != "" and r["shares_outstanding_m"] != "":
                r["market_cap_cutoff_proxy_m"] = float(r["price"]) * float(r["shares_outstanding_m"])
            missing = [k for k in REQUIRED if r.get(k) == ""]
            if r.get("operating_income_fy0") == "" and r.get("pretax_income_fy0") == "":
                missing.append("operating or pretax income")
            if g == "Payments" and r.get("capex_software_fy0") == "":
                missing.append("capex_software_fy0 (rule R4)")
            print(f"{g:20} {r['ticker']:6} missing: {', '.join(missing) or 'none'}")
            rows.append(r)
        path = out_dir / (g.replace(" ", "_") + ".csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=hdr)
            w.writeheader()
            w.writerows(rows)
        print(f"-> {path} ({len(rows)} rows; left out for WInS $5 rule: {', '.join(dropped) or 'none'})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
