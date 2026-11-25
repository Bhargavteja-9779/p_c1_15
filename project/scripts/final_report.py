#!/usr/bin/env python3
"""Section 12: results report from result files only (no LLM). Produces results/raw_results.csv,
results/metrics.json, results/statistics.json, tables/*.csv|md, figures/*.png, results/RESULTS_SUMMARY.md."""
import sys, os, json, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import ROOT, STATE, read_json, now_iso
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

R = ROOT / "results"; T = ROOT / "tables"; F = ROOT / "figures"
df = pd.read_json(R / "raw_results.jsonl", lines=True)
df = df.drop_duplicates(subset=["job_id"], keep="last") if "job_id" in df else df
df.to_csv(R / "raw_results.csv", index=False)
fz = read_json(STATE / "frozen_config.json", {})
NONTRIVIAL = 0.02

def ci_boot(x, n=10000, seed=0):
    x = np.asarray(x, float); rng = np.random.default_rng(seed)
    bs = rng.choice(x, (n, len(x)), replace=True).mean(1); return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

def holm(ps):
    ps = np.asarray(ps, float); o = np.argsort(ps); adj = np.empty_like(ps); run = 0
    for r, i in enumerate(o):
        run = max(run, (len(ps) - r) * ps[i]); adj[i] = min(1.0, run)
    return adj

metrics, statsout, md = {}, {"generated": now_iso()}, []
for exp in sorted(df.experiment.unique()):
    e = df[df.experiment == exp]
    g = e.groupby(["variant", "project"])[["gmean", "r0", "r1", "rdiff", "auc", "mcc", "seconds"]].mean()
    per_proj = g.gmean.unstack()
    per_proj.round(4).to_csv(T / f"{exp}_gmean_by_project.csv")
    summ = e.groupby("variant")[["gmean", "r0", "r1", "rdiff", "auc", "mcc", "seconds"]].agg(["mean", "std"])
    summ.round(4).to_csv(T / f"{exp}_summary.csv")
    metrics[exp] = {}
    for v in per_proj.index:
        x = per_proj.loc[v].dropna().values
        lo, hi = ci_boot(x) if len(x) > 1 else (np.nan, np.nan)
        seed_sd = float(e[e.variant == v].groupby("project").gmean.std().mean())
        metrics[exp][v] = {"gmean_mean_over_projects": round(float(x.mean()), 4), "ci95_projects": [round(lo, 4), round(hi, 4)],
                           "mean_seed_sd": round(seed_sd, 4), "n_projects": int(len(x)),
                           **{f"{m}_mean": round(float(e[e.variant == v][m].mean()), 4) for m in ["r0", "r1", "rdiff", "auc", "mcc", "seconds"]}}
    md.append(f"### {exp}\n\n" + per_proj.assign(MEAN=per_proj.mean(axis=1)).sort_values("MEAN", ascending=False).round(3).to_markdown() + "\n")

def compare(exp, prop, others, label):
    e = df[df.experiment == exp]; pp = e.groupby(["variant", "project"]).gmean.mean().unstack()
    if prop not in pp.index: return None
    rows, ps = [], []
    for o in others:
        if o not in pp.index: continue
        d = (pp.loc[prop] - pp.loc[o]).dropna()
        w = stats.wilcoxon(d.values, alternative="two-sided") if len(d) >= 5 else None
        t = stats.ttest_1samp(d.values, 0.0)
        n = len(d); rpos = stats.rankdata(np.abs(d.values))
        rb = float((rpos[d.values > 0].sum() - rpos[d.values < 0].sum()) / rpos.sum()) if rpos.sum() else 0.0
        lo, hi = ci_boot(d.values)
        rows.append({"proposed": prop, "baseline": o, "n_projects": n, "mean_diff": round(float(d.mean()), 4),
                     "ci95": [round(lo, 4), round(hi, 4)], "wins": int((d > 0).sum()), "losses": int((d < 0).sum()),
                     "wilcoxon_p": float(w.pvalue) if w else None, "paired_t_p": float(t.pvalue), "rank_biserial": round(rb, 3)})
        ps.append(float(w.pvalue) if w else 1.0)
    adj = holm(ps)
    for r, a in zip(rows, adj): r["holm_p"] = float(a); r["G5_pass"] = bool(a < 0.05 and r["ci95"][0] > 0 and r["mean_diff"] >= NONTRIVIAL)
    statsout[label] = rows
    return rows

if "E1" in set(df.experiment) and fz.get("plan") == "plan_v3":
    P = fz["proposed"]["variant"]; B = [b["variant"] for b in fz["baselines"]]
    # primary family (Holm over all 6 non-oracle baselines); primary comparator = fz["primary_comparator"]
    compare("E1", P, B, "E1_main_proposed_vs_baselines")
    statsout["E1_primary_comparator"] = fz["primary_comparator"]
    e12 = pd.concat([df[df.experiment == "E1"], df[df.experiment == "E2"]]).assign(experiment="E12")
    df = pd.concat([df, e12])
    compare("E12", P, ["law_lagakos_model", "law_naive_model_gmax_lat", "law_lagakos_base_gmax_lat", "nowait_gmax_lat"],
            "E2_ablation_full_vs_component_removed")
if "E3" in set(df.experiment) and fz.get("plan") == "plan_v3":
    P = fz["proposed"]["variant"]
    compare("E3", P + "_ds2", ["odasc_W30_ds2", "wait_W90_ds2", "odasc_W15_gmax_lat_ds2"], "E3_robust_delay_x2")
vt = pd.read_csv(STATE / "variants_tried.csv") if (STATE / "variants_tried.csv").exists() else pd.DataFrame()
statsout["n_variants_logged"] = int(len(vt))
json.dump(metrics, open(R / "metrics.json", "w"), indent=1)
json.dump(statsout, open(R / "statistics.json", "w"), indent=1)

# figures
for exp in [x for x in ["E0", "E1"] if x in set(df.experiment)]:
    pp = df[df.experiment == exp].groupby(["variant", "project"]).gmean.mean().unstack()
    pp = pp.loc[pp.mean(axis=1).sort_values().index]
    fig, ax = plt.subplots(figsize=(7, 0.35 * len(pp) + 1.5))
    for i, (v, r) in enumerate(pp.iterrows()):
        ax.scatter(r.values, [i] * len(r), s=12, alpha=.5, color="#888"); ax.scatter([r.mean()], [i], color="#1f5fa8", s=40, zorder=3)
    ax.set_yticks(range(len(pp))); ax.set_yticklabels(pp.index); ax.set_xlabel("G-mean (per project: grey; mean: blue)")
    ax.set_title(f"{exp}: prequential G-mean"); fig.tight_layout(); fig.savefig(F / f"{exp}_gmean.png", dpi=150); plt.close(fig)

with open(R / "RESULTS_SUMMARY.md", "w") as f:
    f.write(f"# RESULTS SUMMARY (auto-generated {now_iso()} by scripts/final_report.py)\n\n")
    f.write("Journal: JKSU-CIS (see journal_selection/selected_journal.md). Topic: topic/selected_topic.md. Plan: experiments/plan_v*.yaml.\n\n")
    f.write(f"Frozen config: `{json.dumps(fz)}`\n\n")
    q = read_json(STATE / "queue.json", {"jobs": []}); from collections import Counter
    f.write(f"Jobs: {dict(Counter(j['status'] for j in q['jobs']))}\n\n")
    f.write("## G-mean by project (mean over seeds)\n\n" + "\n".join(md) + "\n")
    f.write("## Statistics\n\n```json\n" + json.dumps(statsout, indent=1) + "\n```\n")
    b = read_json(STATE / "budget.json", {})
    f.write(f"\nCompute used: {b.get('global_seconds',0)/3600:.2f} CPU-h (summed worker seconds). Variants logged: {len(vt)}.\n")
print("report written")
