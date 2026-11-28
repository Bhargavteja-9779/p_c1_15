# Draft fragments (cycle 2) — merged into manuscript.md once E7/E8 are analysed

## Related work (organised by the gap)

**Verification latency in online JIT-SDP.** Cabral et al. (ICSE 2019) introduced the waiting-time labelling framework: a commit becomes a training negative only after W days, and positives enter as soon as a fix links back to them. Their ORB method adds class-imbalance boosting on top. Cabral and Minku (TSE 2022) show that drift combined with latency impairs the stability of online JIT-SDP. Song, Minku and Yao (EMSE 2023) find that the choice of W has little effect on the validity of retrospective evaluation. None of these measures *which* missing labels cost predictive performance.

**Label noise from latency.** ODaSC (Song, Li, Minku and Yao, IJCNN 2022) formulates the one-sided label noise that waiting-time labelling causes and down-weights low-confidence clean labels using feature-space micro-clusters. It is the strongest baseline in this paper and, on held-out data, our latency-aware weighting does not beat it.

**Human labelling.** HumLa (Song and Minku, FSE 2023) lets developers inspect commits the model flags, which shortens latency for those commits. Liu et al. (Sci. Comput. Program. 2025) revisit HumLa with non-zero inspection time and observed-label evaluation. Both choose which commits to inspect by predicted risk; our E9 dev grid found no better choice.

**Delayed feedback outside software engineering.** Conversion-rate prediction treats late conversions as positive-unlabeled data: DFM (Chapelle, KDD 2014) gives the posterior weight p S(a)/(1-p+p S(a)) that our LAW uses, and FSIW, ES-DFM, DEFER, DEFUSE and ULC refine it. Multi-head online learning (Gao and Yang 2022) trains separate heads per delay window to trade freshness against correctness. In continual learning, Csaba et al. (NeurIPS 2024) show accuracy falls as label delay grows and rehearse samples similar to the newest unlabeled data. These works motivate freshness, but none decomposes the cost of latency by label age on software data.

**Truncated delay estimation.** The reverse-time product-limit estimator for right-truncated data (Lagakos et al., Biometrika 1988; Kalbfleisch and Lawless, JASA 1989) is standard in epidemiological nowcasting. We used it for the discovery-delay distribution; it had no measurable effect (E2).

**Recalibration under delayed labels.** A 2026 replication package (Zenodo 24527309) compares recalibration against retraining for JIT-SDP under limited and delayed labels on ApacheJIT. Our finding that the latency-corrected threshold carries most of the G-mean gain must be read against it.

## Experimental setup (stable parts)

- **Data.** (i) Cabral et al. ICSE'19 artifact (Zenodo 2591761, sha256 recorded in literature/data_sha256.txt): 14 GitHub projects, 14 Kamei change metrics, commit and discovery times. Split once by a seeded draw before modelling: dev = fabric, neutron, nova, sentry; test = the other 10. (ii) ApacheJIT (Keshavarz and Nagappan, MSR 2022; Zenodo 5907847): 8 Apache projects with >= 2000 commits that do not overlap the Cabral test set; discovery time = earliest linked fix date; 'lt' unavailable (set to 0). ApacheJIT was untouched until plan_v4 was written.
- **Simulation.** Prequential test-then-train. The learner (class-balanced LightGBM, 150 trees) is retrained every 100 commits after a 500-commit warm-up, on labels observable at that time. Predictions are made at commit time and scored against the final dataset label; the last 365 days are excluded from scoring.
- **Label policies.** oracle (upper bound), nowait, wait-W, ORB-W, ODaSC-W (kNN stand-in for DenStream micro-clusters), LAW (proposed in cycle 1).
- **Thresholds.** fixed 0.5, or gmax_lat: maximise G-mean over the last 2000 scored commits with not-yet-found commits given a soft positive weight from the delay distribution. Baselines received the same threshold option.
- **Tuning budget.** All 44 configurations (proposed and baselines) were tuned on dev only, 3 seeds each.
- **Seeds.** Explore 0-2; confirmation 100-104 (fixed before any run).
- **Statistics.** Per-project means over seeds; paired two-sided Wilcoxon over projects; Holm correction within each family; 10,000-sample bootstrap 95% CI of the mean paired difference; non-trivial margin 0.02 G-mean.
- **Hardware.** 4 CPU cores, 15 GB RAM, no GPU.
