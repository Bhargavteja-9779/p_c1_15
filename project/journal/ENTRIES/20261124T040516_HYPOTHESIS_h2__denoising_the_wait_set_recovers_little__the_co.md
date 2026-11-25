# HYPOTHESIS: H2: denoising the wait set recovers little; the composition effect dominates (written before E0b)

*Written 2026-11-24T04:05:16+00:00*

H2a: on dev, decomp level 1 (true labels on the wait(W) set) improves G-mean over wait(W) by less than one third of the oracle-wait gap.
H2b: awt with a single eps matches the best per-project fixed W more closely than the single dev-tuned W* does (to be tested on test projects only if awt survives dev).
Things that would prove me wrong: level 1 closes most of the gap (then noise matters and LAW-type correction is the right direction).
