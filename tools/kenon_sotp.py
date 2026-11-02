"""Kenon option 1 (Pat, 2 Nov 2026): value OPC's parts on their own cash flows.

TEST preview. Every input carries a label (RESEARCH / ASSUMPTION / CASE) and a
source. Missing facts are bracketed, never filled:
  - the split of OPC's net debt between Israel, CPV and OPC's head office is
    MISSING, so the share of net debt borne by OPC's shareholders runs from
    the lowest segment ownership (71%) to 100% (all at the head office);
  - Basin Ranch spending to date is MISSING (0% and 25% spent shown);
  - maintenance capex and cash taxes are MISSING, so EBITDA -> free cash flow
    is an explicit conversion ASSUMPTION with a range.

Run: python tools/kenon_sotp.py  (writes nothing; prints the tables)
"""
from itertools import product

IN = {  # value, label, source
    "israel_ebitda_h1": (90, "RESEARCH", "OPC H1 2026 board report (Kenon 6-K), EBITDA after proportionate consolidation, Israel"),
    "us_ebitda_h1": (170, "RESEARCH", "Same, US total (Energy Transition 169, Renewables 22, CPV other -21)"),
    "group_ebitda_h1": (255, "RESEARCH", "Same, consolidated; head office = 255 - 90 - 170 = -5"),
    "fy_over_h1_2025": (457 / 203, "RESEARCH", "FY2025 457 / H1 2025 203 (Kenon FY2025 release; H1 2026 report): H2 is the stronger half"),
    "own_israel": (0.80, "RESEARCH", "OPC 80% of OPC Israel, Veridis 20% (Kenon 20-F)"),
    "own_cpv": (0.7109, "RESEARCH", "OPC about 71.09% of CPV Group at 12 Mar 2026 (Kenon 20-F FY2025)"),
    "debt": (2977, "RESEARCH", "OPC consolidated debt 30 Jun 2026 (Kenon Q2 2026 release)"),
    "cash": (1261, "RESEARCH", "OPC unrestricted cash 30 Jun 2026; restricted 187 excluded"),
    "assoc_debt": (642, "RESEARCH", "OPC's share of CPV associates' debt 30 Jun 2026"),
    "assoc_cash": (56, "RESEARCH", "OPC's share of CPV associates' cash 30 Jun 2026"),
    "kenon_stake": (0.46, "RESEARCH", "Kenon about 46% of OPC (Q2 2026 6-K)"),
    "kenon_cash": (605, "RESEARCH", "Kenon stand-alone cash 31 Aug 2026, no material debt (Q2 2026 release)"),
    "kenon_shares": (52.11, "RESEARCH", "Kenon shares, m (20-F cover, as used by Aryu)"),
    "kenon_price": (64.11, "RESEARCH", "Kenon close 30 Oct 2026 (Yahoo Finance, Aryu)"),
    "opc_shares": (310, "RESEARCH", "OPC shares about 310m (calculated from the March 2026 placement, 8m = 2.65%)"),
    "opc_price_nis": (93.93, "RESEARCH", "OPC TASE close 30 Oct 2026, 9,393 agorot (read by Pat)"),
    "usd_ils": (3.14, "RESEARCH", "About NIS 3.14 per USD, 30 Oct 2026 (aggregators)"),
    "rf": (0.0498, "RESEARCH", "US 10-year, 4.98% (Pat's FRED read; see the 4.94% note)"),
    "erp": (0.05, "ASSUMPTION", "Kit default"),
    "beta": (1.0, "ASSUMPTION", "Kit standard method (Kenon measured 1.03)"),
    "crp_israel": (0.0198, "RESEARCH", "Israel country risk premium, Damodaran July 2026"),
    "debt_weight": (3619 / (3619 + 9273), "RESEARCH", "OPC debt incl. associates 3,619 vs market cap 9,273"),
    "tax": (0.25, "ASSUMPTION", "For the debt tax shield (Israel 23%, US about 25%)"),
    "g": (0.02, "ASSUMPTION", "Long-run growth of the existing fleet: plants age; growth projects valued separately"),
    "conversion": ((0.60, 0.70, 0.80), "ASSUMPTION", "Unlevered free cash flow / EBITDA after maintenance capex and cash tax; MISSING data, range shown"),
    "br_ebitda": ((250, 275), "RESEARCH", "Basin Ranch first-full-year figures about $250m and $275m (Kenon 6-K table, layout unclear)"),
    "br_cost": ((1800, 2000), "RESEARCH", "Basin Ranch expected cost $1.8-2.0bn (Kenon 6-K); CPV owns 100%"),
    "br_first_year": (2030, "ASSUMPTION", "COD 2029 (CPV), so the first full year is 2030"),
    "valuation_date": (2026.83, "CASE", "30 Oct 2026"),
}
V = {k: v[0] for k, v in IN.items()}


def wacc(extra=0.0, shift=0.0):
    ke = V["rf"] + V["beta"] * V["erp"] + extra
    kd = (V["rf"] + 0.005) * (1 - V["tax"])  # kit default: 10-year + 0.5 points
    w = V["debt_weight"]
    return (1 - w) * ke + w * kd + shift


def perpetuity(ebitda, conv, r):
    return ebitda * conv * (1 + V["g"]) / (r - V["g"])


def basin_ranch(conv, r, spent):
    """NPV at the valuation date: perpetuity from the first full year, less remaining cost."""
    ebitda = sum(V["br_ebitda"]) / 2
    cost = sum(V["br_cost"]) / 2
    t_value = V["br_first_year"] - 1 - V["valuation_date"]  # value sits at the start of the first full year
    pv_ops = perpetuity(ebitda, conv, r) / (1 + V["g"]) / (1 + r) ** t_value
    pv_cost = cost * (1 - spent) / (1 + r) ** 1.5  # spread to 2029; midpoint about 1.5 years
    return pv_ops - pv_cost


def run(conv, shift, debt_share, spent, with_br=True):
    scale = V["fy_over_h1_2025"]
    r_us, r_il = wacc(shift=shift), wacc(extra=V["crp_israel"], shift=shift)
    israel = perpetuity(V["israel_ebitda_h1"] * scale, conv, r_il)
    us = perpetuity(V["us_ebitda_h1"] * scale, conv, r_us)
    hq_ebitda = (V["group_ebitda_h1"] - V["israel_ebitda_h1"] - V["us_ebitda_h1"]) * scale
    hq = perpetuity(hq_ebitda, 1.0, r_us)
    br = basin_ranch(conv, r_us, spent) if with_br else 0.0
    net_debt = V["debt"] - V["cash"] + V["assoc_debt"] - V["assoc_cash"]
    opc_equity = (V["own_israel"] * israel + V["own_cpv"] * (us + br) + hq
                  - debt_share * net_debt)
    kenon = (V["kenon_stake"] * opc_equity + V["kenon_cash"]) / V["kenon_shares"]
    opc_nis = opc_equity * V["usd_ils"] / V["opc_shares"]
    return dict(israel=israel, us=us, hq=hq, br=br, net_debt=net_debt,
                opc_equity=opc_equity, opc_nis=opc_nis, kenon=kenon,
                ratio=kenon / V["kenon_price"], r_us=r_us, r_il=r_il)


if __name__ == "__main__":
    lo_share = min(V["own_israel"], V["own_cpv"])
    c = run(0.70, 0.0, (lo_share + 1) / 2, 0.25)
    print(f"WACC US {c['r_us']:.2%}, Israel {c['r_il']:.2%}; net debt (100% basis) {c['net_debt']:,.0f}")
    print(f"Central (conversion 70%, WACC as above, net-debt share midpoint, Basin Ranch 25% spent):")
    print(f"  Israel EV {c['israel']:,.0f}  CPV EV {c['us']:,.0f}  head office {c['hq']:,.0f}  "
          f"Basin Ranch NPV {c['br']:,.0f}")
    print(f"  OPC equity {c['opc_equity']:,.0f} = NIS {c['opc_nis']:.2f}/share (market {V['opc_price_nis']}); "
          f"Kenon ${c['kenon']:.2f} = {c['ratio']:.2f}x price")
    vals = [run(cv, sh, ds, sp, br)["kenon"] for cv, sh, ds, sp, br in
            product(V["conversion"], (-0.01, 0, 0.01), (lo_share, 1.0), (0.0, 0.25), (False, True))]
    print(f"Range over conversion 60-80%, WACC +/-1 point, net-debt share 71-100%, Basin Ranch on/off: "
          f"${min(vals):.2f} to ${max(vals):.2f}")
    print("\nKenon $/share: conversion (rows) x WACC shift (columns), Basin Ranch 25% spent, net-debt midpoint")
    for cv in V["conversion"]:
        print(f"  {cv:.0%}: " + "  ".join(f"{run(cv, sh, (lo_share + 1) / 2, 0.25)['kenon']:7.2f}"
                                            for sh in (-0.01, 0, 0.01)))
    # What the prices imply: OPC equity needed to justify each price.
    need_opc_mkt = V["opc_price_nis"] * V["opc_shares"] / V["usd_ils"]
    need_ken = (V["kenon_price"] * V["kenon_shares"] - V["kenon_cash"]) / V["kenon_stake"]
    print(f"\nOPC equity implied by OPC's own price: {need_opc_mkt:,.0f}; by Kenon's price: {need_ken:,.0f}; "
          f"this DCF (central): {c['opc_equity']:,.0f}")
    print(f"Gap to Kenon's price = value the market gives to projects not in this DCF "
          f"(Shay, Walker, Israeli projects, data centres): {need_ken - c['opc_equity']:,.0f} for OPC's shareholders")
