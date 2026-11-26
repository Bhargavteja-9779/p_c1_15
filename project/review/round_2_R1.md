# Review round 2 — Reviewer R1 (methodology/statistics), verbatim (simulated reviewer: AI agent with fresh context)

# Referee report (methodology and statistics), round 2

**Manuscript:** "Where does verification latency hurt online just-in-time defect prediction? A label-noise decomposition on 23 projects" (v2)

**Overall score: 6/10**
**Recommendation: Major revision.** Most fixes are to the text. One extra diagnostic run is recommended.

## Summary

The revision is a real improvement:
- There is now a 2×2 factorial with a Shapley split and bootstrap CIs.
- AUC is the primary metric for the decomposition.
- W = 90 is decomposed on both families.
- Thresholds are compared like for like on fresh data (H9b).
- The power statement is now correct, the test-set reuse scan is disclosed, and a deviations table has been added.

I recomputed the cell means, the Shapley effects, the age-strata shares, the Wilcoxon and Holm values and the Table 1 statistics from the raw files (`results/raw_results.jsonl`, `results/review1/raw.jsonl`, the per-job `results/E8_*.json`, `data/*.pkl`, and the archive `statistics.json`). Every number I checked matches; I found no transcription errors (table below).

The remaining problems are about how strongly things are claimed:
1. A highlight and the abstract contradict the paper's own fresh-data results on age-only corrections.
2. The localisation claim ("mainly caused by 30–180-day commits") rests on a single-band design that is strongly non-additive on ApacheJIT.
3. The abstract and conclusion quote the Shapley share at W = 90, which flatters labels, while the path share for that cell is 0.44.
4. Metric choice is inconsistent across RQs: AUC for RQ2, G-mean for RQ3. In AUC, the age-only method beats the waiting baseline.
5. The AUC/Shapley/W = 90/strata reanalyses of ApacheJIT were planned after the ApacheJIT cells were known. They are still called the "confirmatory" test of RQ2.

## Status of round-1 MAJOR concerns (R1)

| R1 # | Status | Evidence |
|:--|:--|:--|
| 1 (W = 90 share) | **Partly resolved** | The body reports path share 0.44 [0.33, 0.54] and Shapley share 0.74. The abstract and conclusion give only the Shapley 0.74/0.97 (see concern 3). |
| 2 (fixed-threshold G-mean, path dependence) | Resolved, with interpretation caveats | Table 4 matches `shapley.json`. See concern 3. |
| 3 ("9/9", kafka) | Resolved | 8/1 is stated; kafka is flagged. |
| 4 (test-set reuse) | **Mostly resolved** | S3 leaves out the review-round A3/A4 runs on Cabral test. ApacheJIT reuse is understated (concerns 5 and 9). |
| 5 (ODaSC fairness) | **Partly resolved** | Both adaptations are reported, and declining to retune on used test sets is defensible. But the new claim "depends on implementation" has no supporting evidence (concern 6). |
| 6 (RQ5 confound) | Resolved for fresh data | H9b numbers verified. The "much of the spread is operating point" claim still rests on 2 dev projects × 1 seed (concern 10). |
| 7 (pre-registration) | Mostly resolved | Six-test Holm values verified (0.252/0.252/0.148/0.0117). Table 12 omits the post hoc additions (concern 5). |

## Numbered concerns

### 1. [MAJOR] The age-only claim in the highlights and abstract is contradicted by the paper's own fresh data and by its primary metric

- **Highlight 4** says: "Age-only and feature-based corrections do not beat a 90-day wait **on fresh data**." No age-only method was a planned comparator on ApacheJIT. The only fresh evidence is A5, where LAW (model prior, threshold 0.5) has the **highest** mean: 0.732 vs Wait-90 0.716 (Table 10).
  - My recomputation from `review1/raw.jsonl`: +0.0151, bootstrap CI [0.004, 0.029], 7/2, unadjusted p = 0.039.
  - That is the same strength of evidence the paper calls a "tie" for LAW-M (+0.0113 [0.003, 0.021], 7/2, p = 0.055).
- **The abstract's "Age-only corrections do not beat a 90-day wait"** is a G-mean@0.5 statement on the reused Cabral set only.
  - In AUC, the metric the paper declares primary because G-mean@0.5 "mixes ranking with operating-point shifts", LAW beats Wait-90 on Cabral test: 0.751 vs 0.727, +0.024, 7/3, unadjusted p = 0.027.
  - In AUC on Cabral, Wait-30 also beats Wait-90 (+0.018, 8/2, p = 0.020).
  - So the RQ3 "No" is exactly the kind of operating-point claim RQ5 warns against.
- **Resolution:**
  - Remove "on fresh data" for age-only corrections from the highlight.
  - State RQ3 as "at the 0.5 operating point on the reused Cabral set".
  - Report AUC alongside G-mean in the RQ3 text and say that LAW ranks better than Wait-90.
  - Report the A5 LAW-vs-Wait-90 descriptive difference symmetrically with LAW-M.

### 2. [MAJOR] The localisation claim ("mainly caused by defects one to six months old"; "older commits add nothing") is stronger than the single-band design allows

Recomputed from A3 (all values match Table 5):
- **ApacheJIT AUC.** Relabelling 30–180 d recovers only 0.489 of the L1 gain. The four single-band shares sum to **0.368** (0.394 in G-mean). Most of the gain comes only from relabelling across bands jointly.
  - With that much non-additivity, a "band-in" design cannot show that older bands "add nothing". They may matter only together with the 30–180 band.
  - Relabelling ≥ 730 d *hurts* G-mean on ApacheJIT (1/9 improved, p = 0.027).
- **Cabral.** The bands are not additive either (AUC shares sum to 1.094). The manuscript says non-additivity occurs only "on ApacheJIT" (Section 5.2).
- **Cabral 365–730 d.** This band is small but consistent (+0.004 AUC, 9/10, p = 0.0059). "Adds nothing" (Contribution 2, Section 6.1, Conclusion) overstates this.
- **Which wait.** The strata were run only at W = 30. The practical recommendation is made for the tuned W = 90, where commits aged 30–90 d are not in the training negatives at all.
- **Status.** plan_v8 labels A3 "exploratory diagnostic", yet it drives the abstract's Conclusion sentence.
- **Resolution:**
  - Restate the conclusion as "on Cabral most of the gain comes from 30–180-day commits; on ApacheJIT this band gives about half and the bands interact".
  - Add a leave-one-band-out run (true labels everywhere except band b), at least at W = 30 and ideally at W = 90.
  - Fix the "only on ApacheJIT" sentence.
  - Drop "adds nothing" and "do not matter".

### 3. [MAJOR] The abstract and conclusion report the order-dependent label share selectively

- At W = 90 on Cabral (AUC), the interaction (0.054) is larger than the freshness main effect (0.023). The label share therefore depends on the order of the two factors:
  - noise-first path: 0.44 [0.33, 0.54];
  - Shapley: 0.74;
  - freshness-first path ((Oracle − No-wait)/gap): 1.05 (my computation).
- The abstract quotes the **path** share at W = 30 (0.81/0.92) but the **Shapley** share at W = 90 (0.74/0.97), so readers will compare unlike quantities.
- The deployment-relevant counterfactual, "fix the labels of the Wait-90 training set I actually have", is the path share of 0.44: less than half.
- The conclusion's "still the larger part (0.74 and 0.97)" does not hold under that counterfactual.
- Also, W = 90 is "tuned" for G-mean. On dev, AUC is flat across W (0.785–0.794, `raw_results` E0). On Cabral test, Wait-90 has lower AUC than Wait-30 (0.727 vs 0.745), so much of the W = 90 "freshness" effect (+0.023) is the AUC cost of the G-mean-chosen wait.
- **Resolution:**
  - In the abstract and conclusion, give both path and Shapley shares (or the range 0.44–1.05) for W = 90.
  - Use the same quantity for W = 30 and W = 90.
  - Note that W = 90 is G-mean-optimal, not AUC-optimal.

### 4. [MAJOR] The 2×2 does not cleanly separate "noise" from "freshness"

- In the observed-label row, the window factor adds young commits with mostly wrong (provisionally clean) labels. In the true-label row, it adds them correctly labelled. The "freshness" contrast is therefore partly a label contrast by construction.
- This is why the interaction is positive in all 8 cells. The Shapley 50/50 split of the interaction is a convention, not a measurement.
- The L2 cell is a selection-biased training set, because it adds only the young *defective* commits. It shows this directly: L2 < L1 (Cabral W = 30, AUC 0.782 vs 0.802; Table 3, W = 90 G-mean 0.625 vs 0.684). L2 is reported but never interpreted.
- Section 5.2's "Excluding the youngest 30 days of data costs nothing" averages −0.022 (observed labels) and +0.014 (true labels, Oracle − L1, Cabral AUC).
- **Resolution:**
  - Say explicitly that the freshness factor is confounded with label state.
  - Report the two simple effects of the window factor (−0.022 / +0.014) instead of "costs nothing".
  - Explain or drop L2.

### 5. [MAJOR] ApacheJIT is called "the only confirmatory test of RQ2", but the RQ2 analyses on it were designed after its cells were known

- plan_v7 pre-registered only the G-mean H3-style secondary analysis on ApacheJIT (L1-W30 vs Wait-30/90).
- plan_v8 A1 (Shapley) is a re-analysis of the existing E8 cells ("no new runs"), planned only for W = 30.
- The W = 90 Shapley split, the choice of AUC as primary metric, A2 and A3 were added afterwards. A2 and A3 are labelled "exploratory diagnostic" in plan_v8.
- Section 4.6 says "ApacheJIT, run once per plan". In fact it was used under plan_v7 (E8) and plan_v8 (A2–A5), and plan_v8 itself says "second use disclosed".
- Table 12 does not list: AUC made primary after the fact; the W = 90 Shapley not in plan_v8 A1; ApacheJIT second use.
- **Resolution:**
  - Label the RQ2 AUC/Shapley/W = 90/strata results on ApacheJIT as post hoc or exploratory.
  - Keep "confirmatory" for the plan_v7 G-mean tests, H6 and H9.
  - Add the three deviations to Table 12.

### 6. [MAJOR] "Depends on the implementation" (C4 row, Contribution 4, RQ4 answer) is not supported

- The main-lineage ODaSC was never run on Cabral test: `raw_results` E1 has no odasc variant, and S3 lists odasc only for dreamy-fermat.
- On ApacheJIT, the only dataset where both implementations ran, they give identical means (0.718 vs 0.718). The per-project differences range from −0.028 to +0.025 (my comparison of `odasc_W30_d09_k50@A5` against `odasc_W30_t0.8`).
- No dataset therefore shows the two implementations disagreeing. The pattern is fully explained by dataset (or by test-set selection on Cabral).
- The abstract's plural "Feature-based denoisers beat it on the reused Cabral test set" rests on one non-pre-registered implementation. LAW-M and Dual were never run on Cabral test.
- **Resolution:**
  - Restate as "one adaptation beat Wait-90 on the reused Cabral set; on fresh data both adaptations tie".
  - Remove "and implementation".
  - Make "denoisers" singular in the abstract.

### 7. [MINOR] The RQ5 "distorted vs well-calibrated" split is post hoc and not measured on ApacheJIT

- The abstract and RQ5 answer say the threshold "repairs policies with a distorted class prior". Only No-wait passes Holm (0.027); Wait-30 does not (0.234).
- LAW is called "well-calibrated", but Table 8 shows LAW (model prior) predicting 0.094 positives against a true 0.256 on neutron, and on Cabral the threshold helped LAW (E2 ablation, +0.069, 4 projects).
- My rough predicted-positive rates on ApacheJIT, computed from r0/r1 and the defect rate (true rate 0.39):

| Policy | Predicted-positive rate |
|:--|:--|
| No-wait | 0.25 |
| Wait-30 | 0.30 |
| Wait-90 | 0.38 |
| LAW | 0.43 |
| ODaSC | 0.47 |

  ODaSC over-predicts, yet the threshold does nothing for it.
- **Resolution:**
  - Report predicted-positive versus true rates per policy on ApacheJIT.
  - Define "distorted" before looking at the threshold effect.
  - Use "a policy" (singular) where only No-wait is significant.

### 8. [MINOR] Wording about RQ1 that round 1 asked to fix is still in the highlights

- Highlight 1: "Waiting 90 days removes only a median 15.3% of false-clean training labels." The quantity is actually the relative drop in the false-clean **share of negatives** (`rq1_label_noise.json`), not the share of false-clean labels removed. Round 1 (R2 #8) flagged this and the response says it was fixed.
- The RQ1 answer ("removes few of the false-clean labels") has the same problem.
- **Resolution:** reword, or compute the actual fraction of false-clean labels removed.

### 9. [MINOR] The test-set usage disclosure is incomplete

- S3 (`scripts/test_set_usage.py`) "covers committed results" from before the review round. It does not include the review-round Cabral-test runs: A3 (4 strata configurations × 10 projects × 5 seeds) and A4 (5 configurations × 2 seeds).
- "27 configurations run in full" counts E2/E3 rows with only 2–5 projects as "full".
- **Resolution:** regenerate S3 with A3/A4, and say "complete runs (all projects)" or give project counts.

### 10. [MINOR] The operating-point claim still rests on dev data

- "Much of the G-mean difference between latency policies is an operating-point effect" (RQ5 answer) rests on 2 dev projects × 1 seed (Table 8).
- The held-out data already supports it more strongly, at no extra cost. On Cabral test the AUC range across non-oracle policies is 0.699–0.751, against a G-mean range of 0.429–0.658 (Table 6).
- **Resolution:** add the held-out and fresh AUC versus G-mean spreads, as R1 #6 asked.

### 11. [MINOR] The leakage-test description overstates coverage

- Section 4.5 says the hidden-discovery test covers "the decomposition" and runs on "a Cabral and an ApacheJIT project".
- In `tests/test_no_future.py`:
  - the hidden-discovery test excludes `decomp` and uses only fabric;
  - only the y-flip test uses `aj_kafka`, and it excludes decomp by design.
- **Resolution:** correct the text, or add decomp and an ApacheJIT project to the first test.

### 12. [MINOR] Count of never-discovered defective Cabral commits

- The text gives 991 unmatched copies, as if that were the number of defective commits without a discovery time.
- From `data/*.pkl` I count **1,188** defective Cabral commits with `t_found = inf`. For example, brackets has 4,045 buggy commits but only 4,037 copy rows (`cabral_copy_rows_vs_mstdp.json`), so some defective commits have no copy row at all.
- **Resolution:** report both numbers.

### 13. [MINOR] Small points

- **A4 seeds.** A4 uses 2 seeds (plan_v8). The manuscript does not say so.
- **Power statement.** The 0.02 minimum detectable effect is for unadjusted α = 0.05. Under H6's Holm-over-2 it is about 0.023. State this.
- **"Bound".** RQ4 and Section 6.1 call L1-W30 (0.762) the "true-label bound" for deployable methods. The relevant bound is the oracle (0.770); L1 is one specific counterfactual.
- **IFA.** IFA means (Wait-90 13.756) are dominated by outliers. Report medians.
- **Freshness wording.** The abstract's "contributes nothing" for the W = 30 freshness effect: the Cabral CI [−0.008, −0.000] excludes zero, so "slightly negative" is more accurate.

## Numbers spot-checked (recomputed from raw files unless noted)

| # | Manuscript value | Source / recomputation | Match |
|:--|:--|:--|:--|
| 1 | 331,937 commits; 265,003 / 66,934 | `data/*.pkl` row counts | yes |
| 2 | Median delay 16–568 d; P90 383–2811 d | recomputed from `t_found − t` | yes |
| 3 | Share found after 90 d 0.312–0.722 / 0.430–0.826; defect rates | recomputed | yes |
| 4 | RQ1 reduction 4.6%–33.2%, median 15.3%; excluded 4.8%–13.8% | `rq1_label_noise.json` (0.046–0.333, median 0.1535) | yes (rounding) |
| 5 | Dev: Wait-30 0.621 → L1 0.785, oracle 0.794 | `raw_results` E0/E0b | yes |
| 6 | Table 3 Cabral cells (0.620/0.722/0.702/0.654/0.684/0.625/0.429/0.715) | E1 + E3b | yes |
| 7 | Table 3 ApacheJIT cells (0.687/0.762/0.716/0.751/0.726/0.648/0.770) | E8 + A2 | yes |
| 8 | L1 vs Wait-30 Cabral +0.102 [0.069, 0.141] 10/0; vs Wait-90 +0.068 [0.049, 0.092] | recomputed (+0.1017 [0.069, 0.141]; +0.0677) | yes |
| 9 | ApacheJIT L1 vs Wait-30 +0.075 8/1, Holm 0.0078; vs Wait-90 +0.045 9/0 | recomputed | yes |
| 10 | Table 4 W = 30 AUC: gap 0.071, label 0.075, freshness −0.004, interaction 0.036, path 0.808 | recomputed from cells | yes |
| 11 | Table 4 W = 90 Cabral AUC: gap 0.089, label 0.066, freshness 0.023, share 0.743, path 0.437 | recomputed | yes |
| 12 | Table 4 W = 90 ApacheJIT AUC: 0.075 / 0.074 / 0.002 / 0.974 / 0.778 | recomputed (E8 + A2) | yes |
| 13 | Abstract 0.81 [0.74, 0.86], 0.92 [0.89, 0.95] | `shapley.json` | yes |
| 14 | Table 5 Cabral AUC bands 0.047/0.010/0.004/0.001; shares 0.827/0.173/0.075/0.019; 10/10, 10/10, 9/10, 5/10 | A3 recomputed | yes |
| 15 | Table 5 ApacheJIT AUC 30–180: 0.036, 0.489, 8/9, p = 0.0078 | A3 recomputed | yes |
| 16 | G-mean 30–180 shares 0.913 / 0.685; 180–365 Cabral 0.153 | A3 recomputed | yes |
| 17 | A4: +0.0999 (10/0), +0.0781 (8/1), path 1.057 / 0.904 | A4 recomputed | yes |
| 18 | LAW −0.038 [−0.085, 0.001] 3/7; vs ORB −0.042 2/8; Holm (six tests) 0.252/0.252 | recomputed p's + Holm over 6 | yes |
| 19 | AWT vs ORB −0.039 [−0.077, −0.009], Holm 0.148; vs No-wait +0.187/+0.190, Holm 0.0117 | recomputed | yes |
| 20 | Table 6 AUC (0.815/0.724/0.727/0.699/0.751/0.722) | recomputed | yes |
| 21 | H6 +0.0012 [−0.012, 0.012] 6/3; vs ORB +0.0114; Holm 0.6016 | recomputed (p 0.570/0.301 × Holm 2) | yes |
| 22 | Dual vs ODaSC +0.0175 [0.003, 0.032] 8/1; LAW-M +0.0113 [0.003, 0.021] | recomputed | yes |
| 23 | Table 7 all metrics incl. F1/Popt/IFA (e.g. Wait-90 IFA 13.756, Dual Popt 0.877) | `results/E8_*.json` | yes |
| 24 | Seed SD median 0.0022, max 0.0145; H6 paired SD 0.0192 | recomputed | yes |
| 25 | Table 10/11: 0.732/0.718/0.716/0.687/0.648 and +thr values; H9b +0.0695 9/0, Holm 0.027; Wait-30 +0.0358, Holm 0.234 | A5 recomputed | yes |
| 26 | LAW+thr Cabral 0.696; +0.042 [0.026, 0.058] 9/1, Holm 0.0195; vs ODaSC +0.0009, Holm 1.0 | archive `statistics.json` | yes |
| 27 | S1: neutron S(180) 0.114 vs 0.301; fabric 0.412 vs 0.245; q 0.086 vs 0.061 | `S1`, `diag_law_neutron.json` | yes |
| 28 | Budget: 47 / 51 logged; ODaSC 5 (main) and 10 (lineage 2) | `variants_tried.csv` (47 rows include the "ledger created" header row) | yes (approximately) |
| 29 | 991 unmatched copies leave defective commits undiscovered | `data/*.pkl`: 1,188 defective commits with `t_found = inf` | **partly** (concern 12) |
| 30 | "Hidden-discovery test covers the decomposition and an ApacheJIT project" | `tests/test_no_future.py` | **no** (concern 11) |
| 31 | "ApacheJIT run once per plan"; S3 "every configuration" | plan_v8 header; S3 lacks A3/A4 | **no** (concerns 5 and 9) |

One side observation: the "second-lineage simulator" (A5) gives bit-identical results to the main simulator for No-wait, Wait-30 and Wait-90 on all 9 ApacheJIT projects. This is consistent with the shared starting code and with the Table 9 caption. It is worth one sentence in the Table 10 caption.

No files were modified. Scratch scripts are in /tmp/claude-0/-home-user-p-c1-15/d2d09730-2a6d-533c-ae80-9e44077990c7/scratchpad/.
