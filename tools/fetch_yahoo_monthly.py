"""Fetch Yahoo Finance monthly history (range max) in the Yahoo CSV download format, plus one day's close.

    python tools/fetch_yahoo_monthly.py <folder> TEL FOXA ...   # writes <folder>/<TICKER>.csv
    python tools/fetch_yahoo_monthly.py --close 2026-10-30 INTU QCOM ...   # prints the unadjusted close

Monthly bars are stamped at noon local time so a daylight-saving shift cannot move a month
(the bug fixed in tools/refined_screen.py, 17 Nov). Needs query1.finance.yahoo.com on the network.
"""
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from refined_screen import get  # noqa: E402

BASE = "https://query1.finance.yahoo.com/v8/finance/chart/"


def stamp(t, off):
    return datetime.fromtimestamp(t + off + 43200, tz=timezone.utc).date()


def monthly_csv(sym, folder):
    # range=max returns 3-month bars for long histories (Comcast, 19 Nov), so ask for explicit dates
    now = int(datetime.now(timezone.utc).timestamp())
    d = json.loads(get(f"{BASE}{sym}?period1=-1500000000&period2={now}&interval=1mo&events=div,split"))["chart"]["result"][0]
    q, adj, off = d["indicators"]["quote"][0], d["indicators"]["adjclose"][0]["adjclose"], d["meta"].get("gmtoffset", 0)
    lines = ["Date,Open,High,Low,Close,Adj Close,Volume"]
    for i, t in enumerate(d["timestamp"]):
        day = stamp(t, off)
        if adj[i] is None or day.day != 1:  # skip the live bar stamped with today's date
            continue
        lines.append(f"{day},{q['open'][i]},{q['high'][i]},{q['low'][i]},{q['close'][i]},{adj[i]},{q['volume'][i]}")
    months = [l[:7] for l in lines[1:]]
    gaps = sum(1 for a, b in zip(months, months[1:]) if (int(b[:4]) * 12 + int(b[5:7])) - (int(a[:4]) * 12 + int(a[5:7])) != 1)
    if gaps:
        raise ValueError(f"{sym}: {gaps} gaps between monthly bars; not written")
    (Path(folder) / f"{sym}.csv").write_text("\n".join(lines) + "\n")
    return lines[1].split(",")[0], lines[-1].split(",")[0]


def close_on(sym, day):
    a = int(datetime.combine(day - timedelta(days=4), datetime.min.time(), timezone.utc).timestamp())
    b = int(datetime.combine(day + timedelta(days=2), datetime.min.time(), timezone.utc).timestamp())
    d = json.loads(get(f"{BASE}{sym}?period1={a}&period2={b}&interval=1d"))["chart"]["result"][0]
    off = d["meta"].get("gmtoffset", 0)
    for t, c in zip(d["timestamp"], d["indicators"]["quote"][0]["close"]):
        if stamp(t, off) == day and c is not None:
            return round(c, 4)
    return None


if __name__ == "__main__":
    if sys.argv[1] == "--close":
        day = date.fromisoformat(sys.argv[2])
        for s in sys.argv[3:]:
            print(f"{s},{close_on(s, day)}")
    else:
        Path(sys.argv[1]).mkdir(parents=True, exist_ok=True)
        for s in sys.argv[2:]:
            print(s, *monthly_csv(s, sys.argv[1]))
