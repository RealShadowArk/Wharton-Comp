"""Tests for the M02 loader and the WInS plan port.

Expected numbers come from Laura_Gao_Portfolio_Structure_Model_v1.xlsx
(Inputs and WInS_Plan sheets) and M02_Assumptions_and_Scenarios_v1.xlsx
(Assumptions_Register and Model_Input_Map).
"""

import tempfile
import unittest
from pathlib import Path

from m02.assumptions import (M02_FILE, geometric_to_arithmetic, load_m02,
                             model_inputs)
from m05.inputs import INPUTS_DIR
from structure.plan import floor, glide_share, wins_plan

# The structure model v1 as saved: placeholder inputs.
V1 = dict(bond_yield=0.05, safety_margin=0.0, m=2, max_stock_share=1.0,
          glide_2027=0.8, glide_2032=0.2, tilts_total=0.06)


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

    def test_glide_path_matches_inputs_row_41(self):
        for year, share in zip(range(2027, 2033),
                               (0.8, 0.68, 0.56, 0.44, 0.32, 0.2)):
            self.assertAlmostEqual(glide_share(year, 0.8, 0.2), share, 12)

    def test_plan_matches_wins_plan_sheet(self):
        p = wins_plan(**V1)
        self.assertAlmostEqual(p["portfolio_2028"], 465000, 6)
        self.assertAlmostEqual(p["cushion_2028"], 147365.478203637, 6)
        g = p["growth_by_option"]
        self.assertAlmostEqual(g["Option 1"], 0.316915006889542, 12)
        self.assertAlmostEqual(g["Option 2"], 0.68, 12)
        self.assertAlmostEqual(g["Option 3"], 0.633830013779083, 12)
        self.assertAlmostEqual(p["stage1"]["safety"], 0.32, 12)
        self.assertAlmostEqual(p["stage1"]["growth_core"],
                               0.316915006889542, 12)
        self.assertAlmostEqual(p["stage1"]["parked"], 0.363084993110459, 12)
        self.assertAlmostEqual(p["stage1_dollars"]["growth_core"],
                               95074.5020668625, 6)
        self.assertAlmostEqual(p["stage2"]["safety"], 0.366169986220917, 12)
        self.assertAlmostEqual(p["stage2"]["growth_core"],
                               0.573830013779083, 12)

    def test_stage_totals_equal_account_value(self):
        p = wins_plan(**V1)
        self.assertAlmostEqual(sum(p["stage1_dollars"].values()), 300_000, 6)
        self.assertAlmostEqual(sum(p["stage2_dollars"].values()), 300_000, 6)

    def test_m_of_one_is_option_1(self):
        g = wins_plan(**{**V1, "m": 1})["growth_by_option"]
        self.assertAlmostEqual(g["Option 3"], g["Option 1"], 12)

    def test_safety_margin_shrinks_the_cushion(self):
        base = wins_plan(**V1)
        margin = wins_plan(**{**V1, "safety_margin": 0.05})
        self.assertAlmostEqual(margin["floor_2028"],
                               base["floor_2028"] * 1.05, 6)
        self.assertLess(margin["growth_by_option"]["Option 1"],
                        base["growth_by_option"]["Option 1"])


if __name__ == "__main__":
    unittest.main()
