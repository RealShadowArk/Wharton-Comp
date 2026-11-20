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


def history(start=1928, end=2025):
    return [float(r["sp500_total_return"]) for r in csv.DictReader(open(HISTORY)) if start <= int(r["year"]) <= end]


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


WINDOWS = {1928: "with the Great Depression (1928-2025)", 1940: "without the Great Depression (1940-2025)"}  # Pat 20 Nov: always run both
GEOM_BASE = 0.055   # M02 A-04 BASE geometric, for the non-crash years of the stress replays
REPLAYS = [  # actual S&P 500 total returns (inputs/m07_sp500_annual_1928_2025.csv), placed just before 2033; other years at 5.5%
    ("No crash (every year 5.5%)", {}),
    ("AI-bubble burst: dot-com 2000-2002 in 2030-2032", {2030: -0.0903, 2031: -0.1185, 2032: -0.2197}),
    ("2022 (-18.1%) in 2032", {2032: -0.1811}),
    ("1973-74 in 2031-2032", {2031: -0.1431, 2032: -0.2590}),
    ("2008 (-36.6%) in 2032", {2032: -0.3655}),
    ("1931 (-43.8%) in 2032", {2032: -0.4384}),
    ("Reverse stress: -50% in 2032", {2032: -0.50}),
]


def money(x):
    return f"${x:,.0f}"


def window(start, floors):
    """Every BASE/LOW/HIGH and sensitivity run for one history window, plus its files."""
    h = history(start)
    runs = {(c, 5): simulate(block_paths(shifted(h, ARITH[c]), N_PATHS, len(YEARS), 5, SEED)) for c in ("LOW", "BASE", "HIGH")}
    for b in (1, 3, 10):
        runs[("BASE", b)] = simulate(block_paths(shifted(h, ARITH["BASE"]), N_PATHS, len(YEARS), b, SEED))
    runs[("RAW", 5)] = simulate(block_paths([r - FEE for r in h], N_PATHS, len(YEARS), 5, SEED))
    base = runs[("BASE", 5)]
    with open(OUT / f"M07_fan_BASE_{start}.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["year", "p10", "p25", "p50", "p75", "p90", "floor", "label"])
        for k, y in enumerate(range(FIRST_YEAR, 2034)):
            col = [r["wealth"][k] for r in base]
            w.writerow([y] + [round(q(col, p), 2) for p in (0.10, 0.25, 0.50, 0.75, 0.90)] + [round(floors[y], 2), "TEST"])
    with open(OUT / f"M07_path_summary_{start}.csv", "w", newline="") as f:
        cols = ["run_id", "policy_id", "state_id", "path_id", "value_2031", "value_2033", "reserve_required", "reserve_gap",
                "facility_gift", "all_payments_success", "total_nominal_shortfall", "worst_single_shortfall"]
        w = csv.DictWriter(f, cols, lineterminator="\n")
        w.writeheader()
        for sh in SHARES:
            for r in base:
                w.writerow(dict(run_id=f"m07-0.2_BASE_block5_{start}", policy_id=policy_id(sh), state_id=FROM_2027, path_id=r["path_id"],
                                value_2031=round(r["value_2031"], 2), value_2033=round(r["value_2033"], 2),
                                reserve_required=round(r["required"], 2), reserve_gap=round(r["gap"], 2),
                                facility_gift=round(facility_gift(r["value_2033"], r["required"], sh), 2),
                                all_payments_success=r["success"], total_nominal_shortfall=round(r["total_short"], 2),
                                worst_single_shortfall=round(r["worst_short"], 2)))
    w31 = sorted(r["value_2031"] for r in base)
    cond = [(f"p{int(p * 100)} of simulated 2031 balances", q(w31, p)) for p in (0.10, 0.50, 0.90)]
    cond = [(n, v) + conditional(shifted(h, ARITH["BASE"]), v, 5, SEED + 1) for n, v in cond]
    gifts = {sh: [facility_gift(r["value_2033"], r["required"], sh) for r in base] for sh in SHARES}
    return dict(h=h, S={k: stats(v) for k, v in runs.items()}, base=base, cond=cond, gifts=gifts)


def replay(crash):
    rets = [crash.get(y, GEOM_BASE) for y in YEARS]
    w, share = run_path(rets)
    rv, paid = year_2033(w[-1])
    return w[-1], max(0.0, w[-1] - rv["reserve_required"]), paid, share


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    required = form_reserve(0, BOND_YIELD)["reserve_required"]
    floors = {y: floor(y, BOND_YIELD, MARGIN) for y in range(FIRST_YEAR, 2034)}
    W = {start: window(start, floors) for start in WINDOWS}
    logn = stats(simulate(lognormal_paths(ARITH["BASE"], VOL_BASE, N_PATHS, len(YEARS), SEED)))
    breach = (1 + BOND_YIELD) / M - 1   # one-year fall that wipes out the cushion when stocks = m x cushion
    L = [f"# M07 Monte Carlo: floor rule, 2027-2042 (TEST, m07-0.2, {N_PATHS:,} paths per run, seed {SEED})", "",
         "Generated by `python -m m07.sim`. Method and every default: module docstring. Student judgments (Pat 20 Nov): "
         "every run is shown twice, with and without the Great Depression years; block bootstrap of S&P 500 years with the mean set to M02 "
         "LOW/BASE/HIGH; yearly rebalancing; hold-back 0% (10% and 20% shown). **Simulation results do not prove future outcomes.**", "",
         "## What is simulated", "",
         "- **Laura's plan, not the WInS account:** contributions of $300,000 (2027) and $150,000 (2028), $450,000 in total (CASE); ten $50,000 payments 2033-2042 (CASE). "
         "WInS gains and losses are never added (competition rule).",
         "- **The stock sleeve is the S&P 500**, the longest reliable history (1928-2025), with its average set to M02. Our specific holdings are not modelled; "
         "a variant with our final mix waits for the 2028 additions.",
         f"- Floor rule: stocks = {M} x (wealth - floor), at most {CAP:.0%} of wealth; the rest earns {BOND_YIELD:.2%} (locked ladder yield); rebalanced yearly.",
         f"- Required reserve at the start of 2033: {money(required)}. Floor at the start of 2028: {money(floors[2028])}.",
         f"- **Breach point:** the floor breaks only if stocks fall more than {-breach:.1%} in one year.", "",
         "## Headline: the two histories side by side (BASE mean 6.95%, 5-year blocks)", "",
         "| | " + " | ".join(WINDOWS.values()) + " |", "|---|---|---|"]
    rows = [("Years in the bootstrap", lambda d: f"{len(d['h'])}"),
            ("Raw average, volatility", lambda d: f"{statistics.mean(d['h']):.1%}, {statistics.stdev(d['h']):.1%}"),
            ("Worst year (after the BASE shift)", lambda d: f"{min(d['h']):.1%} ({min(d['h']) + ARITH['BASE'] - statistics.mean(d['h']):.1%})"),
            ("**All ten payments funded**", lambda d: f"**{d['S'][('BASE', 5)]['success']:.2%}**"),
            ("Paths short, average shortfall", lambda d: f"{d['S'][('BASE', 5)]['n_short']}, {money(d['S'][('BASE', 5)]['mean_short'])}"),
            ("**2033 leftover, middle 80%**", lambda d: f"**{money(d['S'][('BASE', 5)]['left'][1])} to {money(d['S'][('BASE', 5)]['left'][5])}**"),
            ("2033 leftover, median", lambda d: money(d['S'][('BASE', 5)]['left'][3])),
            ("Worst 5% of paths, average leftover (CVaR)", lambda d: money(d['S'][('BASE', 5)]['cvar5']))]
    for label, f in rows:
        L.append(f"| {label} | " + " | ".join(f(W[s]) for s in WINDOWS) + " |")
    names = {("LOW", 5): "LOW (mean 5.64%)", ("BASE", 5): "**BASE (6.95%)**", ("HIGH", 5): "HIGH (7.48%)", ("RAW", 5): "Raw history",
             ("BASE", 1): "BASE, 1-year blocks", ("BASE", 3): "BASE, 3-year blocks", ("BASE", 10): "BASE, 10-year blocks"}
    for start, title in WINDOWS.items():
        d = W[start]
        L += ["", f"## {title[0].upper() + title[1:]}", "", "### Leftover in 2033 by case", "",
              "| Run | Payments fully funded | p10 | p25 | Median | p75 | p90 | Worst 5% average |", "|---|---|---|---|---|---|---|---|"]
        for k in names:
            s_ = d["S"][k]
            L.append(f"| {names[k]} | {s_['success']:.2%} | {money(s_['left'][1])} | {money(s_['left'][2])} | {money(s_['left'][3])} | "
                     f"{money(s_['left'][4])} | {money(s_['left'][5])} | {money(s_['cvar5'])} |")
        L += ["", "### Gift range by hold-back (BASE; middle 80%)", "", "| Hold-back | p10 | Median | p90 |", "|---|---|---|---|"]
        for sh, g in d["gifts"].items():
            L.append(f"| {1 - sh:.0%} | {money(q(g, 0.10))} | {money(q(g, 0.50))} | {money(q(g, 0.90))} |")
        L += ["", "### From a known 2031 balance (BASE): the range for co-sponsors in 2031", "",
              "| 2031 state | Balance at the start of 2031 | Payments fully funded | Leftover p10 | Median | p90 |", "|---|---|---|---|---|---|"]
        for n, v, ok, (a, m_, c) in d["cond"]:
            L.append(f"| {n} | {money(v)} | {ok:.2%} | {money(a)} | {money(m_)} | {money(c)} |")
        L += ["", "### Wealth at the start of each year (BASE)", "", "| Year | p10 | Median | p90 | Floor |", "|---|---|---|---|---|"]
        for k, y in enumerate(range(FIRST_YEAR, 2034)):
            col = [r["wealth"][k] for r in d["base"]]
            L.append(f"| {y} | {money(q(col, 0.10))} | {money(q(col, 0.50))} | {money(q(col, 0.90))} | {money(floors[y])} |")
    L += ["", "## Crash replays (actual years placed just before 2033; other years at M02 BASE 5.5%)", "",
          "Deterministic stress tests, the same under both histories.", "",
          "| Replay | Wealth at the start of 2033 | All payments funded | Leftover in 2033 | Leftover vs no crash |", "|---|---|---|---|---|"]
    w0, left0, _, _ = replay({})
    for name, crash in REPLAYS:
        w33, left, paid, _ = replay(crash)
        L.append(f"| {name} | {money(w33)} | {'yes' if paid['all_payments_funded'] else 'NO: short ' + money(paid['total_shortfall'])} | "
                 f"{money(left)} | {(left / left0 - 1):+.0%} |")
    L += ["", f"Lognormal cross-check (M02 BASE 6.95%, 17.8%): payments funded {logn['success']:.2%}; leftover middle 80% "
          f"{money(logn['left'][1])} to {money(logn['left'][5])}, median {money(logn['left'][3])}.", "",
          "Files: `M07_fan_BASE_<start>.csv` (fan chart), `M07_path_summary_<start>.csv` (M08's input: BASE, one row per path and gift share)."]
    (OUT / "M07_summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
