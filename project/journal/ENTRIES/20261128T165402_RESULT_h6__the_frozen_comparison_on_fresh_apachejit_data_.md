# RESULT: H6: the frozen comparison on fresh ApacheJIT data is a tie everywhere

*Written 2026-11-28T16:54:02+00:00*

E8 is complete (8 ApacheJIT projects x seeds 100-104 x 8 frozen variants; results/statistics.json E8_H6_replication_apachejit, tables/E8_*).
Mean G-mean: oracle 0.7627, LAW 0.7259, ODaSC-W15+threshold 0.7256, Wait-W30+threshold 0.7219, ODaSC-W30 0.7207, Wait-W90 0.7172, ORB-W90 0.7114, nowait 0.6551.
LAW vs ODaSC-W30: +0.0052, 95% CI [-0.0208, 0.0295], Wilcoxon p = 0.64. LAW vs Wait-W90: +0.0087, CI [-0.0109, 0.0280], p = 0.55, which does NOT replicate the +0.0417 win of E1. Only nowait is beaten (+0.0708, raw p = 0.016, Holm p = 0.094 with 8 projects).
So the one positive claim left from E1 (LAW beats the waiting-time family) is specific to the Cabral test projects. On ApacheJIT the label policies are within 0.015 of each other and all sit about 0.04 below the oracle.
