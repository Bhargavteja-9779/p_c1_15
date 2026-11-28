# Review round 3: triage (manuscript v3 → v4)

Reports (all simulated reviewers: AI agents with a fresh context):

| Report | Area | Score | Recommendation |
|:--|:--|:--|:--|
| `round_3_R1.md` | Methods | 7/10 | Minor |
| `round_3_R2.md` | Novelty | 7/10 | Minor |
| `round_3_R3.md` | Clarity | 8/10 | Minor |

No new experiments were needed. All changes are wording, plus three numbers derived from existing results.

## R1 (methods)

| # | Concern | Change |
|:--|:--|:--|
| 1 | Age-only corrections lumped into the fresh-data null | Abstract: age-only results restricted to Cabral at the operating point. Highlight 5 restricted to the denoisers and threshold rule. Conclusion: "did not beat"; "LAW ranks better" (not adaptive waiting). |
| 2 | "2–3×" holds only in the leave-out design | Design stated everywhere. Band-in shares stated for ApacheJIT (≈1×). Band-in was the planned design, B3 added later. Older bands: "little on Cabral" restricted to W=30. Temporal proximity (drift) named as an alternative explanation. |
| 3 | Mechanism sentence wrong ("mostly wrong labels"; "same commits") | Replaced with what was measured: the excluded commits have the highest false-clean rate (12–26% / 10.5–23%) and help only when correctly labelled (+0.014/+0.006 AUC at W=30, +0.050/+0.016 at W=90). The most harmful labels sit just past the wait. "Same problem" removed from conclusion and cover letter. |
| 4 | Table 2 C4/C5; "bound"; predicted-positive rates | C4/C5 rewritten. The oracle is called the bound and L1 the counterfactual. Predicted-positive vs true rates on ApacheJIT added (No-wait 0.264, Wait-30 0.315, Wait-90 0.391, LAW 0.445, ODaSC 0.483; true 0.424): the threshold helped where under-prediction was largest. |
| 5 | Cabral AUC/Shapley also post hoc | Labelled exploratory on both families |
| 6 | A4 path shares were G-mean | AUC path shares given (0.780 / 0.923); G-mean shown labelled |
| 7 | AWT vs Wait-90 missing; Table 7 p values; H9 fixed arms known; RQ1 rounding | Test added. Caption notes no multiplicity control. H9 note added. Median recomputed from the unrounded source (15.4%). |
| 8 | Section 6.2 wording | Changed to "the most harmful examples lie just beyond any practical cut-off" |

## R2 (novelty)

| # | Concern | Change |
|:--|:--|:--|
| 1 | Ratio is design-selected | As R1#2 |
| 2 | ODaSC-opt comparison used unlike contrasts | Song et al. Table II means extracted reproducibly (`scripts/song2022_table2.py`): opt/flt beat OOB by +0.039/+0.034. Discussion now centres on "estimated ≈ optimal there, far from optimal here". |
| 3 | Table 2 out of step | C1, C2, C4 and C5 rewritten |
| 4 | Age-only on fresh data | As R1#1 |
| 5 | Liu 2025 partial | Observed-label evaluation recommendation, practical-scenario degradation and label-quality finding added; final-label evaluation justified as a retrospective protocol |
| 6 | BORB under-used | Cited for using a batch learner online (3.1) |
| 7 | Falessi wording | "Significant but modest, particularly little in AUC"; two releases improved recall, reduced precision |
| 8, 9 | Optional context | Not added (would need verification) |

## R3 (clarity)

| # | Concern | Change |
|:--|:--|:--|
| 1 | Table 2 | Fixed |
| 2 | README old numbering, broken table, split code | Renumbered; table fixed; one-line split command (verified); script name explained |
| 3 | Tables 9 and 14 uncited; S order; T3c | Cited. Supplementary items renumbered in order of first citation, all cited. T3c listed in S4. |
| 4 | W15; H1 sixth test; RQ1 wording; L2 dash | Fixed |
| 5 | Table 14 "reviewer request" | Now "internal (AI) review request" |
| 6 | S3 true-label flag | Flag now set from the variant name |
| 7 | Fig. 1 caption; Fig. 3 y-label | Fixed |
| 8 | Bullets | RQ2 and RQ5 answers converted to prose |
| 9 | Highlight 1; graphical abstract needs an image | Highlight reworded; the image must be produced by the authors (noted in SUBMISSION_READINESS) |
| 10 | Declarations | Placeholders need the human authors |
