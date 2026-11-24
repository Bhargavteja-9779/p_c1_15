# DIAGNOSIS: Two causes: a feedback loop with the model prior, and almost no information in age-only soft labels

*Written 2026-11-24T04:05:16+00:00*

I ran scripts/diag_law.py on neutron (dev, seed 0; results/diag_law_neutron.json) and scripts compared delay-survival estimates to the truth (results/diag_survival_dev.txt).
1) The delay estimator is NOT the cause: the Lagakos S(a) is close to the true S(a) on all four dev projects (e.g. neutron at 60% of history: 0.867/0.696/0.462 vs true 0.881/0.728/0.515 at 7/30/90 days).
2) With prior=model, recall-1 decays over time: 0.48, 0.10, 0.15, 0.22 by evaluation quartile, and the predicted-positive rate falls to 0.04 while the true rate is 0.28. The model's own low scores push q down, which teaches the next model lower scores — a self-confirming loop.
3) With prior=base the loop disappears (r1 0.58/0.46/0.52/0.52), but q barely separates truly buggy provisional negatives (mean q 0.086) from truly clean ones (0.061). Most undiscovered bugs are old (S(a) small), so the age-based posterior gives them a small q. In practice LAW becomes near-uniform label smoothing over all unlabeled commits.
4) wait W=30 collapses exactly like law/model (r1 0.24) while W=90 works (0.74): on neutron what matters is whether young commits enter the training set as negatives at all.
