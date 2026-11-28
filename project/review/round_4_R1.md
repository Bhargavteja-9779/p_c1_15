# Review round 4 — Reviewer R1 (methodology/statistics), verbatim (simulated reviewer: AI agent with fresh context)

# Referee report, round 4 (methodology and statistics)

**Overall score: 7.5/10. Recommendation: minor revision.** No MAJOR concerns remain. Nothing blocks acceptance. Most of the round-3 R1 items are now fixed in the manuscript text itself, not only claimed as fixed in `review/round_3.md`. A few are fixed in the body but not in the abstract, contributions or highlights; those should be corrected before acceptance (concerns 1–3). I recomputed 32 quantities from the raw files. All match except one rounding slip (0.016 should read 0.017), and one Holm family size stated in the text disagrees with the p-values reported (concern 5).

## Status of the round-3 R1 concerns (checked in the manuscript text)

| R3-R1 # | Status | Evidence |
|:--|:--|:--|
| 1 (age-only lumped into the fresh-data null) | **Partly resolved** | The fresh-data null is now limited to the denoisers and the threshold (abstract, Highlight 5, conclusion). The conclusion and cover letter say "did not beat" and "LAW ranks better". But the abstract says age-only corrections "lost to a 90-day wait". That is the exact overstatement R1 flagged (Holm p = 0.252 and 0.148). Contribution 3 says age-only corrections "cannot recover", and Table 2 C3 says they "do not recover it". |
| 2 ("2–3×" holds only in one design) | **Mostly resolved** | The design is named in the abstract, Section 5.2, Section 6.1, the conclusion and the cover letter. The Table 7 caption says band-in was the planned design. The 180–365-day band at W = 90 is now reported. Temporal proximity is named as an alternative. Remnants are in concern 2. |
| 3 (wrong mechanism sentence) | **Resolved** | "Mostly wrong labels" and "same commits" are gone. The text now reports the measured false-clean rates (12.2–26.2% and 10.5–23.2%) and the simple effects. |
| 4 (Table 2, "bound", predicted-positive rates) | **Resolved** | C4 and C5 are rewritten. The oracle is called the bound. Predicted-positive rates are added in Section 5.5. A new wording problem in C1 is in concern 4. |
| 5 (exploratory labelling of the Cabral AUC/Shapley results) | **Resolved in the body, not in the abstract** | Section 5.2 now says "exploratory on both families". The abstract still presents 0.81, 0.44 and 0.74 without saying they are exploratory or that the planned G-mean tests agree. |
| 6 (A4 metric) | **Resolved** | AUC path shares 0.780 and 0.923, with G-mean shown and labelled. |
| 7 (statistics details) | **Resolved** | The adaptive-waiting vs Wait-90 test is added. Table 7 has the "no multiplicity control" note. The H9 note is added. The median is 15.4%. |
| 8 (Section 6.2 wording) | **Resolved** | |
| 9 (weak-power caveat in the highlights) | **Not done** | Highlight 5 has no caveat that the tests are weakly informative below 0.023. |

## Numbered concerns

### 1. [MINOR, must fix] The abstract and Contribution 3 still overstate the age-only result

- **Where.**
  - Abstract: "Age-only corrections lost to a 90-day wait at the operating point on Cabral."
  - Contribution 3: "Evidence that age-only corrections cannot recover the penalty."
  - Table 2 C3: "do not recover it".
  - Introduction: "On the ten held-out projects it lost..." — Section 4.6 itself says the Cabral test set is not an untouched hold-out.
- **Evidence.** Recomputed: LAW −0.038, 3/7, raw p 0.131; adaptive waiting −0.035, 2/8, raw p 0.084. Holm p is 0.252 for both. LAW's AUC is higher than Wait-90's (+0.024, unadjusted p 0.027). On ApacheJIT, LAW at 0.5 is ahead of Wait-90 (+0.015, 7/2).
- **Resolution.**
  - Use the conclusion's own wording in the abstract: "did not beat a 90-day wait at the operating point on Cabral (LAW ranked better in AUC)".
  - Change "cannot" to "did not reliably" (the wording of the Section 5.3 heading).
  - Change "held-out" to "reused test".

### 2. [MINOR] Remnants of the band-design over-generalisation

- **Contribution 2: "Older false-clean labels contribute little on Cabral."**
  - This is not restricted to W = 30.
  - At W = 90 the 180–365-day band has leave-out share 0.234 with 0.264 of the labels, and band-in share 0.312. That is about its share, as Section 5.2 now admits.
- **Section 6.1: "On ApacheJIT no single band, recent or old, can be corrected in isolation to much effect."**
  - Relabelling the recent band alone gives 0.489 of the gain at W = 30.
  - The sentence holds for the older bands, and for the recent band at W = 90 (0.203), but not for the recent band at W = 30.
- **A further alternative explanation is not named: noise density.** Recomputed from `flip_counts.json`:
  - Per-band false-clean rate among provisionally clean commits:
    - Cabral, W = 30: 0.121 / 0.092 / 0.070 / 0.037.
    - ApacheJIT, W = 30: 0.312 / 0.229 / 0.150 / 0.052.
  - The oldest band holds 46–55% of the provisionally clean commits.
  - So the recent band's false-clean labels are the densest, not just the most recent. Per-label harm could be non-linear in local noise density, as well as reflecting temporal proximity.
  - The sentence "so the result below is not simply where the false-clean labels are" is right about counts but silent about density.
- **Resolution.**
  - Restrict Contribution 2 to W = 30.
  - Fix the Section 6.1 sentence.
  - Add noise density next to drift as an untested explanation.

### 3. [MINOR] The highlights and abstract omit qualifiers that the body carries

- **Highlight 5** ("no tested denoiser or threshold rule beat a 90-day wait significantly") needs the power caveat: the tests are weakly informative below about 0.02–0.023 G-mean.
- **The abstract** should mark the AUC/Shapley decomposition as exploratory and say that the planned G-mean H3 tests point the same way.
- **Highlight 4** is fine. In both designs and in all four settings, the recent band has the highest share per label.

### 4. [MINOR] Table 2 C1 contradicts itself

- C1 reads "for short waits the penalty is label noise (path share 0.44–0.78 at W = 90)". The claim is about short waits, but the numbers are W = 90 numbers, and they describe a non-majority share on Cabral.
- **Resolution:** "W = 30: path share 0.81–0.92; W = 90: 0.44–0.78 (convention-dependent)".

### 5. [MINOR] The stated Holm family size for the second-lineage confirmation is wrong

- Section 3.4 lists "LAW+thr beats Wait-90, ORB-style-90 and its ODaSC-style rule ... (three tests)".
- The reported Holm p = 0.0195 comes from the six-test family in lineage 2's `plan_v3` (`archive/zealous_lamport_cycle1/results/statistics.json`, E1_main_proposed_vs_baselines). That family also includes No-wait, Wait-30+thr and ODaSC-W15+thr. Holm over three tests would give 0.0117.
- The like-for-like comparison inside that family is not reported: LAW+thr vs Wait-30+thr, +0.0202, 9/1, Holm 0.0195. It is directly relevant to the "threshold vs label policy" argument.
- **Resolution:** state "six tests" and report the Wait-30+thr row.

### 6. [MINOR] Small numeric and citation slips

- **ApacheJIT W = 90 simple effect.** Section 5.2 gives the true-label gain as 0.016; recomputed it is 0.0167, which rounds to 0.017.
- **Table citation.** The 10.5–23.2% rate for commits aged 7–30 days is cited to Table 4, which has no 7–30-day column. Cite `rq1_label_noise.json`, or add the column.
- **Odd wording.** "worth 1 − 0.775 of the gain at most" (Section 5.2) is an exact quantity (0.225), not a bound. Drop "at most".
- **CI drift.** Bootstrap CIs differ in the third decimal from R1's round-3 recomputation (for example LAW AUC [0.0105, 0.037] vs [0.0101, 0.0373]). This is harmless, but state the bootstrap seed.

### 7. [MINOR] Baseline fairness (already disclosed; no new action)

These are disclosed in Sections 3.2, 4.3 and 7:
- unequal tuning budgets (22 configurations for the authors' own families vs 5 for the ODaSC-style rule);
- ORB-style corrects class imbalance twice;
- the ODaSC adaptations use a different mechanism from the original;
- the denoisers were frozen at W = 30 but are compared with Wait-90.

Keep these caveats wherever the fresh-data nulls are summarised.

## Spot-check table (recomputed from raw files)

Sources: `results/raw_results.jsonl`, `results/review1/raw.jsonl`, `flip_counts.json`, `rq1_label_noise.json` and the lineage-2 archive. Project means over seeds 100–104; Wilcoxon exact test; 10,000-resample project bootstrap.

| # | Manuscript value | Recomputed | Match |
|:--|:--|:--|:--|
| 1 | RQ1: 4.6–33.2%, median 15.4%; excluded 4.8–13.8% | 0.0457 / 0.3329 / 0.1538; 0.048 / 0.138 | yes |
| 2 | False-clean rate <7 d 12.2–26.2%; 7–30 d 10.5–23.2%; >2 y 0.1–9.7% | 0.122 / 0.262; 0.105 / 0.232; 0.001 / 0.097 | yes |
| 3 | Dev: Wait-30 0.621 → L1 0.785, oracle 0.794 | 0.6206 / 0.7854 / 0.7938 | yes |
| 4 | Dev: ODaSC 0.760, LAW-M 0.755, Dual 0.681 | 0.7598 / 0.7551 / 0.6812 | yes |
| 5 | Table 5 Cabral (0.620 / 0.722 / 0.702 / 0.654 / 0.684 / 0.625 / 0.429 / 0.715) | identical | yes |
| 6 | Table 5 ApacheJIT (0.687 / 0.762 / 0.716 / 0.751 / 0.726 / 0.648 / 0.770) | identical | yes |
| 7 | Cabral L1 vs Wait-30: +0.102 [0.069, 0.141], 10/0 | +0.1017 [0.0689, 0.1412], 10/0, p 0.002 | yes |
| 8 | Cabral L1 vs Wait-90: +0.068 [0.049, 0.092] | +0.0677 [0.0487, 0.0918] | yes |
| 9 | ApacheJIT L1 vs Wait-30 / Wait-90: +0.075 8/1, +0.045 9/0, Holm 0.0078 | +0.0749 / +0.0453; raw p 0.0078 / 0.0039, Holm 0.0078 | yes |
| 10 | W = 30 Cabral AUC path share 0.808; W = 90 0.437 | 0.808; 0.436 | yes |
| 11 | W = 90 ApacheJIT AUC 0.778 / 0.974 / 1.169 | 0.7785 / 0.9739 / 1.1694 | yes |
| 12 | Simple effects −0.022 / +0.014 (Cabral W = 30); −0.008 / +0.006 (ApacheJIT W = 30) | −0.0223 / +0.0136; −0.0085 / +0.0064 | yes |
| 13 | ApacheJIT W = 90 true-label gain "0.016" | 0.0167 | **rounding (0.017)** |
| 14 | Wait-30 vs Wait-90 AUC on Cabral: +0.0178, 8/2, p 0.0195 | identical | yes |
| 15 | Table 7 band-in / leave-out, recent bands (0.827 / 0.775; 0.489 / 0.729) | 0.827 / 0.775; 0.488 / 0.729 | yes |
| 16 | Table 7 flip shares (Cabral W = 30: 0.309 / 0.223 / 0.226 / 0.243; ApacheJIT W = 90: 0.216 / 0.275 / 0.254 / 0.255) | per-project mean shares identical | yes |
| 17 | "2–3×" in leave-out | 2.51 / 2.76 / 2.14 / 2.30 | yes (leave-out only, as now stated) |
| 18 | A4: +0.0999 10/0; +0.0781 8/1; AUC path shares 0.780 / 0.923 | +0.0999, +0.0781; 0.7797 / 0.9234 | yes |
| 19 | LAW vs Wait-90 −0.038 [−0.085, 0.001] 3/7; vs ORB −0.042 2/8; Holm 0.252 | identical (raw p 0.131 / 0.084; Holm over six = 0.252) | yes |
| 20 | Adaptive waiting vs Wait-90 −0.035 2/8, Holm 0.252; vs ORB −0.039, Holm 0.148 | identical | yes |
| 21 | LAW / adaptive waiting vs No-wait: +0.187 / +0.190, Holm 0.0117 | +0.1872 / +0.1904 | yes |
| 22 | LAW AUC vs Wait-90: +0.0239 [0.0105, 0.037], 7/3, p 0.0273 | identical | yes |
| 23 | Table 8 G-mean / AUC (0.619 / 0.699; 0.616 / 0.751; 0.658 / 0.724) | identical | yes |
| 24 | H6: +0.0012, 6/3; +0.0114; Holm 0.6016 | identical (raw p 0.570 / 0.301) | yes |
| 25 | Dual vs ODaSC +0.0175 [0.003, 0.032], 8/1; LAW-M +0.0113; Holm 0.164 | identical (raw p 0.0547 × 3) | yes |
| 26 | Table 9 Dual 0.735 / 0.808, LAW-M 0.728, ORB 0.706 | identical | yes |
| 27 | A5 LAW@0.5 vs Wait-90: +0.0151 [0.0037, 0.0293], 7/2, p 0.039 | identical | yes |
| 28 | Table 12 (all 15 cells) | identical; A5 fixed-threshold arms equal E8 | yes |
| 29 | H9: No-wait +0.0695 9/0, Holm 0.027; Wait-30 +0.0358, Holm 0.234; LAW+thr vs Wait-90 +0.0117 | identical | yes |
| 30 | Second lineage: LAW+thr 0.696; vs Wait-90 +0.042 9/1; vs ORB +0.038; vs ODaSC +0.0009; Holm 0.0195 | 0.6961; +0.0417 / +0.0377 / +0.0009; Holm 0.0195 **over six tests**, not three | **values yes, family size no** |
| 31 | Second-lineage ODaSC vs Wait-90: +0.0407, 10/0, p 0.0020 | identical | yes |
| 32 | H6 paired SD 0.0192 | 0.0192 | yes |

No files were modified. Scratch scripts are in /tmp/claude-0/-home-user-p-c1-15/d2d09730-2a6d-533c-ae80-9e44077990c7/scratchpad/r4/ (s1.py, s2.py, s3.py).
