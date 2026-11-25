# HYPOTHESIS: H4: a scorer that never sees its own predictions can find dormant bugs (written before E0c)

*Written 2026-11-24T15:04:02+00:00*

Cycle 1 told me the penalty is old undiscovered bugs, that age alone cannot find them, and that the online model's own scores reinforce themselves. So I train separate scorers only on commits older than a year (labels nearly final), cross-fitted so no commit is scored by a model trained on it, and use their probability together with the delay survival S(a) to give each old provisional negative a dormant-bug posterior. A first sanity run on fabric seed 0 (dev) gives G-mean 0.689 vs wait_W30 0.657, and the posterior now separates truly buggy from clean (mean q 0.103 vs 0.019; scorer AUC for dormant bugs 0.756). H4: the best of 4 lawm configs beats orb_W90 (0.724) on mean dev G-mean. I expect the gain to be largest on neutron/nova (long delays).
