# RESULT: E8 fresh ApacheJIT confirmation: H6 fails; H3 replicates on a second dataset; dual ranks first among non-oracle methods (descriptive)

*Written 2026-11-25T21:37:55+00:00*

plan_v7 E8: 9 ApacheJIT projects x 5 confirm seeds x 9 methods, 405 runs, configs frozen on Cabral dev (frozen_config_v6.json); tables/E8_summary.txt, results/statistics.json.
Mean G-mean over 9 projects: oracle 0.770, decomp_L1_W30 (diagnostic, true labels) 0.762, dual_W30_k50 0.735, lawm_soft_W30 0.728,
odasc_W30_t0.8 0.718, wait_W90 0.716, orb_W90 0.706, wait_W30 0.687, nowait 0.648.
H6 (pre-registered primary = best dev candidate = odasc_W30_t0.8 vs wait_W90/orb_W90, Holm over 2): +0.0012 (p_holm 0.60), +0.0114 (0.60) -> FAIL.
Descriptive (NOT confirmatory; these candidates were not the pre-registered primary): dual_W30_k50 vs odasc +0.0175, CI [0.003, 0.032], 8/9 wins, Wilcoxon p=0.055 (min attainable two-sided p with 8/1 split at n=9 is ~0.04);
vs orb_W90 +0.0288, CI [0.006, 0.052]; vs wait_W90 +0.0186, CI [-0.003, 0.040]. AUC: dual 0.808 vs odasc 0.788 vs wait_W90 0.787.
Interpretation (careful): dual's dev failure was driven by one project (nova, AUC 0.36); on fresh data it is the best real method in mean, but this is exactly the kind of post-hoc observation that must NOT be claimed as a confirmed win.
H3 secondary replicated: decomp_L1_W30 beats wait_W90 on 9/9 (Holm p=0.0078), recovers 0.90 of the wait->oracle gap -> the latency cost is mostly label noise (dormant bugs among provisional negatives), on two dataset families.
ApacheJIT is now USED as a confirmation set. Any new confirmation needs another untouched dataset.
