#!/usr/bin/env python3
"""D2 (dev only): are discovery delays predictable from commit features? For discovered defects in each dev
project, train LightGBM on the earliest 70% (by commit time) to predict log(1+delay), evaluate Spearman rho on
the latest 30%. Commits in the last 2 years excluded (their long delays are censored). Writes results/diag/d2_delay_predictability.json"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.data import load_project
from src.jit import FEATS, DAY
import lightgbm as lgb
from scipy.stats import spearmanr
out = {}
for p in ["fabric", "neutron", "nova", "sentry"]:
    d = load_project(p)
    b = d[(d.y == 1) & np.isfinite(d.t_found) & (d.t < d.t.max() - 730 * DAY)].sort_values("t")
    X = np.log1p(np.clip(b[FEATS].to_numpy(float), 0, None)); yv = np.log1p((b.t_found - b.t).to_numpy() / DAY)
    k = int(0.7 * len(b))
    m = lgb.LGBMRegressor(n_estimators=200, learning_rate=0.05, num_leaves=15, min_child_samples=30, verbose=-1, random_state=0).fit(X[:k], yv[:k])
    rho = spearmanr(m.predict(X[k:]), yv[k:]).correlation
    rho_time = spearmanr(b.t.values[k:], yv[k:]).correlation
    out[p] = {"n_defects": int(len(b)), "spearman_features": round(float(rho), 4), "spearman_committime_within_test": round(float(rho_time), 4)}
    print(p, out[p])
os.makedirs("results/diag", exist_ok=True); json.dump(out, open("results/diag/d2_delay_predictability.json", "w"), indent=1)
