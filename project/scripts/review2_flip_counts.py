#!/usr/bin/env python3
"""plan_v9 B2 (model-free): at every retraining time T of the prequential schedule (warm-up 500, every 100 commits, up to the
end of the scored window), count provisionally clean waited-out training commits that are truly defective ('flips') per age band.
Writes results/review1/flip_counts.json (per project: mean flips and mean provisionally clean commits per band, W=30 and W=90)."""
import os, sys, json, numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0, ROOT)
from src.data import load_project
TEST = ["brackets", "broadleaf", "camel", "jgroups", "matplotlib", "npm", "spring-integration", "tomcat", "wagtail", "zulip"]
AJ = ["aj_activemq", "aj_cassandra", "aj_flink", "aj_groovy", "aj_hadoop-hdfs", "aj_hbase", "aj_hive", "aj_ignite", "aj_kafka"]
DAY = 86400.0
BANDS = {30: [(30, 180), (180, 365), (365, 730), (730, np.inf)], 90: [(90, 180), (180, 365), (365, 730), (730, np.inf)]}
out = {}
for p in TEST + AJ:
    df = load_project(p); t = df["t"].to_numpy(float); y = df["y"].to_numpy(int); tf = df["t_found"].to_numpy(float)
    end = t.max() - 365 * DAY
    res = {W: {"flips": np.zeros(4), "prov_clean": np.zeros(4)} for W in BANDS}; nT = 0
    for start in range(500, len(df), 100):
        T = t[start]
        if T > end: break
        tr = t < T; age = (T - t[tr]) / DAY; prov = ~(tf[tr] <= T); yt = y[tr]; nT += 1
        for W, bands in BANDS.items():
            for i, (lo, hi) in enumerate(bands):
                b = prov & (age >= lo) & (age < hi)
                res[W]["flips"][i] += (b & (yt == 1)).sum(); res[W]["prov_clean"][i] += b.sum()
    out[p] = {str(W): {k: (v / max(nT, 1)).round(2).tolist() for k, v in r.items()} for W, r in res.items()}
    print(p, nT, out[p]["30"]["flips"], out[p]["90"]["flips"], flush=True)
json.dump(out, open(os.path.join(ROOT, "results", "review1", "flip_counts.json"), "w"), indent=1)
