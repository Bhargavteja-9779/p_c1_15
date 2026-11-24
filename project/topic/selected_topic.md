# Topic selection (cycle 1, 2026-11-24)

## Constraints that shaped the choice
- Venue: JKSU-CIS (broad CS/AI; publishes software-engineering ML, e.g. JIT defect prediction — see literature/).
- Machine: 4 CPU cores, no GPU, 15 CPU-h per cycle → no large-model training.
- Public data with licence, standard protocol, reproducible baselines.

## Candidates considered (≥ 10)
| # | Candidate | Verdict | Reason |
|---|---|---|---|
| 1 | **Verification-latency–aware online JIT defect prediction via delayed-feedback correction** | **SELECTED** | Public data with discovery times (Cabral et al. 2019, Zenodo 2591761, 14 projects); real practical problem; CPU-cheap; specific gap (no PU/delayed-feedback correction found in JIT-SDP prior-art search so far) |
| 2 | NIDS cross-dataset generalisation (CIC-IDS2017 → UNSW-NB15) | rejected | Overcrowded; known dataset flaws dominate; large downloads behind forms |
| 3 | Label-noise-robust GBDT for tabular data | rejected | Close to confident learning (Northcutt et al. 2021); weak differentiation |
| 4 | Lightweight time-series forecasting (DLinear-style) on ETT | rejected | Overcrowded; "trivial architecture swap" risk |
| 5 | Calibration of GBDTs under natural temporal shift (folktables) | rejected | Close to TableShift/WhyShift benchmarks; mainly negative-result potential |
| 6 | LLM-based commit risk assessment | rejected | Buzzword; needs GPU/API |
| 7 | Federated IoT intrusion detection | rejected | Buzzword-driven, crowded, synthetic splits |
| 8 | Cross-project defect prediction with transfer learning (PROMISE/NASA) | rejected | Very crowded; NASA MDP quality problems |
| 9 | Plant-disease image classification with small CNNs | rejected | Needs GPU for credible baselines; crowded in venue |
| 10 | Feature selection metaheuristic (e.g. new "whale/xyz optimizer") | rejected | Metaphor-based metaheuristics are a known novelty anti-pattern |
| 11 | Phishing-URL detection robustness to temporal drift | rejected | Data licences unclear; datasets small and leaky |
| 12 | Concept-drift detection for JIT-SDP | kept as fallback | Same data; but several recent papers (drift detection via model interpretation, 2025) |

## Selected topic
**Problem.** In just-in-time software defect prediction (JIT-SDP) a model flags risky commits at commit time and is retrained as new labels arrive. A commit's label is *not* known when it is made: a defect it introduced is discovered only when a later bug-fix commit points back at it. In the 14 projects of Cabral et al., the median delay from commit to discovery is 16–416 days per project and the 90th percentile is 383–1964 days (our reconstruction, `src/data.py`). Every "clean" commit used for training is therefore only provisionally clean.

**Who it hurts.** Teams that rely on online JIT-SDP for code review triage: the model learns from mislabelled recent commits (false "clean"), or waits W days and learns from stale data.

**WHAT EXISTS.** (i) The waiting-time rule: treat a commit as clean only after W days (Cabral et al., ICSE 2019; ORB), with W trading label noise against staleness (Cabral & Minku, TSE 2022; Song, Minku & Yao, EMSE 2023). (ii) A human-labelling procedure (Song & Minku, FSE 2023). (iii) Outside SE, the delayed-feedback literature for conversion-rate prediction treats late conversions as a positive-unlabeled problem and corrects with elapsed-time models or importance weights (Chapelle 2014; Yasui et al. 2020 FSIW; ES-DFM 2020; DEFUSE 2022).
**WHAT IS MISSING.** JIT-SDP methods use a hard waiting-time cutoff. No JIT-SDP work found so far models *how likely* a provisionally-clean commit is to be a still-undiscovered defect as a function of its age (discovery-delay distribution), and uses that to use recent data without its label noise. *(To be re-verified with ≥ 8 query phrasings before any novelty claim.)*
**WHY IT MATTERS.** Hard cut-offs throw away the freshest data (bad under concept drift) or inject label noise. Using the delay distribution may give both freshness and cleaner labels.

**Hypothesis (H1).** Re-weighting provisionally-clean commits by the posterior probability that they are undiscovered defects — computed from a Kaplan–Meier estimate of the discovery-delay distribution and the current model's score — improves prequential G-mean over the best waiting-time baseline when evaluated against final labels.

**Research questions.**
- RQ1: How much label noise does the waiting-time rule inject, and how does it depend on commit age and project? (failure-mode characterisation)
- RQ2: Does latency-aware weighting beat waiting-time baselines (W tuned on dev projects) on held-out projects?
- RQ3: Which component matters (delay model vs. model-score posterior vs. using fresh data)?
- RQ4: Is the gain robust to label-delay severity (simulated slower discovery) and to class imbalance?
- RQ5: What does it cost (training time per update)?

**Datasets & licence.** Cabral et al. ICSE'19 artifact, Zenodo record 2591761 (licence "other-open", see data/jit/License.txt): 14 GitHub projects, 7.9k–48.9k commits each, 14 Kamei change metrics, commit timestamps, defect labels, discovery-event rows.
**Protocol.** Projects split once by a seeded random draw (seed 0, before any modelling) into **dev = {fabric, neutron, nova, sentry}** (all tuning and method development) and **test = 10 remaining projects** (touched only by the frozen confirmation run).
**Baselines.** No-wait (face-value labels); Wait-W (W tuned on dev from {15, 30, 60, 90, 180}); ORB-style imbalance-aware online bagging (reimplemented, same tuning budget); FSIW-style importance weighting; Oracle (true labels, upper bound, not a competitor).
**Metrics.** Primary: prequential G-mean of per-class recalls against final labels (as in Cabral et al.); secondary: recall-1, recall-0, |R1−R0|, ROC-AUC, MCC.
**Compute estimate.** One prequential run (one project, one method, one seed, retraining every 30 days) ≈ 5–60 s CPU; full E1–E6 ≈ 2–4 CPU-h, well within 15 h.
