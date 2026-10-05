"""Build structure model v4 (Option 3 only) from v3.

v3 was removed from the repo after v4 was built; this script reads it from
git history (commit 90b8a21). Run from the repo root:
    python tools/build_structure_v4.py
"""
import subprocess
import tempfile
from copy import copy

import openpyxl
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

REPO = "/home/user/Wharton-Comp"
V3_COMMIT = "90b8a21"
SRC = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False).name
with open(SRC, "wb") as f:
    f.write(subprocess.run(
        ["git", "-C", REPO, "show",
         f"{V3_COMMIT}:context/Laura_Gao_Portfolio_Structure_Model_v3.xlsx"],
        check=True, capture_output=True).stdout)
OUT = f"{REPO}/context/Laura_Gao_Portfolio_Structure_Model_v4.xlsx"
M02 = f"{REPO}/context/M02_Assumptions_and_Scenarios_v1.xlsx"

wb = openpyxl.load_workbook(SRC)
vals = openpyxl.load_workbook(SRC, data_only=True)


def style_of(sheet, ref):
    return copy(wb[sheet][ref]._style)


# Style templates captured before any sheet is cleared.
ST = {
    "title": style_of("Step5_Scenarios", "A1"),
    "note": style_of("Step5_Scenarios", "A2"),
    "group": style_of("Step5_Scenarios", "C4"),
    "head": style_of("Step5_Scenarios", "B5"),
    "num": style_of("Step5_Scenarios", "A6"),
    "name": style_of("Step5_Scenarios", "B6"),
    "pct": style_of("Step5_Scenarios", "C6"),
    "pct_in": style_of("Step5_Scenarios", "C13"),
    "usd": style_of("Step5_Scenarios", "U6"),
    "text": style_of("Step5_Scenarios", "AG6"),
    "usd_res": style_of("Step5_Scenarios", "AH6"),
    "label": style_of("Step5_YearByYear", "A6"),
    "section": style_of("Step5_YearByYear", "A23"),
    "yb_pct": style_of("Step5_YearByYear", "B6"),
    "yb_usd": style_of("Step5_YearByYear", "B24"),
    "yb_year": style_of("Step5_YearByYear", "B5"),
    "sim_draw": style_of("Step5_Simulation", "B6"),
    "sim_pct": style_of("Step5_Simulation", "H6"),
    "sim_usd": style_of("Step5_Simulation", "Z6"),
    "sim_txt": style_of("Step5_Simulation", "AL6"),
    "sum_pct": style_of("Step5_Summary", "D5"),
    "sum_usd": style_of("Step5_Summary", "D7"),
    "sum_num": style_of("Step5_Summary", "D15"),
    "sum_note": style_of("Step5_Summary", "E5"),
    "chk_num": style_of("Checks", "A5"),
    "chk_txt": style_of("Checks", "B5"),
    "chk_val": style_of("Checks", "C5"),
    "chk_res": style_of("Checks", "F5"),
    "in_val": style_of("Inputs", "B24"),
    "in_unit": style_of("Inputs", "C24"),
    "in_type": style_of("Inputs", "D24"),
    "in_note": style_of("Inputs", "I24"),
    "blank": style_of("Inputs", "A11"),
    "wp_pct": style_of("WInS_Plan", "B14"),
    "wp_usd": style_of("WInS_Plan", "C19"),
    "wp_label": style_of("WInS_Plan", "A14"),
    "wp_head": style_of("WInS_Plan", "A12"),
}
DRAWS = [[vals["Step5_Simulation"].cell(r, c).value for c in range(2, 8)]
         for r in range(6, 1006)]


def put(ws, ref, value, style=None):
    cell = ws[ref]
    cell.value = value
    if style:
        cell._style = copy(ST[style])
    return cell


def clear_sheet(ws):
    for rng in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(rng))
    ws.delete_rows(1, ws.max_row + 1)


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


# ---------------------------------------------------------------- Inputs
ws = wb["Inputs"]
for row in (14, 23, 41, 45):
    for col in "ABCDEFGHI":
        ws[f"{col}{row}"].value = None
        ws[f"{col}{row}"]._style = copy(ST["blank"])
put(ws, "A21", "Option 3 settings (team choices; P1 approves in M08)")
put(ws, "A22", "Stage 1: lowest multiplier m still being considered")
put(ws, "B22", 1, "in_val")
put(ws, "C22", "x cushion", "in_unit")
put(ws, "D22", "Team choice", "in_type")
put(ws, "I22", "Stage 1 buys only what every m from this value up to B24 agrees on "
    "(WInS_Plan). Set it equal to B24 to trade the full Option 3 target in one stage.", "in_note")
put(ws, "I24", "Stocks = m x cushion, recalculated at the start of every year. m = 1 = lock in "
    "the floor and hold the cushion in stocks. Higher m = more stocks and more gap risk: the "
    "floor breaks if stocks fall by more than (1 + bond yield)/m - bond yield in one year "
    "(47.5% at m = 2, 30% at m = 3 with a 5% yield).")
put(ws, "I25", "Cap on stocks. Lower it to limit how aggressive Option 3 becomes after gains.")
put(ws, "I30", "Pick from the dropdown (list comes from Step5_Scenarios column B, rows 6-21).")
put(ws, "A37", "Derived values (formulas - do not edit)")
put(ws, "A44", "Required reserve at start of 2033 (with margin)")
for dv in ws.data_validations.dataValidation:
    if "B30" in str(dv.sqref):
        dv.formula1 = "Step5_Scenarios!$B$6:$B$21"

# ------------------------------------------------------- Step5_Scenarios
ws = wb["Step5_Scenarios"]
clear_sheet(ws)
put(ws, "A1", "Step 5 - Option 3 (floor rule) under preset market paths", "title")
put(ws, "A2", "Each row is one market path for the stock core. Normal years earn the COMPOUND "
    "base return (EXP(Inputs B18) - 1 = 5.5%), not the arithmetic average, because a fixed-return "
    "path compounds it. Bonds earn the bond yield (Inputs B13). Wealth is at the START of each "
    "year, after contributions. Stocks = m x (wealth - floor), capped (Inputs B24, B25).", "note")
put(ws, "C4", "Stock return during each year", "group")
put(ws, "I4", "Wealth at start of year", "group")
put(ws, "P4", "Stock share at start of year", "group")
put(ws, "V4", "Results at start of 2033 (before forming the reserve)", "group")
heads = ["#", "Scenario"] + [str(y) for y in range(2027, 2033)] + \
    [str(y) for y in range(2027, 2034)] + [str(y) for y in range(2027, 2033)] + \
    ["Reserve fully funded?", "Facility capacity", "Reserve gap",
     "Wealth below floor in any year 2028-2033?", "Type / source"]
for i, h in enumerate(heads):
    put(ws, f"{L(i + 1)}5", h, "head")

G, CR, SV, Y = "EXP(Inputs!$B$18)-1", "Inputs!$B$28", "Inputs!$B$29", "Inputs!$B$13"
presets = [
    ("Steady growth (compound base return)", [G] * 6, "ASSUMPTION: M02 A-04 base, 5.5% compound"),
    ("Crash in 2027", [CR] + [G] * 5, "RESEARCH: crash size Inputs B28 (2008)"),
    ("Crash in 2030", [G] * 3 + [CR] + [G] * 2, "RESEARCH: crash size Inputs B28 (2008)"),
    ("Crash in 2032", [G] * 5 + [CR], "RESEARCH: crash size Inputs B28 (2008)"),
    ("Severe crash in 2032", [G] * 5 + [SV], "RESEARCH: crash size Inputs B29 (1931)"),
    ("Zero stock returns every year", ["0"] * 6, "TEST"),
    ("Stocks earn the bond yield (check)", [Y] * 6, "TEST: must end at the risk-free value"),
    ("Custom (edit blue cells)", [0.10, -0.20, 0.05, 0.08, -0.10, 0.06], "TEST: type any path"),
]
m02 = openpyxl.load_workbook(M02, data_only=True)["Scenario_Definitions"]
for r in range(5, 14):
    sid, name = m02.cell(r, 1).value, m02.cell(r, 2).value
    if sid in (None, "S0") or not str(sid).startswith("S"):
        continue
    # Normal years in the M02 paths are the M02 base compound return (5.5%):
    # link them to the Inputs so they move with the stock-return assumption.
    # Historical crash and replay years stay as typed values.
    rets = [G if abs(m02.cell(r, c).value - 0.055) < 1e-12 else m02.cell(r, c).value
            for c in range(5, 11)]
    flag = m02.cell(r, 16).value
    linked = " (normal years linked to Inputs)" if G in rets else " (all years historical)"
    presets.append((f"M02 {sid}: {name}", rets,
                    f"{flag}: M02 Scenario_Definitions {sid}{linked}"))
assert len(presets) == 16, len(presets)

FIRST, LAST = 6, 6 + len(presets) - 1
for i, (name, rets, kind) in enumerate(presets):
    r = FIRST + i
    put(ws, f"A{r}", i + 1, "num")
    put(ws, f"B{r}", name, "name")
    for k, v in enumerate(rets):
        ref = f"{L(3 + k)}{r}"
        if isinstance(v, str):
            put(ws, ref, f"={v}", "pct")
        else:
            put(ws, ref, v, "pct_in" if name.startswith("Custom") else "pct")
    put(ws, f"I{r}", "=Inputs!$B$39", "usd")
    for k in range(6):
        w = f"{L(9 + k)}{r}"
        fl = f"Inputs!${L(2 + k)}$40"
        ret = f"{L(3 + k)}{r}"
        contrib = f"Inputs!${L(3 + k)}$39"
        stocks = f"MIN(Inputs!$B$24*MAX(0,{w}-{fl}),Inputs!$B$25*{w})"
        put(ws, f"{L(10 + k)}{r}",
            f"={stocks}*(1+{ret})+({w}-{stocks})*(1+Inputs!$B$13)+{contrib}", "usd")
        put(ws, f"{L(16 + k)}{r}", f"=IF({w}>0,{stocks}/{w},0)", "pct")
    put(ws, f"V{r}", f'=IF(O{r}>=Inputs!$B$44-0.01,"Yes","No")', "text")
    put(ws, f"W{r}", f"=MAX(0,ROUND(O{r}-Inputs!$B$44,2))", "usd_res")
    put(ws, f"X{r}", f"=MAX(0,ROUND(Inputs!$B$44-O{r},2))", "usd_res")
    below = ",".join(f"{L(10 + k)}{r}<Inputs!${L(3 + k)}$40-0.01" for k in range(6))
    put(ws, f"Y{r}", f'=IF(OR({below}),"Yes","No")', "text")
    put(ws, f"Z{r}", kind, "text")
put(ws, f"B{LAST + 2}", "Rows 1-8 use the Inputs crash sizes; rows 9-16 are P2's M02 stress paths "
    "(historical replays; S7's -10% is hypothetical). Their normal years use the same compound "
    "base return as rows 1-5, so they move with Inputs B16/B17; crash and replay years are fixed history.", "note")
put(ws, f"B{LAST + 3}", "Reading tip: facility capacity = wealth at the start of 2033 minus the required "
    "reserve (Inputs B44). While the cap is not hit, the cushion is multiplied each year by "
    "1 + yield + m x (stock return - yield), so the ORDER of years does not change the 2033 result.", "note")
widths(ws, {"A": 5, "B": 44, **{L(c): 9 for c in range(3, 9)}, **{L(c): 12 for c in range(9, 16)},
            **{L(c): 8 for c in range(16, 22)}, "V": 11, "W": 13, "X": 12, "Y": 14, "Z": 44})

# ------------------------------------------------------ Step5_YearByYear
ws = wb["Step5_YearByYear"]
clear_sheet(ws)
put(ws, "A1", "Step 5 - Option 3, one scenario year by year", "title")
put(ws, "A2", "Scenario shown (change in Inputs B30):", "label")
put(ws, "B2", "=Inputs!$B$30", "name")
put(ws, "A3", "Values are at the START of each year, after any contribution. Returns in row 6 apply "
    "during that year. Stocks = m x cushion, capped; the rest is in bonds.", "note")
put(ws, "A5", "Year", "head")
SC = f"Step5_Scenarios!$B${FIRST}:$B${LAST}"
for k in range(7):
    c = L(2 + k)
    put(ws, f"{c}5", f"=Inputs!{c}$38", "yb_year")
    put(ws, f"{c}8", f"=Inputs!{c}$39", "yb_usd")
    put(ws, f"{c}9", f"=Inputs!{c}$40", "yb_usd")
    put(ws, f"{c}11", f"=MAX(0,{c}10-{c}9)", "yb_usd")
    if k < 6:
        sc_col = L(3 + k)
        put(ws, f"{c}6", f"=INDEX(Step5_Scenarios!{sc_col}${FIRST}:{sc_col}${LAST},MATCH($B$2,{SC},0))",
            "yb_pct")
        put(ws, f"{c}7", "=Inputs!$B$13", "yb_pct")
        put(ws, f"{c}12", f"=MIN(Inputs!$B$24*{c}11,Inputs!$B$25*{c}10)", "yb_usd")
        put(ws, f"{c}13", f"={c}10-{c}12", "yb_usd")
        put(ws, f"{c}14", f"=IF({c}10>0,{c}12/{c}10,0)", "yb_pct")
    else:
        for row in (6, 7, 12, 13, 14):
            put(ws, f"{c}{row}", "-", "yb_year")
    if k == 0:
        put(ws, "B10", "=B8", "yb_usd")
    else:
        p = L(1 + k)
        put(ws, f"{c}10", f"={p}12*(1+{p}6)+{p}13*(1+{p}7)+{c}8", "yb_usd")
for row, label in [(6, "Stock return during the year"), (7, "Bond yield during the year"),
                   (8, "Contribution at start of year"), (9, "Floor (cost to lock in all payments)"),
                   (10, "Wealth at start of year"), (11, "Cushion = wealth - floor (min 0)"),
                   (12, "Stocks = m x cushion (capped)"), (13, "Bonds = wealth - stocks"),
                   (14, "Stock share")]:
    put(ws, f"A{row}", label, "label")
put(ws, "A16", "RESULT AT START OF 2033 (before forming the reserve)", "section")
for c, h in zip("ABCDE", ["Wealth", "Required reserve", "Reserve fully funded?",
                          "Facility capacity", "Reserve gap"]):
    put(ws, f"{c}17", h, "head")
put(ws, "A18", "=H10", "yb_usd")
put(ws, "B18", "=Inputs!$B$44", "yb_usd")
put(ws, "C18", '=IF(A18>=B18-0.01,"Yes","No")', "text")
put(ws, "D18", "=MAX(0,ROUND(A18-B18,2))", "yb_usd")
put(ws, "E18", "=MAX(0,ROUND(B18-A18,2))", "yb_usd")
widths(ws, {"A": 40, **{L(c): 13 for c in range(2, 9)}})
ch = LineChart()
ch.title = "Option 3: wealth vs floor (selected scenario)"
ch.y_axis.title = "USD"
ch.x_axis.title = "Start of year"
ch.add_data(Reference(ws, min_col=1, max_col=8, min_row=9, max_row=10), from_rows=True, titles_from_data=True)
ch.set_categories(Reference(ws, min_col=2, max_col=8, min_row=5, max_row=5))
ch.height, ch.width = 9, 18
ws._charts = []
ws.add_chart(ch, "A21")

# ------------------------------------------------------ Step5_Simulation
ws = wb["Step5_Simulation"]
clear_sheet(ws)
put(ws, "A1", "Step 5 - Simulation: Option 3 under 1,000 random market paths", "title")
put(ws, "A2", "Columns B-G are stored random draws (seed 20260926); columns H-M turn them into yearly "
    "stock returns using the Inputs log-return mean and volatility (B18, B19). Columns N-T apply "
    "the Option 3 rule year by year, exactly as on Step5_Scenarios.", "note")
put(ws, "B4", "Stored random draws (0-1)", "group")
put(ws, "H4", "Stock return during each year", "group")
put(ws, "N4", "Option 3 - wealth at start of year", "group")
put(ws, "U4", "Results at start of 2033", "group")
heads = ["Path"] + [f"u {y}" for y in range(2027, 2033)] + [str(y) for y in range(2027, 2033)] + \
    [str(y) for y in range(2027, 2034)] + ["Reserve fully funded?", "Facility capacity", "Reserve gap"]
for i, h in enumerate(heads):
    put(ws, f"{L(i + 1)}5", h, "head")
for i, draws in enumerate(DRAWS):
    r = 6 + i
    ws[f"A{r}"].value = i + 1
    for k in range(6):
        ws.cell(r, 2 + k).value = draws[k]
        ws.cell(r, 2 + k)._style = copy(ST["sim_draw"])
        c = ws.cell(r, 8 + k)
        c.value = f"=EXP(Inputs!$B$18+Inputs!$B$19*NORMSINV({L(2 + k)}{r}))-1"
        c._style = copy(ST["sim_pct"])
    ws[f"N{r}"].value = "=Inputs!$B$39"
    ws[f"N{r}"]._style = copy(ST["sim_usd"])
    for k in range(6):
        w = f"{L(14 + k)}{r}"
        fl = f"Inputs!${L(2 + k)}$40"
        stocks = f"MIN(Inputs!$B$24*MAX(0,{w}-{fl}),Inputs!$B$25*{w})"
        c = ws.cell(r, 15 + k)
        c.value = (f"={stocks}*(1+{L(8 + k)}{r})+({w}-{stocks})*(1+Inputs!$B$13)"
                   f"+Inputs!${L(3 + k)}$39")
        c._style = copy(ST["sim_usd"])
    ws[f"U{r}"].value = f'=IF(T{r}>=Inputs!$B$44-0.01,"Yes","No")'
    ws[f"U{r}"]._style = copy(ST["sim_txt"])
    ws[f"V{r}"].value = f"=MAX(0,ROUND(T{r}-Inputs!$B$44,2))"
    ws[f"V{r}"]._style = copy(ST["sim_usd"])
    ws[f"W{r}"].value = f"=MAX(0,ROUND(Inputs!$B$44-T{r},2))"
    ws[f"W{r}"]._style = copy(ST["sim_usd"])
widths(ws, {"A": 6, **{L(c): 9 for c in range(2, 14)}, **{L(c): 12 for c in range(14, 24)}})
ws.freeze_panes = "B6"

# --------------------------------------------------------- Step5_Summary
ws = wb["Step5_Summary"]
clear_sheet(ws)
SIM = "Step5_Simulation!"
N = f"COUNT({SIM}$A$6:$A$1005)"
put(ws, "A1", "Step 5 - Simulation summary (Option 3)", "title")
put(ws, "A2", "Mechanics under the M02 base assumptions. Not a funding-certainty claim until P4's M07 "
    "(block bootstrap of historical returns) replaces this lognormal simulation.", "note")
for c, h in zip("ABCD", ["Measure", "Option 3 - Floor rule", "What it means", "Chart label"]):
    put(ws, f"{c}4", h, "head")
rows = [
    ("Chance the reserve is fully funded at start of 2033",
     f'=COUNTIF({SIM}$U$6:$U$1005,"Yes")/{N}', "sum_pct",
     "Share of paths where the portfolio covers the required reserve.", None),
    ('="Chance facility capacity is at least "&TEXT(Inputs!$B$31,"$#,##0")',
     f'=COUNTIF({SIM}$V$6:$V$1005,">="&Inputs!$B$31)/{N}', "sum_pct",
     "Change the amount in Inputs B31.", None),
    ("Average facility capacity", f"=AVERAGE({SIM}$V$6:$V$1005)", "sum_usd",
     "Averages hide bad outcomes - read with the percentiles below.", None),
    ("Facility capacity - 5th percentile (bad case)", f"=PERCENTILE({SIM}$V$6:$V$1005,0.05)",
     "sum_usd", "95% of paths did at least this well.", "5th pct (bad)"),
    ("Facility capacity - 25th percentile", f"=PERCENTILE({SIM}$V$6:$V$1005,0.25)", "sum_usd",
     None, "25th pct"),
    ("Facility capacity - median", f"=MEDIAN({SIM}$V$6:$V$1005)", "sum_usd", "Middle outcome.", "Median"),
    ("Facility capacity - 75th percentile", f"=PERCENTILE({SIM}$V$6:$V$1005,0.75)", "sum_usd",
     None, "75th pct"),
    ("Facility capacity - 95th percentile (good case)", f"=PERCENTILE({SIM}$V$6:$V$1005,0.95)",
     "sum_usd", "Only 5% of paths did better.", "95th pct (good)"),
    ("Portfolio value at start of 2033 - 5th percentile", f"=PERCENTILE({SIM}$T$6:$T$1005,0.05)",
     "sum_usd", "Before forming the reserve.", None),
    ("Portfolio value at start of 2033 - median", f"=MEDIAN({SIM}$T$6:$T$1005)", "sum_usd", None, None),
    ("Number of paths with a reserve gap", f'=COUNTIF({SIM}$W$6:$W$1005,">0")', "sum_num",
     "Paths where the ten payments are NOT fully covered in 2033.", None),
    ("Average gap in those paths", f'=IFERROR(AVERAGEIF({SIM}$W$6:$W$1005,">0"),0)', "sum_usd",
     "How bad a shortfall typically is (severity).", None),
    ("Largest gap", f"=MAX({SIM}$W$6:$W$1005)", "sum_usd", "Worst simulated shortfall.", None),
]
for i, (label, f, st, note, chart) in enumerate(rows):
    r = 5 + i
    put(ws, f"A{r}", label, "label")
    put(ws, f"B{r}", f, st)
    if note:
        put(ws, f"C{r}", note, "sum_note")
    if chart:
        put(ws, f"D{r}", chart, "sum_note")
put(ws, "A19", "Check on the simulated stock returns", "section")
for c, h in zip("ABC", ["Measure", "Input", "Simulated"]):
    put(ws, f"{c}20", h, "head")
put(ws, "A21", "Average yearly stock return", "label")
put(ws, "B21", "=Inputs!$B$16", "sum_pct")
put(ws, "C21", f"=AVERAGE({SIM}$H$6:$M$1005)", "sum_pct")
put(ws, "A22", "Volatility of yearly stock returns", "label")
put(ws, "B22", "=Inputs!$B$17", "sum_pct")
put(ws, "C22", f"=STDEV({SIM}$H$6:$M$1005)", "sum_pct")
put(ws, "A24", "How to read this sheet: look at the chance the reserve is funded FIRST (Laura's ten "
    "payments), then the spread of facility capacity (the 2031 pitch). The 5th percentile is the "
    "honest 'bad case' number. This lognormal simulation produces crash years less often than "
    "history (fat tails), so treat the bad-case numbers as optimistic.", "note")
widths(ws, {"A": 52, "B": 20, "C": 58, "D": 16})
ch = BarChart()
ch.title = "Option 3: facility capacity in 2033 across 1,000 paths"
ch.y_axis.title = "USD"
ch.add_data(Reference(ws, min_col=2, min_row=8, max_row=12), titles_from_data=False)
ch.set_categories(Reference(ws, min_col=4, min_row=8, max_row=12))
ch.legend = None
ch.height, ch.width = 9, 18
ws._charts = []
ws.add_chart(ch, "A26")

# ------------------------------------------------------------- WInS_Plan
ws = wb["WInS_Plan"]
ws.data_validations.dataValidation = [d for d in ws.data_validations.dataValidation
                                      if "B5" not in str(d.sqref)]
merged_notes = [str(r) for r in ws.merged_cells.ranges if r.min_row >= 12]
for rng in merged_notes:
    ws.unmerge_cells(rng)
for row in range(12, 33):
    for col in "ABCDE":
        ws[f"{col}{row}"].value = None
put(ws, "A2", "Stage 1 = amounts every multiplier still under consideration agrees on (from Inputs B22 "
    "up to the chosen m in B24): safe to trade now. Stage 2 = the full Option 3 target at the "
    "chosen m, plus the sector tilts.")
put(ws, "A5", "Strategy")
put(ws, "B5", "Option 3 - Floor rule")
put(ws, "E5", "Stocks = m x cushion, rebalanced every year (Inputs B24, B25).")
put(ws, "A12", "Option 3 shares at start of 2028", "wp_head")
put(ws, "B12", "Lowest m considered (Stage 1)", "wp_head")
put(ws, "C12", "Chosen m (Stage 2)", "wp_head")
put(ws, "A13", "Multiplier m", "wp_label")
put(ws, "B13", "=Inputs!$B$22", "in_val")
put(ws, "C13", "=Inputs!$B$24", "in_val")
for c in "BC":
    put(ws, f"{c}14", f"=IF($B$8>0,MIN({c}13*MAX(0,$B$10),Inputs!$B$25*$B$8)/$B$8,0)", "wp_pct")
    put(ws, f"{c}15", f"=1-{c}14", "wp_pct")
put(ws, "A14", "Growth (stock) share", "wp_label")
put(ws, "A15", "Safety (bond) share", "wp_label")
put(ws, "A17", "STAGE 1 - no-regret trades (every m considered agrees)", "wp_head")
put(ws, "A18", "Part", "wp_head")
put(ws, "B18", "Share", "wp_head")
put(ws, "C18", "Amount", "wp_head")
put(ws, "A19", "Safety: the smallest bond share any m considered needs (the chosen m)", "wp_label")
put(ws, "B19", "=MIN(B15:C15)", "wp_pct")
put(ws, "A20", "Growth core: the smallest stock share any m considered holds", "wp_label")
put(ws, "B20", "=MIN(B14:C14)", "wp_pct")
put(ws, "A21", "Parked in T-bills until Stage 2", "wp_label")
put(ws, "B21", "=1-B19-B20", "wp_pct")
put(ws, "A22", "Total", "wp_label")
put(ws, "B22", "=SUM(B19:B21)", "wp_pct")
put(ws, "A24", "STAGE 2 - full Option 3 target at the chosen m", "wp_head")
put(ws, "A25", "Part", "wp_head")
put(ws, "B25", "Share", "wp_head")
put(ws, "C25", "Amount", "wp_head")
put(ws, "A26", "Safety target", "wp_label")
put(ws, "B26", "=C15", "wp_pct")
put(ws, "A27", "Growth target (core + tilts)", "wp_label")
put(ws, "B27", "=C14", "wp_pct")
put(ws, "A28", "   of which sector tilts (from Tilt_Sizing)", "wp_label")
put(ws, "B28", "=Tilt_Sizing!$F$16", "wp_pct")
put(ws, "A29", "   of which growth core", "wp_label")
put(ws, "B29", "=B27-B28", "wp_pct")
put(ws, "A30", "Total (safety + growth)", "wp_label")
put(ws, "B30", "=B26+B27", "wp_pct")
for r in (19, 20, 21, 22, 26, 27, 28, 29, 30):
    put(ws, f"C{r}", f"=B{r}*$B$4", "wp_usd")
put(ws, "A32", "How to read: Stage 1 never holds more stocks than the most cautious m you are still "
    "considering, and already holds the bonds the chosen m needs; the rest waits in T-bills. If "
    "Inputs B22 = B24, Stage 1 equals Stage 2 and nothing is parked.")
for rng in merged_notes:
    ws.merge_cells(rng)

# ------------------------------------------------------------ Trade_List
ws = wb["Trade_List"]
put(ws, "A22", "STAGE 2 - after P1 approves m and the tilts")

# ---------------------------------------------------------------- Checks
ws = wb["Checks"]
clear_sheet(ws)
ws.conditional_formatting = type(ws.conditional_formatting)()
put(ws, "A1", "Checks - every row should say PASS", "title")
put(ws, "B2", '="Checks passed: "&COUNTIF(F5:F24,"PASS")&" of "&COUNTA(B5:B24)', "chk_txt")
for c, h in zip("ABCDEF", ["#", "Check", "Expected", "Actual", "Difference", "Result"]):
    put(ws, f"{c}4", h, "head")
RF = f"Inputs!$B$5*(1+Inputs!$B$13)^6+Inputs!$B$6*(1+Inputs!$B$13)^5"
SCB = f"Step5_Scenarios!$B${FIRST}:$B${LAST}"
H0 = 30  # first helper row
checks = [
    ("Reserve cost: PV formula equals the worked discounting table", "=Step4_Sizing!E31", "=Inputs!$B$43", 0.01),
    ("Year axis ends at the first payment year", "=Inputs!$B$9", "=Inputs!H38", 0.01),
    ("Floor in 2033 equals the required reserve", "=Inputs!$B$44", "=Inputs!H40", 0.01),
    ("Step 4 Option 3 stock share equals the WInS plan (chosen m)", "=WInS_Plan!C14", "=Step4_Sizing!B15", 1e-9),
    ("Stocks earn the bond yield: Option 3 ends at the risk-free value", f"={RF}",
     f"=Step5_Scenarios!O{FIRST + 6}", 0.01),
    ("Steady path matches the cushion formula (cushion x (1 + y + m(g - y))^5); n/a if the cap binds",
     f'=IF(MAX(Step5_Scenarios!P{FIRST}:U{FIRST})>=Inputs!$B$25-0.000001,"n/a",Inputs!$H$40+'
     f'(IF(Inputs!$B$39>=Inputs!$B$40,(Inputs!$B$39-Inputs!$B$40)*(1+Inputs!$B$13+Inputs!$B$24*'
     f'(Step5_Scenarios!C{FIRST}-Inputs!$B$13)),(Inputs!$B$39-Inputs!$B$40)*(1+Inputs!$B$13))+Inputs!$C$39)'
     f'*(1+Inputs!$B$13+Inputs!$B$24*(EXP(Inputs!$B$18)-1-Inputs!$B$13))^5)',
     f"=Step5_Scenarios!O{FIRST}", 0.01),
    ("m = 1: rule recomputed step by step equals 'lock in the floor, hold the cushion in stocks' "
     "(all 16 paths, largest difference)", "0", f"=MAX(I{H0 + 1}:I{H0 + len(presets)})", 0.01),
    ("Year-by-year sheet matches the scenario table (selected scenario)",
     f"=INDEX(Step5_Scenarios!$O${FIRST}:$O${LAST},MATCH(Inputs!$B$30,{SCB},0))",
     "=Step5_YearByYear!H10", 0.01),
    ("Option 3 stock share never exceeds the maximum (all preset paths)", "=Inputs!$B$25",
     f"=MAX(Step5_Scenarios!P{FIRST}:U{LAST})", "le"),
    ("Stored random draws are strictly between 0 and 1 (lowest | highest)", "(0, 1)",
     '=TEXT(MIN(Step5_Simulation!B6:G1005),"0.000000")&" | "&TEXT(MAX(Step5_Simulation!B6:G1005),"0.000000")',
     "draws"),
    ("Simulated average return within 1.5 points of the input", "=Inputs!$B$16", "=Step5_Summary!C21", 0.015),
    ("Simulated volatility within 1.5 points of the input", "=Inputs!$B$17", "=Step5_Summary!C22", 0.015),
    ("Stage 1 amounts add up to the WInS account value", "=WInS_Plan!$B$4", "=WInS_Plan!$C$22", 1),
    ("Stage 2 targets add up to the WInS account value", "=WInS_Plan!$B$4", "=Trade_List!D35", 1),
    ("Safety split weights add up to 100%", "1", "=Trade_List!B11", 0.0001),
    ("Every tilt is within its loss-budget limit", "All Yes",
     '=COUNTIF(Tilt_Sizing!G10:G15,"No")&" No"', "tilts"),
    ("Total tilts are within the tilt budget", "=Tilt_Sizing!$F$5", "=Tilt_Sizing!$F$16", "le"),
    ("Growth core target in Stage 2 is not negative (tilts fit inside growth)", ">= 0",
     "=WInS_Plan!$C$29", "nonneg"),
    ("Stage 1 never exceeds Stage 2 targets (safety and growth)", "Stage 1 <= Stage 2",
     '=IF(AND(WInS_Plan!C19<=WInS_Plan!C26+0.01,WInS_Plan!C20<=WInS_Plan!C27+0.01),"OK","Exceeds")', "ok"),
    ("Stage 2 buys and sells net to about zero", "0", "=Trade_List!F35", 1),
]
for i, (label, exp, act, tol) in enumerate(checks):
    r = 5 + i
    put(ws, f"A{r}", i + 1, "chk_num")
    put(ws, f"B{r}", label, "chk_txt")
    put(ws, f"C{r}", float(exp) if exp in ("0", "1") else exp, "chk_val")
    put(ws, f"D{r}", act, "chk_val")
    if isinstance(tol, float) or isinstance(tol, int):
        put(ws, f"E{r}", f'=IF(ISNUMBER(C{r}),ABS(D{r}-C{r}),0)', "chk_val")
        res = f'=IF(OR(C{r}="n/a",E{r}<{tol}),"PASS","FAIL")'
    elif tol == "le":
        put(ws, f"E{r}", f"=D{r}-C{r}", "chk_val")
        res = f'=IF(D{r}<=C{r}+0.000001,"PASS","FAIL")'
    elif tol == "draws":
        res = '=IF(AND(MIN(Step5_Simulation!B6:G1005)>0,MAX(Step5_Simulation!B6:G1005)<1),"PASS","FAIL")'
    elif tol == "tilts":
        res = '=IF(COUNTIF(Tilt_Sizing!G10:G15,"No")=0,"PASS","FAIL")'
    elif tol == "nonneg":
        res = f'=IF(D{r}>=0,"PASS","FAIL")'
    elif tol == "ok":
        res = f'=IF(D{r}="OK","PASS","FAIL")'
    put(ws, f"F{r}", res, "chk_res")
green = PatternFill("solid", start_color="C6EFCE", end_color="C6EFCE")
red = PatternFill("solid", start_color="FFC7CE", end_color="FFC7CE")
ws.conditional_formatting.add("F5:F24", CellIsRule(operator="equal", formula=['"PASS"'], fill=green,
                                                    font=Font(color="006100")))
ws.conditional_formatting.add("F5:F24", CellIsRule(operator="equal", formula=['"FAIL"'], fill=red,
                                                    font=Font(color="9C0006")))
# Helper for check 7: m = 1 step by step vs the closed form.
put(ws, f"B{H0 - 2}", "Helper for check 7: Option 3 recomputed with m = 1 and no cap, versus the closed "
    "form 'floor in 2033 + cushion in 2028 x product of (1 + stock return), 2028-2032'.", "chk_txt")
for c, h in zip("BCDEFGHI", ["Scenario", "Step-by-step wealth 2028", "2029", "2030", "2031", "2032",
                             "2033", "Abs diff vs closed form"]):
    put(ws, f"{c}{H0}", h, "head")
for i in range(len(presets)):
    r, s = H0 + 1 + i, FIRST + i
    put(ws, f"B{r}", f"=Step5_Scenarios!B{s}", "chk_txt")
    prev = "Inputs!$B$39"
    for k in range(6):
        col = L(3 + k)
        fl = f"Inputs!${L(2 + k)}$40"
        stocks = f"MAX(0,{prev}-{fl})"
        put(ws, f"{col}{r}", f"={stocks}*(1+Step5_Scenarios!{L(3 + k)}{s})+({prev}-{stocks})*"
            f"(1+Inputs!$B$13)+Inputs!${L(3 + k)}$39", "chk_val")
        prev = f"{col}{r}"
    closed = (f"Inputs!$H$40+MAX(0,IF(Inputs!$B$39>=Inputs!$B$40,(Inputs!$B$39-Inputs!$B$40)*"
              f"(1+Step5_Scenarios!C{s}),(Inputs!$B$39-Inputs!$B$40)*(1+Inputs!$B$13))+Inputs!$C$39)*"
              + "*".join(f"(1+Step5_Scenarios!{L(4 + k)}{s})" for k in range(5)))
    put(ws, f"I{r}", f"=ABS(H{r}-({closed}))", "chk_val")
widths(ws, {"A": 5, "B": 70, "C": 16, "D": 16, "E": 12, "F": 10, "G": 13, "H": 13, "I": 16})

# ---------------------------------------------------------------- README
ws = wb["README"]
readme = {
    "B1": "Laura Gao - Portfolio Structure Model v4 (Option 3 floor rule + WInS trade plan)",
    "B2": "Status: v4, 5 Oct 2026. Option 3 only (Options 1 and 2 removed by team decision; see v3 for "
          "the comparison). NOT an approved recommendation. Yellow cells are placeholders to be "
          "replaced by approved inputs from M02 (P2), M05 (P4) and M08 (P1).",
    "B6": "Step 5 (Step5_ sheets): runs the Option 3 floor rule from 2027 until the reserve is formed at "
          "the start of 2033, under 16 preset market paths and 1,000 random paths.",
    "B8": "OPTION 3 - THE FLOOR RULE IN PLAIN ENGLISH",
    "B9": "Every year compute the floor: the cost, that year, of bonds that cover all ten payments. "
          "Money above the floor is the 'cushion'.",
    "B10": "Put m x cushion into stocks (capped at the maximum share) and the rest into bonds. Gains "
           "grow the cushion, so stock holdings rise; losses shrink it, so money moves into bonds "
           "automatically.",
    "B11": "Bonds are held to maturity, so their yield is locked when bought. m = 1 is the same as "
           "locking in the floor and holding the cushion in stocks (see Checks).",
    "B17": "3. Step5_Scenarios: Option 3 under 16 preset market paths (steady growth, crashes in "
           "different years, P2's M02 stress paths, a custom path you can type).",
    "B18": "4. Step5_YearByYear: choose a scenario in Inputs B30 to see Option 3 year by year, with a chart.",
    "B28": "Required reserve: the floor at the start of 2033 (Inputs B44).",
    "B33": "- After 2028, the ORDER of good and bad years does not change the 2033 result, only their "
           "combination (as long as the cap is not hit and the cushion stays above zero). Compare the "
           "2030 and 2032 crash rows.",
    "B34": "- A crash in 2027 does not touch Option 3: the 2027 money alone is below the floor, so it "
           "holds no stocks until the 2028 contribution.",
    "B35": "- Option 3 holds MORE stocks after gains, so a crash just before 2033 can erase much of the "
           "facility money even though the reserve stays covered. Lower m or the maximum stock share "
           "to limit this.",
    "B38": "- One flat bond yield for 2027-2033; no yield-curve shape; bond values only grow at that "
           "yield (held-to-maturity ladder). Rebalancing sells bonds at that value, ignoring price "
           "changes from interest rates.",
    "B39": "- Stock returns: one return per year, independent across years, lognormal, using the M02 "
           "base average and volatility. Not a forecast. Real markets have fatter tails and streaks. "
           "Fixed-return preset paths use the compound return (5.5%), not the arithmetic average.",
    "B48": "Crash sizes and stress paths: P2's M02 assumptions (2008 -37.0%, 1931 -43.84%) and "
           "M02 Scenario_Definitions S1-S8.",
    "B52": "WInS_Plan: turns Option 3 into percentages and dollars for the WInS account. Stage 1 = the "
           "amounts every multiplier still under consideration agrees on (safe to trade now). Stage 2 = "
           "the full target at the chosen m.",
    "B56": "Workflow: (1) P5 confirms WInS value and eligible funds; (2) enter WInS prices; (3) write "
           "Trading Notes, then trade Stage 1; (4) after P1 approves m and the tilts, trade Stage 2.",
}
for ref, text in readme.items():
    ws[ref].value = text
ws["B12"].value = ("The floor can only break if stocks fall by more than (1 + bond yield)/m - bond yield "
                   "within one year (47.5% when m = 2 and the yield is 5%). This is called gap risk.")

wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print("saved", OUT, "presets", len(presets), "rows", FIRST, LAST)
