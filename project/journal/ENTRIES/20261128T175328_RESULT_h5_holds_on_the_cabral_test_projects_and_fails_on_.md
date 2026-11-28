# RESULT: H5 holds on the Cabral test projects and fails on ApacheJIT

*Written 2026-11-28T17:53:28+00:00*

E7+E7b complete: 18 projects x 5 confirmation seeds x 6 variants (results/statistics.json E7_H5_decomposition; tables/E7_H5_recovery_*.csv).
Cabral-test (10 projects): median nowait-to-oracle AUC gap 0.0906. Revealing labels younger than 30 days recovers a median 0.7559 of it (>= 0.5 on 9/10 projects); revealing labels older than 180 days recovers 0.0554 (<= 0.2 on 8/10). Young-30 beats old-180 on AUC by +0.058, 95% CI [0.0425, 0.0724], 10/10 projects, Wilcoxon p = 0.002. H5 supported.
ApacheJIT (8 projects): median gap 0.0829, but young-30 recovers only 0.3431 (>= 0.5 on 1/8) while old-30 recovers 0.6024. Young-30 vs old-180: +0.0045, CI [-0.0236, 0.0294], p = 0.74. H5 fails. On activemq and groovy, revealing the newest 30 days recovers nothing (-0.046, -0.114).
The pattern I saw on dev is real on one benchmark and absent on the other.
