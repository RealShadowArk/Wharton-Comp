"""Tests for the M12 score: the guide's fixtures plus the release gates."""

import unittest

from m12.score import (CROSS_MEASURES, CROSS_WEIGHTS, MEASURES, WEIGHTS,
                       percentile_scores, score_group, shortlist_of,
                       variants, weighted_total)

IDS = [m for m, _, _ in MEASURES]
# Guide fixtures: scorecards A-E (Q1..V2) and their TFS.
CARDS = {"A": ([100, 75, 100, 75, 50, 25, 0, 25], 56.25),
         "B": ([75, 100, 75, 100, 0, 50, 25, 0], 53.125),
         "C": ([50, 50, 50, 50, 100, 75, 50, 50], 59.375),
         "D": ([25, 25, 25, 25, 75, 100, 100, 75], 56.25),
         "E": ([0, 0, 0, 0, 25, 0, 75, 100], 25.0)}
# Cross-check fixtures from handoff/M12_score_spec.md (ROE, P/S, P/B scores).
CROSS = {"A": ((75, 0, 25), 55.2083333), "B": ((100, 25, 0), 54.1666667),
         "C": ((50, 50, 75), 60.9375), "D": ((25, 100, 50), 54.6875),
         "E": ((0, 75, 100), 25.0)}


def row(ticker, group="G", **values):
    base = {"ticker": ticker, "peer_group": group, "revenue_fy0": "100",
            "revenue_fy3": "80", "operating_income_fy0": "20",
            "pretax_income_fy0": "18", "total_assets_fy0": "200",
            "total_assets_fy1": "180", "total_debt_fy0": "50",
            "current_assets_fy0": "60", "current_liabilities_fy0": "40",
            "eps_diluted_fy0": "3", "eps_diluted_fy3": "2",
            "earnings_common_fy0": "15", "cfo_fy0": "25", "capex_fy0": "5",
            "market_cap_cutoff_proxy_m": "300", "total_equity_fy0": "100"}
    base.update({k: str(v) for k, v in values.items()})
    return base


class FixtureTests(unittest.TestCase):

    def test_average_rank_example(self):
        s, flag = percentile_scores(dict(zip("abcde", [10, 20, 20, 30, 40])), 1)
        self.assertEqual([s[k] for k in "abcde"], [0, 37.5, 37.5, 75, 100])
        self.assertEqual(flag, "")

    def test_reversing_direction_reverses_ranks(self):
        s, _ = percentile_scores(dict(zip("abcde", [10, 20, 20, 30, 40])), -1)
        self.assertEqual([s[k] for k in "abcde"], [100, 62.5, 62.5, 25, 0])

    def test_single_company_or_all_tied_score_50(self):
        self.assertEqual(percentile_scores({"a": 5}, 1),
                         ({"a": 50.0}, "NO_DISCRIMINATION"))
        s, flag = percentile_scores({"a": 2, "b": 2, "c": 2}, 1)
        self.assertEqual(set(s.values()), {50.0})
        self.assertEqual(flag, "NO_DISCRIMINATION")

    def test_scorecards_a_to_e(self):
        for card, (values, expected) in CARDS.items():
            self.assertAlmostEqual(
                weighted_total(dict(zip(IDS, values)), WEIGHTS), expected, 9,
                msg=card)

    def test_cross_check_scorecards(self):
        for card, ((roe, ps, pb), expected) in CROSS.items():
            scores = dict(zip(IDS, CARDS[card][0]), ROE=roe, PS=ps, PB=pb)
            self.assertAlmostEqual(weighted_total(scores, CROSS_WEIGHTS),
                                   expected, 6, msg=card)

    def test_one_missing_measure_blanks_the_score(self):
        scores = dict(zip(IDS, CARDS["A"][0]))
        scores["G2"] = None
        self.assertIsNone(weighted_total(scores, WEIGHTS))

    def test_32_variants_with_weights_summing_to_one(self):
        vs = variants()
        self.assertEqual(len(vs), 32)
        for name, w in vs:
            self.assertAlmostEqual(sum(w.values()), 1.0, 12, msg=name)
        self.assertEqual(len(variants(CROSS_WEIGHTS, CROSS_MEASURES)), 41)


class GroupTests(unittest.TestCase):

    def group(self, n_complete, n_incomplete):
        rows = [row(f"C{i}", revenue_fy0=100 + i, earnings_common_fy0=10 + i)
                for i in range(n_complete)]
        rows += [row(f"X{i}", eps_diluted_fy3=-1) for i in range(n_incomplete)]
        return score_group(rows)

    def test_release_gate(self):
        self.assertFalse(self.group(4, 0)["released"])   # fewer than 5 complete
        self.assertTrue(self.group(5, 1)["released"])    # 5 of 6 = 83%
        self.assertFalse(self.group(5, 2)["released"])   # 5 of 7 = 71%

    def test_unsuitable_eps_base_is_not_zero_growth(self):
        result = self.group(5, 1)
        self.assertEqual(result["raw"]["X0"]["G2"][1], "UNSUITABLE")
        self.assertIsNone(result["totals"]["X0"])

    def test_r1_switches_whole_group_to_pretax(self):
        rows = [row(f"C{i}") for i in range(5)]
        rows[0]["operating_income_fy0"] = ""
        result = score_group(rows)
        self.assertEqual({result["raw"][t]["Q1"][2] for t in result["raw"]},
                         {"pretax (R1)"})
        self.assertAlmostEqual(result["raw"]["C1"]["Q1"][0], 0.18)

    def test_shortlist_keeps_boundary_ties(self):
        self.assertEqual(shortlist_of({"a": 90, "b": 80, "c": 80, "d": 10}),
                         ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
