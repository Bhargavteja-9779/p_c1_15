# Review round 4: triage (manuscript v4 → v5)

All reviewers are simulated: AI agents with a fresh context.

| Report | Area | Score | Recommendation |
|:--|:--|:--|:--|
| `round_4_R1.md` | Methods | 7.5/10 | Minor, no major |
| `round_4_R2.md` | Novelty | 8/10 | Minor |
| `round_4_R3.md` | Clarity | 8.5/10 | Minor, close to accept |

Rounds 3 and 4 were clean. Gate G10 is set to pass (internal).

## R1 (methods)

| # | Concern | Change |
|:--|:--|:--|
| 1 | Age-only overstatement | Abstract scoped by dataset and "planned test". Contribution 3 and C3: "age-based (delay-posterior) corrections did not reliably recover". Intro: "reused Cabral test projects". |
| 2 | Band remnants; noise density | Contribution 2 restricted to W=30. §6.1 sentence corrected (the recent band alone recovers about half at W=30 and a fifth at W=90 on ApacheJIT). Noise density named next to drift. |
| 3 | Qualifiers in highlights and abstract | Highlight 5 says n = 9. Abstract marks the AUC decomposition as exploratory and says it agrees with the planned G-mean tests. |
| 4 | C1 row | Both waits given |
| 5 | Holm family size | Six tests stated. Like-for-like LAW+thr vs Wait-30+thr reported (+0.0202, 9/1, Holm 0.0195). |
| 6 | 0.016 → 0.017 (computed from unrounded values); 7–30 d source cited; "at most" removed | Fixed. Bootstrap seed is 0 throughout (scripts). |

## R2 (novelty)

| # | Concern | Change |
|:--|:--|:--|
| 1 | "Cannot" | Changed to "did not reliably". Family named "age-based (delay-posterior)". |
| 2 | Falessi §6.2 | Checked in full text: ≈30% gains in recall/F1/kappa/MCC, small in AUC. Text corrected; their recommendation to find mislabelled recent items credited. |
| 3 | ODaSC comparison | Metric caveat added; shared-project ratio (+0.053, about 2×) computed in `song2022_table2.py`; wait-length bullet rephrased |
| 4 | C1 / "almost entirely" | Fixed ("mostly") |
| 5 | Highlight 4 | Qualified ("with other bands relabelled") |
| 6 | BORB in threats | Added |
| 7 | Optional context | Not added |
| 8 | Review-round count | Four, consistent across Declarations and SUBMISSION_READINESS |

## R3 (clarity)

| # | Concern | Change |
|:--|:--|:--|
| 1 | Abstract 264 words | Now 244 words |
| 2 | Round count | Fixed (four) |
| 3 | README label; repository layout | Label fixed; `REPO_ROOT` override for the scanner; expected layout documented |
| 4 | "@" garbled to "S" by the renumbering script; missing full stop; p precision | Fixed (four places); full stop added; p = 0.002 used consistently |
| 5 | "held-out" | Fixed |
| 6 | Supplementary file names | Renamed to match labels (S1, S5, S6) |
| 7 | Length | Not changed (optional) |
