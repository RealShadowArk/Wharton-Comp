# M12 Transparent Fundamental Score (TFS): spec for the peer data

Version 0.2, 14 Oct 2026. Source: the P3 M12 build guide
(`P3_M12_Transparent_Company_Score_and_Stock_Testing.pdf`, Drive folder
"Pat (P3)"), re-read in full for this version.
- Sections 4 and 6 are **proposals pending Pat's sign-off**.
- **Changes from v0.1 are marked (v0.2).**

**The score is a research filter.** It is never a fair value, an expected
return, a trade signal or a portfolio weight.

## 1. The eight measures (4 pillars at 25%; each measure 12.5%)

Column names refer to `M12_peer_data.csv`. FY0 = latest fiscal year,
FY1 = the year before, FY3 = three years before.

| ID | Pillar | Measure | Formula | Better | Validity |
|---|---|---|---|---|---|
| Q1 | Quality | Operating margin | operating income ÷ revenue (FY0) | Higher | Revenue > 0 |
| Q2 | Quality | Asset turnover | revenue_fy0 ÷ ((total_assets_fy0 + total_assets_fy1) ÷ 2) | Higher | Revenue and average assets > 0 |
| B1 | Balance | Interest-bearing debt ÷ assets | total_debt_fy0 ÷ total_assets_fy0 | **Lower** | Assets > 0 |
| B2 | Balance | Current ratio | current_assets_fy0 ÷ current_liabilities_fy0 | Higher | Current liabilities > 0 |
| G1 | Growth | 3-year revenue CAGR | (revenue_fy0 ÷ revenue_fy3)^(1/3) − 1 | Higher | Both revenues > 0; comparable periods |
| G2 | Growth | 3-year diluted EPS CAGR | (EPS_fy0 ÷ EPS_fy3)^(1/3) − 1 | Higher | **Both EPS > 0**; split-consistent; comparable periods |
| V1 | Valuation | Earnings yield | earnings available to common shareholders ÷ market cap | Higher | Market cap > 0 |
| V2 | Valuation | Free-cash-flow yield | (cfo_fy0 − capex_fy0) ÷ market cap | Higher | Market cap > 0 |

- **(v0.2) Debt definition (guide):** short-term borrowings + current
  long-term debt + long-term debt **+ finance leases**. Operating leases are
  excluded. v0.1 wrongly excluded all leases.
- **(v0.2) Market cap (guide):** closing price on the cutoff date ×
  **common shares outstanding at that time**, with any other share classes
  converted at the rates the filing discloses. Record the reconciliation. A
  company whose share structure can't be resolved is excluded from scoring.
- **Allowed values:** negative operating income, earnings or free cash flow
  are valid values. A negative growth base is **UNSUITABLE**, not zero.
- **(v0.2) Two separate codes:** **MISSING** = not available;
  **UNSUITABLE** = the formula doesn't apply (e.g., a negative EPS base).
  Both make the TFS blank.

## 2. Scoring rules (from the guide)

1. **Score each measure within its peer group:**

   s_j = 100 × (RANK.AVG(dir_j × x_j, peer_values, 1) − 1) ÷ (n − 1)

   - dir = +1 if higher is better, −1 for B1.
   - peer_values = the direction-adjusted values.
   - Ties get the average rank.
   - **(v0.2) Rank only the complete companies.** The same set of companies
     is used for every measure (the guide says this explicitly).
   - n = 1, or all values tied: s = 50, flag "no discrimination", and don't
     rank that group by score.
2. **Pillar score** = the average of its two measure scores.
   **TFS** = the average of the 4 pillars (equivalently, Σ 0.125 × s_j).
   - **One invalid measure makes the TFS blank.**
   - No average filling, no zero, no moving its weight to the other measures.
3. **(v0.2) Release gate per peer group:** at least **5 complete companies**
   AND at least **80%** of the group complete. Otherwise, show diagnostics
   only.
4. **Shortlist:** the top 2 TFS in each released group, keeping ties at the
   boundary.
5. **Stability, 32 variants:** w'_j = w_j × a_j ÷ Σ (w_k × a_k), all other
   multipliers = 1.
   - Each measure's multiplier = 0.8, then 1.2 (16 variants).
   - Each pillar's two multipliers together = 0.8, then 1.2 (8 variants).
   - Each measure's multiplier = 0, i.e. removed (8 diagnostic variants).

   Raw data and peers stay fixed. Report the rank change and whether each
   company stays on the shortlist in every variant.

### Test cases (arithmetic tests from the guide, not real companies)

Scores in the order Q1, Q2, B1, B2, G1, G2, V1, V2:

| Card | Measure scores | Expected TFS |
|---|---|---|
| A | 100, 75, 100, 75, 50, 25, 0, 25 | 56.25 |
| B | 75, 100, 75, 100, 0, 50, 25, 0 | 53.125 |
| C | 50, 50, 50, 50, 100, 75, 50, 50 | 59.375 |
| D | 25, 25, 25, 25, 75, 100, 100, 75 | 56.25 |
| E | 0, 0, 0, 0, 25, 0, 75, 100 | 25 |

- A's pillars are 87.5, 87.5, 37.5 and 12.5, which average to 56.25.
- **Ranking test:** values 10, 20, 20, 30, 40 → 0, 37.5, 37.5, 75, 100.
- **Direction test:** reversing the direction reverses the ranks.

## 3. Output files

| File | Contents |
|---|---|
| `M12_scores.csv` | One row per company **including excluded ones**: raw measures, measure scores, pillar scores, TFS, completeness, MISSING/UNSUITABLE codes, status |
| `M12_score_spec.json` | Exactly what's in this file |
| `M12_stability.csv` | Every variant |
| `M12_stock_test_plan.md` | The test plan |

## 4. Adaptations for our data (proposed; pending Pat's sign-off)

| Rule | What | Basis |
|---|---|---|
| R1 (v0.2) | **Preferred:** where the income statement has no operating income line, *build* it: revenue minus every operating expense line above "other income/expense", interest and taxes. Record the lines used. **Fallback** (only if that can't be done consistently): pre-tax margin for **every** company in that group, declared as a deviation. | The guide says to use its exact definitions, so building the real measure beats substituting another |
| R2 | Remove GPN (business swapped, Jan 2026) and GEV (pre-spin-off history) from scoring; keep them in `M12_scores.csv` as excluded. KMB stays, with G1 = UNSUITABLE (restated base). | The guide says to reject materially incomparable periods and archive every excluded company |
| R3 | G2 uses continuing-operations diluted EPS for both years where reported (JNJ, EMR) | Comparable periods |
| R4 | capex includes capitalized software for **every** company | One rule for all, not an adjustment that favours anyone |
| R5 (v0.2) | Market cap = price × cover-page common shares, plus other share classes converted at the disclosed rates (Visa B-1/B-2/B-3/C; Mastercard Class B 1:1). Use net income ÷ diluted EPS **only as a cross-check.** | The guide's market-cap rule |
| R6 | Price = close on 9 Oct 2026 for every company; record the source | The guide requires the same date for all |
| R7 | Keep HUBB and PG as peers by business model; note the GICS conflict | Business-model peers |
| R4 revised (v0.3) | Add capitalized software to capex **only in the Payments group**, where it is material and reported inconsistently. Every other group uses capex as reported. | Ranking needs consistency only within a group. Requiring software data everywhere blanked V2 for 13 companies. |
| R8 (new, v0.3) | Where the 10-K does not quantify finance-lease liabilities (states them immaterial, or reports only operating leases), B1 uses reported borrowings, flagged "borrowings (R8)". The "drop B1" stability variant shows whether any shortlist depends on it. | Relies on the issuer's audited disclosure, not a guess. Affects MA, FIS, LLY, JNJ, MRK, BMY, EMR, HUBB, VRT, PG, ADI and MCHP; ADI and MCHP have no reconciliation note yet. |
| R3 note (v0.3) | Where only one year reports continuing EPS (e.g., ZBH FY-3), use total EPS for the other year, because no operations were discontinued in that year | Same basis in both years |

**Expected coverage (v0.2):**
- **Payments:** 5 of 6 complete (FIS: G2 UNSUITABLE). **Released.**
- **Pharma:** 6 of 6 (with R1). **Released.**
- **Electrical:** 5 of 6 (VRT: G2 UNSUITABLE). **Released.**
- **Household:** only 4 complete companies. **Diagnostics only**, unless a
  sixth comparable company with full data is added before scoring.

## 5. Columns to add

| Column | For |
|---|---|
| `finance_lease_fy0` (v0.2) | Add it into `total_debt_fy0`, and keep it as its own column so the change can be traced |
| `operating_income_built_fy0` + note listing the lines used (v0.2) | R1, for the companies without an operating income line |
| `pretax_income_fy0` | R1 fallback, every row |
| `eps_cont_fy0`, `eps_cont_fy3` | R3 |
| `capex_software_fy0` | R4 |
| `other_class_shares_m` + `conversion_note` (v0.2) | R5 |
| `price`, `price_date` | R6 |
| `total_equity_fy0`, `inventory_fy0` | Video cross-check (section 6) |

## 6. Video cross-check score (proposed; diagnostic only)

**Purpose:** to see whether the shortlist still holds when we add the extra
measures from the "SNP Score" screen in the videos Pat follows.
- **It never replaces the TFS and never changes the shortlist by itself.**
- The guide warns against overlapping ratios. That's why this stays a side
  check and why the near-duplicates below are shown but not scored.

| Pillar (25% each) | Measures (equal shares within the pillar) | New measure | Formula | Better |
|---|---|---|---|---|
| Quality | Q1, Q2, **ROE** (8.33% each) | ROE | earnings available to common ÷ total_equity_fy0 | Higher |
| Balance | B1, B2 (12.5% each) | none | | |
| Growth | G1, G2 (12.5% each) | none | | |
| Valuation | V1, V2, **P/S**, **P/B** (6.25% each) | P/S | market cap ÷ revenue_fy0 | **Lower** |
| | | P/B | market cap ÷ total_equity_fy0 | **Lower** |

- **Shown but not scored:**
  - quick ratio = (current assets − inventory) ÷ current liabilities, a near-duplicate of B2;
  - D/E = total debt ÷ equity, a near-duplicate of B1.
- **Validity:** if equity ≤ 0, ROE and P/B are UNSUITABLE, so that
  company's cross-check score is blank (same no-redistribution rule).
- **Other rules:** same scoring, gates and complete-set rule as the TFS.
- **How to read it:** a company in its group's top 2 under **both** scores
  = consistent. Top 2 under only one = needs explanation in M03.
- **Excluded on purpose:** the SNP measures based on past prices (alpha,
  beta, Sharpe, Treynor, standard deviation) belong in position sizing
  (M04). Piotroski and Beneish are pass/fail red flags for the shortlist
  only.

### Cross-check test cases (made-up scores, for testing only)

Same A–E cards as above, plus scores for the three new measures:

| Card | ROE | P/S | P/B | Expected cross-check score |
|---|---|---|---|---|
| A | 75 | 0 | 25 | 55.2083 |
| B | 100 | 25 | 0 | 54.1667 |
| C | 50 | 50 | 75 | 60.9375 |
| D | 25 | 100 | 50 | 54.6875 |
| E | 0 | 75 | 100 | 25.0000 |

**Worked example, A:**
- Quality = (100 + 75 + 75) ÷ 3 = 83.333
- Balance = 87.5
- Growth = 37.5
- Valuation = (0 + 25 + 0 + 25) ÷ 4 = 12.5
- Average of the 4 pillars = 55.2083

## 7. Red-flag checks for the shortlist only (v0.3)

These run only on the preview shortlist from `outputs/M12_scores_preview.csv`:
PYPL, JKHY, ZTS, LLY, HUBB, ETN, AME, MPWR, ADI, BSX, ISRG (plus MA, NXPI and
TXN if Pat wants the close runners-up).
- They are **pass/fail flags, never part of the TFS**.
- Collect **FY0 and FY-1** values (and FY-2 total assets) from the same 10-Ks.

| Field | Piotroski | Beneish |
|---|---|---|
| revenue, cost of goods sold (or gross profit) | ✓ | ✓ |
| net income, cash from operations | ✓ | ✓ |
| total assets (FY0, FY-1, FY-2) | ✓ | ✓ |
| current assets, current liabilities | ✓ | ✓ |
| long-term debt | ✓ | ✓ |
| weighted diluted shares | ✓ | |
| accounts receivable (net) | | ✓ |
| net PP&E, depreciation | | ✓ |
| SG&A expense | | ✓ |

- **Piotroski F-score** (0–9; higher = stronger). The flag cut-off is Pat's
  judgment; the proposal is to flag a score of 3 or lower.
- **Beneish M-score** (8-variable model, Beneish 1999). A score above
  −1.78 flags possible earnings manipulation. That cut-off is the published
  one.

Same sourcing rules as before. Anything not reported is MISSING, and a
company with missing inputs gets "not checked", never "pass".
