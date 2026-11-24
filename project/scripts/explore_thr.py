#!/usr/bin/env python3
"""Exploratory dev-only check of decision-threshold policies (cycle 1, after the E0 operating-point diagnosis).
Writes results/exploratory/thr_dev.jsonl (append; skips configs already present). Dev projects only."""
import sys, os, json, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.data import load_project
from src.jit import simulate
DEV = ["fabric", "neutron", "nova", "sentry"]
out = os.path.join(os.path.dirname(__file__), "..", "results", "exploratory", "thr_dev.jsonl")
done = set()
if os.path.exists(out):
    for l in open(out): r = json.loads(l); done.add(r["cfg_id"])
projects = sys.argv[1].split(",") if len(sys.argv) > 1 else DEV
seeds = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [0]
cfgs = [dict(method="nowait", thr_policy="mature"), dict(method="nowait", thr_policy="latency"),
        dict(method="wait", W=90, thr_policy="mature"), dict(method="wait", W=90, thr_policy="latency"),
        dict(method="law", prior="base", thr_policy="latency")]
for p in projects:
    for s in seeds:
        df = load_project(p)
        for c in cfgs:
            cid = f"{p}_s{s}_" + "_".join(f"{k}{v}" for k, v in c.items())
            if cid in done: continue
            r = simulate(df, c["method"], seed=s, **{k: v for k, v in c.items() if k != "method"})["metrics"]
            r.update(cfg_id=cid, project=p, seed=s, **c)
            with open(out, "a") as f: f.write(json.dumps(r) + "\n")
            print(cid, round(r["gmean"], 3), round(r["auc"], 3), round(r["r0"], 3), round(r["r1"], 3), round(r.get("thr_mean", 0.5), 3), flush=True)
