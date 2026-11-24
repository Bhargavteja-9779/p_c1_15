# BREAKTHROUGH: (dev only, not yet confirmed) a mature, cross-fitted scorer finds dormant bugs and beats tuned waiting on all four dev projects

*Written 2026-11-24T15:52:36+00:00*

E0c (dev x seeds 0-2): lawm_soft_W30 mean dev G-mean 0.755 vs orb_W90 0.724 (best tuned baseline) and oracle 0.794; per project 0.688/0.837/0.802/0.693 vs 0.653/0.817/0.788/0.637 (fabric/neutron/nova/sentry). The mature scorer separates dormant bugs from clean old provisional negatives with AUC 0.756-0.930 (mean q 0.087-0.180 vs 0.016-0.019). The count (hard-drop) mode is worse (W30 collapses recall-1 on neutron, 0.31), so soft weighting matters. This is dev evidence chosen among 4 configs; it is NOT a result until the frozen config is confirmed on the 10 held-out projects with SEEDS_CONFIRM. H4 supported on dev.
