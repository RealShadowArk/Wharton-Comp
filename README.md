# Wharton Reserve Model

Models for the operating reserve (M05) and the facility contribution (M08)
in the client case of the 2026-27 Wharton Global High School Investment
Competition.

## The problem

The client invests $300,000 at the start of 2027 and $150,000 at the start
of 2028. From 2033 through 2042 she makes ten fixed payments of $50,000, one
at the start of each year. At the start of 2033, before the first payment,
part of the portfolio is set aside as an operating reserve to fund all ten.

The M05 model answers three questions:

1. How big does the reserve need to be at a given yield?
2. How does the reserve pay out year by year?
3. If the portfolio can't fund the full reserve, how big is the gap, and
   which payments go unfunded?

## Status

M05 version m05-0.1, **provisional**. The math is done and tested. Every
rate is a TEST value until the sourced assumptions (M02) arrive, and the
reserve holds a single flat-return asset until the instrument terms (M04)
arrive.

| Scenario | Reserve yield | Portfolio in 2033 | Required reserve | Gap | All ten paid? |
|---|---|---|---|---|---|
| TEST_Y0_A450 | 0% | $450,000.00 | $500,000.00 | $50,000.00 | No, 2042 unpaid |
| TEST_Y0_A593 | 0% | $593,470.93 | $500,000.00 | $0.00 | Yes |
| TEST_Y3_A450 | 3% | $450,000.00 | $439,305.45 | $0.00 | Yes |
| TEST_Y3_A593 | 3% | $593,470.93 | $439,305.45 | $0.00 | Yes |
| TEST_Y3_R1_A593 | sized at 3%, earns 1% | $593,470.93 | $439,305.45 | $0.00 | No, 2042 short $42,648.73 |

## M08: the facility contribution

After the reserve is set aside in 2033, the client decides how much of what
is left to give toward the residency facility. In 2031 she has to tell
co-sponsors a credible range for that gift.

M08 has two passes:

1. **Before any simulation:** fix the rule. The gift is a chosen share of
   the leftover, and zero whenever the reserve can't be fully funded. This
   pass writes `M08_policy_specification.json` for the funding simulation
   (M07) to run, plus `M08_policy_check_cases.csv`, a table of simple cases
   for checking the rule by hand.
2. **After M07's results:** for each declared 2031 starting state, find the
   range of modeled gifts, how many gifts actually fall in it, and how often
   the gift is zero. Payment success is reported beside it, never folded
   into it. This pass writes `M08_2031_ranges.csv` and
   `M08_contribution_comparison.csv`.

Status: version m08-0.1. The rule, the range math, and the comparison are
built and tested on a small fake path set. The policy choices in
`inputs/m08_policy_choices.csv` and the 2031 states in
`inputs/m08_states_2031.csv` are still blank, so the specification is a
draft. Pass 2 runs once `inputs/M07_path_summary.csv` arrives.

## Layout

| Path | Contents |
|---|---|
| `inputs/case_facts.csv` | Fixed case numbers, with the case page each comes from |
| `inputs/test_scenarios.csv` | TEST scenarios: flat illustrative rates, not sourced |
| `m05/reserve.py` | Reserve sizing, transfer, gap, run-off, and summaries |
| `m05/inputs.py` | Loads the input files, including teammates' files once they arrive |
| `m05/policy.py` | The draft reserve policy for the funding simulation (M07) |
| `m05/run.py` | Runs every scenario and writes the output files |
| `inputs/m08_policy_choices.csv` | The M08 choices: gift shares to compare, certainty target, range method and coverage, 2031 date, top-ups |
| `inputs/m08_states_2031.csv` | The declared 2031 starting states |
| `m08/gift.py` | The 2033 split between reserve, gift, and retained flexibility |
| `m08/ranges.py` | Gift ranges, coverage, and policy results from M07's paths |
| `m08/spec.py` | The M08 policy specification |
| `m08/run.py` | Writes the M08 files |
| `outputs/` | Generated CSV and JSON files for the rest of the team |
| `handcheck/M05_hand_check.xlsx` | The same math as spreadsheet formulas, for an independent check |
| `tools/make_hand_check.py` | Rebuilds the hand-check workbook |
| `docs/` | Outlines for the reserve explanation, the M08 decision memo, and the sponsor language |
| `tests/` | Acceptance tests |

## Running it

Needs Python 3.10 or newer. No packages to install.

```
python -m unittest -v
python -m m05.run
python -m m08.run
```

`python -m m05.run` rewrites the three M05 files in `outputs/`:

- `M05_reserve_schedule.csv`: every year of every scenario (balance, payment
  due, amount paid, shortfall, return).
- `M05_reserve_comparison.csv`: one row per scenario (required reserve,
  transfer, gap, whether the reserve was established, whether all ten
  payments were paid).
- `M05_reserve_policy.json`: the rules M07 must follow. Choices that belong
  to the team are marked UNDECIDED.

`python -m m08.run` writes the M08 files that its inputs allow and lists
anything it is still waiting for.

Rebuilding the hand-check workbook needs `openpyxl`:
`python tools/make_hand_check.py`.

## Teammates' files

Put each file in `inputs/` under the name below. Until it's there, the
model says who owns it and which fields to send. The field lists are
proposals to confirm with each owner.

| File | From | Used for |
|---|---|---|
| `M01_cashflows.csv` | P1 | The 2033 portfolio value and the payment schedule |
| `M02_assumptions.csv` | P2 | Sourced reserve yields and returns |
| `M04_reserve_instrument_terms.csv` | P3 | Instrument cash flows in place of the flat return |
| `M08_policy_specification.json` | P1 (copy from `outputs/` once final) | Reserve priority and any top-up rule |
| `M07_path_summary.csv` | M07 | Every simulated path, for the M08 ranges and comparison |

## Conventions

- Timing is beginning of year. Each payment is made first, and then that
  year's return is applied. The first payment is immediate, so it is never
  discounted.
- Ten payments have nine return periods between them. No return is applied
  after the 2042 payment.
- Balances never go negative. Money that isn't there shows up as a
  shortfall, not as a negative balance.
- The 2033 reserve decision uses only what is known in 2033. Later returns
  never change it.
- "Reserve established" and "all payments funded" are reported separately.
  A full reserve can still fall short if returns disappoint.
- Rates are decimals (0.05, not 5).
- Any rate that doesn't come from a sourced assumptions file is labeled
  TEST.
