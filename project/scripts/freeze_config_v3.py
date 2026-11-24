#!/usr/bin/env python3
"""plan_v3 freeze (after E0, E0b, E0c on dev only). For every baseline family pick the config with the highest mean
dev G-mean (mean over seeds, then over dev projects that ALL families completed). The proposed config is fixed in
plan_v2 (law_lagakos_model_cal) and is not selected. Writes state/frozen_config_v3.json; refuses to overwrite."""
import sys, os, json, re, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import STATE, ROOT, write_json, now_iso, log_decision, log_variant
OUT = STATE / "frozen_config_v3.json"
if OUT.exists() and "--force" not in sys.argv:
    print(open(OUT).read()); sys.exit("already frozen (never refreeze after test runs)")
df = pd.read_json(ROOT / "results" / "raw_results.jsonl", lines=True)
dev = df[df.experiment.isin(["E0", "E0b", "E0c"]) & (df.split == "dev")]
tab = dev.groupby(["variant", "project"]).gmean.mean().unstack()
nseed = dev.groupby(["variant", "project"]).seed.nunique().unstack()
complete = [p for p in tab.columns if tab[p].notna().all() and (nseed[p] == 3).all()]
if len(complete) < len(tab.columns) and "--allow-partial" not in sys.argv:
    sys.exit(f"dev grid incomplete; complete projects = {complete}. Wait, or pass --allow-partial (logged).")
tab["mean_dev"] = tab[complete].mean(axis=1); tab = tab.sort_values("mean_dev", ascending=False)
fam = {"wait": r"^wait_W\d+$", "orb": r"^orb_W\d+$", "fsc": r"^fsc_W\d+$", "fr": r"^wait_W\d+_fr\d+$",
       "wait_cal": r"^wait_W\d+_cal$", "orb_cal": r"^orb_W\d+_cal$", "fsc_cal": r"^fsc_W\d+_cal$"}
sel = {}
for f, rx in fam.items():
    sub = tab[[bool(re.match(rx, v)) for v in tab.index]]
    if len(sub): sel[f] = sub.mean_dev.idxmax()
PROPOSED = "law_lagakos_model_cal"
fz = {"frozen": now_iso(), "plan": "plan_v3", "dev_projects_used": complete, "selected": sel, "proposed": PROPOSED,
      "proposed_dev_mean": round(float(tab.loc[PROPOSED, "mean_dev"]), 4),
      "dev_means": {k: round(float(v), 4) for k, v in tab.mean_dev.items()}, "n_dev_runs": int(len(dev))}
write_json(OUT, fz)
tab.round(4).to_csv(ROOT / "tables" / "dev_tuning_v3.csv")
for v, r in tab.iterrows():
    log_variant(cycle=1, variant_id=v, description="dev tuning (plan_v3: E0/E0b/E0c)", data_split_used=f"dev {complete} x seeds 0-2",
                metric="gmean_mean_dev", value=round(float(r.mean_dev), 4),
                outcome="selected" if v in sel.values() else ("proposed (pre-specified)" if v == PROPOSED else "not selected"))
log_decision(f"Frozen (plan_v3): {sel}; proposed={PROPOSED}", "Highest mean dev G-mean per family on dev projects only")
print(tab.round(4).to_string()); print(json.dumps(fz["selected"], indent=1))
