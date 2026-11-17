# Final Report plan (17 Nov 2026; due Fri 4 Dec, 5:00 pm ET)

Source: `2026_WGY_Final_Report-FINAL.pdf` (uploaded 17 Nov; CASE).

## Requirements

- **Purpose:** evaluate how the IPS strategy was implemented and give recommendations for Laura. It "is not an opportunity to create a new strategy or revise the IPS". It must not repeat the IPS or the Trading Notes Analysis.
- **Length:** 9-12 pages, excluding references.

  | Section | Pages |
  |---|---|
  | 1. Title page | 1 |
  | 2. Portfolio Implementation | 2-3 |
  | 3. Integrated Recommendation and Reflection | 6-8 |

- **Title page:** team name, member names, **advisor's first and last name**, WInS username.
- **Format:** Times New Roman 12, double-spaced (tables and graphics may be single-spaced), 1-inch margins, page numbers bottom-left. **APA citations for all sources, images, media and generative AI use**, plus a separate References page. No links that evaluators are expected to open. PDF of 5 MB or less, through SurveyMonkey Apply.
- **Section 2:**
  - A table of **every holding**: ticker, name, asset type, amount and %. It must be expressed at the original **$300,000** (total $300,000 and 100%), never at ending market value. Draft: `outputs/portfolio/final_report_holdings_table.md` (`python tools/portfolio_value.py --report-table`).
  - A narrative on how construction, allocation, diversification and the key holdings reflect the IPS and Laura's goals.
- **Section 3:**
  - What it must cover:
    - how the strategy supports the ten-year commitment;
    - the operating reserve;
    - a responsible facility contribution that preserves flexibility;
    - a **dollar range for 2031**, with its **confidence level** and the factors that could affect it;
    - **language for co-sponsors**;
    - assumptions, uncertainties and limitations;
    - **what to monitor** as 2031 and 2033 approach.
  - Projections start from $300k in 2027 plus $150k in 2028. Never add WInS gains or losses.
  - Then the **team reflection**: research, collaboration, disagreements, decisions and learning.
- **Permitted for all long-term modelling:** stocks, ETFs and Treasuries available on WInS. Not permitted: margin, shorts, crypto, derivatives, individual TIPS or STRIPS.
- **Graded on:**
  - investment strategy;
  - client knowledge;
  - portfolio analysis (quantitative and qualitative; WInS gains are not evidence);
  - articulation of the experience;
  - creativity and presentation (purposeful graphics and projections, co-sponsor communication).

## The 2023 winner's components (brianzhou.org/projects/wharton, read 17 Nov; RESEARCH)

That year's case was different ($100k, a 511-stock approved list), and their stock picking happened before their freeze. **Our holdings are frozen, so their selection steps become evaluation of our holdings, not new picks.** Cite the page in APA if any method is borrowed.

| Their component | Ours now | To do | Section |
|---|---|---|---|
| Model the client's goals first; **Monte Carlo** with a band of the middle 80% of runs | Structure model scenarios (16 paths) | **M07: block bootstrap with fixed seeds** on the floor rule (2027-2042). Gives funding certainty, the 2033 cushion distribution and the 2031 range with confidence | 3 |
| Sector fit (defensive and growth) | Three AI groups, sector tilts | One exposure table (M04 look-through: sector, country, AI, Nvidia through VOO and XLK) | 2 |
| **Country grades A-F** (stability, sovereign risk, policy, inflation, inequality, credit rating) | Macro context and red-flag reports (4 Nov) | Grade the 8 countries we hold, with the criteria labelled student judgment | 2 |
| Alpha above and beta below the industry average | Betas measured (5-year and full history) | Alpha and beta of each holding against its sector ETF, as an evaluation | 2 |
| Company score 0-100 from 12 statement numbers vs industry | **M12** (8 metrics, 0-100, ranked vs peers) | Report it as is; it is a research filter, not a return | 2 |
| Headline tone and a hand-graded management score | AI red-flag reports | Optional. Skip unless time allows | — |
| **Mean-variance optimizer** (minimum risk and best return per unit of risk) | None (sized by the 2% worst-year loss) | Diagnostic only: where our mix sits against a historical frontier. Not used to resize, and backtests do not prove future outcomes | 2 |
| One stock walked through in depth | DCF, reverse DCF, bear and stress tests | Pick one holding to show the full method (for example Wolters Kluwer or Euronet) | 2 |
| Charts that carry the story | Tables | Allocation chart, floor-and-cushion path, Monte Carlo fan, 2031 range chart, reserve ladder table | 2-3 |

## Work plan

1. **17-23 Nov (models):**
   - M07 Monte Carlo;
   - M05 reserve size and composition, connected to M02;
   - M08 facility contribution and the 2031 range;
   - M04 exposures plus the country grades, alpha/beta and frontier diagnostics.
2. **24-30 Nov (writing; US Thanksgiving is 26 Nov):** Pat writes Sections 2 and 3, the co-sponsor language and the reflection. Charts go in.
3. **1-4 Dec:**
   - APA references, including AI use;
   - formatting and page count;
   - advisor name and school documentation;
   - submit by 4 Dec, 5:00 pm ET.

## Pat's decisions (student judgments; never invented by the models)

- The definition of "high degree of certainty": the share of simulated paths that must fully fund all ten payments.
- The confidence level for the 2031 range.
- The flexibility hold-back: how much of the 2033 cushion to keep uncommitted.
- The rebalancing rule: yearly, or also after a large fall.
- The return assumptions: M02 LOW, BASE and HIGH.
