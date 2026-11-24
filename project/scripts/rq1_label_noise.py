#!/usr/bin/env python3
"""RQ1 (failure-mode characterisation, model-free): how wrong are provisional 'clean' labels?
For each project and each update time T (every 100 commits after the 500th, excluding the last 365 days):
  - P(truly defect-inducing | not discovered yet, age in bin)
  - for waiting time W: share of training negatives that are false-clean, and share of commits younger than W (excluded).
Writes results/rq1_label_noise.json, tables/rq1_*.csv, figures/rq1_false_clean_by_age.png"""
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.data import load_project, PROJECTS
from src.state import ROOT
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
DAY = 86400.0
bins = [0, 7, 30, 90, 180, 365, 730, 100000]; labels = ["<7d", "7-30d", "30-90d", "90-180d", "180-365d", "1-2y", ">2y"]
WG = [0, 15, 30, 60, 90, 180, 365]
out, rows_age, rows_w = {}, [], []
for p in PROJECTS:
    d = load_project(p); t = d.t.values; y = d.y.values; tf = d.t_found.values
    acc = {l: [0, 0] for l in labels}; accw = {W: [0, 0, 0, 0] for W in WG}
    for s in range(500, len(d), 100):
        T = t[s]
        if T > t.max() - 365 * DAY: break
        tr = t < T; found = tf <= T; age = (T - t) / DAY
        unl = tr & ~found
        b = np.digitize(age[unl], bins) - 1
        for k, l in enumerate(labels):
            m = b == k; acc[l][0] += int(y[unl][m].sum()); acc[l][1] += int(m.sum())
        for W in WG:
            neg = unl & (age >= W)
            accw[W][0] += int(y[neg].sum()); accw[W][1] += int(neg.sum())
            accw[W][2] += int((tr & (age < W) & ~found).sum()); accw[W][3] += int(tr.sum())
    out[p] = {"false_clean_rate_by_age": {l: (a / n if n else None) for l, (a, n) in acc.items()},
              "by_W": {W: {"false_clean_share_of_negatives": a / max(n, 1), "share_of_history_excluded": e / max(tot, 1)} for W, (a, n, e, tot) in accw.items()}}
    rows_age.append({"project": p, **{l: round(a / n, 4) if n else np.nan for l, (a, n) in acc.items()}})
    rows_w.append({"project": p, **{f"W{W}_false_clean": round(a / max(n, 1), 4) for W, (a, n, e, tot) in accw.items()},
                   **{f"W{W}_excluded": round(e / max(tot, 1), 4) for W, (a, n, e, tot) in accw.items()}})
json.dump(out, open(ROOT / "results" / "rq1_label_noise.json", "w"), indent=1)
A = pd.DataFrame(rows_age).set_index("project"); A.to_csv(ROOT / "tables" / "rq1_false_clean_by_age.csv")
Wt = pd.DataFrame(rows_w).set_index("project"); Wt.to_csv(ROOT / "tables" / "rq1_waiting_time_tradeoff.csv")
print(A.round(3).to_string()); print(Wt[[c for c in Wt.columns if "false" in c]].round(3).to_string()); print(Wt[[c for c in Wt.columns if "excl" in c]].round(4).to_string())
fig, ax = plt.subplots(figsize=(7, 4))
for p, r in A.iterrows(): ax.plot(labels, r.values, marker="o", alpha=.6, label=p)
ax.set_ylabel("P(defect-inducing | not yet discovered)"); ax.set_xlabel("commit age at training time")
ax.legend(fontsize=6, ncol=2); fig.tight_layout(); fig.savefig(ROOT / "figures" / "rq1_false_clean_by_age.png", dpi=150)
