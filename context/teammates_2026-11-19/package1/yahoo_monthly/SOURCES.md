# Sources of these monthly price files

- `INTU.csv`, `QCOM.csv`, `SPY.csv`: the teammate's Yahoo Finance Max monthly downloads (package 1 zip, 19 Nov 2026), copied unchanged.
- `TEL.csv`, `FOXA.csv`, `CMCSA.csv`, `TMUS.csv`: not in the teammate's zip. Fetched from Yahoo Finance on 19 Nov 2026 with `python tools/fetch_yahoo_monthly.py context/teammates_2026-11-19/package1/yahoo_monthly TEL FOXA CMCSA TMUS` (monthly adjusted closes, Yahoo CSV format). RESEARCH.
