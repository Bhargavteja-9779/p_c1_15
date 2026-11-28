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
if "E8" in set(df.experiment) and fz.get("plan") == "plan_v3":
    # H6 (plan_v4): frozen plan_v3 comparison replicated on ApacheJIT, no re-tuning, same statistics
    P = fz["proposed"]["variant"]; B = [b["variant"] for b in fz["baselines"]]
    compare("E8", P, B, "E8_H6_replication_apachejit")
if "E7" in set(df.experiment):
    # H5 (plan_v4): share of the nowait->oracle AUC gap recovered by revealing young / old labels, per project
    e7 = df[df.experiment == "E7"]; out = {}
    for bench, sub in [("cabral_test", e7[~e7.project.str.startswith("aj_")]), ("apachejit", e7[e7.project.str.startswith("aj_")])]:
        a = sub.groupby(["project", "variant"]).auc.mean().unstack()
        if not {"oracle", "nowait"} <= set(a.columns): continue
        gap = a.oracle - a.nowait
        rec = {v: ((a[v] - a.nowait) / gap) for v in a.columns if v.startswith("oracle_")}
        rec_df = pd.DataFrame(rec).assign(gap_auc=gap, auc_nowait=a.nowait, auc_oracle=a.oracle).round(4)
        rec_df.to_csv(T / f"E7_H5_recovery_{bench}.csv")
        med = {v: round(float(r.median()), 4) for v, r in rec.items()}
        out[bench] = {"n_projects": int(len(a)), "median_gap_auc": round(float(gap.median()), 4), "median_recovery": med,
                      "mean_recovery": {v: round(float(r.mean()), 4) for v, r in rec.items()},
                      "H5_young30_ge_0.5": bool(med.get("oracle_young_H30", -1) >= 0.5),
                      "H5_old180_le_0.2": bool(med.get("oracle_old_H180", 9) <= 0.2),
                      "projects_young30_ge_0.5": int((rec.get("oracle_young_H30", pd.Series(dtype=float)) >= 0.5).sum()),
                      "projects_old180_le_0.2": int((rec.get("oracle_old_H180", pd.Series(dtype=float)) <= 0.2).sum())}
        # paired test over projects: young_H30 vs old_H180 AUC (does recent-label access beat old-label access?)
        if {"oracle_young_H30", "oracle_old_H180"} <= set(a.columns):
            d = (a.oracle_young_H30 - a.oracle_old_H180).dropna()
            w = stats.wilcoxon(d.values) if len(d) >= 5 else None
            lo, hi = ci_boot(d.values)
            out[bench]["young30_minus_old180_auc"] = {"mean": round(float(d.mean()), 4), "ci95": [round(lo, 4), round(hi, 4)],
                                                      "wins": int((d > 0).sum()), "n": int(len(d)), "wilcoxon_p": float(w.pvalue) if w else None}
        out[bench]["H5_supported"] = bool(out[bench]["H5_young30_ge_0.5"] and out[bench]["H5_old180_le_0.2"])
    statsout["E7_H5_decomposition"] = out
if "E10" in set(df.experiment) and "E8" in set(df.experiment):
    # H9 (plan_v5): threshold gain per label policy vs spread among thresholded label policies (ApacheJIT)
    aj = df[df.experiment.isin(["E8", "E10"]) & df.project.str.startswith("aj_")]
    pp = aj.groupby(["variant", "project"]).gmean.mean().unstack()
    pairs = [("nowait", "nowait_gmax_lat"), ("wait_W90", "wait_W90_gmax_lat"), ("orb_W90", "orb_W90_gmax_lat"),
             ("odasc_W30", "odasc_W30_gmax_lat"), ("law_lagakos_model", "law_lagakos_model_gmax_lat")]
    rows, ps = [], []
    for fixed, thr in pairs:
        if fixed not in pp.index or thr not in pp.index: continue
        d = (pp.loc[thr] - pp.loc[fixed]).dropna(); w = stats.wilcoxon(d.values); lo, hi = ci_boot(d.values)
        rows.append({"policy": fixed, "thr_minus_fixed": round(float(d.mean()), 4), "ci95": [round(lo, 4), round(hi, 4)],
                     "wins": int((d > 0).sum()), "n": int(len(d)), "wilcoxon_p": float(w.pvalue),
                     "in_H9a_family": fixed != "law_lagakos_model"})
    fam = [r for r in rows if r["in_H9a_family"]]
    for r, a in zip(fam, holm([r["wilcoxon_p"] for r in fam])): r["holm_p"] = float(a)
    thr_vars = ["nowait_gmax_lat", "wait_W30_gmax_lat", "wait_W90_gmax_lat", "orb_W90_gmax_lat", "odasc_W15_gmax_lat",
                "odasc_W30_gmax_lat", "law_lagakos_model_gmax_lat"]
    means = {v: round(float(pp.loc[v].mean()), 4) for v in thr_vars if v in pp.index}
    spread = max(means.values()) - min(means.values()) if means else None
    gain = float(np.mean([r["thr_minus_fixed"] for r in fam])) if fam else None
    statsout["E10_H9_threshold_vs_label_policy"] = {
        "threshold_gain": rows, "thresholded_means": means, "spread_thresholded": round(spread, 4) if spread is not None else None,
        "mean_threshold_gain_H9a_family": round(gain, 4) if gain is not None else None,
        "H9a_supported": bool(fam and all(r["holm_p"] < 0.05 and r["thr_minus_fixed"] > 0 for r in fam)),
        "H9b_supported": bool(spread is not None and gain is not None and spread < gain)}
    pp.round(4).to_csv(T / "E10_E8_gmean_by_project_apachejit.csv")
vt = pd.read_csv(STATE / "variants_tried.csv") if (STATE / "variants_tried.csv").exists() else pd.DataFrame()
statsout["n_variants_logged"] = int(len(vt))
json.dump(metrics, open(R / "metrics.json", "w"), indent=1)
json.dump(statsout, open(R / "statistics.json", "w"), indent=1)

# figures
for exp in [x for x in ["E0", "E1", "E8"] if x in set(df.experiment)]:
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
