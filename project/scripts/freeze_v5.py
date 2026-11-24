#!/usr/bin/env python3
"""plan_v5 freeze (cycle 2): best-dev lawm and odasc configs from E0c/E0d (dev only). Writes
state/frozen_config_v5.json; refuses to overwrite (the cycle-1 freeze stays untouched)."""
import sys, os, json, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import STATE, ROOT, write_json, now_iso, log_decision, log_variant
out = STATE / "frozen_config_v5.json"
if out.exists() and "--force" not in sys.argv: sys.exit(open(out).read() + "\nalready frozen")
df = pd.read_json(ROOT / "results" / "raw_results.jsonl", lines=True)
d = df[df.experiment.isin(["E0", "E0c", "E0d"])]
tab = d.groupby(["variant", "project"]).gmean.mean().unstack(); assert tab.notna().all(axis=1).loc[tab.index.str.startswith(("lawm", "odasc"))].all(), "incomplete dev runs"
tab["mean_dev"] = tab.mean(axis=1)
best = lambda pre: tab[tab.index.str.startswith(pre)].mean_dev.idxmax()
lw, od = best("lawm_"), best("odasc_")
fz = {"frozen": now_iso(), "plan": "plan_v5", "lawm": lw, "lawm_dev": round(float(tab.loc[lw, "mean_dev"]), 4),
      "odasc": od, "odasc_dev": round(float(tab.loc[od, "mean_dev"]), 4), "orb_W90_dev": round(float(tab.loc["orb_W90", "mean_dev"]), 4),
      "lawm_beats_odasc_on_dev": bool(tab.loc[lw, "mean_dev"] > tab.loc[od, "mean_dev"])}
write_json(out, fz); tab.round(4).to_csv(ROOT / "tables" / "E0cd_dev_tuning.csv")
for v, r in tab[tab.index.str.startswith(("lawm", "odasc"))].iterrows():
    log_variant(cycle=2, variant_id=v, description="E0c/E0d dev tuning", data_split_used="dev projects x seeds 0-2",
                metric="gmean_mean_dev", value=round(float(r.mean_dev), 4), outcome="selected" if v in (lw, od) else "not selected")
log_decision(f"plan_v5 freeze: lawm={lw} ({fz['lawm_dev']}), odasc={od} ({fz['odasc_dev']}); lawm beats odasc on dev: {fz['lawm_beats_odasc_on_dev']}", "best mean dev G-mean, dev projects only")
print(json.dumps(fz, indent=1))
