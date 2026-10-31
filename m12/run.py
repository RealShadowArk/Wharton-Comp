"""Score the peer data and write the M12 preview outputs.

Usage: python -m m12.run   (reads inputs/m12/, writes outputs/M12_*_preview.csv)
       python -m m12.run my_peers.csv   (any file with the template's columns;
       writes outputs/M12_scores_my_peers.csv and M12_stability_my_peers.csv)

Everything here is a PREVIEW: rules R1-R8 and the cross-check await Pat's
sign-off. The TFS is a research filter, never a buy signal or a weight.
"""

import csv
import sys
from pathlib import Path

from m12.score import (CROSS_MEASURES, CROSS_WEIGHTS, MEASURES, RULES, load,
                       score_all, stability)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "inputs" / "m12" / "M12_peer_data_v02.csv"
WATCH = ROOT / "inputs" / "m12" / "M12_watchlist_v02.csv"
OUT = ROOT / "outputs"
IDS = [m for m, _, _ in MEASURES] + ["ROE", "PS", "PB"]


def run(data=DATA, watch=WATCH, tag="preview"):
    rows = load(data)
    tfs = score_all(rows)
    cross = score_all(rows, weights=CROSS_WEIGHTS, measure_list=CROSS_MEASURES)
    out_rows, stab_rows = [], []
    for group, res in tfs.items():
        stab = stability(res) if res["released"] else {}
        xres = cross[group]
        for t, raw in res["raw"].items():
            total, xtotal = res["totals"][t], xres["totals"][t]
            kept = stab.get(t)
            rec = {"peer_group": group, "ticker": t,
                   "status": "SCORED" if total is not None else "INCOMPLETE",
                   "group_released": res["released"],
                   "TFS": "" if total is None else round(total, 4),
                   "shortlisted": t in res["shortlist"],
                   "variants_on_shortlist": "" if kept is None else f"{kept[0]}/{kept[1]}",
                   "worst_rank_in_variants": "" if kept is None else kept[2],
                   "crosscheck": "" if xtotal is None else round(xtotal, 4),
                   "crosscheck_shortlisted": t in xres["shortlist"]}
            for m in IDS:
                value, code, note = raw[m]
                rec[f"{m}_raw"] = "" if value is None else round(value, 6)
                rec[f"{m}_code"] = code
                rec[f"{m}_basis"] = note
                rec[f"{m}_score"] = (round(res["scores"][t][m], 4)
                                     if m in res["scores"][t] else "")
            out_rows.append(rec)
            if kept:
                stab_rows.append({"peer_group": group, "ticker": t,
                                  "variants_on_shortlist": kept[0],
                                  "variants": kept[1],
                                  "worst_rank": kept[2]})
    for r in (load(watch) if watch else []):
        out_rows.append({"peer_group": r["peer_group"], "ticker": r["ticker"],
                         "status": "EXCLUDED (R2: incomparable history)"})
    fields = list(dict.fromkeys(k for r in out_rows for k in r))
    OUT.mkdir(exist_ok=True)
    write(OUT / f"M12_scores_{tag}.csv", out_rows, fields)
    write(OUT / f"M12_stability_{tag}.csv", stab_rows,
          ["peer_group", "ticker", "variants_on_shortlist", "variants",
           "worst_rank"])
    return tfs, cross


def write(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        tfs, cross = run(path, None, path.stem)
    else:
        tfs, cross = run()
    print("Rules:", RULES)
    for g, res in tfs.items():
        print(f"{g}: {len(res['complete'])}/{len(res['raw'])} complete, "
              f"released={res['released']}, shortlist={res['shortlist']}, "
              f"cross-check shortlist={cross[g]['shortlist']}")
