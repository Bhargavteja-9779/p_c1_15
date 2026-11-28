# Review round 2: triage (manuscript v2 → v3)

Reports: `round_2_R1.md` (methods 6/10, major), `round_2_R2.md` (novelty 5/10, major), `round_2_R3.md` (clarity 7/10, minor).

All three reviewers are simulated: AI agents with a fresh context. New evidence comes from `experiments/plan_v9_review2.yaml` (B1–B3), committed before the runs.

## Factual errors found by reviewers and verified against sources

| Reviewer | Claim in v2 | Source check | Fix |
|:--|:--|:--|:--|
| R2#1 | "ODaSC-opt could not be located" (round-1 response) | Song_IJCNN2022.txt: ODaSC-opt/flt are in-paper true-label benchmarks, W=15, first 10k commits, p = 0.7278 / 0.6932 vs ODaSC | Added to 2.2, C1 row, and 6.2 (effect-size discussion). Round-1 response was wrong. |
| R2#2 | Song 2023a "showed retrospective evaluation can misjudge methods" | Abstract (PDF): the waiting time had no significant impact on validity | Corrected; added a paragraph on training vs evaluation |
| R2#3 | Falessi: "discarding recent releases"; "removes most of the snoring" | TOSEM full text: only classes labelled non-defective are removed; gains small, esp. AUC | Corrected in 2.2 and 6.2 |
| R1#12 | 991 never-discovered defective commits | data: 1,188 | Corrected (both numbers) |
| R1#11 | Leakage test covers decomp and ApacheJIT | It did not | Tests extended (decomp levels, kafka); they pass |
| R3#1 / R1#9 | S3 "every configuration" | Missed jsonl-stored review runs | Scanner extended; complete/partial/smoke distinguished |

## Claim strength

| Reviewer concern | Change |
|:--|:--|
| R1#3, R2#4: W=90 share reported selectively | Abstract and conclusion give the path share and the Shapley share; all three attribution conventions are in Table 6. The interaction is the headline. W=90 is G-mean-optimal, not AUC-optimal (Wait-30 AUC > Wait-90). |
| R1#4: freshness confounded with label state | Stated; simple effects reported; L2 explained as selection-biased |
| R1#2, R2#5, R3#4: localisation over-claimed | New B1/B2/B3 evidence. Claim is now "per false-clean label, the most recent waited-out commits do 2–3× their share; older labels matter less, mainly jointly (ApacheJIT)". "Adds nothing" removed. |
| R1#1: age-only claim contradicted by AUC / fresh data | RQ3 restricted to the 0.5 operating point on Cabral; AUC and the descriptive ApacheJIT result reported; highlight changed |
| R1#5: ApacheJIT RQ2 analyses called confirmatory | Labelled exploratory; only plan_v7 tests and H9 are confirmatory; 3 deviations added |
| R1#6, R3#3: "depends on implementation" | Removed; both adaptations agree on ApacheJIT; "denoiser" made singular |
| R1#7: "distorted prior" post hoc | Stated as post hoc; "a policy" (No-wait) |
| R1#8: RQ1 wording | Fixed ("lowers the false-clean share of negatives") |
| R1#13 | A4 two seeds stated; MDE under Holm (0.023); oracle as the bound, L1 as counterfactual; IFA caveat; "slightly negative" |
| R2#6 | ODaSC mechanism difference stated |
| R2#7 | Tan 2015 credited for the wait |
| R2#8 | Song & Minku finding stated; Liu 2025 (SCICO) added after reading its abstract |
| R2#9 | Journal-fit paragraph added (2.5) |
| R2#10 | Contributions trimmed to four |

## Clarity (R3)

| Concern | Change |
|:--|:--|
| #2 | Internal AI review disclosed (4.6, Declarations, threats); version-history wording removed; model named |
| #5 | Names unified (ORB-style, lineage tags on ODaSC rows), hypotheses listed (3.4), README maps every table to its file |
| #6 | Fig. 1 legend/log axis/line styles; Fig. 2 markers and panel letters; Fig. 3 redrawn (band-in vs leave-out vs false-clean share, both W) |
| #7 | Threshold rule and second simulator described in Section 3 |
| #8 | Terminology and claim tables numbered; tables renumbered in citation order (1–14); duplicate inline table removed |
| #9 | Abstract single paragraph (233 words); graphical abstract uses AUC |
| #10 | README data section incl. ApacheJIT; legacy block removed; diag command; dev/test split note; torch use explained |
| #11 | Acknowledgements and consent statements added; remaining placeholders need the human authors |

## Not done (stated as limitations)

- Unified ODaSC retune.
- Second learner.
- Adjusted CIs.
- IFA medians.
