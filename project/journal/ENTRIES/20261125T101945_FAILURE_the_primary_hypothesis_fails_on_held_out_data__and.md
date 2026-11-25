# FAILURE: The primary hypothesis fails on held-out data, and the truncation estimator does nothing

*Written 2026-11-25T10:19:45+00:00*

G5 fails: LAW does not beat ODaSC (+0.0009, p = 0.77). ODaSC even ranks commits better on test (AUC 0.7621 vs 0.7506, LAW lower on 7/10 projects), reversing what I saw on dev. The partial ablation (E2, 68/200 runs) shows the Lagakos right-truncation estimator adds nothing over the naive empirical CDF (+0.0001), so the one component I thought was new has no measurable effect. The threshold component is what matters (+0.0687 over LAW without it). My best explanation: once the decision threshold is corrected for latency, every reasonable label policy lands close to the oracle. The oracle with immediate true labels reaches only 0.7148, just 0.019 above LAW. The headroom left for a better label policy on G-mean is smaller than the 0.02 margin I set. The remaining loss is in ranking (oracle AUC 0.8154 vs best 0.7640), not in decisions.
