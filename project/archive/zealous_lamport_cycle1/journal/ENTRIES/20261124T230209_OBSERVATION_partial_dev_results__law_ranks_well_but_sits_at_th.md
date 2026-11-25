# OBSERVATION: Partial dev results: LAW ranks well but sits at the wrong operating point

*Written 2026-11-24T23:02:09+00:00*

With about half of E0 done (tables/E0_summary.csv at 2026-11-24 ~23:00), the best LAW variant (lagakos+base) has dev G-mean 0.678 vs ORB-W90 0.735 and Wait-W90 0.711. Its ROC-AUC (0.814) is equal to ORB-W90 (0.817) and Wait-W90 (0.809). LAW's recall-1 is low (0.53) and recall-0 high (0.86). So LAW is not worse at ranking commits; it predicts 'defective' too rarely at threshold 0.5. All latency-handling methods stay far below the oracle AUC (0.899). Re-weighting by a prior does not add information about WHICH young commit is buggy; this is my working explanation, to be tested when E0 is complete.
