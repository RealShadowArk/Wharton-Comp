"""Wave 3 of new candidates (Pat, 3 Nov 2026): 44 names, 4 per industry, in Pat's three research groups.

Names were chosen as research leads that are NOT already covered, have (to our knowledge) positive
EPS three years ago (so M12 can score them), and trade on lower valuations, because most earlier
finalists failed the value test. Every fact (listing, acquisition status, EPS) must be checked by
the researcher; nothing here is a recommendation.

Run: python tools/build_wave3_packages.py
Writes handoff/wave3_packages_2026-11-03/<group>/ (Round 1 workbook with prefilled rows, Round 2
workbook with prefilled rows, AI prompt, README_prompt.md) and one zip per group.
"""
import shutil
import zipfile
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "handoff" / "wave3_packages_2026-11-03"
R1 = ROOT / "inputs" / "m12" / "new_candidates_2026-11-03" / "New_candidates_M12_data.xlsx"
R2 = ROOT / "handoff" / "Team_Round2_data_template.xlsx"
PROMPT = ROOT / "handoff" / "ai_prompt_new_candidates_2026-11-03.md"

# tab -> [(ticker, company, listing, reporting currency, quote currency, watch-outs)], in priority order
NAMES = {
    "Semiconductors": [
        ("NXPI", "NXP Semiconductors", "Nasdaq", "USD", "USD", "Netherlands domicile, US GAAP"),
        ("2454.TW", "MediaTek", "Taiwan Stock Exchange", "TWD", "TWD", "Reports in TWD (IFRS)"),
        ("005930.KS", "Samsung Electronics", "Korea Exchange", "KRW", "KRW", "KRW; common and preferred shares: add both classes for market cap and say how"),
        ("8035.T", "Tokyo Electron", "Tokyo Stock Exchange", "JPY", "JPY", "Fiscal year ends March; JPY; state the accounting standard"),
    ],
    "Aerospace and defence": [
        ("TXT", "Textron", "NYSE", "USD", "USD", ""),
        ("AIR.PA", "Airbus", "Euronext Paris", "EUR", "EUR", "IFRS: debt without lease liabilities"),
        ("LDO.MI", "Leonardo", "Borsa Italiana", "EUR", "EUR", "IFRS: debt without lease liabilities"),
        ("HO.PA", "Thales", "Euronext Paris", "EUR", "EUR", "IFRS: debt without lease liabilities"),
    ],
    "Payments": [
        ("WU", "Western Union", "NYSE", "USD", "USD", "Settlement assets and customer funds are not corporate cash; say whether they sit in operating cash flow"),
        ("EEFT", "Euronet Worldwide", "Nasdaq", "USD", "USD", "ATM cash and settlement balances are not corporate cash"),
        ("ACIW", "ACI Worldwide", "Nasdaq", "USD", "USD", "Settlement funds are not corporate cash"),
        ("WISE.L", "Wise", "London", "GBP", "GBp", "Fiscal year ends March; IFRS; customer funds are not corporate cash; check where its primary listing is on 30 Oct 2026"),
    ],
    "Power": [
        ("RWE.DE", "RWE", "Xetra", "EUR", "EUR", "IFRS: debt without lease liabilities"),
        ("ENEL.MI", "Enel", "Borsa Italiana", "EUR", "EUR", "IFRS: debt without lease liabilities"),
        ("EDP.LS", "EDP", "Euronext Lisbon", "EUR", "EUR", "IFRS: debt without lease liabilities"),
        ("NEE", "NextEra Energy", "NYSE", "USD", "USD", ""),
    ],
    "Medtech": [
        ("MDT", "Medtronic", "NYSE", "USD", "USD", "Fiscal year ends April; Irish domicile"),
        ("ZBH", "Zimmer Biomet", "NYSE", "USD", "USD", ""),
        ("SN.L", "Smith & Nephew", "London", "USD", "GBp", "Reports in USD, trades in pence: convert the price; ADR SNN = 2 shares (check)"),
        ("BDX", "Becton Dickinson", "NYSE", "USD", "USD", "Fiscal year ends September; check the status of the biosciences/diagnostics separation"),
    ],
    "Software": [
        ("CHKP", "Check Point Software", "Nasdaq", "USD", "USD", "Israel domicile"),
        ("OTEX", "Open Text", "Nasdaq", "USD", "USD", "Fiscal year ends June; Canadian company reporting in USD"),
        ("ZM", "Zoom Communications", "Nasdaq", "USD", "USD", "Fiscal year ends January"),
        ("AKAM", "Akamai Technologies", "Nasdaq", "USD", "USD", ""),
    ],
    "Consumer brands": [
        ("DECK", "Deckers Outdoor", "NYSE", "USD", "USD", "Fiscal year ends March"),
        ("RKT.L", "Reckitt Benckiser", "London", "GBP", "GBp", "IFRS; pence to GBP"),
        ("GIS", "General Mills", "NYSE", "USD", "USD", "Fiscal year ends May"),
        ("MC.PA", "LVMH", "Euronext Paris", "EUR", "EUR", "IFRS: debt without lease liabilities (large store leases)"),
    ],
    "Pharmaceuticals and Biotechnolo": [
        ("MRK", "Merck & Co.", "NYSE", "USD", "USD", ""),
        ("PFE", "Pfizer", "NYSE", "USD", "USD", ""),
        ("BMY", "Bristol-Myers Squibb", "NYSE", "USD", "USD", "Check that 2025 EPS is positive (2024 had a large acquired-R&D charge)"),
        ("BIIB", "Biogen", "Nasdaq", "USD", "USD", ""),
    ],
    "Exchanges and data": [
        ("B3SA3.SA", "B3", "B3 (Sao Paulo)", "BRL", "BRL", "BRL; clearing-member balances: say whether they sit in current assets and operating cash flow"),
        ("8697.T", "Japan Exchange Group", "Tokyo Stock Exchange", "JPY", "JPY", "Fiscal year ends March; IFRS; clearing balances as for B3"),
        ("WKL.AS", "Wolters Kluwer", "Euronext Amsterdam", "EUR", "EUR", "IFRS: debt without lease liabilities"),
        ("TRU", "TransUnion", "NYSE", "USD", "USD", ""),
    ],
    "IT services": [
        ("WIPRO.NS", "Wipro", "NSE (ADR WIT on NYSE)", "INR", "INR", "Fiscal year ends March; IFRS; ADR WIT = 1 share (check)"),
        ("G", "Genpact", "NYSE", "USD", "USD", "Bermuda domicile"),
        ("DOX", "Amdocs", "Nasdaq", "USD", "USD", "Fiscal year ends September; Guernsey domicile"),
        ("SAIC", "Science Applications International", "Nasdaq", "USD", "USD", "Fiscal year ends January"),
    ],
    "Internet and Digital Platforms": [
        ("0700.HK", "Tencent", "HKEX", "CNY", "HKD", "Reports in RMB, trades in HKD: convert the price; IFRS"),
        ("BABA", "Alibaba", "NYSE (ADR; also 9988.HK)", "CNY", "USD", "Fiscal year ends March; reports in RMB; 1 ADS = 8 shares (check)"),
        ("PDD", "PDD Holdings", "Nasdaq (ADR)", "CNY", "USD", "Reports in RMB; 1 ADS = 4 shares (check); merchant funds are not corporate cash"),
        ("MTCH", "Match Group", "Nasdaq", "USD", "USD", ""),
    ],
}
GROUPS = [
    ("1_Aerospace_and_Semiconductors", ["Semiconductors", "Aerospace and defence"]),
    ("2_Payments_Power_Medtech_Software_Consumer_Pharma", ["Payments", "Power", "Medtech", "Software", "Consumer brands", "Pharmaceuticals and Biotechnolo"]),
    ("3_Exchanges_IT_Internet", ["Exchanges and data", "IT services", "Internet and Digital Platforms"]),
]


def round1(tabs, dst):
    wb = openpyxl.load_workbook(R1)
    for ws in list(wb.worksheets):
        if ws.title in ("Start here", "Where to find it"):
            continue
        if ws.title not in tabs:
            wb.remove(ws)
            continue
        hdr = [c.value for c in ws[1]]
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.value = None
        for i, (t, co, lst, rc, qc, note) in enumerate(NAMES[ws.title], start=2):
            vals = {"peer_group": ws.title, "ticker": t, "company": co, "listing_exchange": lst, "reporting_currency": rc,
                    "quote_currency": qc, "price_date": "2026-10-30", "notes": note or None,
                    "market_cap_cutoff_proxy_m": f'=IF(AND(ISNUMBER(AE{i}),ISNUMBER(AD{i})),AE{i}*AD{i},"")'}
            for k, v in vals.items():
                ws.cell(i, hdr.index(k) + 1, v)
    ws = wb["Start here"]
    ws["A1"] = f"Wave 3 candidates: Round 1 data (M12 + screens), {sum(len(NAMES[t]) for t in tabs)} companies. 3 Nov 2026"
    wb.save(dst)


def round2(tabs, dst):
    wb = openpyxl.load_workbook(R2)
    rows = [(t, co, rc, tab) for tab in tabs for t, co, _, rc, _, _ in NAMES[tab]]
    v, rf, rk = wb["Valuation inputs"], wb["Red flags"], wb["Risk"]
    for i, (t, co, rc, tab) in enumerate(rows, start=2):
        v.cell(i, 1, tab), v.cell(i, 2, t), v.cell(i, 3, co), v.cell(i, 4, rc)
        rk.cell(i, 1, t), rk.cell(i, 2, co)
        for j, per in enumerate(("FY0", "FY1")):
            rf.cell(2 + 2 * (i - 2) + j, 1, t), rf.cell(2 + 2 * (i - 2) + j, 2, per)
    wb.save(dst)


def readme(name, tabs):
    lines = [f"# Wave 3 research, group {name.split('_')[0]}: {', '.join(t.replace('Biotechnolo', 'Biotechnology') for t in tabs)} (prompt, 3 Nov 2026)", "",
             "**Deadline:** back by **Wed 4 Nov** so the results are ready before orders on Thu 5 Nov (portfolio freezes 6 Nov). "
             "Each industry lists 4 companies in priority order: if time runs short, do the first 2-3 in every industry rather than all 4 in a few.", "",
             "**One pass, two workbooks.** Because of the deadline, do Round 1 and Round 2 together for every company:", "",
             f"1. `{name}_Round1_data.xlsx`: run `ai_prompt_new_candidates_2026-11-03.md` once per industry tab, pasting that tab's prefilled rows where it says. Paste the CSV back and check every number.",
             f"2. `{name}_Round2_data.xlsx`: one row per company (rows are prefilled) on Valuation inputs and Risk, two rows (FY0, FY1) on Red flags, following its \"Start here\" tab. Use the same fiscal year as Round 1.",
             "3. Yahoo Finance **Max monthly** CSVs, as downloaded (Historical Data > Time period Max > Frequency Monthly), for every company below, plus SPY and the currency pairs listed.", "",
             "| Industry | Ticker | Company | Watch-outs |", "|---|---|---|---|"]
    fx = set()
    for tab in tabs:
        for t, co, _, rc, qc, note in NAMES[tab]:
            lines.append(f"| {tab.replace('Biotechnolo', 'Biotechnology')} | {t} | {co} | {note} |")
            for c in {rc, qc} - {"USD", "GBp"}:
                fx.add({"EUR": "EURUSD=X", "GBP": "GBPUSD=X", "JPY": "JPY=X", "KRW": "KRW=X", "TWD": "TWD=X", "BRL": "BRL=X",
                        "INR": "INR=X", "CNY": "CNY=X", "HKD": "HKD=X"}[c])
            if qc == "GBp":
                fx.add("GBPUSD=X")
    lines += ["", f"**Currency pairs for Yahoo:** {', '.join(sorted(fx)) or 'none'}. For an ADR in USD, the ADR's own CSV is enough for risk.", "",
              "You are a research assistant for a high-school team in the Wharton Global Youth investment competition. Use the attached prompt and workbooks. "
              "Report facts only, with a source link and date for every number.", "",
              "## Team rules", "",
              "- Latest annual report published by 31 Oct 2026. Price = 30 Oct 2026 close in the reporting currency (state the rate if converted).",
              "- If you cannot verify a value, leave it blank and write MISSING with the reason. Never estimate, average or fill with zero (a value the filing reports as nil is a fact: write 0 and say so).",
              "- Debt: US GAAP = borrowings + finance leases; IFRS = borrowings without lease liabilities (lease total in notes). Cash = corporate cash only.",
              "- Shares = outstanding at the cash-and-debt date plus dilutive shares from the latest filing (both numbers and dates in notes).",
              "- Screens to report: market cap at least $2bn; positive free cash flow; not being acquired (name any pending deal); not bank-like. Pat checks WInS.",
              "- Guidance: give the exact wording, the basis (reported, organic, constant currency) and the numeric low and high.",
              "- No recommendations, price targets or opinions. Pat writes all conclusions.",
              "- AI use: \"work generated by an AI program may not be submitted as the team's own\". This output is research notes; open every source yourself and log the date, tool and use.", "",
              "End with a list of every field still MISSING and why."]
    return "\n".join(lines) + "\n"


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for name, tabs in GROUPS:
        d = OUT / name
        d.mkdir()
        round1(tabs, d / f"{name}_Round1_data.xlsx")
        round2(tabs, d / f"{name}_Round2_data.xlsx")
        shutil.copy(PROMPT, d / PROMPT.name)
        (d / "README_prompt.md").write_text(readme(name, tabs), encoding="utf-8")
        with zipfile.ZipFile(OUT / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(d.iterdir()):
                z.write(f, f"{name}/{f.name}")
        print(name, sum(len(NAMES[t]) for t in tabs), "companies")


if __name__ == "__main__":
    main()
