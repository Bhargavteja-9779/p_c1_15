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
df = df.drop_duplicates(subset=["job_id"], keep="last")
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

if "E1" in set(df.experiment) and fz:
    base = ["nowait", f"wait_W{fz['wait_W']}", f"orb_W{fz['orb_W']}"]
    compare("E1", "law_lagakos_model", base, "E1_main_law_vs_baselines")
    e12 = pd.concat([df[df.experiment == "E1"], df[df.experiment == "E2"]]); e12 = e12.assign(experiment="E12")
    df = pd.concat([df, e12])
    compare("E12", "law_lagakos_model", ["law_naive_model", "law_lagakos_base", "law_naive_base"], "E2_ablation_full_vs_variants")
if "E1" in set(df.experiment) and fz and fz.get("candidate"):
    # plan_v3: H1 family = {law_lagakos_model, candidate} x 3 baselines, one Holm correction over all 6 tests
    base = ["nowait", f"wait_W{fz['wait_W']}", f"orb_W{fz['orb_W']}"]
    ra = compare("E1", "law_lagakos_model", base, "_tmp_a") or []; rb_ = compare("E1", fz["candidate"], base, "_tmp_b") or []
    fam = ra + rb_; adj = holm([r["wilcoxon_p"] if r["wilcoxon_p"] is not None else 1.0 for r in fam])
    for r, a in zip(fam, adj): r["holm_p_family6"] = float(a); r["G5_pass"] = bool(a < 0.05 and r["ci95"][0] > 0 and r["mean_diff"] >= NONTRIVIAL)
    statsout["E1_H1_family_law_and_candidate_vs_baselines"] = fam; statsout.pop("_tmp_a", None); statsout.pop("_tmp_b", None)
if "E3b" in set(df.experiment) and "E1" in set(df.experiment):
    # plan_v3 H3: share of oracle - wait_W30 gap recovered by denoising, and decomp_L1_W30 vs wait_W90 (frozen best fixed W)
    e = pd.concat([df[df.experiment == "E3b"], df[(df.experiment == "E1") & (df.variant == "oracle")]])
    pp = e.groupby(["variant", "project"]).gmean.mean().unstack()
    h3 = {}
    if {"oracle", "wait_W30", "decomp_L1_W30", "wait_W90"} <= set(pp.index):
        gap = (pp.loc["oracle"] - pp.loc["wait_W30"]); rec = (pp.loc["decomp_L1_W30"] - pp.loc["wait_W30"])
        h3["gap_recovered_share_of_means"] = round(float(rec.mean() / gap.mean()), 4)
        h3["gap_recovered_share_per_project"] = {k: round(float(v), 3) for k, v in (rec / gap).items()}
        h3["mean_gap_oracle_minus_wait30"] = round(float(gap.mean()), 4)
        for W in (30, 90):
            if {f"decomp_L1_W{W}", f"wait_W{W}"} <= set(pp.index):
                h3[f"denoise_gain_W{W}_mean"] = round(float((pp.loc[f"decomp_L1_W{W}"] - pp.loc[f"wait_W{W}"]).mean()), 4)
                h3[f"denoise_gap_share_W{W}"] = round(float((pp.loc[f"decomp_L1_W{W}"] - pp.loc[f"wait_W{W}"]).mean() / (pp.loc["oracle"] - pp.loc[f"wait_W{W}"]).mean()), 4)
        df_h3 = e.assign(experiment="E3bx"); df = pd.concat([df, df_h3])
        rows = compare("E3bx", "decomp_L1_W30", ["wait_W90", "wait_W30"], "E3b_H3_denoised_W30_vs_wait")
        h3["H3_pass"] = bool(h3["gap_recovered_share_of_means"] >= 0.5 and rows and rows[0]["holm_p"] < 0.05 and rows[0]["mean_diff"] > 0)
    statsout["E3b_H3_decomposition"] = h3
if "E3" in set(df.experiment) and fz:
    compare("E3", "law_lagakos_model_ds2", ["nowait_ds2", f"wait_W{fz['wait_W']}_ds2", f"orb_W{fz['orb_W']}_ds2"], "E3_robust_delay_x2")
fz6 = read_json(STATE / "frozen_config_v6.json", {})
if "E8" in set(df.experiment) and fz6:
    # plan_v7 H6 (fresh ApacheJIT confirmation): primary dev candidate vs wait_W90, orb_W90, odasc (one Holm over 3)
    prim = fz6["primary_candidate"]; od = [c["variant"] for c in fz6["candidates_specs"] if c["method"] == "odasc"][0]
    # a self-comparison is degenerate (all differences 0): if the primary IS odasc, the family is the 2 waiting baselines
    rows = compare("E8", prim, ["wait_W90", "orb_W90"] + ([od] if prim != od else []), "E8_planv7_H6_primary_vs_baselines") or []
    statsout["E8_H6_family_note"] = (f"primary={prim}; " + ("Holm over 3 tests" if prim != od else
        "primary is the odasc baseline itself -> self-comparison dropped, Holm over 2 tests (decision 2026-11-25, before E8 analysis)"))
    for r in rows:   # plan_v7: margin >= 0.02 required vs waiting baselines; vs odasc reported as is (no margin)
        need_margin = r["baseline"] != od
        r["H6_pass"] = bool(r["holm_p"] < 0.05 and r["ci95"][0] > 0 and (r["mean_diff"] >= NONTRIVIAL if need_margin else r["mean_diff"] > 0))
    statsout["E8_H6_all_pass"] = bool(rows and all(r["H6_pass"] for r in rows))
    for c in fz6["candidates_specs"]:   # descriptive: every candidate vs the same baselines (not part of the H6 family)
        if c["variant"] != prim:
            compare("E8", c["variant"], ["wait_W90", "orb_W90"] + ([od] if c["variant"] != od else []), f"E8_descriptive_{c['variant']}")
    pp = df[df.experiment == "E8"].groupby(["variant", "project"]).gmean.mean().unstack(); h = {}
    if {"oracle", "wait_W30", "decomp_L1_W30", "wait_W90"} <= set(pp.index):
        gap = pp.loc["oracle"] - pp.loc["wait_W30"]; rec = pp.loc["decomp_L1_W30"] - pp.loc["wait_W30"]
        h["gap_recovered_share_of_means"] = round(float(rec.mean() / gap.mean()), 4)
        h["gap_recovered_share_per_project"] = {k: round(float(v), 3) for k, v in (rec / gap).items()}
        compare("E8", "decomp_L1_W30", ["wait_W90", "wait_W30"], "E8_secondary_H3_replication")
    statsout["E8_secondary_H3_decomposition"] = h
vt = pd.read_csv(STATE / "variants_tried.csv") if (STATE / "variants_tried.csv").exists() else pd.DataFrame()
statsout["n_variants_logged"] = int(len(vt))
json.dump(metrics, open(R / "metrics.json", "w"), indent=1)
json.dump(statsout, open(R / "statistics.json", "w"), indent=1)

# figures
for exp in [x for x in ["E0", "E0b", "E1", "E3b", "E8"] if x in set(df.experiment)]:
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
