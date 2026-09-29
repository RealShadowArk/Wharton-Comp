# M05 reserve explanation: outline

Headings and the points each section needs. The prose goes in
`M05_reserve_explanation.md`, written in my own words. Numbers come from
`outputs/M05_reserve_comparison.csv` (version m05-0.1, all TEST rates).

Status to state at the top: PROVISIONAL. No sourced yields yet.

## 1. What the reserve is for

- Ten fixed payments of $50,000, one at the start of each year from 2033
  through 2042 (case p.3).
- They must be paid from the portfolio with a high degree of certainty. No
  co-sponsor or grant money can be counted on.
- The reserve is set aside at the start of 2033, before the first payment
  and before any facility gift.

## 2. How the size is worked out

- Add up what each payment needs today. A payment k years away needs less
  today, because the reserve earns a return while it waits.
- The first payment is made the same day the reserve is formed, so it
  needs the full $50,000.
- Ten payments have only nine years of waiting between them.
- Why the model adds the ten terms one by one: the shortcut annuity formula
  breaks at a 0% yield.

## 3. Worked examples

- At 0%, the reserve is exactly $500,000.
- At a flat 3% (TEST, not sourced), it is $439,305.45.
- A higher yield means a smaller reserve. That is the reserve's tie to
  interest rates.

## 4. When the portfolio is short

- The $450,000 case: $450,000 moves into the reserve and the gap is
  $50,000.
- Payments 1 to 9 are paid. Payment 10 (2042) gets nothing, and the model
  shows a $50,000 shortfall instead of a negative balance.
- While there is a gap, the facility gift is zero.

## 5. Risks and limits

- Reinvestment risk: sized at 3% but earning only 1%, the reserve runs out
  in 2042, $42,648.73 short (scenario TEST_Y3_R1_A593).
- Today's yields are not locked in for 2033.
- A bond fund does not mature on a payment date. A ladder of bonds does,
  but each bond still carries issuer risk.
- Costs are not in the model yet.
- A reserve that is fully set aside is not the same as all ten payments
  being paid. Both need reporting.

## 6. Waiting on teammates

- Sourced yields and return scenarios (M02, P2).
- Reserve instruments and their terms (M04, P3).
- Reserve priority and any top-up rule (M08, P1).
- The accepted cash-flow ledger for the 2033 portfolio value (M01, P1).

## 7. Decisions that belong to people

- What counts as a "high degree of certainty."
- What the reserve holds, and in what order it is spent.
- Whether retained assets can ever top up a short reserve.
