# Round 1 results: Pat's three industries (1 Nov 2026)

M12 peer score (eight measures, rank-based, 32-variant stability) on the data in
`inputs/m12/round1_2026-10-31/Pat_Round1_M12_data_reviewed.xlsx`, converted by
`tools/round1_xlsx_to_csv.py` to one CSV per group and run with
`python -m m12.run <file>`. Prices: 30 Oct 2026 close. Scores are a research
filter, never a fair value, a return forecast or a buy signal.

## Main run (as assigned)

| Industry | Complete | Top 2 (TFS, variants on shortlist) | Next |
|---|---|---|---|
| Payments | 8 of 10 (StoneCo, dLocal: no capitalized-software figure, rule R4) | Adyen 66.1 (32/32), PagSeguro 66.1 (32/32) | PayPal 57.1 |
| Exchanges and data | 10 of 10 | CME 65.3 (32/32), ICE 63.9 (32/32) | Moody's 54.2 |
| IT services | 9 of 9 (Wipro left out: WInS ADR $2.16, fails the $5 rule) | Infosys 71.9 (32/32), TCS 65.6 (32/32) | Cognizant 54.7 |

Video cross-check (ROE, P/S, P/B added) gives the same top 2 in every group.

## Sensitivity tests (TEST; not the official run)

| Test | Result |
|---|---|
| dLocal software = reported intangible cash additions (USD 34.503m; Note 20: 99% internally generated software) | dLocal 70.3 (31/32), PagSeguro 64.1 (27/32), Adyen 62.5 (6/32) |
| PagSeguro excluded as bank-like (PagBank deposits inflate operating cash flow and are not counted as debt; rule 0.3), dLocal proxy kept | dLocal 73.2 (32/32), Adyen 62.5 (29/32), PayPal 58.9 (3/32) |
| PagSeguro excluded, no dLocal proxy | Group fails the gate (7 of 9 complete, below 80%) |
| Exchanges split from data firms (clearing balance sheets distort asset turnover and debt/assets) | Exchanges: CME 68.8, ICE 65.6 (both 32/32). Data and ratings: Moody's 59.4 (31/32), Verisk 53.1 (29/32) |

StoneCo cannot be scored in any test: its FY2022 diluted EPS was negative
(BRL -1.67), so 3-year EPS growth is UNSUITABLE.

## Industry scores (Damodaran US, January 2026; proxy industries)

| Industry (Damodaran proxy) | Score | Wins | Caveat |
|---|---|---|---|
| Payments (Financial Svcs., non-bank and insurance) | 66.7 | ROE, margin, growth, forward P/E, P/B | Proxy includes lenders (debt/equity 10.0) |
| Exchanges and data (Information Services) | 50.0 | Debt/equity, forward P/E, P/S, P/B | Proxy margin 11.9% vs 40-60% for our companies |
| IT services (Computer Services) | 45.8 | ROE, debt/equity, P/S | Proxy forward P/E 56.5 vs about 13-20 for our companies; below the 50 preference |

## Data notes

- Debt = three borrowing lines; finance leases outside that sum are excluded
  (the spec includes them). Effect on debt/assets is small for these companies.
- Brazilian companies: USD prices converted to BRL at the 30 Oct PTAX rate
  (5.4209). Infosys and TCS use INR Ind AS annual reports.
- Inventory blanks do not affect M12 (inventory is used only by the unscored
  quick ratio).

## Decisions (Pat, 1 Nov 2026)

1. PagSeguro is excluded from the payments ranking: PagBank deposits make its
   cash-flow and debt measures non-comparable (rule 0.3, bank-like accounts).
2. dLocal's capitalized software = its reported intangible cash additions
   (USD 34.503m; Note 20: 99% internally generated software), as a labelled R4
   decision.
3. IT services continues to round 2 despite its 45.8 industry score; the weak
   proxy is stated in the one-pagers.

Official payments run after these decisions: dLocal 73.2 (32/32), Adyen 62.5
(29/32), PayPal 58.9 (3/32), Jack Henry 55.4, Fiserv 50.0, Mastercard 44.6,
Visa 41.1, FIS 14.3; StoneCo unscored.

## Round 2: the nine

| Industry | Companies |
|---|---|
| Payments | dLocal, Adyen, PayPal |
| Exchanges and data | CME, ICE, Moody's |
| IT services | Infosys, TCS, Cognizant |
