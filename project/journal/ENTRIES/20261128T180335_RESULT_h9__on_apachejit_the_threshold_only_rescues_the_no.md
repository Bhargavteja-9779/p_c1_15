# RESULT: H9: on ApacheJIT the threshold only rescues the no-wait policy

*Written 2026-11-28T18:03:35+00:00*

E10 complete (8 ApacheJIT projects x seeds 100-104; results/statistics.json E10_H9_threshold_vs_label_policy).
Gain from the latency-corrected threshold over the fixed 0.5 threshold: nowait +0.0564 (CI [0.0236, 0.0934], 8/8 projects, Holm p = 0.031), wait-W90 +0.0049 (p = 1.0), ORB-W90 +0.0002 (p = 1.0), ODaSC-W30 +0.0045 (p = 0.74), LAW +/- model prior -0.0006. H9a fails: the threshold matters only for the policy whose newest negatives are wrong (nowait).
Thresholded label policies span only 0.0144 G-mean (0.7115 to 0.7259), below the mean threshold gain 0.0165, so H9b passes, but narrowly and only because of nowait. I will not present H9b as a strong finding.
What both benchmarks do agree on: once the newest provisional negatives are handled by any reasonable mechanism (waiting, re-weighting or a latency-aware threshold), all label policies land within about 0.015 G-mean of each other on ApacheJIT and within about 0.02 on the Cabral test projects (E1: 0.6759 to 0.6961 for the thresholded or confidence-based ones), while the oracle stays about 0.02-0.04 G-mean and 0.05-0.06 AUC above. The remaining cost of latency is in ranking, not in the label policy.
