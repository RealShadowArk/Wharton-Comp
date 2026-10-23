"""Tests for the M03 FCFF/WACC valuation (m03/dcf.py)."""

import unittest
from dataclasses import replace

from m03.dcf import (Inputs, forecast, implied_growth_shift, sensitivity,
                     terminal_value, value, wacc)

# Hand-checkable case: revenue 100 -> 110, EBIT 20%, tax 25%, D&A 5%,
# capex 6%, NWC 10% of the revenue change.
P = Inputs(base_revenue=100.0, growth=(0.10,), ebit_margin=(0.20,),
           tax_rate=0.25, da_pct=(0.05,), capex_pct=(0.06,),
           nwc_pct_of_change=0.10, wacc=0.10, terminal_growth=0.02,
           debt=50.0, non_operating_assets=10.0, diluted_shares=10.0)


class TestFormulas(unittest.TestCase):
    def test_fcff_matches_spec_formula(self):
        r = forecast(P)[0]
        # EBIT(1-t) + D&A - capex - dNWC = 22*0.75 + 5.5 - 6.6 - 1.0
        self.assertAlmostEqual(r["fcff"], 16.5 + 5.5 - 6.6 - 1.0)

    def test_terminal_value_gordon(self):
        self.assertAlmostEqual(terminal_value(10.0, 0.10, 0.02), 125.0)

    def test_wacc_not_above_g_raises(self):
        with self.assertRaises(ValueError):
            terminal_value(10.0, 0.03, 0.03)
        with self.assertRaises(ValueError):
            value(replace(P, wacc=0.02, terminal_growth=0.03))

    def test_equity_bridge(self):
        v = value(P)
        self.assertAlmostEqual(v["equity"], v["ev"] + 10.0 - 50.0)
        self.assertAlmostEqual(v["per_share"], v["equity"] / 10.0)

    def test_hand_value(self):
        # FCFF1 = 14.4, FCFF2 = 112.2*0.15 + 112.2*(-0.01) - 2.2*0.10 = 15.488
        tv = 15.488 / 0.08
        ev = (14.4 + tv) / 1.10
        self.assertAlmostEqual(value(P)["ev"], ev, places=6)

    def test_wacc_formula(self):
        # Ke = 5% + 1.0 * 5% = 10%; weights 80/20; Kd after tax 4%
        self.assertAlmostEqual(wacc(0.05, 1.0, 0.05, 0.05, 0.20, 80, 20),
                               0.8 * 0.10 + 0.2 * 0.04)

    def test_inputs_must_cover_every_year(self):
        with self.assertRaises(ValueError):
            Inputs(100, (0.1, 0.1), (0.2,), 0.25, (0.05, 0.05), (0.06, 0.06),
                   0.1, 0.1, 0.02, 0, 0, 1)

    def test_terminal_reinvestment_rate(self):
        q = replace(P, terminal_reinvestment_rate=0.25)
        rev_next = 110 * 1.02
        expected = rev_next * 0.20 * 0.75 * 0.75 + rev_next * (0.05 - 0.06)
        self.assertAlmostEqual(value(q)["fcff_next"], expected)

    def test_stock_based_pay_subtracted(self):
        q = replace(P, sbc_pct=0.02)
        self.assertAlmostEqual(forecast(q)[0]["fcff"], 14.4 - 110 * 0.02)
        self.assertAlmostEqual(value(q)["fcff_next"],
                               value(P)["fcff_next"] - 110 * 1.02 * 0.02)

    def test_first_year_fraction(self):
        q = replace(P, first_year_fraction=0.5)
        self.assertAlmostEqual(forecast(q)[0]["fcff"], 7.2)
        self.assertAlmostEqual(value(q)["fcff_next"], value(P)["fcff_next"])

    def test_reinvestment_follows_g(self):
        q = replace(P, return_on_new_capital=0.15, terminal_growth=0.03)
        fixed = replace(P, terminal_reinvestment_rate=0.20, terminal_growth=0.03)
        self.assertAlmostEqual(value(q)["fcff_next"], value(fixed)["fcff_next"])
        self.assertAlmostEqual(replace(q, terminal_growth=0.045).reinvestment_rate(), 0.30)

    def test_invalid_inputs_raise(self):
        for bad in ({"diluted_shares": 0.0}, {"tax_rate": 1.0},
                    {"wacc": float("nan")}, {"first_year_fraction": 0.0}):
            with self.assertRaises(ValueError):
                replace(P, **bad)


class TestSensitivities(unittest.TestCase):
    def test_higher_wacc_lowers_value(self):
        s = sensitivity(P, "wacc", [0.08, 0.10, 0.12])
        self.assertGreater(s[0.08], s[0.10])
        self.assertGreater(s[0.10], s[0.12])

    def test_not_defined_when_wacc_below_g(self):
        self.assertIsNone(sensitivity(P, "terminal_growth", [0.11])[0.11])

    def test_reverse_dcf_recovers_price(self):
        price = value(P)["per_share"]
        self.assertAlmostEqual(implied_growth_shift(P, price), 0.0, places=5)
        shift = implied_growth_shift(P, price * 1.1)
        self.assertGreater(shift, 0.0)

    def test_reverse_dcf_when_growth_destroys_value(self):
        # Working capital of $3 per $1 of new revenue: faster growth lowers value.
        q = replace(P, nwc_pct_of_change=3.0)
        price = value(q)["per_share"]
        self.assertLess(value(replace(q, growth=(0.15,)))["per_share"], price)
        self.assertAlmostEqual(implied_growth_shift(q, price), 0.0, places=5)
        self.assertLess(implied_growth_shift(q, price * 1.1), 0.0)

    def test_reverse_dcf_rejects_bad_price(self):
        for bad in (0.0, float("nan")):
            with self.assertRaises(ValueError):
                implied_growth_shift(P, bad)


if __name__ == "__main__":
    unittest.main()
