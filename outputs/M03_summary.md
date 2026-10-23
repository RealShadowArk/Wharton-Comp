# M03 summary: DCF value vs price (standard method, 23 Oct 2026)

Same method for every company (see `tools/make_m03_inputs.py` and each `inputs/m03/<TICKER>_dcf_inputs.csv`): 10-year FCFF forecast (5 stated years, then growth fading to 3%), FY0 margin held flat, beta 1.0, equity premium 5%, 10-year Treasury 5.13%, terminal growth 3% with 20% reinvestment. Values are research estimates under these assumptions: not price targets, returns or position sizes.

| Ticker | DCF value / share | Price | Value / price | Base revenue growth, avg 2026-30 | Growth the price implies, avg 2026-30 | WACC | Cash |
|---|---|---|---|---|---|---|---|
| PYPL | $111 | $55.53 | 2.00 | 3.8% | -6.4% | 9.07% | included |
| ZTS | $85 | $81.92 | 1.04 | 3.1% | 2.7% | 8.93% | MISSING (value understated) |
| BSX | $46 | $46.02 | 0.99 | 7.4% | 7.5% | 9.35% | MISSING (value understated) |
| JKHY | $104 | $149.31 | 0.70 | 5.5% | 10.5% | 10.11% | included |
| HUBB | $301 | $450.83 | 0.67 | 6.0% | 11.2% | 9.08% | included |
| AME | $113 | $236.82 | 0.48 | 4.8% | 14.5% | 9.91% | MISSING (value understated) |
| ETN | $166 | $369.61 | 0.45 | 7.8% | 17.8% | 9.78% | MISSING (value understated) |
| ADI | $182 | $414.68 | 0.44 | 11.0% | 21.9% | 9.91% | MISSING (value understated) |
| ISRG | $186 | $443.84 | 0.42 | 13.6% | 26.9% | 10.13% | included |
| LLY | $466 | $1,307.12 | 0.36 | 14.2% | 27.7% | 9.93% | MISSING (value understated) |
| MPWR | $357 | $1,210.86 | 0.29 | 15.4% | 33.6% | 10.13% | included |
