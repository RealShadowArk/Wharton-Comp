# CLAUDE.md

Wharton Global Youth 2026-27 investment competition. Client: Laura Gao.
The user is P3 (securities, valuation, portfolio exposures) but covers all
five roles (P1-P5) solo. Full background: `context/handoff_2026-09-28.md`.

## Working style

- The user watches usage limits. Keep work lean: no subagents, read only
  the files a task needs, and fetch Drive files one at a time on demand.
- Don't delete files without asking.
- Tests: `python -m pytest -q` (83 tests, pure standard library plus pytest).

## Key dates

- WInS trading opened 28 Sep 2026 (account assumed $300,000; confirm in portal).
- Trading Notes Analysis due **23 Oct**. Notes are written at trade time and
  copied verbatim.
- Portfolio freezes at the IPS deadline, **6 Nov**.
- Judged on reasoning and strategic coherence, not returns or trade count.

## Client facts (CASE, Gao case study pp. 2-4)

- Contributions: $300,000 at start of 2027, $150,000 at start of 2028. Nothing else before 2033.
- Ten fixed **nominal** $50,000 payments, start of each year 2033-2042.
- Start of 2033: form the reserve, then pay the first $50,000, then any facility contribution.
- 2031: recommend a credible range for the 2033 facility contribution.
- Do not infer sector, ESG, risk-tolerance or Taiwan preferences from Laura's biography.

## Guardrails

- Label every value **CASE / RESEARCH / ASSUMPTION / TEST**, with a source ID.
- Never invent risk limits or probability thresholds. Propose limits explicitly
  and mark them as student judgments.
- Nominal returns, net of fees. Never apply fees, distributions or FX twice.
- Simulation and backtest results do not prove future outcomes.
- Never fill missing data with guesses, zeros or means. Mark it missing.
- A score (M12) is a research filter: never fair value, expected return,
  a trade signal or a weight. A valuation target is never an annual return
  or a position size.

## Repo layout

| Path | What |
|---|---|
| `m02/assumptions.py` | Loads `inputs/M02_assumptions.csv` (single input source), run stamp, Model_Input_Map cases |
| `structure/plan.py` | Python port of structure model v4 (Option 3 only): floor, `scenario_path`, WInS target incl. satellites |
| `m05/` | Reserve model: sizing, year-by-year payout, gap (version m05-0.1, provisional) |
| `m08/` | Facility-contribution policy and ranges |
| `inputs/` | Case facts and TEST scenario CSVs |
| `outputs/` | Generated M05/M08 results |
| `tests/` | pytest suite for m05 and m08 |
| `tools/make_hand_check.py` | Builds `handcheck/M05_hand_check.xlsx` |
| `docs/` | `model_input_guide_draft.md` = notes for the user's input-guide doc (create the real doc only when they say "create doc"); outlines for the M05 explanation and M08 memos; `assumptions_and_figures.md` traces every input and Stage 1/2 figure |
| `context/` | Handoff notes and imported Drive files |

## Context files

- `context/handoff_2026-09-28.md`: decisions, next trade steps, coding
  priorities, open items. **Read first.**
- `context/Laura_Gao_Portfolio_Structure_Model_v4.xlsx`: **current model, Option 3 only**
  (the user's decision, 5 Oct 2026). Built from v3 by
  `tools/build_structure_v4.py` (`python tools/build_structure_v4.py`).
  - Step5_Scenarios: 16 paths. Rows 6-13 are presets; rows 14-21 are the M02
    stress paths S1-S8. Normal years use the compound return EXP(B18)-1.
  - Step5_YearByYear, Simulation and Summary are rebuilt for Option 3.
  - WInS_Plan / Trade_List: ONE target (no stages) at m = 2. Inputs B22 is
    the individual-stock (satellite) share of the growth money left after
    tilts: 70%. Target: bonds 36.6%, core fund 17.2%, tilts 6%, individual
    stocks 40.2% (held in SGOV until researched).
  - Inputs B14, B23 and rows 41/45 are cleared (Option 2 only).
  - 19 checks; all pass (verified with `formulas`). The simulation
    was also independently recomputed in Python and matches.
- Older versions were removed from the repo on 5 Oct 2026 at the user's
  request. They are still recoverable from git history:
  - v1: the original three-option model;
  - v2: v1 plus the M02 base inputs;
  - v3: v2 with Step 4 rebuilt;
  - the two-tab Google Sheet export.

  Example: `git show 90b8a21:context/Laura_Gao_Portfolio_Structure_Model_v3.xlsx > v3.xlsx`.
- `inputs/M02_assumptions.csv`: long format with columns assumption_id,
  scenario_id (LOW/BASE/HIGH), asset_id, measure, value, unit, frequency,
  as_of, source_id, status, input_version. Version "M02 v1.0-DRAFT (28 Sep 2026)".
  Values are rounded to 6 decimals (the workbook keeps full precision).
  `m05/inputs.py` TEAM_FILES still describes an older proposed M02 schema;
  rewire M05 to `m02.assumptions` in the reserve-ladder task.
- `context/M02_Assumptions_and_Scenarios_v1.xlsx`: the M02 workbook, including
  Scenario_Definitions, Historical_Returns and Model_Input_Map.

## P3 module specs (from the role PDFs in Drive `Pat (P3)`)

**M03 Company valuation and ETF comparison** (Sep 24 - Oct 8)
- FCFF = EBIT(1 - t) + D&A - capex - ΔNWC. Discount with WACC, never an equity rate.
- TV_N = FCFF_{N+1} / (WACC - g); require WACC > g, otherwise raise an error.
- Equity = EV + non-operating assets - debt and senior claims; divide by diluted shares.
- Show sensitivities: discount rate, terminal growth, one operating driver.
- ETFs are compared on objective, holdings, cost, concentration, tracking and
  trading, never with a DCF. Send the holdings to M04.
- Outputs: `M03_Candidate_Research.xlsx`, `M03_Valuation_<ID>.xlsx`, `M03_Thesis_and_Rejection_Log.md`.

**M04 Portfolio exposures and baselines** (Oct 4-12)
- Look-through: exposure_j = direct_j + Σ fund_i × holding_ij. Don't count the wrapper too.
  Fixture: 20% fund × 5% + 3% direct = 4%.
- Portfolio variance = w'Σw; variance share_i = w_i(Σw)_i / w'Σw. Shares can be negative;
  if variance is 0, report NOT DEFINED.
- HHI = Σw²; effective holdings = 1/HHI. Fixture: 4 × 25% gives HHI 0.25 and 4 effective holdings.
- USD return = (1 + local)(1 + FX) - 1.
- Outputs: `M04_weights.csv` (portfolio_id, instrument_id, weight, as_of, policy_version),
  `M04_returns.csv`, `M04_diagnostics.csv`, `M04_reserve_instrument_terms.csv`, and the workbooks and memo.

**M12 Transparent Fundamental Score (TFS)** (Sep 28 - Oct 7)
- Eight metrics in four pillars, each weighted 12.5%:
  - Quality: Q1 operating margin, Q2 revenue / average assets.
  - Balance: B1 debt/assets (lower is better), B2 current ratio.
  - Growth: G1 3-year revenue CAGR, G2 3-year diluted EPS CAGR (positive endpoints only).
  - Valuation: V1 earnings / market cap, V2 (CFO - capex) / market cap.
- s_j = 100 × (RANK.AVG(dir × x) - 1)/(n - 1). If n = 1 or all values tie, s = 50 and flag it.
- Gates:
  - All eight metrics must be present, otherwise the TFS is blank.
  - Each peer group needs at least 5 companies and 80% coverage.
  - Shortlist the top 2 per group, keeping ties.
- Fixtures:
  - Ranking 10, 20, 20, 30, 40 gives 0, 37.5, 37.5, 75, 100.
  - Scorecards A-E total 56.25, 53.125, 59.375, 56.25, 25.
- Sensitivity: 32 variants. Each metric ×0.8 and ×1.2 (16), each pillar ×0.8 and ×1.2 (8),
  drop each metric once (8). Renormalize weights every time.
- Outputs: `M12_scores.csv`, `M12_score_spec.json`, `M12_stability.csv`, `M12_stock_test_plan.md`.

## Google Drive ("Wharton Comp 2026-2027", id 1SuaEu3xkpU4QGOIsF9o2B7qcx1O19q3_)

Subfolders:
- Case Study and Client
- MAIN
- MAJOR* PDFs for roles
- AI Tools
- Pat (P3), id 1xp_ipMgjHeUGBrTVO8s0gqkG800WaV5B
- Akshath (P2)
- Akshaj R (P1 and P4)
- Akshaj P (P4 and P5)
- Aryu (P4 and P1)

Not yet imported: the case study PDF, the Country and Sector Research doc, and
the other role PDFs. Large files: ask the user to upload them through the GitHub
web UI instead of pulling them through the Drive connector.
US Sector Research artifact: https://claude.ai/code/artifact/d3da66fe-8877-4dea-bda3-b329ee2e5386

## Coding priorities (from the handoff)

1. Data layer: load `M02_assumptions.csv` as the single input source; version every run.
2. M01 ledger: dated contributions and payments; at zero returns everything reconciles.
3. Port the structure model to Python: floor, Options 1-3, WInS plan, trade list.
   Tests:
   - m = 1 equals Option 1.
   - Stocks earning the bond yield make all options equal.
   - Stage totals equal the account value.
4. M05 reserve ladder: match 2033-2042 payments to bonds or target-maturity funds.
5. M06 stress runner: apply the M02 scenarios to each option.
6. M07 simulation: block bootstrap with fixed seeds.
7. Refresh scripts: yields from FRED/H.15; prices from a manual CSV.
8. M12 screen: see the spec above.
