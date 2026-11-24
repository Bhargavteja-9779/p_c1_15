#!/usr/bin/env python3
"""After E0: choose W* for 'wait' and 'orb' (best mean dev G-mean over dev projects x explore seeds),
determine the best non-oracle baseline on dev, and freeze state/frozen_config.json. Refuses to overwrite."""
import sys, os, json, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import STATE, ROOT, write_json, read_json, now_iso, log_decision, log_variant
if "--v2" in sys.argv:
    fz = read_json(STATE / "frozen_config.json"); assert fz, "freeze v1 first"
    if "v2" in fz: print(json.dumps(fz["v2"], indent=1)); sys.exit("v2 already frozen (never refreeze after test runs)")
    df = pd.read_json(ROOT / "results" / "raw_results.jsonl", lines=True)
    e = df[df.experiment == "E0b"]
    assert len(e) == 240, f"E0b incomplete: {len(e)}/240 runs"
    tab = e.groupby(["variant", "project"]).gmean.mean().unstack(); tab["mean_dev"] = tab.mean(axis=1)
    fam = e.groupby("variant").family.first(); tab["family"] = fam
    tab = tab.sort_values("mean_dev", ascending=False); print(tab.round(4).to_string())
    jobs = {j["params"]["variant"]: j["params"] for j in read_json(STATE / "queue.json")["jobs"] if j["params"].get("experiment") == "E0b"}
    v2 = {}
    for f in ("LAT", "MAT", "ODaSC", "OOB"):
        v = tab[tab.family == f].mean_dev.idxmax()
        prm = {k: x for k, x in jobs[v].items() if k not in ("project", "seed", "experiment", "split", "variant")}
        v2[f] = {"variant": v, "params": prm, "mean_dev": round(float(tab.loc[v, "mean_dev"]), 4)}
    v1 = fz["dev_means"]
    base = {"nowait": v1["nowait"], f"wait_W{fz['wait_W']}": v1[f"wait_W{fz['wait_W']}"], f"orb_W{fz['orb_W']}": v1[f"orb_W{fz['orb_W']}"],
            "law_lagakos_model": v1["law_lagakos_model"], **{f: v2[f]["mean_dev"] for f in ("MAT", "ODaSC", "OOB")}}
    fz["v2"] = dict(frozen=now_iso(), families=v2, best_baseline_on_dev=max(base, key=base.get), dev_baselines=base,
                    proposed="LAT* = " + v2["LAT"]["variant"])
    fz["v2"].update({f: v2[f] for f in v2})
    write_json(STATE / "frozen_config.json", fz)
    tab.round(4).to_csv(ROOT / "tables" / "E0b_dev_tuning.csv")
    for v, r in tab.iterrows():
        log_variant(cycle=1, variant_id=v, description=f"E0b dev tuning ({r.family})", data_split_used="dev projects x seeds 0-2",
                    metric="gmean_mean_dev", value=round(float(r.mean_dev), 4), outcome="selected" if v in [x["variant"] for x in v2.values()] else "not selected")
    log_decision(f"Frozen v2: " + ", ".join(f"{f}*={v2[f]['variant']}" for f in v2) + f"; best dev baseline={fz['v2']['best_baseline_on_dev']}",
                 "Highest mean dev G-mean per family (E0b, dev only, 5 configs each)")
    print(json.dumps(fz["v2"], indent=1)); sys.exit(0)
if (STATE / "frozen_config.json").exists() and "--force" not in sys.argv:
    print(open(STATE / "frozen_config.json").read()); sys.exit("already frozen (never refreeze after test runs)")
df = pd.read_json(ROOT / "results" / "raw_results.jsonl", lines=True)
e0 = df[df.experiment == "E0"]
tab = e0.groupby(["variant", "project"]).gmean.mean().unstack()
tab["mean_dev"] = tab.mean(axis=1); tab = tab.sort_values("mean_dev", ascending=False)
print(tab.round(4).to_string())
best = lambda pre: tab[tab.index.str.startswith(pre)].mean_dev.idxmax()
wv, ov = best("wait_W"), best("orb_W")
base = {"nowait": tab.loc["nowait", "mean_dev"], wv: tab.loc[wv, "mean_dev"], ov: tab.loc[ov, "mean_dev"]}
fz = {"frozen": now_iso(), "wait_W": int(wv.split("W")[1]), "orb_W": int(ov.split("W")[1]),
      "best_baseline_on_dev": max(base, key=base.get), "dev_means": {k: round(float(v), 4) for k, v in tab.mean_dev.items()},
      "proposed": "law_lagakos_model (pre-specified in plan_v1)", "n_e0_runs": int(len(e0))}
write_json(STATE / "frozen_config.json", fz)
tab.round(4).to_csv(ROOT / "tables" / "E0_dev_tuning.csv")
for v, r in tab.iterrows():
    log_variant(cycle=1, variant_id=v, description="E0 dev tuning", data_split_used="dev projects x seeds 0-2",
                metric="gmean_mean_dev", value=round(float(r.mean_dev), 4), outcome="selected" if v in (wv, ov, "law_lagakos_model") else "not selected")
log_decision(f"Frozen config: wait W*={fz['wait_W']}, orb W*={fz['orb_W']}, best dev baseline={fz['best_baseline_on_dev']}", "Highest mean dev G-mean (E0, dev projects only); proposed method config pre-specified, not tuned")
print(json.dumps(fz, indent=1))
