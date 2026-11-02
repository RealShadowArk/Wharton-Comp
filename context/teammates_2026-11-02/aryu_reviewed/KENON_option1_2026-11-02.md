# Kenon: option 1, OPC valued on its parts' cash flows (TEST preview, 2 Nov 2026)

Pat chose option 1 on 2 Nov. Aryu's Kenon section and files are still unchanged. Script: `python tools/kenon_sotp.py`; every input and its label is in `IN`.

## What Kenon owns

| Layer | What it is | Share of OPC's EBITDA, H1 2026 |
|---|---|---|
| **Kenon** (NYSE: KEN, Singapore) | Holding company: about 46% of OPC, plus $605m of its own cash (31 Aug), no material debt, no ZIM left | - |
| **OPC Israel** (OPC 80%, Veridis 20%) | Four gas-fired power plants in Israel (Rotem, Hadera, Zomet, Gat). Sells power to private customers and the grid; data-centre contract growing to 460 MW | $90m of $255m (35%) |
| **CPV Group** (OPC about 71%; three Israeli institutions own the rest) | US developer and owner of gas-fired plants, mostly in PJM (stakes in Shore, Maryland and Three Rivers, among others), plus renewables (EBITDA $22m). Basin Ranch (1,350 MW, Texas) is under construction: cost $1.8-2.0bn, COD 2029, $1.1bn Texas Energy Fund loan. Shay (about 2,100 MW, West Virginia) and Walker (1,450 MW, Ohio) are in development | $170m of $255m (67%); head office -$5m |

## Method

1. **Each part valued on its cash flows.** Israel and CPV are valued separately as perpetuities:
   - Run-rate EBITDA = H1 2026 × (FY2025 / H1 2025) = × 2.25, because H2 is the stronger half.
   - Free cash flow = EBITDA × a conversion rate (60/70/80%) for maintenance capex and cash tax. Those figures are MISSING, so the rate is an ASSUMPTION.
   - Growth 2% (ASSUMPTION): the plants age, and projects are valued separately.
   - Discount rates (kit standard: beta 1.0, ERP 5%, 10-year 4.98%): WACC 8.33% for CPV, and 9.76% for Israel, which adds Israel's 1.98% country risk premium.
2. **Basin Ranch.** Valued from its first full year, 2030: about $262m of EBITDA (midpoint of $250-275m) less the remaining cost. Spending to date is MISSING, so 0% and 25% are shown.
3. **Ownership.** OPC's shareholders get 80% of Israel and 71% of CPV.
4. **Net debt.** OPC's net debt on a 100% basis is $2,302m: consolidated debt 2,977 − cash 1,261, plus its share of CPV associates' debt 642 − cash 56. Its split between Israel, CPV and the head office is MISSING, so the share borne by OPC's shareholders is bracketed at 71% to 100%.
5. **Kenon** = 46% × OPC equity + $605m cash, divided by 52.11m shares.

## Result

| Case | Kenon per share | vs $64.11 |
|---|---|---|
| Central: 70% conversion, Basin Ranch 25% spent, net-debt share at the midpoint | **$40.25** | **0.63×** |
| Range: conversion 60-80%, WACC ±1 point, net-debt share 71-100%, Basin Ranch on or off | $19.95 to $62.45 | 0.31× to 0.97× |
| Central, plus Shay and Walker **if built** on Basin Ranch's economics per MW (ASSUMPTION: no investment decision yet) | $51.33 | 0.80× |

Kenon per share at Basin Ranch 25% spent and the net-debt midpoint:

| Conversion | WACC −1 point | WACC as above | WACC +1 point |
|---|---|---|---|
| 60% | $40.71 | $32.32 | $26.18 |
| 70% | $50.11 | $40.25 | $33.03 |
| 80% | $59.52 | $48.19 | $39.89 |

**On our method, Kenon shows no edge.** No combination tested reaches the price without the development projects.

| What it implies | OPC equity for OPC's shareholders |
|---|---|
| OPC's own price (₪93.93) | $9,273m |
| Kenon's price | $5,947m |
| This DCF, central | $3,245m (₪32.87 per OPC share) |

Even Kenon's discounted price assumes about $2.7bn of value from projects not yet under construction: Shay, Walker, Israeli projects and data centres. OPC's own price assumes about $6bn.

## Correction to my earlier Kenon preview

The earlier "consistent look-through" figure of $59.71-60.98 was too high, for two reasons:

- It used Aryu's growth path, which values the consolidated business at about 16× EBITDA.
- It did not deduct the minority owners inside OPC: Veridis's 20% of Israel and the 29% of CPV held by others.

This version fixes both.

## Main uncertainties

- **Run-rate EBITDA.** H1 2026 includes PJM capacity prices at the cap ($333/MW-day through 2028/29) and strong US energy margins. This could be a peak or a new normal.
- **Maintenance capex and tax.** MISSING; the conversion range covers them.
- **Net-debt split by segment.** MISSING. The two extremes are about $6/share apart (±$3 around the midpoint).
- **Basin Ranch figures.** Its EBITDA comes from a garbled table, and spending to date is MISSING.
- **Excluded upside.** Israeli projects and CPV renewables growth are not counted.
- **Rate.** The 10-year: see the 4.94% note in the chat of 2 Nov. It moves the value by under 1%.

## War and politics (sourced facts first, then judgment)

**Facts:**
- The war with Iran began **28 Feb 2026**. Israel shut the Leviathan and Karish gas fields that day; Leviathan restarted about 3 Apr, after 32-33 days.
- A two-week ceasefire was agreed on 7 Apr, tied to reopening the Strait of Hormuz.
- A live tracker (secondary, not authoritative) says that ceasefire collapsed on 7-8 Jul, that a tanker war has run since September, and that no ceasefire is in force as of 1 Nov.
- On 31 Oct an Iranian official said there would be no talks and no reopening of Hormuz until the US accepts Iran's demands.
- Hezbollah is reported to be rearming with Iranian cash.
- One report (New York Post, via Yahoo) says Israel could strike again after the US midterms on 3 Nov. It is unconfirmed.
- Israel voted on 27 Oct. Trump did not endorse Netanyahu, and support for Israel has become a fault line in US politics (Al Jazeera, Mother Jones; partly opinion).
- OPC's Israel EBITDA still rose 22% in H1 2026, which included the March shutdown. In the 2023 war, OPC said its plants had enough gas: Tamar was suspended, Karish was not.

**Judgment: what it means for each part:**

- **Israel (35% of EBITDA): direct exposure.**
  - The plants burn Israeli offshore gas, and the fields are shut whenever fighting starts.
  - Power plants and gas platforms are high-value targets in a war where both sides have struck energy infrastructure.
  - A weaker shekel cuts the dollar value of Israeli profits; NIS debt partly offsets this.
  - H1 2026 shows the business survived one shutdown. A longer one, or physical damage, would hurt more.
- **CPV (65%): no physical exposure, some indirect effects.**
  - Hormuz and LNG disruption raise world gas prices. That lifts power prices but also CPV's fuel costs; the net effect is mixed.
  - PJM capacity prices are capped, so there is no extra upside there.
  - Higher inflation expectations and a 5% 10-year raise the cost of funding Shay and Walker.
  - A US-Israel rift could in principle bring political scrutiny of Israeli ownership of US power plants. I found **no evidence** of this; it is a low-probability risk, not a finding.
- **Kenon's and OPC's share prices.** War headlines widen the "Israel discount" that investors apply. Both stocks are about 31-33% below their highs. War risk is a plausible part of the cause, but no source says so, so the dip's cause stays MISSING.
- **Effect on this valuation.** The Israel discount rate already includes the 1.98% country risk premium. A one-quarter outage costs about $50m of EBITDA, about $0.4 per Kenon share. The war matters more for the share price and its swings than for the cash-flow value, and that value is already below the price.

## Sources

- [Kenon Q2 2026 release (Nasdaq)](https://www.nasdaq.com/press-release/kenon-holdings-reports-q2-2026-results-and-additional-updates-2026-09-08)
- [OPC H1 2026 report (Kenon 6-K)](https://www.sec.gov/Archives/edgar/data/1611005/000117891326004078/exhibit_99-1.htm)
- [Kenon Q2 2026 6-K](https://www.sec.gov/Archives/edgar/data/1611005/000117891326004442/exhibit_99-1.htm)
- [Kenon 20-F FY2025](https://www.sec.gov/Archives/edgar/data/0001611005/000117891326001842/zk2634883.htm)
- [Kenon FY2025 results](https://www.morningstar.com/news/pr-newswire/20260330ln22046/kenon-holdings-reports-full-year-2025-results-and-additional-updates)
- [OPC Q2 2026 (AOL/PR Newswire)](https://www.aol.com/articles/opc-energy-reports-strong-second-102300000.html)
- [OPC H1 segments (TipRanks)](https://www.tipranks.com/news/company-announcements/kenons-opc-energy-posts-strong-h1-2026-ebitda-after-u-s-portfolio-reclassification)
- [Basin Ranch (CPV)](https://cpv.com/our-fleet/cpv-basin-ranch-energy-center/)
- [Basin Ranch Texas Energy Fund loan](https://www.businesswire.com/news/home/20251030191068/en/CPV-Basin-Ranch-and-Texas-Energy-Fund-Ink-Deal-for-1350-MW-ERCOT-Project)
- [Basin Ranch cost (Kenon 6-K)](https://www.sec.gov/Archives/edgar/data/0001611005/000117891326002811/exhibit_99-1.htm)
- [CPV Maryland/Three Rivers swap](https://www-web.itiger.com/news/2616499349)
- [Leviathan and Karish shut 28 Feb (Times of Israel)](https://www.timesofisrael.com/israels-leviathan-natural-gas-field-to-resume-operations-after-iran-ceasefire/)
- [Leviathan restart (Bloomberg)](https://www.bloomberg.com/news/articles/2026-04-03/israel-resumes-biggest-gas-field-after-war-shut-it-for-a-month)
- [Timeline of the 2026 Iran war](https://en.wikipedia.org/wiki/Timeline_of_the_2026_Iran_war)
- [Iran war tracker (secondary)](https://iranwarlive.com/)
- [Times of Israel, 31 Oct](https://timesofisrael.com/liveblog-october-31-2026)
- [Hezbollah rearming](https://www.timesofisrael.com/hezbollah-rearming-for-possible-renewed-conflict-with-israel-lebanese-sources-say/)
- [Post-midterm strike report (Yahoo)](https://www.yahoo.com/news/politics/articles/israel-could-unleash-hezbollah-style-222506301.html)
- [Trump and the Israeli vote (Al Jazeera)](https://www.aljazeera.com/news/2026/10/13/despite-long-history-with-netanyahu-trump-hedges-as-israel-vote-nears)
- [US-Israel politics (Mother Jones)](https://www.motherjones.com/politics/2026/10/united-states-israel-relationship-jewish-political-groups-elections/)
- [FDD brief, 20 Oct](https://www.fdd.org/overnight-brief/october-20-2026/)
- [OPC 2023 war report (Kenon 6-K)](https://www.sec.gov/Archives/edgar/data/1611005/000117891323003724/exhibit_99-1.htm)
