# Universe screen, Round 2 results: all five packages and follow-up Parts A and B (19 Nov 2026, TEST)

These came back on 19 Nov, after the universe screen of 17 Nov (`handoff/universe_packages_2026-11-17.md`) and the follow-up for the winner's-rule names (`handoff/universe_followup_2026-11-19/`). Package 2 (consumer) returned later on 19 Nov without its optional names. Package 4 (health care and industrials) and every follow-up item arrived later on 19 Nov:
- Everest's diluted shares;
- Expand Energy's cost lines;
- Comcast's expense lines and guidance record;
- Package 2's optional names, Deckers' evidence and Dollar General's interest.

**All 53 companies (36 refined shortlist + 17 winner's-rule optional) are now valued.**

**Pat's decisions, 19 Nov:**
- Fox (FOXA) is dropped.
- T-Mobile's worst year is its second worst, 2011 −31.3% (max position $19,169). There is no −93% year in its history; the worst is 2009 −48.6%.

The method is the same as Pat's nine:
- value above price at beta 1.0, at the 5-year beta and at the full-history beta;
- upside/downside of at least 1.0 against the uniform DRAFT bear case;
- max position = $6,000 ÷ the worst calendar-year loss.

Valuation date is **30 Oct** (US 10-year 4.94%). Packages 1 and 5 gave only a 19 Nov collection price, so their 30 Oct closes come from Yahoo (`PX_30OCT` in `tools/round2_team.py`). Every scorecard also re-tests at the teammate's 19 Nov price. **Both dates give the same passes.**

Values are research estimates. They are never price targets, returns or position sizes.

## Scorecards

| Package | Standard method (FCFF) | Insurers and REITs |
|---|---|---|
| 1 | `outputs/round2/Round2_scorecard_pkg1.md` | — |
| 3 | `outputs/round2/Round2_scorecard_pkg3.md` | `outputs/round2/Round2_scorecard_pkg3_financials.md` (RI and FFO, `tools/value_financials.py`) |
| 5 | `outputs/round2/Round2_scorecard_pkg5.md` | `outputs/round2/Round2_scorecard_utilities_financials.md` (utility RI, TEST) |
| 2 | `outputs/round2/Round2_scorecard_pkg2.md` (BF.B, CHD, DG); LULU, BKNG and DECK carry forward from 3 Nov (`consumer_pharma`, `akshat`, `wave3_g2`), same 30 Oct prices | — |
| 4 | `outputs/round2/Round2_scorecard_pkg4.md` (RMD carries forward: failed 3 Nov) | Cigna RI cross-check below |
| Part A | `outputs/round2/Round2_scorecard_partA.md` | — |
| Part B | `outputs/round2/Round2_scorecard_partB.md` | utilities: as package 5 |
| Fox + Roku (TEST) | `outputs/round2/Round2_scorecard_pkg1_foxroku.md` | — |

## Passes: 11 universe names (Fox dropped), plus Deckers (held)

| Ticker | Method | Value / price at 30 Oct (beta 1.0, 5-year, full) | Bear / price | Piotroski, Beneish | Worst year (max position) | Caveat to check |
|---|---|---|---|---|---|---|
| ~~FOXA~~ dropped (Pat, 19 Nov) | FCFF | 1.24, 1.64, 1.42 | 0.92 | 6/8, NOT CHECKED (no cost-of-revenue line) | 2020 −20.2% ($29,673) | Valued as standalone Fox at 30 Oct. Year 1 is +2.8% without Roku (ASSUMPTION; the +32.3% consensus includes it). **Roku closed on 6 Nov**: $95.30 cash plus 0.9799 Class A shares per Roku share, with the $8.4bn bridge loan refinanced with notes on 13 Nov. So the 19 Nov re-test is not like for like: post-close price against pre-close debt and shares. **Combined Fox + Roku TEST at the 19 Nov WInS price ($64.43): fails, 0.78 / 1.10 / 0.92, bear 0.52** (Roku's GAAP operating income is about zero, and the deal added about $10bn of net debt and 145m shares). History only since 2019, so the max position is not meaningful |
| LULU | FCFF (3 Nov inputs) | 1.50, 1.66, 1.19 | 1.18 | 6/9, −1.91 | 2008 −83.3% ($7,206) | Carried forward: year 1 −6.0% matches the current FY2026 guidance (−5% to −7%). Cash check 1.60, but 0.92 on reported cash flow. A securities complaint was filed 2 Nov (Package 2 legal line) |
| DECK (held) | FCFF (3 Nov inputs) | 1.54, 1.46, 1.60 | 1.11 | 5/9, −2.62 | 1998 −70.8% ($8,471) | Price only updated; management evidence MISSING |
| CI | FCFF | 1.87, 3.99, 2.11 | 1.28 | 7/9, −2.31 (Package 4 v2 cost lines) | 2008 −68.6% ($8,745) | **Fails on the teammate's residual-income rows (TEST): value $167–196 against $298** (ROE 11.2%, 3-year average). Book value includes Express Scripts acquisition goodwill, so RI on book understates. Tangible common equity is −$31.8bn (Package 4 v2), so RI on book says little. The FCFF counts cash trapped in regulated subsidiaries (parent-only cash $118m). Price fell to $273 by 19 Nov (Q3 update, 5 Nov). Pat decides the method |
| LDOS | FCFF | 1.63, 2.40, 2.06 | 1.12 | 8/9, −2.60 | 2011 −22.5% ($26,655) | Year 1 = FY2026 guidance +5.4%. Interest = net $203m. US government contracts. Price fell 13% to $124.76 by 19 Nov |
| CMCSA | FCFF | 3.54, 4.37, 3.68 | 2.71 | 8/9, −2.71 (cost of revenue = programming and production, ASSUMPTION) | 1973 −69.6% ($8,624) | The price implies growth 10.3 points a year below consensus: a value-trap test. The FY2025 base includes Versant (spun off). Capex now includes the $2,658m software spending. The worst year is since the 1972 listing (teammate); Yahoo's history from 1980 gives 1994 −36.3%. The NBCUniversal/Sky spin-off is pending |
| TMUS | FCFF | 1.81, 3.17, 2.46 | 1.24 | 6/9, −2.75 | 2011 −31.3% ($19,169), second worst (Pat) | The cash check (0.88) uses net interest of $3,774m, since gross interest is undisclosed. D&A above capex is held flat. Spectrum purchases are outside capex. The worst year comes from the MetroPCS predecessor history; the teammate prefers the post-2013 history (2014 −19.9%, max position $30,126): Pat decides |
| EXE | FCFF | 1.62, 2.84, 3.07 | 1.16 | 8/9, −1.98 (cost lines added) | 2023 −14.8% ($40,615) | Commodity revenue (year 1 consensus −18.7%) with the 2025 margin held flat. Listed only since Feb 2021 (Chesapeake after bankruptcy), so the max position needs a proxy |
| FISV | FCFF | 4.19, 4.67, 4.50 | 3.13 | 6/9, −2.58 | 2025 −67.3% ($8,915) | The FY2025 margin of 27.5% is held flat despite the 2026 guidance reset |
| ACGL | RI | 1.15, 1.37, 1.32 | 0.95 | not applied | 1999 −42.0% ($14,301) | 3-year average ROE; catastrophe-loss years |
| EG | RI | 1.14, 1.35, 1.28 | 1.00 | not applied | 1999 −42.2% ($14,214) | The bear case is right at the price |
| VICI | FFO | 1.43, 1.92, 1.58 | 1.07 | not applied | 2024 −3.1% ($195,404) | Listed only since 2018, so the max position needs a proxy (for example the REIT loss in 2008) |
| O | FFO | 1.34, 1.81, 2.14 | 0.91 | not applied | 2020 −11.6% ($51,750) | Year 1 now the FY2026 consensus +9.1% (Part A top-up) |

## Fails (15)

| Package | Fails |
|---|---|
| 1 | INTU (full-history beta 0.98; upside/downside 0.21), QCOM (0.88; FY2026 GAAP margin 20.1% against 27.9% in FY2025, cause not in the workbook), TEL (0.90) |
| 2 | BF.B (0.75 at beta 1.0; 1.52 at its 5-year beta 0.30), CHD (0.52), DG (0.73; interest and receivables MISSING), BKNG (carried forward: full-history beta 0.81) |
| 2 (optional) | GRMN (0.65), EXPE (0.90), DLTR (0.43), PM (0.58), WMT (0.09: capex far above D&A held flat) |
| 4 | BSX (0.83; year-2 consensus −0.45% to check), AOS (0.84; year 1 = consensus −12.6%; without China (TEST) 0.93, 0.91, 1.01, with the sale proceeds MISSING), CPRT (1.02, 1.01, 1.01 but upside/downside 0.06; cash ASSUMPTION), SNA (0.89), ALLE (0.77) |
| 3 | CBOE (0.62), JKHY (0.63), PGR (0.58, RI), KIM (0.79 on FAD $1.26, Kimco's AFFO-type measure from the Part A top-up; FFO gave 1.10 with upside/downside 0.52) |
| 5 | EOG (0.34), APA (0.62), CF (0.89; at the 19 Nov price 0.95, 1.34, 0.98, a near miss), VMC (0.51), MLM (0.70), PEG, EXC, ED (negative FCFF values; also fail on residual income: see below) |

## WInS eligibility (approved universe: a stock on WInS priced at $5 or more)

- **All 24 meet the price rule.** The lowest 19 Nov price is VICI at $24.22.
- All 24 are S&P 500 members listed on the NYSE, Nasdaq or Cboe BZX.
- **Package 3:** the teammate found all 9 in WInS equity research.
- **Package 1 (second return, 19 Nov):** all six were confirmed by exact ticker in the signed-in WInS (StockTrak) search, with delayed quotes from about 1:40 pm ET.
- **Package 5 and Part B:** all 15 pass the WInS ticker lookup, with 19 Nov WInS quotes (Part B workbook).
- **Part A:** all four have 19 Nov WInS quotes and exchanges (Nasdaq Global Select; Mastercard NYSE).

## Method question for Pat: regulated utilities (PEG, EXC, ED)

- **The problem:** capex is about equal to cash from operations, or above it:

  | Utility | Capex | CFO |
  |---|---|---|
  | PEG | 3,272 | 3,298 |
  | EXC | 8,529 | 6,254 |
  | ED | 4,764 | 4,800 |

  Rate-base growth is funded with new debt and equity, so FCFF at a flat capex share is negative for ten years.
- **Options:**
  - **(a)** Leave them as fails because the method does not fit.
  - **(b)** Add an equity-side method, as for banks and REITs: residual income on book equity.
- **Option (b), tested with the Part B utility rows (TEST, `python tools/value_financials.py utilities`):**
  - The five utilities (PEG, EXC, ED, ATO, AEP) **all still fail**, at 0.48 to 0.62 of the price at beta 1.0, and at most 0.73 at their own betas.
  - Reason: they trade at 1.6 to 2.2 times book value. Their 3-year ROEs are 9.0% to 13.8%; allowed ROEs are 8.9% to 11.5%. At beta 1.0, the cost of equity (9.94%) is at about the allowed return, so the method values them near book.
  - PEG's FY2023 ROE (17.6%) and ED's (12.0%) include one-off gains, so their averages are generous.
  - So **(a) and (b) give the same answer: no utility passes.** Only a method that credits years of rate-base growth above the cost of equity would value them near the price.

## Follow-up Parts A and B: the winner's-rule names (19 Nov)

All ten pass both screening rules (beta below and alpha above the industry). They were outside the refined top 3 on M12. **All ten fail the value tests.**

| Ticker | Value / price at 30 Oct (beta 1.0, 5-year, full) | Note |
|---|---|---|
| FTNT | 0.36, 0.35, 0.32 | Price implies 15.4 points a year more growth than consensus |
| PTC | 0.58, 0.61, 0.39 | FY2026 red-flag lines MISSING (10-K not yet filed); interest MISSING |
| CDNS | 0.35, 0.33, 0.28 | Price implies 14.9 points a year more growth |
| MA | 0.60, 0.71, 0.61 | Piotroski 8/8 |
| COP | 0.47, 1.09, 0.51 | Passes only at its 5-year beta (0.17); commodity revenue |
| XOM | 0.47, 1.05, 0.62 | Passes only at its 5-year beta (0.16); commodity revenue |
| PKG | 0.36, 0.45, 0.37 | Interest MISSING |
| ECL | 0.36, 0.42, 0.45 | |
| ATO | negative FCFF; RI 0.51, 0.56, 0.58 | Capex 4,174 against CFO 2,076 |
| AEP | negative FCFF; RI 0.48, 0.53, 0.54 | Debt = borrowings 54,416 at 30 Sep 2026 (finance leases MISSING) |

- **Debt MISSING only because finance leases are undisclosed or immaterial.** The tool uses the borrowings on each tab: FTNT 996.3, PTC 1,609.8, MA 19,000, AEP 54,416.
- **Qualcomm margin top-up:** the FY2026 EBIT fall of $3,697m is mostly recurring cost growth: R&D +$1,165m, SG&A +$591m, and stock pay up $657m.
  - One-offs are small: restructuring $332m, a $120m legal settlement against revenue, a $177m deferred-compensation loss offset below EBIT, and acquisition costs.
  - Without them, the margin is about 21.5%. **QCOM still fails.**

## Comparing the two rules (all 53 companies, Fox dropped)

| Rule | Companies valued | Pass the value tests |
|---|---|---|
| Refined (beta below the industry, refined top 3) | 36 | 12: ACGL, CI, CMCSA, DECK, EG, EXE, FISV, LDOS, LULU, O, TMUS, VICI |
| Winner's rule (also alpha above the industry) | 34 | 7: ACGL, CI, DECK, EG, LDOS, TMUS, VICI |

- Refined-only passes: CMCSA, EXE, FISV, LULU, O.
- **None of the 17 optional winner's-rule names passes.** Their higher past alpha comes with prices that already assume much faster growth.

## Still to come (19 Nov, after every return)

- **Package 4 feedback:** `handoff/teammate_followups_2026-11-19.md`, section "Package 4 feedback". Cigna and Leidos pass, so their items come first.
- **Not needed:**
  - **Nothing published:** Dollar General's receivables are not itemized; the utilities publish no company ROE (computed instead).
  - **Worst years missing for APA, VMC, ED, XOM, ECL and AEP:** the Yahoo series is used instead.
  - **PTC's FY2026 10-K lines:** PTC fails anyway.
- **Pat's decisions left:**
  - Cigna's method (FCFF passes, residual income fails);
  - max-position proxies for VICI (listed 2018) and EXE (listed 2021);
  - management grades after the rescreen;
  - which holdings get 2028 money.

## Data handling

- **Package 1, second return (19 Nov), `Wharton_Package1_Round2_v2.xlsx`:**
  - adds the 30 Oct closes;
  - Intuit's capex no longer counts software twice ($175m plus $46m software);
  - adds Comcast's software capex ($2,658m);
  - TE Connectivity's consensus now comes from QDD Research (+12.4%, +8.2%, +7.4%);
  - adds the WInS check;
  - includes all seven Yahoo files, which replace the four Claude had fetched (same months).
  The passes are unchanged.
- `tools/fetch_yahoo_monthly.py`: Yahoo's `range=max` sends 3-month bars for long histories, so the tool asks for explicit dates and refuses to write a file with gaps.
- **Package 5:** the teammate's original Yahoo files are used. The PortfoliosLab and Digrin alternatives are not used.
- **Overwritten DCF files:** `inputs/m03/INTU`, `QCOM` and `JKHY` now hold the packages' newer fiscal years. The 3 Nov versions are in git history.
- **Package 1 corrections:**
  - **QCOM tax:** the reported rate is −44.8%, because it includes the release of the FY2025 valuation allowance. The model uses 16.0% without it (ASSUMPTION).
  - **CMCSA tax** uses net income ÷ pretax income. Both include the Hulu gain: 22.4%, against 23.7% reported.

## Watchlist: Anthropic (ANT), listed 19 Nov 2026

- **Listing (Yahoo, 19 Nov):** Anthropic, PBC Class A common stock, NasdaqGS, ticker ANT.
- **First day (19 Nov):**

  | Measure | Value |
  |---|---|
  | Offering price | $83.00 (Yahoo's previous close) |
  | Opening price | $111.50 |
  | Range | $92.72 to $114.99 |
  | Last | $95.28 |

- **Deal, as reported in Yahoo Finance headlines (RESEARCH, unverified):** an $81bn raise at a $1.5tn valuation.
- **Screen status: it cannot pass now.**
  - It is not in the S&P 500 universe.
  - The beta test needs 60 monthly returns (testable from about Nov 2031). A stock with less history cannot pass.
  - Round 2 needs filed financials: the 3-year EPS for M12 and FY0 for the DCF (MISSING until taken from the prospectus).
  - The WInS listing is unchecked.
  - The WInS portfolio is frozen, so this only affects Section 3.
- **Conflict of interest:** Claude is made by Anthropic. Pat and the team should check every fact on this name themselves.
