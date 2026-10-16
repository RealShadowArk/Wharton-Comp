# ETF trades: fact sheets for writing your own Trading Notes (updated 16 Oct 2026)

**These are research notes, not Trading Notes.** The rule is "Work generated
by an AI program may not be submitted as the team's own." For each trade:
1. Write the note yourself, in your own words, **before** clicking Buy.
2. Keep it to 300 characters, covering:
   - purpose;
   - fit with the strategy;
   - one piece of research;
   - its role.
3. Never edit it afterwards.

## The plan (core locked 15 Oct; tilts revised 16 Oct; model `Trade_List`)

| Ticker | Role | Target | Shares at the 14 Oct WInS price | Cost |
|---|---|---|---|---|
| VOO | Core: US | $35,844 (11.9%) | 50 @ $707.43 | $35,371.50 |
| VXUS | Core: international | $15,362 (5.1%) | 183 @ $83.58 | $15,295.14 |
| XLI | Sector tilt | $9,000 (3.0%) | 53 @ $167.04 | $8,853.12 |
| XLK | Sector tilt | $4,500 (1.5%) | 23 @ $190.43 | $4,379.89 |
| XLV | Sector tilt | $7,500 (2.5%) | 43 @ $173.96 | $7,480.28 |
| XLF | Sector tilt | $7,500 (2.5%) | 136 @ $54.83 (**an older quote; refresh it**) | $7,456.88 |
| ~~XLC~~ | Dropped 16 Oct | $0 | n/a | n/a |

The tilts total **9.5%**. The 0.5% taken from health care went back into the
growth money, which raised the individual-stock target to **$119,481** and
VXUS by one share.

**What changed on 16 Oct, and why:**

| Change | Reason |
|---|---|
| XLC dropped | It failed the 5-10-year stability test (see the XLC entry below) |
| XLK 2.4% → 1.5% | Purest exposure to the main risk (an AI bubble). It is kept small, as insurance in case AI keeps winning. |
| XLV 1.8% → 2.5% | More stability. Held below 3% because the individual stocks may add health care. |
| XLF 1.5% → 2.5% | Hedge against an AI-specific bust. Capped because a credit crash is the plan's thinnest stress path (S1). |

**Before each order:**
- refresh the price (WInS shows prices 15 minutes late but fills at the live
  bid/ask);
- recompute shares = target ÷ price, rounded down;
- the commission is $25 per trade.

## Facts that apply to every ETF trade

| Fact | Value | Source |
|---|---|---|
| Laura's goals | Grow money before 2033; ten fixed $50,000 payments in 2033-2042; a credible facility contribution | Case study pp. 2-4 |
| Payments already secured | A Treasury ladder bought 8 Oct, locked at 5.24%, held to maturity | Bond_Ladder tab |
| Why stocks are 66.4% of the portfolio | Floor rule: stocks = 2 × the money above the cost of the bonds. Laura's money in 2028 = $465,720; floor = $311,111; cushion = $154,609; stocks = $309,219 = 66.4%. | Structure model v4 |
| How the growth money is split | 9.5% sector tilts; the rest is 70% individual stocks and 30% core ETFs (team choices, 5, 15 and 16 Oct) | Model / Pat |
| Why now | The strategy sets the stock share at the start and rebalances once a year: **no market timing**. The plan must be in place before the 6 Nov freeze. Prices only change the share count. | Strategy; competition emails |
| Main risk we're positioning for | An AI-spending bubble: tech + communication = 47.4% of the S&P 500 | S&P DJI, 31 Aug 2026 |
| 10-year Treasury | 5.29% (30 Sep 2026) | FRED DGS10 |
| Stress paths 2027-2033 (M02 S1-S8) | All eight cover the $401,623 reserve. Thinnest: S1 credit crash in 2032 ($40,162 spare); next S3 AI-spending pause 2030-32 ($47,521) | `structure/plan.py`, 16 Oct |

## Screening results (rules E1-E8 from `docs/stock_selection_rules.md`)

| Rule | VOO | VXUS | XLI | XLK | XLV | XLF |
|---|---|---|---|---|---|---|
| E1 Approved and tradeable in WInS | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ **not yet checked in WInS** |
| E2 Clear role in the strategy | ✅ US core | ✅ international core | ✅ | ✅ | ✅ | ✅ |
| E3 Cheapest researched way to get the exposure | ✅ 0.03% | ✅ 0.05% | ✅ 0.08% | ✅ 0.08% | ✅ 0.08% | ✅ 0.08% |
| E4 Median spread ≤ 0.05% | ✅ 0.01% (measured on IVV, same index) | ⚠️ not collected (a $156.5bn fund) | ✅ 0.01% | ✅ 0.01% | ✅ 0.01% | ✅ 0.02% |
| E5 1-year tracking difference within ±0.25 points | ✅ −0.04 | ⚠️ +0.68 (pricing-time effect, not a cost) | ✅ −0.08 | ✅ −0.10 | ✅ −0.14 | ✅ −0.08 |
| E6 Research support | ✅ core decision sheet | ✅ core and country research | ✅ "Research now" | ✅ "Research now" | ✅ "Research now" | ✅ "Research now" |
| E7 Loss limit: size × worst year ≤ 2% (tilts) | n/a (core) | n/a (core) | ✅ 1.16% | ✅ 0.63% | ✅ 0.58% | ✅ 1.37% |
| E8 Concentration known and intended | ✅ top 10 = 39.0% (IVV, same index, 9 Oct) | ✅ 15.0% | ✅ 39.1% | ⚠️ 64.5% (deliberate) | ✅ 60.0% | ✅ 57.8% |

⚠️ means "passes with a note" or "needs your check". **XLF** needs its WInS
availability and price checked.

## Combined sector exposure of all ETFs (16 Oct)

As a % of the $300,000 portfolio, using VOO's sector weights (31 Aug). Each
tilt fund counts 100% in its own sector. VXUS's sector split was not collected,
so it is not guessed.

| Sector | Through VOO | Tilt | Total | Total share of US fund money | S&P 500 weight |
|---|---|---|---|---|---|
| Information Technology | 4.47% | 1.46% | 5.93% | 28.0% | 37.9% |
| Industrials | 0.98% | 2.95% | 3.93% | 18.6% | 8.3% |
| Financials | 1.45% | 2.49% | 3.93% | 18.6% | 12.3% |
| Health Care | 1.09% | 2.49% | 3.59% | 16.9% | 9.3% |
| Communication Services | 1.12% | 0 | 1.12% | 5.3% | 9.5% |
| Other five sectors | 2.68% | 0 | 2.68% | 12.7% | 22.7% |
| International (VXUS) | | | 5.10% | n/a | n/a |

**What this shows:**
- The US fund money is **below** the market in tech and communication, on
  purpose (the AI-bubble risk).
- It is **above** the market in industrials, financials and health care.
- The individual stocks (39.8% of the portfolio) will move these figures much
  more than the tilts do.

## Crash replays (one calendar year, % of the $300,000; bonds and cash held flat)

Calculated 16 Oct for the final plan above.

| Year | All ETFs | Tilts only |
|---|---|---|
| 2008 | −10.4% | −3.7% |
| 2018 | −1.8% | −0.6% |
| 2020 | +4.0% | +1.3% |
| 2022 | −3.9% | −0.9% |
| Each fund's worst year at once (TEST) | −10.4% | −3.7% |

**Sources:**
- VOO: IVV NAV;
- VXUS: IXUS NAV, with the MSCI ACWI ex USA IMI index for 2008;
- sector funds: SPDR NAV calendar returns from the industry research.

**The bond ladder in the same years:**
- **2022-type:** if yields rise 2.5 points, the ladder falls about $17k
  (−17%) on paper.
- **2008-type:** if yields fall 1.5 points, it rises about $12.5k.
- The payments are unaffected either way, because the bonds are held to
  maturity.

---

## VOO: Vanguard S&P 500 ETF (US core)

- **What:** about 500 large US companies, weighted by size. Fee 0.03%.
- **Amount, $35,844:** 70% of the core money, which is 30% of the growth money
  left after tilts.
- **Why this fund:** the cheapest S&P 500 tracker researched (IVV has the same
  fee). Equal-weight RSP was rejected because of its 0.20% fee and its
  10-year lag of 3.9 points a year.
- **Why now:** the strategy says invest from the start. J.P. Morgan forward
  P/E is 19.0 vs its 2016-25 average of 19.1, so neither cheap nor
  expensive; its earnings yield (5.26%) roughly equals the Treasury yield.
- **Fit with Laura:**
  - earns the stock return the floor rule depends on;
  - very easy to trade, which the yearly Option 3 rebalancing needs;
  - the payments are already covered by the bonds.
- **Key facts:**
  - IT 37.9% (31 Aug);
  - 10-year return 15.3% a year (IVV, to 30 Sep);
  - 2008: −36.9% (IVV).
- **Risk accepted:** concentration in AI-linked giants. The international
  fund, the tilts and the stock picks offset it.

## VXUS: Vanguard Total International Stock ETF (international core)

- **What:** about 8,700 non-US stocks in 43 markets:
  - by region: Europe 36.4%, Pacific 28.5%, emerging markets 26.2%, Canada
    8.1%;
  - top countries: Japan 15.5%, Taiwan 8.7%, UK 8.3% (31 Aug).
- **Fee:** 0.05%.
- **Amount, $15,362:** 30% of the core. The world market is about 36%
  international; you're slightly under that because Laura's payments are in
  USD (your judgment).
- **Why this fund:** cheaper (0.05%) than IXUS (0.07%) and ACWI (0.32%). Broad
  instead of single-country bets, which were researched and rejected.
- **Why now:** foreign markets are cheaper than the US:
  - P/E: developed markets (EAFE) 17.4 and emerging markets 14.9, vs about
    29.6 for IVV;
  - in 2022 IXUS fell −16.4% vs −18.1% for IVV.
- **Fit with Laura:** diversifies US-specific risk (valuation, concentration)
  in the growth money only. The payments are untouched.
- **Risk accepted:**
  - **currency:** in 2022 the dollar took 7.45 points off international
    returns;
  - **not a crash hedge:** monthly correlation with the US is 0.84.

## XLI: Industrial Select Sector SPDR (tilt, 3.0%)

- **What:** S&P 500 industrials; 83 holdings, top 10 = 39.1% (the most spread
  out of your tilts).
- **What's inside:** weights are approximate, from secondary sites dated
  Aug-1 Oct 2026, because the issuer site could not be reached.

  | Group | Largest names | Link to AI / data centers |
  |---|---|---|
  | Aerospace and defence | GE Aerospace 6.0%, RTX 4.7%, Boeing ~3%, Lockheed Martin ~2% | Low |
  | Machinery (20.2%, issuer, 13 Oct) | Caterpillar 7.1%, Deere 3.1%, Parker-Hannifin ~2% | Partial: Caterpillar has power-related customers |
  | Electrical equipment (15.6%, issuer, 13 Oct) | GE Vernova 4.9%, Eaton 3.2% | **High** |
  | Transport | Union Pacific 3.0%, Uber ~2.7%, UPS 1.3% | Low |

  Roughly a fifth to a quarter of XLI is tied to AI power (**judgment**).
- **Amount, $9,000:** your largest tilt. A repeat of 2008 (−38.7%) would cost
  $3,483 (1.16%), within your 2% limit.
- **Why:**
  - grid, defence and AI data-center build-out;
  - EIA forecasts commercial electricity demand +5.3% in 2027;
  - Eaton's Q2 2026 Electrical Americas sales were up 18% organically, and
    its backlog was up 33%;
  - 10-year return 13.0% a year.
- **Overlap:** VOO holds only 8.3% industrials (about 1% of the portfolio), so
  XLI is not a double count of VOO. The real overlap is with your electrical
  stocks.
- **Why now:** structural demand. **Honest valuation:** J.P. Morgan forward
  P/E 22.5 vs its 19.6 average puts it near the top of its decade range
  (86/100). That's expensive compared with its own history; it is not a rating.
- **Risk accepted:**
  - An AI-spending slowdown would cut orders for the power-equipment names, and
    their prices would fall when spending plans change, not when backlogs run
    out.
  - Correlation with the S&P 500 is 0.91. The 2008 drawdown was −62%.

## XLK: Technology Select Sector SPDR (tilt, 1.5%)

- **What:** S&P 500 tech; 75 holdings, top 10 = 64.5%, semiconductors 44.4%.
- **Amount, $4,500 (cut from 2.4% on 16 Oct):** a repeat of 2000 (−41.9%)
  would cost $1,886 (0.63%).
- **Role:** insurance in case AI keeps winning, rather than a conviction bet.
  - In 2020 XLK returned +43.7%.
  - 10-year return 24.7% a year.
  - WSTS forecasts chip sales +89.9% in 2026.
- **Kept small because:**
  - VOO already holds 37.9% tech;
  - this is the purest exposure to your main risk;
  - your US fund money stays below the market in tech (28.0% vs 37.9%) even
    with XLK.
- **Valuation, honestly:** J.P. Morgan forward P/E 21.5 is below its 2016-25
  average of 23.0 (46/100). But "forward" uses analysts' AI earnings
  forecasts, and an AI bubble is exactly the risk that those forecasts fail.
- **Risk accepted:** 2022: −27.7%; 2008 drawdown −53%.

## XLV: Health Care Select Sector SPDR (tilt, 2.5%)

- **What:** S&P 500 health care; 60 holdings, top 10 = 60.0%, pharma 36.0%.
- **Amount, $7,500 (raised from 1.8%; 2.5% rather than 3.0%):** a repeat of
  2008 (−23.3%) would cost $1,748 (0.58%).
- **Why:**
  - CMS forecasts US health spending growth of 5.4% a year (2025-34);
  - the mildest crashes of your tilts (2022: −2.0%);
  - the lowest correlation of your tilts (0.71), so it diversifies away from
    AI.
- **Why now (honest):** you're buying it for **stability and its role, not
  value**. J.P. Morgan forward P/E 18.4 is **above its decade high** (18.3).
- **Stable is not safe:** 2008 −23.2%; 2007-09 drawdown −39%; 2020 drawdown
  −28%.
- **Fit:** steadier growth for the 2031-32 window.
- **Watch:** health care stocks in the individual sleeve add to this bet.
  Drug-pricing policy is one shared risk, and Eli Lilly is about 15% of the
  sector.

## XLF: Financial Select Sector SPDR (tilt, 2.5%)

- **What:** S&P 500 financials; 76 holdings, top 10 = 57.8%:
  - Financial Services 30.8%, which includes Visa and Mastercard;
  - banks 27.1%.
- **Amount, $7,500 (raised from 1.5%):** a repeat of 2008 (−54.9%) would cost
  $4,118 (1.37%), within 2%.
- **Why:** a **hedge against an AI-specific bust**:
  - earnings come from lending, fees and payments rather than AI spending;
  - the cheapest growth-capable sector (J.P. Morgan forward P/E 14.1; earnings
    yield 7.09%, 1.8 points above the Treasury);
  - bank profits +12% in Q2 2026 (FDIC).
- **Corrected 16 Oct (honest):**
  - Its AI exposure is *indirect*, not zero. Lenders finance data-center
    construction, and asset managers' fees depend on AI-heavy markets
    (judgment).
  - It is **not** low-risk: it has the worst crash record of any fund you hold.
    2008 −55.3%; 2007-09 drawdown −82.9%; 2020 drawdown −42.9% in five weeks.
  - **Warning signs don't protect us.** The portfolio freezes on 6 Nov, and
    the strategy does no market timing.
- **Why capped at 2.5%:** a credit crash just before 2033 (S1) is the stress
  path that leaves Laura's plan the least spare money.
- **Fit:** balances the AI-heavy core and XLK.
- **Risk accepted:**
  - a credit downturn;
  - overlap with your payments stocks.
- **⚠️ Check that XLF loads in WInS, and refresh its price.**

## Rejected 16 Oct: XLC (Communication Services Select Sector SPDR)

Kept here for the rejection log and the IPS (no trade, no note).

- **The test it failed:** stability over 5-10 years.
  - worst year 2022: −37.6%; 2022 drawdown −41.6%;
  - 5-year return 7.9% a year vs 13.8% for the S&P 500;
  - 22 holdings, top 10 = 76.7%;
  - correlation with the S&P 500 0.88.
- Its two dominant companies are among the largest AI spenders, and AI search
  threatens Google's core business. That's the same risk as XLK, not a hedge.
- **The only case for it is valuation** (forward P/E 13.8, issuer, 13 Oct), a
  higher-risk argument, not a stability one. The sector research also labelled
  it "Monitor".
- **Exposure kept:** VOO still holds 9.5% communication services (about 1.1%
  of the portfolio).

---

## Checklist for each note

- [ ] **What** you're buying and its **role** (core or tilt; growth,
  diversifier, hedge).
- [ ] **How it fits** the floor-rule strategy and Laura.
- [ ] **One research fact**, with the number.
- [ ] **One risk** you accept.
- [ ] 300 characters or fewer, your own words, written **before** clicking Buy.

## AI-use record (add to Works Cited / M10 log)

- **Date:** 16 Oct 2026. **Tool:** Claude (Anthropic), via Claude Code.
- **Claude:**
  - calculated the amounts, shares, loss limits, sector look-through and crash
    replays;
  - organized facts from the team's research documents into these sheets;
  - looked up approximate XLI holdings on secondary websites.
- **Students:**
  - chose the funds, sizes and loss limits (tilts revised 16 Oct);
  - verified prices in WInS;
  - wrote every Trading Note.
