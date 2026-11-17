# Refined screen: rules and defaults (17 Nov 2026)

`python tools/refined_screen.py` → `outputs/screen/`. All thresholds below are **student judgments (Pat, 17 Nov, defaults proposed by Claude)**. They are not competition rules. The screen only adds checks to our Round 2 method, so anything that passes it also passes the old screen.

## 1. Old tests, at today's price

- **Test 2:** value above price at all three betas: 1.0, the 5-year measured beta and the full-history beta.
- **Test 3:** upside/downside of at least 1.0. Upside is value at beta 1 ÷ price − 1. Downside is bear value ÷ price − 1.
- **The DCF values are the Round 2 values (3–4 Nov).** Only the price is new: Yahoo, converted into the scorecard's currency at Yahoo's FX rate.
- **Decisions made by hand after Round 2 are not encoded.** They still apply:
  - the AI-replacement drops;
  - the bank-like flags (Tencent, PDD);
  - Amdocs' guidance cut;
  - Reckitt's disposal gain (it fails without it);
  - the Lululemon-to-Sanofi swap.

## 2. Country grade (adapted from Zhou, n.d.)

Each criterion is scored 0–100 and they're averaged with equal weights. Grades: **A ≥ 80, B ≥ 65, C ≥ 50, D ≥ 35, F < 35. F fails; D is flagged.**

| Criterion | Source (RESEARCH) | 0–100 scoring |
|---|---|---|
| Political stability | World Bank WGI, `GOV_WGI_PV.SC` (2025) | as published |
| Government policy | World Bank WGI regulatory quality, `GOV_WGI_RQ.SC` (2025) | as published |
| Inflation | World Bank `FP.CPI.TOTL.ZG` (latest year) | 100 − 12.5 × \|inflation − 2\| |
| Inequality | World Bank Gini `SI.POV.GINI` (latest year) | 100 at 25 or below, 0 at 55 or above |
| Sovereign risk | S&P foreign-currency rating, in `inputs/screen/sovereign_ratings.csv` | AAA 100, AA 90, A 75, BBB 60, BB 40, B 20 (notches ±5) |

- Grades marked * are **provisional**: a criterion is MISSING. Credit ratings are still to be filled with sources. Taiwan's inflation and Gini are missing from the World Bank; use DGBAS.
- **Company country** = headquarters, with overrides in the code where operations are elsewhere (Trip.com, Tencent and PDD → China; dLocal → Uruguay).

## 3. Alpha and beta against the industry (adapted from Zhou, n.d.)

- **Data:** 60 monthly USD returns ending with the last complete month, against ACWI (the global market). The risk-free rate is the 3-month T-bill (FRED TB3MS).
- **Measures:** beta, and annualized Jensen's alpha.
- **Industry = the iShares global sector ETF:** IXN (technology), IXG (financials), IXJ (health care), EXI (industrials), JXI (utilities), RXI (consumer discretionary), KXI (consumer staples), IXP (communication services).
- **Two versions are reported:**
  - **the winner's rule:** alpha above the industry's **and** beta below it;
  - **beta only:** beta below the industry's.
- **Pat chooses which one is binding.**
- Past alpha does not predict future returns (guardrail). A stock with less than 60 months of history is not testable, so it cannot pass.

## 4. Management and governance (hand grade)

`inputs/screen/management_grades.csv`. Four items, each 1–5:
- capital allocation;
- guidance record (beats and misses);
- governance (board, share classes, related parties);
- controversies and legal.

**Pass at an average of 3.0 or more.** Write the evidence in the `evidence` column. Rows stay pending until they're graded.

## Decisions (Pat, 17 Nov)

- **Binding alpha/beta rule: beta below the industry.** Alpha is reported but not binding. Reason: the winner's alpha test conflicts with the IPS principle of valuation discipline. Undervalued stocks have usually lagged, so their past alpha is low; in the Round 2 set, only 4 of 22 value passes also beat their industry's alpha.
- **Sovereign ratings:** S&P foreign-currency ratings from Wikipedia's "List of countries by credit rating" (S&P table, which cites S&P Global Ratings), accessed 17 Nov 2026. They're filled automatically by `tools/universe_screen.py`. Bermuda's grade stays provisional (missing World Bank series).
- **Management grades:** wait until the shortlist has its DCFs.

## Universe screen (`tools/universe_screen.py`, after Zhou, n.d.)

- **Universe:** the S&P 500 constituents (Wikipedia list, 17 Nov), one row per company (duplicate share classes removed by CIK): **500 companies**, about the size of the winner's 511.
- **Funnel:** price ≥ $5 → country grade (by headquarters) → alpha/beta against the **average of the company's GICS sub-industry** (5 or more members, otherwise its sector). This is closer to "the industry's average" than a sector ETF. → M12 within peer groups → top 3 per group, keeping ties.
- **Banks, insurers and REITs are kept, with their own M12 metric sets.** These are student judgments, because the standard metrics don't fit balance-sheet businesses:

  | Metric | Standard | Bank-like (banks, insurers, consumer finance) | REITs |
  |---|---|---|---|
  | Q1 | operating margin | pretax margin | operating margin |
  | Q2 | revenue ÷ average assets | return on average assets | revenue ÷ average assets |
  | B1 | debt ÷ assets (lower is better) | debt ÷ equity (lower is better) | debt ÷ assets (lower is better) |
  | B2 | current ratio | equity ÷ assets | operating income ÷ interest expense |
  | G1, G2 | 3-year revenue and EPS growth | same | same |
  | V1 | earnings ÷ market cap | same | FFO (net income + depreciation) ÷ market cap |
  | V2 | (cash from operations − capex) ÷ market cap | book value ÷ market cap | cash from operations ÷ market cap |

  Each kind is ranked in its **own peer group**: "Financials: banks and insurers", "Financials: other" (payments, exchanges, asset managers) and "Real Estate: REITs".
- **Valuation for these at the DCF stage:**
  - FCFF at WACC doesn't fit them, so use **residual income for banks and insurers**: value = book value per share × (1 + (ROE − cost of equity) ÷ (cost of equity − g)).
  - Use **FFO-based cash flows discounted at the cost of equity for REITs**.
  - Both are equity-side methods. Use them only for these three kinds; they are an extension of M03.
- **Limits:** the universe is US-listed only, so international names come from the Round 2 set (`tools/refined_screen.py`). Statements come from Yahoo, so spot-check them before using any figure in the report.

## 5. Holdings that fail

**Keep them, add no new money in 2028, and review them each year** (student judgment). The Final Report uses the result as evaluation in Section 2, not as a reason to trade.
