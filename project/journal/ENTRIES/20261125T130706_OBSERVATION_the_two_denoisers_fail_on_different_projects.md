# OBSERVATION: The two denoisers fail on different projects

*Written 2026-11-25T13:07:06+00:00*

results/diag_threshold_dev.json (dev, seed 0): lawm_soft_W30 vs odasc_W30_t0.8 G-mean: fabric 0.689 vs 0.713, neutron 0.836 vs 0.781, sentry 0.693 vs 0.715. Threshold tuning in hindsight adds at most ~0.02 to either, so the difference is in which commits they relabel, not in calibration. The mature scorer is strong where defects have long delays and the history is rich (neutron, dormant-bug AUC 0.93); the neighbourhood rule is strong where it is weaker. My hypothesis H5: combining both evidence sources (noisy-OR) beats each.
