# Aryu's research (power, medtech): fact-check log, 2 Nov 2026

The original zip, `../Aryu_stock_research_power_medtech_2026-11-02.zip`, is unchanged. This folder contains:

- `(fact-checked, clean)`: the same two documents with all changes accepted (Pat, 2 Nov);
- the two documents with every fix as a **Word tracked change**, author "Fact-check for Pat (Claude)". Accept or reject each one in Word or Google Docs; rejecting all gives the original back.
- the DCF input files (`inputs/m03/`) and the reports re-run with the kit engine (`outputs/`).

Pat approved fixes 2-5 on 2 Nov. Fix 1 (Kenon's valuation) waits for Pat's questions.

**Nothing in Kenon's section was changed: its text, tables, DCF files and rate are all as Aryu sent them** (`KEN*_dcf_inputs.csv` are identical to the originals).

## Fix 2: one Treasury rate for every DCF

- `risk_free`: 4.929% (Yahoo ^TNX) → **4.98%** (RESEARCH: FRED DGS10, 30 Oct 2026, read by Pat).
- `pre_tax_cost_of_debt` follows it (kit default, 10-year + 0.5 points): 5.429% → 5.48%.
- Risk measures: rf 3.97% → **4.00%** (RESEARCH: FRED DTB3, 30 Oct 2026, read by Pat). This lowers each Sharpe ratio by about 0.001 and each Treynor ratio by under 0.0004, so the displayed values are kept.

| | Beta 1.0 | Measured beta | Adjusted beta | Price implies (vs base path) | Bear | Upside / downside |
|---|---|---|---|---|---|---|
| CEG ($262.38) | $146.41 → **$145.03** (0.55) | $133.79 → **$132.59** (0.51) | $137.74 → **$136.49** (0.52) | +6.5 → **+6.6** points | $64.00 → **$63.25** | no upside (−45%): fails |
| NRG ($96.06) | $130.50 → **$128.24** (1.34) | $106.52 → **$104.75** (1.09) | $113.80 → **$111.89** (1.16) | −2.1 → **−2.0** points | $46.20 → **$44.82** | +33.5% / −53.3% = **0.63** (was 0.69): fails |
| RMD ($229.94) | $187.03 → **$185.77** (0.81) | $221.39 → **$219.58** (0.95) | $208.64 → **$207.05** (0.90) | +3.0 → **+3.1** points | $132.33 → **$131.48** | no upside (−19%): fails |
| ALC ($71.45) | $57.16 → **$56.69** (0.79) | $63.19 → **$62.61** (0.88) | $61.07 → **$60.53** (0.85) | +2.7 → **+2.8** points | $44.29 → **$43.91** | no upside (−21%): fails |
| EW ($92.01) | $46.90 → **$46.62** (0.51) | $51.55 → **$51.21** (0.56) | $49.89 → **$49.58** (0.54) | +10.5 → **+10.6** points | $36.29 → **$36.10** | no upside (−49%): fails |

The Aryu notes that depend on these numbers were updated too:

- NRG with reported D&A: $213 → $210; the cost of debt is now 5.5%.
- ALC with 3 more points of margin: $67 → $66.
- EW with 3 more points of margin: $52, unchanged.

**No conclusion changes.** NRG is still the only one of the five with value above the price at both betas, and it still fails the upside-to-downside test.

## Fix 3: overstated claims

| Claim | Correction | Sources |
|---|---|---|
| CEG has "over 10,000 MW" of long-term deals (drivers, CEG rows 3 and 4) | Confirmed deals total about **4,700 MW plus Crane**: <br>• CyrusOne about 1,100 <br>• Amazon 690 <br>• Google 890 <br>• Meta about 1,100 <br>• 920 signed in Q2 2026, which may overlap with CyrusOne <br>Vistra's and Talen's totals were not found. | [CyrusOne](https://finance.yahoo.com/news/constellation-energy-corporation-ceg-unit-033403560.html), [Amazon](https://baxtel.com/posts/amazon-constellation-sign-20-year-ppa-for-190mw-calvert-cliffs-uprate), [Google](https://w.media/?p=44232), [Q2 2026 8-K](https://www.sec.gov/Archives/edgar/data/0001868275/000186827526000097/ceg-20260806991.htm) |
| Higher PJM capacity prices (industry drivers) | Kept, and added that the last three auctions all cleared at the **price cap**: $329.17, then $333.44/MW-day, then the cap again for 2028/29. Prices are capped, not rising. | [PJM](https://insidelines.pjm.com/pjm-auction-procures-134479-mw-of-generation-resources/), [Utility Dive](https://www.utilitydive.com/news/pjm-interconnection-capacity-auction-data-center/808264/) |

Kenon's edge sentence says "PJM capacity prices are rising". It is part of the Kenon discussion, so it is not changed yet.

## Fix 4: industry scores (forward P/E vs the total market, Pat's Round 1 convention)

| Industry | Forward P/E | Total market | Points | Total |
|---|---|---|---|---|
| Power | 17.59 | 27.66 | 8.3 | 29.1 → **37.5** (still below 50) |
| Medtech | 42.33 | 27.66 | 0 | **45.8** (unchanged, just below 50) |

Source: [Damodaran PE data, US, January 2026](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/pedata.html) (the same table Aryu used for the industry values).

## Fix 5: findings recorded (non-Kenon)

| Where | Added | Sources |
|---|---|---|
| CEG 10-year plan | 6 Aug 2026: 2026 adjusted EPS guidance raised to $11.50-12.50; 920 MW of new long-term contracts | [Q2 2026 8-K](https://www.sec.gov/Archives/edgar/data/0001868275/000186827526000097/ceg-20260806991.htm) |
| NRG competition | About 6m retail energy customers vs Vistra's about 5m (not a same-date comparison) | [NRG 2025 10-K](https://www.sec.gov/Archives/edgar/data/1013871/000101387126000004/nrg-20251231.htm), [Vistra S-3](https://www.sec.gov/Archives/edgar/data/0001692819/000114036126035954/ny20081693x1_s3asr.htm) |
| NRG dip | 2026 adjusted EPS guidance $7.90-9.90, reaffirmed 4 Aug | [NRG Q2 2026 release](https://lasvegassun.com/news/2026/aug/04/nrg-energy-reports-second-quarter-2026-results-and/) |
| ALC competition | J&J Vision and Bausch + Lomb confirmed as the main rivals; Alcon over 60% of presbyopia-correcting lens implants (undated, older estimate) | [Zacks](https://www.zacks.com/stock/news/2165065/alcon-alc-gains-from-growing-market-demand-new-launches) |
| EW competition | TAVR share: Edwards about 55-66%, Medtronic about 28%, Abbott about 3% | [GlobalData](https://www.globaldata.com/media/medical-devices/medtronic-to-increase-share-in-tavr-market-after-positive-evolut-trial-results-says-globaldata/), [GMI](https://www.gminsights.com/industry-analysis/tavr-transcatheter-aortic-valve-replacement-market), [MedTech Dive](https://www.medtechdive.com/news/edwards-raises-2026-forecast-as-tavr-sales-surge/818394/) |

Boston Scientific is **not** listed as a TAVR rival: the only source is undated, and the claim could not be confirmed.

## Waiting for Pat

1. **Kenon (fix 1):** valuation method. Ready to record once decided:
   - 46% OPC stake; parent cash $605m (31 Aug); no ZIM left;
   - $200m dividend; $93m award; Israel CRP 1.98%;
   - rivals: Israel Electric Corp, Dorad, Dalia;
   - Shay and Walker facts;
   - the PJM wording in the edge;
   - rate 4.98%.
2. **OPC's 30 Oct close:** 9,393 agorot = ₪93.93 (RESEARCH: TASE, read by Pat 2 Nov; Pat first read 14,900 in error). 31% below the 52-week high of ₪136.90.
3. **Not part of fixes 2-5, so not done:**
   - Power M12 handling: accept the no-G2 diagnostic, or rank by judgment;
   - CEG's short-history sizing (no losing calendar year).
