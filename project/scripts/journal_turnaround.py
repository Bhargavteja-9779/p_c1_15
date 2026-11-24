#!/usr/bin/env python3
"""Phase 1 evidence: compute (Accepted - Received) days from publisher-deposited Crossref
'assertion' metadata for a random sample of articles published in the last 24 months.
Writes journal_selection/turnaround/<issn>.json and turnaround_summary.csv.
Data source: https://api.crossref.org/journals/<ISSN>/works?sample=100&filter=...
Idempotent: skips ISSNs already fetched unless --refresh."""
import json, sys, os, time, statistics, urllib.request, urllib.parse, datetime, argparse, csv
from pathlib import Path
from dateutil import parser as dp  # python-dateutil ships with pandas

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "journal_selection" / "turnaround"; OUT.mkdir(parents=True, exist_ok=True)
FROM, UNTIL = "2024-11-24", "2026-11-24"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "research-loop-journal-check/0.1"})
    for k in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
        except Exception as e:
            time.sleep(3 * (k + 1)); err = e
    raise err

def parse(v):
    try: return dp.parse(v).date()
    except Exception: return None

def fetch(issn, n_rounds=3):
    items = {}
    for _ in range(n_rounds):
        f = f"from-pub-date:{FROM},until-pub-date:{UNTIL},type:journal-article"
        url = f"https://api.crossref.org/journals/{issn}/works?sample=100&filter={f}&select=DOI,title,assertion,container-title,publisher,published"
        d = get(url)
        for it in d["message"]["items"]: items[it["DOI"]] = it
        time.sleep(1)
    rows = []
    for doi, it in items.items():
        a = {x.get("name"): x.get("value") for x in it.get("assertion", []) if x.get("name")}
        r, acc = parse(a.get("received") or ""), parse(a.get("accepted") or "")
        if r and acc and acc >= r:
            rows.append({"doi": doi, "title": (it.get("title") or [""])[0][:150], "received": str(r),
                         "revised": a.get("revised"), "accepted": str(acc), "days": (acc - r).days})
    meta = {"issn": issn, "container": (next(iter(items.values()), {}).get("container-title") or [""])[0] if items else "",
            "publisher": next(iter(items.values()), {}).get("publisher", "") if items else "",
            "sampled": len(items), "with_dates": len(rows), "window": [FROM, UNTIL],
            "fetched": datetime.datetime.utcnow().isoformat(timespec="seconds"),
            "source": f"https://api.crossref.org/journals/{issn}/works (sample=100 x {n_rounds}, assertion received/accepted)"}
    if rows:
        d = sorted(x["days"] for x in rows)
        meta.update(median_days=statistics.median(d), min_days=d[0], max_days=d[-1],
                    q25=d[len(d)//4], q75=d[(3*len(d))//4], frac_le_72=round(sum(x <= 72 for x in d)/len(d), 3))
    return {"meta": meta, "articles": rows}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("issns", nargs="+"); ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    for issn in a.issns:
        p = OUT / f"{issn}.json"
        if p.exists() and not a.refresh:
            res = json.load(open(p))
        else:
            res = fetch(issn); json.dump(res, open(p, "w"), indent=1)
        m = res["meta"]
        print(f"{issn} {m['container'][:45]:45s} n={m['with_dates']:3d}/{m['sampled']:3d} median={m.get('median_days')} range=[{m.get('min_days')},{m.get('max_days')}] le72={m.get('frac_le_72')}", flush=True)
    # summary
    rows = []
    for p in sorted(OUT.glob("*.json")):
        m = json.load(open(p))["meta"]; rows.append({k: m.get(k) for k in ["issn", "container", "publisher", "sampled", "with_dates", "median_days", "q25", "q75", "min_days", "max_days", "frac_le_72", "fetched"]})
    with open(ROOT / "journal_selection" / "turnaround_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
