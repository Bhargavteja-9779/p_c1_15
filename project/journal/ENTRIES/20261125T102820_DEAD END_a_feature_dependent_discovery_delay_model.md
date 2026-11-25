# DEAD END: A feature-dependent discovery-delay model

*Written 2026-11-25T10:28:20+00:00*

I considered replacing LAW's population-level S(a) by a feature-dependent S(a|x), a mixture-cure model, in case some kinds of change are found faster. Dev check D2 (scripts/diag_delay_predictability.py -> results/diag/d2_delay_predictability.json): LightGBM trained on the earliest 70% of discovered defects predicts log-delay of the latest 30% with Spearman rho 0.061 (fabric), 0.130 (neutron), -0.001 (nova), 0.047 (sentry). Commit features carry almost no information about how long a defect stays hidden. Abandoned; the population S(a) is adequate.
