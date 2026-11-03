# Prompts for each teammate: what is still missing (3 Nov 2026)

Send each teammate their own section: everything from "Prompt" down to the next line of dashes. Attach `Team_Round2_data_template.xlsx` to the prompts for Akshaj P, Akshat, Akshaj K and Aryu.

Pat writes the bear cases and the reasons for investing after all industries are done. These prompts therefore ask only for facts and data, not for conclusions.

---

## Akshaj P: software and consumer brands

**Prompt**

You are helping a high-school team in the Wharton Global Youth investment competition fill data gaps in my research. I am attaching my research packet (M12 CSVs, M03 drafts, red-flag files) and the team's Round 2 workbook. Do only what is listed below. Every number needs a source link and a date. Leave anything you cannot verify blank and mark it MISSING: never estimate, average or fill with zero. Do not write recommendations, price targets or opinions; I check every source and write any conclusions myself.

**Team conventions (Pat, 1-3 Nov):**
- Prices are the 30 Oct 2026 close, in the same currency as the financials.
- M12 rule R8 is on: debt = borrowings plus finance leases. For IFRS companies, use borrowings without lease liabilities, and record the lease liabilities separately.
- Cash = corporate cash only.
- Shares = shares outstanding at the same date as the cash and debt, plus the dilutive shares from the latest filing.
- D&A is the reported figure, and stock-based pay is recorded separately.
- Euro companies use the German 10-year yield, 3.34%.

**1. Complete M12, then rerun it (`python -m m12.run`):**
- SAP (use SAP.DE in EUR, with price and financials in EUR): borrowings, earnings to common shareholders, operating cash flow and capex for B1, V1 and V2. Market cap = price × shares at a stated date.
- Consumer brands:
  - Unilever: borrowings; 3-year revenue and EPS growth on a continuing-operations basis after the ice-cream demerger (use restated figures if published, otherwise MISSING); operating cash flow minus capex.
  - Diageo: borrowings; earnings to common shareholders; operating cash flow minus capex. Note that 1 ADS = 4 ordinary shares, so price and share count must be on the same basis. Also note the change in reporting currency.
  - PepsiCo and Coca-Cola: total debt including finance leases.

**2. Pick three per industry,** using the M12 result (top 2 plus one more). Give the M12 score and the 32-variant count for each pick.

**3. For the six picks, fill the Round 2 workbook:**
- **Valuation inputs:** debt, corporate cash, diluted shares, D&A, stock-based pay, interest, numeric guidance, and consensus revenue growth for years 1-3.
- **Red flags:** both years. Fill the components your red-flag notes list as missing:
  - CRM: FY1 depreciation, continuing net income.
  - INTU: gross profit.
  - SAP: long-term debt, shares, PP&E, depreciation.
  - NKE, EL, KO, PEP: shares and continuing net income.
  - EL, UL, KO: long-term debt.
  - DEO: SG&A.
  - PEP: receivables.
- **Risk:** worst complete calendar year in US dollars, from the Max history.

**4. Yahoo Finance downloads:** Historical Data, Time period Max, Frequency Monthly. Download each pick, plus SPY, plus EURUSD=X if a euro company is picked. Send the CSVs as they are.

**5. WInS:** confirm the exact listing and its 30 Oct price for each pick.

End with a list of every field still MISSING and why.

---

## Akshat: internet and digital platforms, pharma and biotech

**Prompt**

You are helping a high-school team in the Wharton Global Youth investment competition finish my research. I am attaching my M12 CSVs, industry cards and the team's Round 2 workbook. Do only what is listed below. Every number needs a source link and a date. If you cannot verify something, write MISSING: never estimate. No recommendations or opinions; I verify everything and write conclusions myself.

**Team conventions (Pat, 1-3 Nov):**
- Prices are the 30 Oct 2026 close, in the same currency as the financials.
- M12 rule R8 is on. For IFRS companies, B1 debt = reported borrowings without lease liabilities; record total lease liabilities separately.
- Free-cash-flow screen: the latest audited annual report. Amazon's FY2025 is positive, so it stays.
- Cash = corporate cash only.
- Shares = outstanding at the cash-and-debt date, plus dilutive shares.
- For each ADR, state the ratio of ordinary shares per ADS.

**1. Pharma M12:**
- Fill borrowings for AstraZeneca, Novartis, Sanofi and Takeda, then rerun. Pharma should then have 5 of 6 complete, which releases the group. Takeda stays incomplete because its ending EPS is negative.
- Note each company's ADR ratio and reporting currency: AstraZeneca USD, Novartis USD, Sanofi EUR, Takeda JPY.

**2. Industry cards:** compare each industry with Damodaran's US total market (January 2026). Use the "Drugs (Pharmaceutical)" row, not biotech, and "Software (Internet)" or the closest internet row. Give 25 points per pillar:

| Pillar | Points | Total-market value |
|---|---|---|
| ROE | 12.5 | 17.21% |
| Pre-tax operating margin | 12.5 | 12.82% |
| Market debt/equity (lower wins) | 25 | 35.01% |
| Expected 5-year EPS growth | 25 | 13.95% |
| Forward P/E (lower wins) | 8.33 | 27.66 |
| P/S (lower wins) | 8.33 | 3.07 |
| P/B (lower wins) | 8.33 | 4.61 |

**3. Pick three per industry** (top 2 plus one more). In digital platforms, note that Meta, Alphabet and Amazon are VOO top-10 holdings.

**4. Trip.com:** check whether WInS has 9961.HK or TCOM. It reports in RMB, so give the price in RMB at the 30 Oct exchange rate, and China's 10-year yield on 30 Oct.

**5. MercadoLibre and Sea,** if picked: report the size of each item, with its date:
- operating-cash-flow lines from customer funds (MercadoLibre: funds payable to customers 5,341, card payables 1,592; Sea: escrow and customer advances 474.4);
- the loan book;
- customer deposits.

Pat decides whether the bank-like rule excludes them.

**6. For the six picks, fill the whole Round 2 workbook:**
- valuation inputs;
- red flags for two years;
- risk.

Add Yahoo Max monthly downloads for each pick, SPY, and the needed currency pairs (EURUSD=X, JPY=X, CNY=X or HKD=X).

**7. Pharma picks only:** list key patent expiries and the next trial readouts. Each must be dated and sourced, and must separate a target date from a completed event.

End with a list of every field still MISSING and why.

---

## Akshaj K: semiconductors, aerospace and defence

**Prompt**

You are helping a high-school team in the Wharton Global Youth investment competition fix and finish my research. I am attaching my two workbooks, my company pages and the team's Round 2 workbook. Do only what is listed below. Every number needs a source link and a date. If you cannot verify something, write MISSING. No recommendations or opinions; I check everything and write conclusions myself.

**Team conventions (Pat, 1-3 Nov):**
- Prices are the 30 Oct 2026 close.
- US 10-year yield 4.94% (Treasury, 30 Oct); euro companies use 3.34%.
- M12 rule R8 is on.
- Cash = corporate cash only.
- Shares = outstanding at the cash-and-debt date, plus dilutive shares.
- D&A is the reported figure.
- The DCF method is:
  - growth: year 1 = numeric guidance midpoint (otherwise consensus), years 2-3 = consensus, then a straight-line fade to 3% by year 10;
  - margin: the last full year's operating margin, held flat.

**1. Fix the example DCFs first.**
- NVIDIA comes out at about 24× its price ($4,984 a share), which cannot be right. Check:
  - revenue and share units;
  - the fiscal year (FY0 ends January 2026);
  - whether very high growth is compounding for ten years.

  Rebuild it with the team method above.
- The defence names come out at 2-4× their price at the measured beta, because their 5-year betas are very low. Download Max monthly histories so the team can also test the full-history beta.

**2. Fill the MISSING cells in "Annual inputs":** 62 for semiconductors and 85 for aerospace and defence. Also fill the red-flag gaps: 2 and 15. Where the data truly does not exist (for example, no cost-of-revenue line), say so.

**3. WInS:** check each of the 12 for the exact listing and its 30 Oct price, including ASML (ASML.AS in EUR, or the ADR) and Elbit (Nasdaq or Tel Aviv).

**4. Industry scorecards:** compare with Damodaran's US total market (January 2026), using the "Semiconductor" plus "Semiconductor Equip" rows and the "Aerospace/Defense" row. Give 25 points per pillar:

| Pillar | Points | Total-market value |
|---|---|---|
| ROE | 12.5 | 17.21% |
| Pre-tax operating margin | 12.5 | 12.82% |
| Market debt/equity (lower wins) | 25 | 35.01% |
| Expected 5-year EPS growth | 25 | 13.95% |
| Forward P/E (lower wins) | 8.33 | 27.66 |
| P/S (lower wins) | 8.33 | 3.07 |
| P/B (lower wins) | 8.33 | 4.61 |

Use market debt/equity and forward P/E against the market, not against each industry's own 10-year average.

**5. Run M12 with R8 on, then pick three per industry** (top 2 plus one more). Note:
- NVIDIA and Broadcom are VOO top-10 holdings;
- the AI exposure of each pick;
- Elbit's Israel war exposure.

**6. For the six picks, fill the Round 2 workbook** (valuation inputs, red flags for two years, risk). Send Yahoo Max monthly downloads for each pick, SPY, and EURUSD=X if needed.

End with a list of every field still MISSING and why.

---

## Aryu: power and medtech (fact-checked; a few items left)

**Prompt**

You are helping a high-school team in the Wharton Global Youth investment competition finish my power and medtech research. Pat has already fact-checked it. Do only what is listed below. Every number needs a source link and a date. If you cannot verify something, write MISSING. No recommendations; I write conclusions myself.

**1. Kenon:** the team revalued it on its parts' cash flows (OPC's Israeli plants and CPV's US plants separately). The result is about $40 a share (range $20-62) against the $64.11 price, so there is no edge on our method.

I will rewrite my Kenon section in my own words. Give me only these facts, each with its source:
- Kenon owns about 46% of OPC, has $605m of its own cash (31 Aug 2026) and no ZIM stake left;
- the $200m dividend (Apr 2026) and the $93m legal award (Aug 2026);
- Israel's country risk premium (1.98%);
- PJM capacity prices at the cap for three auctions;
- Shay (about 2.1 GW) and Walker (1.45 GW) are not yet under construction;
- Israel shut its Leviathan and Karish gas fields on 28 Feb 2026, when the Iran war began (Leviathan restarted about 3 Apr).

Search once more for any dated statement explaining why Kenon and OPC fell from their highs. If none exists, keep it MISSING.

**2. Yahoo Max monthly downloads:** CEG, NRG, KEN, RMD, ALC, EW and SPY. Send the CSVs as they are, so the team can test full-history betas.

**3. WInS:** confirm the listing and the 30 Oct price for CEG, NRG, RMD, ALC and EW.

**4. Round 2 workbook:** fill one row each for CEG, NRG, RMD, ALC and EW. Kenon is valued separately. Fill:
- shares outstanding at the cash-and-debt date plus dilutive shares;
- reported D&A and stock-based pay;
- interest;
- corporate cash;
- debt;
- numeric guidance and consensus revenue growth for years 1-3;
- red-flag lines for two years;
- the worst calendar year in US dollars.

Reuse my existing figures where they are already sourced.

End with a list of every field still MISSING and why.

---

## For every teammate (add to any prompt)

- **AI use:** the competition rule is that "work generated by an AI program may not be submitted as the team's own". Keep this output as research notes. Open every source yourself, and log the date, tool and what you used.
- **Never guess Laura's preferences** (sector, ESG, risk or country) from her biography.
- **The bar every company must clear:**
  - on WInS at $5 or more (or the local equivalent);
  - market cap of at least $2bn;
  - positive free cash flow in the latest annual report;
  - not bank-like (no deposits or loan book inside operating cash flow).
