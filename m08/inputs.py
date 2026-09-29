"""Reading M08's inputs: the policy choices, the declared 2031 states, and
M07's path results.
"""

from pathlib import Path

from m05.inputs import INPUTS_DIR, MissingInput, read_csv
from m08.gift import check_share

CHOICES_FILE = "m08_policy_choices.csv"
STATES_FILE = "m08_states_2031.csv"
M07_FILE = "M07_path_summary.csv"
UNDECIDED = "UNDECIDED"

# state_id for M07 runs that start in 2027 instead of a declared 2031 state.
FROM_2027 = "FROM_2027"

M07_COLUMNS = [
    "run_id", "policy_id", "state_id", "path_id", "value_2031",
    "value_2033", "reserve_required", "reserve_gap", "facility_gift",
    "all_payments_success", "total_nominal_shortfall",
    "worst_single_shortfall",
]
M07_NUMBERS = [
    "value_2031", "value_2033", "reserve_required", "reserve_gap",
    "facility_gift", "total_nominal_shortfall", "worst_single_shortfall",
]


def load_choices(inputs_dir=INPUTS_DIR):
    """{parameter: row}. A blank value means the choice is not made yet."""
    choices = {}
    for row in read_csv(Path(inputs_dir) / CHOICES_FILE):
        choices[row["parameter"]] = {**row, "value": row["value"].strip()
                                     or None}
    return choices


def undecided(choices):
    return [name for name, row in choices.items() if row["value"] is None]


def gift_shares(choices):
    """The candidate gift shares, or [] if none are chosen yet."""
    raw = choices["gift_share_candidates"]["value"]
    if raw is None:
        return []
    shares = [float(x) for x in raw.split(";") if x.strip()]
    for share in shares:
        check_share(share)
    return shares


def policy_id(share):
    return f"share_{share:.2f}"


def load_states(inputs_dir=INPUTS_DIR):
    """The declared 2031 starting states. Declared before any M07 results
    are seen, never picked because of how they turn out."""
    return [{
        "state_id": row["state_id"],
        "information_date": row["information_date"],
        "value_2031": float(row["value_2031"]),
        "holdings": row["holdings"],
        "notes": row["notes"],
    } for row in read_csv(Path(inputs_dir) / STATES_FILE)]


def flag(text):
    return text.strip().upper() in ("TRUE", "1", "YES")


def load_m07_paths(inputs_dir=INPUTS_DIR):
    """One dict per M07 path. Raises MissingInput until the file arrives."""
    path = Path(inputs_dir) / M07_FILE
    if not path.exists():
        raise MissingInput(
            f"{M07_FILE} from M07 is not in inputs/ yet. Needed for the "
            f"2031 ranges and the policy comparison. Ask for one row per "
            f"path with these fields: {', '.join(M07_COLUMNS)}.")
    rows = read_csv(path)
    missing = [c for c in M07_COLUMNS if rows and c not in rows[0]]
    if not rows or missing:
        raise ValueError(f"{M07_FILE} is empty or missing: "
                         f"{', '.join(missing)}")
    paths = []
    for row in rows:
        p = dict(row)
        for name in M07_NUMBERS:
            p[name] = float(row[name])
        p["all_payments_success"] = flag(row["all_payments_success"])
        paths.append(p)
    return paths
