"""M12 Transparent Fundamental Score (TFS), from the P3 M12 build guide.

Eight measures in four pillars, scored by average rank inside each peer
group. The score is a research filter: never a fair value, an expected
return, a trade signal or a portfolio weight.

Rules R1-R8 adapt the guide to our data. They are proposals pending Pat's
sign-off (handoff/M12_score_spec.md), so each one is a switch in RULES.
"""

import csv

MISSING, UNSUITABLE = "MISSING", "UNSUITABLE"

# (id, pillar, direction): +1 higher is better, -1 lower is better.
MEASURES = [("Q1", "Quality", 1), ("Q2", "Quality", 1),
            ("B1", "Balance", -1), ("B2", "Balance", 1),
            ("G1", "Growth", 1), ("G2", "Growth", 1),
            ("V1", "Valuation", 1), ("V2", "Valuation", 1)]
WEIGHTS = {m: 0.125 for m, _, _ in MEASURES}

# Video cross-check (diagnostic only): pillars stay at 25%, new measures
# share their pillar equally.
CROSS_MEASURES = MEASURES + [("ROE", "Quality", 1), ("PS", "Valuation", -1),
                             ("PB", "Valuation", -1)]
CROSS_WEIGHTS = {"Q1": 0.25 / 3, "Q2": 0.25 / 3, "ROE": 0.25 / 3,
                 "B1": 0.125, "B2": 0.125, "G1": 0.125, "G2": 0.125,
                 "V1": 0.0625, "V2": 0.0625, "PS": 0.0625, "PB": 0.0625}

RULES = {
    "R1": True,    # group-wide pre-tax margin when an operating income is unavailable
    "R3": True,    # continuing-operations EPS for both years where reported
    "R4": "Payments",  # add capitalized software to capex only in these groups
    "R8": True,    # finance leases not quantified -> reported borrowings (issuer immaterial)
}
MIN_COMPLETE, MIN_COVERAGE = 5, 0.8


def num(row, key):
    value = (row.get(key) or "").strip()
    return float(value) if value else None


def percentile_scores(values, direction):
    """s = 100 x (RANK.AVG(dir x value, ascending) - 1) / (n - 1).

    Returns ({id: score}, flag). n = 1 or all tied gives 50 for everyone.
    """
    adjusted = {k: direction * v for k, v in values.items()}
    n = len(adjusted)
    if n == 1 or len(set(adjusted.values())) == 1:
        return {k: 50.0 for k in adjusted}, "NO_DISCRIMINATION"
    ordered = sorted(adjusted.values())
    scores = {}
    for k, v in adjusted.items():
        first = ordered.index(v) + 1
        rank = first + (ordered.count(v) - 1) / 2  # RANK.AVG
        scores[k] = 100 * (rank - 1) / (n - 1)
    return scores, ""


def weighted_total(scores, weights):
    """Weighted score; blank (None) if any weighted measure is missing."""
    if any(scores.get(m) is None for m, w in weights.items() if w):
        return None
    total = sum(weights.values())
    return sum(scores[m] * w for m, w in weights.items()) / total


def cagr(end, start):
    if end is None or start is None:
        return None, MISSING
    if end <= 0 or start <= 0:
        return None, UNSUITABLE
    return (end / start) ** (1 / 3) - 1, ""


def operating_income(row):
    reported = num(row, "operating_income_fy0")
    if reported is not None:
        return reported
    if row.get("operating_build_verified", "").upper() == "TRUE":
        return num(row, "operating_income_built_fy0")
    return None


def measures(row, group_rows, rules=RULES):
    """Raw values for one company: {measure: (value or None, code, note)}."""
    out = {}
    rev, rev3 = num(row, "revenue_fy0"), num(row, "revenue_fy3")
    a0, a1 = num(row, "total_assets_fy0"), num(row, "total_assets_fy1")
    mcap = num(row, "market_cap_cutoff_proxy_m")

    # Q1: operating margin, or group-wide pre-tax margin (R1).
    use_pretax = rules["R1"] and any(operating_income(r) is None
                                     for r in group_rows)
    profit = num(row, "pretax_income_fy0") if use_pretax else operating_income(row)
    note = "pretax (R1)" if use_pretax else "operating"
    out["Q1"] = ((profit / rev, "", note) if profit is not None and rev and rev > 0
                 else (None, MISSING, note))

    out["Q2"] = ((rev / ((a0 + a1) / 2), "", "") if None not in (rev, a0, a1)
                 and rev > 0 and a0 + a1 > 0 else (None, MISSING, ""))

    # B1: finance-lease-inclusive debt; R8 falls back to reported borrowings.
    debt, note = num(row, "total_debt_fy0"), "reconciled"
    if debt is None and rules["R8"]:
        debt, note = num(row, "borrowing_debt_original_fy0"), "borrowings (R8)"
    out["B1"] = ((debt / a0, "", note) if debt is not None and a0 and a0 > 0
                 else (None, MISSING, note))

    ca, cl = num(row, "current_assets_fy0"), num(row, "current_liabilities_fy0")
    out["B2"] = ((ca / cl, "", "") if ca is not None and cl and cl > 0
                 else (None, MISSING, ""))

    g1, code = cagr(rev, rev3)
    out["G1"] = (g1, code, "")

    e0, e3, note = num(row, "eps_diluted_fy0"), num(row, "eps_diluted_fy3"), "total"
    c0, c3 = num(row, "eps_cont_fy0"), num(row, "eps_cont_fy3")
    # A year with no discontinued operations reports only total EPS, which is
    # then the continuing figure (e.g. ZBH: continuing EPS only for FY-3).
    if rules["R3"] and (c0 is not None or c3 is not None):
        e0 = c0 if c0 is not None else e0
        e3 = c3 if c3 is not None else e3
        note = "continuing (R3)"
    g2, code = cagr(e0, e3)
    out["G2"] = (g2, code, note)

    earnings = num(row, "earnings_common_fy0")
    out["V1"] = ((earnings / mcap, "", "") if earnings is not None and mcap
                 and mcap > 0 else (None, MISSING, ""))

    cfo, capex = num(row, "cfo_fy0"), num(row, "capex_fy0")
    note = "capex as reported"
    if row["peer_group"] in rules["R4"].split(",") and capex is not None:
        software = num(row, "capex_software_fy0")
        capex = None if software is None else capex + software
        note = "capex + capitalized software (R4)"
    out["V2"] = (((cfo - capex) / mcap, "", note) if None not in (cfo, capex)
                 and mcap and mcap > 0 else (None, MISSING, note))

    # Cross-check extras (diagnostic only).
    equity = num(row, "total_equity_fy0")
    bad_equity = equity is None or equity <= 0
    code = MISSING if equity is None else UNSUITABLE
    out["ROE"] = ((None, code, "") if bad_equity or earnings is None
                  else (earnings / equity, "", ""))
    out["PB"] = ((None, code, "") if bad_equity or not mcap
                 else (mcap / equity, "", ""))
    out["PS"] = ((mcap / rev, "", "") if mcap and rev and rev > 0
                 else (None, MISSING, ""))
    return out


def score_group(group_rows, rules=RULES, weights=WEIGHTS,
                measure_list=MEASURES):
    """Score one peer group. Only complete companies are ranked."""
    raw = {r["ticker"]: measures(r, group_rows, rules) for r in group_rows}
    ids = [m for m, _, _ in measure_list if weights.get(m)]
    complete = [t for t in raw if all(raw[t][m][0] is not None for m in ids)]
    coverage = len(complete) / len(raw) if raw else 0
    released = len(complete) >= MIN_COMPLETE and coverage >= MIN_COVERAGE
    scores = {t: {} for t in raw}
    flags = []
    for m, _, direction in measure_list:
        if m not in ids or not complete:
            continue
        s, flag = percentile_scores({t: raw[t][m][0] for t in complete},
                                    direction)
        if flag:
            flags.append(f"{m}:{flag}")
        for t, v in s.items():
            scores[t][m] = v
    totals = {t: weighted_total(scores[t], weights) if t in complete else None
              for t in raw}
    shortlist = shortlist_of(totals) if released else []
    return {"raw": raw, "scores": scores, "totals": totals,
            "complete": complete, "coverage": coverage, "released": released,
            "shortlist": shortlist, "flags": flags}


def shortlist_of(totals, size=2):
    """Top `size` scores, keeping ties at the boundary."""
    ranked = sorted((v for v in totals.values() if v is not None), reverse=True)
    if not ranked:
        return []
    cutoff = ranked[min(size, len(ranked)) - 1]
    return sorted((t for t, v in totals.items() if v is not None and v >= cutoff),
                  key=lambda t: -totals[t])


def variants(weights=WEIGHTS, measure_list=MEASURES):
    """The guide's 32 sensitivity variants: (name, renormalized weights)."""
    out = []

    def renorm(mult):
        raw = {m: weights[m] * mult.get(m, 1.0) for m in weights}
        total = sum(raw.values())
        return {m: w / total for m, w in raw.items()}

    ids = [m for m, _, _ in measure_list]
    for m in ids:
        for a in (0.8, 1.2):
            out.append((f"{m} x{a}", renorm({m: a})))
    for pillar in dict.fromkeys(p for _, p, _ in measure_list):
        members = [m for m, p, _ in measure_list if p == pillar]
        for a in (0.8, 1.2):
            out.append((f"{pillar} x{a}", renorm({m: a for m in members})))
    for m in ids:
        out.append((f"drop {m}", renorm({m: 0.0})))
    return out


def stability(result, weights=WEIGHTS, measure_list=MEASURES):
    """How often each ranked company stays on the shortlist across variants."""
    kept = {t: 0 for t in result["complete"]}
    worst_rank = {t: 1 for t in result["complete"]}
    names = variants(weights, measure_list)
    for _, w in names:
        totals = {t: sum(result["scores"][t][m] * w[m] for m in w)
                  for t in result["complete"]}
        for t in shortlist_of(totals):
            kept[t] += 1
        order = sorted(totals, key=lambda t: -totals[t])
        for t in order:
            worst_rank[t] = max(worst_rank[t], order.index(t) + 1)
    return {t: (kept[t], len(names), worst_rank[t]) for t in kept}


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def score_all(rows, rules=RULES, weights=WEIGHTS, measure_list=MEASURES):
    groups = {}
    for r in rows:
        groups.setdefault(r["peer_group"], []).append(r)
    return {g: score_group(rs, rules, weights, measure_list)
            for g, rs in groups.items()}
