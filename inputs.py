"""Reading the model's input files.

Case facts and TEST scenarios live in inputs/. Teammates' files go in the
same folder under the names in TEAM_FILES. Until a file arrives, its loader
raises MissingInput saying who owns it and which fields to ask for.
"""

import csv
import hashlib
import json
from pathlib import Path

INPUTS_DIR = Path(__file__).resolve().parent.parent / "inputs"


class MissingInput(Exception):
    """A teammate's file the model needs has not arrived yet."""


# The fields each teammate file must have. These are proposals to confirm
# with each owner, not an agreed schema.
TEAM_FILES = {
    "M01": {
        "file": "M01_cashflows.csv",
        "owner": "P1 (M01 cash-flow ledger)",
        "columns": ["scenario_id", "year", "payment_required",
                    "available_before_reserve", "version"],
        "use": "the start-2033 portfolio value for each scenario, and the "
               "payment schedule",
    },
    "M02": {
        "file": "M02_assumptions.csv",
        "owner": "P2 (M02 macro assumptions)",
        "columns": ["scenario_id", "year", "sizing_yield", "reserve_return",
                    "fee_rate", "source", "retrieval_date", "version",
                    "status"],
        "use": "sourced reserve yields and reserve returns for 2033 to 2041",
    },
    "M04": {
        "file": "M04_reserve_instrument_terms.csv",
        "owner": "P3 (M04 exposures and baseline portfolios)",
        "columns": ["instrument_id", "instrument_type", "price", "price_date",
                    "coupon_rate", "maturity_date", "cost",
                    "eligible_in_wins", "source_id"],
        "use": "instrument cash flows that replace the flat-return shortcut",
    },
    "M08": {
        "file": "M08_policy_specification.json",
        "owner": "P1 (M08 facility contribution policy)",
        "columns": ["version", "reserve_priority", "top_up_policy",
                    "underfunding_response"],
        "use": "reserve priority and any permitted top-up rule",
    },
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def file_version(path):
    """Short fingerprint of a file's contents, so every output row can say
    exactly which input version produced it. Line endings are ignored."""
    data = Path(path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()[:8]


def load_case_facts(inputs_dir=INPUTS_DIR):
    """Case facts as {name: number}."""
    facts = {}
    for row in read_csv(Path(inputs_dir) / "case_facts.csv"):
        value = float(row["value"])
        facts[row["name"]] = int(value) if value.is_integer() else value
    return facts


def load_test_scenarios(inputs_dir=INPUTS_DIR):
    """TEST scenarios: flat illustrative rates, not sourced assumptions."""
    scenarios = []
    for row in read_csv(Path(inputs_dir) / "test_scenarios.csv"):
        if row["status"] != "TEST":
            raise ValueError(
                f"{row['scenario_id']}: test_scenarios.csv holds TEST rows "
                f"only; sourced rates belong in M02_assumptions.csv")
        scenarios.append({
            "scenario_id": row["scenario_id"],
            "sizing_yield": float(row["sizing_yield"]),
            "runoff_return": float(row["runoff_return"]),
            "available_2033": float(row["available_2033"]),
            "status": row["status"],
            "note": row["note"],
        })
    return scenarios


def load_team_file(module, inputs_dir=INPUTS_DIR):
    """Rows from a teammate's file, after checking it has every field the
    model needs. Raises MissingInput if the file is not there yet."""
    spec = TEAM_FILES[module]
    path = Path(inputs_dir) / spec["file"]
    if not path.exists():
        raise MissingInput(
            f"{spec['file']} from {spec['owner']} is not in inputs/ yet. "
            f"Needed for {spec['use']}. Ask for these fields: "
            f"{', '.join(spec['columns'])}.")
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        present = set(data)
    else:
        data = read_csv(path)
        present = set(data[0]) if data else set()
    missing = [c for c in spec["columns"] if c not in present]
    if missing:
        raise ValueError(
            f"{spec['file']} is missing: {', '.join(missing)}")
    return data
