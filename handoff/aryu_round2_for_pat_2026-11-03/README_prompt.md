# Aryu's Round 2 (power and medtech), done by Pat: prompt (3 Nov 2026)

**For Pat:** Aryu's research has already been fact-checked, and his five companies fail the value tests at beta 1.0 (NRG fails upside/downside). This Round 2 is needed so the report uses one method for every industry. **Priority:** items 1 and 2. Item 3 (Kenon) only if there is time.

**In this folder:**
- `Team_Round2_data_template.xlsx`: fill this (Valuation inputs, Red flags FY0 and FY1, Risk).
- `Aryu_starting_figures.csv`: every figure Aryu already sourced (reported FY0 from his M12 file, cash, debt, diluted shares and guidance notes from his DCF files), with links. **Start here.** Check each figure against its source before copying, then fill only the gaps.
- Aryu's two fact-checked documents: background, guidance and competitors.
- `KENON_option1_2026-11-02.md`: the team's Kenon valuation (item 3 only).

Paste everything below the line into the AI tool, then attach the template and `Aryu_starting_figures.csv`.

---

You are a research assistant for a high-school team in the Wharton Global Youth investment competition. Fill the attached Round 2 workbook for five companies, following its "Start here" tab. The attached `Aryu_starting_figures.csv` holds figures a teammate already sourced: **re-verify each one against its link** before using it, and correct any that do not match.

| Ticker | Company | Industry | Watch-outs |
|---|---|---|---|
| CEG | Constellation Energy | Power | Bought Calpine after its 2025 year-end. **Valuation inputs:** use the 2025 pro forma statements (8-K, Calpine as if owned all year) for revenue, operating income, pretax income, net income, D&A, capex, debt and cash, and shares after the deal. Say "pro forma" in notes. **Red flags:** reported 2025 and 2024 (not pro forma). |
| NRG | NRG Energy | Power | Bought the LS Power portfolio after its 2025 year-end: same treatment as CEG. Give the Series A preferred stock's liquidation amount from the filing (it counts as debt). |
| RMD | ResMed | Medtech | Fiscal year ended 30 Jun 2026. FY2027 guidance: give the exact wording and basis (for example "core, constant currency"). |
| ALC | Alcon | Medtech | IFRS, reports in USD: debt = financial debts **without** lease liabilities (give the lease total in notes). |
| EW | Edwards Lifesciences | Medtech | Critical Care sold in 2024 (discontinued): use continuing figures. 2026 sales-growth guidance from the latest release. |

**1. Round 2 workbook.**
- **Valuation inputs** (FY0 as above):
  - revenue, operating income, pretax income, net income to common, operating cash flow, capex;
  - debt; corporate cash (no restricted funds, no decommissioning trust funds); shares outstanding at the cash-and-debt date plus dilutive shares from the latest filing (both numbers and dates in notes);
  - reported D&A (for CEG, say whether nuclear-fuel amortization is included), stock-based pay, interest expense and interest income;
  - numeric revenue guidance for the next fiscal year, only if the company gives a number (otherwise MISSING and why);
  - analyst consensus revenue growth for years 1-3, with source and date.
- **Red flags, FY0 and FY1:** revenue, cost of revenue, SG&A, depreciation, receivables, current assets, net PP&E, total assets (and at the start of the year), current liabilities, long-term debt, shares outstanding, continuing net income, operating cash flow. Where a line does not exist, say so.
- **Risk:** the worst calendar year (December to December, through 2025) in US dollars.

**2. Yahoo Finance Max monthly CSVs**, as downloaded (Historical Data > Time period Max > Frequency Monthly): CEG, NRG, KEN, RMD, ALC, EW and SPY.

**3. Kenon (only if time).** From OPC's and Kenon's filings (Kenon 6-Ks, OPC H1 2026 report):
- OPC's debt and cash at 30 Jun 2026, **split between OPC Israel, CPV and OPC's head office**;
- 2025 maintenance capex and cash taxes paid for OPC Israel and for CPV, if disclosed;
- Basin Ranch: amount spent to 30 Jun 2026, and the expected first-full-year EBITDA.

## Rules

- Every number needs a source link and a date. If you cannot verify something, leave it blank and write MISSING with the reason. Never estimate, average or fill with zero (a value the filing itself reports as nil is a fact: write 0 and say so).
- Prices are the 30 Oct 2026 close (the WInS listing).
- US GAAP debt = borrowings plus finance leases; IFRS = borrowings without lease liabilities.
- No recommendations, price targets or opinions. The team writes all conclusions.
- This output is research notes: the team checks every source and logs the date, tool and what was used (competition AI rule).

End with a list of every field still MISSING and why.
