#!/usr/bin/env python3
"""Frontiers deposits no received/accepted dates in Crossref, so read them from article pages
(frontiersin.org/articles/<DOI>/full) for a random Crossref sample. Writes journal_selection/turnaround/<issn>.json."""
import json, re, sys, time, random, statistics, urllib.request, datetime
from pathlib import Path
from dateutil import parser as dp
ROOT = Path(__file__).resolve().parent.parent; OUT = ROOT / "journal_selection" / "turnaround"
def get(u, js=True):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
    return json.loads(r) if js else r.decode("utf-8", "ignore")
for issn in sys.argv[1:]:
    items = get(f"https://api.crossref.org/journals/{issn}/works?sample=60&filter=from-pub-date:2024-11-24,until-pub-date:2026-11-24,type:journal-article&select=DOI,container-title,publisher")["message"]["items"]
    rows = []
    for it in items:
        try:
            h = get(f"https://www.frontiersin.org/articles/{it['DOI']}/full", js=False)
            f = dict(re.findall(r"(Received|Accepted)[^0-9]{0,40}(\d{1,2} \w+ \d{4})", h)[:2])
            r, a = dp.parse(f["Received"]).date(), dp.parse(f["Accepted"]).date()
            rows.append({"doi": it["DOI"], "received": str(r), "accepted": str(a), "days": (a - r).days})
        except Exception:
            pass
        time.sleep(0.5)
    d = sorted(x["days"] for x in rows)
    meta = {"issn": issn, "container": items[0]["container-title"][0], "publisher": items[0]["publisher"], "sampled": len(items),
            "with_dates": len(rows), "source": "Crossref sample + Received/Accepted printed on frontiersin.org article pages",
            "fetched": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}
    if d: meta.update(median_days=statistics.median(d), min_days=d[0], max_days=d[-1], q25=d[len(d)//4], q75=d[3*len(d)//4], frac_le_72=round(sum(x <= 72 for x in d)/len(d), 3))
    json.dump({"meta": meta, "articles": rows}, open(OUT / f"{issn}.json", "w"), indent=1)
    print(issn, meta["container"], "n", len(rows), "median", meta.get("median_days"), "range", meta.get("min_days"), meta.get("max_days"), "le72", meta.get("frac_le_72"))
