#!/usr/bin/env python3
"""Cycle-1 diagnostic (DEV projects only): why does LAW lose recall-1 on dev?
Logs q calibration (mean q of truly-buggy vs truly-clean provisional negatives) and recall-1 by time quartile.
Writes results/diag_law_<project>.json. Idempotent (skips if output exists unless --force)."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.data import load_project
from src.jit import simulate
proj = sys.argv[1] if len(sys.argv) > 1 else "neutron"
assert proj in ("fabric", "neutron", "nova", "sentry"), "diagnostics only on dev projects"
out = f"results/diag_law_{proj}.json"
if os.path.exists(out) and "--force" not in sys.argv: print(open(out).read()); sys.exit()
df = load_project(proj)
cfgs = {"law_lagakos_model": dict(method="law", prior="model"), "law_lagakos_base": dict(method="law", prior="base"),
        "wait_W90": dict(method="wait", W=90), "wait_W30": dict(method="wait", W=30), "oracle": dict(method="oracle")}
res = {}
for k, c in cfgs.items():
    o = simulate(df, seed=0, return_preds=True, label_noise_log=True, **c)
    y = df.reset_index(drop=True).y.to_numpy(); ev = o["eval_mask"]; idx = np.where(ev)[0]
    qs = np.array_split(idx, 4)
    r1q = [float(np.mean(o["pred"][q][y[q] == 1] == 1)) for q in qs]
    r0q = [float(np.mean(o["pred"][q][y[q] == 0] == 0)) for q in qs]
    pos_rate_pred = [float(np.mean(o["pred"][q] == 1)) for q in qs]
    true_rate = [float(np.mean(y[q])) for q in qs]
    d = o.get("diag", [])
    entry = dict(metrics=o["metrics"], r1_by_quartile=r1q, r0_by_quartile=r0q, pred_pos_rate_by_quartile=pos_rate_pred,
                 true_pos_rate_by_quartile=true_rate)
    if d and "mean_q_true_bug" in d[0]:
        entry["mean_q_true_bug"] = float(np.nanmean([x["mean_q_true_bug"] for x in d]))
        entry["mean_q_clean"] = float(np.nanmean([x["mean_q_clean"] for x in d]))
    if d and "frac_false_clean" in d[0]:
        entry["frac_false_clean"] = float(np.nanmean([x["frac_false_clean"] for x in d]))
    res[k] = entry; print(k, json.dumps(entry))
json.dump(res, open(out, "w"), indent=1)
