"""Run every scenario and write the M05 output files.

From the repo folder:
    python -m m05.run
"""

import argparse
import csv
import json
from pathlib import Path

from m05 import inputs
from m05.policy import draft_policy
from m05.reserve import form_reserve, run_off, summarize_run_off

MODEL_VERSION = "m05-0.1"
STATUS = "PROVISIONAL"
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

SCHEDULE_COLUMNS = [
    "scenario_id", "year", "balance_before_payment", "payment_due",
    "payment_funded", "shortfall", "balance_after_payment",
    "return_or_cash_receipts", "next_balance", "return_rate", "status",
    "model_version",
]

COMPARISON_COLUMNS = [
    "scenario_id", "reserve_required", "available_assets",
    "actual_reserve_transfer", "reserve_gap", "reserve_established",
    "first_payment_cash", "post_payment_reserve", "all_payments_funded",
    "first_shortfall_year", "total_shortfall", "sizing_yield",
    "runoff_return", "source_versions", "status",
]


def payment_terms(facts):
    """Payment amount, first year, and count, from the case facts."""
    first = facts["first_payment_year"]
    last = facts["last_payment_year"]
    return {
        "payment": facts["operating_payment"],
        "first_year": first,
        "n_payments": last - first + 1,
    }


def run_scenario(scenario, terms):
    """Size the reserve from the 2033 state, then run it off."""
    decision = form_reserve(scenario["available_2033"],
                            scenario["sizing_yield"],
                            terms["payment"], terms["n_payments"])
    returns = [scenario["runoff_return"]] * (terms["n_payments"] - 1)
    rows = run_off(decision["actual_reserve_transfer"], returns,
                   terms["payment"], terms["first_year"], terms["n_payments"])
    return decision, rows, summarize_run_off(rows)


def money(x):
    return f"{x:.2f}"


def flag(x):
    return "TRUE" if x else "FALSE"


def write_csv(path, columns, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def build(inputs_dir=inputs.INPUTS_DIR, out_dir=OUTPUTS_DIR):
    """Run all TEST scenarios and write the three output files. Returns
    the paths written."""
    inputs_dir, out_dir = Path(inputs_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    terms = payment_terms(inputs.load_case_facts(inputs_dir))
    source_versions = (
        f"case_facts.csv@{inputs.file_version(inputs_dir / 'case_facts.csv')}"
        f"; test_scenarios.csv@"
        f"{inputs.file_version(inputs_dir / 'test_scenarios.csv')}"
        f"; {MODEL_VERSION}")

    schedule, comparison = [], []
    for scenario in inputs.load_test_scenarios(inputs_dir):
        decision, rows, summary = run_scenario(scenario, terms)
        sid = scenario["scenario_id"]
        for r in rows:
            schedule.append({
                "scenario_id": sid,
                "year": r["year"],
                "balance_before_payment": money(r["balance_before_payment"]),
                "payment_due": money(r["payment_due"]),
                "payment_funded": money(r["payment_funded"]),
                "shortfall": money(r["shortfall"]),
                "balance_after_payment": money(r["balance_after_payment"]),
                "return_or_cash_receipts":
                    money(r["next_balance"] - r["balance_after_payment"]),
                "next_balance": money(r["next_balance"]),
                "return_rate": "" if r["return_rate"] is None
                               else r["return_rate"],
                "status": f"{STATUS} {scenario['status']}",
                "model_version": MODEL_VERSION,
            })
        first_year = summary["first_shortfall_year"]
        comparison.append({
            "scenario_id": sid,
            "reserve_required": money(decision["reserve_required"]),
            "available_assets": money(decision["available_assets"]),
            "actual_reserve_transfer":
                money(decision["actual_reserve_transfer"]),
            "reserve_gap": money(decision["reserve_gap"]),
            "reserve_established": flag(decision["reserve_established"]),
            "first_payment_cash": money(rows[0]["payment_funded"]),
            "post_payment_reserve": money(rows[0]["balance_after_payment"]),
            "all_payments_funded": flag(summary["all_payments_funded"]),
            "first_shortfall_year": "" if first_year is None else first_year,
            "total_shortfall": money(summary["total_shortfall"]),
            "sizing_yield": scenario["sizing_yield"],
            "runoff_return": scenario["runoff_return"],
            "source_versions": source_versions,
            "status": f"{STATUS} {scenario['status']}",
        })

    paths = {
        "schedule": out_dir / "M05_reserve_schedule.csv",
        "comparison": out_dir / "M05_reserve_comparison.csv",
        "policy": out_dir / "M05_reserve_policy.json",
    }
    write_csv(paths["schedule"], SCHEDULE_COLUMNS, schedule)
    write_csv(paths["comparison"], COMPARISON_COLUMNS, comparison)
    policy = draft_policy(terms, MODEL_VERSION, source_versions)
    with open(paths["policy"], "w", encoding="utf-8", newline="\n") as f:
        json.dump(policy, f, indent=2)
        f.write("\n")
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=OUTPUTS_DIR, type=Path,
                        help="folder for the output files")
    args = parser.parse_args()
    for path in build(out_dir=args.out).values():
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
