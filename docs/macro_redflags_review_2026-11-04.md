# Macro and red-flag review, 4 November 2026

This review covers all 21 company reports in `handoff/macro_redflags_2026-11-04/results/`, plus the portfolio check (the portfolio prompt, done here instead of in a separate chat).

The reports are AI output. This summary is also AI analysis. Pat rewrites the conclusions in his own words before anything is submitted. Labels used below:
- **FACT** = stated in a report, with its source.
- **TEST** = our own rerun.
- **JUDGMENT** = opinion.

The retests can be reproduced with `python tools/retest_redflags_2026-11-04.py`. Official outputs are unchanged.

## 1. Checks on our numbers

| Company | What the report found | Already in our model? | Retest (TEST) |
|---|---|---|---|
| **Amdocs (DOX)** | On 3 Nov, FY2027 guidance was revenue -14.3% to -17.9% (reported) and EPS -26% to -30%. Amdocs and T-Mobile (19.9% of FY2025 revenue) have sent each other material-breach notices. After hours the shares were $34.58 vs a $62.43 close (secondary feed). The 4 Nov close is MISSING. | **No.** Year 1 was +3.2%. | See the Amdocs table below. |
| **Wolters Kluwer (WKL.AS)** | FY2025 IFRS operating profit of €1,735m includes a **€232m disposal gain** (FRR). | **Yes, the gain is included.** EBIT margin 28.33% = 1,735 / 6,125. | Excluding the gain (margin 24.54%): value/price 1.23 / 1.77 / 1.39 (was 1.42 / 2.04 / 1.61). Bear 0.84 (was 0.98). Upside/downside 1.49 (was 21.59). **Still passes**, with a thinner cushion. The €232m needs a human check in the annual report. | **Applied 4 Nov (Pat).** |
| **Trip.com (TCOM)** | The workbook's FY2025 operating cash flow (RMB 19,625m) is the audited **FY2024** figure. FY2025 is RMB 14,379m (it is in the teammate's own Red flags tab). | **The value is unaffected** (the DCF does not use CFO). The cash check is affected. | Cash check **0.80 → about 1.14**, so Trip.com moves from Clean to the Mild-caveat band (above 1.10). Value/price 2.11 / 1.97 has a large margin. The RMB 5.18bn SAMR fine paid in 2026 is about RMB 7.50 per share (2.8% of price) and is not in the model. | **Applied 4 Nov (Pat).** |
| Deckers (DECK) | Sales guidance cut on 22 Oct. | Yes: year 1 uses $5.700–5.725bn. | None needed. |
| Euronet (EEFT) | Revenue guidance cut on 27 Oct to about $4.375bn. | Yes: the guidance file uses $4.375bn. | None needed. |
| Lululemon (LULU) | FY26 revenue guidance -5% to -7%. | Yes. | None needed. |
| Cognizant (CTSH) | Growth range narrowed on 29 Oct to 4.0–4.4% at constant currency. | Year 1 is 4.70%; it is unclear whether that is the reported-dollar range. | Pat to check the range used. A 0.5-point difference in year 1 moves value by well under 1% (JUDGMENT). |
| Reckitt (RKT.L) | Core growth guidance cut on 27 Oct. | Year-1 consensus implies £13.14bn, close to the post-results S&P figure of £13.1bn (29 Oct). | None needed. |
| Genpact (G) | India tax assessment of $792m (on appeal at India's Supreme Court, no reserve). | Not in the model. | $792m = **$4.61 per share**, 12% of the $39.62 price. Value is 1.62× price, so a loss would not break the case on its own (JUDGMENT). |

**Amdocs retest** (all TEST). Year 1 is set to the -16.1% guidance midpoint, as the method requires. Years 2-3 are still the pre-dispute consensus, which is stale (updated consensus MISSING).

| Variant | Beta 1.0 | 5-year beta 0.42 | Full-history beta 1.16 | Bear (beta 1.0) |
|---|---|---|---|---|
| As run (year 1 +3.2%) | $93.77 (1.49× at $62.83) | $155.98 | (1.34×) | $70.46 |
| Year 1 -16.1% | $75.68: 1.20× at $62.83, 2.19× at $34.58 | $126.25 | $68.17: 1.09× / 1.97× | $63.49 |
| Year 1 -16.1%, margin × 19.5/21.6 (guided adjusted-margin drop) | $69.07: 1.10× / 2.00× | $115.45 | $62.19: **0.99×** / 1.80× | $58.09 |

JUDGMENT on Amdocs: at the after-hours price it passes easily, but the model cannot see the main risk, which is whether T-Mobile leaves. At the old price it is borderline. Two options:
- drop it (it was the smallest mild-caveat name, max $8,440);
- hold off until the 4 Nov close and updated consensus.

Pat decides.

## 2. Each company

The tier shown is from the 4 Nov cards. The "main red flags" are the report's RED items, plus anything that changes the model. Report dates are 2026.

### Core list (clean + mild caveats)

**Adobe (ADBE), Clean, max $11,636**
- Main red flags (RED in the report):
  - Cheaper rivals are pulling routine design work out of Creative Cloud: Canva's free Affinity tools, Figma's AI features and Microsoft Copilot.
  - AI costs are rising faster than revenue: subscription delivery costs +24% vs subscription revenue +14%. Our model holds the margin flat, so it cannot see this squeeze.
  - A US court order forces easier cancellation ($75m penalty plus $75m of free services), and the UK CMA case is still open.
- Also:
  - The new CEO starts 1 Dec.
  - $850m of notes are due Feb 2027.
  - Figma reports 4 Nov after the close.
- Model: no input change. The bear case (margin × 0.8) gives 1.04×, so the cushion is thin if margin and pricing weaken together.
- JUDGMENT: keep.

**Trip.com (TCOM), Clean → Mild after the fix, max $10,258**
- Main red flag (RED): China's antitrust order. SAMR fined Trip.com RMB 5.18bn and banned hotel exclusivity and forced lowest-price terms. Trip.com may have to accept lower commissions, so a margin anchored on FY2025 could be too high.
- Also:
  - Agoda signed a five-year deal with H World (a Trip.com hotel partner).
  - The $1.5bn convertible can be put back to Trip.com for cash in June 2027.
  - About RMB 10.5bn of China cash cannot be paid out to the parent.
  - The shares are +4.5% (ADS) since 30 Oct.
- Model:
  - the cash-check correction above (0.80 → about 1.14);
  - the fine is about 2.8% of the price.
- JUDGMENT: still the strongest value case. Move it to the mild-caveat tier.

**Sanofi (SAN.PA), Clean, max $21,517**
- Main red flags (RED):
  - **Dupixent is 39% of sales.** Its compound patents run out in 2031 (US), 2032 (EU, 2033 with paediatric extensions) and 2034 (Japan), right at the start of the 2033-2042 window. Biosimilars are in development (Bio-Thera, Qilu phase 3).
  - Dupixent lymphoma lawsuits: 40 federal cases, now in discovery.
- Also:
  - Pipeline setbacks: amlitelimab dropped in eczema, itepekimab stopped.
  - Divestitures take about €1.3bn of 2027 sales.
  - Guidance was raised on 30 Oct (already in the team's notes).
- Model: no change. The 0.73 cash check is conservative. Bear 0.95.
- JUDGMENT: keep, but the 2033+ Dupixent cliff belongs in the long-term risk section of the report.

**Genpact (G), Clean, max $13,036**
- Main red flags (RED), both in India:
  - The Enforcement Directorate's seizure of the Gurgaon office was upheld.
  - The $792m tax assessment is at the Supreme Court ($4.61 per share).
- Also:
  - H1 operating cash flow was $48.9m vs $217.8m a year earlier, so the card's 0.80 cash check needs a fresh look after Q3.
  - Core outsourcing grew only +1.9% (the AI repricing risk).
  - **Q3 results come out 5 Nov after the US close.**
  - A vote on moving from Bermuda to Delaware is on 10 Nov (tax effect unknown).
- JUDGMENT: keep. Buy on 5 Nov before the release, or wait until 6 Nov and read it first.

**Euronet (EEFT), Clean, max $9,185**
- The report's RED item is the 27 Oct guidance cut, which is **already in our year 1**.
- Remaining risks:
  - When Chase takes over Apple Card (about late 2027), CoreCard loses about half its revenue.
  - Cross-border operating income fell 37%, and Wise is cutting prices.
  - Fee rules: Greece's ATM fee cap and the EU's PSD3 package.
  - ATM cash facilities have deadlines on 15 and 30 Nov.
  - Convertible dilution is MISSING.
  - The shares are +4.9% since 30 Oct.
- Model: no change. Value is 3.3×.
- JUDGMENT: keep.

**Deckers (DECK), Clean, max $8,471**
- RED: the 22 Oct sales cut (already in year 1). HOKA growth slowed to 6.8%, and US direct comparable sales fell 6.4%.
- Also:
  - Earnings guidance is lifted by tariff refunds ($0.52 per share).
  - Six-month operating cash flow was negative (seasonal, before UGG's peak quarter).
  - Deckers lost a trade-dress case on two UGG styles.
  - Vietnam/Indonesia tariffs are 12.5%/10%.
- Model: no change. FY0 (to March 2026) is before the refunds, so the margin is not inflated.
- JUDGMENT: keep.

**Wolters Kluwer (WKL.AS), Clean, max $14,924**
- No RED in the report.
- Model fix: the €232m gain (above) lowers value to 1.23× and the bear case to 0.84×. It **still passes**.
- Risks:
  - Clinical AI: OpenEvidence is free for clinicians, and the University of Arkansas medical school (UAMS) let its UpToDate subscription lapse.
  - Legal and tax AI from RELX and Thomson Reuters.
- The nine-month update came out 4 Nov (check it).
- JUDGMENT: keep, maybe a little smaller.

**Cognizant (CTSH), Mild, max $12,824**
- Main red flags (RED):
  - The US Labor Department's inspector general has a criminal investigation, and green-card labour certifications (PERM) are suspended.
  - A lower growth ceiling (4.0–4.4% constant currency).
- Also:
  - Collection days rose to 89.
  - Operating cash flow is down.
  - India tax: ₹33bn claimed, with a $360m deposit.
  - The *Palmer* trial is on 8 Dec.
  - H-1B fee and offshore-tax bills.
- Model: check the year-1 range (small effect).
- JUDGMENT: keep. It shares its risks with Genpact (see the portfolio section).

**Amdocs (DOX), Mild, max $8,440**
- RED: the 3 Nov guidance collapse and the T-Mobile dispute (see section 1).
- FY2027 free cash flow guidance is $440–500m vs $729m.
- JUDGMENT: drop, or hold off. This is the one card where the facts changed after the price date.

**Open Text (OTEX), Mild, max $16,719**
- No RED.
- Risks:
  - FY27 free cash flow guidance is $625–725m vs $807.5m.
  - Support revenue fell 4.8% at constant currency.
  - Debt is $5.8bn. The new notes mature in 2031 and Oct 2033 (the start of the window).
  - Canada tax dispute: up to a $470m deferred-tax write-down.
- **Q1 results come out 5 Nov before the US market opens.**
- JUDGMENT: keep, but only buy after reading the 5 Nov results.

**PayPal (PYPL), Mild, max $9,641**
- Main red flags (RED):
  - Branded checkout grew only 1% (its fourth quarter at 1–2%), and PayPal product transaction revenue fell about $240m.
  - Regulators: an FTC demand (Sept), the UK FCA wallet investigation and a German case.
- Also:
  - Foreign subsidiaries hold $7.1bn of the cash (the zero-cash variant, 1.62×, is already computed).
  - Merchant charge-offs rose to 8.3%.
- JUDGMENT: keep at the mild tier.

### Alternates (strong caveats or screened)

| Company | Main red flags (from the reports) | JUDGMENT |
|---|---|---|
| Lululemon (LULU) | Securities class action filed 2 Nov. US revenue -8%; Q3 guided -10% to -11%. The Q2 margin includes a 5.6-point tariff refund. Two executives leave 6 Nov. | Low-priority alternate |
| adidas (ADS.DE) | The card's cash check comes from FY25 (CFO €751m); nine-month 2026 CFO recovered to €1,971m. The profit upgrade includes a €200m tariff refund. Nike takes over the German national-team kit 2027-34. | Better than its card, still an alternate |
| Zimmer Biomet (ZBH) | False Claims Act (sales commissions) case partly survived summary judgment on 21 Oct. Knees +0.1%. Price cuts. CMS bundled payments from 2028. **Q3 came out 4 Nov.** | Alternate; read Q3 first |
| Reckitt (RKT.L) | Guidance cut 27 Oct (consensus in the model is already post-cut). Cash check 1.72 (0.57× on reported cash flow). 847 infant-formula (NEC) cases. | Alternate |
| NRG | Cash conversion (0.99× with D&A = capex). Results 9 Nov (after the freeze). Gas-collateral swings ($1.4bn per $0.50). | Alternate |
| Nvidia (NVDA) | **$105bn guarantee on an OpenAI-linked data centre** (contingent, running into 2033-42). Collection days 45 → 60. Supply commitments $279bn. China rules. Taiwan. Already 8.39% of VOO. | Skip (VOO overlap) |
| MediaTek (2454.TW) | No RED. AI-chip (ASIC) ramp behind consensus +77%/+69%. Q3 operating cash flow negative; inventory +56% q/q. $3.9bn convertible. Phone share 34% → 28%. Price -6% since 30 Oct. | Alternate |
| Samsung (005930.KS) | Memory cycle. **US ITC Maxell decision due 5 Nov** (possible import ban on covered phones). China (Xi'an) export licences. | Alternate |
| Tencent (0700.HK) | Lending is small next to its cash flow (fintech receivables RMB 23bn vs CFO RMB 303bn), which supports overriding the bank-like flag. But AI capex rose 176% and reported free cash flow was -RMB 13.8bn in Q2, so a flat FY2025 capex ratio is too low (the Meta problem). US 1260H list. | Skip unless re-run with higher capex |
| PDD | **EU €2 handling fee from 1 Nov**; Temu's EU spending share fell 7% → 4.5%. US de minimis exemption gone. €200m EU fine. Audit committee down to two members (its charter requires three). | Skip |

## 3. Portfolio check

The list assumed is the 11 core names at their maximum positions: $136,651 vs the $119,481 sleeve. Pat sets the final sizes. Without Amdocs the total is $128,211, still $8,730 over.

**Shared exposures (FACT from the cards and reports; dollar sums at maximum positions):**

- **Countries:**
  - India delivery: Cognizant, Genpact, Amdocs ($34,300).
  - China: Trip.com, plus Tencent/PDD if added.
  - Israel: Amdocs R&D (under 15% of staff).
  - Taiwan supply: alternates only (Nvidia, MediaTek).
- **Currencies:**
  - EUR: Sanofi and Wolters Kluwer ($36,441).
  - RMB: Trip.com.
  - INR costs: the IT services names.
  - The rest is USD.
- **Industries:**
  - IT services: 3 names ($34,300).
  - Software: 2 ($28,355).
  - Payments: 2 ($18,826).
  - One each in pharma, data, consumer and internet.
- **Common drivers:**
  - **AI substitution or repricing** is the main long-term risk for Adobe, Cognizant, Genpact, Amdocs, Open Text and Wolters Kluwer: **6 of 11 names, $77,579 (57%)**. PayPal also faces AI shopping agents.
  - US tariffs: Deckers, plus Lululemon and adidas if added.
  - Rates: every name, through the discount rate.

**Overlap with the ETFs.**
- FACT: Nvidia is 8.39% of VOO (Vanguard, 30 Sep). That is about $3,000 of the $35,844 VOO position.
- JUDGMENT, to verify in the fund holdings files:
  - Adobe, PayPal, Cognizant and Deckers are S&P 500 members, so they are small VOO holdings (weights MISSING).
  - Adobe and Cognizant are likely in XLK, and PayPal in XLF.
  - Sanofi and Wolters Kluwer are likely in VXUS.
  - Genpact, Euronet, Amdocs and Open Text are not in VOO.
- Overlap is small except Nvidia, which supports skipping it.

**Events between now and the 6 Nov freeze that hit several names:**

| Date | Event | Names affected |
|---|---|---|
| 4 Nov | Zimmer, Smith+Nephew, Wolters Kluwer nine-month update; Figma, Expedia, Qualcomm, Western Union and Remitly after the close; Amdocs' first session after its guidance | ZBH, WKL, ADBE, TCOM, MediaTek, EEFT, DOX |
| 5 Nov | **Open Text Q1 (before the open)**, **Genpact Q3 (after the close)**, Bank of England decision, Canadian budget, US ITC Maxell target | OTEX, G, RKT (GBP), Samsung |
| 6 Nov | US jobs report (8:30 ET), Vistra results, Lululemon executive departures | All (rates), NRG, LULU |
| Just after the freeze (cannot trade) | NRG 9 Nov; China Section 301 exclusions end 9-10 Nov; Genpact Delaware vote 10 Nov; Euronet ATM facility deadlines 15/30 Nov; Nvidia 17 Nov; Tencent 18 Nov | Monitor only |

Rates common to all reports (FACT):
- US 10-year 4.94% (30 Oct) → 4.95% (3 Nov).
- The 3-month bill was **3.99%** on 30 Oct. The pack's 4.00% is the 29 Oct value; the difference is negligible, since the DCF uses the 10-year.
- Brent $103.60 (3 Nov). The Fed held at 3.75–4.00%; the ECB at 2.50%.
- Midterms: Democrats won the Senate (AP call); the House is projected Democratic by other outlets; nothing is certified.

**Portfolio-level flags (JUDGMENT, ranked):**

1. **RED: AI risk is concentrated.** 57% of the stock dollars sit in names whose main long-term risk is AI replacing or repricing their product. Over 2033-2042 this acts as one shared risk factor, not six independent ones. Ways to reduce it:
   - fewer of these names;
   - smaller sizes;
   - say so plainly in the report as an accepted risk.
2. **RED: IT services and India cluster.** Cognizant, Genpact and Amdocs share several risks:
   - the US visa fee and the proposed 25% offshore-service tax (HIRE Act);
   - India tax disputes;
   - the rupee;
   - AI repricing.

   Dropping Amdocs leaves two.
3. **AMBER: news inside the trade window.** Amdocs showed that a single guidance update can halve a price. Open Text and Genpact report while orders are being placed, and most consensus vintages are MISSING.
4. **AMBER: cash conversion.** 5 of 11 core names have model cash above reported cash by more than 10%: Cognizant 1.13, Amdocs 1.19, Open Text 1.26, PayPal 1.16, and Trip.com about 1.14 (corrected).
5. **AMBER: China regulation.** Trip.com's SAMR remedies are permanent. Adding Tencent or PDD would add US–China rule risk (1260H, the proposed COINS rules, Section 301).

## 4. Decisions for Pat

1. Amdocs: drop it, or hold off until the 4 Nov close and updated consensus.
2. Apply the Wolters Kluwer gain fix and the Trip.com cash fix to the official outputs (they are TEST until then). The €232m figure needs a check in the annual report.
3. Open Text and Genpact: trade after their results, or before.
4. Final sizes to fit $119,481, and whether to trim the AI-exposed names.
5. Tencent and PDD: keep both out (recommended).
