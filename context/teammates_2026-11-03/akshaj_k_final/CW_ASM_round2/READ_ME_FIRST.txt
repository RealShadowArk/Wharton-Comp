ROUND 2 — CW AND ASM INTERNATIONAL
Prepared 3 November 2026

Open CW_and_ASM_Round2.xlsx. It follows the new README, covering CW and optional ASM.AS only.
FY0 is 2025 and FY1 is 2024. Cash/debt/year-end outstanding shares are dated 31 December 2025; the latest quarterly incremental dilution is added separately.
Review Research_notes_and_AI_use_log.pdf before using the data. Source_ledger.csv gives field-level sources. Yahoo_Max_monthly contains four unmodified original downloads and a manifest.
Evidence contains the December endpoints and annual USD return calculations. Yahoo EURUSD starts in December 2003; the Federal Reserve original supplies earlier FX endpoints.
All requested red-flag fields are filled. Two main valuation numerical cells remain blank: CW capitalized software and standalone interest income. Two supplementary ASM disclosure gaps remain unresolved.
FOLLOW-UP: ASM WInS listing is verified as Europe > Amsterdam > ASM. No order was reviewed or submitted. Gap_review.csv and Valuation inputs rows 18-26 list rejected, incomplete and not fully verified provider candidates. These are not accepted model replacements.

EVERY FIELD STILL MISSING

CW | capex_software
No separately quantified software-capitalization cash outflow found in FY2025 annual report. Not zero. Follow-up: expanded Yahoo Gold annual cash flows show FY2025 Purchase of Intangibles as -- and no software-only row. The FY2025 SEC inline filing and Companyfacts have no standalone software-capitalization fact. The blank does not mean zero.
Effect: Cannot add a verified separate software cash deduction to a DCF.
Importance: Moderate; exact FCF scope.
Possible source: Company IR clarification or a future expanded software-cost note.
Source: https://www.sec.gov/Archives/edgar/data/0000026324/000162828026007587/cw-20251231.htm; https://finance.yahoo.com/quote/CW/cash-flow/; https://data.sec.gov/api/xbrl/companyfacts/CIK0000026324.json
Checked: 2026-11-03

CW | interest_income
Interest income is included in other income, net, with pension and other items; no standalone FY2025 amount verified. Follow-up: Yahoo Gold has no standalone interest-income row after expansion. Macroaxis labels USD 43.15m as Interest Income, but that equals the rounded FY2025 reported interest expense of USD 43.148m, also classified as expense by Yahoo. This candidate is REJECTED for interest income.
Effect: Cannot isolate interest income for an exact operating-earnings/tax bridge.
Importance: Moderate; does not block EBIT-based DCF inputs.
Possible source: Company IR breakdown; a provider value reconciled to the filing.
Source: https://www.sec.gov/Archives/edgar/data/0000026324/000162828026007587/cw-20251231.htm; https://finance.yahoo.com/quote/CW/financials/; https://www.macroaxis.com/financial-statements/CW/Interest-Income
Checked: 2026-11-03

ASM.AS | total_discounted_lease_liability
Current carrying lease liability is 13.9m. The 19.6m noncurrent figure appears in a contractual-obligations table; it is not verified as discounted carrying value. Official 2025 ESEF package also checked: lease-payment and lease-note tags were found, but no separate lease-liability carrying-value fact. Follow-up candidates: StockAnalysis/S&P reports EUR 77.9m total debt including EUR 64.0m long-term leases, but EUR 64.0m equals all noncurrent Other liabilities in the filing and is not reconciled as leases. FT reports rounded EUR 34m total debt, without a discounted lease reconciliation. Yahoo Gold shows EUR 13.9m Capital Lease Obligations but leaves FY2025 long-term leases blank; the displayed total covers only the current amount. All three are NOT FULLY VERIFIED as the requested total.
Effect: Lease-inclusive sensitivity remains incomplete; requested IFRS borrowings-only debt is verified at zero.
Importance: Supplementary; does not block debt under this README.
Possible source: Company IR or an audited lease reconciliation splitting current and noncurrent discounted carrying values; the available ESEF package has already been checked.
Source: https://www.asm.com/media/3skhiimk/asm-2025-annual-report.pdf; https://stockanalysis.com/quote/ams/ASM/financials/balance-sheet/; https://markets.ft.markitdigital.com/data/equities/tearsheet/financials?s=ASM%3AAEX&subview=BalanceSheet; https://finance.yahoo.com/quote/ASM.AS/balance-sheet/
Checked: 2026-11-03

ASM.AS | software_only_cash_outflow
Note 6 separately reports 44.5m software additions. The cash-flow statement reports 44.7m total intangible purchases, not software-only cash payments. Follow-up: Yahoo Gold reports EUR 468.3m aggregate capex, reconciling to PPE 218.5m + capitalized development 205.1m + all intangible cash purchases 44.7m. It has no separate FY2025 software cash figure. The EUR 44.5m additions figure is VERIFIED as additions, NOT FULLY VERIFIED as software-only cash capex.
Effect: 44.5m is identified as an accrual addition; do not assume it exactly equals software cash capex.
Importance: Moderate; FCF interpretation.
Possible source: Company IR reconciliation of software additions to software cash paid.
Source: https://www.asm.com/media/3skhiimk/asm-2025-annual-report.pdf; https://finance.yahoo.com/quote/ASM.AS/cash-flow/
Checked: 2026-11-03