#!/usr/bin/env python3
"""After E0: choose W* for 'wait' and 'orb' (best mean dev G-mean over dev projects x explore seeds),
determine the best non-oracle baseline on dev, and freeze state/frozen_config.json. Refuses to overwrite."""
import sys, os, json, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import STATE, ROOT, write_json, read_json, now_iso, log_decision, log_variant
if (STATE / "frozen_config.json").exists() and "--force" not in sys.argv:
    print(open(STATE / "frozen_config.json").read()); sys.exit("already frozen (never refreeze after test runs)")
df = pd.read_json(ROOT / "results" / "raw_results.jsonl", lines=True)
e0 = df[df.experiment == "E0"]
tab = e0.groupby(["variant", "project"]).gmean.mean().unstack()
tab["mean_dev"] = tab.mean(axis=1); tab = tab.sort_values("mean_dev", ascending=False)
print(tab.round(4).to_string())
best = lambda pre: tab[tab.index.str.startswith(pre)].mean_dev.idxmax()
wv, ov, dv = best("wait_W"), best("orb_W"), best("odasc_W")
lv = tab[tab.index.str.startswith("law_")].mean_dev.idxmax()    # plan_v2: LAW = best of its 4 dev variants
base = {"nowait": tab.loc["nowait", "mean_dev"], wv: tab.loc[wv, "mean_dev"], ov: tab.loc[ov, "mean_dev"], dv: tab.loc[dv, "mean_dev"]}
fz = {"frozen": now_iso(), "plan": "plan_v2", "wait_W": int(wv.split("W")[1]), "orb_W": int(ov.split("W")[1]),
      "odasc_W": int(dv.split("W")[1]), "odasc_delta": 0.9,
      "law_delay_est": lv.split("_")[1], "law_prior": lv.split("_")[2], "law_variant": lv,
      "best_baseline_on_dev": max(base, key=base.get), "dev_means": {k: round(float(v), 4) for k, v in tab.mean_dev.items()},
      "proposed": f"{lv} (best of 4 LAW variants on dev, plan_v2)", "n_e0_runs": int(len(e0))}
write_json(STATE / "frozen_config.json", fz)
tab.round(4).to_csv(ROOT / "tables" / "E0_dev_tuning.csv")
for v, r in tab.iterrows():
    log_variant(cycle=1, variant_id=v, description="E0 dev tuning", data_split_used="dev projects x seeds 0-2",
                metric="gmean_mean_dev", value=round(float(r.mean_dev), 4), outcome="selected" if v in (wv, ov, dv, lv) else "not selected")
log_decision(f"Frozen config: wait W*={fz['wait_W']}, orb W*={fz['orb_W']}, odasc W*={fz['odasc_W']}, LAW={lv}, best dev baseline={fz['best_baseline_on_dev']}", "Highest mean dev G-mean (E0+E0b, dev projects only), plan_v2 selection rule")
print(json.dumps(fz, indent=1))
