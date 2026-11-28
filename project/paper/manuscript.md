# What verification latency costs online just-in-time defect prediction, and where: a pre-registered study on two benchmarks

*Authors, affiliations, ORCID: to be completed by the authors.*

*Target journal: Journal of King Saud University – Computer and Information Sciences (Springer Nature).*

## Abstract

**Problem.** Online just-in-time software defect prediction (JIT-SDP) retrains a model as labels arrive. A commit's label is not known when it is made: a defect it introduced is only found later, when a fix points back at it. Every recent "clean" commit is therefore only provisionally clean, and the standard remedy is to wait W days before trusting a clean label.
**What existing approaches miss.** Methods for this problem propose new label policies (waiting, class re-weighting, confidence-based relabelling), but no study has measured where the cost of latency actually lies: in the decision threshold, in the label policy, or in the ranking learned from missing labels.
**What we did.** We started by proposing a latency-aware weighting (LAW) of provisionally clean commits, borrowed from delayed-feedback conversion modelling and fitted with a truncation-corrected discovery-delay estimator. We tuned it and six baselines on four development projects with equal budgets, froze it, and tested it on 10 held-out projects of the Cabral et al. benchmark and on 8 projects of ApacheJIT that no part of the study had touched, with five pre-fixed seeds.
**Key numbers.** LAW beat the waiting-time baselines on the Cabral test projects (+0.0417 G-mean over Wait-90, Holm p = 0.0195) but tied the strongest baseline, ODaSC (+0.0009, 95% CI [-0.0086, 0.0114]), and tied every baseline on ApacheJIT (+0.0052 vs ODaSC-W30, CI [-0.0208, 0.0295]). Its new component, the truncation-corrected delay estimator, had no measurable effect. Once the newest provisional negatives were handled by any reasonable mechanism, label policies fell within about 0.02 G-mean of each other, while an oracle with immediate labels stayed 0.05–0.06 ROC-AUC above. Revealing only the labels of commits younger than 30 days recovered a median 76% of that ranking gap on the Cabral test projects (labels older than 180 days: 6%), but only 34% on ApacheJIT, where commits are sparser and defects are found later.
**Implication.** The choice among existing label policies matters less than the literature's focus suggests; the remaining cost of latency is the missing labels of recent commits, and how much they matter depends on commit density and discovery speed. We report the failed method openly and release all code, configurations and per-run results.

## 1 Introduction

### 1.1 The problem

JIT-SDP flags risky commits at commit time so that reviewers can look at them first. In practice the model is trained online: every so often it is retrained on past commits, using whatever labels are known at that moment. The difficulty is that a defect-inducing commit is only recognised as such when a later bug fix is traced back to it. In the 14 projects of Cabral et al. (2019), we reconstructed discovery times and found median commit-to-discovery delays per project between 16 days (brackets) and 416 days (spring-integration). At any moment, many recent commits that look clean are in fact defect-inducing.

### 1.2 What people do, and what we expected to fix

The established remedy is a waiting time: a commit is trusted as clean only after W days (Cabral et al. 2019). ODaSC (Song et al. 2022) adds a feature-space confidence for those clean labels. Our first observation, from a model-free analysis of all 14 projects, was that waiting barely cleans the labels. Moving from W = 0 to W = 90 days lowered the share of training negatives that are truly defect-inducing only from 0.125 to 0.1193 for tomcat and from 0.0566 to 0.0442 for brackets (Table 1). Its main effect is to change what the recent training data look like: recent commits enter training only if they are already known to be buggy.

This suggested an idea from the delayed-feedback literature in online advertising (Chapelle 2014): keep every recent commit, but weight its provisional clean label by the probability that it is in fact an undiscovered defect, given its age and the distribution of discovery delays. We called this latency-aware weighting (LAW) and fitted the delay distribution with a reverse-time estimator for right-truncated data (Lagakos et al. 1988), because the long delays are only observable for old commits.

### 1.3 It did not work

We tuned LAW and all baselines on four development projects with equal budgets (44 configurations), froze the best LAW variant, and ran a confirmation on 10 held-out projects with five seeds fixed in advance. LAW beat the waiting-time family but tied ODaSC, the strongest baseline. The ablation showed that the truncation-corrected estimator, the one component we thought was new, changed nothing. A no-re-tuning replication on 8 ApacheJIT projects, which no part of the study had touched before, produced a tie with every baseline. Section 5 reports these failures in full.

### 1.4 What the failure taught us

Two observations from the failed method changed the question. First, most of LAW's apparent advantage on development data came from a latency-corrected decision threshold rather than from the weights, and giving the same threshold to the baselines closed most of the gap. Second, the oracle that sees true labels immediately was only about 0.02–0.04 G-mean above the best policies but 0.05–0.06 ROC-AUC above them: the remaining cost of latency is in how commits are ranked, not in where the cut-off is placed. We therefore asked which missing labels carry this ranking cost, and pre-registered the answer we expected from a development-set diagnostic before running it on the held-out data.

### 1.5 Contributions

1. A pre-registered negative result: a latency-aware weighting method adapted from delayed-feedback modelling, with a truncation-corrected delay estimator, does not beat the strongest existing baseline on two benchmarks (Tables 3 and 4). The estimator component has no measurable effect (Table 5).
2. Evidence that, once the newest provisional negatives are handled, the choice among existing label policies changes G-mean by about 0.02 or less on both benchmarks (Tables 3, 4 and 7).
3. A decomposition of the ranking cost of latency by label age (Table 6): on the Cabral test projects, the labels of the last 30 days recover a median 76% of the oracle gap and labels older than 180 days 6%; on ApacheJIT the pre-registered hypothesis fails, and an exploratory analysis links the difference to commit density and discovery speed (Table 8).
4. A model-free characterisation of waiting-time labelling on 14 projects (Table 1) and a full, re-runnable evaluation harness with every run's result file.

## 2 Related work

**Verification latency in online JIT-SDP.** Cabral et al. (2019) introduced the waiting-time labelling framework and the ORB method, which adds class-imbalance boosting. Cabral and Minku (2023) show that concept drift combined with latency impairs the stability of online JIT-SDP. Song, Minku and Yao (2023b) find that the waiting time has little effect on the validity of retrospective evaluation. These works design or evaluate label policies; they do not measure which missing labels carry the predictive cost.

**Label noise from latency.** ODaSC (Song et al. 2022) formulates the one-sided label noise created by waiting-time labelling and down-weights low-confidence clean labels using feature-space micro-clusters. It is the closest prior work and the strongest baseline here.

**Human labelling.** HumLa (Song et al. 2023) lets developers inspect commits the model flags, which removes latency for those commits. Liu et al. (2025) revisit it with non-zero inspection time and observed-label evaluation. Our development-only check of which commits to inspect (Section 6.4) found nothing better than their top-risk choice.

**Delayed feedback outside software engineering.** In conversion-rate prediction, Chapelle (2014) introduced the posterior weight p·S(a)/(1 − p + p·S(a)) that LAW uses; FSIW (Yasui et al. 2020), ES-DFM (Yang et al. 2021), DEFER (Gu et al. 2021), DEFUSE (Chen et al. 2022) and ULC (Wang et al. 2023) refine it. Gao and Yang (2022) train separate heads per delay window to trade freshness against correctness. In continual learning, Csaba et al. (2024) show that accuracy falls as label delay grows. These works motivate freshness, but none decomposes the cost of latency by label age on software data.

**Truncated delay estimation.** The reverse-time product-limit estimator for right-truncated data (Lagakos et al. 1988; Kalbfleisch and Lawless 1989) is standard in epidemiological nowcasting (Höhle and an der Heiden 2014).

**Recalibration under delayed labels.** A 2026 replication package (Zenodo record 24527309) compares recalibration against retraining for JIT-SDP under limited and delayed labels on ApacheJIT. Our threshold observation (Section 6.2) overlaps with its question and is not claimed as new.

**Claim → closest prior work → difference.**

| Claim | Closest prior work | Exact difference |
|---|---|---|
| C1 LAW improves online JIT-SDP | ODaSC (Song et al. 2022); DFM weight (Chapelle 2014) | Not supported; we report it as a negative result |
| C2 After handling the newest negatives, label policies differ by ≤ ~0.02 G-mean | Cabral et al. 2019; Song et al. 2022 (each compares a new policy against waiting) | We compare seven policies under the same tuned threshold on two benchmarks with pre-fixed seeds |
| C3 The ranking cost of latency is concentrated in the newest labels when commits are dense | Csaba et al. 2024 (delay hurts; rehearse samples similar to new data); Gao and Yang 2022 (per-window heads) | First per-age decomposition with partial oracles on JIT-SDP; shown to be benchmark-dependent |
| C4 Waiting barely denoises | Song, Minku and Yao 2023b (waiting time and evaluation validity) | Measures training-label noise by age rather than evaluation validity |

## 3 Problem formulation

Commits arrive in time order. Commit i, made at time t_i with change metrics x_i, has a final label y_i ∈ {0, 1}; if y_i = 1, the defect is discovered at time t_i + D_i. At an update time T the learner sees, for every earlier commit, the observed label 1[y_i = 1 and t_i + D_i ≤ T]. Commits with an observed 0 are provisionally clean. A label policy decides which past commits to train on and with which labels and weights. Predictions for commits made between two updates are made at commit time with the current model and a threshold, and are scored against final labels (prequential test-then-train).

**Label policies compared.** *Oracle*: true labels at once (upper bound). *Nowait*: observed labels at face value. *Wait-W*: positives as soon as found; negatives only when older than W days (Cabral et al. 2019). *ORB-W*: Wait-W with ORB class-weight boosting. *ODaSC-W*: Wait-W where a clean label with low confidence (from its k = 50 nearest labelled neighbours, a stand-in for ODaSC's DenStream micro-clusters) is counted as both classes. *LAW*: every provisionally clean commit of age a is split into a positive copy with weight q and a negative copy with weight 1 − q, q = p·S(a)/(1 − p + p·S(a)), where S(a) is the probability that a defect is still undiscovered at age a (estimated from discoveries seen before T, with the reverse-time estimator or naively) and p is the previous model's de-biased probability (model prior) or the mature defect rate (base prior).

**Thresholds.** Fixed 0.5, or *gmax_lat*: the threshold that maximises G-mean over the last 2000 scored commits, where not-yet-found commits receive a soft positive weight from S(a). Every baseline was offered the same threshold.

## 4 Experimental setup

**Data.** (i) The Cabral et al. (2019) artifact (Zenodo 2591761; sha256 in `literature/data_sha256.txt`): 14 GitHub projects with 14 change metrics, commit times and discovery times. Before any modelling, a seeded draw split them into dev = {fabric, neutron, nova, sentry} and test = the other 10. (ii) ApacheJIT (Keshavarz and Nagappan 2022; Zenodo 5907847): the 8 Apache projects with at least 2000 commits and at least one defect that do not overlap the Cabral test set (activemq, cassandra, flink, groovy, hbase, hive, ignite, kafka). Discovery time is the earliest linked fix date; the 'lt' metric is unavailable and set to 0. ApacheJIT is a curated sample of commits, not full histories.

**Learner and protocol.** Class-balanced LightGBM (150 trees, learning rate 0.05, 31 leaves), retrained every 100 commits after a 500-commit warm-up on the labels observable at that time. The last 365 days of each project are excluded from scoring so that final labels are reasonably complete. Features are log-transformed commit-time metrics; no statistic is fitted on future data (`tests/test_no_future.py` checks that future discoveries cannot change past predictions).

**Tuning budget.** On dev only, with seeds 0–2, we ran 44 configurations (528 runs): W ∈ {15, 30, 60, 90, 180} for Wait, ORB and ODaSC, each with and without the latency-corrected threshold, and 12 LAW variants. Every idea tried is logged in `state/variants_tried.csv`.

**Confirmation.** Seeds 100–104 were fixed before any run. The frozen comparison (plan_v3) ran on the Cabral test projects (E1–E3) and, without re-tuning, on ApacheJIT (E8). Hypotheses H5 (decomposition) and H6 (replication) were written in `experiments/plan_v4.yaml` before any ApacheJIT run; H9 in `plan_v5.yaml` before its runs.

**Statistics.** Per-project means over seeds; paired two-sided Wilcoxon signed-rank tests over projects; Holm correction within each family; 10,000-sample bootstrap 95% CIs of the mean paired difference. A difference counts as non-trivial at ≥ 0.02 G-mean (fixed in plan_v1). Metrics: G-mean of the per-class recalls (primary, as in Cabral et al. 2019), ROC-AUC, recalls, MCC.

**Hardware.** 4 CPU cores, 15 GB RAM, no GPU.

## 5 What did not work: the latency-aware weighting

### 5.1 Development results

On dev, LAW ranked commits best but decided worst. With a fixed threshold its mean dev G-mean was 0.6128 (model prior), below Wait-90 (0.7095) and ODaSC-W30 (0.7497), while its mean dev ROC-AUC was the highest. Adding the latency-corrected threshold lifted it to 0.7632 and lifted the baselines too (Wait-30: 0.6206 to 0.7437; nowait: 0.3855 to 0.6881). The best LAW variant led the best baseline by 0.0135 after 44 configurations, below our 0.02 margin. We froze it anyway rather than keep tuning.

### 5.2 Confirmation on the Cabral test projects

Table 3 shows the frozen comparison on 10 held-out projects with five seeds each.

**Table 3. Mean G-mean over the 10 Cabral test projects (seeds 100–104) and paired comparison with LAW.**

| Policy | G-mean | 95% CI | ROC-AUC | LAW − policy | CI of difference | Holm p |
|---|---|---|---|---|---|---|
| Oracle (upper bound) | 0.7148 | [0.691, 0.7398] | 0.8154 | — | — | — |
| LAW (frozen) | 0.6961 | [0.675, 0.7202] | 0.7506 | — | — | — |
| ODaSC-W15 + threshold | 0.6953 | [0.6711, 0.7208] | 0.764 | 0.0008 | [-0.005, 0.0067] | 1.0 |
| ODaSC-W30 (primary comparator) | 0.6952 | [0.6756, 0.7146] | 0.7621 | 0.0009 | [-0.0086, 0.0114] | 1.0 |
| Wait-W30 + threshold | 0.6759 | [0.6475, 0.7057] | 0.7445 | 0.0202 | [0.0115, 0.0289] | 0.0195 |
| ORB-W90 | 0.6584 | [0.6316, 0.6861] | 0.7241 | 0.0377 | [0.0216, 0.0511] | 0.0195 |
| Wait-W90 | 0.6544 | [0.6262, 0.682] | 0.7267 | 0.0417 | [0.0258, 0.0575] | 0.0195 |
| Nowait | 0.4291 | [0.3618, 0.4936] | 0.7222 | 0.267 | [0.2165, 0.3199] | 0.0117 |

LAW beat the waiting-time family on 9 of 10 projects but did not differ from ODaSC (Wilcoxon p = 0.7695). ODaSC also ranked commits better on these projects (ROC-AUC 0.7621 vs 0.7506). The primary hypothesis (≥ 0.02 over the best baseline, Holm p < 0.05) fails.

### 5.3 Replication on ApacheJIT

**Table 4. Frozen comparison on 8 ApacheJIT projects (seeds 100–104), no re-tuning.**

| Policy | G-mean | 95% CI | ROC-AUC | LAW − policy | CI of difference | Holm p |
|---|---|---|---|---|---|---|
| Oracle (upper bound) | 0.7627 | [0.7322, 0.7874] | 0.853 | — | — | — |
| LAW (frozen) | 0.7259 | [0.683, 0.7644] | 0.7893 | — | — | — |
| ODaSC-W15 + threshold | 0.7256 | [0.6923, 0.755] | 0.7914 | 0.0002 | [-0.0115, 0.0112] | 1.0 |
| Wait-W30 + threshold | 0.7219 | [0.6882, 0.7518] | 0.7873 | 0.004 | [-0.0071, 0.0149] | 1.0 |
| ODaSC-W30 | 0.7207 | [0.6898, 0.7478] | 0.7928 | 0.0052 | [-0.0208, 0.0295] | 1.0 |
| Wait-W90 | 0.7172 | [0.6733, 0.7541] | 0.789 | 0.0087 | [-0.0109, 0.028] | 1.0 |
| ORB-W90 | 0.7114 | [0.6784, 0.7423] | 0.7788 | 0.0145 | [-0.0097, 0.0374] | 1.0 |
| Nowait | 0.6551 | [0.6036, 0.7033] | 0.7709 | 0.0708 | [0.0315, 0.1144] | 0.0938 |

H6 fails: on fresh data LAW is indistinguishable from every baseline, including the waiting-time family it beat on the Cabral projects.

### 5.4 Ablation

{{E2_TABLE}}

## 6 What latency actually costs

### 6.1 Waiting barely denoises

**Table 1. Share of training negatives that are truly defect-inducing (averaged over update times), by waiting time (model-free; all 14 projects; `tables/rq1_waiting_time_tradeoff.csv`).** Selected projects:

| Project | W = 0 | W = 90 | W = 365 | History excluded at W = 90 |
|---|---|---|---|---|
| tomcat | 0.125 | 0.1193 | 0.108 | 0.048 |
| neutron | 0.1124 | 0.0993 | 0.0814 | 0.1022 |
| nova | 0.0686 | 0.0536 | 0.0325 | 0.0705 |
| brackets | 0.0566 | 0.0442 | 0.0262 | 0.1182 |
| spring-integration | 0.1288 | 0.1187 | 0.0992 | 0.0851 |

Most remaining false-clean commits are old ones whose defects take longer than W to surface. Waiting mainly changes the class composition of recent training data, which explains why its effect on G-mean is largely an operating-point effect.

### 6.2 Label policies converge once the newest negatives are handled

On the Cabral test projects the four policies that handle the newest negatives (LAW, ODaSC-W30, ODaSC-W15 with threshold, Wait-W30 with threshold) span 0.6759 to 0.6961 G-mean (Table 3). On ApacheJIT, seven thresholded policies span 0.7115 to 0.7259 (Table 7). The latency-corrected threshold itself was decisive only for the policy that keeps the newest negatives at face value: on ApacheJIT it raised nowait by 0.0564 (CI [0.0236, 0.0934], 8/8 projects, Holm p = 0.0312) and changed Wait-90, ORB-90 and ODaSC-30 by less than 0.005 (H9a fails; Table 7).

**Table 7. Effect of the latency-corrected threshold on ApacheJIT (E10 + E8; seeds 100–104).**

| Label policy | Fixed 0.5 → corrected threshold (mean gain) | 95% CI | Wins / 8 | Holm p | Thresholded G-mean |
|---|---|---|---|---|---|
| Nowait | 0.0564 | [0.0236, 0.0934] | 8 | 0.0312 | 0.7115 |
| Wait-W90 | 0.0049 | [-0.01, 0.0243] | 4 | 1.0 | 0.7221 |
| ORB-W90 | 0.0002 | [-0.0083, 0.0092] | 4 | 1.0 | 0.7116 |
| ODaSC-W30 | 0.0045 | [-0.0114, 0.0207] | 4 | 1.0 | 0.7252 |
| LAW (model prior) | -0.0006 | [-0.0192, 0.0152] | 5 | not in family | 0.7259 |

### 6.3 The ranking cost sits in the newest labels — on one benchmark

To locate the remaining cost, we re-ran the simulation with partial oracles that reveal true labels only for commits younger (or older) than H days at each update, and expressed each as the share of the nowait-to-oracle ROC-AUC gap it recovers. On dev (three projects, one seed) the last 30 days recovered about 81% and labels older than 180 days about 5%. We pre-registered H5 (young-30 recovers ≥ 50% and old-180 ≤ 20% for the median project of each benchmark) and ran it on all 18 held-out projects with five seeds.

**Table 6. Share of the nowait→oracle ROC-AUC gap recovered by partial oracles (median over projects; E7, seeds 100–104).**

| Benchmark | Median gap (AUC) | Young < 30 d | Young < 180 d | Old > 30 d | Old > 180 d | H5 |
|---|---|---|---|---|---|---|
| Cabral test (10) | 0.0906 | 0.7559 | 0.9383 | 0.2876 | 0.0554 | supported |
| ApacheJIT (8) | 0.0829 | 0.3431 | 0.776 | 0.6024 | 0.0909 | refuted |

On the Cabral test projects, revealing the last 30 days beat revealing everything older than 180 days by 0.058 ROC-AUC (95% CI [0.0425, 0.0724], 10/10 projects, Wilcoxon p = 0.002). On ApacheJIT the same contrast was 0.0045 (CI [-0.0236, 0.0294], p = 0.7422), and on activemq and groovy the last 30 days recovered nothing.

**An exploratory explanation (formed after seeing these results).** ApacheJIT is a curated sample: its projects have 24–169 commits per 30 days against 72–248 in the Cabral projects, and only 10–33% of their defects are found within 30 days against 18–57% (Table 8). Across all 18 projects, the share recovered by the young-30 labels correlates with commit density (Spearman ρ = 0.69, p = 0.002) and with the share of defects found within 30 days (ρ = 0.70, p = 0.001), but not with the defect rate (ρ = -0.22, p = 0.38). Our reading is that what matters is how many informative labels a recent window holds, not calendar age. We could not test this on untouched data and state it as a conjecture.

**Table 8. Benchmark profile (`tables/E7_diag_benchmark_profile.csv`).** Commits per 30 days, median discovery delay (days) and share of discovered defects found within 30 days, per project.

| Project | Commits | Commits per 30 d | Defect rate | Median delay (d) | Found within 30 d | Young-30 recovery |
|---|---|---|---|---|---|---|
| brackets | 17310 | 248.2 | 0.234 | 16.0 | 0.571 | 0.8971 |
| broadleaf | 14910 | 139.6 | 0.169 | 45.0 | 0.456 | 0.7686 |
| camel | 30517 | 234.2 | 0.205 | 29.0 | 0.505 | 0.7763 |
| jgroups | 18316 | 106.3 | 0.172 | 117.0 | 0.351 | 0.7432 |
| matplotlib | 19061 | 195.0 | 0.161 | 115.0 | 0.36 | 0.3908 |
| npm | 7892 | 81.1 | 0.178 | 104.0 | 0.288 | 0.7933 |
| spring-integration | 8691 | 71.8 | 0.268 | 416.0 | 0.183 | 0.597 |
| tomcat | 18877 | 132.7 | 0.276 | 196.0 | 0.313 | 0.6298 |
| wagtail | 8103 | 133.0 | 0.123 | 87.0 | 0.347 | 0.7387 |
| zulip | 18465 | 236.6 | 0.244 | 82.0 | 0.355 | 0.8066 |
| aj_activemq | 6126 | 36.0 | 0.229 | 568.3 | 0.113 | -0.0461 |
| aj_cassandra | 8159 | 62.2 | 0.382 | 142.3 | 0.21 | 0.5918 |
| aj_flink | 11691 | 106.4 | 0.24 | 95.9 | 0.224 | 0.4555 |
| aj_groovy | 8059 | 40.6 | 0.2 | 561.2 | 0.099 | -0.1141 |
| aj_hbase | 8730 | 56.4 | 0.433 | 137.0 | 0.231 | 0.2909 |
| aj_hive | 6842 | 49.8 | 0.617 | 97.2 | 0.276 | 0.4612 |
| aj_ignite | 12036 | 169.1 | 0.203 | 128.8 | 0.229 | 0.3528 |
| aj_kafka | 2384 | 23.9 | 0.468 | 67.1 | 0.334 | 0.3335 |


### 6.4 Inspection budgets (development only)

Because the newest labels mattered on development data, we tested whether a small budget of developer inspections at commit time helps, and which commits to inspect (E9; dev projects, seeds 0–2, 18 variants). Inspecting the top-risk commits, as HumLa does, was at least as good as inspecting the commits nearest the threshold for every base policy (pre-registered H7 refuted), and the best 5% budget raised mean dev ROC-AUC by 0.0112–0.0234, less than the 0.0328 spread between label policies without inspection (H8 refuted). We did not take any inspection variant to confirmation.

## 7 Robustness

{{E3_TEXT}}

## 8 Threats to validity and limitations

- **Construct.** Labels come from SZZ-style fix linking in both benchmarks; defects never fixed, or fixed without a link, remain labelled clean. Discovery times on ApacheJIT come from the earliest linked fix date, and its 'lt' metric is missing.
- **Benchmark dependence.** Our main positive finding (C3) holds on one benchmark and fails on the other. The density explanation was formed after seeing the data and is untested.
- **Internal.** ODaSC is re-implemented with a kNN stand-in for DenStream micro-clusters; the original may behave differently. All baselines received the same tuning budget and the same threshold option.
- **Statistical.** With 8–10 projects, a Wilcoxon test cannot reach very small p-values, and a 0.02 G-mean difference is near the detection limit. We counted 18 E9 variants, 44 dev configurations and every confirmation variant (`state/variants_tried.csv`).
- **External.** Only open-source projects; ApacheJIT samples commits rather than full histories; one learner (LightGBM).
- **Re-use of test projects.** The 10 Cabral test projects were used for the frozen confirmation (E1) and afterwards for the pre-registered decomposition (E7). E7 tests a different hypothesis, but these projects are no longer untouched.

## 9 Conclusion

We set out to make online JIT-SDP cope better with verification latency by weighting provisionally clean commits, and it did not work: on two benchmarks the method tied the strongest existing baseline, and its new estimator did nothing. The failure pointed elsewhere. Once the newest provisional negatives are handled, the choice among existing label policies changes G-mean by about 0.02 at most, and what remains is a ranking cost from labels the model does not yet have. Where commits are dense and defects are found quickly, that cost lies almost entirely in the labels of the last month; where they are not, it does not. Methods for this problem should be judged against a policy that handles the newest negatives with a latency-aware threshold, and against the oracle's ranking gap, rather than against a fixed waiting time.

## Declarations

- **Data availability.** Both datasets are public (Zenodo 2591761 and 5907847). All per-run results (`results/raw_results.jsonl`), configurations, seeds and code are in the replication package.
- **Code availability.** To be completed by the authors (repository URL / archive DOI).
- **Compute.** All runs used CPU only; the compute ledger is in `state/budget.json`.
- **Use of AI assistance.** This study, its code and this draft were produced with an AI research agent under the authors' supervision; to be completed and verified by the authors.
- **Funding, competing interests, ethics, author contributions.** To be completed by the authors.

## References

- Cabral, G. G., Minku, L. L., Shihab, E., Mujahid, S. (2019). Class imbalance evolution and verification latency in just-in-time software defect prediction. ICSE 2019. https://doi.org/10.1109/ICSE.2019.00076
- Cabral, G. G., Minku, L. L. (2023). Towards reliable online just-in-time software defect prediction. IEEE TSE. https://doi.org/10.1109/TSE.2022.3175789
- Chapelle, O. (2014). Modeling delayed feedback in display advertising. KDD 2014. https://doi.org/10.1145/2623330.2623634
- Chen, Y., et al. (2022). Asymptotically unbiased estimation for delayed feedback modeling via label correction (DEFUSE). WWW 2022. https://doi.org/10.1145/3485447.3511965
- Csaba, B., et al. (2024). Label delay in online continual learning. NeurIPS 2024. https://arxiv.org/abs/2312.00923
- Gao, H., Yang, Y. (2022). Multi-head online learning for delayed feedback modeling. arXiv:2205.12406. https://arxiv.org/abs/2205.12406
- Gu, S., et al. (2021). Real negatives matter: continuous training with real negatives for delayed feedback modeling (DEFER). KDD 2021. https://doi.org/10.1145/3447548.3467086
- Höhle, M., an der Heiden, M. (2014). Bayesian nowcasting during the STEC O104:H4 outbreak in Germany, 2011. Biometrics. https://doi.org/10.1111/biom.12194
- Kalbfleisch, J. D., Lawless, J. F. (1989). Inference based on retrospective ascertainment. JASA. https://doi.org/10.1080/01621459.1989.10478780
- Keshavarz, H., Nagappan, M. (2022). ApacheJIT: a large dataset for just-in-time defect prediction. MSR 2022. Data: https://doi.org/10.5281/zenodo.5907847
- Lagakos, S. W., Barraj, L. M., De Gruttola, V. (1988). Nonparametric analysis of truncated survival data, with application to AIDS. Biometrika. https://doi.org/10.1093/biomet/75.3.515
- Liu, X., Zhou, Y., Tang, Y., Qian, J., Zhou, Y. (2025). Human-in-the-loop online just-in-time software defect prediction: what have we achieved and what do we still miss? Sci. Comput. Program. 244:103296. https://doi.org/10.1016/j.scico.2025.103296
- Song, L., Li, S., Minku, L. L., Yao, X. (2022). A novel data stream learning approach to tackle one-sided label noise from verification latency (ODaSC). IJCNN 2022. https://doi.org/10.1109/IJCNN55064.2022.9891911
- Song, L., Minku, L. L., Teng, X., Yao, X. (2023). A practical human labeling method for online just-in-time software defect prediction (HumLa). ESEC/FSE 2023. https://doi.org/10.1145/3611643.3616307
- Song, L., Minku, L. L., Yao, X. (2023b). On the validity of retrospective predictive performance evaluation procedures in just-in-time software defect prediction. EMSE. https://doi.org/10.1007/s10664-023-10341-8
- Wang, Y., et al. (2023). Unbiased delayed feedback label correction for conversion rate prediction (ULC). KDD 2023. https://doi.org/10.1145/3580305.3599536
- Yang, J., et al. (2021). Capturing delayed feedback in conversion rate prediction via elapsed-time sampling (ES-DFM). AAAI 2021. https://doi.org/10.1609/aaai.v35i5.16587
- Yasui, S., et al. (2020). A feedback shift correction in predicting conversion rates under delayed feedback (FSIW). WWW 2020. https://doi.org/10.1145/3366423.3380032
- Replication package: Recalibration vs. retraining for JIT defect prediction under limited and delayed labels (2026). Zenodo. https://doi.org/10.5281/zenodo.24527309
