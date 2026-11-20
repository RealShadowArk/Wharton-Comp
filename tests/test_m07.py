"""Tests for the M07 block-bootstrap Monte Carlo (m07/sim.py)."""
import statistics

from m07 import sim
from structure.plan import scenario_path


def test_same_seed_same_paths():
    h = sim.history()
    assert sim.block_paths(h, 50, 6, 5, 7) == sim.block_paths(h, 50, 6, 5, 7)


def test_blocks_are_consecutive_years_wrapping_round():
    series = list(range(10))
    for path in sim.block_paths(series, 200, 5, 5, 1):
        assert all((b - a) % 10 == 1 for a, b in zip(path, path[1:]))


def test_shift_hits_the_target_mean_and_keeps_the_spread():
    h = sim.history()
    s = sim.shifted(h, 0.0695)
    assert abs(statistics.mean(s) - 0.0695) < 1e-12
    assert abs(statistics.stdev(s) - statistics.stdev(h)) < 1e-12


def test_path_matches_the_structure_model_port():
    rets = [0.10, -0.20, 0.05, 0.15, -0.10, 0.08]
    w, _ = sim.run_path(rets)
    assert w == scenario_path(rets, sim.BOND_YIELD, sim.MARGIN, sim.M, sim.CAP)


def test_stocks_earning_the_bond_yield_fund_every_payment():
    w, _ = sim.run_path([sim.BOND_YIELD] * 6)
    rv, paid = sim.year_2033(w[-1])
    assert paid["all_payments_funded"] and rv["reserve_gap"] <= 0.005


def test_a_fall_beyond_the_breach_point_leaves_a_shortfall():
    # 2032 is the last stock year; a -60% year at full exposure breaks the floor, a -40% year does not
    bad, _ = sim.run_path([0.0524] * 5 + [-0.60])
    ok, _ = sim.run_path([0.0524] * 5 + [-0.40])
    assert not sim.year_2033(bad[-1])[1]["all_payments_funded"]
    assert sim.year_2033(ok[-1])[1]["all_payments_funded"]
