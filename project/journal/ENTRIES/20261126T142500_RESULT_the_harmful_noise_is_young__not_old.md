# RESULT: The harmful noise is young, not old

*Written 2026-11-26T14:25:00+00:00*

plan_v8 A2–A4 are complete (1110/1110 runs in results/review1/raw.jsonl; tables T8–T10).

**A3, age strata at W = 30.** True labels are given only to training commits in one age band. Commits aged 30–180 days carry almost the whole gain:
- Cabral test: G-mean +0.093 = 0.913 of the full-relabel gain, 10/10 projects, p = 0.002; AUC 0.827 of the gain.
- ApacheJIT: +0.051 = 0.685, 9/9, p = 0.0039.

The 180–365-day band adds a little on Cabral (0.153) and nothing on ApacheJIT. Bands of 365 days and more add nothing, or slightly hurt.

This **refutes** the explanation in manuscript v1, and R2's reading of it, that "a recency cut-off fails because the noise is old". The harmful false-clean labels are commits that are 1–6 months old when the model retrains: past any practical wait, but not yet discovered. Waiting longer would remove them only together with all fresh data (the freshness cost measured at W = 90). This changes the story for the better. Age-only weighting fails not because the noise is old, but because within 30–180 days age alone cannot separate the defective commits from the clean ones.

**A2, ApacheJIT W = 90.** The noise share of the Wait-90 → oracle gap is 0.652 [0.534, 0.772] in G-mean and 0.779 [0.718, 0.851] in AUC. On Cabral test it is 0.498 [0.266, 0.709] and 0.437 [0.325, 0.539]. So at the tuned wait the penalty is split between noise and lost freshness, and the split depends on the dataset. C1 must be conditional on W.

**A4, evaluation window excluding the last 730 days.** The W = 30 decomposition is stable:
- Cabral share 1.057, L1 vs Wait-30 +0.0999 (10/0);
- ApacheJIT share 0.904, +0.0781 (8/1).

Dormant evaluation labels do not drive it.
