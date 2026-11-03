# New candidates: results (TEST preview, 3 Nov 2026, all Round 1 data in)

Full rankings: `outputs/new_candidates/M12_new_candidates_summary.md` (`python tools/score_new_candidates.py`). Round 2 values: `outputs/round2/Round2_scorecard_newcands.md` (`python tools/round2_team.py newcands`). M12 is a research filter, never a value, return or weight.

**Pat, 3 Nov:** the top-2-per-industry rule is a guide, not a hard limit. Several strong picks from one industry are fine.

## M12 with the new names (existing peers + new names that pass the screens)

| Industry | Released? | Top 3 | New names worth a look |
|---|---|---|---|
| Payments | yes | DLO 32/32, ADYEN 28/32, PYPL 4/32 | none (Edenred 6th) |
| Exchanges and data | yes | **HKEX 31/32, Tradeweb 29/32**, Morningstar 3/32 | HKEX, Tradeweb: valued below, both fail |
| IT services | yes | INFY 30/32, TCS 30/32, Booz Allen 2/32 | Booz Allen, Leidos (weak, 2-3/32). Cognizant drops to 8th of 13 |
| Power | no (diagnostic) | Kenon 32/32, PSEG 29/32, Drax 4/32 | none robust |
| Medtech | yes | ResMed 32/32, **Dexcom 32/32**, Alcon 0/32 | Dexcom: Round 2 requested |
| Software | yes | INTU 32/32, ADBE 28/32, Veeva 2/32 | Veeva (weak) |
| Consumer brands | yes (L'Oreal on combined capex) | **Lululemon 32/32, Haleon 25/32**, adidas 7/32 | Lululemon, Haleon: Round 2 requested; adidas optional |
| Pharma and biotech | yes | **Novo Nordisk 32/32**, Novartis 30/32, Vertex 2/32 | Novo: Round 2 requested |
| Internet and digital | no (diagnostic) | Trip.com 32/32, Meta 27/32, Booking 1/32 | Auto Trader 6th: valued below, fails |
| Semiconductors | yes | NVDA 32/32, Lam 24/32, ASM International 9/32 | ASM International optional |
| Aerospace and defence | yes (GE on combined capex) | GD 32/32, **Curtiss-Wright 31/32**, GE 0/32 | Curtiss-Wright: Round 2 requested |

Screened out: Corpay (bank-like), EVERTEC (market cap about $1.95bn, under $2bn), Payoneer, PTC, MarketAxess and eBay (being acquired), Engie (negative operating cash flow). Not scorable (a loss three years ago makes EPS growth undefined): Toast, Kyndryl, DXC, Centrica, Workday, Constellation Brands, Uber, Spotify, Pinterest, Safran, Embraer.

## Round 2 for the first three new names (beta 1.0 unless stated)

| | Value / price | Full-history beta | Bear / price | Result |
|---|---|---|---|---|
| HKEX (HK$367.40) | 0.72 | 0.64 (beta 1.18) | 0.51 | fails. Capex excludes the one-off HK$3,148m headquarters purchase; including it lowers the value further |
| Tradeweb ($122.54) | 0.70 | 0.87 (beta 0.69) | 0.47 | fails |
| Auto Trader (£5.38) | 0.97 | 1.02 (beta 0.92) | 0.68 | fails (no upside at beta 1.0) |

## Meta (Akshath, 3 Nov)

- 2026 capex guidance $135-145bn (21 Oct 2026 release, includes finance-lease principal); MarketScreener consensus capex $139.9bn (2026), $211.3bn (2027), $229.5bn (2028), revision date MISSING.
- 2025 one-off tax charge $15.93bn (Q3 2025; One Big Beautiful Bill Act; $14.03bn valuation allowance on US deferred tax assets).
- Removing the charge (tax 11.1% instead of 29.6%) lifts the standard-method value from $16 to **$223 (0.36x the $614.99 price)**.
- Guided and consensus capex is 55%, 68% and 62% of consensus revenue in 2026-28, against 35% in 2025, so using it would lower the value again.
- **Conclusion:** our method cannot value Meta. The value depends on the return the AI spending earns, which the method does not model. Meta stays "not validly valued"; the portfolio already holds it through VOO.
