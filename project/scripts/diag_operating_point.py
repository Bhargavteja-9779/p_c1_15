#!/usr/bin/env python3
"""DEV-ONLY diagnostic (Section 6.4 rung 1): does a method lose on ranking (AUC) or on its operating point
(threshold 0.5)? For each method: AUC, G-mean@0.5, best-threshold G-mean (diagnostic upper bound, chosen on
the same data, NEVER used for model selection), predicted-positive rate vs true defect rate, and the
effective class-balance weights. Writes results/diag/operating_point_dev.csv. Idempotent (skips done rows)."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.data import load_project
from src.jit import simulate
from sklearn.metrics import roc_curve, roc_auc_score
OUT = "results/diag/operating_point_dev.csv"
CFG = [("nowait", {}), ("oracle", {}), ("wait_W90", dict(method="wait", W=90)), ("orb_W90", dict(method="orb", W=90)),
       ("law_lagakos_base", dict(method="law", delay_est="lagakos", prior="base")),
       ("law_lagakos_model", dict(method="law", delay_est="lagakos", prior="model"))]
projects = sys.argv[1].split(",") if len(sys.argv) > 1 else ["fabric", "neutron"]
os.makedirs("results/diag", exist_ok=True)
done = pd.read_csv(OUT) if os.path.exists(OUT) else pd.DataFrame(columns=["project", "variant"])
rows = done.to_dict("records")
for p in projects:
    df = load_project(p)
    for v, kw in CFG:
        if ((done.project == p) & (done.variant == v)).any(): continue
        kw = dict(kw); m = kw.pop("method", v)
        o = simulate(df, m, seed=0, return_preds=True, **kw)
        ev = o["eval_mask"]; y = df.y.to_numpy()[ev]; pr = o["prob"][ev]
        fpr, tpr, th = roc_curve(y, pr); g = np.sqrt(tpr * (1 - fpr)); k = int(np.argmax(g))
        rows.append(dict(project=p, variant=v, auc=roc_auc_score(y, pr), gmean_at_05=o["metrics"]["gmean"],
                         gmean_best_thr=float(g[k]), best_thr=float(th[k]), pred_pos_rate=float((pr >= .5).mean()),
                         true_pos_rate=float(y.mean()), mean_p_bug=float(pr[y == 1].mean()), mean_p_clean=float(pr[y == 0].mean())))
        pd.DataFrame(rows).to_csv(OUT, index=False); print(rows[-1], flush=True)
