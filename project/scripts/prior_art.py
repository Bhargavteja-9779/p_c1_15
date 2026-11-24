#!/usr/bin/env python3
"""Run prior-art queries against OpenAlex (title+abstract search), log every query and every hit
(with reconstructed abstract) into literature/prior_art_hits.json and the query list into
state/novelty_ledger.json. Usage: python scripts/prior_art.py "<claim id>" "query 1" "query 2" ..."""
import json, sys, time, urllib.request, urllib.parse, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import ROOT, STATE, read_json, write_json, now_iso

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "research-loop/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)

def abstract(inv):
    if not inv: return ""
    pos = sorted((p, w) for w, ps in inv.items() for p in ps); return " ".join(w for _, w in pos)

claim, queries = sys.argv[1], sys.argv[2:]
hits_p = ROOT / "literature" / "prior_art_hits.json"; hits = read_json(hits_p, {})
led = read_json(STATE / "novelty_ledger.json", {"queries": [], "papers_opened": [], "claims": [], "scores": []})
for q in queries:
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"search": q, "per-page": 15,
          "select": "id,doi,title,publication_year,primary_location,abstract_inverted_index,cited_by_count"})
    d = get(url); ids = []
    for w in d["results"]:
        k = w["id"].split("/")[-1]; ids.append(k)
        if k not in hits:
            src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
            hits[k] = {"title": w["title"], "year": w["publication_year"], "doi": w.get("doi"), "venue": src,
                       "cited_by": w.get("cited_by_count"), "abstract": abstract(w.get("abstract_inverted_index"))}
    led["queries"].append({"claim": claim, "query": q, "source": "OpenAlex search (title/abstract/fulltext)",
                           "n_results_total": d["meta"]["count"], "top15": ids, "time": now_iso()})
    print(f"[{d['meta']['count']:6d}] {q}")
    for k in ids[:8]: print(f"     {hits[k]['year']} {str(hits[k]['title'])[:100]}")
    time.sleep(0.5)
write_json(hits_p, hits); write_json(STATE / "novelty_ledger.json", led)
