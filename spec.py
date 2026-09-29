"""The M08 policy specification: the rules M07 must run, written before
any simulation result is seen.
"""

from m08.inputs import (FROM_2027, M07_COLUMNS, M07_FILE, UNDECIDED,
                        gift_shares, policy_id, undecided)
from m08.ranges import RANGE_METHODS

DECIMAL_CHOICES = ("payment_success_target", "range_target_coverage")


def check_choices(choices):
    """Reject a choice that is filled in but not usable."""
    gift_shares(choices)
    for name in DECIMAL_CHOICES:
        value = choices[name]["value"]
        if value is not None and not 0 < float(value) < 1:
            raise ValueError(f"{name} must be between 0 and 1, got {value}")
    method = choices["range_method"]["value"]
    if method is not None and method not in RANGE_METHODS:
        raise ValueError(f"range_method must be one of {RANGE_METHODS}")


def field(choices, name):
    row = choices[name]
    if row["value"] is None:
        return {"value": None, "status": UNDECIDED, "owner": row["owner"],
                "options": row["options"]}
    value = row["value"]
    if name in DECIMAL_CHOICES:
        value = float(value)
    return {"value": value, "status": "SET", "owner": row["owner"]}


def build_spec(choices, states, model_version, source_versions):
    check_choices(choices)
    open_choices = undecided(choices)
    if not states:
        open_choices.append("states_2031")
    shares = gift_shares(choices)
    return {
        "policy_id": "M08-facility-contribution",
        "version": model_version,
        "status": "DRAFT: choices undecided" if open_choices
                  else "READY FOR M07",
        "undecided": open_choices,
        "source_versions": source_versions,
        "observed_inputs_2033": [
            "available_2033: portfolio value before the reserve, the first "
            "payment, and any gift",
            "reserve_required: from M05's sizing rule",
        ],
        "reserve_priority": field(choices, "reserve_priority"),
        "gift_rule": {
            "formula": "facility_gift = share * max(0, available_2033 - "
                       "reserve_required)",
            "retained_flexibility": "(1 - share) * max(0, available_2033 - "
                                    "reserve_required)",
            "notes": "reserve_required already includes the immediate 2033 "
                     "payment, so it is not subtracted again. The gift "
                     "leaves the portfolio for good and never funds a later "
                     "payment.",
        },
        "candidate_policies": [
            {"policy_id": policy_id(s), "gift_share": s} for s in shares
        ] or field(choices, "gift_share_candidates"),
        "constraints": [
            "0 <= share <= 1",
            "No gift while the reserve gap is above zero",
            "No gift is ever negative",
            "No outside money for operating payments",
        ],
        "underfunding_response": field(choices, "underfunding_response"),
        "top_up_policy": field(choices, "top_up_policy"),
        "payment_success_target": field(choices, "payment_success_target"),
        "range_method": field(choices, "range_method"),
        "range_target_coverage": field(choices, "range_target_coverage"),
        "information_date_2031": field(choices, "information_date_2031"),
        "states_2031": states or {
            "value": None, "status": UNDECIDED, "owner": "P1 and P4",
            "options": "Declare each 2031 starting state in "
                       "inputs/m08_states_2031.csv before seeing any M07 "
                       "result",
        },
        "m07_request": {
            "file": M07_FILE,
            "fields": M07_COLUMNS,
            "notes": [
                "One row per path. Keep every path, including failed "
                "payments and zero gifts.",
                "Use the policy_id values in candidate_policies.",
                f"Use state_id {FROM_2027} for runs that start in 2027, and "
                "the declared state_id for runs that start in 2031.",
                "Apply the gift rule above in 2033, after the reserve is "
                "formed.",
            ],
        },
    }
