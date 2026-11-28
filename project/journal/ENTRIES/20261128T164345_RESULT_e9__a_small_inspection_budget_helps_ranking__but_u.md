# RESULT: E9: a small inspection budget helps ranking, but uncertainty sampling does not win

*Written 2026-11-28T16:43:45+00:00*

E9 dev grid is complete (162 runs: fabric, neutron, sentry; seeds 0-2; results/raw_results.jsonl experiment E9).
Mean dev AUC without inspection (E0, same projects and seeds): nowait+threshold 0.7836, ODaSC-W30 0.8034, LAW 0.8164, oracle 0.8705.
At a 5% inspection budget: nowait 0.8015 (rand) / 0.8070 (top) / 0.8048 (unc); ODaSC 0.8133 / 0.8179 / 0.8131; LAW 0.8261 / 0.8275 / 0.8250.
H7 is refuted: inspecting the top-risk commits (HumLa-like) is at least as good as inspecting the uncertain ones for every base method; 'unc' is never best at 5%.
H8 is refuted too: the best 5% gain is +0.0234 (nowait), +0.0145 (ODaSC), +0.0111 (LAW), all smaller than the 0.0328 AUC spread between the label policies without inspection.
So the label policy matters more than a 5% inspection budget, and the inspection-policy question is already answered by HumLa's top-risk choice. I counted 18 variants.
