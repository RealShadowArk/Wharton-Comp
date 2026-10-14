# M12 Transparent Fundamental Score (TFS): spec for the peer data

Version 0.1, 14 Oct 2026. Source: the P3 M12 build guide (Drive folder
"Pat (P3)"). Section 4 lists proposed adaptations that are **pending Pat's
sign-off**.

**The score is a research filter.** It is never a fair value, an expected
return, a buy/sell signal or a portfolio weight.

## 1. The eight measures (4 pillars, each measure weighted 12.5%)

Column names refer to `M12_peer_data.csv`. FY0 = latest fiscal year,
FY1 = the year before, FY3 = three years before.

| ID | Pillar | Measure | Formula (CSV columns) | Better |
|---|---|---|---|---|
| Q1 | Quality | Operating margin | operating_income_fy0 ÷ revenue_fy0 | Higher |
| Q2 | Quality | Revenue ÷ average assets | revenue_fy0 ÷ ((total_assets_fy0 + total_assets_fy1) ÷ 2) | Higher |
| B1 | Balance sheet | Debt ÷ assets | total_debt_fy0 ÷ total_assets_fy0 | **Lower** |
| B2 | Balance sheet | Current ratio | current_assets_fy0 ÷ current_liabilities_fy0 | Higher |
| G1 | Growth | 3-year revenue growth (CAGR) | (revenue_fy0 ÷ revenue_fy3)^(1/3) − 1 | Higher |
| G2 | Growth | 3-year diluted EPS growth (CAGR) | (EPS_fy0 ÷ EPS_fy3)^(1/3) − 1, **only if both EPS values are positive**; otherwise MISSING | Higher |
| V1 | Valuation | Earnings ÷ market value | net_income_fy0 ÷ market_cap | Higher |
| V2 | Valuation | Free cash flow ÷ market value | (cfo_fy0 − capex_fy0) ÷ market_cap | Higher |

`market_cap` = price × diluted shares (see R5 in section 4 for which share
count).

## 2. Scoring rules

1. **Score each measure within its peer group only:**

   s = 100 × (RANK.AVG(dir × x) − 1) ÷ (n − 1)

   - Ranks are in ascending order, with ties averaged (Excel `RANK.AVG(..., 1)`).
   - dir = +1 if higher is better, −1 for B1.
   - n = number of companies being ranked.
   - Best gets 100, worst gets 0.
   - If n = 1, or all values tie: s = 50, and flag it.
   - **Test case:** values 10, 20, 20, 30, 40 must score 0, 37.5, 37.5, 75, 100.
2. **TFS** = 12.5% × (sum of the 8 measure scores).
   - **If any of the 8 measures is missing, the TFS is blank.** No filling with zero or an average.
   - Proposed (the guide doesn't say): rank only the companies that have all 8 measures, so every score compares the same set.
3. **Gates per peer group.** Both must pass, or the group isn't scored:
   - at least **5 companies**;
   - at least **80%** of them with all 8 measures.
4. **Shortlist:** the top 2 TFS in each group, keeping ties.
5. **Stability check (32 variants):**
   - each measure's weight × 0.8 and × 1.2 (16 variants);
   - each pillar's weight × 0.8 and × 1.2 (8 variants);
   - drop each measure once (8 variants).

   Renormalize the weights to 100% every time. Report how often each
   shortlisted company stays in its group's top 2.
6. **Second test case:** scorecards A–E must total 56.25, 53.125, 59.375,
   56.25 and 25 (from the guide's worked example).

## 3. Output files

- `M12_scores.csv`: one row per company, with the 8 raw measures, the 8
  scores, the TFS and the flags.
- `M12_score_spec.json`: the weights, directions and rules above.
- `M12_stability.csv`: the stability results.
- `M12_stock_test_plan.md`: the tests and their results.

## 4. Proposed adaptations for our data (R1–R7, pending Pat's sign-off)

| Rule | What changes | Why |
|---|---|---|
| R1 | If any company in a group has no operating income line, use **pre-tax margin** (pretax_income_fy0 ÷ revenue_fy0) as Q1 **for every company in that group** | Pharma, electrical and household can then be scored on one consistent measure |
| R2 | Remove **GPN** (business swapped with FIS, Jan 2026) and **GEV** (pre-spin-off history) from scoring; list them on a watchlist. **KMB stays**, with G1 = MISSING (restated base). | Growth must compare like with like |
| R3 | G2 uses **continuing-operations** diluted EPS for both years where the company reports both (JNJ, EMR) | Same business in both years |
| R4 | capex = capex_fy0 + capitalized software, for **every** company | Free cash flow measured the same way |
| R5 | Diluted shares = net_income_fy0 ÷ eps_diluted_fy0 (both total, as reported); market_cap = price × that | Handles Visa and Mastercard share classes automatically |
| R6 | price = **close on 9 Oct 2026** for every company; record the source | Same date for everyone |
| R7 | Keep **HUBB** and **PG** as peers by business model; note the GICS conflict | M11 defines peers by business model |

## 5. Columns to add now

| New column | For | Notes |
|---|---|---|
| `pretax_income_fy0` | R1 | Every row, from the income statement |
| `eps_cont_fy0`, `eps_cont_fy3` | R3 | Only where continuing-operations EPS is reported; otherwise blank |
| `capex_software_fy0` | R4 | The separate capitalized-software line. Enter 0 where it's already inside capex, and say so in notes. |
| `price`, `price_date` | R6 | Close, 9 Oct 2026 |
| `total_equity_fy0` | Video cross-check | Shareholders' equity, excluding noncontrolling interests |
| `inventory_fy0` | Video cross-check | From the balance sheet; 0 only if the company truly holds none |

**The "video cross-check"** comes from the SNP screen in the videos Pat
follows. These columns are shown next to the TFS, and we run a second score
that adds them. They are **not** part of the official TFS:
- ROE = net income ÷ equity;
- P/B = market_cap ÷ equity;
- P/S = market_cap ÷ revenue;
- quick ratio = (current assets − inventory) ÷ current liabilities;
- D/E = total debt ÷ equity.

**Later, for the shortlist only (about 10 companies):** Piotroski F-score and
Beneish M-score inputs, which need prior-year values. Pat will send the exact
list after the first scoring run.

Same rules as before: every value from the filing, with its source.
Anything not reported is **MISSING**, never estimated.
