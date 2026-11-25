# RESULT: E0 complete: LAW ranks best but decides worst

*Written 2026-11-25T00:25:33+00:00*

All 192 plain E0 runs are done (dev projects x seeds 0-2; results/raw_results.jsonl). Mean dev G-mean: oracle 0.794, ORB-W90 0.724, ORB-W60 0.712, Wait-W90 0.709, LAW lagakos+base 0.664, LAW lagakos+model 0.613, nowait 0.385. The ODaSC-style baseline (E0b, 45/60 runs, nova pending) is at 0.725-0.727 for W=15/30 on three projects. So on G-mean LAW loses clearly to every tuned baseline; H1 is not supported on dev.
But mean dev ROC-AUC tells the opposite story: LAW lagakos+model 0.827, naive+model 0.825, lagakos+base 0.822, against ODaSC-W15 0.804, Wait-W90 0.793, ORB-W90 0.793. Per project, LAW+model ranks better than Wait-W90 on fabric (0.768 vs 0.724), nova (0.858 vs 0.844) and sentry (0.794 vs 0.709), worse on neutron (0.888 vs 0.895). The re-weighting does carry information about which commits are risky. It is the threshold that fails, worst with the model prior (feedback loop, see DIAGNOSIS).
