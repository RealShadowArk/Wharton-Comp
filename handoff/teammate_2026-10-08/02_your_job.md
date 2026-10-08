# Your job: industry research and peer data for stock picking

## Why this matters

**42% of the portfolio ($126,831) goes into individual stocks.** To pick them
fairly, we:
1. choose a few industries worth looking at;
2. list comparable companies in each one (a "peer group");
3. collect the same 8 financial measures for every company;
4. rank them inside each group with our M12 score;
5. research the top 2 per group in depth.

**You own steps 1-3.** Pat builds the scoring tool and does steps 4-5 and the
trades.

## Your four industries

Each comes from a "next research question" in Pat's sector research. Pat can
swap any of them. Semiconductors (analog chips) stays with Pat.

| # | Industry (GICS sub-industry) | Sector | Question to answer | Starting candidates (verify each one's GICS classification) |
|---|---|---|---|---|
| 1 | **Transaction & Payment Processing Services** | Financials | Payment networks earn fees, not loan interest. Do they avoid the credit risk that gave Financials the worst crash on record (-54.9% in 2008)? | Visa (V), Mastercard (MA), PayPal (PYPL), Fiserv, FIS, Global Payments (GPN), Jack Henry (JKHY) |
| 2 | **Pharmaceuticals** | Health Care | How much would Medicare drug-price negotiation and slower drug-spending growth (CMS forecast) hurt drug makers? How dependent is the group on Eli Lilly and GLP-1 drugs? | Eli Lilly (LLY), Johnson & Johnson (JNJ), Merck (MRK), Pfizer (PFE), Bristol-Myers Squibb (BMY), Zoetis (ZTS) |
| 3 | **Electrical Components & Equipment** (add Heavy Electrical Equipment if needed to reach 5) | Industrials | What share of earnings comes from AI data-center and power-grid spending, and how badly would a spending pause hurt? | Eaton (ETN), Emerson (EMR), AMETEK (AME), Hubbell (HUBB), Rockwell Automation (ROK), Vertiv (VRT), GE Vernova (GEV) |
| 4 | **Household Products** | Consumer Staples | Can these companies protect profit margins when shoppers trade down to cheaper brands and some input costs rise? | Procter & Gamble (PG), Colgate-Palmolive (CL), Kimberly-Clark (KMB), Church & Dwight (CHD), Clorox (CLX) |

**Watch-outs:**
- **GE Vernova** has only traded on its own since 2024, so its 3-year history
  may be incomplete. Mark missing years MISSING; don't estimate them.
- **Mergers distort growth numbers.** Check whether any company had a major
  merger in the last 3 years (for example Kimberly-Clark and Kenvue; verify
  that deal's status) and say so in the notes.
- **Eaton** is legally based in Ireland but files a US 10-K. Record
  domicile, listing and revenue geography as separate facts.
- **Payment companies** hold large customer "settlement" balances, which can
  make the current ratio look strange. Note it; don't adjust it.

## Deliverables and deadlines

| By | Deliverable | Format |
|---|---|---|
| **Fri 9 Oct** | Read this folder. Have a 10-minute call with Pat to confirm the industries and definitions. Get added to the roster. | none |
| **Sun 11 Oct** | **Peer lists:** at least 5 companies per industry, each with its GICS sub-industry and source | First columns of `M12_peer_data_template.csv` |
| **Wed 14 Oct** | **Peer data:** every column filled in for every company, or marked MISSING | `M12_peer_data.csv` (same columns as the template) |
| **Thu 15 Oct** | **Four short industry records**, 1-2 pages each (format below) | `M11_industry_<name>.md` or a Google Doc |

Pat needs 15-22 Oct to score, value and trade before the 23 Oct deadline, so
these dates are firm. **If you're stuck for more than 30 minutes, message Pat.**

Put your files in the Drive folder "Wharton Comp 2026-2027", in a subfolder
with your name, and tell Pat when each one is there.

## Part A: the peer data (most important)

**Rules**

- Use the company's latest **annual report: the 10-K** (a 20-F for foreign
  companies; flag it). Find it free on SEC EDGAR (sec.gov). Use **"FY0"**,
  the latest completed fiscal year, for everything except where a column
  says otherwise.
- **Collect the raw numbers, not ratios.** Pat's code calculates the ratios,
  which avoids arithmetic mistakes.
- **Units:** USD millions, except EPS and price (USD) and shares (millions).
- Every row needs the 10-K link and the page or note where you found the
  numbers.
- **Can't find a number? Leave it blank and write MISSING in `status`.**
  Never estimate, never use zero.

**Columns**, in order (`M12_peer_data_template.csv` has the header row):

| Column | What to enter |
|---|---|
| `peer_group` | Payments / Pharma / Electrical / Household |
| `ticker`, `company` | As listed |
| `gics_sub_industry`, `gics_source` | Classification and where you checked it (S&P/MSCI page, an ETF holdings file, etc.) |
| `domicile`, `listing_exchange`, `reporting_currency` | Separate facts; don't merge them |
| `fiscal_year`, `fy_end_date` | For example, 2025 and 2025-12-31 |
| `revenue_fy0`, `revenue_fy3` | Total revenue in FY0 and three years earlier (FY0 minus 3) |
| `operating_income_fy0` | As reported. If the company doesn't report it, write MISSING and explain in `notes`. |
| `total_assets_fy0`, `total_assets_fy1` | End of FY0 and end of the year before (needed for an average) |
| `total_debt_fy0` | Short-term borrowings + current portion of long-term debt + long-term debt. **Exclude** lease liabilities. (Proposed definition; Pat confirms on the call.) |
| `current_assets_fy0`, `current_liabilities_fy0` | From the balance sheet |
| `eps_diluted_fy0`, `eps_diluted_fy3` | Diluted EPS, as reported |
| `net_income_fy0` | Net income attributable to the company's shareholders |
| `cfo_fy0` | Net cash from operating activities |
| `capex_fy0` | Purchases of property, plant and equipment, entered as a positive number |
| `shares_outstanding_m`, `shares_date` | From the cover page of the latest 10-Q or 10-K |
| `price`, `price_date` | Closing price, **the same date for every company** (agree it with Pat) |
| `source_url` | 10-K link |
| `status` | COMPLETE or MISSING:<columns> |
| `notes` | Mergers, odd items, anything that surprised you |

**What the score will do with your data** (so you know why each number
matters):
- **Quality:** operating margin; revenue ÷ average assets.
- **Balance sheet:** debt ÷ assets (lower is better); current ratio.
- **Growth:** 3-year revenue growth; 3-year EPS growth (only when both EPS
  numbers are positive).
- **Valuation:** earnings ÷ market cap; free cash flow ÷ market cap.

A company missing any of the 8 measures gets no score. A peer group needs at
least 5 companies, and at least 80% of them with complete data, so
**completeness matters more than speed.**

## Part B: four short industry records (1-2 pages each)

Use Pat's template (file 04), short form:

1. **Scope:** industry, GICS level, which of Laura's three jobs it serves.
2. **What these businesses sell, and the main business types** inside the
   industry.
3. **Demand:** what drives sales, with 2-3 sourced numbers.
4. **Profits:** margins now vs a few years ago (from your data).
5. **What's priced in:** P/E of the group (Calc from your data) vs the 10-year
   Treasury yield (5.18% on 24 Sep 2026, Fed H.15).
6. **Bad scenario:** what goes wrong, and the worst past year if an industry
   ETF or index has the history (label it Secondary if it comes from a data
   site). Then: what if that happened in 2032?
7. **Country exposure:** revenue by region from each 10-K's segment note.
   Use only the regions disclosed; don't invent country shares.
8. **Answer to the question above,** a priority label (Research now /
   Monitor / Insufficient evidence), and the 1-2 companies you'd want Pat to
   look at first, with a reason. This is a research suggestion, not a buy
   call.
9. **Optional:** list any ETF that tracks this industry (ticker, expense
   ratio, number of holdings). Pat may compare it with buying single stocks.

## Do not

- Place trades in WInS or write Trading Notes for Pat's trades.
- Recommend buying, set weights, or predict returns.
- Invent, round off or "fill in" numbers. MISSING is a perfectly good answer.
- Use Laura's biography to guess what she'd like.
- Edit anything in the repo's `context/` or model files.

## AI-use log (required; one line per session)

Keep a simple table in your folder: date | tool | what you asked it to do |
what you checked or changed yourself.

**Every number in your files must come from a source you opened yourself,
not from the AI's memory.** AI is often wrong about financial figures and
dates.
