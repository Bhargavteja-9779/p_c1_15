# RESULT: E1 on 10 held-out projects confirms the negative result for LAW and awt

*Written 2026-11-24T15:00:34+00:00*

E1, 10 test projects x SEEDS_CONFIRM (results/statistics.json, E1_H1_family...): mean G-mean oracle 0.715, orb_W90 0.658, wait_W90 0.654, awt_e0.4 0.619, law_lagakos_model 0.616, nowait 0.429. LAW vs wait_W90: -0.038 (95% CI -0.085..0.001), 3 wins / 7 losses, Holm p (family of 6) 0.25; vs orb_W90: -0.042 (CI -0.091..-0.003), 2/8, Holm p 0.25. awt vs orb_W90: -0.039 (CI -0.077..-0.009), 2/8, Holm p 0.15. Both only beat nowait (+0.19, 10/10, Holm p 0.012). H1 is not supported on held-out data, as dev predicted.
Side observation (NOT pre-registered, exploratory): LAW has the highest mean AUC among non-oracle methods (0.751 vs 0.727 wait_W90 and 0.724 orb_W90) but recall-1 0.453 vs 0.713: it ranks better and thresholds worse.
