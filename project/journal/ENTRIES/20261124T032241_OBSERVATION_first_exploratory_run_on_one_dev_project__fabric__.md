# OBSERVATION: First exploratory run on one dev project (fabric, seed 0)

*Written 2026-11-24T03:22:41+00:00*

Before freezing anything, I ran each method once on fabric (a dev project) to check the code. G-mean: oracle 0.751, nowait 0.474, wait W=90 0.636, ORB-style (after fixing a bug where class re-balancing cancelled the ORB factors) 0.655, LAW 0.670. The no-wait baseline almost never flags defects (R1 0.233) because recent defects are mostly still labelled clean. Wait-90 swings the other way (R0 0.479, R1 0.844): recent commits only enter training if they are already known to be buggy, so the newest data is positive-heavy. LAW sits between them (R0 0.825, R1 0.545). One project and one seed: not evidence, just a sanity check. These runs are logged in variants_tried.csv as exploratory.
