"""Acceptance tests for M05.

Expected values come from the case (the payment schedule) or were worked
out by hand. Every rate here is a TEST value, not a sourced assumption.
"""

import unittest

from m05.reserve import (actual_reserve_transfer, form_reserve,
                         required_reserve, reserve_gap, run_off,
                         summarize_run_off)

ZERO_RETURNS = [0.0] * 9


class RequiredReserveTests(unittest.TestCase):

    def test_zero_yield_is_exactly_500000(self):
        self.assertEqual(required_reserve(0.0), 500_000)

    def test_first_payment_is_not_discounted(self):
        # With a single payment, the reserve is that payment at any yield.
        self.assertEqual(required_reserve(0.05, n_payments=1), 50_000)

    def test_three_percent_flat_yield(self):
        self.assertAlmostEqual(required_reserve(0.03), 439_305.45, places=2)

    def test_higher_yield_needs_smaller_reserve(self):
        self.assertLess(required_reserve(0.04), required_reserve(0.02))

    def test_yield_of_minus_one_is_rejected(self):
        with self.assertRaises(ValueError):
            required_reserve(-1.0)


class TransferAndGapTests(unittest.TestCase):

    def test_short_portfolio_moves_everything_and_shows_gap(self):
        transfer = actual_reserve_transfer(500_000, 450_000)
        self.assertEqual(transfer, 450_000)
        self.assertEqual(reserve_gap(500_000, transfer), 50_000)

    def test_large_portfolio_moves_only_what_is_required(self):
        transfer = actual_reserve_transfer(500_000, 600_000)
        self.assertEqual(transfer, 500_000)
        self.assertEqual(reserve_gap(500_000, transfer), 0)

    def test_negative_portfolio_moves_nothing(self):
        self.assertEqual(actual_reserve_transfer(500_000, -10_000), 0)


class RunOffTests(unittest.TestCase):

    def test_ten_payments_from_2033_to_2042(self):
        rows = run_off(500_000, ZERO_RETURNS)
        self.assertEqual([r["year"] for r in rows], list(range(2033, 2043)))
        self.assertEqual(sum(r["payment_due"] for r in rows), 500_000)

    def test_zero_yield_full_reserve_ends_at_zero(self):
        rows = run_off(500_000, ZERO_RETURNS)
        self.assertEqual(sum(r["shortfall"] for r in rows), 0)
        self.assertEqual(rows[-1]["balance_after_payment"], 0)

    def test_short_reserve_leaves_last_payment_unfunded(self):
        # $450,000 transferred at zero return: payments 1 to 9 are funded,
        # payment 10 is not, and nothing is borrowed.
        rows = run_off(450_000, ZERO_RETURNS)
        for row in rows[:9]:
            self.assertEqual(row["payment_funded"], 50_000)
            self.assertEqual(row["shortfall"], 0)
        self.assertEqual(rows[9]["payment_funded"], 0)
        self.assertEqual(rows[9]["shortfall"], 50_000)
        self.assertEqual(rows[9]["balance_after_payment"], 0)

    def test_partial_payment_when_cash_runs_short(self):
        # $120,000 funds two full payments and $20,000 of the third.
        rows = run_off(120_000, ZERO_RETURNS)
        self.assertEqual(rows[2]["payment_funded"], 20_000)
        self.assertEqual(rows[2]["shortfall"], 30_000)
        self.assertEqual(sum(r["payment_funded"] for r in rows), 120_000)
        self.assertEqual(sum(r["shortfall"] for r in rows), 380_000)

    def test_balances_never_go_negative(self):
        rows = run_off(120_000, ZERO_RETURNS)
        for row in rows:
            self.assertGreaterEqual(row["balance_after_payment"], 0)
            self.assertGreaterEqual(row["next_balance"], 0)

    def test_return_is_applied_after_the_payment(self):
        rows = run_off(100_000, [0.10] + [0.0] * 8)
        self.assertEqual(rows[0]["balance_after_payment"], 50_000)
        self.assertAlmostEqual(rows[0]["next_balance"], 55_000)
        self.assertAlmostEqual(rows[1]["balance_before_payment"], 55_000)

    def test_no_return_after_the_last_payment(self):
        rows = run_off(600_000, [0.05] * 9)
        self.assertIsNone(rows[-1]["return_rate"])
        self.assertEqual(rows[-1]["next_balance"],
                         rows[-1]["balance_after_payment"])

    def test_reserve_sized_at_a_rate_runs_off_to_zero_at_that_rate(self):
        rows = run_off(required_reserve(0.03), [0.03] * 9)
        self.assertAlmostEqual(sum(r["shortfall"] for r in rows), 0, places=6)
        self.assertAlmostEqual(rows[-1]["balance_after_payment"], 0, places=6)

    def test_wrong_number_of_returns_is_rejected(self):
        with self.assertRaises(ValueError):
            run_off(500_000, [0.0] * 10)

    def test_negative_starting_balance_is_rejected(self):
        with self.assertRaises(ValueError):
            run_off(-1, ZERO_RETURNS)

    def test_return_of_minus_one_is_rejected(self):
        with self.assertRaises(ValueError):
            run_off(500_000, [-1.0] + [0.0] * 8)

    def test_more_starting_cash_never_worsens_funding(self):
        returns = [0.02, -0.10, 0.04, 0.0, -0.05, 0.03, 0.01, 0.0, 0.02]
        smaller = summarize_run_off(run_off(400_000, returns))
        larger = summarize_run_off(run_off(410_000, returns))
        self.assertLessEqual(larger["total_shortfall"],
                             smaller["total_shortfall"])


class FormReserveTests(unittest.TestCase):

    def test_ledger_case_is_not_established(self):
        decision = form_reserve(450_000, 0.0)
        self.assertEqual(decision["reserve_required"], 500_000)
        self.assertEqual(decision["actual_reserve_transfer"], 450_000)
        self.assertEqual(decision["reserve_gap"], 50_000)
        self.assertFalse(decision["reserve_established"])

    def test_enough_assets_establishes_the_reserve(self):
        decision = form_reserve(593_470.93, 0.03)
        self.assertAlmostEqual(decision["actual_reserve_transfer"],
                               439_305.45, places=2)
        self.assertEqual(decision["reserve_gap"], 0)
        self.assertTrue(decision["reserve_established"])

    def test_same_2033_state_gets_same_decision_whatever_follows(self):
        # The decision is made before any later return is known. Two paths
        # that start from the same 2033 state get the same reserve, even
        # though their futures differ.
        first = form_reserve(593_470.93, 0.03)
        second = form_reserve(593_470.93, 0.03)
        self.assertEqual(first, second)
        good = run_off(first["actual_reserve_transfer"], [0.05] * 9)
        bad = run_off(second["actual_reserve_transfer"], [-0.05] * 9)
        self.assertNotEqual(summarize_run_off(good)["total_shortfall"],
                            summarize_run_off(bad)["total_shortfall"])


class SummaryTests(unittest.TestCase):

    def test_ledger_case_summary(self):
        summary = summarize_run_off(run_off(450_000, ZERO_RETURNS))
        self.assertFalse(summary["all_payments_funded"])
        self.assertEqual(summary["first_shortfall_year"], 2042)
        self.assertEqual(summary["total_shortfall"], 50_000)
        self.assertEqual(summary["worst_single_shortfall"], 50_000)

    def test_fully_funded_summary(self):
        summary = summarize_run_off(run_off(500_000, ZERO_RETURNS))
        self.assertTrue(summary["all_payments_funded"])
        self.assertIsNone(summary["first_shortfall_year"])

    def test_established_reserve_can_still_fall_short(self):
        # Sized at 3% but only earning 1%: the reserve is fully set aside,
        # yet the late payments are not all covered.
        decision = form_reserve(593_470.93, 0.03)
        rows = run_off(decision["actual_reserve_transfer"], [0.01] * 9)
        self.assertTrue(decision["reserve_established"])
        self.assertFalse(summarize_run_off(rows)["all_payments_funded"])

    def test_floating_point_noise_is_not_a_shortfall(self):
        rows = run_off(required_reserve(0.03), [0.03] * 9)
        self.assertTrue(summarize_run_off(rows)["all_payments_funded"])


if __name__ == "__main__":
    unittest.main()
