"""Operating reserve: sizing, transfer, gap, and run-off (M05).

All amounts are nominal US dollars. Rates are decimals.
"""

PAYMENT = 50_000
N_PAYMENTS = 10
FIRST_PAYMENT_YEAR = 2033

# Shortfalls smaller than half a cent are floating-point noise, not unpaid
# money. Used only when summarizing; the schedule keeps full precision.
TOLERANCE = 0.005


def required_reserve(net_yield, payment=PAYMENT, n_payments=N_PAYMENTS):
    """Dollars needed at the start of 2033 to fund every payment at a flat
    net yield. The first payment is made immediately.

    Raises ValueError if net_yield is -1 or lower.
    """
    if net_yield <= -1:
        raise ValueError(f"net_yield must be greater than -1, got {net_yield}")
    # Explicit sum over the ten payments. Payment k is k years away, so it is
    # divided by (1 + y) once per year. k = 0 is the immediate payment.
    return sum(payment / (1 + net_yield) ** k for k in range(n_payments))


def actual_reserve_transfer(required, available):
    """Dollars actually moved into the reserve, given what the portfolio
    holds right before the transfer."""
    return min(required, max(0, available))


def reserve_gap(required, transfer):
    """Part of the required reserve the portfolio could not fund."""
    return required - transfer


def form_reserve(available_2033, sizing_yield, payment=PAYMENT,
                 n_payments=N_PAYMENTS):
    """The reserve decision at the start of 2033.

    Uses only what is known then: the portfolio value and the sizing yield.
    Future returns are not an input, so two paths with the same 2033 state
    always get the same decision.
    """
    required = required_reserve(sizing_yield, payment, n_payments)
    transfer = actual_reserve_transfer(required, available_2033)
    gap = reserve_gap(required, transfer)
    return {
        "reserve_required": required,
        "available_assets": available_2033,
        "actual_reserve_transfer": transfer,
        "reserve_gap": gap,
        "reserve_established": gap <= TOLERANCE,
    }


def run_off(starting_balance, annual_returns, payment=PAYMENT,
            first_year=FIRST_PAYMENT_YEAR, n_payments=N_PAYMENTS):
    """Year-by-year schedule of the reserve paying out.

    annual_returns holds one return for each gap between payments, so it
    has n_payments - 1 values. Raises ValueError if the length is wrong.

    Returns a list of n_payments dicts, one per year, with the keys:
    year, balance_before_payment, payment_due, payment_funded, shortfall,
    balance_after_payment, return_rate, next_balance.
    In the last year, return_rate is None and next_balance equals
    balance_after_payment.
    """
    if len(annual_returns) != n_payments - 1:
        raise ValueError(
            f"need {n_payments - 1} annual returns (one per gap between "
            f"payments), got {len(annual_returns)}")
    if starting_balance < 0:
        raise ValueError("starting_balance cannot be negative")
    if any(r <= -1 for r in annual_returns):
        raise ValueError("an annual return of -100% or worse is impossible")

    rows = []
    balance = starting_balance
    for i in range(n_payments):
        # Payment first. Pay what is there, up to the amount due.
        funded = min(payment, max(0, balance))
        after = balance - funded
        # Then that year's return, except after the final payment.
        last = i == n_payments - 1
        rate = None if last else annual_returns[i]
        next_balance = after if last else after * (1 + rate)
        rows.append({
            "year": first_year + i,
            "balance_before_payment": balance,
            "payment_due": payment,
            "payment_funded": funded,
            "shortfall": payment - funded,
            "balance_after_payment": after,
            "return_rate": rate,
            "next_balance": next_balance,
        })
        balance = next_balance
    return rows


def summarize_run_off(rows):
    """Funding results for one schedule, in the terms M07 reports."""
    short_years = [r["year"] for r in rows if r["shortfall"] > TOLERANCE]
    return {
        "all_payments_funded": not short_years,
        "first_shortfall_year": short_years[0] if short_years else None,
        "total_shortfall": sum(r["shortfall"] for r in rows),
        "worst_single_shortfall": max(r["shortfall"] for r in rows),
    }
