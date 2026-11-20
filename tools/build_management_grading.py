"""Management grading workbooks for the 12 finalists (20 Nov 2026).

    python tools/build_management_grading.py

Writes handoff/management_grading_2026-11-20/: one master workbook (all 12) and one per grader.
Evidence lines and sources are copied from the teammates' Round 2 workbooks (19 Nov). Grades and
reasons are left blank: they are the team's own judgments (competition AI rule). The scale is a
DRAFT for Pat to approve.
"""
import re
from pathlib import Path

import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "context/teammates_2026-11-19"
OUT = ROOT / "handoff/management_grading_2026-11-20"
SRC = {"package1/Wharton_Package1_Round2_v2.xlsx": ["CMCSA", "TMUS"],
       "package2/Wharton_Package2_Consumer_Round2_v2.xlsx": ["LULU", "DECK"],
       "package3/Wharton_Package3_Financials_and_REITs_v2.xlsx": ["ACGL", "EG", "FISV", "VICI", "O"],
       "package4/Wharton_Package4_Healthcare_Industrials_v2.xlsx": ["CI", "LDOS"],
       "partB/Wharton_Package_5_Part_B_Round_2_v2.xlsx": ["EXE"]}
ITEMS = [("cap", "Capital allocation"), ("guid", "Guidance record"), ("gov", "Governance"), ("con", "Controversies and legal")]
KEYS = [("cap", r"(?i)^capital allocation"), ("guid", r"(?i)^guidance (record|track)"), ("gov", r"(?i)^governance"),
        ("con", r"(?i)^controvers|^legal"), ("sub", r"(?i)substitut|replace"), ("ai", r"(?i)^ai\b")]
TABLE = r"(?i)quarterly (issuer )?guidance|guidance record by|management guidance ·|quarterly guidance evidence|eight[- ]quarter"
URL = re.compile(r"https?://[^\s|,;)]+")

# Proposed split (Pat 20 Nov: Pat grades 4, everyone else 2), by the packages each person worked on. Edit and re-run to change.
GRADERS = {"Pat": ["ACGL", "EG", "FISV", "VICI"], "Akshaj R": ["CMCSA", "TMUS"], "Akshaj P": ["LULU", "DECK"],
           "Akshath": ["CI", "LDOS"], "Aryu": ["EXE", "O"]}
ORDER = ["ACGL", "CI", "DECK", "EG", "LDOS", "TMUS", "VICI", "CMCSA", "EXE", "FISV", "LULU", "O"]

# Context from docs/finalists_2026-11-19.md (TEST): strategies, value/price at beta 1.0 / 5-year / full, alpha and beta vs industry, M12
SNAP = {
    "ACGL": ("Arch Capital Group", "Both", "1.15 / 1.37 / 1.32 (residual income)", "+17.2% vs +13.0%", "0.23 vs 0.34", "84.7"),
    "CI": ("The Cigna Group", "Both", "1.87 / 3.99 / 2.11", "+6.5% vs +4.8%", "0.33 vs 0.73", "63.5"),
    "DECK": ("Deckers Outdoor (held)", "Both", "1.54 / 1.46 / 1.60", "+0.6% vs -0.6%", "1.08 vs 1.22", "89.2"),
    "EG": ("Everest Group", "Both", "1.14 / 1.35 / 1.28 (residual income)", "+8.0% vs +5.7%", "0.24 vs 0.77", "72.7"),
    "LDOS": ("Leidos Holdings", "Both", "1.63 / 2.40 / 2.06", "+5.3% vs +3.5%", "0.59 vs 1.11", "69.3"),
    "TMUS": ("T-Mobile US", "Both", "1.81 / 3.17 / 2.46", "+2.8% vs +2.5%", "0.42 vs 0.97", "50.0"),
    "VICI": ("VICI Properties", "Both", "1.43 / 1.92 / 1.58 (FFO)", "-5.2% vs -7.4%", "0.74 vs 1.06", "79.8"),
    "CMCSA": ("Comcast", "Ours only", "3.54 / 4.37 / 3.68", "-17.2% vs +2.5%", "0.88 vs 0.97", "56.2"),
    "EXE": ("Expand Energy", "Ours only", "1.62 / 2.84 / 3.07", "+9.7% vs +16.5%", "0.37 vs 0.38", "61.2"),
    "FISV": ("Fiserv", "Ours only", "4.19 / 4.67 / 4.50", "-15.3% vs -11.0%", "0.83 vs 1.08", "58.0"),
    "LULU": ("Lululemon Athletica", "Ours only", "1.50 / 1.66 / 1.19", "-30.1% vs -0.6%", "0.81 vs 1.22", "80.1"),
    "O": ("Realty Income", "Ours only", "1.34 / 1.81 / 2.14 (FFO)", "-5.9% vs -2.6%", "0.79 vs 1.01", "54.8"),
}
FLAGS = {
    "ACGL": ["Piotroski and Beneish not applied (insurer).", "Staggered board; bye-laws can cap a large US holder's votes."],
    "CI": ["FTC insulin-rebate settlement requires Express Scripts to change pricing and rebate practices.",
           "Price fell 8.45% (30 Oct to 19 Nov) in a managed-care selloff after CMS proposed broader Medicare Advantage audits.",
           "Tangible common equity is negative (-$31.8bn): the 2018 Express Scripts deal left $38.4bn of goodwill."],
    "DECK": ["Two proposed consumer class actions over tariff-related pricing (October 10-Q).",
             "Piotroski 5/9, the lowest of the finalists (not a formal red flag: the line is below 4)."],
    "EG": ["$751m of adverse prior-year reserve development in FY2025: reserves for past claims had to be raised.",
           "Missed analysts' operating EPS estimates in 5 of 8 quarters."],
    "LDOS": ["DOJ Antitrust Division criminal investigation and grand jury subpoena over three federal procurements; liability not estimable.",
             "3 Nov: Q3 revenue miss and flat FY2027 earnings signalled; FY2026 revenue range cut after the SES/Industrial Automation JV closed, while EPS and cash-flow guidance were raised (price -12.7% to 19 Nov)."],
    "TMUS": ["Deutsche Telekom holds about 55.9% of the votes and its CEO chairs the board.",
             "$350m paid under the 2021 cyberattack class settlement; possible further losses from agency inquiries.",
             "Leverage rose (Piotroski fail)."],
    "VICI": ["None found in the evidence (ordinary-course claims only).", "Listed only since 2018, so its risk history is short."],
    "CMCSA": ["Brian Roberts' Class B shares hold 33 1/3% of the votes, with separate approval rights.",
              "$117.5m Xfinity data-breach settlement (2023 incident), approved August 2026.",
              "Beneish score relies on our mapping of its expense lines (ASSUMPTION)."],
    "EXE": ["Beneish -1.98, close to the -1.78 flag line (not flagged).", "Issued new shares (Piotroski fail); legacy Chapter 11 claims still being reconciled."],
    "FISV": ["Consolidated securities class action plus SEC and SDNY information requests about its 2025 earnings guidance.",
             "Cut FY2025 organic growth guidance from about 10% to 3.5-4.0% (Oct 2025); shares fell 67.3% in 2025."],
    "LULU": ["Federal securities complaint (2 Nov 2026) alleging misstatements about the turnaround and demand.",
             "Revenue guided down 5-7% for FY2026.", "Beneish -1.91, the closest of the finalists to the -1.78 line (not flagged)."],
    "O": ["None found in the evidence (ordinary-course claims only)."],
}
GENERIC = {
    "cap": "- Are buybacks and dividends paid from free cash flow, or from new debt?\n- At what prices were shares bought back?\n"
           "- Have past acquisitions paid off, or led to write-downs?\n- Is debt kept within the company's own target?\n- Is enough reinvested to keep the business competitive?",
    "guid": "- Over the last 8 quarters, how often did results beat, meet or miss the company's OWN guidance?\n- Were there guidance cuts during the year, and how big?\n"
            "- Is the guidance specific (numbers) or vague?\n- Did management explain misses honestly?\n"
            "- Careful: beats against ANALYSTS' estimates are not the same as beats against the company's guidance. Apply the team rule (Start here) when issuer guidance is MISSING.",
    "gov": "- Is the chair independent of the CEO, or is there a strong lead independent director?\n- One share, one vote? Is there a controlling holder or super-voting class?\n"
           "- Related-party dealings, relatives on the payroll, pledged shares?\n- Entrenchment devices (staggered board, voting caps)?\n- Is pay tied to performance?",
    "con": "- Any regulator or criminal investigation (DOJ, SEC, FTC)? What could it cost?\n- Class actions (securities, consumer): size relative to the company?\n"
           "- Data breaches, product safety, accounting restatements?\n- Ordinary-course litigation, or a threat to the business or its reputation?",
}
SPECIFIC = {
    "ACGL": {"cap": "FY2025 buybacks of $1,923m and a $5 special dividend in FY2024: paid from earnings? At what price relative to book value?",
             "guid": "Arch gives no issuer guidance; the evidence is 7 beats and 1 miss against analysts. Apply the team rule.",
             "gov": "Staggered board and a bye-law cap on large US holders' votes: how much do they reduce shareholders' say?",
             "con": "The ERISA class settlement (2 Nov 2026) is resolved. Anything open beyond ordinary insurance disputes?"},
    "EG": {"cap": "$1,200m of buybacks in 9M 2026, in the same period reserves were strengthened: prudent?",
           "guid": "No issuer guidance; against analysts it missed 5 of 8 quarters. Apply the team rule. What do the misses say?",
           "gov": "Independent chair, annual elections and majority voting, but a 9.9% voting-power cap in the bye-laws. Net effect?",
           "con": "$751m adverse reserve development (FY2025): a one-off clean-up, or a sign earlier reserves were too thin? It is not a lawsuit, but it bears on management's judgment."},
    "FISV": {"cap": "Buybacks restart with $500m in Q4 2026 after the 2025 reset: sensible use of cash, or too early?",
             "guid": "One large cut (FY2025 organic growth ~10% to 3.5-4.0%), then FY2026 reaffirmed at -1% to 0%. How heavily should one large cut weigh?",
             "gov": "All 11 directors on one-year terms; a shareholder proposal asked for an independent chair. Who chairs now?",
             "con": "Securities class action and SEC/SDNY requests about the 2025 guidance: possible cost? Linked to the guidance item?"},
    "VICI": {"cap": "New $500m term loan and partial redemption of 2027 notes. How is growth funded (debt or new shares), and is leverage within target? What share of rent comes from the largest tenants (10-K)?",
             "guid": "AFFO guidance met in FY2024, beaten in FY2025, FY2026 range raised. Any quarter missed?",
             "gov": "New independent director (regulatory approval pending). Chair and CEO roles? Say-on-pay result?",
             "con": "Only ordinary-course claims. Any tenant disputes or rent deferrals in the 10-Q?"},
    "O": {"cap": "New hyperscale data-center platform with Cloud Capital: sensible extension, or drifting from its core? How are acquisitions funded (new shares dilute holders)?",
          "guid": "AFFO within range in FY2024, beat in FY2025, FY2026 raised. Consistent over 8 quarters?",
          "gov": "Independent non-executive chair, all other nominees independent, no related-party transactions. Anything negative?",
          "con": "Only ordinary-course claims. Anything else in the 10-Q?"},
    "CMCSA": {"cap": "Buybacks paused from Q3 2026 ahead of the NBCUniversal/Sky separation. Will the separation create value? How did past deals (Sky, 2018) work out?",
              "guid": "No numeric company guidance in 8 quarters; adjusted EPS beat analysts 8 of 8. Apply the team rule.",
              "gov": "Brian Roberts (chair and co-CEO) controls 33 1/3% of the votes through Class B; family members are employed. How much does that limit outside shareholders?",
              "con": "$117.5m data-breach settlement (2023 incident): contained, or part of a pattern?"},
    "TMUS": {"cap": "$2.4bn buybacks and $1.1bn dividends in Q3 within an $18.2bn programme, with about $86bn of debt: paid from free cash flow?",
             "guid": "Company EBITDA guidance met in FY2024 and beaten in FY2025; quarterly EPS beat analysts 7 of 8. Apply the team rule for the quarterly part.",
             "gov": "Deutsche Telekom has about 55.9% of the votes and its CEO chairs the board; there are affiliate transactions. Stable owner, or a risk for minority holders?",
             "con": "$350m cyberattack settlement, $150m extra security spend, possible agency losses: has security improved?"},
    "LULU": {"cap": "$330m buybacks in Q2 FY2026 plus $118.8m in August, while revenue is guided down 5-7%: good timing?",
             "guid": "Beat its own revenue range in 6 of 8 quarters; missed Q2 FY2025 and Q2 FY2026. Is the recent trend worse?",
             "gov": "A cooperation agreement with founder Chip Wilson added a director. What was the dispute, and is it settled?",
             "con": "Federal securities complaint (2 Nov 2026) about the turnaround: early stage; how serious?"},
    "DECK": {"cap": "$637.5m buybacks in H1 FY2027 and a $3.5bn authorization increase: paid from cash flow? At what price?",
             "guid": "3 sales beats and 1 miss in 4 comparable quarters, 4 EPS beats, both year-end releases beat the annual guide; 2 quarters had no comparable guidance.",
             "gov": "Independent chair, one share one vote; a director's child was paid over $120,000 (director recused). Material?",
             "con": "Two proposed tariff-pricing class actions plus IP cases (Quince appeal, UK): serious or routine?"},
    "CI": {"cap": "Buybacks cut from about $2.6bn to about $500m (9M 2026): why? Express Scripts (2018) left $38.4bn of goodwill: has it paid off?",
           "guid": "See the eight disclosures and outcomes table below; note the FY2026 medical cost ratio guide after Q3.",
           "gov": "10 of 12 nominees independent, lead independent director, one share one vote, no related-person transactions. Anything negative?",
           "con": "FTC insulin-rebate settlement (pricing changes at Express Scripts) and the proposed Medicare Advantage audits: how much could they change the business?"},
    "LDOS": {"cap": "$2.4bn cash for Entrust (grid modernization) and $766m buybacks in 9M FY2026, while guidance was cut: sensible mix?",
             "guid": "FY2025 beat its EPS, margin and cash-flow guides; FY2026 raised twice, then the revenue range cut after the JV closed (EPS raised). Structural or a real miss? See the eight-quarter table.",
             "gov": "Independent chair separate from the CEO; jobs approved for two relatives of former executives. Material?",
             "con": "DOJ criminal antitrust investigation over three federal procurements, liability not estimable, DCAA audits open: how serious for a government contractor?"},
    "EXE": {"cap": "Twin Eagle acquisition (16 Sep 2026) and about $900m of buybacks this year: paid from cash flow? How did the 2024 Southwestern merger work out?",
            "guid": "Production above the guidance midpoint in 7 of 8 quarters (Q1 2026 just under, within range). Production is one guide: check capex guidance too.",
            "gov": "8 of 9 nominees independent; related-party review policy. Any legacy issues from the Chesapeake bankruptcy?",
            "con": "Ordinary-course claims and legacy Chapter 11 claims. Any environmental or royalty-owner litigation?"},
}
SCALE = {
    "cap": ("Value-destroying: large write-downs from past deals, buybacks funded with debt at high prices, dividend cut after over-promising, leverage far above target.",
            "Ordinary or mixed: sensible returns, but a questionable deal or rising debt; nothing alarming.",
            "Clearly value-creating: returns paid from free cash flow, deals with a record of paying off, debt within stated targets."),
    "guid": ("Repeated misses or large guidance cuts; guidance proved unreliable.",
             "Mostly met; one or two misses or a modest cut, clearly explained.",
             "Met or beat its own guidance nearly every quarter for 8 quarters, with no cuts."),
    "gov": ("Outside shareholders have little say (controlling holder or super-voting shares) plus related-party dealings or entrenchment.",
            "Some concerns (combined chair and CEO, staggered board, minor related-party employment) offset by independence elsewhere.",
            "Independent chair or strong lead director, one share one vote, no material related-party dealings, no entrenchment devices."),
    "con": ("An unresolved matter that could change the business or its reputation (criminal or regulator investigation, large securities claim, major breach).",
            "A notable but contained matter (settled class action, modest fine) unlikely to change the business.",
            "Only ordinary-course claims."),
}

ARIAL = "Arial"
F = lambda **k: Font(name=ARIAL, size=k.pop("size", 10), **k)
YELLOW = PatternFill("solid", fgColor="FFFF00")
GREY = PatternFill("solid", fgColor="F2F2F2")
HEAD = PatternFill("solid", fgColor="D9E1F2")
WRAP = Alignment(wrap_text=True, vertical="top")
THIN = Border(*(Side(style="thin", color="BFBFBF"),) * 4)


def evidence():
    out = {}
    for f, ts in SRC.items():
        wb = openpyxl.load_workbook(C / f, data_only=True)
        extra = None
        if "CMCSA" in ts:  # Comcast's guidance record arrived in Part A v2
            extra = openpyxl.load_workbook(C / "partA/Wharton_Part_A_Technology_and_Financials_v2.xlsx", data_only=True)["CMCSA follow-up"]
        for t in ts:
            rows = [[str(c).strip() for c in r if c is not None and str(c).strip()] for r in wb[t].iter_rows(values_only=True)]
            sids = {r[0]: " · ".join(r[1:]) for r in rows if r and re.fullmatch(r"S\d+", r[0])}
            d = {"items": {}, "table": [], "urls": [], "where": f"context/teammates_2026-11-19/{f}, tab {t}"}
            for k, pat in KEYS:
                for r in rows:
                    if len(r) >= 2 and k not in d["items"] and re.search(pat, r[0][:60]):
                        if k == "ai" and re.search(r"(?i)substitut|replace", r[0]):
                            continue
                        src = " | ".join(r[2:])
                        for s in re.findall(r"\bS\d+\b", src):
                            if s in sids:
                                src += f"\n{s}: {sids[s]}"
                        d["items"][k] = (r[0], r[1], src)
            trows = rows if t != "CMCSA" else [[str(c).strip() for c in r if c is not None and str(c).strip()] for r in extra.iter_rows(values_only=True)]
            for i, r in enumerate(trows):
                if r and len(r[0]) < 80 and re.search(TABLE, r[0]):
                    for r2 in trows[i:i + 14]:
                        if not r2:
                            if len(d["table"]) > 2:
                                break
                            continue
                        d["table"].append(" | ".join(r2))
                    break
            seen = set()
            for r in rows + (trows if t == "CMCSA" else []):
                for c in r:
                    for u in URL.findall(c):
                        u = u.rstrip(".")
                        if u not in seen:
                            seen.add(u)
                            d["urls"].append((r[0][:80], u))
            out[t] = d
    return out


def put(ws, r, c, v, font=None, fill=None, wrap=True, border=True):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = font or F()
    if fill:
        cell.fill = fill
    if wrap:
        cell.alignment = WRAP
    if border:
        cell.border = THIN
    return cell


def start_sheet(wb, tickers, who):
    ws = wb.active
    ws.title = "Start here"
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 110
    rows = [
        ("Management grading: finalists after the universe screen", None, F(bold=True, size=14)),
        ("For", who, None),
        ("Due", "Pat sets the date (suggested: Sun 22 Nov, 9 pm ET). Send this file back to Pat.", None),
        ("What this is", "Our last screen: how well each company is run, graded on four items (1 to 5). It catches what the numbers miss. "
                         "It can only remove a company, never add one back. Grade how the company is RUN, not whether the stock is cheap.", None),
        ("How to fill it in", "Only the YELLOW cells: one whole-number grade (1 to 5) per item, a one- or two-line reason in your own words, "
                              "and any extra evidence you found (with source and date). Grey cells are the teammates' evidence: do not edit them. "
                              "Blue text is data from our models (TEST).", None),
        ("AI rule", "\"Work generated by an AI program may not be submitted as the team's own.\" AI may help you FIND and CHECK facts, "
                    "but the grade and the reason must be yours. Note any AI use in the AI log rows at the bottom of each company tab (the report cites AI use in APA).", None),
        ("Pass mark", "Average of 3.0 or more (student judgment, Pat 17 Nov). Equal weights for the four items.", None),
        ("TEAM RULE NEEDED (Pat)", "Several companies give no issuer guidance (the evidence compares results with ANALYSTS' estimates instead). Pick one rule for everyone: "
                                   "(a) grade on the evidence available, treating analyst beats as weaker evidence; (b) leave that item blank and average the other three; "
                                   "(c) give a neutral 3. Pat's choice:", F(bold=True)),
        ("Scale", "See the 'Scale (draft)' tab: what a 1, 3 and 5 look like for each item. It is a DRAFT for Pat to approve or edit before grading.", None),
        ("Example (format only)", "Example Co, Capital allocation: grade 4. Reason: 'Bought back shares only from free cash flow and kept debt under its 2x target; "
                                  "one 2024 acquisition was written down, so not a 5.' Source: 2025 10-K pp. 40-42, filed 2026-02-20.", F(italic=True)),
    ]
    for i, (a, b, font) in enumerate(rows, 1):
        put(ws, i, 1, a, F(bold=True) if i > 1 else font, border=i > 1)
        if b is not None:
            put(ws, i, 2, b, font if i > 1 and font else None)
    rule_row = 8
    put(ws, rule_row, 3, None, fill=YELLOW)
    ws.column_dimensions["C"].width = 30
    ws.cell(row=rule_row, column=3).comment = Comment("Pat: write a, b or c (applies to every grader).", "Claude")
    r = len(rows) + 2
    put(ws, r, 1, "Assignment (proposed by package; edit freely)", F(bold=True), border=False)
    for g, ts in GRADERS.items():
        if set(ts) & set(tickers):
            r += 1
            put(ws, r, 1, g)
            put(ws, r, 2, ", ".join(f"{SNAP[t][0]} ({t})" for t in ts if t in tickers))
    r += 2
    put(ws, r, 1, "Where the evidence came from", F(bold=True), border=False)
    put(ws, r, 2, "The teammates' Round 2 workbooks of 19 Nov (each company tab names its file). Red flags and model figures: docs/finalists_2026-11-19.md (TEST).", border=False)


def scale_sheet(wb):
    ws = wb.create_sheet("Scale (draft)")
    for col, w in zip("ABCD", (24, 55, 55, 55)):
        ws.column_dimensions[col].width = w
    put(ws, 1, 1, "DRAFT scale proposed by Claude: Pat approves or edits it before anyone grades (student judgment). 2 and 4 sit between the anchors.", F(bold=True), border=False)
    for c, h in enumerate(("Item", "1 = serious concern", "3 = acceptable", "5 = clear strength"), 1):
        put(ws, 3, c, h, F(bold=True), HEAD)
    for i, (k, name) in enumerate(ITEMS, 4):
        put(ws, i, 1, name, F(bold=True))
        for j, text in enumerate(SCALE[k], 2):
            put(ws, i, j, text)


def company_sheet(wb, t, ev):
    ws = wb.create_sheet(t)
    for col, w in zip("ABC", (30, 95, 60)):
        ws.column_dimensions[col].width = w
    name, strat, vp, alpha, beta, m12 = SNAP[t]
    put(ws, 1, 1, f"{name} ({t}): management grade", F(bold=True, size=13), border=False)
    put(ws, 2, 1, "Grader", F(bold=True))
    put(ws, 2, 2, None, fill=YELLOW)
    put(ws, 3, 1, "Remember", F(bold=True))
    put(ws, 3, 2, "Grade how the company is run, not whether the stock is cheap. The figures below are context only.", F(italic=True))
    r = 5
    put(ws, r, 1, "Context (TEST, docs/finalists_2026-11-19.md)", F(bold=True), HEAD)
    put(ws, r, 2, None, fill=HEAD)
    put(ws, r, 3, None, fill=HEAD)
    for label, val in (("Strategies passed", strat), ("Value/price (beta 1.0 / 5-year / full)", vp),
                       ("Alpha vs industry", alpha), ("Beta vs industry", beta), ("M12 score", m12)):
        r += 1
        put(ws, r, 1, label)
        put(ws, r, 2, val, F(color="0000FF"))
    r += 2
    put(ws, r, 1, "Red flags to weigh", F(bold=True), HEAD)
    put(ws, r, 2, None, fill=HEAD)
    put(ws, r, 3, None, fill=HEAD)
    for fl in FLAGS[t]:
        r += 1
        put(ws, r, 1, "Red flag")
        put(ws, r, 2, fl, fill=GREY)
    cells = {}
    for k, title in ITEMS:
        r += 2
        put(ws, r, 1, title.upper(), F(bold=True), HEAD)
        put(ws, r, 2, "Evidence (teammate, 19 Nov)", F(bold=True), HEAD)
        put(ws, r, 3, "Source", F(bold=True), HEAD)
        it = ev["items"].get(k)
        r += 1
        put(ws, r, 1, it[0] if it else "Evidence")
        put(ws, r, 2, it[1] if it else "MISSING in the workbook", fill=GREY)
        put(ws, r, 3, it[2] if it else "", F(size=9), GREY)
        r += 1
        put(ws, r, 1, "Questions to consider")
        put(ws, r, 2, GENERIC[k])
        r += 1
        put(ws, r, 1, "For this company")
        put(ws, r, 2, SPECIFIC[t][k], F(bold=True))
        r += 1
        put(ws, r, 1, "Your grade (1 to 5)", F(bold=True))
        put(ws, r, 2, None, F(bold=True), YELLOW)
        cells[k] = f"B{r}"
        r += 1
        put(ws, r, 1, "Why (your own words)", F(bold=True))
        put(ws, r, 2, None, fill=YELLOW)
        ws.row_dimensions[r].height = 45
        cells[k + "_why"] = f"B{r}"
        r += 1
        put(ws, r, 1, "Extra evidence you found")
        put(ws, r, 2, None, fill=YELLOW)
        put(ws, r, 3, None, fill=YELLOW)
        ws.cell(row=r, column=3).comment = Comment("Source and date for your extra evidence.", "Claude")
    r += 2
    put(ws, r, 1, "AI exposure (context, not graded)", F(bold=True), HEAD)
    put(ws, r, 2, None, fill=HEAD)
    put(ws, r, 3, None, fill=HEAD)
    for k in ("ai", "sub"):
        it = ev["items"].get(k)
        if it:
            r += 1
            put(ws, r, 1, it[0])
            put(ws, r, 2, it[1], fill=GREY)
            put(ws, r, 3, it[2], F(size=9), GREY)
    if ev["table"]:
        r += 2
        put(ws, r, 1, "Guidance table (from the workbook)", F(bold=True), HEAD)
        put(ws, r, 2, None, fill=HEAD)
        put(ws, r, 3, None, fill=HEAD)
        for line in ev["table"]:
            r += 1
            put(ws, r, 2, line, F(size=9), GREY)
    r += 2
    put(ws, r, 1, "All sources in the teammate's tab", F(bold=True), HEAD)
    put(ws, r, 2, ev["where"], F(size=9), HEAD)
    put(ws, r, 3, None, fill=HEAD)
    for label, u in ev["urls"]:
        r += 1
        put(ws, r, 1, label, F(size=9))
        c = put(ws, r, 2, u, F(size=9, color="0563C1", underline="single"))
        c.hyperlink = u
    r += 2
    put(ws, r, 1, "Your AI use (tool, what for, what you checked)", F(bold=True))
    put(ws, r, 2, None, fill=YELLOW)
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True,
                        showErrorMessage=True, errorTitle="Grade", error="Enter a whole number from 1 to 5.")
    ws.add_data_validation(dv)
    for k, _ in ITEMS:
        dv.add(cells[k])
    ws.freeze_panes = "A4"
    return cells


def grades_sheet(wb, tickers, cells):
    ws = wb.create_sheet("Grades", 1)
    widths = (26, 9, 14, 13, 13, 13, 13, 9, 10, 10)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    put(ws, 1, 1, "Grades summary (fills itself from each company tab)", F(bold=True, size=12), border=False)
    put(ws, 2, 1, "Pass mark (average)", F(bold=True))
    put(ws, 2, 2, 3.0, F(color="0000FF"))
    ws["B2"].number_format = "0.0"
    ws["B2"].comment = Comment("Student judgment (Pat, 17 Nov).", "Claude")
    heads = ("Company", "Ticker", "Grader", "Capital allocation", "Guidance record", "Governance", "Controversies and legal", "Items graded", "Average", "Result")
    for c, h in enumerate(heads, 1):
        put(ws, 4, c, h, F(bold=True), HEAD)
    for i, t in enumerate(tickers, 5):
        put(ws, i, 1, SNAP[t][0])
        put(ws, i, 2, t)
        put(ws, i, 3, f"=IF('{t}'!B2=\"\",\"\",'{t}'!B2)", F(color="008000"))
        for j, (k, _) in enumerate(ITEMS, 4):
            put(ws, i, j, f"=IF('{t}'!{cells[t][k]}=\"\",\"\",'{t}'!{cells[t][k]})", F(color="008000"))
        put(ws, i, 8, f"=COUNT(D{i}:G{i})")
        put(ws, i, 9, f"=IF(H{i}=0,\"\",AVERAGE(D{i}:G{i}))")
        ws.cell(row=i, column=9).number_format = "0.00"
        put(ws, i, 10, f"=IF(H{i}=0,\"\",IF(I{i}>=$B$2,\"PASS\",\"fail\"))")
    ws.freeze_panes = "A5"


def build(path, tickers, who, ev):
    wb = openpyxl.Workbook()
    start_sheet(wb, tickers, who)
    scale_sheet(wb)
    cells = {t: company_sheet(wb, t, ev[t]) for t in tickers}
    grades_sheet(wb, tickers, cells)
    wb.save(path)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ev = evidence()
    build(OUT / "Management_Grading_ALL_12.xlsx", ORDER, "Pat (master copy: all 12 companies)", ev)
    for g, ts in GRADERS.items():
        build(OUT / f"Management_Grading_{g.replace(' ', '_')}.xlsx", ts, g, ev)
    print("\n".join(sorted(p.name for p in OUT.glob("*.xlsx"))))
