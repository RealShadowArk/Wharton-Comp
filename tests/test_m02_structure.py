"""Tests for the M02 loader and the WInS plan port.

Expected numbers come from Laura_Gao_Portfolio_Structure_Model_v4.xlsx
(Inputs, Step5_Scenarios and WInS_Plan sheets, recalculated) and
M02_Assumptions_and_Scenarios_v1.xlsx (Assumptions_Register and
Model_Input_Map).
"""

import tempfile
import unittest
from pathlib import Path

from m02.assumptions import (M02_FILE, geometric_to_arithmetic, load_m02,
                             model_inputs)
from m05.inputs import INPUTS_DIR
from structure.plan import floor, scenario_path, wins_plan

# The structure model v4 policy settings: m = 2, Stage 1 at m = 1, no cap.
V4 = dict(bond_yield=0.05, safety_margin=0.0, m=2, max_stock_share=1.0,
          tilts_total=0.06, m_lowest=1)
PATH = dict(bond_yield=0.05, safety_margin=0.0, m=2, max_stock_share=1.0)
G = 1.055 - 1  # compound base return used by the steady preset paths


class M02LoaderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.m02 = load_m02()

    def test_case_facts_match(self):
        a = self.m02["assumptions"]
        self.assertEqual(a["C-01"].value(), 300_000)
        self.assertEqual(a["C-02"].value(), 150_000)
        self.assertEqual(a["C-03"].value(), 50_000)
        self.assertEqual(a["C-01"].status, "CASE")

    def test_arithmetic_return_reproduces_a06(self):
        # A-06 pairs the low return with the high volatility, and the high
        # return with the low volatility (the worse and better ends).
        a = self.m02["assumptions"]
        pairs = {"BASE": ("BASE", "BASE"), "LOW": ("LOW", "HIGH"),
                 "HIGH": ("HIGH", "LOW")}
        for case, (g_case, v_case) in pairs.items():
            got = geometric_to_arithmetic(a["A-04"].value(g_case),
                                          a["A-05"].value(v_case))
            # The CSV stores A-06 rounded to 6 decimals.
            self.assertAlmostEqual(got, a["A-06"].value(case), places=6)

    def test_nine_scenarios_with_six_years_each(self):
        scenarios = self.m02["scenarios"]
        self.assertEqual(sorted(scenarios), [f"S{i}" for i in range(9)])
        for s in scenarios.values():
            self.assertEqual(sorted(s["returns"]), list(range(2027, 2033)))
            self.assertIsNotNone(s["reserve_yield_2033"])

    def test_scenario_s1_is_the_2008_crash_in_2032(self):
        s1 = self.m02["scenarios"]["S1"]
        self.assertEqual(s1["returns"][2032], -0.37)
        self.assertEqual(s1["reserve_yield_2033"], 0.0325)

    def test_model_input_map_matches_m02_workbook(self):
        expected = {  # Model_Input_Map: pessimistic, base, optimistic
            "Inputs!B13": (0.04, 0.05, 0.055),
            "Inputs!B14": (0.0325, 0.044, 0.055),
            "Inputs!B16": (0.0563754516607931, 0.0695115844753669,
                           0.0747768674858667),
            "Inputs!B17": (0.194, 0.178, 0.13),
            "Inputs!B28": (-0.4384, -0.37, -0.1811),
            "Inputs!B29": (-0.4384, -0.4384, -0.4384),
        }
        for i, case in enumerate(("PESSIMISTIC", "BASE", "OPTIMISTIC")):
            got = model_inputs(self.m02, case)
            for cell, values in expected.items():
                # The CSV stores values to 6 decimals; the workbook keeps
                # full precision.
                self.assertAlmostEqual(got[cell]["value"], values[i],
                                       places=6, msg=f"{case} {cell}")

    def test_run_stamp_names_the_version(self):
        stamp = self.m02["run_stamp"]
        self.assertIn("M02 v1.0", stamp["input_version"])
        self.assertEqual(len(stamp["file_version"]), 8)

    def test_unknown_status_is_rejected(self):
        text = (Path(INPUTS_DIR) / M02_FILE).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, M02_FILE).write_text(
                text.replace(",CASE,", ",GUESS,", 1), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_m02(tmp)


class WinsPlanTests(unittest.TestCase):

    def test_floor_matches_inputs_row_40(self):
        self.assertAlmostEqual(floor(2027, 0.05, 0), 302509.068377489, 6)
        self.assertAlmostEqual(floor(2028, 0.05, 0), 317634.521796363, 6)
        self.assertAlmostEqual(floor(2033, 0.05, 0), 405391.083782203, 6)

    def test_plan_matches_wins_plan_sheet(self):
        p = wins_plan(**V4)
        self.assertAlmostEqual(p["portfolio_2028"], 465000, 6)
        self.assertAlmostEqual(p["cushion_2028"], 147365.478203637, 6)
        self.assertAlmostEqual(p["growth_lowest_m"], 0.316915006889542, 12)
        self.assertAlmostEqual(p["growth_target"], 0.633830013779083, 12)
        self.assertAlmostEqual(p["stage1"]["safety"], 0.366169986220917, 12)
        self.assertAlmostEqual(p["stage1"]["growth_core"],
                               0.316915006889542, 12)
        self.assertAlmostEqual(p["stage1"]["parked"], 0.316915006889542, 12)
        self.assertAlmostEqual(p["stage1_dollars"]["safety"],
                               109850.995866275, 6)
        self.assertAlmostEqual(p["stage2"]["safety"], 0.366169986220917, 12)
        self.assertAlmostEqual(p["stage2"]["growth_core"],
                               0.573830013779083, 12)

    def test_stage_totals_equal_account_value(self):
        p = wins_plan(**V4)
        self.assertAlmostEqual(sum(p["stage1_dollars"].values()), 300_000, 6)
        self.assertAlmostEqual(sum(p["stage2_dollars"].values()), 300_000, 6)

    def test_one_stage_when_lowest_m_is_the_chosen_m(self):
        p = wins_plan(**{**V4, "m_lowest": 2})
        self.assertAlmostEqual(p["stage1"]["parked"], 0, 12)
        self.assertAlmostEqual(p["stage1"]["growth_core"],
                               p["growth_target"], 12)

    def test_safety_margin_shrinks_the_cushion(self):
        base = wins_plan(**V4)
        margin = wins_plan(**{**V4, "safety_margin": 0.05})
        self.assertAlmostEqual(margin["floor_2028"],
                               base["floor_2028"] * 1.05, 6)
        self.assertLess(margin["growth_target"], base["growth_target"])


class ScenarioPathTests(unittest.TestCase):

    def test_steady_path_matches_step5_scenarios(self):
        wealth = scenario_path([G] * 6, **PATH)
        self.assertAlmostEqual(wealth[0], 300_000, 6)
        self.assertAlmostEqual(wealth[1], 465_000, 6)
        self.assertAlmostEqual(wealth[-1], 602599.335969565, 4)

    def test_crash_in_2032_matches_step5_scenarios(self):
        wealth = scenario_path([G] * 5 + [-0.37], **PATH)
        self.assertAlmostEqual(wealth[-1], 444460.643177812, 4)

    def test_stocks_earning_the_bond_yield_give_the_risk_free_value(self):
        wealth = scenario_path([0.05] * 6, **PATH)
        self.assertAlmostEqual(wealth[-1],
                               300_000 * 1.05 ** 6 + 150_000 * 1.05 ** 5, 6)

    def test_crash_timing_after_2028_does_not_matter(self):
        crash_2030 = scenario_path([G] * 3 + [-0.37] + [G] * 2, **PATH)
        crash_2032 = scenario_path([G] * 5 + [-0.37], **PATH)
        self.assertAlmostEqual(crash_2030[-1], crash_2032[-1], 6)

    def test_m_of_one_holds_the_cushion_in_stocks(self):
        returns = [0.10, -0.20, 0.05, 0.08, -0.10, 0.06]
        wealth = scenario_path(returns, **{**PATH, "m": 1})
        cushion = 300_000 * 1.05 + 150_000 - floor(2028, 0.05, 0)
        product = 1.0
        for r in returns[1:]:
            product *= 1 + r
        self.assertAlmostEqual(wealth[-1],
                               floor(2033, 0.05, 0) + cushion * product, 6)

    def test_floor_breaks_only_beyond_the_gap_threshold(self):
        # (1 + y)/m - y = 47.5% at m = 2: a 47% fall keeps the reserve,
        # a 48% fall does not.
        reserve = floor(2033, 0.05, 0)
        self.assertGreater(scenario_path([G] * 5 + [-0.47], **PATH)[-1],
                           reserve)
        self.assertLess(scenario_path([G] * 5 + [-0.48], **PATH)[-1],
                        reserve)


if __name__ == "__main__":
    unittest.main()
