# Review round 3 — Reviewer R1 (methodology/statistics), verbatim (simulated reviewer: AI agent with fresh context)

# Referee report, round 3 (methodology and statistics)

**Overall score: 7/10. Recommendation: minor revision.** No new experiments are needed. The three items tagged MAJOR are wording changes that must be made before acceptance, in the abstract, highlights, Table 2, the conclusion and the cover letter.

## Summary

I recomputed about 30 quantities from the raw files: `results/raw_results.jsonl`, `results/review1/raw.jsonl`, `results/review1/flip_counts.json`, `results/rq1_label_noise.json` and `data/**/*.pkl`. Every table value I checked matches; I found no transcription errors (table at the end).

Most round-2 concerns are now fixed in the manuscript text, not just claimed as fixed in `round_2.md`:
- W = 90 path and Shapley shares are both in the abstract and conclusion.
- The window factor is said to be confounded with label state, and its simple effects are reported.
- L2 is explained as selection-biased.
- The ApacheJIT RQ2 analyses are labelled exploratory.
- "Adds nothing" is gone, and the leave-one-band-out run (B3) was added.
- The RQ1 wording is fixed, S3 now covers A3/A4/B1/B3, the leakage tests now include decomp and kafka, and 1,188 never-discovered commits is stated.

What remains is claim strength: some sentences go further than the paper's own analyses, and a few remnants of the round-2 problems survive.

## Status of round-2 R1 MAJOR concerns

| R2-R1 # | Status | Evidence |
|:--|:--|:--|
| 1 (age-only claim vs fresh data and AUC) | **Partly resolved** | Section 5.3 is now symmetric. But the abstract still says "Age-only corrections ... did not significantly beat a 90-day wait on the fresh data", and Highlight 5 says "No tested correction significantly beat ... on fresh data". Adaptive waiting never ran on ApacheJIT. The only fresh age-only run, LAW at 0.5, beat Wait-90: +0.0151 [0.004, 0.029], 7/2, unadjusted p = 0.039, never formally tested. See concern 1. |
| 2 (localisation over-claimed) | **Partly resolved** | B3 was added and "adds nothing" removed. The new "2–3× its share in all four settings" holds only under leave-one-band-out (concern 2). |
| 3 (selective W = 90 share) | Resolved | Abstract and conclusion give 0.44/0.78 (path) and 0.74/0.97 (Shapley); Table 6 gives all three conventions. |
| 4 (2×2 confound) | **Resolved in 5.2, but the text now has a factual error** | "mostly wrong labels" is false (concern 3). |
| 5 (ApacheJIT RQ2 called confirmatory) | Mostly resolved | Section 4.6 and Table 14 are fixed. The Cabral AUC/Shapley split is also post hoc but is not labelled so (concern 5). |
| 6 ("depends on implementation") | **Not fully resolved** | Removed from the RQ4 answer, but Table 2 row C4 still reads "depends on dataset and implementation" (concern 4). |

## Numbered concerns

### 1. [MAJOR] The abstract and Highlight 5 still lump age-only corrections into a fresh-data null that was never tested

- **Evidence.**
  - Adaptive waiting was never run on ApacheJIT.
  - LAW at 0.5 on ApacheJIT has the highest fixed-threshold mean (0.732 vs 0.716) and an unadjusted p of 0.039 (recomputed from A5).
  - Saying "did not significantly beat" therefore rests only on the absence of a planned test.
- **Related errors in the conclusion.**
  - "age-only corrections ... though they rank better" is wrong for adaptive waiting: its AUC is 0.699, below Wait-90's 0.727 (Table 8).
  - "lose to a 90-day wait" overstates a non-significant difference (Holm p = 0.252, 3/7 and 2/8).
- **Resolution.**
  - Abstract: "At the 0.5 operating point on the reused Cabral set, age-only corrections did not beat a 90-day wait (LAW ranked better in AUC); on fresh data, feature-based denoisers and a latency-aware threshold did not significantly beat it."
  - Highlight 5: restrict to the corrections actually tested on fresh data.
  - Conclusion: write "LAW ranks better", and use "did not beat" rather than "lose to".

### 2. [MAJOR] "Two to three times their share" in all four settings comes from one of the two band designs

The per-label ratio is the band's share of the L1 gain divided by its share of the false-clean labels. My recomputation for the most recent band, AUC, with project-bootstrap 95% CIs:

| Setting | Leave-out ratio | Band-in ratio |
|:--|:--|:--|
| Cabral, W = 30 | 2.51 [2.12, 3.09] | 2.68 [2.29, 3.25] |
| Cabral, W = 90 | 2.76 [2.31, 3.44] | 3.12 [2.68, 3.80] |
| ApacheJIT, W = 30 | 2.14 [1.67, 2.67] | **1.44** [1.11, 1.66] |
| ApacheJIT, W = 90 | 2.30 [1.74, 2.94] | **0.94** [−0.18, 1.57] |

- **The two designs disagree badly on ApacheJIT.**
  - Band-in shares sum to 0.368 at W = 30 and 0.165 at W = 90 (−0.48 in G-mean).
  - Leave-out shares sum to 1.17 and 1.23.
  - The two designs bracket the attribution, and on ApacheJIT that bracket is wide.
- **The headline design was not the pre-specified one.** plan_v9 B2 defined "gain per 1% of flips" against the band-in gain (B1). B3 was added later, and the headline "2–3×" uses B3 only.
- **"Older labels matter little on Cabral" holds only at W = 30.** At W = 90 the 180–365-day band does about its share (leave-out 0.234 vs 0.264 of the false-clean labels; band-in 0.312).
- **"Matter little even jointly" (Section 5.2) cites leave-out shares, which measure one band given the others corrected.** The joint effect of the older bands is 1 − band-in(recent): 0.17 on Cabral and 0.51 on ApacheJIT at W = 30.
- **There is an untested alternative explanation.** Higher per-label harm in the band closest in time to the scored commits is also what temporal relevance (drift) would predict. The "too young for their defects to have been found" sentence explains why these labels are false-clean, not why each one does more harm.
- **Resolution.**
  - In the abstract, highlights and conclusion, state the design: "when the other bands are corrected, ... 2–3×; relabelling the recent band alone gives 0.9–3.1× its share".
  - Note that the band-in design was the planned one.
  - Fix the "jointly" wording.
  - Restrict "little on Cabral" to W = 30.
  - Name temporal proximity as an alternative explanation, or add a recency-matched control.

### 3. [MAJOR] The mechanism sentence behind the headline claim is wrong as written

- **Where it appears.**
  - Section 5.2: "in the observed-label row it adds recent commits with mostly wrong labels".
  - Contribution 1, the conclusion and the cover letter: "the commits a wait excludes are those whose labels are wrong".
  - Sections 5.2 and 6.1: "the noisy commits and the fresh ones are largely the same commits".
- **Evidence.**
  - From `rq1_label_noise.json`, the false-clean rate among provisionally clean commits younger than 7 days is 0.122–0.262 (median 0.198), and 0.105–0.232 at 7–30 days. Roughly 75–88% of the excluded commits are correctly labelled.
  - Table 7 places the most harmful labels in the band just past the wait, which the wait keeps, not in the window it excludes.
  - With true labels the excluded window is worth little at W = 30: Oracle − L1 is +0.014 [0.010, 0.017] AUC on Cabral and +0.006 [0.003, 0.011] on ApacheJIT. It is worth more at W = 90: +0.050 and +0.017.
  - So "the same commits" is an interpretation of a positive interaction that is partly built into the design (round-2 #4). It was not measured.
- **Resolution.** Replace with something like: "the wait excludes the commits with the highest false-clean rate (12–26%), and they help, modestly at W = 30, only when correctly labelled; the most harmful false-clean labels are those just past the wait." Soften "same problem" in the conclusion and cover letter.

### 4. [MINOR] Remnants in Table 2 contradict the revised text

- **C4** still says "depends on dataset and implementation". Both implementations agree on ApacheJIT: +0.0004, 6/3, p = 0.91 (recomputed).
- **C5** ("helps only policies with a distorted prior") is plural and stated as a finding. The text calls it a post-hoc reading supported by one policy (No-wait, Holm p = 0.027).
- **Section 2.5** still calls L1 (0.762) "an upper target", and the end of Section 1 says "the true-label bound". Round 2 (#13) asked that the oracle be called the bound.
- **R2-#7's request** for predicted-positive versus true rates per policy on ApacheJIT is still not met.

### 5. [MINOR] The confirmatory/exploratory labelling is incomplete for Cabral

- AUC was made primary only after the G-mean results were known (Table 14), and the Shapley analysis comes from plan_v8. The Cabral AUC/Shapley numbers in the abstract (0.81, 0.44, 0.74) are therefore post hoc too.
- Section 5.2 labels the factorial split "exploratory on ApacheJIT" only, which implies the Cabral split is confirmatory. The confirmatory evidence is the G-mean H3 tests.
- **Resolution:** label the AUC decomposition exploratory on both families, and note in the abstract that the planned G-mean tests point the same way.

### 6. [MINOR] The robustness check reports G-mean path shares while AUC is declared primary

- Section 5.2 / S4 give "path shares of 1.057 and 0.904". These are G-mean values.
- The AUC path shares are 0.780 (Cabral) and 0.923 (ApacheJIT), recomputed from A4.
- Report AUC, or label the metric.

### 7. [MINOR] Statistics details

- The H1 test of adaptive waiting against Wait-90 (−0.035 [−0.074, −0.003], 2/8, Holm 0.252) is in the pre-registered family but is not reported.
- Table 7 shows 64 unadjusted p-values (32 per metric across Table 7 and T12) with "projects hurt" counts. Readers will take these as significance; add an explicit "no multiplicity control" note to the caption.
- H9 is called confirmatory, but its fixed-threshold arms for No-wait, Wait-30 and Wait-90 were already known: A5 is bit-identical to E8. The +thr arms were not known, so the label is defensible, but say so.
- The RQ1 median relative reduction is 0.1538 from the json (the manuscript gives 15.3%). This is trivial rounding through an intermediate CSV.

### 8. [MINOR] Section 6.2 wording

"The harmful examples are not confined to the most recent window" sits awkwardly next to "the harm is concentrated in recent commits". Clarify that "window" here means the window the wait excludes.

### 9. [MINOR] Baseline fairness (already disclosed; no action beyond the current limitations)

- Tuning budgets were unequal: 22 configurations for the authors' own families against 5 for the main-lineage ODaSC-style rule.
- ORB-style corrects class imbalance twice.
- The ODaSC adaptations use a different mechanism from the original.
- The denoisers are frozen at W = 30 but compared with Wait-90.

The fresh-data nulls should keep their "weakly informative below 0.023" caveat wherever they are summarised (highlights).

## Spot-checked numbers (recomputed from raw files)

| # | Manuscript value | Recomputation (source) | Match |
|:--|:--|:--|:--|
| 1 | 331,937 commits = 265,003 + 66,934 | data/jit + aj pkl row counts | yes |
| 2 | 1,188 defective Cabral commits never discovered | `t_found = inf` in pkl | yes |
| 3 | Median delay 16–568 d; P90 383–2811 d; share found after 90 d 0.312–0.722 / 0.430–0.826 | recomputed from pkl (all 23 rows match Table 3) | yes |
| 4 | RQ1 4.6%–33.2%, median 15.3%; excluded 4.8–13.8%; <7 d 12.2–26.2%; >2 y 0.1–9.7% | rq1 json: 0.0457/0.3329/0.1538; 0.048/0.138; 0.122/0.262; 0.001/0.097 | yes (rounding) |
| 5 | Dev Wait-30 0.621 → L1 0.785, oracle 0.794 | E0/E0b | yes |
| 6 | Table 5 Cabral (0.620/0.722/0.702/0.654/0.684/0.625/0.429/0.715) | E1 + E3b | yes |
| 7 | Table 5 ApacheJIT (0.687/0.762/0.716/0.751/0.726/0.648/0.770) | E8 + A2 | yes |
| 8 | Cabral L1 vs Wait-30 +0.102 [0.069, 0.141] 10/0; vs Wait-90 +0.068 | +0.1017 [0.069, 0.141]; +0.0677 | yes |
| 9 | ApacheJIT L1 vs Wait-30 +0.075 8/1; vs Wait-90 +0.045 9/0 | +0.0749, p 0.0078; +0.0453, p 0.0039 | yes |
| 10 | Table 6 W = 30 Cabral AUC: gap 0.071, label 0.075, freshness −0.004, interaction 0.036, shares 0.808/1.061/1.315 | 0.071/0.075/−0.004/0.036; 0.808/1.061/1.314 | yes |
| 11 | Table 6 W = 90 Cabral AUC: 0.089/0.066/0.023/0.054; 0.437 [0.325, 0.539]/0.743/1.050 | same; path CI [0.328, 0.538] | yes |
| 12 | Table 6 W = 90 ApacheJIT AUC: 0.778/0.974/1.169 | 0.779/0.974/1.169 | yes |
| 13 | Table 6 G-mean rows (e.g. W = 90 Cabral 0.498/2.615/4.733) | same | yes |
| 14 | Simple effects −0.022/+0.014 (Cabral), −0.008/+0.006 (ApacheJIT) | same | yes |
| 15 | Wait-30 vs Wait-90 AUC +0.0178, 8/2, p = 0.0195 | same | yes |
| 16 | Table 7, all 16 AUC rows (flip shares, band-in, leave-out, projects hurt, p) | A3/B1/B3 + flip_counts (per-project mean shares) | yes |
| 17 | Band-in sums: >1 on Cabral, <1 on ApacheJIT | 1.094 / 0.368 (W = 30); 1.103 / 0.165 (W = 90) | yes |
| 18 | "2–3× in all four settings" | leave-out 2.51/2.76/2.14/2.30; band-in 2.68/3.12/1.44/0.94 | **only for leave-out** |
| 19 | A4: +0.0999 10/0; +0.0781 8/1; path 1.057/0.904 | same, but these are G-mean; AUC 0.780/0.923 | **metric unlabelled** |
| 20 | LAW −0.038 [−0.085, 0.001] 3/7; vs ORB −0.042 2/8; Holm 0.252/0.252 | same | yes |
| 21 | AWT vs ORB −0.039, Holm 0.148; vs No-wait +0.187/+0.190, Holm 0.0117 | same | yes |
| 22 | Table 8 G-mean and AUC (0.715/0.658/0.654/0.619/0.616/0.429; 0.815/0.724/0.727/0.699/0.751/0.722) | E1 | yes |
| 23 | LAW AUC vs Wait-90 +0.0239 [0.0105, 0.037] 7/3, p = 0.0273 | +0.0239 [0.0101, 0.0373], p 0.0273 | yes |
| 24 | H6 +0.0012 [−0.012, 0.012] 6/3; vs ORB +0.0114; Holm 0.6016 | same | yes |
| 25 | Dual vs ODaSC +0.0175 [0.003, 0.032] 8/1, Holm 0.164; LAW-M +0.0113 [0.003, 0.021] | p 0.0547 × 3 = 0.164 | yes |
| 26 | Table 9 means and AUC (0.770/0.735/0.728/0.718/0.716/0.706/0.687/0.648; Dual AUC 0.808) | E8 | yes |
| 27 | Table 13 H9a/H9b diffs, W/L and Holm (0.027, 0.234, 1.0 ...) | recomputed, Holm over 7: 0.0273/0.2344 | yes |
| 28 | A5 LAW@0.5 vs Wait-90 +0.0151 [0.0037, 0.0293] 7/2, p = 0.039 | +0.0151 [0.0041, 0.0294], p 0.0391 | yes |
| 29 | Second-lineage fixed-threshold arms identical to main simulator | np.allclose for nowait/W30/W90 | yes |
| 30 | Seed SD median 0.0022, max 0.0145; H6 paired SD 0.0192 | same | yes |
| 31 | Dev ODaSC 0.760, LAW-M 0.755, Dual 0.681 | same | yes |
| 32 | "Older bands matter little on Cabral" | true at W = 30 only; at W = 90 the 180–365 band leave-out 0.234 vs its 0.264 of false-clean labels | **partly** |
| 33 | "recent commits with mostly wrong labels" | false-clean rate among young provisionally clean commits 0.105–0.262 | **no** |

No files were modified. My scratch scripts (`load.py`, `s1.py`–`s5.py`) are in /tmp/claude-0/-home-user-p-c1-15/d2d09730-2a6d-533c-ae80-9e44077990c7/scratchpad/.
