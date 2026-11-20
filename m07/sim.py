"""M07: block-bootstrap Monte Carlo of the floor rule (Option 3), 2027-2042.

    python -m m07.sim            # writes outputs/m07/

Method (student judgments, Pat 20 Nov defaults, all TEST):
- Stock returns: annual S&P 500 total returns 1928-2025 (inputs/m07_sp500_annual_1928_2025.csv,
  RESEARCH), resampled in circular blocks of consecutive years (default 5, about n^(1/3)), so
  crashes and recoveries keep their order. Fixed seed 20260926 (structure model Inputs B35).
- Cases: the history is shifted so its arithmetic mean equals M02 A-06 (LOW 5.64%, BASE 6.95%,
  HIGH 7.48%, net of fees); its volatility (19.4%) and fat tails are kept. RAW = history minus
  the 0.03% fund fee. A lognormal run with M02 BASE (6.95%, 17.8%) is a cross-check.
- Floor rule as in structure/plan.py: stocks = m x (wealth - floor), capped at the maximum
  stock share; the rest earns the locked bond yield (5.24%, Inputs B13); rebalanced yearly.
- 2033: the reserve is formed first (M05 form_reserve at the bond yield), paid out from bonds
  matched to the payments (M05 run_off), then the gift = share x leftover (M08 facility_gift).
  Hold-back = 1 - share (0%, 10%, 20% shown; Pat decides).
Simulation results do not prove future outcomes.
"""
import csv
import math
import random
import statistics
from pathlib import Path

from m05.reserve import TOLERANCE, form_reserve, run_off, summarize_run_off
from m08.gift import facility_gift
from m08.inputs import FROM_2027, policy_id
from structure.plan import CONTRIBUTIONS, FIRST_YEAR, floor, stocks

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "inputs" / "m07_sp500_annual_1928_2025.csv"
OUT = ROOT / "outputs" / "m07"
SEED = 20260926
N_PATHS = 10_000
BOND_YIELD = 0.0524      # Inputs B13 (RESEARCH): blended yield locked in by the ladder
MARGIN = 0.0             # Inputs B15
M, CAP = 2, 1.0          # Inputs B24, B25
FEE = 0.0003             # M02 A-10 BASE (core fund expense ratio)
ARITH = {"LOW": 0.056375, "BASE": 0.069512, "HIGH": 0.074777}   # M02 A-06
VOL_BASE = 0.178         # M02 A-05 BASE
YEARS = list(range(FIRST_YEAR, 2033))   # stock years 2027-2032
SHARES = (1.0, 0.9, 0.8)                # gift share = 1 - hold-back


def history():
    return [float(r["sp500_total_return"]) for r in csv.DictReader(open(HISTORY))]


def shifted(hist, target):
    """Same shape, arithmetic mean moved to `target`."""
    d = target - statistics.mean(hist)
    return [r + d for r in hist]


def block_paths(series, n_paths, n_years, block, seed):
    """Circular block bootstrap: each path strings together blocks of `block`
    consecutive years starting at random years (wrapping around the end)."""
    rng = random.Random(seed)
    n = len(series)
    out = []
    for _ in range(n_paths):
        path = []
        while len(path) < n_years:
            start = rng.randrange(n)
            path += [series[(start + k) % n] for k in range(block)]
        out.append(path[:n_years])
    return out


def lognormal_paths(arith, vol, n_paths, n_years, seed):
    s2 = math.log(1 + vol ** 2 / (1 + arith) ** 2)
    mu = math.log(1 + arith) - s2 / 2
    rng = random.Random(seed)
    return [[math.exp(rng.gauss(mu, math.sqrt(s2))) - 1 for _ in range(n_years)] for _ in range(n_paths)]


def run_path(returns, start_year=FIRST_YEAR, start_wealth=None, contributions=CONTRIBUTIONS):
    """Wealth at the start of each year from start_year to 2033, plus the stock share each year."""
    w = [contributions.get(start_year, 0) if start_wealth is None else start_wealth]
    share = []
    for k, ret in enumerate(returns):
        year = start_year + k
        s = stocks(w[-1], floor(year, BOND_YIELD, MARGIN), M, CAP)
        share.append(s / w[-1] if w[-1] > 0 else 0.0)
        w.append(s * (1 + ret) + (w[-1] - s) * (1 + BOND_YIELD) + contributions.get(year + 1, 0))
    return w, share


def year_2033(value_2033):
    rv = form_reserve(value_2033, BOND_YIELD)
    paid = summarize_run_off(run_off(rv["actual_reserve_transfer"], [BOND_YIELD] * 9))
    return rv, paid


def q(xs, p):
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def simulate(paths):
    rows = []
    for i, rets in enumerate(paths):
        w, share = run_path(rets)
        rv, paid = year_2033(w[-1])
        rows.append(dict(path_id=i + 1, wealth=w, share=share, value_2031=w[YEARS.index(2031)], value_2033=w[-1],
                         required=rv["reserve_required"], gap=rv["reserve_gap"], success=paid["all_payments_funded"],
                         total_short=paid["total_shortfall"], worst_short=paid["worst_single_shortfall"],
                         leftover=max(0.0, w[-1] - rv["reserve_required"])))
    return rows


def stats(rows):
    left = [r["leftover"] for r in rows]
    w33 = [r["value_2033"] for r in rows]
    short = [r for r in rows if not r["success"]]
    return dict(success=1 - len(short) / len(rows), n_short=len(short),
                mean_short=(sum(r["total_short"] for r in short) / len(short)) if short else 0.0,
                worst_short=max((r["total_short"] for r in rows), default=0.0),
                w33=[q(w33, p) for p in (0.05, 0.10, 0.50, 0.90, 0.95)],
                left=[q(left, p) for p in (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)],
                left_mean=statistics.mean(left),
                cvar5=statistics.mean(sorted(left)[:max(1, len(left) // 20)]),
                zero_left=sum(1 for x in left if x <= TOLERANCE) / len(left),
                share_2028=statistics.median(r["share"][1] for r in rows))


def conditional(hist_case, value_2031, block, seed, n_paths=N_PATHS):
    """From a known 2031 balance: two more stock years (2031, 2032), then 2033."""
    paths = block_paths(hist_case, n_paths, 2, block, seed)
    left = []
    ok = 0
    for rets in paths:
        w, _ = run_path(rets, start_year=2031, start_wealth=value_2031, contributions={})
        rv, paid = year_2033(w[-1])
        left.append(max(0.0, w[-1] - rv["reserve_required"]))
        ok += paid["all_payments_funded"]
    return ok / n_paths, [q(left, p) for p in (0.10, 0.50, 0.90)]


def money(x):
    return f"${x:,.0f}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hist = history()
    required = form_reserve(0, BOND_YIELD)["reserve_required"]
    floors = {y: floor(y, BOND_YIELD, MARGIN) for y in range(FIRST_YEAR, 2034)}
    runs = {}
    for case in ("LOW", "BASE", "HIGH"):
        runs[(case, 5)] = simulate(block_paths(shifted(hist, ARITH[case]), N_PATHS, len(YEARS), 5, SEED))
    for b in (1, 3, 10):
        runs[("BASE", b)] = simulate(block_paths(shifted(hist, ARITH["BASE"]), N_PATHS, len(YEARS), b, SEED))
    runs[("RAW", 5)] = simulate(block_paths([r - FEE for r in hist], N_PATHS, len(YEARS), 5, SEED))
    runs[("LOGNORMAL", 0)] = simulate(lognormal_paths(ARITH["BASE"], VOL_BASE, N_PATHS, len(YEARS), SEED))
    S = {k: stats(v) for k, v in runs.items()}
    base = runs[("BASE", 5)]

    # Fan chart data: wealth percentiles by year (BASE, block 5)
    with open(OUT / "M07_fan_BASE.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["year", "p10", "p25", "p50", "p75", "p90", "floor", "label"])
        for k, y in enumerate(range(FIRST_YEAR, 2034)):
            col = [r["wealth"][k] for r in base]
            w.writerow([y] + [round(q(col, p), 2) for p in (0.10, 0.25, 0.50, 0.75, 0.90)] + [round(floors[y], 2), "TEST"])

    # M08 input: one row per path and gift share (BASE, block 5)
    with open(OUT / "M07_path_summary.csv", "w", newline="") as f:
        cols = ["run_id", "policy_id", "state_id", "path_id", "value_2031", "value_2033", "reserve_required", "reserve_gap",
                "facility_gift", "all_payments_success", "total_nominal_shortfall", "worst_single_shortfall"]
        w = csv.DictWriter(f, cols, lineterminator="\n")
        w.writeheader()
        for sh in SHARES:
            for r in base:
                w.writerow(dict(run_id="m07-0.1_BASE_block5", policy_id=policy_id(sh), state_id=FROM_2027, path_id=r["path_id"],
                                value_2031=round(r["value_2031"], 2), value_2033=round(r["value_2033"], 2),
                                reserve_required=round(r["required"], 2), reserve_gap=round(r["gap"], 2),
                                facility_gift=round(facility_gift(r["value_2033"], r["required"], sh), 2),
                                all_payments_success=r["success"], total_nominal_shortfall=round(r["total_short"], 2),
                                worst_single_shortfall=round(r["worst_short"], 2)))

    # 2031 states: what a co-sponsor range would look like from a known 2031 balance
    w31 = sorted(r["value_2031"] for r in base)
    states = [(f"p{int(p * 100)} of simulated 2031 balances", q(w31, p)) for p in (0.10, 0.50, 0.90)]
    cond = [(name, v) + conditional(shifted(hist, ARITH["BASE"]), v, 5, SEED + 1) for name, v in states]

    breach = (1 + BOND_YIELD) / M - 1   # one-year fall that wipes out the cushion when stocks = m x cushion
    b = S[("BASE", 5)]
    L = [f"# M07 Monte Carlo: floor rule, 2027-2042 (TEST, m07-0.1, {N_PATHS:,} paths per run, seed {SEED})", "",
         "Generated by `python -m m07.sim`. Method and every default: module docstring. Student judgments (Pat 20 Nov defaults): "
         "block bootstrap of 1928-2025 S&P 500 years, mean set to M02 LOW/BASE/HIGH, yearly rebalancing, hold-back 0% (10% and 20% shown). "
         "**Simulation results do not prove future outcomes.**", "",
         "## Plan facts used", "",
         f"- Contributions $300,000 (2027) and $150,000 (2028), CASE. Ten $50,000 payments 2033-2042, CASE.",
         f"- Floor rule: stocks = {M} x (wealth - floor), at most {CAP:.0%} of wealth; bonds earn {BOND_YIELD:.2%} (locked ladder yield); rebalanced yearly.",
         f"- Required reserve at the start of 2033: {money(required)} (present value of the ten payments at {BOND_YIELD:.2%}). Floor at the start of 2028: {money(floors[2028])}.",
         f"- Median stock share in 2028 (after both contributions): {b['share_2028']:.0%}.",
         f"- One-year stock fall that would break the floor when stocks are exactly {M} x the cushion: {breach:.1%}. "
         f"Worst year in the 1928-2025 history: -43.8% (1931); after the BASE mean shift: {-0.4384 + ARITH['BASE'] - statistics.mean(hist):.1%}.", "",
         "## Headline (BASE, 5-year blocks)", "",
         f"- **All ten payments funded in {b['success']:.2%} of paths** ({b['n_short']} of {N_PATHS:,} short; average shortfall in those paths {money(b['mean_short'])}, worst {money(b['worst_short'])}).",
         f"- **Leftover at the start of 2033** (after the reserve and the first payment's funding), middle 80% of paths: **{money(b['left'][1])} to {money(b['left'][5])}**, median {money(b['left'][3])}.",
         f"- Worst 5% of paths average a leftover of {money(b['cvar5'])} (expected shortfall, CVaR 5%); leftover is zero in {b['zero_left']:.1%} of paths.", "",
         "## Leftover in 2033 by case (the pool for a facility gift)", "",
         "| Run | Payments fully funded | p10 | p25 | Median | p75 | p90 | Worst 5% average |", "|---|---|---|---|---|---|---|---|"]
    names = {("LOW", 5): "LOW (M02 mean 5.64%)", ("BASE", 5): "**BASE (6.95%)**", ("HIGH", 5): "HIGH (7.48%)", ("RAW", 5): "Raw history (11.8%)",
             ("BASE", 1): "BASE, 1-year blocks", ("BASE", 3): "BASE, 3-year blocks", ("BASE", 10): "BASE, 10-year blocks",
             ("LOGNORMAL", 0): "Lognormal cross-check (6.95%, 17.8%)"}
    for k in [("LOW", 5), ("BASE", 5), ("HIGH", 5), ("RAW", 5), ("BASE", 1), ("BASE", 3), ("BASE", 10), ("LOGNORMAL", 0)]:
        s = S[k]
        L.append(f"| {names[k]} | {s['success']:.2%} | {money(s['left'][1])} | {money(s['left'][2])} | {money(s['left'][3])} | "
                 f"{money(s['left'][4])} | {money(s['left'][5])} | {money(s['cvar5'])} |")
    L += ["", "## Gift range by hold-back (BASE, 5-year blocks; middle 80% of paths)", "",
          "| Hold-back | Gift share | p10 | Median | p90 |", "|---|---|---|---|---|"]
    for sh in SHARES:
        g = [facility_gift(r["value_2033"], r["required"], sh) for r in base]
        L.append(f"| {1 - sh:.0%} | {sh:.0%} | {money(q(g, 0.10))} | {money(q(g, 0.50))} | {money(q(g, 0.90))} |")
    L += ["", "## From a known 2031 balance (BASE): the range a co-sponsor would hear in 2031", "",
          "Two more stock years (2031, 2032) from the stated balance; 10,000 paths each.", "",
          "| 2031 state | Balance at the start of 2031 | Payments fully funded | Leftover p10 | Median | p90 |", "|---|---|---|---|---|---|"]
    for name, v, ok, (a, m_, c) in cond:
        L.append(f"| {name} | {money(v)} | {ok:.2%} | {money(a)} | {money(m_)} | {money(c)} |")
    L += ["", "## Wealth path (BASE): percentiles at the start of each year", "", "| Year | p10 | Median | p90 | Floor |", "|---|---|---|---|---|"]
    for k, y in enumerate(range(FIRST_YEAR, 2034)):
        col = [r["wealth"][k] for r in base]
        L.append(f"| {y} | {money(q(col, 0.10))} | {money(q(col, 0.50))} | {money(q(col, 0.90))} | {money(floors[y])} |")
    L += ["", "Files: `M07_fan_BASE.csv` (fan chart), `M07_path_summary.csv` (M08's input: BASE, one row per path and gift share)."]
    (OUT / "M07_summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
