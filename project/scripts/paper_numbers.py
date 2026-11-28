#!/usr/bin/env python3
"""Derived quantities quoted in paper/manuscript.md, computed ONLY from result files
(results/raw_results.jsonl, tables/*). Writes results/paper_numbers.json. Idempotent."""
import sys, os, json, numpy as np, pandas as pd
from scipy.stats import spearmanr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import ROOT, now_iso

R, T = ROOT / "results", ROOT / "tables"
df = pd.read_json(R / "raw_results.jsonl", lines=True).drop_duplicates("job_id", keep="last")
out = {"generated": now_iso()}

# dev tuning: lead of frozen LAW over best baseline (E0, mean over dev projects x seeds 0-2)
e0 = df[df.experiment == "E0"].groupby(["variant", "project"]).gmean.mean().unstack().mean(1)
out["dev_lead_law_over_odasc_W30"] = round(float(e0["law_lagakos_model_gmax_lat"] - e0["odasc_W30"]), 4)
e0a = df[df.experiment == "E0"].groupby(["variant", "project"]).auc.mean().unstack().mean(1)
out["dev_auc_law_lagakos_model"] = round(float(e0a["law_lagakos_model"]), 4)
out["dev_auc_best_baseline"] = round(float(e0a.drop([v for v in e0a.index if v.startswith("law") or v == "oracle"]).max()), 4)

# D1 dev decomposition (fabric, neutron, sentry; seed 0)
d1 = df[df.experiment.isin(["D1", "E0"]) & df.project.isin(["fabric", "neutron", "sentry"]) & (df.seed == 0)]
a = d1.groupby(["project", "variant"]).auc.mean().unstack()
gap = a.oracle - a.nowait
out["D1_dev_mean_recovery"] = {v: round(float(((a[v] - a.nowait) / gap).mean()), 4) for v in a.columns if v.startswith("oracle_")}
out["D1_dev_recovery_of_mean_auc"] = {v: round(float((a[v].mean() - a.nowait.mean()) / (a.oracle.mean() - a.nowait.mean())), 4)
                                      for v in a.columns if v.startswith("oracle_")}

# E9 inspection (dev): gains of best 5% policy vs no inspection; spread of label policies without inspection
e9 = df[df.experiment == "E9"]; projs, seeds = set(e9.project), set(e9.seed)
base = df[(df.experiment == "E0") & df.project.isin(projs) & df.seed.isin(seeds)].groupby("variant").auc.mean()
g = {}
for b in ["nowait_gmax_lat", "odasc_W30", "law_lagakos_model_gmax_lat"]:
    best5 = max(e9[e9.variant == f"{b}__insp_{p}_5"].auc.mean() for p in ["rand", "top", "unc"])
    g[b] = round(float(best5 - base[b]), 4)
out["E9_best5_gain_auc"] = g
b3 = base[["nowait_gmax_lat", "odasc_W30", "law_lagakos_model_gmax_lat"]]
out["E9_label_policy_spread_auc"] = round(float(b3.max() - b3.min()), 4)

# convergence / gaps
m = json.load(open(R / "metrics.json"))
e1 = m["E1"]; e8 = m["E8"]
conv1 = [e1[v]["gmean_mean_over_projects"] for v in ["law_lagakos_model_gmax_lat", "odasc_W30", "odasc_W15_gmax_lat", "wait_W30_gmax_lat"]]
out["E1_spread_handled_policies"] = round(max(conv1) - min(conv1), 4)
out["E1_oracle_minus_law_gmean"] = round(e1["oracle"]["gmean_mean_over_projects"] - e1["law_lagakos_model_gmax_lat"]["gmean_mean_over_projects"], 4)
out["E8_oracle_minus_law_gmean"] = round(e8["oracle"]["gmean_mean_over_projects"] - e8["law_lagakos_model_gmax_lat"]["gmean_mean_over_projects"], 4)
out["E1_oracle_minus_best_auc"] = round(e1["oracle"]["auc_mean"] - max(v["auc_mean"] for k, v in e1.items() if k != "oracle"), 4)
out["E8_oracle_minus_best_auc"] = round(e8["oracle"]["auc_mean"] - max(v["auc_mean"] for k, v in e8.items() if k != "oracle"), 4)

# E7 diagnostic correlations (exploratory)
prof = pd.read_csv(T / "E7_diag_benchmark_profile.csv")
rec = pd.concat([pd.read_csv(T / "E7_H5_recovery_cabral_test.csv"), pd.read_csv(T / "E7_H5_recovery_apachejit.csv")])
rec = rec.rename(columns={rec.columns[0]: "project"}).merge(prof, on="project")
out["E7_spearman_young30_recovery"] = {c: {"rho": round(float(spearmanr(rec[c], rec.oracle_young_H30)[0]), 2),
                                           "p": round(float(spearmanr(rec[c], rec.oracle_young_H30)[1]), 3)}
                                       for c in ["commits_per_30d", "share_found_within_30d", "median_delay_d", "bug_rate"]}
json.dump(out, open(R / "paper_numbers.json", "w"), indent=1)
print(json.dumps(out, indent=1))
