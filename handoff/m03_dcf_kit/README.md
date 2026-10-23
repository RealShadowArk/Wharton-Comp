# M03 DCF kit, version 2 (23 Oct 2026)

A self-contained copy of the team's company-valuation code (module M03) and
the 11 valuations done so far. The master copy lives in Pat's GitHub repo
(`realshadowark/wharton-comp`, branch `main-eiek71`). If you have access,
use that instead of this zip. Please don't change the engine (`m03/`)
yourself; send suggested changes to Pat so we keep one version.

Version 1 was wrongly dated 24 Oct; it was built on 23 Oct.

## What changed in version 2

| Change | Why |
|---|---|
| Inputs are the teammate-corrected files of 23 Oct | Cash for all 11, 22 Oct closes, verified diluted shares |
| New row `sbc_pct` (stock-based pay / revenue), subtracted from FCFF | The D&A row is calibrated from operating cash flow, which adds stock-based pay back. Blank = MISSING, and the report shows the effect of each 1% of revenue |
| New row `net_interest_pct` (ETN, LLY, ZTS) | Their margin is a pretax margin; adding net interest gives EBIT. Blank = value understated |
| `return_on_new_capital` (0.15) replaces the fixed 20% reinvestment | Reinvestment = g / 15%, so the growth sensitivity stays consistent |
| New row `first_year_fraction` | Counts only the part of year 1 not already in the bridge's cash (use 0.5 with 30 June balances) |
| New row `beta_measured` | The report shows the value at beta 1.0, the measured beta and the adjusted beta (0.67 x measured + 0.33). Pat chooses which one the DCF uses |
| Input checks and a sturdier reverse DCF | Errors on impossible inputs or a bad price; the solver also works when growth lowers value |
| `tools/make_m03_summary.py` | Rebuilds `outputs/M03_summary.md` and all 11 reports |

## Why you saw "No module named 'm03'"

The first handoff didn't include the code. Python also looks for `m03`
in the folder you run it from. Unzip this kit, open a terminal **inside the
unzipped folder** (the one that contains `m03/`), and run the commands below.

## Run it (Python 3.9 or newer; no extra packages)

```
python -m m03.run PYPL                  # one company
python tools/make_m03_summary.py        # all 11 plus the summary table
python -m pytest -q tests/test_m03.py   # optional: 17 checks (needs pytest)
```

Each run writes `outputs/M03_Valuation_<TICKER>.md` (the readable report)
and `.csv` (the year-by-year numbers).

## Add a company

1. Copy `inputs/m03/TEMPLATE_dcf_inputs.csv` to `inputs/m03/<TICKER>_dcf_inputs.csv`.
2. Fill every row. Give each value a label (RESEARCH, ASSUMPTION or MISSING)
   and a source. Never fill a missing number with a guess: leave it blank
   and mark it MISSING.
3. Run `python -m m03.run <TICKER>` and read the report, including its
   "Data gaps and open choices" table.

## What the model does

| Step | Formula |
|---|---|
| Free cash flow to the firm | FCFF = EBIT x (1 - tax) + D&A - capex - change in working capital - stock-based pay (only when D&A is the cash-flow calibration) |
| Discount rate | WACC = equity share x (Treasury + beta x premium) + debt share x cost of debt x (1 - tax) |
| Terminal value | TV = FCFF in year 11 / (WACC - g); the model stops if WACC <= g |
| Value per share | (present value of FCFF + TV) + cash - debt, divided by diluted shares |
| Reverse DCF | Shifts every year's growth until the value equals the price, which shows the growth the price assumes |

Standard settings: 10-year forecast, Treasury 5.13%, beta 1.0, equity
premium 5%, terminal growth 3% with reinvestment g / 15%. Results:
`outputs/M03_summary.md`. Decisions: `outputs/M03_Thesis_and_Rejection_Log.md`.

## Still missing (requested from P2 on 23 Oct)

- Stock-based pay for the 10 companies other than HUBB.
- Net interest for ETN, LLY and ZTS.
- Debt and diluted shares at the same date as the interim cash (needed
  before switching to 30 June balances).

A DCF value is a research estimate under stated assumptions. It is never a
price target, an annual return or a position size.
