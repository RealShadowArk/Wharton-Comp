# Akshaj P. | M12 and Round 2 data update

The October 30, 2026 regular closes were verified in WInS Historical Prices with the Unadjusted setting. All six match the public prices in the earlier package. Listing, source and verification timestamp are in the Round 2 source ledger. No EURUSD=X download is required for these picks.

## M12 rerun

Both groups cleared the kit’s coverage gate with R8 enabled. The software file had six of six complete. The consumer file had five of six complete. Unilever remains incomplete. Scores come from the rerun of the repo kit on November 2, 2026 ET. [Repo kit commit](https://github.com/RealShadowArk/Wharton-Comp/tree/95cb3b31b9f171dc0e18a9263e421706ba45e7dc)

| Group | Ticker | M12 score | Variants in the top two |
|---|---|---:|---:|
| Software | INTU | 67.5 | 32/32 |
| Software | ADBE | 62.5 | 32/32 |
| Software | NOW | 50.0 | 2/32 |
| Consumer brands | NKE | 65.625 | 32/32 |
| Consumer brands | PEP | 56.25 | 18/32 |
| Consumer brands | KO | 56.25 | 16/32 |

The additional software slot goes to the next-highest base score. PEP and KO tie for second in the base score. Both advance, with PEP listed first by stability count. The consumer cross-check selects NKE and PEP.

The patched inputs are `Software.csv` and `M12_peer_data.csv`. New SAP input sources, fiscal dates and the market-cap arithmetic are in the SAP row notes. New consumer values have a separate field-level source table. The two JSON files preserve provenance for carried-forward fields, and the patched CSVs take precedence where fields changed. IAS/IFRS borrowings exclude lease liabilities. Separate leases are documented in the evidence.

## Round 2 workbook

The workbook uses the team’s six-row template from the research branch. `Round 2 sources.csv` records values, dates, links, definitions and MISSING reasons. The named red-flag checks for companies outside the six selections are in that same ledger. Forecast growth is the published analyst consensus snapshot retrieved November 2 ET. The source does not separately timestamp each estimate. Consensus basis and company guidance basis can differ.

Balance-sheet cash, debt and outstanding shares share a date within each company. The source ledger dates the incremental dilution separately. Annual D&A, SBC and interest use FY0. PEP uses R8 borrowings where a separate finance-lease amount is unavailable. KO debt includes the separately presented held-for-sale debt once.

Risk was recalculated from the original Yahoo Finance Max monthly CSVs. A calendar year requires all twelve monthly observations and the prior December. Worst years and displayed returns agree with the earlier workbook. The original Nike export begins in 1985. The original exports include a partial November 2026 row. The risk calculations exclude all of 2026.

The seven original CSVs are in the Yahoo original CSVs folder. Round 2 sources.csv records each download page and timestamp. The remaining issuer fields are listed in MISSING.md.


Independent issuer cross-checks.md records the independent source values, fiscal dates and differences in reporting basis.

Nike’s valuation interest cells contain two S&P standardized inputs marked NOT FULLY VERIFIED. Diageo and Unilever comparison figures appear in the source ledger. M12 inputs and scores were preserved.

The package includes a separate provisional consumer M12 input CSV. The Round 2 workbook and source ledger flag proxy values as NOT FULLY VERIFIED. See MISSING.md for the exact fields and their substitutes.
