# Universe screen, Round 2 results: packages 1, 3 and 5 (19 Nov 2026, TEST)

These packages came back on 19 Nov, after the universe screen of 17 Nov (`handoff/universe_packages_2026-11-17.md`). Packages 2 (consumer) and 4 (health care and industrials) are still out.

The method is the same as Pat's nine:
- value above price at beta 1.0, at the 5-year beta and at the full-history beta;
- upside/downside of at least 1.0 against the uniform DRAFT bear case;
- max position = $6,000 ÷ the worst calendar-year loss.

Valuation date is **30 Oct** (US 10-year 4.94%). Packages 1 and 5 gave only a 19 Nov collection price, so their 30 Oct closes come from Yahoo (`PX_30OCT` in `tools/round2_team.py`). Every scorecard also re-tests at the teammate's 19 Nov price. **Both dates give the same nine passes.**

Values are research estimates. They are never price targets, returns or position sizes.

## Scorecards

| Package | Standard method (FCFF) | Insurers and REITs |
|---|---|---|
| 1 | `outputs/round2/Round2_scorecard_pkg1.md` | — |
| 3 | `outputs/round2/Round2_scorecard_pkg3.md` | `outputs/round2/Round2_scorecard_pkg3_financials.md` (RI and FFO, `tools/value_financials.py`) |
| 5 | `outputs/round2/Round2_scorecard_pkg5.md` | — |

## Passes (9 of 24)

| Ticker | Method | Value / price at 30 Oct (beta 1.0, 5-year, full) | Bear / price | Piotroski, Beneish | Worst year (max position) | Caveat to check |
|---|---|---|---|---|---|---|
| FOXA | FCFF | 1.24, 1.64, 1.42 | 0.93 | 7/9, −2.22 | 2020 −20.2% ($29,673) | Valued as standalone Fox at 30 Oct. Year 1 is +2.8% without Roku (ASSUMPTION; the +32.3% consensus includes it). **Roku closed on 6 Nov**: $95.30 cash plus 0.9799 Class A shares per Roku share, with the $8.4bn bridge loan refinanced with notes on 13 Nov. So the 19 Nov re-test is not like for like: post-close price against pre-close debt and shares. A combined Fox + Roku valuation needs the top-up data. History only since 2019, so the max position is not meaningful |
| CMCSA | FCFF | 4.31, 5.28, 4.47 | 3.47 | 7/8, NOT CHECKED | 1994 −36.3% ($16,512) | The price implies growth 12.3 points a year below consensus: a value-trap test. The FY2025 base includes Versant (spun off). Capex excludes software and intangibles (MISSING). The NBCUniversal/Sky spin-off is pending |
| TMUS | FCFF | 1.81, 3.17, 2.46 | 1.24 | 6/9, −2.75 | 2009 −48.6% ($12,341) | Interest expense MISSING, so the cash check of 1.03 is generous. D&A above capex is held flat. Spectrum purchases are outside capex |
| EXE | FCFF | 1.62, 2.84, 3.07 | 1.16 | 7/8, NOT CHECKED | 2023 −14.8% ($40,615) | Commodity revenue (year 1 consensus −18.7%) with the 2025 margin held flat. Listed only since Feb 2021 (Chesapeake after bankruptcy), so the max position needs a proxy |
| FISV | FCFF | 4.19, 4.67, 4.50 | 3.13 | 6/9, −2.58 | 2025 −67.3% ($8,915) | The FY2025 margin of 27.5% is held flat despite the 2026 guidance reset |
| ACGL | RI | 1.15, 1.37, 1.32 | 0.95 | not applied | 1999 −42.0% ($14,301) | 3-year average ROE; catastrophe-loss years |
| EG | RI | 1.14, 1.35, 1.28 | 1.00 | not applied | 1999 −42.2% ($14,214) | The bear case is right at the price |
| VICI | FFO | 1.43, 1.92, 1.58 | 1.07 | not applied | 2024 −3.1% ($195,404) | Listed only since 2018, so the max position needs a proxy (for example the REIT loss in 2008) |
| O | FFO | 1.29, 1.74, 2.06 | 0.89 | not applied | 2020 −11.6% ($51,750) | Year-1 consensus MISSING, so year 2 is used |

## Fails (15)

| Package | Fails |
|---|---|
| 1 | INTU (full-history beta 0.97; upside/downside 0.17), QCOM (0.88; FY2026 GAAP margin 20.1% against 27.9% in FY2025, cause not in the workbook), TEL (0.91) |
| 3 | CBOE (0.62), JKHY (0.63), PGR (0.58, RI), KIM (FFO 1.10, but upside/downside 0.52; AFFO MISSING, so FFO is used) |
| 5 | EOG (0.34), APA (0.62), CF (0.89; at the 19 Nov price 0.95, 1.34, 0.98, a near miss), VMC (0.51), MLM (0.70), PEG, EXC, ED (negative values: see the method question below) |

## WInS eligibility (approved universe: a stock on WInS priced at $5 or more)

- **All 24 meet the price rule.** The lowest 19 Nov price is VICI at $24.22.
- All 24 are S&P 500 members listed on the NYSE, Nasdaq or Cboe BZX.
- **Package 3:** the teammate found all 9 in WInS equity research.
- **Packages 1 and 5:** the WInS listing is MISSING (not checked by the teammates). Pat can confirm each one in a WInS trade ticket.

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
  - **(b)** Add an equity-side method, as for banks and REITs. One example is residual income on book equity, using the allowed return on equity. This needs dividends per share and FY2023 equity from Aryu's package.

## Data handling

- **Package 1's price histories:**
  - INTU, QCOM and SPY are the teammate's Yahoo files.
  - TEL, FOXA, CMCSA and TMUS were fetched on 19 Nov with `tools/fetch_yahoo_monthly.py` (see `context/teammates_2026-11-19/package1/yahoo_monthly/SOURCES.md`).
  - Yahoo's `range=max` sends 3-month bars for long histories, so the tool asks for explicit dates and refuses to write a file with gaps.
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
