# Stock evaluation kit (31 Oct 2026)

The team's two models plus everything needed to evaluate a company the way we
do: the M12 peer score (with the "SNP Score" measures from Pat's videos), the
M03 DCF and reverse DCF, the red-flag formulas and the risk measures. The team
doc ("Team stock research", parts 3 and 4) says what to hand back; this file
says how to run each step.

Python 3.9 or newer, no extra packages. Open a terminal **inside this folder**
(the one that contains `m03/` and `m12/`). Optional check that everything works:

```
python -m unittest discover -s tests     # 28 checks, nothing to install
```

## The method, in order

| Stage | What | Tool | For |
|---|---|---|---|
| 1 | Industry score vs the S&P 500 | By hand (team doc, Template 1) | Each of your 2 industries |
| 2 | Peer ranking: M12 score, video cross-check, 32-variant stability | `m12` | All 6-10 candidates in each industry |
| 3 | DCF and reverse DCF, with stock-based pay, at three betas, plus a bear case | `m03` | Your top 3 per industry |
| 4 | Red flags: Piotroski F-score and Beneish M-score | Your own spreadsheet (formulas below) | Your top 3 |
| 5 | Risk: beta, volatility, Sharpe, Treynor, alpha, worst calendar year, position size | Your own spreadsheet (formulas below) | Your top 3 |
| 6 | Dip test, 10-year plan, competitors, fit for Laura | Your research (team doc, Template 2) | Your top 3 |

Every number needs a source link and a date. A number you can't find is left
blank (MISSING), never guessed.

## Stage 2: M12 peer score

1. Copy `inputs/m12/TEMPLATE_M12_peer_data.csv` to, for example,
   `inputs/m12/Software.csv`. One row per company, `peer_group` the same for
   all rows of one industry. `EXAMPLE_M12_peer_data_v02.csv` shows 33 filled rows.
2. Fill the columns from each company's latest annual report (10-K, or 20-F
   for foreign companies). Amounts in millions, all in **one currency per
   company** (market cap and financials in the same currency).
   - `_fy0` = latest fiscal year, `_fy1` = the year before, `_fy3` = three
     years before.
   - `market_cap_cutoff_proxy_m` = price x shares outstanding, using **one
     price date for the whole group**.
   - `earnings_common_fy0` = net income to common shareholders.
   - `total_debt_fy0` includes finance leases, not operating leases.
   - `eps_cont_*`: only if the company reports continuing-operations EPS.
   - `capex_software_fy0`: only for a group named `Payments`.
   - `accounting_standard`: US GAAP or IFRS (Pat decides how IFRS companies
     are ranked; mark them).
3. Run:

   ```
   python -m m12.run inputs/m12/Software.csv
   ```

   It writes `outputs/M12_scores_Software.csv` and
   `outputs/M12_stability_Software.csv`.

**What it computes** (full spec: `M12_score_spec.md`):

- Eight measures, four pillars of 25%: operating margin, revenue / average
  assets, debt / assets (lower is better), current ratio, 3-year revenue and
  EPS growth, earnings / market cap, (operating cash flow - capex) / market cap.
- Each measure is scored by rank inside the group: 100 x (average rank - 1) /
  (n - 1).
- A group is scored only with at least 5 complete companies and 80% coverage;
  one missing measure leaves that company unscored.
- The top 2 per group are shortlisted.
- `crosscheck` adds the videos' ROE, P/S and P/B inside the same pillars.
- `variants_on_shortlist` counts the 32 weight changes under which the company
  stays in the top 2. Robust = 24 or more (our judgment).

A high score is a research filter, never a buy signal or a fair value.

## Stage 3: DCF and reverse DCF

1. Copy `inputs/m03/TEMPLATE_dcf_inputs.csv` to `inputs/m03/<TICKER>_dcf_inputs.csv`
   and fill every row. The 11 filled files are worked examples.
2. Run `python -m m03.run <TICKER>`. It writes `outputs/M03_Valuation_<TICKER>.md`
   and `.csv`.
3. Read three things in the report:
   - **value / price**;
   - **what the price assumes** (the reverse DCF growth path), compared with
     guidance and the company's own long-term plan;
   - the **"Data gaps and open choices"** table: stock-based pay, EBIT basis,
     and the value at beta 1.0, the measured beta and the adjusted beta.
4. **Bear case:** copy the file to `<TICKER>bear_dcf_inputs.csv`, cut growth and
   margin to what a bad decade looks like, and say why. Our PayPal lesson: its
   base case was +15% above the price but its bear case was -41%. A price that
   sits near the base case is not a margin of safety.

Rules that matter:

- Fill `sbc_pct` (stock-based pay / revenue, from the cash-flow statement)
  whenever `da_pct` is calibrated from operating cash flow. Otherwise the value
  is overstated.
- If the margin row is a pretax margin, fill `net_interest_pct`.
- Foreign companies: price and financials in the same currency.

## Stage 4: red flags (pass/fail, top 3 only)

Two years of the annual report (t = latest, t-1 = the year before). Missing
data = "not checked", never "pass".

**Piotroski F-score:** one point for each test passed, 0-9. Flag at 3 or lower
(our judgment).

1. Net income / total assets at the start of the year > 0
2. Operating cash flow > 0
3. That return on assets is higher than last year
4. Operating cash flow > net income
5. Long-term debt / average total assets is lower than last year
6. Current ratio is higher than last year
7. No new shares issued (shares outstanding not up)
8. Gross margin is higher than last year
9. Revenue / total assets at the start of the year is higher than last year

**Beneish M-score** (8-variable model, Beneish 1999). Flag if M > -1.78:

```
M = -4.84 + 0.920 DSRI + 0.528 GMI + 0.404 AQI + 0.892 SGI + 0.115 DEPI
    - 0.172 SGAI + 4.679 TATA - 0.327 LVGI
```

| Index | Formula |
|---|---|
| DSRI | (receivables_t / sales_t) / (receivables_t-1 / sales_t-1) |
| GMI | gross margin_t-1 / gross margin_t |
| AQI | [1 - (current assets_t + net PP&E_t) / total assets_t] / the same for t-1 |
| SGI | sales_t / sales_t-1 |
| DEPI | [depreciation_t-1 / (depreciation_t-1 + net PP&E_t-1)] / the same for t |
| SGAI | (SG&A_t / sales_t) / (SG&A_t-1 / sales_t-1) |
| TATA | (income from continuing operations_t - operating cash flow_t) / total assets_t |
| LVGI | [(current liabilities_t + long-term debt_t) / total assets_t] / the same for t-1 |

A company without a gross-profit line (many payments and service companies)
gets GMI = MISSING; say so instead of building a proxy.

## Stage 5: risk measures (from the videos; for sizing, not scoring)

Use 60 monthly returns (5 years of month-end prices, for example from Yahoo
Finance) for the stock and the S&P 500. rf = the 3-month T-bill yield.

| Measure | Formula |
|---|---|
| Beta | slope of the stock's monthly returns on the S&P 500's (Excel: `=SLOPE(stock, index)`) |
| Volatility | standard deviation of monthly returns x sqrt(12) |
| Sharpe ratio | (annual return - rf) / volatility |
| Treynor ratio | (annual return - rf) / beta |
| Alpha | annual return - [rf + beta x (S&P 500 annual return - rf)] |
| Worst calendar year | the lowest January-December return in the stock's history |
| **Maximum position** | **$6,000 / worst calendar-year loss** (our 2% limit) |

Past returns describe risk; they do not predict returns.

## What makes a buy candidate (proposals; Pat decides)

1. Top 2 in its M12 group and robust (24 of 32 variants or more), or a written
   reason why not.
2. DCF value above the price at both beta 1.0 and the measured beta, with
   stock-based pay counted, and the price assuming less growth than the
   evidence supports.
3. The base-case upside at least as large as the bear-case downside.
4. No red flag (Piotroski 4 or more, Beneish -1.78 or lower), or a written
   explanation.
5. The dip has a temporary cause, with evidence.
6. A one-sentence edge, the news that would prove us wrong, and the fit for
   Laura, written by you.
