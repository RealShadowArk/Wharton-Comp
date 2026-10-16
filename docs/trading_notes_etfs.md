# ETF trades: fact sheets for writing your own Trading Notes (16 Oct 2026)

**These are research notes, not Trading Notes.** The rule is "Work generated
by an AI program may not be submitted as the team's own." For each trade:
1. Write the note yourself, in your own words, **before** clicking Buy.
2. Keep it to 300 characters, covering:
   - purpose;
   - fit with the strategy;
   - one piece of research;
   - its role.
3. Never edit it afterwards.

## The plan (locked 15 Oct; model `Trade_List`)

| Ticker | Role | Target | Shares at the 14 Oct WInS price | Cost |
|---|---|---|---|---|
| VOO | Core: US | $35,529 (11.8%) | 50 @ $707.43 | $35,371.50 |
| VXUS | Core: international | $15,227 (5.1%) | 182 @ $83.58 | $15,211.56 |
| XLI | Sector tilt | $9,000 (3.0%) | 53 @ $167.04 | $8,853.12 |
| XLK | Sector tilt | $7,200 (2.4%) | 37 @ $190.43 | $7,045.91 |
| XLV | Sector tilt | $5,400 (1.8%) | 31 @ $173.96 | $5,392.76 |
| XLC | Sector tilt | $3,900 (1.3%) | 35 @ $110.82 | $3,878.70 |
| XLF | Sector tilt | $4,500 (1.5%) | 82 @ $54.83 (**an older quote; refresh it**) | $4,496.06 |

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
| How the growth money is split | 10% sector tilts; the rest is 70% individual stocks and 30% core ETFs (team choices, 5 and 15 Oct) | Model / Pat |
| Why now | The strategy sets the stock share at the start and rebalances once a year: **no market timing**. The plan must be in place before the 6 Nov freeze. Prices only change the share count. | Strategy; competition emails |
| Main risk we're positioning for | An AI-spending bubble: tech + communication = 47.4% of the S&P 500 | S&P DJI, 31 Aug 2026 |
| 10-year Treasury | 5.29% (30 Sep 2026) | FRED DGS10 |

## Screening results (rules E1-E8 from `docs/stock_selection_rules.md`)

| Rule | VOO | VXUS | XLI | XLK | XLV | XLC | XLF |
|---|---|---|---|---|---|---|---|
| E1 Approved and tradeable in WInS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ **not yet checked in WInS** |
| E2 Clear role in the strategy | ✅ US core | ✅ international core | ✅ | ✅ | ✅ | ✅ | ✅ |
| E3 Cheapest researched way to get the exposure | ✅ 0.03% | ✅ 0.05% | ✅ 0.08% | ✅ 0.08% | ✅ 0.08% | ✅ 0.08% | ✅ 0.08% |
| E4 Median spread ≤ 0.05% | ✅ 0.01% (measured on IVV, same index) | ⚠️ not collected (a $156.5bn fund) | ✅ 0.01% | ✅ 0.01% | ✅ 0.01% | ✅ 0.01% | ✅ 0.02% |
| E5 1-year tracking difference within ±0.25 points | ✅ −0.04 | ⚠️ +0.68 (pricing-time effect, not a cost) | ✅ −0.08 | ✅ −0.10 | ✅ −0.14 | ✅ −0.07 | ✅ −0.08 |
| E6 Research support | ✅ core decision sheet | ✅ core and country research | ✅ "Research now" | ✅ "Research now" | ✅ "Research now" | ⚠️ sector research said **"Monitor"** | ✅ "Research now" |
| E7 Loss limit: size × worst year ≤ 2% (tilts) | n/a (core) | n/a (core) | ✅ 1.16% | ✅ 1.01% | ✅ 0.42% | ✅ 0.49% | ✅ 0.82% |
| E8 Concentration known and intended | ✅ top 10 = 37.9% | ✅ 15.0% | ✅ 39.1% | ⚠️ 64.5% (deliberate) | ✅ 60.0% | ⚠️ 76.7% (deliberate) | ✅ 57.8% |

⚠️ means "passes with a note" or "needs your check".
- **XLF** needs its WInS availability and price checked.
- **XLC** overrides the sector research's "Monitor" label. Say why (see its
  sheet).

---

## VOO: Vanguard S&P 500 ETF (US core)

- **What:** about 500 large US companies, weighted by size. Fee 0.03%.
- **Amount, $35,529:** 70% of the core money, which is 30% of the growth money
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
- **Amount, $15,227:** 30% of the core. The world market is about 36%
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
- **Amount, $9,000:** your largest, highest-conviction tilt. A repeat of 2008
  (−38.7%) would cost $3,483 (1.16%), within your 2% limit.
- **Why:**
  - grid, defence and AI data-center build-out;
  - EIA forecasts commercial electricity demand +5.3% in 2027;
  - Vertiv's backlog grew from $7.2bn to $15.0bn (your partner's research);
  - 10-year return 13.0% a year.
- **Why now:** structural demand. **Honest valuation:** J.P. Morgan forward
  P/E 22.5 vs its 19.6 average puts it near the top of its decade range
  (86/100).
- **Fit:** growth with a driver beyond software. It overlaps your electrical
  stocks on purpose.
- **Risk accepted:** an AI-spending pause would hit the data-center names.
  Correlation with the S&P 500 is 0.91.

## XLK: Technology Select Sector SPDR (tilt, 2.4%)

- **What:** S&P 500 tech; 75 holdings, top 10 = 64.5%, semiconductors 44.4%.
- **Amount, $7,200:** a repeat of 2000 (−41.9%) would cost $3,017 (1.01%).
  Kept smaller than XLI because VOO already holds 37.9% tech.
- **Why:**
  - the growth engine: 10-year return 24.7% a year;
  - WSTS forecasts chip sales +89.9% in 2026.
- **Why now:** J.P. Morgan forward P/E 21.5 is **below** its 2016-25 average
  of 23.0 (46/100). Tech is cheaper than usual on forward earnings.
- **Fit:** your deliberate growth bet, accepting overlap with VOO and your
  analog-chip stocks.
- **Risk accepted:** this *is* the AI-bubble risk. 2022: −27.7%.

## XLV: Health Care Select Sector SPDR (tilt, 1.8%)

- **What:** S&P 500 health care; 60 holdings, top 10 = 60.0%, pharma 36.0%.
- **Amount, $5,400:** a repeat of 2008 (−23.3%) would cost $1,258 (0.42%).
- **Why:**
  - CMS forecasts US health spending growth of 5.4% a year (2025-34);
  - the mildest crashes of your tilts (2022: −2.0%);
  - the lowest correlation of your tilts (0.71), so it diversifies away from
    AI.
- **Why now (honest):** you're buying it for **stability and its role, not
  value**. J.P. Morgan forward P/E 18.4 is **above its decade high** (18.3).
- **Fit:** steadier growth for the 2031-32 window. Overlaps your pharma and
  medical-device stocks on purpose.
- **Risk accepted:** drug-pricing policy; dependence on Eli Lilly (about 15%
  of the sector).

## XLC: Communication Services Select Sector SPDR (tilt, 1.3%)

- **What:** Alphabet, Meta and others; 22 holdings, top 10 = 76.7%.
- **Amount, $3,900:** kept small because two companies dominate. A repeat of
  2022 (−37.6%) would cost $1,466 (0.49%).
- **Why:**
  - digital advertising and AI platforms;
  - Alphabet's ad revenue was $81.6bn in Q2 2026 vs $71.3bn a year earlier.
- **Why now:**
  - J.P. Morgan forward P/E 18.6 vs its 17.9 average (54/100);
  - earnings yield 5.38% is just above the Treasury yield.
- **⚠️ Your sector research labelled it "Monitor"** because of concentration
  and one-off gains. Your note should show this is a **deliberate, small,
  higher-risk bet**.
- **Risk accepted:** a bet on two companies; antitrust; AI changing search.

## XLF: Financial Select Sector SPDR (tilt, 1.5%)

- **What:** S&P 500 financials; 76 holdings, top 10 = 57.8%:
  - Financial Services 30.8%, which includes Visa and Mastercard;
  - banks 27.1%.
- **Amount, $4,500:** a repeat of 2008 (−54.9%) would cost $2,471 (0.82%),
  within 2%.
- **Why:** your **hedge against an AI bubble**:
  - little AI exposure;
  - the cheapest growth-capable sector (J.P. Morgan forward P/E 14.1; earnings
    yield 7.09%, 1.8 points above the Treasury);
  - bank profits +12% in Q2 2026 (FDIC).
- **Why now:** cheap vs both bonds and the market; no sign of a banking
  crisis in your research.
- **Fit:** balances the AI-heavy core and the XLK/XLC tilts.
- **Risk accepted:**
  - a credit downturn (2008 peak-to-trough −82.9%);
  - overlap with your payments stocks.
- **⚠️ Check that XLF loads in WInS, and refresh its price.**

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
  - calculated the amounts, shares and loss limits;
  - organized facts from the team's research documents into these sheets.
- **Students:**
  - chose the funds, sizes and loss limits;
  - verified prices in WInS;
  - wrote every Trading Note.
