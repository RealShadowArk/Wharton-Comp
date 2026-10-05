# How the assumptions and model figures are derived

> **Update, 5 Oct 2026 (structure model v4, Option 3 only).** Sections 1-2
> still hold. Section 3's Stage 1 used the smallest shares across Options
> 1-3. In v4, Stage 1 uses the lowest m still being considered (Inputs B22,
> default 1). It is now 36.6% bonds / 31.7% stocks / 31.7% T-bills: the
> 32% bond share came from Option 2, which no longer exists. Stage 2 is
> unchanged: 36.6% bonds / 57.4% core / 6% tilts.

As of 29 Sep 2026. Inputs: `inputs/M02_assumptions.csv` (M02 v1.0-DRAFT,
28 Sep 2026) and `context/Laura_Gao_Portfolio_Structure_Model_v1.xlsx`.
Every number below can be reproduced with `m02/assumptions.py` and
`structure/plan.py`; `tests/test_m02_structure.py` checks them against both
workbooks.

## 1. Case facts (CASE, SRC-17 Gao case study pp. 2-4)

| ID | Fact | Value |
|---|---|---|
| C-01 | Contribution, start of 2027 | $300,000 |
| C-02 | Contribution, start of 2028 | $150,000 |
| C-03 | Payment, start of each year 2033-2042, fixed and nominal | $50,000 × 10 |

## 2. Market assumptions (M02)

Low / base / high. All are nominal and net of fund fees, so no model
subtracts fees again. Worse end = the end that is bad for Laura.

| ID | Input | Low | Base | High | Worse | How the base was chosen | Sources |
|---|---|---|---|---|---|---|---|
| A-01 | Bond yield locked in by 2027-28 ladder purchases | 4.0% | 5.0% | 5.5% | Low | 5- to 10-year Treasuries were 5.03-5.18% on 24 Sep 2026, minus about 0.07% iBonds fee, rounded down. Low = CBO pre-shock 2026 baseline (4.1%). | SRC-01 H.15, SRC-06 CBO, SRC-15 iShares |
| A-02 | Yield available in 2033 (Option 2 buys its reserve then) | 3.25% | 4.4% | 5.5% | Low | CBO baseline 10-year yield for 2031 onward. Low = Fed longer-run rate 3.2% (no term premium). | SRC-02 FOMC SEP, SRC-06, SRC-01 |
| A-03 | T-bill parking return, 2026-28 | 3.25% | 4.0% | 4.5% | Low | 3-month bill 4.24% today; FOMC median 4.1% for end-2027; less fees. Not yet a model input. | SRC-01, SRC-02 |
| A-04 | Stocks, **compound** annual return 2027-32 | 3.9% | 5.5% | 6.7% | Low | Average of three published forecasts: J.P. Morgan 6.7%, Vanguard midpoint 4.9%, Invesco 5.0%. Low = Vanguard low end; high = J.P. Morgan. | SRC-12, 13, 14 |
| A-05 | Stock volatility (annual SD) | 13% | 17.8% | 19.4% | High | SD of S&P 500 annual returns 1998-2025. High = 1928-2025. Low = the calm last 12 months (12.8%, rounded up). | SRC-08, 10, 11 |
| A-06 | Stocks, **arithmetic** annual return (model input) | 5.64% | 6.95% | 7.48% | Low | Converted from A-04 and A-05; see below. | calc |
| A-07 | Stock-bond correlation | -0.6 | 0 | +0.5 | High | About 0 over 1928-2018. Used only by M07 later. | SRC-10, 11 |
| A-08 | Crash size, one year | -43.8% | -37.0% | -18.1% | Low | 2008 = -37.0%; 1931 = -43.8%; 2022 = -18.1%. | SRC-10, 11 |
| A-09 | Severe crash (reverse stress) | -43.8% | -43.8% | -43.8% | | 1931, the worst calendar year since 1928. | SRC-10 |
| A-10 to A-12 | Fund fees: core, iBonds, SGOV | 0.03% (RSP 0.20%), 0.07%, 0.09% | | | | Already deducted in A-04, A-01 and A-03. If RSP is chosen, cut A-04 by about 0.17 points. | |

**Why A-06 differs from A-04.** A compound (geometric) return is lower
than the average (arithmetic) return because of volatility drag. The
simulation draws yearly returns, so it needs the arithmetic average. For a
lognormal return:

    arithmetic = (1+g) × sqrt((1 + sqrt(1 + 4v²/(1+g)²)) / 2) − 1
    base: g = 5.5%, v = 17.8%  →  6.95%

The low case pairs the low return with the **high** volatility, and the
high case the reverse, so "pessimistic" is bad on both at once:
3.9% and 19.4% give 5.64%.

The model then turns the arithmetic mean and volatility into lognormal
parameters (Inputs!B18:B19):

    s = sqrt(ln(1 + v²/(1+A)²)),   μ = ln(1+A) − s²/2

Nine scenario paths (S0-S8) replay actual S&P 500 years; see
Scenario_Definitions in the M02 workbook. For example, S1 applies 2008's
-37% in 2032 with a 3.25% yield in 2033. S7's -10% core return is
hypothetical and flagged as such.

## 3. From assumptions to the Stage 1 / Stage 2 percentages

The steps below use the v1 settings: bond yield 5%, margin 0%, m = 2,
stock cap 100%, glide path 80%→20%, tilts 6%.

1. **Reserve needed at the start of 2033.** This is the present value of
   ten $50,000 payments, the first one immediate:

       Σ_{k=0..9} 50,000 / 1.05^k = $405,391   (× (1 + safety margin))

2. **Floor in 2028.** The amount that grows into that reserve at the bond
   yield: 405,391 / 1.05^5 = **$317,635**.
3. **Portfolio at the start of 2028.** This assumes a neutral 2027, where
   everything earns the bond yield: 300,000 × 1.05 + 150,000 = **$465,000**.
4. **Cushion** = 465,000 − 317,635 = **$147,365**. This is the money not
   needed to lock in the payments.
5. **Growth share under each option:**
   - Option 1 (lock in early): stocks = cushion, so 147,365 / 465,000 = **31.7%**.
   - Option 2 (glide path): straight line from 80% in 2027 to 20% in 2032,
     which gives **68.0%** in 2028.
   - Option 3 (floor rule): stocks = min(m × cushion, cap × portfolio),
     so 2 × 147,365 / 465,000 = **63.4%**.
6. **Stage 1 (no-regret).** Each part is the smallest share that all three
   options agree on:
   - Safety = the smallest safety share = 1 − 68.0% = **32.0%** (set by Option 2).
   - Growth core = the smallest growth share = **31.7%** (set by Option 1).
   - Parked in T-bills = the rest = **36.3%**.

   On $300,000 this gives $96,000, $95,075 and $108,925.
7. **Stage 2 (Option 3).** Safety **36.6%**; growth 63.4%, of which the
   tilts are 6% (XLV and XLP at 3% each) and the core is **57.4%**.
8. **Tilt limit** (Tilt_Sizing). Maximum tilt = the loss you accept from
   one tilt ÷ that sector's worst year. For example, XLV: 1% ÷ 23.3% = 4.3%
   maximum, so 3% passes. The 1% loss budget and the 10% total tilt cap are
   PLACEHOLDERS for P1 to decide.

## 4. What the M02 cases change

Stage 1 and Stage 2 shares depend only on the **bond yield**, the **safety
margin**, and the option settings (m, cap, glide path). The stock return and
volatility do not change them; those only feed the scenarios and the
simulation. So the M02 base case (5% yield) leaves the WInS plan exactly as
it is in v1.

| Case | Yield | Margin | Floor 2028 | Option 1 | Option 3 | Stage 1 safety / growth / parked | Stage 2 safety / core |
|---|---|---|---|---|---|---|---|
| Base | 5.0% | 0% | $317,635 | 31.7% | 63.4% | 32.0 / 31.7 / 36.3 | 36.6 / 57.4 |
| Pessimistic | 4.0% | 0% | $346,661 | 25.0% | 49.9% | 32.0 / 25.0 / 43.0 | 50.1 / 43.9 |
| Optimistic | 5.5% | 0% | $304,225 | 34.8% | 69.6% | 30.4 / 34.8 / 34.8 | 30.4 / 63.6 |
| Base + 5% margin | 5.0% | 5% | $333,516 | 28.3% | 56.6% | 32.0 / 28.3 / 39.7 | 43.4 / 50.6 |
| Base + 10% margin | 5.0% | 10% | $349,398 | 24.9% | 49.7% | 32.0 / 24.9 / 43.1 | 50.3 / 43.7 |

**Finding for decision (P1/M08).** The Stage 1 growth buy of 31.7% is
"no-regret" across the three *options*, but not across the M02 *yield range*
or a positive safety margin. At a 4% yield, or with a 10% margin, Option 1
would hold only about 25% in stocks. Buying 25% now would stay no-regret
under all of these cases. Buying 31.7% bets that yields stay near 5% and
the margin stays near 0%. Which to use is a team choice, not an M02 fact.

## 5. Open items that affect these figures

- **Safety margin is 0%.** "High certainty" is still undefined (M08).
- **Nothing funds the Jan 2033 payment.** IBTM (the Dec 2032 iBonds fund) is
  unverified. 2037-2042 have no ladder funds yet.
- **iBonds yields (4.42-4.48%) are from July,** before the September rate
  rise. Refresh them.
- **The CBO yield path (A-02) comes from a secondary summary.** The Invesco
  forecast date (SRC-14) is also unverified.
- **Instrument prices are stale,** and VOO, VTI and RSP have no price.
