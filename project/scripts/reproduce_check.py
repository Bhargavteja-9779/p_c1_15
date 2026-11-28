#!/usr/bin/env python3
"""G9 reproducibility check: re-run a stratified sample of finished jobs (one per experiment x variant, on the
smallest project available for it, first seed) and compare every metric with the stored result.
Usage: python scripts/reproduce_check.py [--max N]   Writes results/reproduce_check.json. Exit 1 on any mismatch."""
import sys, os, json, argparse, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import ROOT, now_iso
from src.data import load_any
from src.jit import simulate
ap = argparse.ArgumentParser(); ap.add_argument("--max", type=int, default=40); a = ap.parse_args()
df = pd.read_json(ROOT / "results" / "raw_results.jsonl", lines=True).drop_duplicates("job_id", keep="last")
SMALL = ["aj_kafka", "npm", "wagtail", "fabric", "spring-integration"]
q = {j["id"]: j for j in json.load(open(ROOT / "state" / "queue.json"))["jobs"]}
picked = []
for (exp, var), g in df.groupby(["experiment", "variant"]):
    g = g[g.job_id.isin(q)]
    if g.empty: continue
    g = g.assign(rank=g.project.map(lambda p: SMALL.index(p) if p in SMALL else 99)).sort_values(["rank", "seed"])
    picked.append(g.iloc[0])
picked = picked[: a.max]
KW = ["W", "delay_est", "prior", "delay_scale", "label_noise_log", "odasc_delta", "thr_policy", "oracle_H", "insp_policy", "insp_budget"]
rows, bad = [], 0
for r in picked:
    p = q[r.job_id]["params"]; kw = {k: p[k] for k in KW if k in p}
    m = simulate(load_any(p["project"]), p["method"], seed=p["seed"], **kw)["metrics"]
    ok = all(abs(m[k] - r[k]) < 1e-9 for k in ["gmean", "auc", "r0", "r1"])
    bad += not ok
    rows.append({"job_id": r.job_id, "stored_gmean": r.gmean, "rerun_gmean": m["gmean"], "stored_auc": r.auc, "rerun_auc": m["auc"], "match": ok})
    print(("OK  " if ok else "DIFF"), r.job_id, round(r.gmean, 6), round(m["gmean"], 6), flush=True)
json.dump({"generated": now_iso(), "n_checked": len(rows), "n_mismatch": bad, "rows": rows},
          open(ROOT / "results" / "reproduce_check.json", "w"), indent=1)
print(f"checked {len(rows)}, mismatches {bad}"); sys.exit(1 if bad else 0)
