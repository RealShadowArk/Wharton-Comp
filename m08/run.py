"""Write the M08 files: the policy specification and hypothetical check
cases always, and the 2031 ranges and policy comparison once M07's path
file is in inputs/.

From the repo folder:
    python -m m08.run
"""

import argparse
import json
from pathlib import Path

from m05.inputs import INPUTS_DIR, MissingInput, file_version
from m05.run import OUTPUTS_DIR, flag, money, write_csv
from m08 import inputs
from m08.gift import split_2033
from m08.ranges import check_state, gift_range, policy_outcomes
from m08.spec import build_spec

MODEL_VERSION = "m08-0.1"
STATUS = "PROVISIONAL"

# Round numbers for hand-checking the rule. Not projections.
HYPOTHETICAL_REQUIRED = 440_000
CHECK_CASES = [
    ("ENOUGH", "More than enough for the reserve", 600_000),
    ("EXACT", "Exactly enough for the reserve", 440_000),
    ("SHORT", "Not enough for the reserve", 400_000),
    ("EMPTY", "Nothing available", 0),
]

CHECK_COLUMNS = [
    "case_id", "description", "available_2033", "reserve_required",
    "leftover", "reserve_gap", "reserve_established", "policy_id",
    "gift_share", "facility_gift", "retained_flexibility",
    "assets_after_gift", "status",
]
COMPARISON_COLUMNS = [
    "policy_id", "gift_share", "state_id", "n_paths",
    "reserve_not_established_rate", "gift_mean", "gift_p10", "gift_median",
    "gift_p90", "retained_median", "all_payments_success_rate",
    "mean_total_shortfall", "worst_single_shortfall",
    "gift_rule_mismatches", "input_versions", "status",
]
RANGE_COLUMNS = [
    "policy_id", "state_id", "information_date", "value_2031",
    "range_method", "target_coverage", "lower_bound", "upper_bound",
    "achieved_coverage", "zero_gift_frequency", "payment_success_rate",
    "n_paths", "input_versions", "status",
]


def rate(x):
    return f"{x:.4f}"


def check_rows(shares):
    """The guide's hand-over table: each case under each candidate share."""
    rows = []
    for case_id, description, available in CHECK_CASES:
        for share in shares or [None]:
            split = split_2033(available, HYPOTHETICAL_REQUIRED, share or 0)
            decided = share is not None
            rows.append({
                "case_id": case_id,
                "description": description,
                "available_2033": money(available),
                "reserve_required": money(HYPOTHETICAL_REQUIRED),
                "leftover": money(split["leftover"]),
                "reserve_gap": money(split["reserve_gap"]),
                "reserve_established": flag(split["reserve_established"]),
                "policy_id": inputs.policy_id(share) if decided
                             else inputs.UNDECIDED,
                "gift_share": share if decided else "",
                "facility_gift": money(split["facility_gift"])
                                 if decided else "",
                "retained_flexibility":
                    money(split["retained_flexibility"]) if decided else "",
                "assets_after_gift": money(split["assets_after_gift"])
                                     if decided else "",
                "status": "HYPOTHETICAL",
            })
    return rows


def pass_b(paths, choices, states, versions):
    """Policy comparison for every (policy, state), and 2031 ranges for
    every declared state."""
    shares = {inputs.policy_id(s): s for s in inputs.gift_shares(choices)}
    declared = {s["state_id"]: s for s in states}
    groups = {}
    for p in paths:
        if p["policy_id"] not in shares:
            raise ValueError(f"path {p['path_id']} uses {p['policy_id']}, "
                             f"which is not a declared candidate policy")
        if p["state_id"] != inputs.FROM_2027 and \
                p["state_id"] not in declared:
            raise ValueError(f"path {p['path_id']} starts from "
                             f"{p['state_id']}, which is not a declared "
                             f"2031 state")
        groups.setdefault((p["policy_id"], p["state_id"]), []).append(p)

    method = choices["range_method"]["value"]
    coverage = float(choices["range_target_coverage"]["value"])
    comparison, ranges = [], []
    for (pid, sid), group in sorted(groups.items()):
        out = policy_outcomes(group, shares[pid])
        comparison.append({
            "policy_id": pid, "gift_share": shares[pid], "state_id": sid,
            "n_paths": out["n_paths"],
            "reserve_not_established_rate":
                rate(out["reserve_not_established_rate"]),
            **{k: money(out[k]) for k in (
                "gift_mean", "gift_p10", "gift_median", "gift_p90",
                "retained_median", "mean_total_shortfall",
                "worst_single_shortfall")},
            "all_payments_success_rate":
                rate(out["all_payments_success_rate"]),
            "gift_rule_mismatches": out["gift_rule_mismatches"],
            "input_versions": versions, "status": STATUS,
        })
        if sid == inputs.FROM_2027:
            continue
        state = declared[sid]
        check_state(group, sid, state["value_2031"])
        r = gift_range([p["facility_gift"] for p in group], method, coverage)
        ranges.append({
            "policy_id": pid, "state_id": sid,
            "information_date": state["information_date"],
            "value_2031": money(state["value_2031"]),
            "range_method": method, "target_coverage": coverage,
            "lower_bound": money(r["lower_bound"]),
            "upper_bound": "" if r["upper_bound"] is None
                           else money(r["upper_bound"]),
            "achieved_coverage": rate(r["achieved_coverage"]),
            "zero_gift_frequency": rate(r["zero_gift_frequency"]),
            "payment_success_rate": rate(out["all_payments_success_rate"]),
            "n_paths": r["n_paths"],
            "input_versions": versions, "status": STATUS,
        })
    return comparison, ranges


def build(inputs_dir=INPUTS_DIR, out_dir=OUTPUTS_DIR):
    """Write what can be written now. Returns (paths written, notes)."""
    inputs_dir, out_dir = Path(inputs_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    choices = inputs.load_choices(inputs_dir)
    states = inputs.load_states(inputs_dir)
    names = [inputs.CHOICES_FILE, inputs.STATES_FILE]
    if (inputs_dir / inputs.M07_FILE).exists():
        names.append(inputs.M07_FILE)
    versions = "; ".join(
        [f"{n}@{file_version(inputs_dir / n)}" for n in names]
        + [MODEL_VERSION])

    written, notes = {}, []
    spec = build_spec(choices, states, MODEL_VERSION, versions)
    written["spec"] = out_dir / "M08_policy_specification.json"
    with open(written["spec"], "w", encoding="utf-8", newline="\n") as f:
        json.dump(spec, f, indent=2)
        f.write("\n")
    written["checks"] = out_dir / "M08_policy_check_cases.csv"
    write_csv(written["checks"], CHECK_COLUMNS,
              check_rows(inputs.gift_shares(choices)))
    if spec["undecided"]:
        notes.append("Undecided: " + ", ".join(spec["undecided"]))

    try:
        paths = inputs.load_m07_paths(inputs_dir)
    except MissingInput as missing:
        notes.append(str(missing))
        return written, notes
    blocking = [n for n in ("gift_share_candidates", "range_method",
                            "range_target_coverage")
                if choices[n]["value"] is None]
    if blocking:
        notes.append("M07 paths found, but ranges need: "
                     + ", ".join(blocking))
        return written, notes
    comparison, ranges = pass_b(paths, choices, states, versions)
    written["comparison"] = out_dir / "M08_contribution_comparison.csv"
    write_csv(written["comparison"], COMPARISON_COLUMNS, comparison)
    written["ranges"] = out_dir / "M08_2031_ranges.csv"
    write_csv(written["ranges"], RANGE_COLUMNS, ranges)
    return written, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=OUTPUTS_DIR, type=Path,
                        help="folder for the output files")
    args = parser.parse_args()
    written, notes = build(out_dir=args.out)
    for path in written.values():
        print(f"wrote {path}")
    for note in notes:
        print(note)


if __name__ == "__main__":
    main()
