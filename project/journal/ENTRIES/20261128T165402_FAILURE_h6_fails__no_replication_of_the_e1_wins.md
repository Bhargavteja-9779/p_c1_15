# FAILURE: H6 fails: no replication of the E1 wins

*Written 2026-11-28T16:54:02+00:00*

I pre-registered H6 as a no-re-tuning replication. It fails: LAW is indistinguishable from all six baselines on ApacheJIT. My best explanation is that ApacheJIT is a curated sample with a much higher defect share (e.g. cassandra 3117 of 8159 commits buggy, 38%), which makes waiting-time negatives scarcer and the decision less sensitive to label policy; but I have not tested this explanation and will state it as a conjecture. The method claim (Type B novelty) is now dead on two benchmarks.
