# Trading Notes: bond ladder (draft, 7 Oct 2026 quotes)

**How to use these.** Write each note at the time of the trade. Numbers in
[brackets] are planned figures from WInS quotes on 7 Oct 2026. Replace them
with the actual fill (price, units or shares, total) before you submit. The
notes are copied verbatim into the Trading Notes Analysis, due 23 Oct.

## The reasoning behind every bond trade

1. **The obligation.** Laura owes ten fixed $50,000 payments, at the start of
   each year from 2033 to 2042. They are nominal: never adjusted for inflation
   (CASE, SRC-17). Missing one is a real failure, so these payments come before
   any growth goal.
2. **The tool.** A fixed dollar payment on a fixed date is best matched by an
   asset that repays a fixed dollar amount just before that date. US Treasuries
   held to maturity do exactly that. They are backed by the US government, paid
   in dollars (no currency risk), and their price swings before maturity don't
   matter if we never sell.
3. **The ladder.** Each payment gets its own holding that matures shortly
   before it. Where WInS has no individual Treasury in the right year
   (2033-2037), we use iShares iBonds funds. Each holds Treasuries maturing in
   one specific year and pays out in December of that year.
4. **The size.** Under our Option 3 floor rule (m = 2), bonds are 33.6% of the
   portfolio at today's 5.24% blended yield. The rest is growth. Money is split
   across the ten payments in proportion to each payment's present value, so
   every holding grows to the same amount (about $17,245 per payment on the
   $300,000 WInS account). If stocks fall, the rule moves money into bonds;
   by the start of 2033 the bonds must cover the full reserve.
5. **The timing.** 5- to 10-year Treasury yields were 5.03-5.18% on 24 Sep 2026
   (Federal Reserve H.15, SRC-01). Our bonds lock in 5.2-5.6%. Official
   projections expect lower rates: the CBO's 10-year yield path is about 4.4%
   from 2031 (SRC-06, secondary summary), and the FOMC median puts the fed
   funds rate at 4.1% by end-2027 (SRC-02). Buying now locks in today's higher
   yields. A higher locked yield makes the floor cheaper and leaves more money
   for growth.
6. **The risk we accept.** If yields rise further, we will have locked in less
   than we could have. We accept that, because the goal is certainty for the
   payments, not the best bond return.

---

## 1. IBTM: iShares iBonds Dec 2032 Term Treasury ETF (funds the Jan 2033 payment)

Bought [589] shares of IBTM at [$21.73] (limit order), about [$12,799].

IBTM holds US Treasuries that all mature in 2032 and pays out in December 2032,
just before Laura's first $50,000 payment in January 2033. That payment comes
first, right as the reserve is formed, so it has the least time to grow and
gets the largest share of the bond money (12.7%). No individual Treasury
tradeable in WInS matures between Feb 2031 and Feb 2036, so a fund is the
closest match. Estimated yield [~4.9%]: estimated from the fund's price fall
since July, to be replaced by iShares' published yield to maturity. Expense
ratio 0.07%. At that yield the holding grows to about [$17,245] by January
2033.

Risk: the fund price moves with interest rates before 2032. That doesn't matter
if we hold to maturity. We used a limit order because the after-hours bid/ask
spread was about 8% wide.

## 2. IBTO: iShares iBonds Dec 2033 Term Treasury ETF (funds the Jan 2034 payment)

Bought [530] shares of IBTO at [$22.96] (limit order), about [$12,169].

IBTO's Treasuries mature in 2033 and the fund pays out in December 2033,
funding Laura's January 2034 payment. WInS has no individual Treasury maturing
in 2033, so this iBonds fund is the exact-year substitute. Estimated yield
[~4.95%]: the price fell from $23.79 (July NAV) to $22.96 as yields rose in
September, which means we now lock in a higher yield than in summer. Expense
ratio 0.07%. Size: 12.1% of the bond sleeve, in proportion to the present value
of the 2034 payment. It grows to about [$17,245] by January 2034.

Risk: if rates rise further, the price falls before maturity. Held to December
2033, that doesn't affect the payment. Limit order used because of wide
after-hours quotes.

## 3. IBTP: iShares iBonds Dec 2034 Term Treasury ETF (funds the Jan 2035 payment)

Bought [481] shares of IBTP at [$24.01] (limit order), about [$11,549].

IBTP matures in December 2034 and funds the January 2035 payment. It's the
third rung of the ladder, and again no individual Treasury in WInS matures in
2034. Estimated yield [~5.0%]: the price fell 4% since July (from $25.01),
reflecting the September rise in yields that we are now locking in. Expense
ratio 0.07%. Size: 11.5% of the bond sleeve. It grows to about [$17,245] by
January 2035.

Risk: price moves before maturity are irrelevant if held to December 2034. The
small fee is accepted as the cost of having an exact 2034 maturity.

## 4. IBTQ: iShares iBonds Dec 2035 Term Treasury ETF (funds the Jan 2036 payment)

Bought [462] shares of IBTQ at [$23.59] (limit order), about [$10,899].

IBTQ matures in December 2035 and funds the January 2036 payment. We considered
the 4.500% Treasury maturing 15 Feb 2036 and rejected it. WInS prices it at
$1,029.77, a yield to maturity of only 4.11%, while neighbouring maturities
yield 5.0-5.2%. At a fair yield it should cost about $955, so buying it would
have meant overpaying by about 8%. It also matures six weeks after the payment
is due. IBTQ matures before the payment at an estimated [~5.1%] yield (its
price fell 4.4% since July). Size: 10.8% of the bond sleeve. It grows to about
[$17,245] by January 2036.

Risk: held to maturity, so price moves before 2035 don't matter. Limit order
used.

## 5. IBTR: iShares iBonds Dec 2036 Term Treasury ETF (funds the Jan 2037 payment)

Bought [441] shares of IBTR at [$23.37] (limit order), about [$10,306].

IBTR matures in December 2036 and funds the January 2037 payment. Without it,
the only Treasury nearby (15 Feb 2037) matures six weeks after the payment and
would have to be sold early. IBTR keeps our rule that every payment is funded
by something that has already matured. Estimated yield [~5.15%], between the
2035 fund and the 2037 Treasury. Size: 10.2% of the bond sleeve. It grows to
about [$17,245] by January 2037.

Risk: the after-hours quote was $11.66 / $34.98, so a market order would have
paid about 50% too much. We used a limit order near the last trade ($23.37)
during market hours.

## 6. T-BOND 4.750% 15-Feb-2037 (funds the Jan 2038 payment)

Bought [10] units ($1,000 face each) at [$962.07] plus [$6.64] accrued
interest, about [$9,687]. Yield to maturity [5.23%].

This bond matures on 15 Feb 2037. Its $10,000 principal plus reinvested coupons
(4.75% a year) is held in T-bills until Laura's January 2038 payment, about
10.5 months later. We would have preferred a bond maturing in late 2037, but
the Feb 2038 Treasury is listed and not tradeable in WInS, and nothing else
matures in 2037. Using a bond that matures before the payment means we never
depend on selling a bond early at an unknown price. The cost is that the cash
earns T-bill rates for those 10 months. As an individual Treasury it has no
fund fee, and its yield is fixed at purchase. Size: 9.6% of the bond sleeve. It
grows to about [$17,245] by January 2038.

Risk: reinvestment risk on about 10 months of cash, which is small. Held to
maturity, price moves don't matter.

## 7. T-BOND 4.500% 15-May-2038 (funds the Jan 2039 payment)

Bought [10] units at [$932.88] plus [$6.29] accrued interest, about [$9,392].
Yield to maturity [5.28%].

This bond matures on 15 May 2038, about 7.5 months before Laura's January 2039
payment. The principal and coupons wait in T-bills until then. It is the
closest tradeable Treasury maturing before that payment. Bought below its
$1,000 face value, part of its 5.28% yield comes from the price rising to face
value by 2038 and part from the 4.5% coupon. No fee, and the yield is fixed for
12 years. Size: 9.1% of the bond sleeve. It grows to about [$17,245] by January
2039.

Note: WInS lists this bond's last coupon as 15 Aug 2026, which is unusual for a
May-maturity bond. It only affects accrued interest by a few dollars; recorded
in case the order total differs slightly.

## 8. T-BOND 4.500% 15-Aug-2039 (funds the Jan 2040 payment)

Bought [9] units at [$916.51] plus [$6.04] accrued interest, about [$8,303].
Yield to maturity [5.41%].

This bond matures on 15 Aug 2039, about 4.5 months before the January 2040
payment, and is the closest tradeable maturity before that date. It locks in
5.41% for 13 years. That's above the model's 5% assumption and above the CBO's
~4.4% long-run projection, which lowers the cost of securing this payment. Size:
8.5% of the bond sleeve. It grows to about [$17,245] by January 2040.

Risk: if yields rise after purchase, the bond's market price falls. We hold it
to maturity, so the $9,000 principal plus coupons arrive regardless.

## 9. T-BOND 4.250% 15-Nov-2040 (funds the Jan 2041 payment)

Bought [9] units at [$878.88] plus [$16.65] accrued interest, about [$8,060].
Yield to maturity [5.50%].

This bond matures on 15 Nov 2040, about six weeks before the January 2041
payment: a close match between maturity and obligation. It locks in 5.50% for
14 years with no fee. Size: 8.0% of the bond sleeve. It grows to about
[$17,245] by January 2041.

Risk: as a long bond it has the most price movement before maturity of the
holdings so far. That's irrelevant because we hold it to maturity. Its price
risk also offsets the floor's: if rates fall, the cost of securing the payments
rises, but so does this bond's value.

## 10. T-BOND 3.125% 15-Nov-2041 (funds the Jan 2042 payment)

Bought [10] units at [$751.05] plus [$12.24] accrued interest, about [$7,633].
Yield to maturity [5.59%].

This bond matures on 15 Nov 2041, six weeks before Laura's last payment in
January 2042, so it closes the ladder. It trades at a deep discount: we pay
$751 for $1,000 repaid at maturity. Most of its 5.59% yield comes from that rise
to face value, plus a 3.125% coupon. That also means a larger share of the
return is fixed at purchase rather than depending on reinvesting coupons. It is
the highest yield in the ladder and the smallest holding (7.5%), because the
last payment has 15 years to grow. It grows to about [$17,245] by January 2042.

Risk: the longest maturity has the largest price swings in the meantime. Held
to maturity, they don't affect the payment.
