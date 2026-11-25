#!/usr/bin/env python3
"""plan_v6 freeze (cycle 2): best dual config from E0e (dev only) + the plan_v5 frozen lawm/odasc.
Writes state/frozen_config_v6.json with job specs of the confirmation candidates (used by E7 and the plan_v7
ApacheJIT confirmation E8). The 'primary' candidate is the one with the best mean dev G-mean. Refuses to overwrite."""
import sys, os, json, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import STATE, ROOT, read_json, write_json, now_iso, log_decision, log_variant
out = STATE / "frozen_config_v6.json"
if out.exists() and "--force" not in sys.argv: sys.exit(open(out).read() + "\nalready frozen")
v5 = read_json(STATE / "frozen_config_v5.json"); assert v5, "plan_v5 freeze missing"
df = pd.read_json(ROOT / "results" / "raw_results.jsonl", lines=True)
d = df[df.experiment.isin(["E0c", "E0d", "E0e"])].drop_duplicates("job_id", keep="last")
e = d[d.experiment == "E0e"]; assert len(e) == 48, f"E0e incomplete: {len(e)}/48"
tab = d.groupby(["variant", "project"]).gmean.mean().unstack(); tab["mean_dev"] = tab.mean(axis=1)
dual = tab[tab.index.str.startswith("dual_")].mean_dev.idxmax()
_, w, k = dual.split("_"); W, K = int(w[1:]), int(k[1:])
_, lmode, lw = v5["lawm"].split("_"); _, ow, ot = v5["odasc"].split("_")
specs = [dict(method="lawm", mode="dual", W=W, knn_k=K, delay_est="lagakos", variant=dual),
         dict(method="lawm", mode=lmode, W=int(lw[1:]), delay_est="lagakos", variant=v5["lawm"]),
         dict(method="odasc", W=int(ow[1:]), theta=float(ot[1:]), knn_k=20, variant=v5["odasc"])]
dev = {s["variant"]: round(float(tab.loc[s["variant"], "mean_dev"]), 4) for s in specs}
primary = max(dev, key=dev.get)
fz = {"frozen": now_iso(), "plan": "plan_v6/plan_v7", "dual": dual, "dev_means": dev, "primary_candidate": primary,
      "H5_dual_beats_lawm_and_odasc_on_dev": bool(dev[dual] > dev[v5["lawm"]] and dev[dual] > dev[v5["odasc"]]),
      "candidates_specs": specs}
write_json(out, fz); tab.round(4).to_csv(ROOT / "tables" / "E0e_dev_tuning.csv")
for v, r in tab[tab.index.str.startswith("dual_")].iterrows():
    log_variant(cycle=2, variant_id=v, description="E0e dev tuning (dual-evidence denoiser)", data_split_used="dev projects x seeds 0-2",
                metric="gmean_mean_dev", value=round(float(r.mean_dev), 4), outcome="selected" if v == dual else "not selected")
log_decision(f"plan_v6 freeze: dual={dual} ({dev[dual]}); lawm={v5['lawm']} ({dev[v5['lawm']]}), odasc={v5['odasc']} ({dev[v5['odasc']]}); primary (best dev) = {primary}; H5 on dev: {fz['H5_dual_beats_lawm_and_odasc_on_dev']}",
             "best mean dev G-mean, dev projects only (plan_v6/plan_v7)")
print(json.dumps(fz, indent=1))
