# Submission readiness — JKSU-CIS (assessed 2026-11-25, branch claude/zealous-lamport-bjc4um)

Every number below comes from a result file in this repo (path given). Nothing is estimated or rounded up.

## 1. Bottom line

**The project is not ready to submit as a "new, better method" paper, and no one can promise acceptance.**
In three separate confirmation runs on held-out data, none of our proposed methods beat the strongest baseline (ODaSC-style) with statistical significance. A manuscript claiming otherwise would be false, and a reviewer who reruns the code would find out.

What we *do* have is a rigorous empirical result that can honestly support a paper. Section 4 sets out two routes.

## 2. What has been improved (verified)

| Area | Before (handoff, 2026-11-24) | Now |
|---|---|---|
| Baselines | wait / ORB only | + ODaSC-style (closest prior work, IJCNN 2022), same tuning budget; + thresholded versions of every baseline |
| Protocol | one pre-specified method, untested | prequential online simulation with verification latency; project-level dev/test split; leakage tests for every method (`tests/test_no_future.py`); frozen pre-registered plans before every test run |
| Confirmation data | none | Cabral test projects (10 × 5 seeds) **and** a fresh dataset: ApacheJIT (9 projects × 5 seeds) |
| Prior art | 5 papers | 41+ papers opened (`state/novelty_ledger.json`); credited Chapelle's delayed-feedback weight; found that a reference in MSTDP (Liu 2024a) does not exist |
| Forking-paths honesty | — | every variant logged (`state/variants_tried.csv`); multiplicity reported |

**Results that hold up statistically:**
- **Beats the waiting-time methods** of Cabral et al. (ICSE 2019) on the 10 held-out Cabral projects. LAW with the latency-corrected threshold gains +0.042 G-mean over Wait-W90 and +0.038 over ORB-W90, Holm-corrected p = 0.0195, 9/10 project wins (`archive/zealous_lamport_cycle1/results/statistics.json`).
- **Where the latency cost comes from.** Label noise in the waited-out training set accounts for **90 % of the gap** between the waiting rule and the oracle. This holds on 9/9 fresh ApacheJIT projects (per project 75–98 %, Holm p = 0.0078) and on 10/10 Cabral test projects (`results/statistics.json` → `E8_secondary_H3_*`). It is a diagnostic that uses true labels, not a deployable method.
- **The operating point dominates.** Most of the G-mean differences between latency-handling methods come from where scores cross the 0.5 threshold, not from ranking quality. The spread of G-mean@0.5 across methods (0.25–0.82) collapses at each method's best threshold (0.77–0.84) (`archive/zealous_lamport_cycle1/results/diag/operating_point_dev.csv`, dev only).

**Results that do NOT hold:**
- LAW + threshold vs ODaSC-W30 on Cabral test: +0.0009, 95 % CI [−0.009, +0.011], Holm p = 1.0.
- Best candidate on ApacheJIT (`dual_W30_k50`) vs ODaSC: +0.0175, CI [0.003, 0.032], 8/9 wins, but Holm p = 0.16. Descriptive only; not significant.
- Our pre-registered success criterion was ≥ +0.02 with Holm p < 0.05. That criterion (gate G5) fails.

## 3. Comparison with papers in the target journal

Source: `literature/jksu_benchmark.md` (24 JKSU-CIS papers, opened in full text).

| | **MSTDP** (JKSU-CIS 2026, the only JIT-SDP paper in the journal since 2023) | **Typical JKSU-CIS method paper** (24 surveyed) | **Ours** |
|---|---|---|---|
| Setting | offline, one chronological 80/20 split | mostly offline | online prequential, retrain every 100 commits |
| Verification latency | ignored: training uses final labels, including commits that would still look clean at deployment | n/a | modelled explicitly; this is the problem studied |
| Seeds / repetitions | one split, none reported | 0–30 runs; many report none | 3 dev + 5 confirmation seeds |
| Statistics | Wilcoxon over 9 projects; tested metric not stated | Friedman/Nemenyi, Wilcoxon, t-tests; several report none | Wilcoxon + Holm, bootstrap 95 % CI, effect sizes, pre-registration |
| Datasets | 9 projects (same Cabral data as ours) | 1–26 | 14 Cabral + 9 ApacheJIT |
| Claim | beats 7 baselines | beats baselines | ties the strongest baseline; beats the waiting-time ones |
| Reference integrity | cites Liu 2024a, which we could not find; its neighbour (Liu 2024b) also fails | — | all references DOI-checked |

**Comparability:** MSTDP's numbers (accuracy/F1/AUC, offline) are **not directly comparable** with ours (prequential G-mean under label delay). Under our protocol an offline model trained on final labels corresponds to the "oracle", which nothing deployable can reach. So we cannot honestly claim to "beat MSTDP".

**Why this matters for acceptance:**
- Our methodology is stricter than any paper in the survey.
- But every accepted paper in the survey reports a method that wins.
- Reviewers at this journal will ask "what is the improvement?". Today our honest answer is "a tie with ODaSC".

## 4. Two honest routes to a submission

**Route A — empirical/diagnostic paper (writable now, supported by the evidence)**
- Working title: *Where does verification latency hurt online just-in-time defect prediction? An empirical decomposition on 23 projects.*
- Contributions, each backed by a result file:
  - (i) a latency-cost decomposition: 90 % of the cost comes from label noise, replicated on fresh data;
  - (ii) the operating-point finding;
  - (iii) a reproducible protocol plus code;
  - (iv) a statistically supported negative result: age-based (LAW) and feature-based (ODaSC) label confidence are tied, and both beat the waiting rule.
- Risk: JKSU-CIS mostly publishes method papers, so the fit is uncertain. An empirical-SE venue would fit better, but G1 already selected this journal for turnaround.

**Route B — keep iterating on a method (owner directive in USER_DIRECTIVES.md)**
- Next step from the main lineage's HANDOFF: plan_v8 (dev only), a latency-corrected neighbour posterior to fix the `dual` method's failure on nova.
- It then needs an **untouched** confirmation dataset, because Cabral test and ApacheJIT are already used.
- Success is not guaranteed. The ApacheJIT signal (+0.0175 vs ODaSC, 8/9 wins) suggests it is worth one more round.

## 5. Gate status (main lineage, see HANDOFF.md)

| Gate | Status |
|---|---|
| G1 journal | pass (marginal: median 71–74 d turnaround; 2025 quartile UNVERIFIED) |
| G2 prior art | pass on count (41+ opened) |
| G3 novelty ≥ 20/25 | **fail** (self-score 11–14/25) |
| G4 baselines | pass with caveat |
| G5 main result | **fail** |
| G6 ablation | fail / incomplete |
| G7 generalisation | pass (the latency-cost decomposition replicates on fresh data) |
| G8 leakage | pass |
| G9 reproducibility, G10 review, G11 audit | not yet run |
