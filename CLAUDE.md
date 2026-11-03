# CLAUDE.md

Wharton Global Youth 2026-27 investment competition. Client: Laura Gao.
The user is P3 (securities, valuation, portfolio exposures) but covers all
five roles (P1-P5) solo. Full background: `context/handoff_2026-09-28.md`.

## Working style

- The user watches usage limits. Keep work lean: no subagents, read only
  the files a task needs, and fetch Drive files one at a time on demand.
- Don't delete files without asking. On 3 Nov Pat asked for unused files to be removed: the v1/v2 DCF kit zips, the legacy `tools/make_m03_inputs.py`, the blank Round 1/2 templates, `docs/model_guide.md`, the prompt .docx duplicates and the 8 Oct onboarding pack (all recoverable from git history).
- Tests: `python -m pytest -q` (111 tests, pure standard library plus pytest).

## Key dates

- WInS trading opened 28 Sep 2026 (account assumed $300,000; confirm in portal).
- Trading Notes Analysis due **23 Oct**. Notes are written at trade time and
  copied verbatim.
- Portfolio freezes at the IPS deadline, **6 Nov**.
- Final Report instructions posted 9 Nov, 9am ET; school documentation and
  **Final Report due 4 Dec**, 5pm ET (Week 1-3 emails, `context/`-level source:
  user uploads 14 Oct).
- Judged on reasoning and strategic coherence, not returns or trade count.

## Competition rules from the weekly emails (Weeks 1-3)

- Approved universe, for BOTH contributions and all recommendations:
  - stocks on any WInS exchange priced at $5 or more (or the local equivalent);
  - any ETF on WInS;
  - government/Treasury bonds on WInS.

  Nothing else, not even in the long-term plan: no mutual funds, CDs or other
  asset classes.
- WInS holds $300,000 only; the $150,000 contribution is not added to WInS.
- Long-term projections start from the case cash flows with reasonable
  assumptions. Never add WInS gains or losses to them.
- Teams may not contact the client. The team is finalized (no new members).

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
| `m12/` | M12 score (`score.py`) and preview run (`python -m m12.run`); rules R1/R3/R4/R8 are switches in `RULES`, all pending Pat's sign-off |
| `m03/` | DCF (FCFF at WACC) per the M03 spec: `dcf.py` (forecast, terminal value with WACC > g check, equity bridge, sensitivities, reverse DCF) and `run.py` (`python -m m03.run HUBB`) |
| `inputs/m03/` | One labelled input CSV per company (`<TICKER>_dcf_inputs.csv`): the teammate-corrected files of 23 Oct (22 Oct closes, cash, diluted shares) plus kit-v2 rows `sbc_pct`, `net_interest_pct` (ETN/LLY/ZTS), `first_year_fraction`, `beta_measured` and `return_on_new_capital` (blank = MISSING). `python tools/make_m03_summary.py` rebuilds all 11 reports and `outputs/M03_summary.md`; decisions in `outputs/M03_Thesis_and_Rejection_Log.md` |
| `inputs/m12/` | Teammate's peer data v0.2 (33 active companies, 6 groups) and watchlist (GPN, GEV, KMB) |
| Claude Doc https://claude.ai/artifact/QWNmM3QzJd7zcNvtNMZ2sa | Model guide: every model (procedure, inputs and why each value), plus the models and data still missing (23 Oct) |
| `context/teammates_2026-10-23/` | Teammates' 23 Oct zips: research update (60-month betas, worst calendar years, cash, guidance for 33 companies) and completed M03 inputs plus an audit (22 Oct closes; engine unchanged) |
| `docs/stock_longlist_international_midcap.md` | 23 Oct long-list beyond PayPal: international ADRs and mid-caps (Novo, Smith & Nephew, Philips, PagSeguro/StoneCo/dLocal; Fiserv and Diageo parked), with the rule 7.2 sizing arithmetic |
| Claude Doc https://claude.ai/artifact/8AHqV4n5y7zWj8zsyUXGmi | 31 Oct team stock research: catch-up, assignments (4 teammates x 2 industries x top 3), industry scorecard and company one-pager templates, AI prompt; research due Mon 2 Nov 9pm ET, freeze 6 Nov |
| `handoff/stock_evaluation_kit_2026-10-31/` + `handoff/Wharton_stock_evaluation_kit_2026-10-31.zip` | Teammate kit: m03 + m12 code, 28 tests (`python -m unittest discover -s tests`), DCF and M12 templates, red-flag and risk formulas; `python -m m12.run <file.csv>` scores any peer file. Rebuild the zip after changing m03 or m12 |
| Claude Doc https://claude.ai/artifact/7UBd26um6mJyL3MUvHHhkX | Single-tab copy of the team research doc (all five parts, for export); keep it in sync with the tabbed doc |
| `inputs/m12/round1_2026-10-31/` + `docs/round1_results_2026-11-01.md` | Pat's round 1 (payments, exchanges and data, IT services): filled workbook, M12 CSVs (`tools/round1_xlsx_to_csv.py`), results, sensitivity tests and Pat's 1 Nov decisions (PagSeguro excluded, dLocal R4 stand-in). Finalists: DLO, ADYEN, PYPL, CME, ICE, MCO, INFY, TCS, CTSH |
| `context/teammates_2026-11-02/` | Aryu's 2 Nov research (power, medtech) as received (zip). `aryu_reviewed/`: both docs with fact-check fixes 2-5 as Word tracked changes (`tools/aryu_tracked_fixes.py`), DCF inputs re-run at the FRED 30 Oct 10-year yield 4.98% (T-bill 4.00%), and `REVIEW_LOG.md`. Kenon's section and files are untouched; Pat chose option 1 (parts valued on cash flows): `KENON_option1_2026-11-02.md` + `tools/kenon_sotp.py` (TEST: $40 central, 0.63x) with the Iran-war analysis |
| `inputs/round2_2026-11-01/` | Round 2 data for the nine (valuation inputs, red-flag lines, risk, monthly prices). `Finalists_DCF_Supplement_Reviewed.xlsx` (Pat, 2 Nov): CFO corrections for merchant/customer/clearing funds (DLO 415.5 -> 227.5; ADYEN 1,030.4 -> 1,246.2 EUR m; others none) and lease liabilities (MCO finance leases MISSING, immaterial). `Pat_Round2_data_completed.xlsx` + `yahoo_monthly_adjclose_max.csv` (3 Nov) feed `tools/round2_risk_redflags.py` and `tools/make_round2_dcfs.py` -> `outputs/round2/` (risk, red flags, `Round2_scorecard.md`) and `inputs/m03/<T>[bear]_dcf_inputs.csv` for the nine (Pat's 3 Nov decisions: US 4.94%, EUR 3.34%, INR 7.40%, dLocal CRP 3.0%/5.3%, Adyen own cash = gross - merchant payables; bears are a uniform DRAFT). PYPL's file now uses 30 Oct and true D&A, so `outputs/M03_summary.md` (22 Oct) is stale for PYPL |
| `context/research_2026-11-02/` | Teammates' 8-page research compilation (2 Nov, AI-assisted, human checks pending): weekly reports, 11 company cases, 30 Oct macro inputs (US 10-year 4.94% Treasury CMT; FRED 4.98% is 29 Oct), FX, dLocal country weights |
| `context/teammates_2026-11-03/` | Remaining teammates' research as received (3 Nov): Akshaj P (software ADBE CRM INTU NOW SAP ADSK; consumer brands NKE EL UL DEO PEP KO; M12, M03 drafts, risk, red flags), Akshat (digital platforms, pharma: M12 inputs and Round 2 starter only), Akshaj K (semiconductors NVDA AMD AVGO QCOM LRCX ASML; aerospace and defence RTX LMT GD NOC HII ESLT: workbooks + 12 company pages). Not yet fact-checked; ask Pat before filling |
| `context/teammates_2026-11-03/akshaj_p_final/` + `tools/round2_team.py` | Akshaj P's final package (3 Nov): M12 rerun (software INTU, ADBE, NOW; consumer NKE, PEP, KO), filled team Round 2 workbook, source ledger, Yahoo Max CSVs. `python tools/round2_team.py akshajp` runs the same Round 2 method as Pat's nine -> `outputs/round2/Round2_scorecard_akshajp.md` (add a SETS entry for each new teammate workbook) |
| `context/teammates_2026-11-03/Akshat_Round2_gap_review.xlsx` | Akshat's Round 2 (digital: 9961.HK, META, BKNG; pharma: NVS, AZN, SAN.PA). Feedback sent 3 Nov (FY2026 guidance, consensus from his Source alternatives tab, Booking own cash = cash - deferred merchant bookings, TCOM ADR for Trip.com risk, Trip.com 2025 one-off gains, raw Yahoo CSVs, pharma M12). Pat 3 Nov: Trip.com's discount rate includes China's country risk premium; re-test Trip.com's M12 rank once the one-off gains arrive |
| `context/teammates_2026-11-03/akshaj_k_final/` | Akshaj K's (= Akshaj R) package: revised workbooks, deep missing-field review, and `Akshaj_Seven_Companies_Round2.xlsx` (3 Nov: the six plus QCOM, his Yahoo Max monthly closes, SG&A, ASML debt split). `monthly_from_seven_workbook/` = those closes as CSVs. `CW_ASM_round2/` = his group 6 Round 2 for the new names (`python tools/round2_team.py akshajr_new`: CW 0.55x, ASM.AS 0.61x with capitalized development in capex; both fail). `python tools/round2_team.py akshajk` -> `outputs/round2/Round2_scorecard_akshajk.md` (QCOM tax excludes the one-off 5,724m charge; a fiscal year that ended before 30 Oct is rolled forward) |
| `docs/more_candidates_2026-11-03.md` | Research leads beyond everything covered: 5-7 new names per industry for all 11 industries, with checks first |
| `handoff/teammate_prompts_2026-11-03.md` + `handoff/Team_Round2_data_template.xlsx` | One prompt per teammate (Akshaj P, Akshat, Akshaj K, Aryu) covering exactly what each pack is missing, with the team conventions of 1-3 Nov; blank Round 2 workbook (same format as Pat's, so `tools/make_round2_dcfs.py` can be reused) |
| `handoff/teammate_handouts_2026-11-03/` | What is still missing from each teammate's original research (3 Nov, after their returns): Akshaj R (= the Akshaj K files) Yahoo Max CSVs, M12 stability files, QCOM Round 2 (tied 2nd), ASML exact debt, GD/HII SG&A, two interest lines; Aryu everything in his 3 Nov prompt plus Kenon's MISSING inputs (net debt by segment, maintenance capex and tax, Basin Ranch spend); Akshath one optional Meta capex item; Akshaj P nothing |
| `handoff/aryu_round2_for_pat_2026-11-03/` (+ zip) | Aryu's Round 2 for Pat to do himself (Aryu unreachable, 3 Nov): prompt, blank template, `Aryu_starting_figures.csv` (every figure Aryu sourced, from his M12 and DCF files, to re-verify), his two fact-checked docs, Kenon note. CEG/NRG valuation inputs on the 2025 pro forma basis (acquisitions after year-end), red flags reported |
| `handoff/ai_prompt_new_candidates_2026-11-03.md` + `inputs/m12/new_candidates_2026-11-03/New_candidates_M12_data.xlsx` | Prompt and prefilled Round 1 workbook (Pat's 35 columns + quote_currency, adr_shares_per_ads, not_being_acquired, bank_like) for the 67 new candidates in 11 industry tabs; `tools/round1_xlsx_to_csv.py` now converts every tab whose A1 is peer_group |
| `handoff/new_candidates_packages_2026-11-03/` (6 folders + zips) | One package per split group (1 payments+power, 2 exchanges+IT, 3 medtech+software, 4 consumer+pharma, 5 internet, 6 semis+A&D): that group's tabs and evidence, `README_prompt.md` (gaps to close, team rules), the Round 2 template where a new name made the cut (HKEX, Tradeweb, Dexcom, Auto Trader) and the Round 1 AI prompt for groups 4 and 6. Built by `tools/build_new_candidate_packages.py`. Sources: `Round1_Four_Industries.xlsx` (payments, power, medtech, software) and `New_candidates_M12_data_with_Internet_Digital.xlsx` (exchanges, IT, internet; superset of `Exchanges_IT_Round1_researched.xlsx`). Results so far: `docs/new_candidates_results_2026-11-03.md` |
| `tools/score_new_candidates.py` -> `outputs/new_candidates/` | All 11 industries scored with M12: existing peers (Pat's round 1, Aryu's `context/teammates_2026-11-02/aryu_m12/`, Akshaj P, Akshat, Akshaj K converted from his Annual inputs + Review tabs) plus the new names in `inputs/m12/new_candidates_2026-11-03/` (`Round1_Four_Industries.xlsx` and `final_2026-11-03/`). Screens: being acquired, bank-like, FCF, $2bn; combined capex accepted (OR.PA, GE filled from the MISSING notes). Results and Meta update: `docs/new_candidates_results_2026-11-03.md`. Pat 3 Nov: top 2 per industry is a guide, several strong picks per industry are fine |
| `tools/round2_team.py newcands` + `handoff/final_round2_request_2026-11-03/` | Round 2 for HKEX, Tradeweb, Auto Trader (all fail value; HKEX capex ex HQ purchase, TW tax before NCI) -> `outputs/round2/Round2_scorecard_newcands.md`. Last request: Round 2 for DXCM, LULU, HLN, NVO, CW (optional ASM.AS, ADS.DE); `by_group/` splits it into split groups 3 (DXCM), 4 (LULU, HLN, NVO, ADS.DE) and 6 (CW, ASM.AS); groups 1, 2 and 5 have nothing left |
| `docs/final_list_2026-11-03.md` | The list after all Round 2 data: nine pass the value tests (ADBE, Trip.com, CTSH, PYPL, SAN.PA, NVDA with a Beneish flag, LULU and adidas with cash-flow caveats, NRG only on reported D&A), near misses, fails, Pat's decisions left. No research outstanding |
| `context/teammates_2026-11-03/aryu_round2_pat/` + `round2_groups34/` | Pat's fill of Aryu's Round 2 (CEG, NRG pro forma; RMD, ALC, EW; Kenon segment net debt, Basin Ranch) and groups 3-4 (DXCM; LULU, HLN, NVO, ADS.DE). `python tools/round2_team.py aryu|dxcm|consumer_pharma`; CEG D&A adds nuclear-fuel amortization (capex includes fuel); guidance ranges -> midpoint; missing year-3 consensus -> fade from year 2; `tools/kenon_sotp.py` updated ($46.39, 0.72x) |
| `tools/build_wave3_packages.py` -> `handoff/wave3_packages_2026-11-03/` | Wave 3 (Pat, 3 Nov, to fill the ~$16.6k left after the nine passes): 44 new names, 4 per industry in priority order, chosen for lower valuations and positive EPS three years ago, in Pat's three groups (1 aerospace + semis; 2 payments, power, medtech, software, consumer, pharma; 3 exchanges, IT, internet). Round 1 and Round 2 in one pass (prefilled workbooks), due Wed 4 Nov. Group 3 returned 3 Nov: `inputs/m12/wave3_2026-11-03/return1/`, `python tools/round2_team.py wave3_g3`: Genpact, Wolters Kluwer, Amdocs pass; Tencent and PDD pass but are flagged bank-like (Pat decides); B3 bank-like, Alibaba negative FCF |
| `handoff/ai_prompt_macro_redflags_2026-11-02.md` | AI prompt for the final macro and red-flag check on each pick and its competitors |
| `tools/etf_review.py` | ETF look-through, crash replays and M02 stress paths (16 Oct analysis) |
| `docs/` | `prompts/` = the October research prompts (Markdown); `model_input_guide_draft.md` = notes for the user's input-guide doc (create the real doc only when they say "create doc"); outlines for the M05 explanation and M08 memos; `assumptions_and_figures.md` traces every input and Stage 1/2 figure |
| `context/` | Handoff notes and imported Drive files |
| `handoff/news_monitor_2026-10-15/` | Handoff for a third person: thesis cards for the 11 shortlisted stocks, plus a daily news/signal log (RED/AMBER/GREEN) to 6 Nov |

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
    tilts: 70%. ETF plan (Pat): core VOO 70% + VXUS 30% (Trade_List B4/B6/B7), locked 15 Oct;
    tilts revised 16 Oct to XLI 3.0%, XLK 1.5%, XLV 2.5%, XLF 2.5% = 9.5% (XLC dropped, kept at 0%);
    loss budget 2% per position (Tilt_Sizing F4). Targets: bonds 33.6%, core 17.1% ($51,206: 50 VOO,
    183 VXUS), tilts $28,500, individual stocks 39.8% ($119,481, in SGOV until researched).
    Prices: WInS 14 Oct (XLF older). Fact sheets and crash replays: `docs/trading_notes_etfs.md`.
    India (INDA) and Mexico (EWW) were considered and rejected.
  - Bond_Ladder: the ten holdings bought 8 Oct 2026 (IBTM-IBTR funds for
    2033-37; Feb37, May38, Nov39, Nov40, Nov41 T-bonds for 2038-42). Cash
    spent $100,879.41 incl. $175 commissions. Blended locked-in yield 5.2423%
    (one yield giving the payments the same PV); Inputs B13 = 5.24% (RESEARCH).
    Fund yields are estimates. Trade_List has one "Bought" ladder row.
  - Inputs B14, B23 and rows 41/45 are cleared (Option 2 only).
  - 20 checks; all pass (verified with `formulas`). The simulation
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
  - Scorecards A-E total 56.25, 53.125, 59.375, 56.25, 25. Inputs (Q1..V2):
    A 100,75,100,75,50,25,0,25; B 75,100,75,100,0,50,25,0; C 50,50,50,50,100,75,50,50;
    D 25,25,25,25,75,100,100,75; E 0,0,0,0,25,0,75,100.
- Guide details: debt includes finance leases (not operating leases); market cap =
  price × contemporaneous common shares with share classes reconciled; rank only
  complete companies; gate = at least 5 complete companies and 80% coverage.
  Full spec for the peer data, plus R1-R7 and the video cross-check: `handoff/M12_score_spec.md`.
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
