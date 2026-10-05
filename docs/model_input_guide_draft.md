# Structure model: input guide (DRAFT)

Notes for the doc the user will ask for with "create doc". It covers the
structure model, `context/Laura_Gao_Portfolio_Structure_Model_v4.xlsx` (Option 3 only).
This is the portfolio structure model, not M04, which is the later
portfolio-fit model. Add each tab's notes as we go through it.

## Inputs tab: what each input means

**Stock average annual return (B16, 6.95%; ASSUMPTION, M02 A-06).**
- It's the average yearly return the stock part is assumed to earn.
- It is the arithmetic version of a 5.5% compound return. Volatility drag
  makes the simple average higher than the compound return, so never
  compound 6.95%.
- Changing it changes the stress scenarios and the simulation (Step 5):
  the paths, payment success and facility capacity.
- It does **not** change the floor, the cushion or the trade sizes.
- Present results at 3.9%, 5.5% and 6.7% compound, not at one value only.

**Stock annual volatility (B17, 17.8%; RESEARCH, M02 A-05).**
- How much yearly returns swing around the average: the standard deviation
  of S&P 500 annual returns, 1998-2025.
- A typical year lands between about -11% and +25%; about one year in
  three falls outside even that.
- Higher volatility means a wider spread of simulated outcomes.
- It applies to a US core fund. Once holdings are chosen, M04 calculates
  the whole portfolio's volatility, using how the holdings move together.
  A weighted average of each holding's volatility would overstate the risk.

**Log-return mean (B18, 5.35%) and log-return volatility (B19, 16.53%).**
These are formulas, so don't edit them. The simulation builds each year's
return as `e^(mu + s x z) - 1`, where z is a stored bell-curve random
number. That form means a return can never fall below -100%, and gains and
losses compound properly.

    s^2 = ln(1 + volatility^2 / (1 + average)^2)
    mu  = ln(1 + average) - s^2 / 2

Check: `e^mu - 1` = 5.5%, the compound return. So mu and s are the same two
assumptions (B16, B17), just translated into log form.

**Multiplier m (B24, 2; your choice, M08).** Option 3's rule, recalculated
every year: **stocks = m x cushion**, and the rest goes into bonds.
- m = 1 means: lock in the floor in bonds and hold the cushion in stocks.
- At 2028 values: m = 2 means 63.4% stocks; m = 3 means 95%.
- After gains the cushion grows, so you buy more stocks. After losses it
  shrinks, so money moves to bonds automatically.
- **Gap risk:** the floor breaks if stocks fall more than
  `(1 + bond yield)/m - bond yield` in one year. At a 5% yield:
  - m = 2: -47.5% (survives 1931's -43.8%);
  - m = 3: -30% (breaks in 2008's -37% and 1937's -35%).
- A higher m means more growth and a bigger facility in good markets, but a
  smaller crash breaks the floor.

**Maximum stock share (B25, 100%; your choice).** A ceiling on Option 3's
stock share after long rallies.

**Crash sizes (B28 -37%, B29 -43.84%; RESEARCH, M02 A-08 and A-09).**
- They are **alternative sizes for one crash**, used in separate preset
  stress scenarios ("Crash in 2032", "Severe crash in 2032"). They never
  both happen in the same scenario.
  - -37% is 2008.
  - -43.84% is 1931, the worst calendar year since 1928.
- The 1,000-path simulation does not use them: crashes appear randomly from
  the volatility.
- Known weakness: the bell-curve simulation produces a year worse than -30%
  about 0.7% of the time, against about 3% historically (1931, 1937 and
  2008 out of 98 years). The planned M07 block bootstrap fixes this.

**Facility amount to test (B31, $100,000; your choice).**
- It's the target the simulation measures against. Step5_Summary reports
  the share of simulated paths where the 2033 facility capacity is at least
  this much.
- Changing it changes only that reported percentage, not the portfolio or
  the trades.
- It's the number behind the 2031 pitch: "in X% of futures Laura can give
  at least $Y."

**Simulated paths (B34, 1,000) and random seed (B35, 20260926).**
- A path is one possible future: six stock returns, 2027-2032. Every path
  uses the same average and volatility but different random numbers.
- All three options run through every path, and the results are counted.
  The output is a range of outcomes, not a prediction. 1,000 paths make the
  percentages reliable to about +/-1.5 points.
- The seed is the starting number for the random generator, so the same
  seed gives the same numbers.
- The draws are stored as plain values (Step5_Simulation, columns B-G), so
  editing the workbook doesn't reshuffle them. When you change an input,
  the same futures are reused, so any change in results comes from your
  input, not from luck.

**Stage 1: lowest m still being considered (B22, 1; your choice, new in v4).**
- Stage 1 trades only what every m from this value up to the chosen m (B24)
  agrees on. That means the bonds the chosen m needs, and the stocks the
  lowest m holds. The rest waits in T-bills.
- At B22 = 1 and B24 = 2: 36.6% bonds, 31.7% stocks, 31.7% parked.
- Set B22 equal to B24 to trade the full target in one stage.

**Removed in v4:** the reserve purchase yield in 2033 (old B14) and the
glide-path settings (old B22-B23, row 41). They were used only by Option 2.

## Step4_Sizing tab: notes

**Purpose.** It works backwards from Laura's ten payments to answer three
questions, using only the payments, the bond yield and the safety margin.
Stock returns play no part.

1. How much must be in the reserve on the first day of 2033?
2. What does it cost to lock that in now (the floor)?
3. What is left over to invest (the cushion)?

Under Option 3, the floor is a target that rebalancing protects, not an
amount held entirely in bonds.

**Key results (rows 5-16).**
- B7/B8, reserve at the start of 2033: **$405,391** at 5%. It's less than
  10 x $50,000 because each payment's money earns 5% in a bond until its
  date. The $94,609 difference is the ladder's interest. Payment 1 is paid
  immediately, so it isn't discounted (Excel `PV`, type = 1).
- B9/B10, the floor (cost to lock in all payments): $302,509 at the start
  of 2027, **$317,635** at the start of 2028.
- B11: the 2027 money alone is about $2.5k short, so the 2028 money tops it up.
- B12/B13, the cushion: $140,348 in 2027 and **$147,365** in 2028. That's
  the money not needed for the payments.
- B14-B16 (Option 3, added in v3):
  - stocks in 2028 = m x cushion = **$294,731**;
  - stock share **63.4%** (it matches WInS_Plan D14);
  - one-year stock fall that breaks the floor: **-47.5%**.

**Discount table (rows 19-31).** Each payment x 1/1.05^t gives its value at
the start of 2033. Later payments need less today. The total equals B7
(Checks #1).

**Chart.** "Cushion in 2028 by bond yield" is column H drawn as a line.
Below about a 1% yield the cushion is negative, so the payments can't be
locked in. Each +1% of yield frees about $30k.

**Sensitivity table (rows 34-50).** The same results at bond yields from
0% to 7%:

| Column | Meaning |
|---|---|
| B, C | Reserve in 2033, without and with the safety margin |
| D, E | Floor at the start of 2027 / 2028 |
| F | Is the 2027 money alone enough? |
| G, H | Cushion at the start of 2027 / 2028 |
| I | Cushion as a % of the 2028 portfolio |
| J, K | Option 3 stocks in 2028 ($ and %) |
| L | One-year stock fall that breaks the floor |

At 4%: cushion $115k, Option 3 stocks 49.9%. At 6%: $177k, 75.4%.

**Changes made in v3 (5 Oct 2026).**
- Removed the "required return if nothing is locked in" block (old rows
  14-17 and columns J-Q). It described a no-lock-in plan, not Option 3, and
  priced the reserve at the lock-in yield instead of the 2033 yield.
- Replaced it with Option 3 results (B14-B16, J-L).
- Relabeled the "Option 1" columns and the chart as "cushion".
- Corrected the floor-break rule in the README, Inputs I24 and Inputs I29,
  from "more than 1/m" (50% at m = 2) to `(1 + yield)/m - yield`
  (47.5% at m = 2 with a 5% yield).

**Open caveats.**
- One flat 5% yield is used for every maturity. Real 5-year yields are
  5.03% and 10-year yields 5.18%, so the flat rate is mildly cautious.
- The actual iBonds fund yields (4.4% in July) need refreshing in WInS.
- The safety margin is 0% until "high certainty" is defined (M08).

## Step5_Scenarios tab: notes (v4, Option 3 only)

**Purpose.** It runs Option 3 through 16 preset market paths, 2027-2032, and
shows where it ends at the start of 2033. Each row is one path.
- Rows 1-8 use the Inputs crash sizes.
- Rows 9-16 are P2's M02 stress paths: credit crash, 2022-style rate
  spike, AI capex pause (2000-02 replay), early crash, lost decade
  (2000-05), strong growth (2019-24), oil collapse, stagflation (1973-74).

**Layout.**

| Columns | What they show |
|---|---|
| C-H | Stock return each year. Normal years use the compound 5.5%, not the arithmetic 6.95% |
| I-O | Wealth at the start of each year, 2027-2033 |
| P-U | Stock share at the start of each year |
| V | Reserve fully funded? |
| W | Facility capacity: wealth in 2033 minus the reserve |
| X | Reserve gap |
| Y | Did wealth fall below the floor in any year, 2028-2033? |
| Z | Type and source of the path |

**How a row is calculated.** Each year:
1. floor = the cost of bonds that cover all ten payments;
2. cushion = wealth - floor (never below zero);
3. stocks = m x cushion (capped);
4. bonds = everything else;
5. next year's wealth = stocks x (1 + stock return) + bonds x (1 + bond
   yield) + any contribution.

**Results in v4** (M02 base inputs, m = 2). Facility capacity in 2033;
the reserve is funded in every row and the floor never breaks:

| Path | Facility |
|---|---|
| Steady 5.5% (compound base) | $197k |
| Crash in 2027 | $197k (no stocks in 2027) |
| Crash in 2030 / 2032 (-37%) | $39k |
| Severe crash 2032 (-43.8%) | $14k |
| Zero stock returns | $114k |
| Stocks earn the bond yield (check) | $188k |
| Custom path | $76k |
| M02 S2, 2022-style rate spike 2031 | $109k |
| M02 S3, AI capex pause 2030-32 | $46k |
| M02 S5, lost decade start | $99k |
| M02 S6, strong growth (2019-24) | $372k |
| M02 S7, oil collapse 2032 (-10%) | $140k |
| M02 S8, stagflation 2031-32 | $50k |

**How Option 3 works in one line.** While the cap isn't hit, the cushion is
multiplied each year by `1 + yield + m x (stock return - yield)`.
- A normal year at 5.5%, m = 2: **x1.06**.
- A -37% year: **x0.21**.
- At -47.5% the factor is 0 and the floor breaks.
- The order of years after 2028 doesn't change the result.
- In 2027 the money alone is below the floor, so Option 3 holds no stocks.

**What it means.** Option 3 protects all ten payments in every path tested,
including 1931's -43.8%. The facility is what absorbs the risk: $197k in a
steady market, $39-50k after a 2008-style crash or stagflation, $14k after
a 1931-size crash.

**Fixed in v4 (5 Oct 2026).**
- Fixed-return paths compounded the arithmetic 6.95%. They now use the
  compound 5.5%. Steady-path facility: $226k becomes $197k.
- Options 1 and 2 removed.
- M02 paths S1-S8 added. Their normal years are linked to the Inputs
  stock return; their crash and replay years are fixed history. S5 and S6
  are full historical replays, so they don't move with B16. The zero-return,
  bond-yield check and custom rows are also fixed by design.
- Checks rewritten for Option 3 (20/20 pass). They include an independent
  closed-form check of the rule (Checks 10 and 11).

**Open caveats.**
- **Thin equity premium in the M02 base:** stocks 5.5% vs bonds 5.0%. The
  case for m = 2 rests on stocks beating the base case.
- **2027 is all bonds in the model, but WInS uses the 2028 target**
  (WInS_Plan B6). State this in the Trading Notes.
- **Bonds are valued at their locked yield.** Rebalancing would really sell
  them at market prices, which move with interest rates.

## Step5_YearByYear, Step5_Simulation, Step5_Summary: notes (v4)

- **YearByYear:** the Inputs B30 scenario, year by year (return, floor,
  wealth, cushion, stocks, bonds, stock share), with a wealth-vs-floor chart.
- **Simulation:** the same rule on 1,000 random paths (stored draws,
  seed 20260926).
- **Summary (M02 base, m = 2):**
  - reserve funded in 100% of paths;
  - facility of at least $100k in 72.8% of paths;
  - facility percentiles: 5th $42k, median $176k, 95th $581k; average $224k.
  - Independently recomputed in Python: identical.
  - The lognormal model produces crash years less often than history, so
    the bad-case numbers are optimistic.
