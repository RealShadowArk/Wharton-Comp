"""Tests for the output files the runner writes."""

import json
import tempfile
import unittest

from m05 import inputs
from m05.run import COMPARISON_COLUMNS, SCHEDULE_COLUMNS, build


class OutputTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        paths = build(out_dir=cls.tmp.name)
        cls.schedule = inputs.read_csv(paths["schedule"])
        cls.comparison = {r["scenario_id"]: r
                          for r in inputs.read_csv(paths["comparison"])}
        with open(paths["policy"], encoding="utf-8") as f:
            cls.policy = json.load(f)
        cls.scenario_ids = [s["scenario_id"]
                            for s in inputs.load_test_scenarios()]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_schedule_has_the_guide_columns(self):
        self.assertEqual(list(self.schedule[0]), SCHEDULE_COLUMNS)

    def test_schedule_has_ten_rows_per_scenario(self):
        for sid in self.scenario_ids:
            rows = [r for r in self.schedule if r["scenario_id"] == sid]
            self.assertEqual([int(r["year"]) for r in rows],
                             list(range(2033, 2043)))

    def test_every_row_is_labeled_provisional(self):
        for row in self.schedule + list(self.comparison.values()):
            self.assertIn("PROVISIONAL", row["status"])

    def test_no_negative_balance_in_any_scenario(self):
        for row in self.schedule:
            self.assertGreaterEqual(float(row["balance_after_payment"]), 0)
            self.assertGreaterEqual(float(row["next_balance"]), 0)

    def test_comparison_has_the_guide_columns(self):
        row = next(iter(self.comparison.values()))
        self.assertEqual(list(row), COMPARISON_COLUMNS)

    def test_ledger_case_in_comparison(self):
        row = self.comparison["TEST_Y0_A450"]
        self.assertEqual(row["reserve_required"], "500000.00")
        self.assertEqual(row["actual_reserve_transfer"], "450000.00")
        self.assertEqual(row["reserve_gap"], "50000.00")
        self.assertEqual(row["reserve_established"], "FALSE")
        self.assertEqual(row["first_payment_cash"], "50000.00")
        self.assertEqual(row["post_payment_reserve"], "400000.00")
        self.assertEqual(row["first_shortfall_year"], "2042")
        self.assertEqual(row["total_shortfall"], "50000.00")

    def test_reinvestment_case_in_comparison(self):
        row = self.comparison["TEST_Y3_R1_A593"]
        self.assertEqual(row["reserve_established"], "TRUE")
        self.assertEqual(row["all_payments_funded"], "FALSE")

    def test_rows_name_their_input_versions(self):
        for row in self.comparison.values():
            self.assertIn("case_facts.csv@", row["source_versions"])
            self.assertIn("test_scenarios.csv@", row["source_versions"])

    def test_policy_leaves_human_choices_undecided(self):
        for key in ["asset_composition", "payment_order", "rebalancing_rule",
                    "top_up_rule", "high_certainty_definition"]:
            self.assertEqual(self.policy[key]["status"], "UNDECIDED")
            self.assertIsNone(self.policy[key]["value"])
        self.assertEqual(self.policy["sizing_rule"]["sizing_yield"]["status"],
                         "UNDECIDED")

    def test_policy_matches_case_payments(self):
        self.assertEqual(self.policy["payments"]["amount"], 50_000)
        self.assertEqual(self.policy["payments"]["count"], 10)
        self.assertEqual(self.policy["payments"]["first_year"], 2033)


if __name__ == "__main__":
    unittest.main()
