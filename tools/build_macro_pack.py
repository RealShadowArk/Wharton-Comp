"""Macro and red-flag check pack (4 Nov 2026): prompt, one context card per passing company, macro facts.

Run: python tools/build_macro_pack.py  -> handoff/macro_redflags_2026-11-04/ (+ zip)
Numbers come from outputs/round2/Round2_scorecard*.md (TEST previews, 30 Oct prices). The cards describe
what our model assumes; they are not investment theses (Pat writes those in his own words).
"""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "handoff" / "macro_redflags_2026-11-04"

# ticker: (name, trade listing, HQ country, industry, tier, price 30 Oct, value/price at beta 1.0 / 5y / full,
#          bear/price, upside:downside, price-implied growth shift, cash check, red flags, max position, caveats, competitors, exposures to check)
C = {
 "ADBE": ("Adobe", "Nasdaq: ADBE", "US", "Software", "Clean", "$250.23", "1.58 / 1.27 / 1.26", "1.04", "no downside", "-6.3", "0.95", "7/9, -2.86", "$11,636",
          "none found by the model", "Figma (FIG), Canva (private), Microsoft (MSFT)", "AI image and design tools; pricing of Creative Cloud; enterprise seat counts"),
 "TCOM": ("Trip.com Group", "Nasdaq: TCOM (or HKEX: 9961)", "China", "Internet and digital platforms", "Clean", "RMB 265.17 (valued in RMB)", "2.11 / n/a / 1.97", "1.43", "no downside", "-12.0", "0.80", "7/9, -1.89", "$10,258",
          "China country risk premium included; 2025 profit includes RMB 19.4bn of one-off gains", "Booking (BKNG), Expedia (EXPE), Meituan (3690.HK), Tongcheng Travel (0780.HK)", "China regulation, US-China delisting or sanctions risk, outbound travel demand, RMB"),
 "SAN.PA": ("Sanofi", "Euronext Paris: SAN (ADR SNY)", "France", "Pharmaceuticals", "Clean", "EUR 79.74", "1.35 / 2.69 / 1.81", "0.95", "7.45", "-3.6", "0.73", "6/9, -2.60", "$21,517",
            "M12 9th of 14 (advisory)", "AbbVie (ABBV), Eli Lilly (LLY), GSK (GSK)", "Dupixent patent and competition, US drug-pricing rules and tariffs on pharma imports, pipeline readouts"),
 "G": ("Genpact", "NYSE: G", "US (Bermuda-incorporated; delivery mainly India)", "IT services", "Clean", "$39.62", "1.62 / 2.38 / 1.64", "1.04", "no downside", "-6.1", "0.80", "8/9, -2.73", "$13,036",
       "M12 5th of 17", "Accenture (ACN), EXL Service (EXLS), Cognizant (CTSH)", "AI automation of outsourced work, India costs and rupee, US visa or outsourcing rules"),
 "EEFT": ("Euronet Worldwide", "Nasdaq: EEFT", "US (operations mainly Europe)", "Payments", "Clean", "$63.15", "3.32 / 3.50 / 2.66", "2.29", "no downside", "-12.5", "0.87", "8/9, -2.50", "$9,185",
          "dilution MISSING (convertible notes counted as debt); capex net of sale proceeds; M12 not scored", "Western Union (WU), Wise (WSE), Remitly (RELY), NCR Atleos (NATL)", "European ATM fee rules, cash usage decline, remittance taxes, euro"),
 "DECK": ("Deckers Outdoor (HOKA, UGG)", "NYSE: DECK", "US", "Consumer brands", "Clean", "$81.99", "1.54 / 1.46 / 1.60", "1.11", "no downside", "-7.1", "0.92", "5/9, -2.62", "$8,471",
          "Piotroski 5/9", "Nike (NKE), On Holding (ONON), Birkenstock (BIRK)", "US tariffs on footwear made in Vietnam and China, HOKA growth slowdown, consumer demand"),
 "WKL.AS": ("Wolters Kluwer", "Euronext Amsterdam: WKL", "Netherlands", "Exchanges and data", "Clean", "EUR 87.00", "1.42 / 2.04 / 1.61", "0.98", "21.59", "-4.0", "1.08", "6/9, -2.71", "$14,924",
            "2025 operating income includes a disposal gain (amount MISSING); capex is a combined line", "RELX (REL.L), Thomson Reuters (TRI)", "AI tools replacing professional information products (legal, tax, health), euro, US healthcare spending"),
 "CTSH": ("Cognizant", "Nasdaq: CTSH", "US (delivery mainly India)", "IT services", "Mild caveat", "$65.11", "1.45 / 1.61 / 1.24", "1.08", "no downside", "-5.4", "1.13", "6/9, -2.50", "$12,824",
          "cash check 1.13; tax set at 25% (team decision); M12 8th of 17", "Accenture (ACN), Infosys (INFY), TCS (TCS.NS)", "AI automation, India costs and rupee, US H-1B and outsourcing rules, client budgets"),
 "DOX": ("Amdocs", "Nasdaq: DOX", "US/Guernsey (large R&D base in Israel)", "IT services", "Mild caveat", "$62.83", "1.49 / 2.48 / 1.34", "1.12", "no downside", "-5.4", "1.19", "6/9, -2.71", "$8,440",
         "cash check 1.19; FY2026 (Sep) ended before 30 Oct, so the forecast starts at FY2027; low 5-year beta (0.42)", "CSG Systems (CSGS), Netcracker (NEC), Oracle Communications (ORCL)", "Israel war (staff and operations), telecom client spending, AI coding tools"),
 "OTEX": ("Open Text", "Nasdaq: OTEX (TSX: OTEX)", "Canada", "Software", "Mild caveat", "$26.59", "3.19 / 3.24 / 2.82", "2.60", "no downside", "-10.2", "1.26", "9/9, -2.48", "$16,719",
          "cash check 1.26; debt $5.8bn against a $6.4bn market cap; revenue guided down 1.7% in FY2027", "Microsoft (MSFT), IBM (IBM), Box (BOX)", "debt refinancing and ratings, shrinking legacy revenue, divestitures, AI document tools"),
 "PYPL": ("PayPal", "Nasdaq: PYPL", "US", "Payments", "Mild caveat", "$57.01", "1.93 / 1.60 / 1.69", "1.39", "no downside", "-8.8", "1.16", "8/9, -2.54", "$9,641",
          "counts all corporate cash; the uniform bear case is too mild; M12 3rd", "Apple (Apple Pay), Block (XYZ), Stripe (private), Adyen (ADYEN.AS)", "branded checkout share, regulation of payments and stablecoins, consumer credit losses"),
 "LULU": ("Lululemon", "Nasdaq: LULU", "US/Canada", "Consumer brands", "Strong caveat (alternate)", "$107.24", "1.50 / 1.66 / 1.19", "1.18", "no downside", "-6.5", "1.60", "6/9, -1.91", "$7,206",
          "cash check 1.60 (0.92x on 2025 reported cash flow); revenue guided down 5-7%", "Nike (NKE), adidas (ADS.DE), Alo and Vuori (private)", "US tariffs, US demand, competition in athleisure"),
 "ADS.DE": ("adidas", "Xetra: ADS", "Germany", "Consumer brands", "Strong caveat (alternate)", "EUR 168.55", "1.60 / 1.44 / 1.40", "1.15", "no downside", "-6.2", "at least 4.1", "6/9, -2.26", "$11,668",
            "2025 operating cash flow EUR 751m vs 2,910m in 2024; stock pay and dilution MISSING", "Nike (NKE), Puma (PUM.DE), On Holding (ONON)", "US tariffs, inventory, euro, sports-event cycle"),
 "ZBH": ("Zimmer Biomet", "NYSE: ZBH", "US", "Medtech", "Strong caveat (alternate)", "$94.52", "1.22 / 1.95 / 1.45", "0.90", "2.36", "-2.0", "1.39", "7/9, -2.53", "$15,426",
         "cash check 1.39 (0.74x on reported cash flow)", "Stryker (SYK), Johnson & Johnson (JNJ), Smith & Nephew (SN.L)", "joint-replacement volumes, hospital pricing, China volume-based procurement"),
 "RKT.L": ("Reckitt", "London: RKT", "UK", "Consumer brands", "Strong caveat (alternate)", "GBP 54.08", "1.26 / 2.19 / 1.89", "0.94", "4.46", "-2.7", "1.72", "7/9, -2.42", "$17,283",
           "cash check 1.72 (0.57x on reported cash flow); Essential Home disposal", "Haleon (HLN), Procter & Gamble (PG), Unilever (ULVR.L)", "infant-formula (NEC) litigation, disposal proceeds, sterling"),
 "NRG": ("NRG Energy", "NYSE: NRG", "US", "Power", "Strong caveat (alternate)", "$96.06", "1.81 / 1.50 / 1.88", "1.23", "no downside", "-4.1", "MISSING", "6/9, -2.49", "$10,904",
         "passes only with reported D&A (0.99x with D&A = capex); 2025 pro forma with the LS Power plants", "Vistra (VST), Constellation (CEG), Talen (TLN)", "Texas and PJM power prices, capacity auctions, gas prices, data-centre demand"),
 "NVDA": ("NVIDIA", "Nasdaq: NVDA", "US", "Semiconductors", "Strong caveat (alternate)", "$204.64", "2.00 / 1.03 / 1.10", "0.63", "2.70", "-10.7", "1.19", "4/9, -1.17 (Beneish flag)", "$7,247",
          "Beneish -1.17 above the -1.78 flag line (mostly 65% revenue growth); already a top-10 VOO holding", "AMD (AMD), Broadcom (AVGO), Google TPUs (GOOGL)", "export controls to China, hyperscaler capex, TSMC and Taiwan supply"),
 "2454.TW": ("MediaTek", "Taiwan: 2454", "Taiwan", "Semiconductors", "Strong caveat (alternate)", "TWD 3,915", "3.30 / 1.50 / 2.67", "0.81", "12.23", "-17.5", "0.65", "4/9, -2.51", "$12,529",
             "value depends on consensus growth of 77% and 69% in years 2-3; price nearly tripled in 2026", "Qualcomm (QCOM), Broadcom (AVGO), Marvell (MRVL)", "China-Taiwan tension, AI ASIC contracts, smartphone cycle, TWD"),
 "005930.KS": ("Samsung Electronics", "Korea: 005930", "South Korea", "Semiconductors", "Strong caveat (alternate)", "KRW 225,000", "1.46 / 1.07 / 1.28", "0.67", "1.39", "-6.1", "MISSING", "6/9, -2.64", "$14,664",
               "value depends on consensus revenue growth of 117% next year (memory boom); stock pay MISSING", "SK Hynix (000660.KS), Micron (MU)", "memory price cycle, HBM qualification, Korea politics, KRW, export controls"),
 "0700.HK": ("Tencent", "HKEX: 0700", "China", "Internet and digital platforms", "Screened out as bank-like unless Pat overrules", "HKD 383.6 (RMB 325.68)", "1.34 / 2.95 / 1.43", "0.78", "1.56", "-3.6", "0.90", "8/9, -2.61", "$24,544",
             "loan receivables inside operating cash flow; China country risk premium included", "NetEase (NTES), ByteDance (private), Alibaba (BABA)", "China regulation (games, fintech), US investment restrictions, RMB"),
 "PDD": ("PDD Holdings (Temu, Pinduoduo)", "Nasdaq: PDD (ADR)", "Ireland/China", "Internet and digital platforms", "Screened out as bank-like unless Pat overrules", "$78.61 per ADS", "2.27 / n/a / 3.03", "1.50", "no downside", "-12.8", "MISSING", "5/9, -2.10", "$8,930",
         "merchant deposits inside operating cash flow; China country risk premium included", "Alibaba (BABA), JD.com (JD), Shein (private), Amazon (AMZN)", "US de minimis and tariff rules on Temu, EU rules, China regulation, accounting transparency"),
}

PROMPT = """# Macro and red-flag check before trading (prompt, 4 Nov 2026)

**How to use (Pat):**
1. For each company you plan to buy, open its card in `companies/` and paste it where the prompt says. Attach `macro_context.md` too. Run one company per chat (two at most): big batches make AI tools skip checks.
2. Run the portfolio prompt at the bottom once, with your final list and sizes.
3. Save each output as `results/<TICKER>.md`. Open every source the AI cites and rewrite the findings in your own words (competition AI rule: "work generated by an AI program may not be submitted as the team's own").
4. A RED flag means stop and look before buying. An AMBER flag goes in your trade note.

Core companies (clean and mild caveat): ADBE, TCOM, SAN.PA, G, EEFT, DECK, WKL.AS, CTSH, DOX, OTEX, PYPL. Alternates have cards too.

---

You are a research assistant for a high-school investment team (Wharton Global Youth investment competition). Our models already did the technical work:
- a peer score (M12);
- a discounted-cash-flow value with a bear case;
- red-flag scores (Piotroski, Beneish);
- risk measures.

Your job is to find what those numbers can miss: events, macro exposures and competitor moves that could break the case. Today is 4 November 2026. The portfolio freezes on 6 November 2026. The client's money is needed from 2033 to 2042, so look at both the next few days and the long term.

**Company card (what our model assumes):**
[PASTE THE COMPANY CARD HERE]

**Background facts the team has already sourced:** see the attached `macro_context.md`. Use them as a starting point only: check whether anything has changed since.

## Rules

1. Every fact needs a working link, the publication date, and whether it is a primary source (company filing, regulator, central bank, court, exchange) or a secondary one (news, analyst, aggregator). Prefer primary sources.
2. If you cannot find something, write MISSING. Never estimate, fill a gap or guess a number.
3. Label each line FACT or JUDGMENT.
4. No price targets, buy or sell advice, expected returns or position sizes.
5. Do not use or guess anything about our client's personal preferences.
6. When sources disagree, give both.

## What to check (company first, then each listed competitor briefly)

1. **Since 30 October 2026** (our prices are from 30 Oct): results, guidance changes, profit warnings, M&A, management changes, credit-rating actions, and the share-price move. Anything that changes the card's numbers?
2. **Last 90 days:** results versus guidance; buybacks or share issues; debt raised or refinanced; covenant problems.
3. **Accounting and governance:** restatements, auditor changes or qualified opinions, material weaknesses, related-party deals, controlling shareholders, unusual insider selling, short-seller reports, customer concentration.
4. **Legal and regulatory:** investigations, fines, lawsuits, antitrust, sanctions, export controls, tariffs, pending laws in its main countries.
5. **Macro exposure** (say how each would hit revenue, costs or financing): interest rates; currencies and country risk; commodities and energy; tariffs and trade; wars and geopolitics (the Iran war and the Strait of Hormuz, Israel and Lebanon, Russia and Ukraine, China and Taiwan); the result of the US midterms on 3 November 2026.
6. **The card's caveats and exposures:** check each one listed on the card specifically.
7. **Competitors:** price wars, new entrants, AI disruption, market-share shifts with numbers, and any competitor move in the last 90 days that weakens our case.
8. **Scheduled events:** results dates, court or regulator decisions, product approvals and debt maturities, from now to 6 November 2026 and over the next 12 months.
9. **What could make our model wrong:** the three most likely ways, each with evidence. Name the model input it would change (growth, margin, discount rate, cash, debt) and the direction only.

## Output

1. A table: `| # | Item | FACT/JUDGMENT | Source and date | Flag |`, where Flag is:
   - **RED:** could break the case. For example: a guidance cut, a regulator action, an accounting problem, a fraud allegation, a covenant breach, war or sanctions hitting operations.
   - **AMBER:** needs a closer look.
   - **GREEN:** checked, nothing found. Say what was checked.
2. Up to five RED or AMBER items, ranked, with one line each on why they matter.
3. Model inputs the evidence might change (input and direction only).
4. Coverage limits: what you could not open or verify.
5. AI-use note: what you did and which sources you could not read.

---

## Portfolio prompt (run once, after the company checks)

You are a research assistant for the same team. Here is our planned list of individual stocks with dollar amounts: [PASTE NAMES, TICKERS AND AMOUNTS]. The rest of the account holds US and international index ETFs (VOO, VXUS), four sector ETFs (XLI, XLK, XLV, XLF) and a Treasury bond ladder for payments from 2033 to 2042.

Using the attached company cards and `macro_context.md`, and the same rules as above (sources, FACT/JUDGMENT labels, MISSING, no advice), report:
1. Shared exposures across the list: countries (China, India, Israel, Taiwan), currencies, industries (for example several IT-services names), and common drivers (AI disruption, tariffs, consumer demand, interest rates).
2. Overlap with the ETFs: which picks are large holdings of VOO or the sector ETFs (we hold Nvidia through VOO already).
3. Events between now and 6 November 2026 that hit several names at once.
4. Up to five portfolio-level RED or AMBER items, ranked.
"""

MACRO = """# Macro facts already sourced by the team (as of 30 Oct - 3 Nov 2026)

Use these as a starting point; check what has changed. Labels: RESEARCH = sourced by the team; see the repo files named for links.

| Item | Value | Label and source |
|---|---|---|
| US 10-year Treasury yield, 30 Oct 2026 | 4.94% | RESEARCH: US Treasury par yield curve (team research compilation, 2 Nov) |
| US 3-month T-bill, 30 Oct 2026 | 4.00% | RESEARCH: FRED DTB3 (read by Pat) |
| German 10-year (euro rate), 30 Oct 2026 | 3.34% | RESEARCH: team decision 3 Nov |
| UK 10-year gilt, 30 Oct 2026 | 5.29% | RESEARCH: new-candidates Round 2 workbook |
| China 10-year, 30 Oct 2026 | 1.63% | RESEARCH: Akshat's source; China country risk premium 0.91% (Damodaran, Jan 2026) |
| India 10-year, 30 Oct 2026 | 7.40% | RESEARCH: team decision 3 Nov |
| Israel country risk premium | 2.07% | RESEARCH: Damodaran page dated 5 Jan 2026 |
| EUR/USD, 30 Oct 2026 | about 1.116-1.121 | RESEARCH: researchers' FX sources (Federal Reserve, Yahoo) |
| Iran war | Began 28 Feb 2026; Israel shut the Leviathan and Karish gas fields that day (Leviathan restarted about 2-3 Apr); a ceasefire of 7 Apr collapsed 7-8 Jul per a secondary tracker; tanker war since September; no ceasefire in force as of 1 Nov; on 31 Oct an Iranian official said no talks and no reopening of Hormuz until the US accepts Iran's demands | RESEARCH: `context/teammates_2026-11-02/aryu_reviewed/KENON_option1_2026-11-02.md` (Times of Israel, Bloomberg, Argus, tracker) |
| US politics | Midterm elections on 3 Nov 2026 (results not yet in our files) | CASE: calendar |
| PJM capacity prices | $329.17/MW-day (2026/27), $333.44 (2027/28), $325.00 (2028/29); the July 2026 auction cleared at the cap | RESEARCH: OPC H1 2026 report, PJM |

Not in our files (check fresh): the US midterm results, tariff decisions since 30 Oct, central-bank meetings in November, China-Taiwan and Korea developments, and any market moves since 30 Oct.
"""


def card(t, v):
    (name, listing, country, ind, tier, price, vp, bear, ud, shift, cash, rf, cap, cav, comp, exp) = v
    return f"""# {name} ({t})

- **Listing to trade:** {listing}. **Headquarters / main country:** {country}. **Industry:** {ind}.
- **Tier in our list:** {tier}.
- **Price used (30 Oct 2026 close):** {price}.
- **Our DCF value / price** at beta 1.0, the 5-year beta and the full-history beta: {vp}. Bear case / price: {bear}. Upside : downside: {ud}.
- **What the price implies:** revenue growth about {shift.lstrip('-')} percentage points a year below the analyst-consensus path our model uses (margins held at the latest full-year level).
- **Cash check** (model cash flow / reported cash flow; above about 1.10 the model is generous): {cash}.
- **Red flags:** Piotroski, Beneish = {rf} (Beneish above -1.78 is a flag).
- **Position limit** ($6,000 / worst calendar-year loss in USD): {cap}.
- **Model caveats:** {cav}.
- **Exposures to check:** {exp}.
- **Main competitors to check:** {comp}.

Source of these numbers: the team's Round 2 scorecards in `outputs/round2/` (TEST previews, not facts about the future).
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "companies").mkdir(parents=True)
    (OUT / "results").mkdir()
    (OUT / "README_prompt.md").write_text(PROMPT, encoding="utf-8")
    (OUT / "macro_context.md").write_text(MACRO, encoding="utf-8")
    (OUT / "results" / "README.md").write_text("Save one file per company here: <TICKER>.md (the AI output, then your own rewrite).\n", encoding="utf-8")
    for t, v in C.items():
        (OUT / "companies" / f"{t}.md").write_text(card(t, v), encoding="utf-8")
    z = OUT.parent / "macro_redflags_2026-11-04.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                f.write(p, p.relative_to(OUT.parent))
    print(len(C), "cards ->", z)


if __name__ == "__main__":
    main()
