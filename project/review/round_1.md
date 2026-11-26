# Review round 1: triage and response (manuscript v1 → v2)

Reports: `round_1_R1.md` (methodology/statistics, 5/10), `round_1_R2.md` (novelty, 5/10), `round_1_R3.md` (clarity/reproducibility, 6/10). All three recommended major revision.

New evidence was produced by `experiments/plan_v8_review1.yaml`, committed before the runs: 1,110 runs in `results/review1/raw.jsonl`, plus the Shapley analysis and the test-set usage scan.

Status key: **F** = fixed in text; **E** = new evidence; **R** = rebuttal or limitation.

## Reviewer 1 (methodology and statistics)

| # | Concern | Status | Response |
|:--|:--|:--|:--|
| 1 | "Mostly noise" only at W=30; W=90 share omitted; no ApacheJIT W=90 | E+F | A2 ran L1/L2 at W=90 on ApacheJIT. Table 4 reports the W=90 split for both families. Abstract, C1 and the conclusion are now conditional on W. "Excluding young negatives costs little" was removed. |
| 2 | Fixed-threshold G-mean, path dependence, shares >1 | E+F | 2×2 factorial with Shapley split and bootstrap CIs (Table 4). AUC is primary. Why L1 > oracle in G-mean is explained. Shares >1 are not interpreted. |
| 3 | "9/9" wrong (8/1); kafka negative-denominator ratio | F | Corrected to 8/1. Per-project ratios removed; Fig. 2 shows absolute differences. kafka is noted. |
| 4 | Test-set reuse understated | E+F | `scripts/test_set_usage.py` scans all 170 result-bearing commits on all branches: 27 full configurations plus 3 smoke-only (Table S3). Section 4.6 rewritten. Cabral is declared not a hold-out; ApacheJIT is the only confirmatory set. RQ5 was rerun on ApacheJIT (A5). |
| 5 | Two ODaSC implementations; lineage-2 version beats Wait-90 10/0; budgets | E+F+R | Both implementations reported, including lineage 2 vs Wait-90 (+0.0407, 10/0) and on ApacheJIT (0.718 vs 0.716). Per-family budget counts given. A unified retune was not run because it would be another selection round on used test sets; this is stated as a deviation and a limitation. River ODaSC: never reached test (Section 4.6). |
| 6 | RQ5 confounds threshold with policy; primary hypothesis failed; dev-only C4 | E+F | Like-for-like design on fresh data (H9b). The failed primary hypothesis is stated. The threshold claim is narrowed to policies with a distorted prior. Spread at best threshold remains a dev diagnostic and is labelled as such. |
| 7 | Pre-registration claims inaccurate; six-test Holm; dropped analyses | F | "Frozen before any held-out run" removed. "Pre-registered" defined. Six-test Holm values reported (0.252, 0.148, 0.0117). Deviations table added (Table 12). |
| 8 | Wilcoxon power statement wrong | F | Exact values given (0.0039 for 9/0, 0.0078 for 8/1). An MDE for H6 is added (0.02 at 80% power with SD 0.0192). |
| 9 | CIs unadjusted vs Holm | F+R | Stated explicitly. Results are treated as significant only by Holm p. We did not switch to adjusted intervals, to keep continuity with the frozen plans. |
| 10 | Seeds add little | F | Seed SD reported (median 0.0022); limitation stated. A second learner is not run (limitation). |
| 11 | Leakage test coverage | E+F | Tests extended: dual, decomposition, both threshold rules, binary decisions, flipped final labels of undiscovered commits, a Cabral and an ApacheJIT project. |
| 12 | ORB not faithful | F | Renamed ORB-style; the double correction is stated. The no-class-balancing variant was not run (limitation). |
| 13 | Delay-estimator diagnostic selective | F | Table S1 covers all projects and time points. Text gives mean/max error and both error directions. |
| 14 | Inconsistencies (AWT, 0.34, Table 7 rows) | F | AWT wording fixed. The 0.34 sentence removed. Table 9 caption marks the shared deterministic rows. |
| 15 | Evaluation-label dormancy; ApacheJIT fix-before-commit | E+F | A4 (exclude the last 730 days): result unchanged (Table S4). The 2 fix-before-commit cases are reported. The sampled-stream cadence is a threat. |

## Reviewer 2 (novelty and related work)

| # | Concern | Status | Response |
|:--|:--|:--|:--|
| 1 | C1 overstated vs Falessi/Fan noisy-vs-clean | F | The design is credited. The contribution is restated as the online setting plus noise/freshness separation plus age localisation. |
| 2 | Order dependence | E | Shapley split (Table 4). |
| 3 | RQ2 only G-mean@0.5 | E | AUC is primary, G-mean secondary (Table 4). |
| 4 | "Old" not tested | E | A3 age strata (Table 5, Fig. 3). **The "old noise" explanation is refuted**: the harmful labels sit on commits aged 30–180 days. The story is rewritten accordingly. |
| 5 | Reconcile with Song EMSE 2023, Song & Minku TSE 2023, ODaSC-opt | F/R | Song et al. 2023a and Song & Minku 2023 are discussed. "ODaSC-opt" could not be located as a separate verifiable publication, so it is not cited. |
| 6 | C4 row inaccurate | F | Claim table rebuilt; C5 row cites ORB and Cabral & Minku 2023 with verified content. Pessoa 2021 and the arXiv item could not be verified and are not cited. |
| 7 | Abstract uses dev numbers | F | The abstract uses held-out and fresh numbers only. |
| 8 | Wording | F | "Contradicts" changed to "refines". L2 now reported for both families at W=90. SZZ-final alignment stated. |
| 9 | Missing related work | F | 13 added and DOI-checked: Tan 2015, Kim 2011, Tantithamthavorn 2015, Liu 2023, Herbold 2022, Vandehei 2021, McIntosh & Kamei 2018, Falessi 2020, Zliobaite 2010, Souza 2015, Plasse & Adams 2016, Gomes 2023, Song & Minku 2023. SCICO 2025 is not cited because its content was not verified for our claims. |
| 10 | Reference names | F | Di Penta, De Gruttola and Fujita fixed (`scripts/build_references.py`). |
| 11 | C3 is about the kNN adaptation | F | Stated in the C4 row and in threats. |
| 12 | Evaluation dormancy | E | A4. |

## Reviewer 3 (clarity, reproducibility, ethics)

| # | Concern | Status | Response |
|:--|:--|:--|:--|
| 1 | README cannot reproduce tables | F | The README maps every table and figure to a command; the fast path regenerates all numbers. |
| 2 | Checksum not asserted | F | Zip and per-ARFF SHA-256 values are asserted. |
| 3 | Data cleaning undocumented | F | Section 4.1 covers copy rows, unmatched copies (991) and dropped commits; Table S2 compares counts with MSTDP. |
| 4 | Leakage claim | E+F | See R1#11. |
| 5 | Pre-registration definition; deviations | F | Section 4.6 and Table 12. |
| 6 | AI and lineage disclosure | F | Section 4.6 and the Declarations describe the sessions, branches and lineages. Authors must complete the AI statement. |
| 7 | Declaration placeholders, code DOI | R | These require the human authors (cannot be filled by the agent). |
| 8 | Fig. 2 bug, titles, few figures | F | Fig. 2 redrawn (absolute differences, no in-image title); Fig. 3 added. |
| 9 | Wilcoxon statement | F | See R1#8. |
| 10 | Share >1 | F | See R1#2. |
| 11 | No variability; supplementary unlabeled | F | CIs in Table 4, p values in Table 5, seed SD; supplementary S1–S5 listed. |
| 12 | RQ5 abstract overstated | F | Now based on fresh-data results. |
| 13 | Terminology | F | Terminology table added. |
| 14 | Limitations | F | Single learner, kNN ODaSC, constant lt, unrun E5/E6/E7. |
| 15 | Reference list short | F | 44 references. |

## Change of story

The most important change is to the story itself. v1 said the harmful noise is *old* dormant defects. A3 shows it is commits one to six months old. The paper now says this, and lists the earlier explanation among the things that did not hold (Section 6.3).
