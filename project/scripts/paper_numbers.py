#!/usr/bin/env python3
"""Route A manuscript: compute EVERY number, table and figure the paper uses from result/data files only.
Writes results/paper_numbers.json (named values), paper/tables/T*.md, paper/figures/F*.png. Idempotent."""
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import ROOT
from src.data import load_project
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

R, P = ROOT / "results", ROOT / "paper"; (P / "tables").mkdir(parents=True, exist_ok=True); (P / "figures").mkdir(exist_ok=True)
DAY = 86400.0
DEV = ["fabric", "neutron", "nova", "sentry"]
TEST = ["brackets", "broadleaf", "camel", "jgroups", "matplotlib", "npm", "spring-integration", "tomcat", "wagtail", "zulip"]
AJ = ["aj_activemq", "aj_cassandra", "aj_flink", "aj_groovy", "aj_hadoop-hdfs", "aj_hbase", "aj_hive", "aj_ignite", "aj_kafka"]
N = {}                                   # named numbers
S = json.load(open(R / "statistics.json"))
df = pd.read_json(R / "raw_results.jsonl", lines=True)
ARCH = ROOT / "archive" / "zealous_lamport_cycle1"
da = pd.read_json(ARCH / "results" / "raw_results.jsonl", lines=True)
Sa = json.load(open(ARCH / "results" / "statistics.json"))
f3 = lambda x: float(round(float(x), 3)); f4 = lambda x: float(round(float(x), 4))

def md(tab, path, floatfmt=".3f"):
    open(P / "tables" / path, "w").write(tab.to_markdown(floatfmt=floatfmt) + "\n")

# ---------------------------------------------------------------- T1 datasets + delay distribution
rows, curves = [], {}
for p in DEV + TEST + AJ:
    d = load_project(p); bug = d[d.y == 1]; dl = (bug.t_found - bug.t) / DAY; fin = np.isfinite(dl)
    rows.append(dict(project=p.replace("aj_", ""), family="ApacheJIT" if p.startswith("aj_") else "Cabral",
                     role="fresh confirmation" if p.startswith("aj_") else ("dev" if p in DEV else "test"),
                     commits=len(d), years=round((d.t.max() - d.t.min()) / DAY / 365.25, 1), defect_rate=d.y.mean(),
                     median_delay_d=np.median(dl[fin]), p90_delay_d=np.percentile(dl[fin], 90),
                     found_after_90d=float((dl[fin] > 90).mean())))
    g = np.arange(0, 1500, 5); curves[p] = (g, [(dl[fin] <= a).mean() for a in g])
T1 = pd.DataFrame(rows).set_index("project")
md(T1.round({"defect_rate": 3, "median_delay_d": 0, "p90_delay_d": 0, "found_after_90d": 3}), "T1_datasets.md")
N["n_commits_total"] = int(T1.commits.sum()); N["n_projects"] = len(T1)
for fam in ["Cabral", "ApacheJIT"]:
    t = T1[T1.family == fam]
    N[f"{fam}_median_delay_range"] = [int(round(t.median_delay_d.min())), int(round(t.median_delay_d.max()))]
    N[f"{fam}_p90_delay_range"] = [int(round(t.p90_delay_d.min())), int(round(t.p90_delay_d.max()))]
    N[f"{fam}_found_after_90d_range"] = [f3(t.found_after_90d.min()), f3(t.found_after_90d.max())]
    N[f"{fam}_defect_rate_range"] = [f3(t.defect_rate.min()), f3(t.defect_rate.max())]
    N[f"{fam}_commits"] = int(t.commits.sum())
fig, ax = plt.subplots(figsize=(6.5, 3.6))
for p, (g, c) in curves.items():
    ax.plot(g, c, color="#c0392b" if p.startswith("aj_") else "#1f5fa8", alpha=.6, lw=1)
ax.axvline(30, ls=":", c="k", lw=.8); ax.axvline(90, ls="--", c="k", lw=.8)
ax.set_xlabel("days from commit to discovery of its defect"); ax.set_ylabel("share of defects discovered")
ax.set_title("Discovery delay of defect-inducing commits (blue: Cabral, red: ApacheJIT)", fontsize=9)
fig.tight_layout(); fig.savefig(P / "figures" / "F1_discovery_delay.png", dpi=200); plt.close(fig)

# ---------------------------------------------------------------- T2 RQ1 label noise under waiting (model-free)
rq1 = pd.read_csv(ROOT / "tables" / "rq1_waiting_time_tradeoff.csv").set_index("project")
age = pd.read_csv(ROOT / "tables" / "rq1_false_clean_by_age.csv").set_index("project")
T2 = rq1[["W0_false_clean", "W30_false_clean", "W90_false_clean", "W90_excluded"]].join(age[["<7d", ">2y"]])
md(T2, "T2_rq1_label_noise.md", ".3f")
red = 1 - rq1.W90_false_clean / rq1.W0_false_clean
N["rq1_relative_reduction_W90_range"] = [f3(red.min()), f3(red.max())]; N["rq1_relative_reduction_W90_median"] = f3(red.median())
N["rq1_W90_excluded_range"] = [f3(rq1.W90_excluded.min()), f3(rq1.W90_excluded.max())]
N["rq1_young_lt7d_false_clean_range"] = [f3(age["<7d"].min()), f3(age["<7d"].max())]
N["rq1_old_gt2y_false_clean_range"] = [f3(age[">2y"].min()), f3(age[">2y"].max())]

# ---------------------------------------------------------------- helpers
def pp(frame, exp, variants, projects):
    e = frame[(frame.experiment.isin(exp if isinstance(exp, list) else [exp])) & frame.variant.isin(variants) & frame.project.isin(projects)]
    return e.groupby(["variant", "project"]).gmean.mean().unstack()[projects]

# ---------------------------------------------------------------- T3 RQ2 decomposition (Cabral test E3b + E1 oracle; ApacheJIT E8)
c = pd.concat([pp(df, "E3b", ["wait_W30", "decomp_L1_W30", "decomp_L2_W30", "wait_W90", "decomp_L1_W90", "decomp_L2_W90"], TEST),
               pp(df, "E1", ["oracle"], TEST)])
a = pp(df, "E8", ["wait_W30", "decomp_L1_W30", "wait_W90", "oracle"], AJ); a.columns = [x.replace("aj_", "") for x in a.columns]
T3 = pd.concat([c.mean(axis=1).rename("Cabral test (10)"), a.mean(axis=1).rename("ApacheJIT (9)")], axis=1)
T3 = T3.loc[["wait_W30", "decomp_L1_W30", "decomp_L2_W30", "wait_W90", "decomp_L1_W90", "decomp_L2_W90", "oracle"]]
md(T3, "T3_rq2_decomposition_means.md")
N["rq2_cabral"] = {k: f3(v) for k, v in T3["Cabral test (10)"].items() if v == v}
N["rq2_apachejit"] = {k: f3(v) for k, v in T3["ApacheJIT (9)"].items() if v == v}
N["rq2_gap_share_cabral_W30"] = S["E3b_H3_decomposition"]["denoise_gap_share_W30"]
N["rq2_gap_share_cabral_W90"] = S["E3b_H3_decomposition"]["denoise_gap_share_W90"]
N["rq2_gap_share_cabral_per_project_range"] = [min(S["E3b_H3_decomposition"]["gap_recovered_share_per_project"].values()), max(S["E3b_H3_decomposition"]["gap_recovered_share_per_project"].values())]
N["rq2_gap_share_aj_W30"] = S["E8_secondary_H3_decomposition"]["gap_recovered_share_of_means"]
N["rq2_gap_share_aj_per_project_range"] = [min(S["E8_secondary_H3_decomposition"]["gap_recovered_share_per_project"].values()), max(S["E8_secondary_H3_decomposition"]["gap_recovered_share_per_project"].values())]
N["rq2_tests_cabral"] = S["E3b_H3_denoised_W30_vs_wait"]; N["rq2_tests_aj"] = S["E8_secondary_H3_replication"]
SH = json.load(open(R / "review1" / "shapley.json"))
fig, axs = plt.subplots(1, 2, figsize=(8, 3.4), sharey=True)
for ax, (fam, P_, lab, col) in zip(axs, [("cabral_test", TEST, "Cabral test (10)", "#1f5fa8"), ("apachejit", AJ, "ApacheJIT (9)", "#c0392b")]):
    for k, (metric, mk) in enumerate([("gmean", "o"), ("auc", "s")]):
        g = SH[f"{fam}_{metric}"]["per_project_abs_gain_L1_minus_wait"]; gap = SH[f"{fam}_{metric}"]["per_project_gap_oracle_minus_wait"]
        names = list(g); x = np.arange(len(names)) + (k - 0.5) * 0.35
        ax.bar(x, [gap[n] for n in names], width=0.35, color="none", edgecolor=col, lw=1, label=f"oracle - Wait-30 ({metric.upper() if metric=='auc' else 'G-mean'})" if True else None)
        ax.bar(x, [g[n] for n in names], width=0.35, color=col, alpha=0.9 if metric == "gmean" else 0.45, label=f"true labels - Wait-30 ({'AUC' if metric=='auc' else 'G-mean'})")
    ax.set_xticks(np.arange(len(names))); ax.set_xticklabels(names, rotation=60, ha="right", fontsize=7); ax.axhline(0, c="k", lw=.6)
    ax.set_xlabel(lab, fontsize=8)
axs[0].set_ylabel("absolute difference"); axs[1].legend(fontsize=6, loc="upper right")
fig.tight_layout(); fig.savefig(P / "figures" / "F2_gap_recovered.png", dpi=200); plt.close(fig)
for k in SH: N["review1_" + k] = {kk: vv for kk, vv in SH[k].items()}
rows3b = []
for fam, lab in [("cabral_test", "Cabral test (10)"), ("apachejit", "ApacheJIT (9)")]:
    for metric in ["gmean", "auc"]:
        e = SH[f"{fam}_{metric}"]; f = lambda k: f"{e[k]['est']:.3f} [{e[k]['ci95'][0]:.3f}, {e[k]['ci95'][1]:.3f}]"
        rows3b.append({"family": lab, "metric": "AUC" if metric == "auc" else "G-mean", "gap (oracle - Wait-30)": f("gap"),
                       "noise effect (Shapley)": f("noise"), "freshness effect (Shapley)": f("fresh"), "interaction": f("interaction"),
                       "noise-first path share": f("share_path_noise_first")})
pd.DataFrame(rows3b).to_markdown(P / "tables" / "T3b_shapley.md", index=False)
w90 = [{"metric": "G-mean" if m == "gmean" else "AUC", **{k: (f"{v['est']:.3f} [{v['ci95'][0]:.3f}, {v['ci95'][1]:.3f}]" if k == "share" else v) for k, v in
        {"share": SH[f"cabral_test_W90_share_{m}"], "Wait-90": SH[f"cabral_test_W90_share_{m}"]["wait_W90"], "Wait-90 true labels": SH[f"cabral_test_W90_share_{m}"]["L1_W90"],
         "oracle": SH[f"cabral_test_W90_share_{m}"]["oracle"]}.items()}} for m in ["gmean", "auc"]]
pd.DataFrame(w90).to_markdown(P / "tables" / "T3c_W90_share_cabral.md", index=False)

# ---------------------------------------------------------------- T4 RQ3 age-only label policies on Cabral test (main-lineage E1)
v4 = ["oracle", "orb_W90", "wait_W90", "awt_e0.4", "law_lagakos_model", "nowait"]
e1 = df[(df.experiment == "E1") & df.variant.isin(v4)]
T4 = e1.groupby("variant")[["gmean", "auc", "r1", "r0"]].mean().loc[v4]
md(T4, "T4_rq3_age_only_cabral_test.md")
N["rq3_means"] = {v: {k: f3(T4.loc[v, k]) for k in T4.columns} for v in v4}
N["rq3_tests"] = S["E1_H1_family_law_and_candidate_vs_baselines"]
law_diag = json.load(open(R / "diag_law_neutron.json")) if (R / "diag_law_neutron.json").exists() else {}
N["rq3_diag_law_neutron_keys"] = list(law_diag)[:20]

# ---------------------------------------------------------------- T5 RQ4 feature-based denoisers on ApacheJIT (E8) + effort-aware metrics
v5 = ["oracle", "dual_W30_k50", "lawm_soft_W30", "odasc_W30_t0.8", "wait_W90", "orb_W90", "wait_W30", "nowait"]
e8 = df[(df.experiment == "E8") & df.variant.isin(v5)]
T5 = e8.groupby("variant")[["gmean", "auc", "r1", "r0", "f1", "mcc", "recall20e", "popt", "ifa"]].mean().loc[v5]
md(T5, "T5_rq4_apachejit_all_metrics.md")
T5p = pp(df, "E8", v5, AJ); T5p.columns = [x.replace("aj_", "") for x in T5p.columns]; T5p["mean"] = T5p.mean(axis=1)
md(T5p.loc[v5], "T5b_rq4_apachejit_gmean_by_project.md")
N["rq4_means"] = {v: {k: f3(T5.loc[v, k]) for k in T5.columns} for v in v5}
N["rq4_confirmatory_H6"] = S["E8_planv7_H6_primary_vs_baselines"]
N["rq4_descriptive_dual"] = S["E8_descriptive_dual_W30_k50"]; N["rq4_descriptive_lawm"] = S["E8_descriptive_lawm_soft_W30"]
# Cabral-test G-mean by project for the main comparison (E1 main lineage)
T4p = pp(df, "E1", v4, TEST); T4p["mean"] = T4p.mean(axis=1); md(T4p.loc[v4], "T4b_rq3_cabral_gmean_by_project.md")

# ---------------------------------------------------------------- T6 RQ5 operating point (dev diagnostic + independent-lineage confirmation)
op = pd.read_csv(ARCH / "results" / "diag" / "operating_point_dev.csv")
T6 = op.set_index(["project", "variant"])[["auc", "gmean_at_05", "gmean_best_thr", "pred_pos_rate", "true_pos_rate"]]
md(T6, "T6_rq5_operating_point_dev.md")
for p in ["fabric", "neutron"]:
    o = op[(op.project == p) & (op.variant != "oracle")]
    N[f"rq5_{p}_spread_at05"] = [f3(o.gmean_at_05.min()), f3(o.gmean_at_05.max())]
    N[f"rq5_{p}_spread_bestthr"] = [f3(o.gmean_best_thr.min()), f3(o.gmean_best_thr.max())]
va = ["law_lagakos_model_gmax_lat", "odasc_W15_gmax_lat", "odasc_W30", "wait_W30_gmax_lat", "orb_W90", "wait_W90", "nowait", "oracle"]
T7 = da[(da.experiment == "E1") & da.variant.isin(va)].groupby("variant")[["gmean", "auc", "r1", "r0"]].mean().loc[va]
md(T7, "T7_rq5_threshold_cabral_test_independent_lineage.md")
N["rq5_cabral_means"] = {v: f3(T7.loc[v, "gmean"]) for v in va}
N["rq5_tests"] = Sa["E1_main_proposed_vs_baselines"]
de = da[da.experiment == "E0"].groupby("variant").gmean.mean()
for v in ["wait_W30", "wait_W30_gmax_lat", "nowait", "nowait_gmax_lat"]: N[f"rq5_dev_{v}"] = f3(de[v])

# ---------------------------------------------------------------- supplementary: delay estimator, data preparation
import re as _re
txt = open(R / "diag_survival_dev.txt").read(); rows = []
for blk in _re.finditer(r"(\w+) T@([\d.]+).*?S_true\s+\[([^\]]+)\]\s+S_lagak\s+\[([^\]]+)\]\s+S_naive\s+\[([^\]]+)\]", txt, _re.S):
    pr, at, st, sl, sn = blk.groups(); st, sl, sn = [list(map(float, x.split(","))) for x in (st, sl, sn)]
    for a, t_, l_, n_ in zip([7, 30, 90, 180, 365], st, sl, sn):
        rows.append(dict(project=pr, at_share_of_history=float(at), age_days=a, S_true=t_, S_truncation_corrected=l_, S_naive=n_))
SD = pd.DataFrame(rows); SD.to_markdown(P / "tables" / "S1_delay_estimator.md", index=False, floatfmt=".3f")
N["s1_max_abs_err_lagakos"] = f3((SD.S_truncation_corrected - SD.S_true).abs().max()); N["s1_max_abs_err_naive"] = f3((SD.S_naive - SD.S_true).abs().max())
N["s1_mean_abs_err_lagakos"] = f3((SD.S_truncation_corrected - SD.S_true).abs().mean()); N["s1_mean_abs_err_naive"] = f3((SD.S_naive - SD.S_true).abs().mean())
CP = pd.DataFrame(json.load(open(R / "review1" / "cabral_copy_rows_vs_mstdp.json"))).T
CP.to_markdown(P / "tables" / "S2_cabral_rows_vs_mstdp.md"); N["s2"] = CP.to_dict(orient="index")
N["aj_fix_before_bug_total"] = int(sum(v["fix_before_bug"] for v in json.load(open(R / "review1" / "apachejit_prep.json")).values()))
ds = json.load(open(R / "data_summary.json")); N["cabral_unmatched_copies_total"] = int(sum(v["unmatched_copies"] for v in ds.values()))
N["cabral_unmatched_copies_range"] = [int(min(v["unmatched_copies"] for v in ds.values())), int(max(v["unmatched_copies"] for v in ds.values()))]
# ---------------------------------------------------------------- review round 1 runs (plan_v8 A2-A5), when present
from scipy import stats as _st
RV = R / "review1" / "raw.jsonl"
if RV.exists():
    rv = pd.read_json(RV, lines=True)
    def _pp(an, variants, projects, metric="gmean"):
        e = rv[(rv.analysis == an) & rv.variant.isin(variants) & rv.project.isin(projects)]
        return e.groupby(["variant", "project"])[metric].mean().unstack()
    def _cmp(a, b, label):
        d = (a - b).dropna(); rng = np.random.default_rng(0)
        bs = [d.values[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
        w = _st.wilcoxon(d.values) if len(d) >= 5 and (d != 0).any() else None
        return dict(comparison=label, n=int(len(d)), mean_diff=f4(d.mean()), ci95=[f4(np.percentile(bs, 2.5)), f4(np.percentile(bs, 97.5))],
                    wins=int((d > 0).sum()), losses=int((d < 0).sum()), wilcoxon_p=float(w.pvalue) if w else None)
    # A2: ApacheJIT W=90 decomposition
    if (rv.analysis == "A2").any():
        base = df[(df.experiment == "E8") & df.project.isin(AJ)]
        out = {}
        for metric in ["gmean", "auc"]:
            b = base.groupby(["variant", "project"])[metric].mean().unstack()
            a2 = _pp("A2", ["decomp_L1_W90", "decomp_L2_W90"], AJ, metric)
            w, l1, o = b.loc["wait_W90", AJ], a2.loc["decomp_L1_W90", AJ], b.loc["oracle", AJ]
            rng = np.random.default_rng(0); bs = []
            for _ in range(10000):
                i = rng.integers(0, len(AJ), len(AJ)); bs.append((l1.values[i] - w.values[i]).mean() / (o.values[i] - w.values[i]).mean())
            out[metric] = dict(wait_W90=f3(w.mean()), L1_W90=f3(l1.mean()), L2_W90=f3(a2.loc["decomp_L2_W90", AJ].mean()), oracle=f3(o.mean()),
                               share=f3((l1 - w).mean() / (o - w).mean()), share_ci95=[f3(np.percentile(bs, 2.5)), f3(np.percentile(bs, 97.5))])
        N["a2_apachejit_W90"] = out
        pd.DataFrame(out).T.to_markdown(P / "tables" / "T8_A2_apachejit_W90.md")
    # A3: age strata (W=30): gain over wait_W30 by band, as share of the L1_W30 gain
    if (rv.analysis == "A3").any():
        res = []
        for fam, P_, exps in [("Cabral test", TEST, ["E3b"]), ("ApacheJIT", AJ, ["E8"])]:
            for metric in ["gmean", "auc"]:
                b = df[df.experiment.isin(exps) & df.project.isin(P_)].groupby(["variant", "project"])[metric].mean().unstack()
                w, l1 = b.loc["wait_W30", P_], b.loc["decomp_L1_W30", P_]
                a3 = _pp("A3", [x for x in rv.variant.unique() if str(x).startswith("strata_")], P_, metric)
                for band in ["strata_30_180", "strata_180_365", "strata_365_730", "strata_730_inf"]:
                    if band in a3.index and a3.loc[band].notna().sum() == len(P_):
                        g = a3.loc[band, P_] - w
                        res.append(dict(family=fam, metric="AUC" if metric == "auc" else "G-mean", age_band=band.replace("strata_", "").replace("_", "-") + " d",
                                        gain_over_wait30=f3(g.mean()), share_of_full_relabel_gain=f3(g.mean() / (l1 - w).mean()), projects_improved=int((g > 0).sum())))
        if res:
            A3 = pd.DataFrame(res); A3.to_markdown(P / "tables" / "T9_A3_age_strata.md", index=False); N["a3"] = res
    # A4: evaluation-window sensitivity (exclude last 730 days)
    if (rv.analysis == "A4").any():
        res = {}
        for fam, P_ in [("Cabral test", TEST), ("ApacheJIT", AJ)]:
            a4 = _pp("A4", [x for x in rv.variant.unique() if str(x).endswith("_gap730")], P_)
            if a4.notna().all(axis=None) and a4.shape[1] == len(P_):
                m_ = a4.mean(axis=1); w, l1, o = m_["wait_W30_gap730"], m_["decomp_L1_W30_gap730"], m_["oracle_gap730"]
                res[fam] = dict({k.replace("_gap730", ""): f3(v) for k, v in m_.items()}, share_W30=f3((l1 - w) / (o - w)))
        if res: N["a4_gap730"] = res; pd.DataFrame(res).T.to_markdown(P / "tables" / "T10_A4_eval_gap730.md")
    # A5: threshold rule on ApacheJIT (confirmatory, plan_v8 H9; Holm over 7)
    if (rv.analysis == "A5").any() and rv[rv.analysis == "A5"].shape[0] >= 450:
        a5 = _pp("A5", rv[rv.analysis == "A5"].variant.unique(), AJ); a5auc = _pp("A5", rv[rv.analysis == "A5"].variant.unique(), AJ, "auc")
        T11 = pd.DataFrame({"G-mean": a5.mean(axis=1), "AUC": a5auc.mean(axis=1)}).sort_values("G-mean", ascending=False)
        T11.to_markdown(P / "tables" / "T11_A5_threshold_apachejit.md", floatfmt=".3f")
        tests = [_cmp(a5.loc["law_lagakos_model_gmax_lat"], a5.loc["wait_W90"], "H9a: LAW+thr vs Wait-90"),
                 _cmp(a5.loc["law_lagakos_model_gmax_lat"], a5.loc["odasc_W30_d09_k50"], "H9a: LAW+thr vs ODaSC-style (lineage 2)")]
        for v in ["nowait", "wait_W30", "wait_W90", "law_lagakos_model", "odasc_W30_d09_k50"]:
            tests.append(_cmp(a5.loc[v + "_gmax_lat"], a5.loc[v], f"H9b: {v} +thr vs fixed"))
        ps = np.array([t["wilcoxon_p"] if t["wilcoxon_p"] is not None else 1.0 for t in tests]); o_ = np.argsort(ps); adj = np.empty_like(ps); run = 0
        for r_, i in enumerate(o_): run = max(run, (len(ps) - r_) * ps[i]); adj[i] = min(1.0, run)
        for t, a in zip(tests, adj): t["holm_p"] = float(a); t["pass_margin"] = bool(a < 0.05 and t["ci95"][0] > 0 and t["mean_diff"] >= 0.02)
        N["a5_tests"] = tests; N["a5_means"] = {k: dict(gmean=f3(v["G-mean"]), auc=f3(v["AUC"])) for k, v in T11.iterrows()}
        pd.DataFrame(tests).to_markdown(P / "tables" / "T11b_A5_tests.md", index=False)

# ---------------------------------------------------------------- bookkeeping numbers
vt = pd.read_csv(ROOT / "state" / "variants_tried.csv"); vta = pd.read_csv(ARCH / "state" / "variants_tried.csv")
N["variants_logged_main"] = int(len(vt)); N["variants_logged_independent_lineage"] = int(len(vta))
N["runs_main"] = int(len(df)); N["runs_independent_lineage"] = int(len(da))
b = json.load(open(ROOT / "state" / "budget.json")); N["cpu_hours_main"] = round(b.get("global_seconds", 0) / 3600, 1)
N["cpu_hours_independent_lineage"] = round(json.load(open(ARCH / "state" / "budget.json")).get("global_seconds", 0) / 3600, 1)
json.dump(N, open(R / "paper_numbers.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in N.items() if not k.endswith("tests") and "H6" not in k and "descriptive" not in k}, indent=0, default=float)[:6000])
