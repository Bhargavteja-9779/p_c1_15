#!/usr/bin/env python3
"""After E0: choose W* for 'wait' and 'orb' (best mean dev G-mean over dev projects x explore seeds),
determine the best non-oracle baseline on dev, and freeze state/frozen_config.json. Refuses to overwrite."""
import sys, os, json, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import STATE, ROOT, write_json, read_json, now_iso, log_decision, log_variant
if (STATE / "frozen_config.json").exists() and "--force" not in sys.argv:
    print(open(STATE / "frozen_config.json").read()); sys.exit("already frozen (never refreeze after test runs)")
df = pd.read_json(ROOT / "results" / "raw_results.jsonl", lines=True)
e0 = df[df.experiment.isin(["E0", "E0b"]) & ~df.method.isin(["decomp"])]   # decomp = true-label diagnostic, never a candidate
tab = e0.groupby(["variant", "project"]).gmean.mean().unstack()
tab["mean_dev"] = tab.mean(axis=1); tab = tab.sort_values("mean_dev", ascending=False)
print(tab.round(4).to_string())
best = lambda pre: tab[tab.index.str.startswith(pre)].mean_dev.idxmax()
wv, ov = best("wait_W"), best("orb_W")
base = {"nowait": tab.loc["nowait", "mean_dev"], wv: tab.loc[wv, "mean_dev"], ov: tab.loc[ov, "mean_dev"]}
# plan_v2 rule: candidate = best mean-dev among law_* and awt_* (dev only); carried as a method claim only if it beats best baseline on dev
cands = tab[tab.index.str.startswith("law_") | tab.index.str.startswith("awt_")]
cand = cands.mean_dev.idxmax(); best_base = max(base, key=base.get)
fz_extra = {"plan": "plan_v2", "candidate": cand, "candidate_dev_mean": round(float(cands.mean_dev.max()), 4),
            "best_baseline_dev_mean": round(float(base[best_base]), 4),
            "candidate_beats_baseline_on_dev": bool(cands.mean_dev.max() > base[best_base]),
            "n_candidates_tried_on_dev": int(len(cands))}
fz = {"frozen": now_iso(), **fz_extra, "wait_W": int(wv.split("W")[1]), "orb_W": int(ov.split("W")[1]),
      "best_baseline_on_dev": max(base, key=base.get), "dev_means": {k: round(float(v), 4) for k, v in tab.mean_dev.items()},
      "proposed_plan_v1": "law_lagakos_model (pre-specified in plan_v1; kept in E1 as pre-registered)", "n_e0_runs": int(len(e0))}
write_json(STATE / "frozen_config.json", fz)
tab.round(4).to_csv(ROOT / "tables" / "E0_dev_tuning.csv")
for v, r in tab.iterrows():
    log_variant(cycle=1, variant_id=v, description="E0 dev tuning", data_split_used="dev projects x seeds 0-2",
                metric="gmean_mean_dev", value=round(float(r.mean_dev), 4), outcome="selected" if v in (wv, ov, cand, "law_lagakos_model") else "not selected")
log_decision(f"Frozen config: wait W*={fz['wait_W']}, orb W*={fz['orb_W']}, best dev baseline={fz['best_baseline_on_dev']}", "Highest mean dev G-mean (E0, dev projects only); proposed method config pre-specified, not tuned")
print(json.dumps(fz, indent=1))
