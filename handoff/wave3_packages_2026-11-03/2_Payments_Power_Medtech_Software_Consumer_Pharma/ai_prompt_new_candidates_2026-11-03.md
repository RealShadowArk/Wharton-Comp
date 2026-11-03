# AI prompt: Round 1 data for the 67 new candidates

**How to use it:**
- Run it once per industry tab of `inputs/m12/new_candidates_2026-11-03/New_candidates_M12_data.xlsx`. A big batch makes AI tools skip fields, so do one tab at a time.
- Paste everything below the line, then paste that tab's prefilled rows (ticker, company, listing, currencies, notes) where marked.
- Paste the CSV it returns into the tab with Data > Text to Columns, and check every number against its source.
- Send the workbook back. I'll convert it, score each new name against the existing peers in its industry, and list the top 3 per industry for Round 2.

---

You are a research assistant for a high-school team in the Wharton Global Youth investment competition. We screen companies with a peer score (M12) that ranks eight measures within each industry. I need the raw Round 1 inputs for the companies below. Report facts only: no opinions, recommendations, price targets or forecasts.

**Industry:** [INDUSTRY NAME]
**Companies (ticker | company | listing | quote currency | reporting currency | note):**
[PASTE THE PREFILLED ROWS]

## Rules

1. Use the **latest annual report published by 31 Oct 2026** (10-K, 20-F or annual report). FY0 = that year, FY1 = the year before, FY3 = three years before FY0.
2. Every number needs a source.
   - Prefer the company's own filing. StockAnalysis.com is fine for checking, but say which one you used.
   - Put the main link in `source_url`, and list the rest in the evidence table (format below).
3. If you cannot find or verify a value, leave it **blank** and list it as MISSING. Never estimate, average, use zero, or take a figure from a different year or scope.
4. **Units:**
   - Amounts are in **millions of the reporting currency**. Indian "crore" × 10 = millions.
   - EPS and price are per share.
   - Shares are in millions.
5. **One currency per row.**
   - `price` is the **30 Oct 2026 close** in the **reporting currency**.
   - If the quote currency differs (London pence, Toronto CAD, a US ADR for a company that reports in DKK, GBP, EUR or TWD), convert using the 30 Oct exchange rate. Give the rate and its source in `notes`.
6. **ADRs:** fill `adr_shares_per_ads`. Price and shares must be on the same basis: either both per ordinary share, or both per ADS.

## Columns (in this exact order)

`peer_group, ticker, company, in_wins_at_5_plus, domicile, listing_exchange, reporting_currency, accounting_standard, fiscal_year, fy_end_date, revenue_fy0, revenue_fy3, operating_income_fy0, pretax_income_fy0, total_assets_fy0, total_assets_fy1, total_debt_fy0, current_assets_fy0, current_liabilities_fy0, inventory_fy0, total_equity_fy0, eps_diluted_fy0, eps_diluted_fy3, eps_cont_fy0, eps_cont_fy3, earnings_common_fy0, cfo_fy0, capex_fy0, capex_software_fy0, shares_outstanding_m, price, price_date, market_cap_cutoff_proxy_m, source_url, notes, quote_currency, adr_shares_per_ads, not_being_acquired, bank_like`

**Identity and screens:**
- `in_wins_at_5_plus`: leave blank. I check it in WInS myself.
- `domicile`: country of incorporation, from the cover page.
- `accounting_standard`: US GAAP, IFRS or Ind AS.
- `not_being_acquired`: Y or N. N if a takeover, merger or take-private was announced and not completed or withdrawn by 31 Oct 2026. Name the deal and date in `notes`.
- `bank_like`: Y or N. Y if the company takes deposits or holds a loan book whose flows sit inside operating cash flow.

**Income statement:**
- `operating_income_fy0`: as reported. If there is no operating-income line, leave it blank and say so.
- `pretax_income_fy0`: as reported.

**Balance sheet (all at the FY0 year-end unless stated):**
- `total_debt_fy0`: borrowings plus finance leases (US GAAP). For IFRS and Ind AS companies, use borrowings without lease liabilities, and give total lease liabilities in `notes`.
- `current_assets_fy0`, `current_liabilities_fy0`, `inventory_fy0`, `total_equity_fy0`: as reported.
- `total_assets_fy1`: total assets one year before FY0.

**Per share:**
- `eps_diluted_fy0` and `_fy3`: total diluted EPS.
- `eps_cont_fy0` and `_fy3`: continuing-operations diluted EPS, only if the company reports it.
- If a year's EPS is negative, report it as it is. Do not adjust it.

**Cash flow and market data:**
- `earnings_common_fy0`: net income to common shareholders.
- `cfo_fy0`: operating cash flow as reported. If it contains customer, merchant, clearing or escrow funds, give the line name and amount in `notes`. Do not adjust the number.
- `capex_fy0`: purchases of property, plant and equipment.
- `capex_software_fy0`: Payments only. Capitalized software or intangible additions, otherwise blank.
- `shares_outstanding_m`: from the cover page or the latest report. Give the date in `notes`.
- `market_cap_cutoff_proxy_m`: leave blank. The workbook calculates it.

## Watch-outs for this list

- Fiscal years that don't end in December: Booz Allen, Kyndryl, DXC, Workday, Veeva, Lululemon, Constellation Brands, PTC, Cooper, Coloplast, Siemens Healthineers, Infineon, Applied Materials, KLA, Prosus, Auto Trader. Use their latest full year and give the year-end date.
- Share classes:
  - Clearway: Class A and Class C.
  - Roche: the non-voting Genussschein (dividend-right certificate) versus bearer shares.

  Add up all classes for market cap, and say how in `notes`.
- Holding company: Prosus mainly owns part of Tencent. Report its own figures and note the Tencent stake. The team values holding companies separately.
- Exchanges (Cboe, Euronext, HKEX): clearing-member balances inflate assets and cash. Say whether they sit inside `current_assets_fy0` and `cfo_fy0`.

## Output

1. **One CSV block** with the header row above and one row per company, ready to paste.
2. **An evidence table:**

   | ticker | column | value | source URL | statement and line | period/date |
   |---|---|---|---|---|---|

3. **MISSING list:** every blank field and why it is blank.
4. **Coverage note:** pages you could not open, and figures from secondary sources only.

AI use: this output is research notes. The team checks every source and writes all analysis in its own words.
