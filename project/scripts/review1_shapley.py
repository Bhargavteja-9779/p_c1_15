#!/usr/bin/env python3
"""plan_v8 A1: 2x2 factorial (labels observed/true x window waited-W30/all) on existing runs; Shapley split with
project-bootstrap CIs. Writes results/review1/shapley.json."""
import json, numpy as np, pandas as pd, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
df = pd.read_json(os.path.join(ROOT, "results/raw_results.jsonl"), lines=True)
TEST = ["brackets","broadleaf","camel","jgroups","matplotlib","npm","spring-integration","tomcat","wagtail","zulip"]
AJ = ["aj_activemq","aj_cassandra","aj_flink","aj_groovy","aj_hadoop-hdfs","aj_hbase","aj_hive","aj_ignite","aj_kafka"]
rv = pd.read_json(os.path.join(ROOT, "results/review1/raw.jsonl"), lines=True)
rv = rv[rv.analysis == "A2"].assign(experiment="A2")
dfx = pd.concat([df, rv[["experiment", "project", "variant", "seed", "gmean", "auc"]]], ignore_index=True)
def cells(exps, projects, metric, W=30):
    e = dfx[dfx.experiment.isin(exps) & dfx.project.isin(projects)]
    t = e.groupby(["variant", "project"])[metric].mean().unstack()[projects]
    return t.loc[f"wait_W{W}"].values, t.loc[f"decomp_L1_W{W}"].values, t.loc["nowait"].values, t.loc["oracle"].values
def effects(w, l1, nw, o):
    noise = 0.5 * ((l1 - w) + (o - nw)); fresh = 0.5 * ((nw - w) + (o - l1)); inter = (o - nw) - (l1 - w)
    gap = o - w
    return dict(gap=gap.mean(), noise=noise.mean(), fresh=fresh.mean(), interaction=inter.mean(),
                share_path_noise_first=(l1 - w).mean() / gap.mean(), shapley_noise_share=noise.mean() / gap.mean())
out = {}
for fam, exps, P in [("cabral_test", ["E1", "E3b"], TEST), ("apachejit", ["E8"], AJ)]:
    for metric in ["gmean", "auc"]:
        w, l1, nw, o = cells(exps, P, metric); point = effects(w, l1, nw, o)
        rng = np.random.default_rng(0); boots = []
        for _ in range(10000):
            i = rng.integers(0, len(P), len(P)); boots.append(effects(w[i], l1[i], nw[i], o[i]))
        ci = {k: [float(np.percentile([b[k] for b in boots], 2.5)), float(np.percentile([b[k] for b in boots], 97.5))] for k in point}
        out[f"{fam}_{metric}"] = {k: dict(est=round(float(v), 4), ci95=[round(c, 4) for c in ci[k]]) for k, v in point.items()}
        out[f"{fam}_{metric}"]["cells_mean"] = dict(wait_W30=round(float(w.mean()),4), L1_W30=round(float(l1.mean()),4), nowait=round(float(nw.mean()),4), oracle=round(float(o.mean()),4))
        out[f"{fam}_{metric}"]["per_project_abs_gain_L1_minus_wait"] = dict(zip([p.replace("aj_","") for p in P], np.round(l1 - w, 4).tolist()))
        out[f"{fam}_{metric}"]["per_project_gap_oracle_minus_wait"] = dict(zip([p.replace("aj_","") for p in P], np.round(o - w, 4).tolist()))
# W=90 Shapley split, both families (A2 supplies ApacheJIT L1-W90)
for fam, exps, P in [("cabral_test", ["E1", "E3b"], TEST), ("apachejit", ["E8", "A2"], AJ)]:
    for metric in ["gmean", "auc"]:
        w, l1, nw, o = cells(exps, P, metric, W=90); point = effects(w, l1, nw, o)
        rng = np.random.default_rng(0); boots = []
        for _ in range(10000):
            i = rng.integers(0, len(P), len(P)); boots.append(effects(w[i], l1[i], nw[i], o[i]))
        ci = {k: [float(np.percentile([b[k] for b in boots], 2.5)), float(np.percentile([b[k] for b in boots], 97.5))] for k in point}
        out[f"{fam}_W90_{metric}"] = {k: dict(est=round(float(v), 4), ci95=[round(c, 4) for c in ci[k]]) for k, v in point.items()}
# W=90 share on Cabral with CI (R1#1)
e = df[df.experiment.isin(["E1","E3b"]) & df.project.isin(TEST)]
for metric in ["gmean","auc"]:
    t = e.groupby(["variant","project"])[metric].mean().unstack()[TEST]
    w, l, o = t.loc["wait_W90"].values, t.loc["decomp_L1_W90"].values, t.loc["oracle"].values
    rng = np.random.default_rng(0); bs = []
    for _ in range(10000):
        i = rng.integers(0, 10, 10); bs.append((l[i]-w[i]).mean()/(o[i]-w[i]).mean())
    out[f"cabral_test_W90_share_{metric}"] = dict(est=round(float((l-w).mean()/(o-w).mean()),4), ci95=[round(float(np.percentile(bs,2.5)),4), round(float(np.percentile(bs,97.5)),4)],
                                                 wait_W90=round(float(w.mean()),4), L1_W90=round(float(l.mean()),4), oracle=round(float(o.mean()),4))
os.makedirs(os.path.join(ROOT, "results/review1"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "results/review1/shapley.json"), "w"), indent=1)
for k, v in out.items():
    print(k, {kk: vv for kk, vv in v.items() if not kk.startswith("per_project")})
