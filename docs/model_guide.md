# Model guide: every model, what it does, and why each value was chosen

Version 1, 24 Oct 2026. Written for Pat to read through; keep it updated when
a model or an input changes.

**Labels used throughout** (the project's guardrail):

| Label | Meaning |
|---|---|
| CASE | A fact from the Gao case study |
| RESEARCH | Sourced data: a filing, an official statistic or a cited article |
| ASSUMPTION | A judgment we chose; it must be defended in the IPS |
| TEST | A made-up value used only to test a model |
| MISSING | Not collected yet; never replaced by a guess |

**Status icons:** ✅ built and used · 🟡 built but provisional · ❌ not built.

---

## 0. How the models fit together

The models answer six questions, in this order:

| # | Question | Model | Status |
|---|---|---|---|
| 1 | How much of Laura's money can take risk without endangering her ten payments? | Structure model v4 (§A1) using M02 inputs (§A2) | ✅ |
| 2 | Are the payments locked in? | Bond ladder + M05 reserve model (§A3) | ✅ ladder, 🟡 M05 |
| 3 | What is the growth money for, and how much can Laura give in 2033? | M08 facility contribution (§A4) | 🟡 waits for M07 |
| 4 | How is the growth money spread? | ETF toolkit: rules E1–E8, look-through, crash replays (§A5) | ✅ |
| 5 | Which individual companies are worth researching? | M12 score (§A6), then thesis cards | ✅ |
| 6 | Is a company's price justified? | M03 DCF and reverse DCF (§A7) | ✅ |

Then come sizing (the 2% loss rule), the trade note, and monitoring (the
news log and sell triggers). Part B lists the models still missing, and
Part C the data still missing.

---

# Part A: Models that exist

## A1. Structure model v4 (Option 3, the "floor rule") ✅

**Files:**
- the workbook `context/Laura_Gao_Portfolio_Structure_Model_v4.xlsx`, built by `tools/build_structure_v4.py`;
- its Python port `structure/plan.py`;
- a cell-by-cell input guide in `docs/model_input_guide_draft.md`.

**What it is for:** deciding how much money goes into stocks each year
while always keeping enough in bonds to pay Laura's ten $50,000 payments.

**The idea, in four lines:**
1. **Floor** = the cost *today* of bonds that would fund all ten payments.
2. **Cushion** = Laura's money − floor.
3. **Stocks = m × cushion**; everything else sits in bonds.
4. Rebalance once a year. A crash shrinks the cushion, so the stock share
   falls automatically, while the floor keeps growing at the bond yield.

**Key inputs, and why each value was chosen:**

| Input | Value | Label | Meaning | Why this value |
|---|---|---|---|---|
| Contributions | $300k (2027), $150k (2028) | CASE | Laura's deposits | Case study |
| Payments | 10 × $50,000, 2033–42, start of year, nominal | CASE | What must be funded | Case study |
| Bond yield | 5.24% | RESEARCH | Return on the safe money | The yield we actually locked in: blended yield of the 10 holdings bought 8 Oct |
| Safety margin | 0% | ASSUMPTION | Extra reserve above the exact cost | The ladder is held to maturity, so no margin is needed for price swings |
| Multiplier m | 2 | ASSUMPTION (team, 5 Oct) | How aggressively the cushion is used | See the box below |
| Maximum stock share | 100% | ASSUMPTION | A cap on stocks | Never binds in practice; the floor does the limiting |
| Stock return | 6.95% arithmetic mean (about 5.4% compound) | RESEARCH/ASSUMPTION (M02 BASE) | Average yearly stock return used in the projections | From M02: published 10-year forecasts and history (§A2) |
| Stock volatility | 17.8% a year | RESEARCH (M02) | How much yearly returns swing | Long-run S&P 500 history (M02) |
| Crash sizes | −37% and −43.84% | RESEARCH | Shocks used in the preset scenarios | 2008 and 1931, the two worst S&P 500 calendar years since 1928 |
| Simulation | 1,000 paths, seed 20260926 | TEST setting | Random paths for the simulation tab | Fixed seed, so results can be repeated |
| Satellite share | 70% | ASSUMPTION (Pat, 5 Oct) | Share of growth money (after tilts) in individual stocks | Pat's choice: research-driven stocks rather than mostly index funds |
| Sector tilts | 9.5% | ASSUMPTION (Pat, 16 Oct) | Deliberate sector ETFs | See `docs/trading_notes_etfs.md` |
| Loss budget | 2% of the portfolio per position | ASSUMPTION (Pat, 15 Oct) | Size × worst calendar year ≤ 2% | Caps the damage from any single bet repeating its worst year |

> **Why m = 2.** The cushion is wiped out only if stocks fall far enough in
> a single year: crash = (m − 1)(1 + bond yield) ÷ m − 1.
> - **m = 2:** −47.4%. That's worse than any S&P 500 calendar year since
>   1928; the worst were −43.8% in 1931 and −37% in 2008.
> - **m = 3:** about −30%, so 2008 alone would have broken the floor.
> - **m = 1:** never breaks, but holds far less stock, so less growth.
>
> m = 2 is the most growth that still survives the worst year on record.

**Procedure (what the workbook does each year, 2027–2033):**
1. Floor = reserve needed in 2033 ($401,623 at 5.24%), discounted back at
   5.24% to that year.
2. Cushion = wealth − floor. Stocks = 2 × cushion (never below 0).
3. Grow stocks at that year's stock return and bonds at 5.24%; add the
   2028 contribution.
4. Repeat. In 2033, form the reserve, pay the first $50,000, and the
   leftover can fund the facility contribution (§A4).

**Outputs:**
- **WInS_Plan / Trade_List:** one target for the $300k account. 2028
  numbers: portfolio $465,720, floor $311,111, cushion $154,609, so
  stocks are 66.4% of the money.
- **Tilt_Sizing:** the 2% check for each ETF tilt.
- **Step5_Scenarios:** 16 return paths, including M02's S1–S8.
- **Step5_Simulation / Summary:** 1,000 random paths.
- **Checks:** 20 internal checks, all passing.

**Results so far:**
- Every M02 stress path covers the $401,623 reserve.
- The thinnest is S1, a credit crash in 2032, which leaves $40,162 spare.
- S3, an AI-spending pause in 2030–32, leaves $47,521.

**Limits:**
1. One stock return for all stocks: the model can't tell PayPal from MPS.
2. It assumes yearly rebalancing; a crash between rebalances is "gap risk".
3. The simulation is lognormal; the spec asks for a block bootstrap (Part B).
4. Projections use the case cash flows only. WInS gains are never added
   (competition rule).

**Run it:** `python tools/build_structure_v4.py` rebuilds the workbook. The
Python port is tested in `tests/test_m02_structure.py`.

---

## A2. M02 assumptions and scenarios ✅ (draft)

**Files:**
- `inputs/M02_assumptions.csv`, loaded by `m02/assumptions.py`;
- the workbook `context/M02_Assumptions_and_Scenarios_v1.xlsx`.

**What it is for:** the single source of every market assumption, so no
model types in its own numbers. Each row keeps its label and source ID.

**What's inside:**

| Part | Meaning |
|---|---|
| Assumptions (A-01 …) | Each with LOW / BASE / HIGH values, e.g. bond yield, stock return, volatility, crash size |
| Scenario paths S0–S8 | Year-by-year stock returns for 2027–2032, used as stress tests |
| Historical_Returns | S&P 500, T-bill and 10-year Treasury returns since 1928 (Damodaran; S&P via YCharts) |
| Sector_Risk | Weight, P/E, beta, volatility and worst year for each S&P 500 sector (S&P DJI, 31 Aug 2026) |

**The scenarios:**

| ID | Story | Why it is there |
|---|---|---|
| S0 | Base: steady average returns | Reference point |
| S1 | 2008-style credit crash in 2032 | Hits just before the reserve is formed (the worst timing) |
| S2 | 2022-style rate spike in 2031 | Inflation and rate risk |
| S3 | AI-spending pause 2030–32 (2000–02 replay) | Our main named risk |
| S4 | 2008-style crash in 2027 | Tests an early crash |
| S5 | Lost decade (2000–05 replay) | Long weak period |
| S6 | Strong growth (2019–24 replay) | The upside case |
| S7 | Oil collapse and recession in 2032 | Commodity shock |
| S8 | Stagflation 2031–32 (1973–74 replay) | Inflation plus falling stocks |

**Why these values:**
- Scenario returns replay **actual historical years** rather than invented
  numbers, so each stress has a real precedent.
- BASE stock returns come from published forecasts (Vanguard, J.P. Morgan)
  cross-checked against history.

**Limits:**
- Labelled "v1.0-DRAFT".
- Its bond yield (5.0%) is out of date. The model now uses the locked 5.24%.

---

## A3. Bond ladder and M05 reserve model ✅ / 🟡

**Files:**
- the `Bond_Ladder` tab in the structure model;
- `m05/` (`reserve.py`, `policy.py`, `run.py`) and `outputs/M05_*`.

**What it is for:** locking in Laura's ten payments, and checking how a
2033 reserve would pay them out.

**The ladder (bought 8 Oct):**
- Ten holdings, each maturing just before the payment it funds:
  - iBonds funds IBTM–IBTR for 2033–37;
  - Treasuries maturing Feb 2037, May 2038, Nov 2039, Nov 2040 and Nov 2041
    for 2038–42.
- Cost: $100,879 including commissions.
- Blended yield: 5.2423%. That is the one yield that gives the payments the
  same present value as the holdings.
- Held to maturity, so price swings don't affect the payments.

In WInS ($300k only), each holding funds about a third of its payment. The
full plan, with the $150k contribution, funds all of it.

**M05, the reserve formula:**
- **Required reserve:** R = 50,000 × [1 − (1 + y)^−10] ÷ y × (1 + y). It's
  an annuity *due*, because the first payment is made immediately.
- At y = 5.24%, **R = $401,623**.
- **Transfer** = the smaller of R and the money available.
- **Gap** = R − transfer.
- **Run-off:** a year-by-year schedule of the reserve paying out, with
  returns between payments.

**Procedure:**
1. Read the case facts and the TEST scenarios.
2. Size the reserve.
3. Form it in 2033 using only what is known then.
4. Run the payments off.
5. Report whether all ten were funded, and the first shortfall year if not.

**Status:** version m05-0.1, provisional.
- It still reads an older input format and needs rewiring to M02.
- The policy choices that belong to people are marked UNDECIDED, with the
  role who decides.

---

## A4. M08 facility contribution 🟡

**Files:** `m08/` (`gift.py`, `ranges.py`, `spec.py`, `run.py`) and
`outputs/M08_*`.

**What it is for:** the case asks, in 2031, for a credible **range** for
Laura's 2033 facility contribution.

**Rules:**
- **Order in 2033:** reserve first → gift → retained flexibility.
- **Gift = share × leftover**, where leftover = money in 2033 − the full
  required reserve. The first payment is already inside the reserve, so it
  is not subtracted twice.
- **No leftover means no gift.** The gift is never negative.
- **The share is UNDECIDED.** P1 chooses it; the model never picks it.
- **Ranges** come from simulated paths (M07) as quantiles:
  - "equal tail": cut the same share off both ends;
  - "one-sided minimum": "at least $X".
- **Payment success rate** (the share of paths funding all ten payments) is
  reported separately. One never stands in for the other.

**Outputs:**
- **Now:** the policy specification (JSON) and four hypothetical check
  cases (enough, exact, short, empty).
- **Waiting:** the ranges, once M07's path file exists (Part B).

---

## A5. ETF toolkit ✅

**Files:**
- `docs/trading_notes_etfs.md` (fact sheets);
- `docs/stock_selection_rules.md` (rules E1–E8);
- `tools/etf_review.py` (look-through and crash replays).

**What it is for:** choosing and sizing the index funds (VOO, VXUS) and the
sector tilts (XLI, XLK, XLV, XLF).

**Screening rules (each ETF must pass):**

| Rule | Test | Value | Why |
|---|---|---|---|
| E1 | Tradeable in WInS | n/a | Competition rule |
| E2 | Clear role (core or tilt) | n/a | Every holding must serve the strategy |
| E3 | Cheapest fund for the exposure | e.g., VOO 0.03% | Fees compound against Laura |
| E4 | Median bid-ask spread | ≤ 0.05% (ASSUMPTION) | Cheap to trade and rebalance |
| E5 | 1-year tracking difference | within ±0.25 points (ASSUMPTION) | It must deliver its index |
| E6 | Research support | n/a | No unresearched bets |
| E7 | Size × worst calendar year | ≤ 2% (ASSUMPTION, Pat) | Loss limit per position |
| E8 | Concentration known | top-10 weight | Know the bet you are making |

**Look-through (how much of each sector we really own):** exposure to a
sector = VOO amount × VOO's weight in that sector + the tilt fund in that
sector.

- **Result:** our US fund money is **28% tech vs 38% for the S&P 500**
  (deliberately under), and above the market in industrials, financials and
  health care.
- **Gap:** VXUS's sector split is MISSING.

**Crash replays:** apply each fund's actual calendar-year return in 2008,
2018, 2020, 2022 and an "every fund's worst year at once" TEST. Bonds and
cash are held flat.

| Replay | Result for the ETFs, as % of the portfolio |
|---|---|
| 2008 | −10.4% |
| 2022 | −3.9% |

**Bond prices:** a separate test moves yields by −1.5 to +2.5 points. If
yields rise 2.5 points, the ladder loses about 17% on paper, but the
payments are unaffected.

**Limit:** a replay is one historical path, not a forecast.

---

## A6. M12 Transparent Fundamental Score ✅

**Files:**
- `m12/score.py` and `m12/run.py`;
- `outputs/M12_scores_preview.csv` and `outputs/M12_stability_preview.csv`;
- spec in `handoff/M12_score_spec.md`.

**What it is for:** a **research filter.** It ranks companies *against
their peers* so we know which few to research properly. It is never a
value, a return forecast or a buy signal.

**The eight measures** (each 12.5%; four pillars of 25%):

| Measure | Formula | Higher or lower is better | What it tells you |
|---|---|---|---|
| Q1 Operating margin | Operating income ÷ revenue | Higher | Pricing power and cost control |
| Q2 Asset turnover | Revenue ÷ average assets | Higher | How hard the company's assets work |
| B1 Debt ratio | Debt ÷ assets | **Lower** | Ability to survive a bad year |
| B2 Current ratio | Current assets ÷ current liabilities | Higher | Short-term cash safety |
| G1 Revenue growth | 3-year compound growth | Higher | Is the business growing? |
| G2 EPS growth | 3-year compound growth (both years positive) | Higher | Is profit per share growing? |
| V1 Earnings yield | Earnings ÷ market value | Higher | Profit you get per dollar paid |
| V2 Cash-flow yield | (Operating cash flow − capex) ÷ market value | Higher | Cash you get per dollar paid |

**Procedure:**
1. Score each measure within the peer group:
   **s = 100 × (average rank − 1) ÷ (n − 1)**, so 0 is the worst and 100
   the best. Ties share their rank.
2. Total = the weighted average. If any measure is missing, the total is
   blank: we never fill gaps.
3. **Gates:** a group is scored only with **at least 5 complete companies
   and 80% coverage**. Small groups give unstable ranks.
4. **Shortlist the top 2** per group, keeping ties.
5. **Stability:** re-score under 32 weight changes (each measure × 0.8 and
   × 1.2, each pillar × 0.8 and × 1.2, drop each measure once).
   "Robust" = on the shortlist in **at least 24 of 32** (ASSUMPTION,
   pending your sign-off).
6. **Cross-check:** a second version adds ROE, price/sales and price/book,
   taken from the stock-screen videos.

**Data rules R1–R8** (pending your sign-off):
- R1: if there is no operating-income line, use pretax margin for the
  whole group.
- R2: exclude companies with incomparable histories (GPN, GEV).
- R3: use continuing-operations EPS where reported.
- R4: count capitalised software as capex, for Payments only.
- R5: reconcile share classes.
- R6: one price date (9 Oct).
- R7: HUBB and PG are kept as business-model peers.
- R8: if finance leases aren't quantified, use reported borrowings.

**Why equal weights:** set by the M12 spec, so nobody can tune the weights
to favour a stock they already like.

**Results:**
- Shortlist: PYPL, JKHY, ZTS, LLY, HUBB, ETN = AME (tied), MPWR, ADI, BSX, ISRG.
- Household products wasn't released: it failed the gate.

---

## A7. M03 DCF valuation ✅

**Files:**
- `m03/dcf.py` (the maths) and `m03/run.py` (`python -m m03.run PYPL`);
- inputs `inputs/m03/<TICKER>_dcf_inputs.csv` and the template
  `TEMPLATE_dcf_inputs.csv`;
- standard inputs written by `tools/make_m03_inputs.py`;
- outputs `outputs/M03_Valuation_<TICKER>.md/.csv`, `M03_summary.md` and
  `M03_Thesis_and_Rejection_Log.md`;
- a standalone kit for teammates in `handoff/`.

**What it is for:** checking whether a company's **price** is justified by
the **cash** it will produce, and what growth the price already assumes.

**Procedure:**
1. **Forecast 10 years of free cash flow to the firm:**
   FCFF = EBIT × (1 − tax) + D&A − capex − change in working capital.
   This is the cash left for all investors after tax and reinvestment.
2. **Discount at WACC.** WACC is what shareholders and lenders together
   require:
   - equity share × (Treasury + beta × equity premium);
   - plus debt share × cost of debt × (1 − tax).
3. **Terminal value** for all years after year 10:
   **TV = FCFF in year 11 ÷ (WACC − g)**. The model stops with an error if
   WACC ≤ g.
4. **Bridge to a share price:** (present value of the FCFF + TV) + cash −
   debt, divided by diluted shares.
5. **Sensitivities:** WACC × long-run growth, and WACC × profit margin.
6. **Reverse DCF:** shift every year's growth until the value equals the
   price. The result is the growth the market is assuming.
7. **Decision (rule 6.4):** buy only if our evidence-based view beats what
   the price assumes, and write the edge statement.

**Standard inputs, and why each value:**

| Input | Value | Label | Why |
|---|---|---|---|
| Base revenue, margin, tax, capex | Latest 10-K | RESEARCH | Audited, comparable |
| Growth, years 1–5 | Per company: guidance → latest quarters → 3-year trend | ASSUMPTION | Evidence-based central case |
| Growth, years 6–10 | Fades linearly to 3% | ASSUMPTION | Fast growth can't last forever; avoids cutting fast growers off at year 5 |
| Operating margin | Last year's actual, held flat | ASSUMPTION | Cautious: no margin improvement assumed |
| D&A | Calibrated so year 0 matches the company's *actual* cash flow (operating cash flow − capex + after-tax interest) | ASSUMPTION | D&A wasn't collected for every company; this uses sourced cash data instead |
| Treasury | 5.13% (FRED, 21 Oct) | RESEARCH | The risk-free rate today |
| Beta | 1.0 for every company | ASSUMPTION | Company betas MISSING; 1.0 is the market average |
| Equity premium | 5% | ASSUMPTION | A common textbook value; tested ±1 point through WACC |
| Cost of debt | 5.6% (Treasury + 0.5) | ASSUMPTION | Investment-grade borrowers; yields not collected |
| Terminal growth g | 3% | ASSUMPTION | Below long-run nominal GDP growth |
| Terminal reinvestment | 20% of profit (= 3% ÷ 15% return on new capital) | ASSUMPTION | Growth after year 10 must be paid for |
| Cash | Latest balance sheet | RESEARCH, or MISSING | MISSING for ZTS, BSX, AME, ETN, ADI and LLY, whose values are understated |
| Acquisitions after the base year (NSI, Indicor…) | Valued at cost | ASSUMPTION | Assumes the company paid a fair price |

**Results (23 Oct):** value ÷ price.

| Company | Value ÷ price |
|---|---|
| PYPL | 2.00 |
| ZTS | 1.04 |
| BSX | 0.99 |
| JKHY | 0.70 |
| HUBB | 0.67 |
| AME | 0.48 |
| ETN | 0.45 |
| ADI | 0.44 |
| ISRG | 0.42 |
| LLY | 0.36 |
| MPWR | 0.29 |

At a 5.13% Treasury, most quality stocks sit above their DCF value, so
trust the **ranking** more than any single number.

**Limits:**
- The DCF is only as good as its growth and margin inputs.
- Stock-based pay is counted as a non-cash add-back, which flatters heavy
  payers.
- A beta of 1.0 hides real risk differences.

---

## A8. Rules and monitoring (process, not models) ✅

- **`docs/stock_selection_rules.md`:** the rulebook, Steps 0–7 plus E1–E8.
  Every parameter is labelled GUIDE (from the spec) or JUDGMENT (yours).
- **News monitor** (`handoff/news_monitor_2026-10-15/`):
  - a daily RED/AMBER/GREEN log;
  - thesis cards;
  - proposed sell triggers, awaiting your approval.

---

# Part B: Models still needed (in priority order)

| # | Model | What it would do | Why it matters | Data it needs |
|---|---|---|---|---|
| 1 | **Red-flag checks** | Beneish M-score (signs of earnings manipulation; flag if above −1.78, the published cut-off) and Piotroski F-score (financial strength 0–9; flag if 3 or lower, ASSUMPTION) | Rulebook step 5. Not done for any stock yet, PayPal included | Two years of receivables, sales, gross profit, SG&A, D&A, PP&E, total assets, debt, current ratio, shares, net income and CFO |
| 2 | **Stock sizing tool** | Max position = 2% of the portfolio ÷ worst calendar-year loss; also shows the largest peak-to-trough fall | Turns the 2% rule into share counts | Annual returns per stock (PYPL: worst year −62% in 2022, secondary source) |
| 3 | **Beta estimator** | Beta from 60 monthly returns vs the S&P 500 | Replaces the beta = 1.0 placeholder in every DCF | Monthly prices for each company and for the S&P 500 |
| 4 | **M04 exposures** | Look-through including stocks; risk share of each holding (w'Σw); concentration (HHI); currency effect | Shows how much risk each holding *adds*, e.g. PayPal vs XLF overlap | Monthly returns for every holding, ETF holdings files, VXUS sectors |
| 5 | **M03 upgrades** | Bull/base/bear output; margin path from guidance; stock-pay adjustment; Excel output (spec) | Better valuations, and spec-compliant files | Guidance, consensus estimates, stock-based compensation |
| 6 | **M06 stress runner** | Applies the M02 scenarios to the *actual* holdings, with sector shocks | Tests the real portfolio, not one average stock | Sector and stock returns in each scenario |
| 7 | **M07 block-bootstrap simulation** | Replaces the lognormal simulation (spec); feeds M08's ranges | Required for the 2031 facility range | Historical monthly or annual return series |
| 8 | **M01 ledger** | Every dated contribution, trade, fill and payment; reconciles to zero at zero returns | An audit trail for the IPS | WInS transaction history |
| 9 | **Refresh scripts** | Pull the latest Treasury yield (FRED) and prices (CSV) | Keeps every model current | — |
| 10 | **M05 rewire** | Point M05 at M02 | Removes the provisional label | — |

---

# Part C: Information still missing

| Item | Needed for | Companies or scope | Suggested owner | Priority |
|---|---|---|---|---|
| **Company betas** (5-year monthly) | M03 WACC | All 11 + new candidates | P2 | High |
| **Cash and investments** | M03 cash/debt bridge | ZTS, BSX, AME, ETN, ADI, LLY; MPWR's investments | P2 | High |
| **Worst calendar year and largest fall** | 2% sizing rule | All candidates (PYPL done, to verify) | P2 | High |
| **Accounting outlook**: latest guidance for revenue, margin, EPS and capex, plus analyst consensus | M03 growth and margins; reverse-DCF context | All candidates; update after each results release | P2 / news monitor | High |
| **Red-flag inputs** (see B1) | Beneish and Piotroski | Shortlist, starting with PYPL | P2 | High |
| D&A, stock-based compensation, interest expense | Cleaner FCFF | All 11 | P2 | Medium |
| Monthly returns, 5 years, plus the S&P 500 | Betas, M04 correlations | All holdings and candidates | P2 | Medium |
| VXUS sector weights | M04 look-through | VXUS | P2 | Medium |
| Credit ratings / bond yields | Cost of debt | All 11 | P2 | Low |
| Equity premium source (e.g., a published implied premium) | M03 WACC | All | P3 (your decision) | Medium |
| Live WInS prices and the transaction history (actual fills) | Trade notes, M01, Trade_List | All trades | Pat | High |
| International companies: 20-F reports, earnings currency, ADR ratio | M03 international track | Any foreign candidate | P2 | When chosen |
| Case study PDF and role PDFs (not yet imported) | Checking the specs | — | Pat (upload) | Medium |
| Fed decision (27–28 Oct) and Q3 results (PYPL/HUBB 27 Oct, BSX 28 Oct, MPWR/LLY 29 Oct) | Thesis checks, refreshed DCFs | Watchlist | News monitor | High |
