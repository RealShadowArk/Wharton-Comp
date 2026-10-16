# Stock selection rulebook (living document)

Version 1, 15 Oct 2026. This is updated whenever a rule changes.

**Two kinds of rule:**
- **GUIDE**: fixed by the competition rules or the P3 M12 build guide.
- **JUDGMENT**: a student choice. It needs Pat's sign-off and must be
  defended in the IPS.

**Pending** = proposed, not yet approved.

## Step 0: What can be bought at all

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| 0.1 | Only stocks priced at **$5 or more** on a WInS exchange, ETFs on WInS, and Treasury bonds | $5 | GUIDE (Week 1 email) | Competition rule; applies to both contributions and the long-term plan |
| 0.2 | Individual stocks are **US-listed operating companies** filing a US 10-K | US filers | JUDGMENT | Their accounts are comparable (US GAAP), so the M12 ranking is fair. Foreign stocks would need their own research outside M12. |
| 0.3 | No banks, insurers or REITs in M12 peer groups | n/a | GUIDE (M12 guide, step 2) | Their accounts make these ratios meaningless. Payment processors are allowed because they earn fees, not loan income. |

## Step 1: Where to look (industries)

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| 1.1 | Industries come from the sector research's "next research question" lines, then the growth focus | Payments, pharma, electrical equipment, analog chips, medical devices (household: diagnostics only) | JUDGMENT | Each industry answers a stated research question; chosen before any scores were seen |
| 1.2 | Peers are defined by **business model**, using GICS as a starting point | e.g., keep HUBB and PG despite the GICS conflict (R7) | GUIDE (M11) + JUDGMENT | Ranking only makes sense among companies that make money the same way |
| 1.3 | **Freeze** the peer list before looking at returns; never swap losers for winners | n/a | GUIDE | Prevents cherry-picking |

## Step 2: Data rules

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| 2.1 | Use the latest annual 10-K (FY0), the prior year (FY1) and three years back (FY3) | Annual filings | GUIDE | Audited, public, comparable |
| 2.2 | **One price date** for every company | Close on **9 Oct 2026** (R6) | GUIDE + JUDGMENT (the date) | Valuation measures must compare companies on the same day |
| 2.3 | Market cap = price × common shares outstanding, with other share classes converted | Cover-page shares (R5) | GUIDE | Visa and Mastercard have several share classes |
| 2.4 | Never estimate. Not reported = **MISSING**; formula doesn't apply = **UNSUITABLE** | n/a | GUIDE | A guess is worse than a blank |
| 2.5 | Every number has a source link | n/a | GUIDE | So it can be audited |

## Step 3: The M12 score (ranking inside each peer group)

**The eight measures**, each weighted 12.5% (4 pillars at 25%). GUIDE.

| Measure | Formula | Better | Why it's there |
|---|---|---|---|
| Q1 Operating margin | operating income ÷ revenue | Higher | Pricing power and efficiency |
| Q2 Asset turnover | revenue ÷ average assets | Higher | How hard the assets work |
| B1 Debt ÷ assets | interest-bearing debt (including finance leases) ÷ assets | **Lower** | Ability to survive a downturn |
| B2 Current ratio | current assets ÷ current liabilities | Higher | Short-term cash safety |
| G1 Revenue growth | 3-year CAGR | Higher | Is the business growing? |
| G2 EPS growth | 3-year CAGR, only if both years' EPS are positive | Higher | Is profit per share growing? |
| V1 Earnings yield | earnings ÷ market cap | Higher | How much profit you get per dollar paid |
| V2 Free-cash-flow yield | (operating cash flow − capex) ÷ market cap | Higher | How much cash you get per dollar paid |

**Scoring:**

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| 3.1 | Score = 100 × (average rank − 1) ÷ (n − 1), ranked within the peer group | 0 = worst, 100 = best | GUIDE | Compares like with like; not affected by extreme values |
| 3.2 | Rank **only complete companies**; one missing measure = no score | n/a | GUIDE | No filling gaps |
| 3.3 | A group is scored only if it has at least **5 complete companies** and at least **80%** coverage | 5 and 80% | GUIDE (proposed safeguards in the guide) | Small groups give unstable ranks |
| 3.4 | Shortlist = top **2** per group, keeping ties | 2 | GUIDE | Equal research effort per industry |
| R1 | No operating income line → build it from the income statement, or use **pre-tax margin for the whole group** | Whole group | JUDGMENT (pending) | Consistent within the group |
| R2 | Exclude companies with incomparable history (GPN, GEV); KMB growth = UNSUITABLE | n/a | GUIDE ("reject incomparable periods") + JUDGMENT | Growth figures would be artifacts |
| R3 | Use continuing-operations EPS where reported | n/a | JUDGMENT (pending) | Measures the business you'd actually buy |
| R4 | Add capitalized software to capex **in Payments only** | Payments | JUDGMENT (pending) | Large and inconsistently reported there |
| R8 | Finance leases not quantified in the 10-K → use reported borrowings | 12 companies | JUDGMENT (pending) | Relies on the issuer's own disclosure. The "drop B1" test checks it. |

## Step 4: Is the ranking robust?

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| 4.1 | Re-score under 32 weight variations | Each measure ×0.8 and ×1.2; each pillar ×0.8 and ×1.2; drop each measure once | GUIDE | A pick that only wins under one weighting is fragile |
| 4.2 | "Robust" = on the shortlist in at least **24 of 32** variants (75%) | 24/32 | JUDGMENT (pending) | Fragile picks need an explanation in M03, not a quiet change of weights |
| 4.3 | Video cross-check: add ROE (higher better), P/S and P/B (lower better) inside the same 4 pillars | 25% per pillar | JUDGMENT (pending) | From the SNP screen in the videos. Agreement makes a stronger case. |

## Step 5: Red flags (shortlist only, pass/fail)

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| 5.1 | Beneish M-score (signs of earnings manipulation) | Flag if above **−1.78** | Published cut-off (Beneish 1999) | Screens out companies whose accounts may be overstated |
| 5.2 | Piotroski F-score (financial strength, 0–9) | Flag if **3 or lower** | JUDGMENT (pending) | Screens out weakening businesses |
| 5.3 | Missing red-flag data = "not checked", never "pass" | n/a | GUIDE spirit | Same no-guessing rule |

## Step 6: Valuation and thesis (M03)

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| 6.1 | DCF using free cash flow to the firm, discounted at WACC; WACC must exceed g | Sensitivities: discount rate, terminal growth, one operating driver | GUIDE (M03) | Tests whether the price already assumes too much |
| 6.2 | Write a falsifiable thesis and a "what would prove us wrong" signal **before** buying | n/a | GUIDE (M12 step 7) | That signal becomes the sell rule |
| 6.3 | A valuation target is never an annual return or a position size | n/a | GUIDE | Avoids false precision |

## Step 7: Sizing and buying

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| 7.1 | Individual stocks share the stock money left after tilts; 70% of growth money after tilts | $118,431 (39.5%) | JUDGMENT (decided 5 Oct) | Set by the floor rule plus Pat's 70/30 choice |
| 7.2 | Loss limit per position: size × worst calendar year ≤ **2% of the portfolio** | 2% | JUDGMENT (Pat, 15 Oct) | Caps the damage from any one bet repeating its worst year |
| 7.3 | Money not yet invested waits in SGOV/cash | n/a | JUDGMENT | Earns T-bill interest while stocks are researched |
| 7.4 | Whole shares, rounded down; refresh prices before ordering; $25 commission per trade | n/a | WInS mechanics | Execution happens at the live bid/ask |
| 7.5 | A Trading Note written by Pat before each trade (300 characters max) | 300 characters | GUIDE | Competition rule; judged on reasoning |

## ETF selection rules (added 16 Oct 2026)

ETFs are **never** valued with a DCF. They are compared on objective,
holdings, cost, concentration, tracking and trading (GUIDE, M03).

| # | Rule | Parameter | Type | Why |
|---|---|---|---|---|
| E1 | Approved and tradeable in WInS (loads in the trade form) | n/a | GUIDE (competition) | Only approved securities count |
| E2 | Has a clear role: core (market exposure) or tilt (deliberate sector bet) | n/a | JUDGMENT | Every holding must tie back to the strategy |
| E3 | Cheapest researched fund that delivers the exposure | e.g., VOO 0.03% over RSP 0.20%; VXUS 0.05% over ACWI 0.32% | JUDGMENT | Fees compound against Laura's growth |
| E4 | 30-day median bid-ask spread ≤ **0.05%** | 0.05% | JUDGMENT | Cheap to buy and to rebalance every year |
| E5 | 1-year tracking difference within **±0.25 points** of its index | ±0.25 points | JUDGMENT | It must deliver what it claims |
| E6 | Research support: the core decision sheet, or a sector labelled "Research now" (an override must be explained in the Trading Note) | n/a | JUDGMENT | Research-backed decisions |
| E7 | Tilts only: size × worst calendar year ≤ **2%** of the portfolio | 2% | JUDGMENT (Pat, 15 Oct) | Limits the damage from any one sector bet |
| E8 | Concentration (top-10 weight) recorded and intended | n/a | JUDGMENT | Know exactly what bet is being made |
