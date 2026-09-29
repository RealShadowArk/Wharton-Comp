"""Acceptance tests for M08.

M07 does not exist yet, so the path results here are a small FAKE set
with round numbers, built to make each rule easy to check by hand.
"""

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from m05.inputs import INPUTS_DIR, MissingInput, load_team_file, read_csv
from m05.reserve import required_reserve
from m08 import inputs
from m08.gift import facility_gift, split_2033
from m08.ranges import (check_state, gift_range, policy_outcomes,
                        quantile)
from m08.run import build

# FAKE M07 output: ten paths from one declared 2031 state, gift share 0.5,
# a 440,000 required reserve. The two poorest paths also miss payments.
FAKE_VALUES_2033 = [400_000, 420_000, 440_000, 460_000, 480_000,
                    500_000, 520_000, 540_000, 560_000, 580_000]
FAKE_REQUIRED = 440_000
FAKE_SHARE = 0.5


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fake_paths(share=FAKE_SHARE, state_id="S_MID", value_2031=500_000):
    paths = []
    for i, v in enumerate(FAKE_VALUES_2033):
        gap = max(0, FAKE_REQUIRED - v)
        paths.append({
            "run_id": "FAKE", "policy_id": inputs.policy_id(share),
            "state_id": state_id, "path_id": f"p{i}",
            "value_2031": value_2031, "value_2033": v,
            "reserve_required": FAKE_REQUIRED, "reserve_gap": gap,
            "facility_gift": facility_gift(v, FAKE_REQUIRED, share),
            "all_payments_success": gap == 0,
            "total_nominal_shortfall": 50_000 if gap else 0,
            "worst_single_shortfall": 50_000 if gap else 0,
        })
    return paths


def write_inputs(folder, choices=None, states=None, paths=None):
    """Copy the real choice files into folder, then override some."""
    for name in (inputs.CHOICES_FILE, inputs.STATES_FILE):
        shutil.copy(Path(INPUTS_DIR) / name, Path(folder) / name)
    if choices:
        rows = read_csv(Path(folder) / inputs.CHOICES_FILE)
        for row in rows:
            if row["parameter"] in choices:
                row["value"] = choices[row["parameter"]]
        with open(Path(folder) / inputs.CHOICES_FILE, "w", newline="",
                  encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    if states:
        with open(Path(folder) / inputs.STATES_FILE, "w", newline="",
                  encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "state_id", "information_date", "value_2031", "holdings",
                "notes"])
            writer.writeheader()
            writer.writerows(states)
    if paths:
        with open(Path(folder) / inputs.M07_FILE, "w", newline="",
                  encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=inputs.M07_COLUMNS)
            writer.writeheader()
            for p in paths:
                writer.writerow({**p, "all_payments_success":
                                 "TRUE" if p["all_payments_success"]
                                 else "FALSE"})


FILLED = {
    "gift_share_candidates": "0.5",
    "payment_success_target": "0.95",
    "range_method": "equal_tail",
    "range_target_coverage": "0.8",
    "information_date_2031": "2031-01-01",
    "top_up_policy": "none",
}
FAKE_STATE = {"state_id": "S_MID", "information_date": "2031-01-01",
              "value_2031": "500000", "holdings": "FAKE",
              "notes": "test only"}


class GiftRuleTests(unittest.TestCase):
    # Guide tests: residual arithmetic, underfunded reserve, and
    # irreversible outflow.

    def test_gift_and_retained_add_up_to_the_leftover(self):
        required = required_reserve(0.03)
        split = split_2033(593_470.93, required, 0.5)
        self.assertAlmostEqual(split["leftover"], 154_165.48, places=2)
        self.assertAlmostEqual(split["facility_gift"], 77_082.74, places=2)
        self.assertAlmostEqual(
            split["facility_gift"] + split["retained_flexibility"],
            split["leftover"])

    def test_first_payment_is_not_subtracted_twice(self):
        # The required reserve already holds the 2033 payment. At 0% with
        # $500,000 there is nothing left over, not -$50,000.
        split = split_2033(500_000, required_reserve(0.0), 1.0)
        self.assertEqual(split["leftover"], 0)
        self.assertEqual(split["facility_gift"], 0)

    def test_short_portfolio_gives_nothing_and_shows_the_gap(self):
        split = split_2033(400_000, 440_000, 1.0)
        self.assertEqual(split["facility_gift"], 0)
        self.assertEqual(split["retained_flexibility"], 0)
        self.assertEqual(split["reserve_gap"], 40_000)
        self.assertFalse(split["reserve_established"])

    def test_every_2033_dollar_is_accounted_for_once(self):
        for available in (0, 400_000, 440_000, 600_000):
            for share in (0, 0.3, 1):
                s = split_2033(available, 440_000, share)
                self.assertAlmostEqual(
                    s["actual_reserve_transfer"] + s["retained_flexibility"]
                    + s["facility_gift"], available)
                self.assertAlmostEqual(
                    s["assets_after_gift"], available - s["facility_gift"])

    def test_share_outside_zero_to_one_is_rejected(self):
        for share in (-0.1, 1.1):
            with self.assertRaises(ValueError):
                facility_gift(600_000, 440_000, share)


class QuantileTests(unittest.TestCase):

    def test_equal_tail_on_one_to_one_hundred(self):
        r = gift_range(list(range(1, 101)), "equal_tail", 0.9)
        self.assertEqual((r["lower_bound"], r["upper_bound"]), (5, 95))
        self.assertAlmostEqual(r["achieved_coverage"], 0.91)

    def test_bounds_are_values_that_occurred(self):
        values = [0, 0, 0, 12_345.67, 50_000, 99_999.99]
        self.assertIn(quantile(values, 0.37), values)

    def test_floating_point_does_not_shift_the_position(self):
        self.assertEqual(quantile(list(range(1, 101)), 0.07), 7)

    def test_one_sided_minimum_has_no_upper_bound(self):
        r = gift_range(list(range(1, 101)), "one_sided_minimum", 0.9)
        self.assertEqual(r["lower_bound"], 10)
        self.assertIsNone(r["upper_bound"])
        self.assertGreaterEqual(r["achieved_coverage"], 0.9)

    def test_bad_coverage_or_method_is_rejected(self):
        with self.assertRaises(ValueError):
            gift_range([1, 2], "equal_tail", 1.0)
        with self.assertRaises(ValueError):
            gift_range([1, 2], "middle_half", 0.5)


class PathSetTests(unittest.TestCase):
    # Guide tests: complete conditional sample, coverage versus funding,
    # and the 2031 information boundary.

    def test_every_path_counts_including_failures_and_zero_gifts(self):
        paths = fake_paths()
        r = gift_range([p["facility_gift"] for p in paths], "equal_tail", 0.8)
        self.assertEqual(r["n_paths"], 10)
        self.assertAlmostEqual(r["zero_gift_frequency"], 0.3)
        self.assertEqual((r["lower_bound"], r["upper_bound"]), (0, 60_000))
        self.assertAlmostEqual(r["achieved_coverage"], 0.9)

    def test_gift_range_and_payment_success_are_separate(self):
        out = policy_outcomes(fake_paths(), FAKE_SHARE)
        self.assertAlmostEqual(out["all_payments_success_rate"], 0.8)
        self.assertAlmostEqual(out["reserve_not_established_rate"], 0.2)
        self.assertEqual(out["gift_rule_mismatches"], 0)

    def test_gift_that_breaks_the_rule_is_flagged(self):
        paths = fake_paths()
        paths[9]["facility_gift"] += 1_000
        self.assertEqual(policy_outcomes(paths, FAKE_SHARE)
                         ["gift_rule_mismatches"], 1)

    def test_state_must_start_from_its_declared_balance(self):
        paths = fake_paths()
        check_state(paths, "S_MID", 500_000)
        paths[3]["value_2031"] = 510_000
        with self.assertRaises(ValueError):
            check_state(paths, "S_MID", 500_000)


class RunnerTests(unittest.TestCase):

    def test_repo_inputs_give_a_draft_spec_and_wait_for_m07(self):
        with tempfile.TemporaryDirectory() as tmp:
            written, notes = build(out_dir=tmp)
            spec = read_json(written["spec"])
            checks = read_csv(written["checks"])
        self.assertEqual(spec["status"], "DRAFT: choices undecided")
        self.assertIn("gift_share_candidates", spec["undecided"])
        self.assertIn("states_2031", spec["undecided"])
        self.assertNotIn("comparison", written)
        self.assertTrue(any(inputs.M07_FILE in n for n in notes))
        self.assertEqual({r["case_id"] for r in checks},
                         {"ENOUGH", "EXACT", "SHORT", "EMPTY"})
        self.assertTrue(all(r["status"] == "HYPOTHETICAL" for r in checks))

    def test_missing_m07_file_names_the_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(MissingInput) as caught:
                inputs.load_m07_paths(tmp)
        self.assertIn("facility_gift", str(caught.exception))

    def test_changed_choices_change_the_spec_version(self):
        # Guide test: policy dependency. A revised rule gets a new
        # fingerprint instead of silently replacing the old one.
        versions = []
        for choices in (None, FILLED):
            with tempfile.TemporaryDirectory() as tmp:
                write_inputs(tmp, choices=choices)
                written, _ = build(inputs_dir=tmp, out_dir=tmp)
                spec = read_json(written["spec"])
            versions.append(spec["source_versions"])
        self.assertNotEqual(versions[0], versions[1])

    def test_full_run_on_fake_m07_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_inputs(tmp, choices=FILLED, states=[FAKE_STATE],
                         paths=fake_paths())
            written, notes = build(inputs_dir=tmp, out_dir=tmp)
            spec = read_json(written["spec"])
            ranges = read_csv(written["ranges"])
            comparison = read_csv(written["comparison"])
            checks = read_csv(written["checks"])
        self.assertEqual(spec["status"], "READY FOR M07")
        self.assertEqual(notes, [])
        row = ranges[0]
        self.assertEqual((row["lower_bound"], row["upper_bound"]),
                         ("0.00", "60000.00"))
        self.assertEqual(row["achieved_coverage"], "0.9000")
        self.assertEqual(row["zero_gift_frequency"], "0.3000")
        self.assertEqual(row["payment_success_rate"], "0.8000")
        self.assertIn(inputs.M07_FILE, row["input_versions"])
        self.assertEqual(comparison[0]["gift_rule_mismatches"], "0")
        enough = next(r for r in checks if r["case_id"] == "ENOUGH")
        self.assertEqual(enough["facility_gift"], "80000.00")
        self.assertEqual(enough["retained_flexibility"], "80000.00")

    def test_spec_has_the_fields_m05_reads(self):
        with tempfile.TemporaryDirectory() as tmp:
            # The spec is written under the same name M05 looks for.
            build(out_dir=tmp)
            spec = load_team_file("M08", tmp)
        self.assertEqual(spec["reserve_priority"]["status"], "SET")

    def test_undeclared_state_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_inputs(tmp, choices=FILLED, states=[FAKE_STATE],
                         paths=fake_paths(state_id="S_PICKED_LATER"))
            with self.assertRaises(ValueError):
                build(inputs_dir=tmp, out_dir=tmp)


if __name__ == "__main__":
    unittest.main()
