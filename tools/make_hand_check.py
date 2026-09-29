"""Build handcheck/M05_hand_check.xlsx: the M05 math as plain spreadsheet
formulas, so a teammate can rebuild and check it without reading Python.

Needs openpyxl (only for this script). From the repo folder:
    python tools/make_hand_check.py
"""

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from m05 import inputs  # noqa: E402
from m05.run import MODEL_VERSION, payment_terms, run_scenario  # noqa: E402

OUT = ROOT / "handcheck" / "M05_hand_check.xlsx"
DEFAULT_SCENARIO = "TEST_Y0_A450"

FONT = "Arial"
BLUE = Font(name=FONT, color="0000FF")
BLACK = Font(name=FONT)
GREEN = Font(name=FONT, color="008000")
BOLD = Font(name=FONT, bold=True)
TITLE = Font(name=FONT, bold=True, size=14)
NOTE = Font(name=FONT, italic=True, color="595959")
YELLOW = PatternFill("solid", fgColor="FFFF00")

USD = '$#,##0.00;($#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'
YEAR = "0"
TOL = 0.005


def header(ws, row, labels):
    for col, label in enumerate(labels, start=1):
        cell = ws.cell(row=row, column=col, value=label)
        cell.font = BOLD
        cell.alignment = Alignment(wrap_text=True)


def put(ws, ref, value, font=BLACK, fmt=None, fill=None):
    cell = ws[ref]
    cell.value = value
    cell.font = font
    if fmt:
        cell.number_format = fmt
    if fill:
        cell.fill = fill
    return cell


def build_inputs(ws, scenario, terms):
    ws.title = "Inputs"
    put(ws, "A1", "M05 hand check: operating reserve", TITLE)
    put(ws, "A2", "Blue cells are inputs; yellow cells are assumptions you "
                  "can change. Black cells are formulas. Green cells pull "
                  "from another sheet.", NOTE)
    header(ws, 4, ["Input", "Value", "Unit", "Status", "Source"])
    rows = [
        ("Payment", terms["payment"], "USD", "CASE",
         "Case study p.3 (fixed; not adjusted for inflation)", USD, None),
        ("First payment year", terms["first_year"], "year", "CASE",
         "Case study p.3", YEAR, None),
        ("Sizing yield", scenario["sizing_yield"], "decimal", "TEST",
         "Not sourced. Replace with P2's M02 yield once approved", PCT,
         YELLOW),
        ("Reserve return (run-off)", scenario["runoff_return"], "decimal",
         "TEST", "Not sourced. Same flat rate every year", PCT, YELLOW),
        ("Portfolio at start of 2033", scenario["available_2033"], "USD",
         "TEST", "M01 guide p.5 test value; replace with M01's output",
         USD, YELLOW),
    ]
    for i, (name, value, unit, status, source, fmt, fill) in enumerate(
            rows, start=5):
        put(ws, f"A{i}", name)
        put(ws, f"B{i}", value, BLUE, fmt, fill)
        put(ws, f"C{i}", unit)
        put(ws, f"D{i}", status)
        put(ws, f"E{i}", source)
    put(ws, "A11", f"Default inputs are scenario {DEFAULT_SCENARIO}. To "
                   "check another scenario, copy its three yellow values "
                   "from the Scenarios sheet.", NOTE)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 10
    ws.column_dimensions["D"].width = 10
    ws.column_dimensions["E"].width = 58


def build_reserve(ws):
    put(ws, "A1", "Required reserve: the explicit ten-payment sum", TITLE)
    put(ws, "A2", "Payment k is k years after the reserve is formed, so it "
                  "is discounted k times. k = 0 is the immediate first "
                  "payment, so its factor is 1.", NOTE)
    header(ws, 4, ["k (years away)", "Year", "Payment", "Discount factor",
                   "Present value"])
    for k in range(10):
        r = 5 + k
        put(ws, f"A{r}", k, BLUE)
        put(ws, f"B{r}", f"=Inputs!$B$6+A{r}", GREEN, YEAR)
        put(ws, f"C{r}", "=Inputs!$B$5", GREEN, USD)
        put(ws, f"D{r}", f"=1/(1+Inputs!$B$7)^A{r}", BLACK, "0.000000")
        put(ws, f"E{r}", f"=C{r}*D{r}", BLACK, USD)
    labels = [
        (16, "Required reserve", "=SUM(E5:E14)", USD),
        (17, "Portfolio at start of 2033", "=Inputs!$B$9", USD),
        (18, "Actual reserve transfer", "=MIN(B16,MAX(0,B17))", USD),
        (19, "Reserve gap", "=B16-B18", USD),
        (20, "Reserve established?", f'=IF(B19<={TOL},"YES","NO")', None),
    ]
    for r, label, formula, fmt in labels:
        put(ws, f"A{r}", label, BOLD)
        put(ws, f"B{r}", formula, GREEN if "Inputs" in formula else BLACK,
            fmt)
    ws["B18"].comment = Comment(
        "Move what the portfolio has, up to the required amount. "
        "Never below zero.", "M05")
    put(ws, "A22", "The gap is recorded before any facility gift. While the "
                   "gap is above zero, the facility gift is zero.", NOTE)
    for col, width in zip("ABCDE", [30, 16, 14, 16, 16]):
        ws.column_dimensions[col].width = width


def build_run_off(ws):
    put(ws, "A1", "Run-off: the reserve paying out year by year", TITLE)
    put(ws, "A2", "Each year the payment comes first, then that year's "
                  "return. Balances never go below zero; money that is not "
                  "there shows up as a shortfall.", NOTE)
    header(ws, 4, ["Year", "Balance before payment", "Payment due",
                   "Payment funded", "Shortfall", "Balance after payment",
                   "Return rate", "Next balance", "Short year"])
    for i in range(10):
        r = 5 + i
        last = i == 9
        put(ws, f"A{r}", f"=Inputs!$B$6+{i}", GREEN, YEAR)
        before = "=Reserve!$B$18" if i == 0 else f"=H{r - 1}"
        put(ws, f"B{r}", before, GREEN if i == 0 else BLACK, USD)
        put(ws, f"C{r}", "=Inputs!$B$5", GREEN, USD)
        put(ws, f"D{r}", f"=MIN(C{r},MAX(0,B{r}))", BLACK, USD)
        put(ws, f"E{r}", f"=C{r}-D{r}", BLACK, USD)
        put(ws, f"F{r}", f"=B{r}-D{r}", BLACK, USD)
        if last:
            put(ws, f"G{r}", 0, BLUE, PCT)
            ws[f"G{r}"].comment = Comment(
                "No return after the final payment: the plan ends here.",
                "M05")
        else:
            put(ws, f"G{r}", "=Inputs!$B$8", GREEN, PCT)
        put(ws, f"H{r}", f"=F{r}*(1+G{r})", BLACK, USD)
        put(ws, f"I{r}", f'=IF(E{r}>{TOL},A{r},"")', BLACK, YEAR)
    totals = [
        (16, "Total paid", "=SUM(D5:D14)", USD),
        (17, "Total shortfall", "=SUM(E5:E14)", USD),
        (18, "All ten payments funded?", '=IF(COUNT(I5:I14)=0,"YES","NO")',
         None),
        (19, "First short year", '=IF(COUNT(I5:I14)=0,"none",MIN(I5:I14))',
         YEAR),
        (20, "Lowest balance after a payment", "=MIN(F5:F14)", USD),
    ]
    for r, label, formula, fmt in totals:
        put(ws, f"A{r}", label, BOLD)
        put(ws, f"B{r}", formula, BLACK, fmt)
    for col, width in zip("ABCDEFGHI", [26, 16, 14, 14, 14, 16, 12, 16, 11]):
        ws.column_dimensions[col].width = width


def build_checks(ws, decision, rows, summary):
    put(ws, "A1", f"Checks against the Python model ({MODEL_VERSION})",
        TITLE)
    put(ws, "A2", f"Expected values come from the Python model for the "
                  f"default inputs ({DEFAULT_SCENARIO}). They only apply "
                  f"while Inputs holds those values.", NOTE)
    header(ws, 4, ["Check", "Expected (Python)", "Actual (this sheet)",
                   "Difference", "Pass?"])
    checks = [
        ("Required reserve", decision["reserve_required"], "=Reserve!B16"),
        ("Actual reserve transfer", decision["actual_reserve_transfer"],
         "=Reserve!B18"),
        ("Reserve gap", decision["reserve_gap"], "=Reserve!B19"),
        ("Total paid", sum(r["payment_funded"] for r in rows),
         "='Run-off'!B16"),
        ("Total shortfall", summary["total_shortfall"], "='Run-off'!B17"),
        ("First short year", summary["first_shortfall_year"] or 0,
         "=IF(ISNUMBER('Run-off'!B19),'Run-off'!B19,0)"),
        ("Payment 10 funded", rows[9]["payment_funded"], "='Run-off'!D14"),
        ("Balance after payment 10", rows[9]["balance_after_payment"],
         "='Run-off'!F14"),
    ]
    for i, (label, expected, formula) in enumerate(checks, start=5):
        fmt = YEAR if "year" in label else USD
        put(ws, f"A{i}", label)
        put(ws, f"B{i}", round(expected, 2), BLUE, fmt)
        put(ws, f"C{i}", formula, GREEN, fmt)
        put(ws, f"D{i}", f"=C{i}-B{i}", BLACK, USD)
        put(ws, f"E{i}", f'=IF(ABS(D{i})<=0.01,"PASS","FAIL")', BLACK)
    last = 4 + len(checks)
    put(ws, f"A{last + 2}", "All checks pass?", BOLD)
    put(ws, f"B{last + 2}",
        f'=IF(COUNTIF(E5:E{last},"PASS")={len(checks)},"YES","NO")', BOLD)
    put(ws, f"A{last + 4}", "Reviewer:", BOLD)
    put(ws, f"A{last + 5}", "Date checked:", BOLD)
    ws.column_dimensions["A"].width = 28
    for col in "BCDE":
        ws.column_dimensions[col].width = 18


def build_scenarios(ws, results):
    put(ws, "A1", "Scenarios: inputs and Python results", TITLE)
    put(ws, "A2", "Copy a row's three input values into Inputs, then "
                  "compare this sheet's results with Reserve and Run-off. "
                  "All rates are TEST values, not sourced.", NOTE)
    header(ws, 4, ["Scenario", "Sizing yield", "Reserve return",
                   "Portfolio 2033", "Required reserve", "Reserve gap",
                   "All funded?", "Total shortfall", "Note"])
    for i, (s, decision, summary) in enumerate(results, start=5):
        values = [
            (s["scenario_id"], None),
            (s["sizing_yield"], PCT),
            (s["runoff_return"], PCT),
            (s["available_2033"], USD),
            (round(decision["reserve_required"], 2), USD),
            (round(decision["reserve_gap"], 2), USD),
            ("YES" if summary["all_payments_funded"] else "NO", None),
            (round(summary["total_shortfall"], 2), USD),
            (s["note"], None),
        ]
        for col, (value, fmt) in enumerate(values, start=1):
            cell = ws.cell(row=i, column=col, value=value)
            cell.font = BLUE
            if fmt:
                cell.number_format = fmt
    for col, width in zip("ABCDEFGHI", [20, 12, 14, 16, 16, 14, 11, 16, 60]):
        ws.column_dimensions[col].width = width


def main():
    terms = payment_terms(inputs.load_case_facts())
    scenarios = inputs.load_test_scenarios()
    results = []
    default = None
    for s in scenarios:
        decision, rows, summary = run_scenario(s, terms)
        results.append((s, decision, summary))
        if s["scenario_id"] == DEFAULT_SCENARIO:
            default = (s, decision, rows, summary)

    wb = Workbook()
    build_inputs(wb.active, default[0], terms)
    build_reserve(wb.create_sheet("Reserve"))
    build_run_off(wb.create_sheet("Run-off"))
    build_checks(wb.create_sheet("Checks"), *default[1:])
    build_scenarios(wb.create_sheet("Scenarios"), results)
    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
