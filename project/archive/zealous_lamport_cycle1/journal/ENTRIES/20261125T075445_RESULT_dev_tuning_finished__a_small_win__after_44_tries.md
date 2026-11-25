# RESULT: Dev tuning finished: a small win, after 44 tries

*Written 2026-11-25T07:54:45+00:00*

All 528 dev runs are done (tables/E0_dev_tuning.csv). The only configuration above the best baseline is LAW with the model prior PLUS the latency-corrected G-mean threshold: mean dev G-mean 0.763 (fabric 0.713, neutron 0.828, nova 0.800, sentry 0.713), against ODaSC-W30 at 0.750 and ODaSC-W15 with the same threshold at 0.749. It loses on nova (0.800 vs 0.817). The threshold alone lifts most methods (wait-W30: 0.621 -> 0.744; nowait: 0.385 -> 0.688), which supports H2. The rate-matching rule I pre-registered as H3 does not work (LAW-base 0.678, nowait 0.633), so H3 as written is refuted. The G-mean rule I tested alongside it works.
I tried 44 variants on dev and the margin is +0.013, below the 0.02 I fixed in plan_v1. I expect the test margin to shrink. I froze the configuration (plan_v3, state/frozen_config.json) and will run the confirmation on the 10 untouched projects.
