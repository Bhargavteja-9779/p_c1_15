# HYPOTHESIS: Two hypotheses written before testing

*Written 2026-11-24T23:10:58+00:00*

H2 (Type C, failure-mode): differences among latency-handling policies in online JIT-SDP G-mean are mainly operating-point (prior-shift) differences. Test: on dev, for every E0 configuration, compare the spread of G-mean@0.5 with the spread of AUC and best-threshold G-mean; it is refuted if the best-threshold ranking of methods matches the @0.5 ranking with similar gaps on the 4 dev projects. I will only extend this analysis to test projects after the method is frozen.
H3 (method): if the operating point is the bottleneck, a threshold set from information available at time T should close most of the gap, without touching labels. Candidate rule, fixed now before testing: choose the threshold at each update so that the share of recent mature commits (age >= the 90th percentile discovery delay estimated by the truncation-corrected estimator) predicted defective matches the share among them already found defective. This uses only labels observable at T. Refuted if it does not beat the best wait/ORB/ODaSC configuration on dev G-mean.
