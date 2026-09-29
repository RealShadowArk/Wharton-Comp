"""Tests for the input files and the teammate-file loaders."""

import tempfile
import unittest
from pathlib import Path

from m05 import inputs, reserve


class CaseFactTests(unittest.TestCase):

    def test_case_facts_match_the_model_defaults(self):
        facts = inputs.load_case_facts()
        self.assertEqual(facts["operating_payment"], reserve.PAYMENT)
        self.assertEqual(facts["first_payment_year"],
                         reserve.FIRST_PAYMENT_YEAR)
        count = facts["last_payment_year"] - facts["first_payment_year"] + 1
        self.assertEqual(count, reserve.N_PAYMENTS)

    def test_contributions_total_450000(self):
        facts = inputs.load_case_facts()
        self.assertEqual(facts["contribution_1"] + facts["contribution_2"],
                         450_000)


class TestScenarioTests(unittest.TestCase):

    def test_every_scenario_is_labeled_test(self):
        for s in inputs.load_test_scenarios():
            self.assertEqual(s["status"], "TEST")
            self.assertTrue(s["scenario_id"].startswith("TEST_"))

    def test_5pct_portfolio_matches_its_formula(self):
        # 300,000 grows for six years and 150,000 for five, at 5%.
        expected = 300_000 * 1.05 ** 6 + 150_000 * 1.05 ** 5
        values = {s["scenario_id"]: s["available_2033"]
                  for s in inputs.load_test_scenarios()}
        self.assertAlmostEqual(values["TEST_Y3_A593"], expected, places=1)

    def test_zero_accumulation_portfolio_is_the_contributions(self):
        values = {s["scenario_id"]: s["available_2033"]
                  for s in inputs.load_test_scenarios()}
        self.assertEqual(values["TEST_Y0_A450"], 450_000)


class TeamFileTests(unittest.TestCase):

    def test_missing_file_says_what_to_ask_for(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(inputs.MissingInput) as caught:
                inputs.load_team_file("M02", tmp)
        message = str(caught.exception)
        self.assertIn("M02_assumptions.csv", message)
        self.assertIn("sizing_yield", message)

    def test_file_missing_a_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "M01_cashflows.csv").write_text(
                "scenario_id,year\nTEST,2033\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                inputs.load_team_file("M01", tmp)

    def test_complete_file_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "M01_cashflows.csv").write_text(
                "scenario_id,year,payment_required,available_before_reserve,"
                "version\nTEST,2033,50000,450000,v1\n", encoding="utf-8")
            rows = inputs.load_team_file("M01", tmp)
        self.assertEqual(rows[0]["available_before_reserve"], "450000")


if __name__ == "__main__":
    unittest.main()
