# Review round 1 — Reviewer R1 (methodology/statistics), verbatim

# Reviewer 1 report: methodology and statistics

**Manuscript:** "Where does verification latency hurt online just-in-time defect prediction? A label-noise decomposition on 23 projects"

**Overall score: 5 / 10**
**Recommendation: Major revision**

## Summary assessment

The paper asks a useful diagnostic question: is the verification-latency penalty in online JIT-SDP label noise or missing fresh data? It answers with a prequential simulation, a true-label decomposition and a fresh ApacheJIT replication. Several things are better than usual in this literature:
- one shared learner;
- frozen plans written before runs;
- negative results reported openly;
- a replication on a dataset family that was not touched during development.

I checked the code (`src/jit.py`) and found no leakage in the label-construction paths I read. The headline numbers are reproducible from `results/raw_results.jsonl`.

The central claim, however, is stated more broadly than the evidence allows. "The latency penalty is mostly label noise" holds for W = 30 in this design. It does not hold for the tuned W = 90 baseline. The decomposition is also measured with a threshold-dependent metric that the paper itself (RQ5) shows is dominated by operating-point shifts.

There are also problems with:
- disclosure of how many analysis branches used the Cabral test set;
- baseline fairness and consistency (two different "ODaSC-style" implementations give opposite conclusions);
- several factual or statistical misstatements.

All of these can be fixed, mostly with existing outputs or cheap reruns.

## Numbered concerns

### 1. [MAJOR] The "mostly label noise" claim holds only for W = 30. At the tuned W = 90 it is about half, and this number is computed but not reported.

`results/statistics.json` → `E3b_H3_decomposition.denoise_gap_share_W90 = 0.4977`, also in `paper_numbers.json`. The manuscript never states this share.

On Cabral test, true labels on the Wait-90 set recover only 0.654 → 0.684 of the gap to the oracle (0.715). My bootstrap 95% CI for that share is [0.27, 0.71]. In AUC it is 0.44 [0.33, 0.54].

With clean labels, the cost of excluding young commits is also not small:
- L1-W30 minus L1-W90 = 0.038 G-mean and 0.036 AUC.
- This is as large as the denoising gain at W = 90 (0.030).

So Section 5.2's statement that "excluding young negatives costs little" is contradicted by Table 3. The abstract, the C1 row, the RQ2 answer and the Conclusion generalise a W = 30 result to "the verification-latency penalty".

Wait-90 is the deployed, tuned rule. So the practically relevant penalty is roughly half noise and half freshness. ApacheJIT has no W = 90 decomposition at all.

*Resolution:*
- Report the W = 90 share with a CI in the abstract and in Table 3.
- Run L1/L2 at W = 90 (ideally the whole W grid) on ApacheJIT.
- Restate C1 as conditional on W, e.g. "for short waits the penalty is dominated by noise; at the G-mean-optimal W it is split roughly evenly".

### 2. [MAJOR] The decomposition uses fixed-threshold G-mean, which the paper shows is confounded by the operating point. The "share" is path-dependent and can exceed 1.

RQ5 argues that G-mean differences between label policies are largely threshold effects. Two observations from the result files:
- No-wait and Wait-90 have almost the same AUC on Cabral test (0.722 vs 0.727) but differ by 0.225 in G-mean.
- On neutron, Wait-30 has AUC 0.882 but G-mean 0.485 (`diag_law_neutron.json`).

So the G-mean gain of L1 over Wait-30 partly reflects the different class prior seen by a class-balanced learner at a fixed 0.5 threshold. The share of 1.08 (L1 above the oracle) is itself evidence that G-mean at 0.5 does not respect the oracle as an upper bound. In AUC, L1-W30 is 0.802 against an oracle of 0.815.

My recomputation from `raw_results.jsonl`:

| Family | AUC share (95% CI) | G-mean share (95% CI) |
|:--|:--|:--|
| Cabral test, W = 30 | 0.81 [0.74, 0.86] | 1.08 [0.995, 1.20] |
| ApacheJIT, W = 30 | 0.92 [0.89, 0.95] | 0.90 [0.86, 0.95] |

The qualitative W = 30 conclusion survives in AUC, but "108%" and "essentially all" do not.

The decomposition is also a single path (noise first, then freshness), and the two factors interact strongly:
- Adding fresh data with observed labels costs about −0.19 G-mean (Wait-30 0.620 → No-wait 0.429).
- Adding the same data with true labels costs about −0.007 (L1 0.722 → oracle 0.715).

A "share" is not well defined when the interaction is this large.

*Resolution:*
- Make AUC (and/or G-mean at each condition's best or deployable threshold) the primary decomposition metric.
- Present a 2×2 factorial (labels {observed, true} × training window {waited, all}) with main effects and interaction, or a Shapley-style decomposition, with CIs.
- Drop or heavily qualify shares above 1.

### 3. [MAJOR] The per-project share and the abstract's "9/9" claim are wrong for ApacheJIT.

The abstract says "0.90 on the 9 fresh ApacheJIT projects (9/9 projects, Holm p = 0.0078)". But L1-W30 vs Wait-30 on ApacheJIT is 8 wins / 1 loss (statistics.json `E8_secondary_H3_replication`). The 9/0 result belongs to L1 vs Wait-90.

On kafka, Wait-30 (0.7842) is already above the oracle (0.7835) and L1 is below Wait-30 (0.7837). The gap denominator is negative, so the reported per-project share of 0.75 is a ratio of two negative numbers. It is meaningless, and it sets the lower end of the reported range "0.75–0.983".

*Resolution:*
- Correct the abstract to 8/9.
- Report per-project absolute differences with CIs rather than ratios, or exclude or flag projects where |oracle − wait| is smaller than the seed SD.
- Report a CI for the pooled share, and note that Holm p refers to the paired test, not to the share.

### 4. [MAJOR] The Cabral test set was used by more branches than disclosed, so test-set multiplicity is understated.

The manuscript (Section 4.6, Threats) reports "two independent analysis lineages" and "98 logged configurations". But `experiments/plan_v7.yaml` states that the ten Cabral test projects "have been used by several parallel branches of this project (dreamy-fermat, zealous-lamport, keen-edison, magical-bardeen) ... with dozens of variants". `state/decisions.md` (lines 80–108) also names zen-cray, a river-based ODaSC reimplementation and LAT threshold policies in magical-bardeen, and keen-edison calibration grids.

Which lineage's results reach the paper was decided after those results existed. That is a forking-paths problem the reader cannot assess. In addition:
- The H3 Cabral confirmation and the RQ5 confirmation reused one test set.
- RQ5 has no fresh replication.

*Resolution:*
- Disclose every branch: which experiments each ran on the Cabral test projects, how many configurations, and outcomes, including the river-based ODaSC.
- State plainly that the Cabral confirmations are not untouched-holdout evidence.
- Treat ApacheJIT as the only confirmatory test, and run the RQ5 threshold rule (frozen) on ApacheJIT.

### 5. [MAJOR] Baseline fairness: the two "ODaSC-style" implementations differ, and the one not tested confirmatorily beats waiting 10/10 on Cabral.

The main lineage's ODaSC (`src/jit.py` l.179–195) differs from the independent lineage's (`archive/.../plan_v2.yaml`):

| | Main lineage | Independent lineage |
|:--|:--|:--|
| k | 20 | 50 |
| θ / δ | 0.8 | 0.9 |
| Features for kNN | log1p, **unstandardised** | standardised |
| Neighbour pool | all past training commits | 5,000 most recent |

The independent lineage's version reaches 0.695 on Cabral test (Table 7) against Wait-90 0.654. Per project (archive RESULTS_SUMMARY) it wins on all 10 projects, so Wilcoxon p ≈ 0.002. This comparison is never reported.

The main lineage's version, used for H6 on ApacheJIT, ties Wait-90. C3 ("feature-based denoising does not beat the waiting baselines") therefore depends on the implementation or the dataset, and the manuscript's framing hides this.

The tuning budget is also not equal:
- The main ODaSC never had k tuned (fixed at 20), and its selected θ = 0.8 sits on the edge of the grid.
- The authors' own Dual tuned k ∈ {20, 50}, and k = 50 was selected.
- LAW-M plus Dual add up to 8 configurations plus design iterations made after Cabral test results were seen (plan_v4 was written after cycle-1 test results).
- In the independent lineage, LAW+thr was chosen from 44 dev variants (journal "after 44 tries"), while ODaSC had about 5–10.
- "Every tuned method received at most five configurations" is therefore not accurate at the family level.

*Resolution:*
- Use one ODaSC implementation with standardised features and tune k ∈ {20, 50} × θ ∈ {0.8, 0.9, 0.95} × W (the same total budget as LAW-M + Dual).
- Rerun it on ApacheJIT and report both lineages' ODaSC numbers.
- Report the river-based reimplementation, or explain why it was dropped.
- Count tuning budget per method family, including design iterations.

### 6. [MAJOR] RQ5 confounds the threshold rule with the label policy, and its primary hypothesis failed.

The text says the threshold "turned LAW from a loser into a method that beats the waiting baselines". But the comparison is LAW **+thr** against Wait-90 and ORB-90 **without** the threshold.

The like-for-like comparison is Wait-30+thr (in the family), where the gain is +0.020, exactly at the non-triviality margin. Wait-90+thr was not in the confirmatory family. The independent-lineage ablation, although incomplete, suggests the threshold does most of the work: No-wait+thr is 0.718 against LAW+thr 0.734 on 3 projects.

The pre-registered primary comparison of that lineage (vs ODaSC-W30) failed (+0.0009, p = 0.77). The text calls this a "tie" but does not say it was the primary hypothesis.

The C4 claim about how much of the policy spread disappears at the best threshold rests on 2 development projects with one seed (Table 6).

*Resolution:*
- Compare every policy with and without the deployable threshold (2 × k design) on test and fresh data.
- State that the pre-registered primary RQ5 hypothesis was not supported.
- Compute the best-threshold and AUC spread on all 19 held-out and fresh projects from saved predictions, not only on 2 dev projects.

### 7. [MAJOR] Several pre-registration claims are inaccurate.

- The abstract says "All hypotheses and configurations were frozen before any held-out run". LAW-M, Dual and H6 were designed after Cabral test results (E1, E3b) were seen (plan_v4 header). The claim holds only for the ApacheJIT run.
- plan_v3 sets the H1 Holm family to six tests (LAW and AWT each vs {No-wait, Wait-90, ORB-90}), and plan_v2 says the family "counts all candidates tried on dev". The manuscript instead reports three-test families per method.
  - The pre-registered six-test values are in statistics.json as `holm_p_family6`, e.g. 0.0117 instead of 0.0059, and AWT vs ORB-90 0.148 instead of 0.0742.
  - Conclusions do not change, but the reported values deviate from the plan.
- H3 as pre-registered ("recovers ≥ 50%") is judged on a point estimate. No interval-based test of the share was planned or reported.
- Planned analyses that were silently dropped or left unfinished:
  - E7 (MSTDP protocol, plan_v6);
  - E5/E6 ablations and robustness (plan_v5);
  - E3 delay_scale = 2 robustness (partial: 3 projects, 11–15 runs);
  - E2 ablation (2–3 projects).

*Resolution:*
- Correct the abstract.
- Report the pre-registered six-test Holm values.
- Add a "deviations from plan" table listing every planned experiment, whether it was run, and why not.
- Either complete E3 robustness or report it as incomplete.

### 8. [MINOR] The Wilcoxon power statement is wrong.

Sections 4.4 and 7 say "With n = 9 the smallest two-sided Wilcoxon p-value for an 8/1 split is about 0.04". The exact minimum for an 8/1 split (loss at rank 1) is 2·2/512 = 0.0078, and a 9/0 split gives 0.0039. statistics.json itself shows p = 0.0078 for an 8/1 split (L1 vs Wait-30, ApacheJIT).

The real power limits are different:
- With Holm over 3 at n = 9, the smallest attainable adjusted p is 0.0117.
- Any 6/3 split cannot pass.

*Resolution:*
- Correct the statement.
- Add a sensitivity analysis giving the minimum detectable mean difference at n = 9/10 with the observed SD of paired differences (about 0.017–0.03) and the 0.02 margin. This makes clear whether H6's "failure" is informative.

### 9. [MINOR] Bootstrap CIs are not multiplicity-adjusted and are anti-conservative at n = 9/10, so CIs and Holm p-values disagree.

Examples:
- LAW vs ORB-90: CI [−0.091, −0.003] but Holm p = 0.168.
- Dual vs ODaSC: CI [0.003, 0.032] but Holm p = 0.164.
- LAW-M vs Wait-90: CI [0.003, 0.021] but Holm p = 0.164.

Readers will take these intervals as significant.

*Resolution:* use BCa or t-based intervals (or exact Hodges–Lehmann intervals matched to the Wilcoxon test), adjust them to the Holm family (e.g. Bonferroni-level intervals), and state the inconsistency explicitly.

### 10. [MINOR] The seeds add almost no replication.

Seed SDs per project are about 0.001–0.003 (my computation), because seeds affect only LightGBM subsampling. "5 confirmation seeds" therefore adds little information beyond n = 10 projects.

*Resolution:* say so, and consider additional sources of variation: random project-start offsets, different update intervals (50/100/200), or a second learner (e.g. Hoeffding tree or OOB, as in Cabral et al.). The latter also addresses the external-validity threat that "other learners could rank the policies differently".

### 11. [MINOR] The leakage test covers less than the text claims.

Section 4.5 says the test "covers every label policy and both threshold rules". `tests/test_no_future.py`:
- tests nowait, wait, orb, law, awt, lawm (soft) and odasc only;
- does not test `mode="dual"`;
- does not cover the threshold rules (`choose_threshold`, `gmax_lat`/`ratematch`), which live only in the archived lineage's code;
- uses one project prefix (fabric, 3,000 commits), one cut point and `eval_end_gap_days=0`;
- only perturbs `t_found`. A policy that read the final `y` of undiscovered commits directly would pass unless `t_found` also changed.

*Resolution:*
- Extend the test to dual and both threshold rules.
- Also permute or flip `y` for commits undiscovered at T0.
- Run it on several projects and cut points, including ApacheJIT.

### 12. [MINOR] The ORB baseline is not faithful to the original.

The "ORB" in this paper multiplies the class-balanced LightGBM weights by ORB boosting factors computed from a 100-prediction moving average. That double-corrects class imbalance and departs from the original online-bagging/Hoeffding-tree ORB. Calling it "ORB" invites direct comparison with Cabral et al.

*Resolution:* rename it ("ORB-style weighting"), add the no-class-balancing variant, and note the departure in the threats to validity.

### 13. [MINOR] The delay-estimator diagnostic is selective.

"The delay estimator is not the problem" quotes neutron at 60% of history. `diag_survival_dev.txt` shows clear underestimation at 30% of history:
- neutron S(90) = 0.307 vs true 0.459, and S(180) = 0.114 vs 0.301;
- sentry S(90) = 0.317 vs 0.429.

*Resolution:* report all time points and projects (a small table), or quantify the error across all updates.

### 14. [MINOR] Internal inconsistencies.

- Section 6.3 says AWT was "abandoned on development projects", yet AWT is a frozen test candidate in E1 and Table 4.
- "Lost to a tuned waiting rule by up to 0.34 G-mean on one project" compares against per-project W = 180 on neutron (0.838). Against the tuned W = 90 the gap is 0.29 (Wait-90) or 0.32 (ORB-90).
- Table 7 rows for Wait-90, ORB-90, No-wait and oracle are identical to Table 4. They are the same deterministic computation, not independent replications, and the caption should say so.

*Resolution:* fix the wording, and label the reused rows in Table 7.

### 15. [MINOR] Evaluation-label completeness and ApacheJIT construction.

Scoring excludes only the last 365 days, while P90 delays reach 2,811 days. So "final" labels in the evaluation window are themselves right-censored, and the bias interacts with policies that predict more positives.

In ApacheJIT, defective commits whose fix date precedes the commit date are treated as "discovered at commit time". Their number is not reported, and they give No-wait and Wait an immediate free positive label. ApacheJIT is also a curated sample, so the prequential cadence (one update per 100 *sampled* commits) is not a real deployment timeline.

*Resolution:*
- Report the count of such commits and rerun with them excluded.
- Add a sensitivity analysis excluding the last 730 or 1,095 days.
- Discuss the effect of sampled streams on the update schedule.

## Numbers spot-checked

| # | Claim in manuscript | Checked in | Match? |
|:--|:--|:--|:--|
| 1 | 331,937 commits (265,003 Cabral + 66,934 ApacheJIT) | T1_datasets.md (summed), paper_numbers.json | Yes |
| 2 | Median delay 16–568 d; P90 383–2811 d; 31%–83% found after 90 d | paper_numbers.json, T1 | Yes |
| 3 | RQ1: reduction 4.6%–33.2%, median 15.3%; excluded 4.8%–13.8%; <7 d 12.2%–26.2%; >2 y 0.1%–9.7% | paper_numbers.json (consistent with rounded T2 within rounding) | Yes |
| 4 | Dev decomposition: Wait-30 0.621 → L1 0.785, oracle 0.794 | raw_results.jsonl (E0/E0b: 0.6206 / 0.7854 / 0.7938) | Yes |
| 5 | Cabral test: Wait-30 0.620, L1 0.722, oracle 0.715, share 1.08, per project 0.849–1.36 | statistics.json E3b; raw_results (E3b, E1) | Yes |
| 6 | L1 vs Wait-90 +0.068 [0.049, 0.092] 10/0 Holm 0.0039; vs Wait-30 +0.102 [0.069, 0.141] | statistics.json E3b_H3 | Yes |
| 7 | ApacheJIT: 0.687 → 0.762, oracle 0.770, share 0.90, L1 vs Wait-90 +0.045 [0.029, 0.062] 9/0 Holm 0.0078 | statistics.json E8_secondary | Yes |
| 8 | Abstract: ApacheJIT "9/9 projects" for the gap recovery | statistics.json E8 (L1 vs Wait-30 is **8/1**); kafka gap is negative | **No** |
| 9 | Per-project ApacheJIT share 0.75–0.983 | statistics.json (values present, but the kafka ratio has a negative denominator, so it is meaningless) | Numerically yes, substantively invalid |
| 10 | L2-W30 0.702; L1-W90 0.684; L2-W90 0.625 | T3, raw_results E3b | Yes |
| 11 | W = 90 recovered share | statistics.json `denoise_gap_share_W90 = 0.4977` | **Omitted from manuscript** |
| 12 | LAW 0.616, −0.038 [−0.085, 0.001] 3/7 Holm 0.168; vs ORB −0.042 [−0.091, −0.003] 2/8 | statistics.json E1 | Yes (three-test family; six-test family per plan_v3 gives 0.252) |
| 13 | AWT vs ORB-90 −0.039 [−0.077, −0.009] 2/8 Holm 0.0742; both vs No-wait Holm 0.0059 | statistics.json | Yes for three-test families; pre-registered six-test values are 0.148 / 0.0117 |
| 14 | Table 4 means (G-mean / AUC / r1 / r0) | T4, paper_numbers.json rq3_means | Yes |
| 15 | H6: +0.0012 [−0.012, 0.012] 6/3 Holm 0.6016; vs ORB +0.0114 6/3 | statistics.json E8 (re-ran Wilcoxon: p = 0.5703) | Yes |
| 16 | Dual vs ODaSC +0.0175 [0.003, 0.032] 8/9, Holm 0.164 | statistics.json; re-ran Wilcoxon p = 0.0547 | Yes |
| 17 | Dev means: ODaSC 0.760, LAW-M 0.755, Dual 0.681; Dual collapsed on nova | raw_results E0c–E0e (0.7598 / 0.7551 / 0.6812; nova 0.475) | Yes |
| 18 | Table 5 metrics (all 8 rows) | T5, paper_numbers.json rq4_means | Yes |
| 19 | Neutron S(a) 0.867/0.696/0.462 vs 0.881/0.728/0.515; r1 0.10 in quarter 2; predicted-positive rate 0.04 vs 0.28; q 0.086 vs 0.061 | diag_survival_dev.txt (T@0.6), diag_law_neutron.json | Yes (but selective, see concern 13) |
| 20 | RQ5: LAW+thr 0.696; vs Wait-90 +0.042 [0.026, 0.058] 9/1 Holm 0.0195; vs ORB +0.038; vs ODaSC +0.0009 Holm 1.0 | archive/zealous_lamport_cycle1/results/statistics.json | Yes |
| 21 | Threshold lifts Wait-30 0.621 → 0.744, No-wait 0.385 → 0.688; rate-match 0.678 / 0.633 | archive RESULTS_SUMMARY.md (frozen_config dev_means) | Yes |
| 22 | Table 6 spreads (fabric 0.474–0.676 vs 0.668–0.717; neutron 0.246–0.819 vs 0.765–0.843) | T6, paper_numbers.json | Yes |
| 23 | "Minimum two-sided p for an 8/1 split at n = 9 is about 0.04" | Exact Wilcoxon; statistics.json E8 shows 0.0078 for 8/1 | **No** |
| 24 | "Leakage test covers every label policy and both threshold rules" | tests/test_no_future.py | **No** (no dual, no threshold rules) |
| 25 | "Two independent analysis lineages, 98 configurations" | plan_v7.yaml header; state/decisions.md lines 80–108 (at least 4–5 branches used the Cabral test set) | **Incomplete disclosure** |

## Bottom line

The W = 30 decomposition is a real and useful finding. It replicates in AUC on both dataset families (0.81 and 0.92 shares).

To be publishable, the paper must:
1. Narrow C1 to short waits, and report the W = 90 share (about 0.5) and the ApacheJIT W = 90 decomposition.
2. Make a threshold-free decomposition (AUC, or a factorial or Shapley design) primary.
3. Fix the "9/9", power and leakage-test misstatements.
4. Disclose all branches that touched the Cabral test set.
5. Unify, properly tune and re-confirm the ODaSC baseline, and report that the independent lineage's ODaSC beats Wait-90 on all 10 Cabral test projects.
6. Separate the threshold effect from the label-policy effect in RQ5.

No files were modified during this review.
