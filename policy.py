"""Draft reserve policy for M07 to execute.

Rules that follow from the case and the model are filled in. Choices that
belong to people are left as UNDECIDED with the roles who decide them.
"""


def undecided(owner, question):
    return {"value": None, "status": "UNDECIDED", "owner": owner,
            "question": question}


def draft_policy(terms, model_version, source_versions):
    return {
        "policy_id": "M05-operating-reserve",
        "version": model_version,
        "status": "PROVISIONAL",
        "source_versions": source_versions,
        "payments": {
            "amount": terms["payment"],
            "count": terms["n_payments"],
            "first_year": terms["first_year"],
            "timing": "beginning of each year; not adjusted for inflation",
        },
        "sizing_rule": {
            "formula": "reserve_required = payment * sum over k = 0 to "
                       "n - 1 of (1 + sizing_yield) ^ -k",
            "method": "explicit sum; k = 0 is the immediate first payment",
            "sizing_yield": undecided(
                "P2 (M02), approved by P1 and P4",
                "Which sourced yield sizes the reserve? TEST rates only "
                "until M02 is approved."),
            "information_rule": "Uses only what is known at the start of "
                                "2033. Never uses a path's later returns.",
        },
        "transfer_rule": "actual_reserve_transfer = min(reserve_required, "
                         "max(0, available_2033))",
        "gap_rule": "reserve_gap = reserve_required - actual_reserve_transfer",
        "facility_gift_rule": "Zero while reserve_gap > 0. Otherwise set "
                              "by M08.",
        "run_off_rule": {
            "order": "Pay first, then apply that year's return. No return "
                     "after the final payment.",
            "funding": "payment_funded = min(payment_due, max(0, balance)); "
                       "shortfall = payment_due - payment_funded",
            "limits": "Balances never go negative. No borrowing. No outside "
                      "money.",
            "return_model": "Flat total return on the whole reserve. To be "
                            "replaced by instrument cash flows after M04.",
        },
        "success_measures": {
            "reserve_established": "reserve_gap is zero at formation",
            "all_payments_funded": "every shortfall is zero",
            "note": "Report both. A reserve that starts short can still pay "
                    "everything on lucky returns; that is not the same as "
                    "being established.",
            "tolerance_dollars": 0.005,
        },
        "asset_composition": undecided(
            "P1 and P4, with P3's M04 evidence",
            "What does the reserve hold at formation: a bond ladder, a "
            "bond fund, cash, or a mix?"),
        "payment_order": undecided(
            "P1 and P4",
            "Which assets are sold or mature to fund each payment?"),
        "rebalancing_rule": undecided(
            "P1 and P4",
            "Does the composition change as payments approach, and when?"),
        "top_up_rule": undecided(
            "P1 (M08)",
            "Can retained assets top up a short reserve? Default is no."),
        "high_certainty_definition": undecided(
            "P1 and P4, after M07",
            "What funding probability counts as a high degree of "
            "certainty?"),
        "eligibility_caveats": [
            "Check any proposed instrument in the WInS portal; a public "
            "ticker is not proof of eligibility.",
            "A bond fund does not mature on a payment date. Model its "
            "sales and price risk instead.",
            "Today's yield is not a locked 2033 reinvestment rate.",
        ],
    }
