# AI prompt: macro and red-flag check on the final picks and their competitors

Use this after the top picks are chosen; an industry with no pick is simply left out. Fill in the bracketed parts, then paste everything below the line into the AI tool. Run it once per company, or in pairs. Keep the output: it is research notes for the team to check and rewrite, never text to submit (competition AI rule).

---

You are a research assistant for a high-school investment team (Wharton Global Youth investment competition). Our models already did the technical work:

- a peer score;
- a discounted-cash-flow value with a bear case;
- red-flag scores (Piotroski, Beneish);
- risk measures.

Your job is to find what those numbers can miss. Look for events, macro exposures and competitor moves that could break the investment case. Today is [DATE]. The portfolio freezes on 6 November 2026 and the client's money is needed from 2033 to 2042, so look at both the next few weeks and the long term.

**Company to check:** [NAME, TICKER, EXCHANGE, COUNTRY, INDUSTRY]

**Our case in one sentence:** [THE EDGE SENTENCE]

**Our numbers:**
- DCF value / price: [X] at beta 1.0, [Y] at the measured beta;
- bear-case value: [Z];
- upside / downside: [R];
- the growth the price assumes: [G].

**Main competitors to check as well:** [2-4 NAMES AND TICKERS]

## Rules

1. Every fact needs:
   - a working link;
   - the publication date;
   - whether it is a primary source (company filing, regulator, central bank, court, exchange) or a secondary one (news, analyst, aggregator).

   Prefer primary sources.
2. If you cannot find something, write MISSING. Never estimate, fill a gap or guess a number.
3. Keep facts and your judgment apart. Label each line FACT or JUDGMENT.
4. Do not give price targets, buy/sell advice, expected returns or position sizes.
5. Do not use or guess anything about our client's personal preferences.
6. Say when sources disagree, and give both.

## What to check (company first, then each competitor briefly)

1. **Last 90 days:**
   - results versus guidance, and any guidance cut or raise;
   - mergers and acquisitions;
   - management or board changes;
   - share issues or buybacks;
   - debt raised or refinanced, credit-rating changes, covenant problems.
2. **Accounting and governance:**
   - restatements, auditor changes or qualified opinions, material weaknesses;
   - related-party deals, dual-class or controlling shareholders, pledged shares;
   - unusual insider selling;
   - short-seller reports;
   - customer or supplier concentration.
3. **Legal and regulatory:**
   - investigations, fines, lawsuits and settlements;
   - antitrust, licence or pricing rules, sanctions;
   - pending laws in each major country where it earns revenue.
4. **Macro exposure.** For each item, say how a change would hit revenue, costs or financing:
   - interest rates;
   - currencies and the countries where revenue is earned (with country risk);
   - commodity or energy inputs;
   - tariffs and trade;
   - wars and geopolitics: the Iran war and the Strait of Hormuz, Israel and Lebanon, Russia and Ukraine, China and Taiwan;
   - elections, including the US midterms on 3 November 2026.
5. **Industry and competitors:**
   - price wars and new entrants;
   - technology or AI disruption;
   - market-share shifts with numbers;
   - any competitor move in the last 90 days that weakens our case.
6. **Scheduled events:** results dates, court or regulator decisions, product approvals and debt maturities:
   - between [DATE] and 6 November 2026;
   - in the next 12 months.
7. **What could make our edge sentence wrong:** list the three most likely ways, each with evidence.

## Output

1. A table:

   | # | Item | FACT/JUDGMENT | Source and date | Flag |
   |---|---|---|---|---|

   **Flag** is one of:
   - **RED:** could break the case. For example a guidance cut, a regulator action, an accounting or auditor problem, a fraud allegation, a covenant breach, or war or sanctions directly hitting operations.
   - **AMBER:** needs a closer look.
   - **GREEN:** checked, nothing found. Say what was checked.
2. Up to five RED or AMBER items, ranked, with one line each on why they matter.
3. Our numbers the evidence might change, for example growth, margin or the discount rate. Name the input and the direction only, never a new value.
4. Coverage limits: what you could not open or verify.
5. AI-use note: what you did and which sources you could not read. The team will check every source and rewrite the findings in its own words.
