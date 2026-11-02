"""Apply fact-check fixes 2-5 to Aryu's two docs as Word tracked changes.

Usage: python3 -I tools/aryu_tracked_fixes.py <folder with the two original docx> <out_dir>
(the originals are in context/teammates_2026-11-02/Aryu_stock_research_power_medtech_2026-11-02.zip)
Kenon's sections are deliberately not touched (Pat, 2 Nov).
"""
import sys
from copy import deepcopy
from pathlib import Path

import docx
from docx.oxml.ns import qn

AUTHOR = "Fact-check for Pat (Claude)"
DATE = "2026-11-02T12:00:00Z"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
NEXT_ID = [7000]

RF = "rf 4.00% (FRED DTB3, 30 Oct 2026; 3.97% before, which moves these ratios by about 0.001)"
PE_NOTE = ("Forward P/E row: scored against Damodaran's US total market forward P/E (27.66), "
           "the convention Pat used in Round 1, because the 10-year average could not be read "
           "from FactSet's chart. Damodaran PE data, January 2026.")
FPE_MEASURE = (" vs its own 10-year average", " vs the US total market (Pat's Round 1 convention)")
FPE_SOURCE = "Damodaran PE data (total market row, January 2026); see note"

POWER = [
    # Fix 4: industry score, forward P/E against the total market.
    (None, "Note on the forward P/E row: FactSet's 30 Oct 2026 Earnings Insight has a chart of each "
     "sector's forward P/E with its 10-year average (page 34), but the chart is a picture and I could "
     "not read the numbers. If the Utilities value is below its 10-year average, add 8.3 points "
     "(total 37.5, still below 50). FactSet Earnings Insight, 30 Oct 2026.",
     PE_NOTE + " Power's 17.59 is lower, so it earns 8.3 points (total 37.5, still below 50)."),
    ("Forward P/E (lower wins)",) + FPE_MEASURE,
    ("17.59", "MISSING", "27.66"),
    ("17.59", "Not scored", "Yes"),
    ("17.59", "0 of 8.3 (MISSING)", "8.3"),
    ("17.59", "Same; 10-year average not found (see note)", FPE_SOURCE),
    (None, "29.1 out of 100 (91.7 checked)", "37.5 out of 100"),
    (None, "The industry scores only 29 of 100", "The industry scores only 37.5 of 100"),
    # Fix 3: overstated claims.
    (None, "Constellation reports over 10,000 MW of long-term deals, including Microsoft (Crane restart) "
     "and Meta (Clinton, from mid-2027) (Constellation summary, Secondary).",
     "Constellation's long-term deals that I could confirm total about 4,700 MW plus the Crane restart "
     "for Microsoft: CyrusOne about 1,100 MW, Amazon 690 MW, Google 890 MW, Meta (Clinton, from "
     "mid-2027) about 1,100 MW, and 920 MW signed in Q2 2026, which may overlap with CyrusOne "
     "(Yahoo Finance, Baxtel, W.Media, Constellation Q2 2026 8-K). The \"over 10,000 MW\" in the "
     "secondary summary is not supported."),
    (None, "lifted OPC's (Kenon's) Q2 2026 earnings (OPC Q2 2026 release).",
     "lifted OPC's (Kenon's) Q2 2026 earnings (OPC Q2 2026 release). But the last three PJM capacity "
     "auctions all cleared at the price cap ($329.17, then $333.44 per MW-day, then the cap again for "
     "2028/29), so capacity prices are capped, not rising (PJM Inside Lines; Utility Dive)."),
    # Fix 2: CEG DCF at the FRED 30 Oct 10-year yield (4.98%).
    (None, "Beta 1.0: $146.41 (0.56). Measured 1.12: $133.79 (0.51). Adjusted 1.08: $137.74 (0.52)",
     "Beta 1.0: $145.03 (0.55). Measured 1.12: $132.59 (0.51). Adjusted 1.08: $136.49 (0.52)"),
    (None, "about 6.5 points a year above my base path: 11.5% to 12.5% a year early on, still 9.5% in year 10",
     "about 6.6 points a year above my base path: 11.6% to 12.6% a year early on, still 9.6% in year 10"),
    (None, "$64.00 (0.24 x price)", "$63.25 (0.24 x price)"),
    (None, "Base case is already 44% below the price", "Base case is already 45% below the price"),
    (None, "rf 3.97% (13-week T-bill)", RF),
    # Fix 3 and 5: CEG plan, guidance and competition.
    (None, "over 10,000 MW of long-term deals. Sources:",
     "about 4,700 MW of confirmed long-term deals in total plus Crane, not over 10,000 MW (see the "
     "drivers note). 6 Aug 2026: 2026 adjusted EPS guidance raised to $11.50 to $12.50, and 920 MW of "
     "new long-term contracts (Q2 2026 8-K). Sources:"),
    (None, "over 10,000 MW of signed long-term deals (comparison to verify)",
     "about 4,700 MW of confirmed long-term deals plus Crane (Vistra's and Talen's totals not found, "
     "so the comparison is still unverified)"),
    # Fix 2: NRG.
    (None, "Beta 1.0: $130.50 (1.36). Measured 1.22: $106.52 (1.11). Adjusted 1.15: $113.80 (1.18)",
     "Beta 1.0: $128.24 (1.34). Measured 1.22: $104.75 (1.09). Adjusted 1.15: $111.89 (1.16)"),
    (None, "Revenue growth 2.1 points below my base path (1.9% to 2.9% early)",
     "Revenue growth 2.0 points below my base path (2.0% to 3.0% early)"),
    (None, "$46.20 (0.48 x price)", "$44.82 (0.47 x price)"),
    (None, "+35.9% / -51.9% = 0.69", "+33.5% / -53.3% = 0.63"),
    (None, "With reported D&A instead the value was $213", "With reported D&A instead the value is $210"),
    (None, "The kit's cost of debt (5.4%)", "The kit's cost of debt (5.5%)"),
    # Fix 5: NRG competition and guidance.
    (None, "a large retail customer base (to verify against Vistra)",
     "a larger retail base: about 6 million retail energy customers vs Vistra's about 5 million "
     "(NRG 2025 10-K; Vistra S-3; not a same-date comparison)"),
    (None, "Guidance was kept (Motley Fool, 6 Aug 2026; Benzinga)",
     "Guidance was kept: 2026 adjusted EPS $7.90 to $9.90, reaffirmed 4 Aug (NRG Q2 2026 release; "
     "Motley Fool, 6 Aug 2026; Benzinga)"),
]

MEDTECH = [
    (None, "Forward P/E row: FactSet's 30 Oct 2026 Earnings Insight (page 34) charts the Health Care "
     "sector's forward P/E against its 10-year average, but the chart is a picture I could not read. "
     "If it is below its average, add 8.3 (total 54.2, above 50). FactSet Earnings Insight, 30 Oct 2026.",
     PE_NOTE + " Medtech's 42.33 is higher, so it earns 0 points (total stays 45.8)."),
    ("Forward P/E (lower wins)",) + FPE_MEASURE,
    ("42.33", "MISSING", "27.66"),
    ("42.33", "Not scored", "No"),
    ("42.33", "0 of 8.3 (MISSING)", "0 of 8.3"),
    ("42.33", "Same; 10-year average not found", FPE_SOURCE),
    (None, "45.8 out of 100 (91.7 checked)", "45.8 out of 100"),
    # Fix 2: RMD.
    (None, "Beta 1.0: $187.03 (0.81). Measured 0.77: $221.39 (0.96). Adjusted 0.84: $208.64 (0.91)",
     "Beta 1.0: $185.77 (0.81). Measured 0.77: $219.58 (0.95). Adjusted 0.84: $207.05 (0.90)"),
    (None, "3.0 points a year above my base path", "3.1 points a year above my base path"),
    (None, "$132.33 (0.58 x price)", "$131.48 (0.57 x price)"),
    (None, "rf 3.97%", RF),
    # Fix 2: ALC.
    (None, "Beta 1.0: $57.16 (0.80). Measured 0.87: $63.19 (0.88). Adjusted 0.91: $61.07 (0.85)",
     "Beta 1.0: $56.69 (0.79). Measured 0.87: $62.61 (0.88). Adjusted 0.91: $60.53 (0.85)"),
    (None, "2.7 points a year above my base path: about 8.7% a year early on",
     "2.8 points a year above my base path: about 8.8% a year early on"),
    (None, "$44.29 (0.62 x price)", "$43.91 (0.61 x price)"),
    (None, "Base case is 20% below the price", "Base case is 21% below the price"),
    (None, "Even with 3 points more margin the value is $67", "Even with 3 points more margin the value is $66"),
    (None, "The price assumes about 8.7% growth", "The price assumes about 8.8% growth"),
    # Fix 5: ALC competition.
    (None, "Bausch + Lomb (named from general knowledge; to verify)",
     "Bausch + Lomb (confirmed as the main rivals by a 2026 market overview and Zacks)"),
    (None, "scale in surgical eye care (to verify)",
     "scale in surgical eye care (Zacks: over 60% of the global market for presbyopia-correcting "
     "lens implants; undated, older estimate)"),
    # Fix 2: EW.
    (None, "Beta 1.0: $46.90 (0.51). Measured 0.84: $51.55 (0.56). Adjusted 0.90: $49.89 (0.54)",
     "Beta 1.0: $46.62 (0.51). Measured 0.84: $51.21 (0.56). Adjusted 0.90: $49.58 (0.54)"),
    (None, "10.5 points a year above my base path: about 21% in 2026",
     "10.6 points a year above my base path: about 22% in 2026"),
    (None, "$36.29 (0.39 x price)", "$36.10 (0.39 x price)"),
    # Fix 5: EW competition.
    (None, "Medtronic and Abbott in TAVR (named from general knowledge; to verify)",
     "Medtronic (about 28% of TAVR) and Abbott (about 3%) (GlobalData)"),
    (None, "TAVR leader and early", "TAVR leader with about 55% to 66% of the market (GMI; GlobalData) and early"),
]


def text_runs(p):
    """(run, text) for every run in the paragraph, hyperlinks included, in order."""
    return [(r, "".join(t.text or "" for t in r.findall(qn("w:t")))) for r in p.iter(qn("w:r"))]


def ptext(p):
    return "".join(t for _, t in text_runs(p))


def cut(p, offset):
    """Make sure a run boundary falls at character `offset`."""
    pos = 0
    for r, t in text_runs(p):
        if pos < offset < pos + len(t):
            k = offset - pos
            w = r.find(qn("w:t"))
            r2 = deepcopy(r)
            w2 = r2.find(qn("w:t"))
            w.text, w2.text = t[:k], t[k:]
            for x in (w, w2):
                x.set(XML_SPACE, "preserve")
            r.addnext(r2)
            return
        pos += len(t)


def mark(tag):
    NEXT_ID[0] += 1
    el = docx.oxml.OxmlElement(tag)
    el.set(qn("w:id"), str(NEXT_ID[0]))
    el.set(qn("w:author"), AUTHOR)
    el.set(qn("w:date"), DATE)
    return el


def top(p, el):
    while el.getparent() is not p:
        el = el.getparent()
    return el


def track(p, old, new):
    full = ptext(p)
    s = full.index(old)
    e = s + len(old)
    cut(p, e)
    cut(p, s)
    pos, hit = 0, []
    for r, t in text_runs(p):
        if s <= pos < e and t:
            hit.append(r)
        pos += len(t)
    for r in hit:
        d = mark("w:del")
        r.addprevious(d)
        d.append(r)
        for w in r.findall(qn("w:t")):
            w.tag = qn("w:delText")
    ins = mark("w:ins")
    run = docx.oxml.OxmlElement("w:r")
    rpr = hit[0].find(qn("w:rPr"))
    if rpr is not None:
        run.append(deepcopy(rpr))
    w = docx.oxml.OxmlElement("w:t")
    w.text = new
    w.set(XML_SPACE, "preserve")
    run.append(w)
    ins.append(run)
    top(p, hit[-1].getparent()).addnext(ins)


def apply(src, dst, edits):
    d = docx.Document(src)
    body = d.element.body
    # Kenon's section (heading to the next heading, tables included) is off limits.
    kenon, inside = set(), False
    for el in body:
        if el.tag == qn("w:p"):
            style = el.find(qn("w:pPr") + "/" + qn("w:pStyle"))
            heading = style is not None and style.get(qn("w:val")).lower().replace(" ", "") in (
                "heading1", "heading2")
            if heading:
                inside = "KEN (Kenon" in ptext(el)
        if inside:
            kenon.update(el.iter(qn("w:p")))
    for ctx, old, new in edits:
        paras = [p for p in body.iter(qn("w:p")) if old in ptext(p)]
        if ctx:  # the paragraph must sit in a table row that also contains ctx
            rows = {p: next(p.iterancestors(qn("w:tr")), None) for p in paras}
            paras = [p for p in paras if rows[p] is not None and ctx in
                     "".join(t.text or "" for t in rows[p].iter(qn("w:t")))]
        if len(paras) > 1:  # e.g. "MISSING" in a row: take the cell that is exactly `old`
            paras = [p for p in paras if ptext(p) == old]
        assert len(paras) == 1 and ptext(paras[0]).count(old) == 1, (old, len(paras))
        assert paras[0] not in kenon, ("Kenon section", old)
        track(paras[0], old, new)
    print(f"  Kenon section: {len(kenon)} paragraphs left untouched")
    d.save(dst)


def views(path):
    """(original, accepted) text of every paragraph, to verify the edits."""
    d = docx.Document(path)
    orig, acc = [], []
    for p in d.element.body.iter(qn("w:p")):
        o = a = ""
        for el in p.iter(qn("w:t"), qn("w:delText")):
            in_ins = any(x.tag == qn("w:ins") for x in el.iterancestors())
            if el.tag == qn("w:delText"):
                o += el.text or ""
            else:
                a += el.text or ""
                if not in_ins:
                    o += el.text or ""
        orig.append(o)
        acc.append(a)
    return orig, acc


if __name__ == "__main__":
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name, edits in (("Aryu - Power producers and utilities", POWER),
                        ("Aryu - Medical technology and lab tools", MEDTECH)):
        a, b = src / f"{name}.docx", out / f"{name} (fact-checked).docx"
        apply(a, b, edits)
        o0, _ = views(a)
        o1, acc = views(b)
        assert o0 == o1, "rejecting all changes must give the original back"
        changed = sum(x != y for x, y in zip(o1, acc))
        print(f"{b.name}: {len(edits)} edits, {changed} paragraphs changed, original recoverable")
