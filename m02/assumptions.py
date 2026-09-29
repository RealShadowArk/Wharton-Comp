"""Reading P2's M02 assumptions file, the single source of model inputs.

inputs/M02_assumptions.csv is in long format: one row per assumption and
case (LOW, BASE, HIGH) or per scenario path value (S0-S8). Every row keeps
its status (CASE, RESEARCH, ASSUMPTION) and source IDs, so any number a
model uses can be traced back to where it came from.
"""

import math
from pathlib import Path

from m05.inputs import INPUTS_DIR, file_version, read_csv

M02_FILE = "M02_assumptions.csv"
COLUMNS = ["assumption_id", "scenario_id", "asset_id", "measure", "value",
           "unit", "frequency", "as_of", "source_id", "status",
           "input_version"]
STATUSES = {"CASE", "RESEARCH", "ASSUMPTION", "TEST"}
CASES = ("LOW", "BASE", "HIGH")

# Which end of each range is worse for Laura (M02 Assumptions_Register,
# "Worse end for Laura"). The pessimistic run takes the worse end of every
# input at once.
WORSE_END = {"A-01": "LOW", "A-02": "LOW", "A-05": "HIGH", "A-06": "LOW",
             "A-08": "LOW", "A-09": "LOW"}

# Structure model cells fed by M02 (M02 Model_Input_Map). Safety margin,
# option choice, m, stock cap and tilts are M08 policy choices, not M02.
MODEL_INPUT_MAP = [
    ("Inputs!B13", "bond_yield", "A-01"),
    ("Inputs!B14", "reserve_yield_2033", "A-02"),
    ("Inputs!B16", "stock_arithmetic_return", "A-06"),
    ("Inputs!B17", "stock_volatility", "A-05"),
    ("Inputs!B28", "crash_size", "A-08"),
    ("Inputs!B29", "severe_crash_size", "A-09"),
]


class Assumption:
    """One M02 input with its LOW / BASE / HIGH values and provenance."""

    def __init__(self, assumption_id, measure, unit, status, source_ids,
                 as_of):
        self.id = assumption_id
        self.measure = measure
        self.unit = unit
        self.status = status
        self.source_ids = source_ids
        self.as_of = as_of
        self.values = {}

    def value(self, case="BASE"):
        return self.values[case]

    def __repr__(self):
        return f"Assumption({self.id}, {self.values}, {self.status})"


def _check_rows(rows):
    if not rows:
        raise ValueError(f"{M02_FILE} is empty")
    missing = [c for c in COLUMNS if c not in rows[0]]
    if missing:
        raise ValueError(f"{M02_FILE} is missing: {', '.join(missing)}")
    for row in rows:
        if row["status"] not in STATUSES:
            raise ValueError(
                f"{row['assumption_id']}/{row['scenario_id']}: status "
                f"{row['status']!r} is not one of {sorted(STATUSES)}")


def load_m02(inputs_dir=INPUTS_DIR):
    """All of M02, as {"assumptions", "scenarios", "run_stamp"}.

    assumptions: {id: Assumption} for the C-, A- and M- rows.
    scenarios: {scenario_id: {"returns": {year: r}, "reserve_yield_2033": y}}.
    run_stamp: the file's input_version and content fingerprint, to be
    written next to every result.
    """
    path = Path(inputs_dir) / M02_FILE
    rows = read_csv(path)
    _check_rows(rows)

    assumptions, scenarios = {}, {}
    for row in rows:
        value = float(row["value"])
        if row["assumption_id"].startswith("SCN-"):
            path_ = scenarios.setdefault(
                row["scenario_id"], {"returns": {}, "reserve_yield_2033": None})
            measure = row["measure"]
            if measure.startswith("core_total_return_"):
                path_["returns"][int(measure.rsplit("_", 1)[1])] = value
            elif measure == "reserve_yield_2033":
                path_["reserve_yield_2033"] = value
            else:
                raise ValueError(f"unknown scenario measure {measure!r}")
            continue
        a = assumptions.get(row["assumption_id"])
        if a is None:
            a = assumptions[row["assumption_id"]] = Assumption(
                row["assumption_id"], row["measure"], row["unit"],
                row["status"],
                [s.strip() for s in row["source_id"].split(";")],
                row["as_of"])
        a.values[row["scenario_id"]] = value

    for a in assumptions.values():
        missing = [c for c in CASES if c not in a.values]
        if missing:
            raise ValueError(f"{a.id} has no {', '.join(missing)} value")

    versions = {row["input_version"] for row in rows}
    if len(versions) != 1:
        raise ValueError(f"{M02_FILE} mixes versions: {sorted(versions)}")
    run_stamp = {"input_version": versions.pop(),
                 "file_version": file_version(path)}
    return {"assumptions": assumptions, "scenarios": scenarios,
            "run_stamp": run_stamp}


def geometric_to_arithmetic(geometric, volatility):
    """Arithmetic mean return for a lognormal return whose median (compound)
    return is `geometric`. Same formula as M02 A-06:
    (1+g) x sqrt((1 + sqrt(1 + 4 v^2 / (1+g)^2)) / 2) - 1."""
    g1 = 1 + geometric
    return g1 * math.sqrt((1 + math.sqrt(1 + 4 * volatility ** 2 / g1 ** 2))
                          / 2) - 1


def model_inputs(m02, case="BASE"):
    """Values to type into the structure model for one case.

    case is "BASE", "PESSIMISTIC" (worse end of every input) or
    "OPTIMISTIC" (better end). Returns {cell: {name, value, from, status}}.
    """
    assumptions = m02["assumptions"]
    out = {}
    for cell, name, aid in MODEL_INPUT_MAP:
        a = assumptions[aid]
        if case == "BASE":
            pick = "BASE"
        elif case in ("PESSIMISTIC", "OPTIMISTIC"):
            worse = WORSE_END[aid]
            better = "HIGH" if worse == "LOW" else "LOW"
            pick = worse if case == "PESSIMISTIC" else better
        else:
            raise ValueError(f"unknown case {case!r}")
        out[cell] = {"name": name, "value": a.value(pick),
                     "from": f"{aid} {pick}", "status": a.status}
    return out
