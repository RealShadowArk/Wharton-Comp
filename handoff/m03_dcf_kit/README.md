# M03 DCF kit (24 Oct 2026)

A self-contained copy of the team's company-valuation code (module M03) and
the 11 valuations done so far. The master copy lives in Pat's GitHub repo
(`realshadowark/wharton-comp`, branch `main-eiek71`). If you have access,
use that instead of this zip.

## Why you saw "No module named 'm03'"

The earlier handoff didn't include the code. Python also looks for `m03`
in the folder you run it from. Unzip this kit, open a terminal **inside the
unzipped folder** (the one that contains `m03/`), and run the commands below.

## Run it (Python 3.9 or newer; no extra packages)

```
python -m m03.run PYPL              # one company
python -m pytest -q tests/test_m03.py   # optional: 11 checks (needs pytest)
```

Each run writes `outputs/M03_Valuation_<TICKER>.md` (the readable report)
and `.csv` (the year-by-year numbers).

## Add a company

1. Copy `inputs/m03/TEMPLATE_dcf_inputs.csv` to `inputs/m03/<TICKER>_dcf_inputs.csv`.
2. Fill every row. Give each value a label (RESEARCH, ASSUMPTION or MISSING)
   and a source. Never fill a missing number with a guess: mark it MISSING.
3. Run `python -m m03.run <TICKER>` and read the report.

`tools/make_m03_inputs.py` shows how the standard inputs were built for the
ten companies (run it from the kit folder to rebuild them).

## What the model does

| Step | Formula |
|---|---|
| Free cash flow to the firm | FCFF = EBIT x (1 - tax) + D&A - capex - change in working capital |
| Discount rate | WACC = equity share x (Treasury + beta x premium) + debt share x cost of debt x (1 - tax) |
| Terminal value | TV = FCFF in year 11 / (WACC - g); the model stops if WACC <= g |
| Value per share | (present value of FCFF + TV) + cash - debt, divided by diluted shares |
| Reverse DCF | Shifts every year's growth until the value equals the price, which shows the growth the price assumes |

Standard settings used on 23 Oct: 10-year forecast, Treasury 5.13%, beta 1.0,
equity premium 5%, terminal growth 3% with 20% reinvestment. Results:
`outputs/M03_summary.md`. Decisions: `outputs/M03_Thesis_and_Rejection_Log.md`.

## What is still missing (data collection)

- Cash for ZTS, BSX, AME, ETN, ADI and LLY.
- Company betas: all use 1.0 for now.
- Each stock's worst calendar year, needed for the 2% loss rule.
- PayPal's live price: $55.53 is from 9 Oct.

A DCF value is a research estimate under stated assumptions. It is never a
price target, an annual return or a position size.
