#!/usr/bin/env python3
"""DEV-only diagnostic (cycle 2): how much G-mean is lost to the 0.5 threshold? For each method, report
G-mean at 0.5 and the best fixed threshold chosen in hindsight (upper bound, NOT a method)."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.data import load_project
from src.jit import simulate
from sklearn.metrics import roc_auc_score
out = {}
for proj in sys.argv[1:] or ["fabric", "neutron", "sentry"]:
    assert proj in ("fabric", "neutron", "nova", "sentry")
    df = load_project(proj); y = df.reset_index(drop=True).y.to_numpy()
    for name, kw in {"wait_W90": dict(method="wait", W=90), "lawm_soft_W30": dict(method="lawm", W=30, mode="soft"),
                     "odasc_W30_t0.8": dict(method="odasc", W=30, theta=0.8), "law_lagakos_model": dict(method="law"),
                     "oracle": dict(method="oracle")}.items():
        o = simulate(df, seed=0, return_preds=True, **kw); ev = o["eval_mask"]; p = o["prob"][ev]; yy = y[ev]
        g = lambda th: float(np.sqrt(np.mean(p[yy == 1] >= th) * np.mean(p[yy == 0] < th)))
        ths = np.linspace(0.05, 0.95, 91); gs = [g(t) for t in ths]
        out[f"{proj}/{name}"] = dict(g05=round(g(0.5), 4), g_best=round(max(gs), 4), th_best=round(float(ths[int(np.argmax(gs))]), 2), auc=round(roc_auc_score(yy, p), 4))
        print(proj, name, out[f"{proj}/{name}"], flush=True)
json.dump(out, open("results/diag_threshold_dev.json", "w"), indent=1)
