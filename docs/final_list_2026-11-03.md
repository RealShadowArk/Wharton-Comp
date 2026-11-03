# Individual stocks: the list after all Round 2 data (TEST preview, 3 Nov 2026)

All research is in: every industry through Round 1 (M12), and every finalist through Round 2 with one method. That method is:

- a DCF at beta 1.0, at the 5-year beta and at the full-history beta;
- a uniform DRAFT bear case;
- Piotroski and Beneish red flags;
- the worst calendar year.

Pat, 3 Nov: the top-2 M12 rule is a guide (test 1 is advisory), and several picks from one industry are fine. Values are research estimates, never price targets, returns or position sizes. Bear cases and the reasons for investing are Pat's to write.

"Cash check" = the model's year-0 free cash flow / the cash flow actually reported. Above about 1.10, the model is generous.

## Pass the value tests

Test 2: value above price at all three betas. Test 3: upside/downside at least 1.0.

| Company | Industry | Value / price (beta 1.0, 5-year, full-history) | Bear / price | Red flags (Piotroski, Beneish) | M12 (all peers) | Max position ($6,000 / worst year) | Caveat |
|---|---|---|---|---|---|---|---|
| Adobe (ADBE) | Software | 1.58, 1.27, 1.26 | 1.04 | 7/9, -2.86 | 2nd of 10, 28/32 | $11,636 | none |
| Trip.com (9961.HK / TCOM) | Internet | 2.11, n/a (5-year beta 0.00), 1.97 | 1.43 | 7/9, -1.89 | 1st of 10 (group not released), 32/32 | $10,258 | China country risk premium included; 2025 one-off gains |
| Cognizant (CTSH) | IT services | 1.45, 1.61, 1.24 | 1.08 | 6/9, -2.50 | 8th of 13, 0/32 | $12,824 | cash check 1.13 |
| PayPal (PYPL) | Payments | 1.93, 1.60, 1.69 | 1.39 | 8/9, -2.54 | 3rd of 10, 4/32 | $9,641 | counts all corporate cash; the uniform bear is too mild |
| Sanofi (SAN.PA) | Pharma | 1.35, 2.69, 1.81 | 0.95 | 6/9, -2.60 | 8th of 10, 0/32 | $21,517 | none |
| Nvidia (NVDA) | Semis | 2.00, 1.03, 1.10 | 0.63 | **4/9, -1.17 (Beneish flag)** | 1st of 12, 32/32 | $7,247 | explain the Beneish flag (65% revenue growth) or drop; already a top-10 VOO holding |
| **Lululemon (LULU)**, new | Consumer brands | 1.50, 1.66, 1.19 | 1.18 | 6/9, -1.91 | 1st of 10, 32/32 | $7,206 (2008: -83.3%) | **cash check 1.60**: on its 2025 reported cash flow, 0.92x. Revenue guided down 5-7% this year |
| **NRG Energy (NRG)** | Power | 1.81, 1.50, 1.88 | 1.23 | 6/9, -2.49 | power group not released | $10,904 (2015: -55.0%) | **passes only with reported D&A** (1,866, which includes amortization of customer-acquisition costs whose cash cost sits in operating costs). With D&A = capex (Aryu's stricter treatment): 0.99x, bear 0.46. 2025 pro forma with the LS Power plants; capex is an ASSUMPTION |
| **adidas (ADS.DE)**, new | Consumer brands | 1.60, 1.44, 1.40 (1.51 with leases as debt) | 1.15 | 6/9, -2.26 | 3rd of 10, 7/32 | $11,668 (2022: -51.4%) | **2025 operating cash flow 751 vs 2,910 in 2024**: on 2025 reported cash flow, 0.31x at most. Stock pay and dilution MISSING |

The first six caps add up to $73,123. With Lululemon, NRG and adidas the total is $102,901, against the $119,481 individual-stock sleeve.

## Wave 3, group 3 (exchanges, IT, internet; returned 3 Nov)

`python tools/round2_team.py wave3_g3` -> `outputs/round2/Round2_scorecard_wave3_g3.md`.

| Company | Value / price (beta 1.0, 5-year, full-history) | Bear / price | Red flags | M12 | Max position | Caveat |
|---|---|---|---|---|---|---|
| **Genpact (G)** | 1.62, 2.38, 1.64 | 1.04 | 8/9, -2.73 | 5th of 17, 1/32 | $13,036 | none: cash check 0.80 (the model is conservative) |
| **Wolters Kluwer (WKL.AS)** | 1.42, 2.04, 1.61 | 0.98 | 6/9, -2.71 | 12th of 19 | $14,924 | 2025 operating income includes a disposal gain (amount MISSING); capex = combined line |
| **Amdocs (DOX)** | 1.49, 2.48, 1.34 | 1.12 | 6/9, -2.71 | 11th of 17 | $8,440 | cash check 1.19 |
| Tencent (0700.HK) | 1.34, 2.95, 1.43 | 0.78 | 8/9, -2.61 | screened out | $24,544 | **bank-like flag** (loan receivables inside operating cash flow): out unless Pat overrules; China |
| PDD (PDD) | 2.27, 10.04, 3.03 | 1.50 | 5/9, -2.10 | screened out | $8,930 | **bank-like flag** (merchant deposits inside operating cash flow): out unless Pat overrules; China; 5-year beta -0.03 is an artifact |

- **Near misses:** Japan Exchange Group (1.05x but upside/downside 0.18) and SAIC (1.11x, 0.69).
- **Fail:** TransUnion, Wipro, Match Group.
- **Screened out:** B3 (bank-like, no operating-income line) and Alibaba (negative free cash flow after AI capex).

**Filling the sleeve:** the nine passes above leave $16,580. Genpact alone ($13,036) covers most of it. Genpact plus Wolters Kluwer or Amdocs covers all of it.

## Wave 3, group 1 (semiconductors, aerospace and defence; returned 3 Nov)

`python tools/round2_team.py wave3_g1` -> `outputs/round2/Round2_scorecard_wave3_g1.md`. Yahoo's KRW, TWD, JPY and EUR files contain glitch months (for example, KRW at 0.11 in 2015-16), which are replaced by the Federal Reserve month-end rate supplied in the package.

| Company | Value / price (beta 1.0, 5-year, full-history) | Bear / price | Red flags | M12 | Max position | Caveat |
|---|---|---|---|---|---|---|
| MediaTek (2454.TW) | 3.30, 1.50, 2.67 | 0.81 | **4/9**, -2.51 | 11th of 16 | $12,529 (2022: -47.9%) | **driven by consensus growth of 15%, 77% and 69% in years 1-3**: check it before relying; the price has nearly tripled in 2026 |
| Samsung Electronics (005930.KS) | 1.46, 1.07, 1.28 | 0.67 | 6/9, -2.64 | 8th of 16 | $14,664 (2008: -40.9%) | **driven by consensus revenue growth of 117% next year** (a memory boom): check it; memory is cyclical; stock pay MISSING; preferred shares counted |

- **Fail:** NXP (0.87x), Tokyo Electron (0.75x), Thales (0.92x), Leonardo (0.64x), Airbus (0.74x, also flagged bank-like for Airbus Bank).
- **Screened out:** Textron (bank-like: Textron Financial; no operating-income line or classified balance sheet).

## Near misses

| Company | What fails |
|---|---|
| dLocal | upside/downside 0.91 |
| Intuit | 0.97x at the full-history beta |
| Qualcomm | 0.84x and 0.97x at measured betas |
| Booking | 0.81x at the full-history beta |
| Auto Trader | 0.97x at beta 1.0 |
| Alcon | 0.93x at beta 1.0 (1.03x and 1.11x at its lower measured betas) |
| Haleon | 0.91x at beta 1.0 (passes only at its 0.15 beta, from 51 months of data) |

## Fail

Adyen, CME, ICE, Moody's, Infosys, TCS, ServiceNow, Nike, PepsiCo, Coca-Cola, Novartis, AstraZeneca, Lam Research, ASML, General Dynamics, Huntington Ingalls, Elbit, HKEX, Tradeweb, Curtiss-Wright, ASM International, Dexcom (0.41x), Novo Nordisk (0.70x), Constellation Energy (0.39x), ResMed (0.77x), Edwards (0.41x).

Kenon: 0.72x on the parts valuation, updated with the Round 2 facts: central $46.39, range $27.46-66.65. Meta is not validly valued by the method.

## What is left (wave 3 group 2 still out: optional now)

1. **Pat's decisions:**
   - Nvidia's Beneish flag.
   - NRG's D&A treatment (the pass depends on it).
   - Whether the cash-flow caveats on Lululemon and adidas rule them out.
   - Corpay (bank-like, screened out).
   - Scoring loss-three-years-ago companies without G2.
   - The final picks and position sizes, and where unused sleeve money goes.
2. **Before orders (Thu 5 Nov):**
   - Run the macro and red-flag AI check on the final picks (`handoff/ai_prompt_macro_redflags_2026-11-02.md`).
   - Check the price in WInS for each pick (Aryu's names, including NRG, were not checked in WInS).
   - Write the bear cases and reasons in Pat's own words.
3. **Small data gaps (not blocking):**
   - stock pay and dilution for adidas;
   - dilution for Novo;
   - pro forma operating cash flow for CEG and NRG;
   - continuing operating cash flow for Edwards.

Akshaj R used the 3-month Treasury par yield (4.16%) for his Sharpe ratios; the team uses FRED DTB3 (4.00%).
