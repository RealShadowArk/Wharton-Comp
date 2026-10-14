# Sector Valuation History Brief

**Instructions for the AI:** follow every instruction in this document. It is my full request. Today's date is 14 October 2026. Use web browsing. Accuracy matters more than length.

## 1. Context

I am a high-school student researching a long-term US stock portfolio for an investment competition. I am choosing sector ETFs (XLK Technology, XLI Industrials, XLV Health Care, XLC Communication Services) and need to know whether each sector is expensive or cheap **compared with its own history and with US Treasury bonds**. I also need one country data point for a risk calculation.

Background figures I already have (verify them if you use them):

- 10-year Treasury yield: 5.24% on 9 October 2026; 5.29% on 30 September 2026 (Federal Reserve H.15).
- Select Sector SPDR index P/E on 13 October 2026, trailing / forward: XLK 33.80 / 24.58; XLC 16.37 / 13.77; XLI 28.69 / 24.72; XLV 31.41 / 20.46; XLF 15.41 / 15.32; XLY 26.18 / 22.41; XLP 25.18 / 20.11; XLE 19.08 / 12.59; XLB 23.20 / 16.82; XLU 18.87 / 17.46; XLRE 31.43 / 33.36.

## 2. Task A: sector valuation history

For the **S&P 500 index and each of its 11 GICS sectors**, collect the **forward 12-month P/E** at **each year-end from 2015 to 2025**, plus the **latest available 2026 value** with its exact date.

1. Use **one source for all sectors and all years** so the numbers are comparable. Preferred sources, in order:
   - Yardeni Research "S&P 500 Sectors & Industries Forward P/Es" (based on LSEG I/B/E/S forward earnings);
   - S&P Dow Jones Indices sector data;
   - FactSet Earnings Insight.

   State which one you used and why. If no single source covers everything, say exactly where you had to switch, and do not mix sources inside one row.
2. If a **trailing P/E** series from the same source is available, collect it too. Otherwise write "Not collected".
3. Collect the **10-year Treasury constant-maturity yield** (FRED series DGS10) on the **same dates**. If a date is a holiday, use the last trading day before it and say so.
4. Calculate, showing your arithmetic:
   - forward earnings yield = 100 ÷ forward P/E;
   - gap = forward earnings yield − Treasury yield, in percentage points.
5. For each sector, calculate:
   - the 2015–2025 **average** forward P/E;
   - the **highest and lowest** year-end values;
   - where the latest value sits against that range, as a **percentile** (0 = cheapest year in the range, 100 = most expensive).

## 3. Task B: India's worst calendar year

I need a stand-in for the worst year of the iShares MSCI India ETF (INDA), which only began in 2012.

1. Collect **MSCI India Index calendar-year total returns in US dollars (net)** for 2000–2025, especially **2008**.
2. Collect **MSCI Emerging Markets** returns (USD, net) for the same years for comparison.
3. Collect **INDA's annual NAV total returns** for 2013–2025 from iShares.
4. Report MSCI India's worst calendar year and its value. If 2008 is not available from a primary source, say "Not collected" and name where it could be found.

## 4. Accuracy rules (follow every one)

1. **Never state a number from memory as a fact.** Every number needs:
   - its value;
   - the date it refers to;
   - its source name and URL.

   If you cannot browse, say so at the top and give a data-collection checklist instead of numbers.
2. Label every number:
   - **Sourced**: a primary source such as an index provider, the Federal Reserve or FRED, or the fund issuer;
   - **Secondary**: a data site or news report;
   - **Calc**: your own arithmetic, shown;
   - **Forecast**.
3. If you cannot find or verify something, write **"Not collected"**. Never estimate, fill gaps, use zero or average.
4. **Flag sector-definition changes that break comparability:**
   - Real Estate became its own sector in 2016.
   - Communication Services was created in September 2018, moving companies out of IT and Consumer Discretionary.
   - Payment companies such as Visa and Mastercard moved from IT to Financials in March 2023.

   Mark the affected years and sectors, and say how they distort the history.
5. Say whether the forward earnings are "operating" or "as reported", and keep one basis throughout.
6. Do not interpret a cheap or expensive reading as a prediction. Historical valuation does not forecast returns.
7. Do not recommend what to buy, how much, or what return to expect.

## 5. Output format

1. **Summary table:** one row per sector, with these columns:
   - latest forward P/E and its date;
   - 2015–2025 average;
   - high and low;
   - percentile;
   - latest forward earnings yield;
   - gap vs the 10-year Treasury.
2. **Full history table:** sectors as rows, year-ends as columns, forward P/E.
3. **Gap history table:** the same layout, showing forward earnings yield minus the Treasury yield.
4. **Treasury table:** DGS10 on each date.
5. **India table:** MSCI India, MSCI EM and INDA annual returns; the worst year identified.
6. **Comparability notes:** the sector changes from rule 4 and any source switches.
7. **Numbered source list** with URLs and access dates.
8. **A short list of the claims you are least sure about**, so I can check them first.

Ask me if anything is unclear before you start.
