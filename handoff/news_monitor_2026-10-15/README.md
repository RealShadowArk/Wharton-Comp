# Handoff: fundamental analysis and news monitoring (15 Oct 2026)

## 1. The project in two minutes

- **The competition:** Wharton Global High School Investment Competition
  2026-27. We manage a simulated $300,000 portfolio in **WInS** for a
  fictional client, Laura Gao.
- **How we're judged:** on **reasoning and strategic coherence**, not returns
  or the number of trades. The weekly emails also say teams should "document
  research, decision-making and reasoning" and show how they "responded to
  changing market conditions". **That's where your job matters.**
- **Laura:**
  - she contributes $300,000 (2027) and $150,000 (2028);
  - she must pay **ten fixed $50,000 payments, at the start of each year
    2033-2042**;
  - the riskiest window is **2031-2032**, just before the payments start.
- **Strategy (floor rule):** Treasury bonds that cover all ten payments are
  already bought. Stocks equal 2 × the money above that floor.
- **Portfolio:**

| Part | Holdings | % |
|---|---|---|
| Bond ladder (bought 8 Oct) | IBTM, IBTO, IBTP, IBTQ, IBTR + Treasuries maturing Feb 2037, May 2038, Nov 2039, Nov 2040, Nov 2041 | 33.6% |
| Core ETFs | VOO (S&P 500), VXUS (all non-US markets) | 16.9% |
| Sector tilt ETFs | XLI (industrials), XLK (tech), XLV (health care), XLC (communication), XLF (financials) | 10% |
| Individual US stocks | Chosen from the shortlist below by the M12 score and M03 valuation | 39.5% |

- **Biggest risk we're watching: an AI-spending bubble.** About 47% of the
  S&P 500 is tech plus communication, both driven by AI.
- **Key dates:**
  - **23 Oct:** Trading Notes Analysis due;
  - **6 Nov:** the portfolio freezes and the IPS is due;
  - **4 Dec:** Final Report due.

## 2. Your job (two parts)

### Part A: Thesis cards for the shortlisted companies (fundamental, qualitative)

**Due:**
- the first 7 by **Mon 19 Oct**;
- the other 4 by **Tue 20 Oct**.

| Priority | Companies |
|---|---|
| First 7 (robust leaders) | PYPL (PayPal), ZTS (Zoetis), LLY (Eli Lilly), HUBB (Hubbell), MPWR (Monolithic Power), BSX (Boston Scientific), ISRG (Intuitive Surgical) |
| Next 4 | JKHY (Jack Henry), ETN (Eaton), AME (AMETEK), ADI (Analog Devices) |

**One page per company,** with these sections:
1. **Business model:** what it sells, to whom, and how it makes money (two or
   three sentences).
2. **Competitive position:** a short Porter's Five Forces check (rivalry,
   new entrants, substitutes, customer power, supplier power), one line each.
3. **SWOT:** two bullets each.
4. **Three drivers** that decide its next 1-3 years.
5. **Contrary thesis:** the strongest case *against* owning it, plus **one
   measurable "what would prove us wrong" signal**. Examples: "revenue growth
   below 5% for two quarters"; "loses FDA approval for X". This becomes our
   sell trigger.
6. **Recent news (last 90 days):** date, headline, source link, why it
   matters.
7. **Next catalyst:** the next earnings date, an FDA decision, a court
   ruling, etc.
8. **Financially material ESG risks only:** e.g., a product-safety recall.
   Not personal preferences.

**Do not:**
- give price targets or buy/sell calls;
- say how much to invest.

Pat does the valuation (M03) and decides.

### Part B: Daily news scan and signal log (16 Oct to 6 Nov, then weekly to 4 Dec)

**What to watch** (`watchlist.csv`):
- every holding;
- the shortlist;
- these themes:
  - **AI bubble indicators:** big-tech AI spending guidance (Microsoft,
    Alphabet, Amazon, Meta), Nvidia results, data-center power deals;
  - **Interest rates:** Federal Reserve decisions, the 10-year Treasury yield
    (FRED series DGS10);
  - **Credit and banks:** bank earnings, loan losses (this matters for XLF);
  - **Oil.**

**Where to look:**
1. company press releases and SEC filings (EDGAR 8-K);
2. Yahoo Finance news;
3. Reuters or AP;
4. Federal Reserve and Treasury releases;
5. WInS research pages.

Always open the original article. A headline is not evidence.

**Signal levels.** The thresholds are **proposals; Pat confirms them**:

| Level | What triggers it | What you do |
|---|---|---|
| **RED** | For a held or shortlisted company: guidance cut, restatement, auditor resignation, new material weakness, fraud or regulator action, CEO/CFO sudden exit, dividend cut, merger announced, or a hit to its "prove us wrong" signal. **One-day price move of ±10% or more for a stock, or ±5% for an ETF.** Fed surprise. 10-year Treasury moves 0.25 points or more in a week. | **Message Pat the same day** with the link and two sentences on why it matters |
| **AMBER** | Earnings results; outlook changes; analyst rating changes; AI-spending announcements; inflation or jobs reports | Log it the same day |
| **GREEN** | Routine news | Log it in the weekly summary only |

**Outputs:**
- `signal_log.csv` (the template is in this folder), updated daily;
- a **one-page summary every Friday**:
  - the top 3 developments;
  - any RED items;
  - whether any thesis "prove us wrong" signal is getting closer.

## 3. Rules you must follow

1. **News is information, not a trade signal.** Nothing you log triggers a
   trade automatically. Pat decides. Under our rules, only a pre-written
   "prove us wrong" signal prompts a formal review.
2. **No guessing:**
   - every entry needs a date, a source link and the time you read it;
   - mark rumours "unconfirmed".
3. **Label everything:**
   - **Sourced:** a company, regulator or official release;
   - **Secondary:** news or data sites;
   - **Judgment:** your interpretation.
4. **Don't infer Laura's preferences** (sectors, ESG, risk tolerance, Taiwan)
   from her biography.
5. **AI use is allowed for summarizing and brainstorming**, but:
   - read the original yourself;
   - log each AI session (date, tool, what you asked, what you checked);
   - never submit AI-written text as the team's own;
   - never let AI write Trading Notes or reflections.
6. **Don't place trades.** One shared WInS account; only Pat trades.

## 4. Files in this folder

- `README.md`: this file.
- `watchlist.csv`: tickers and themes to monitor, and why each matters.
- `signal_log_template.csv`: the log columns.
- `ai_catch_up_prompt.md`: paste into your AI with this README attached.
