# TURN: The owner says the work is not yet good enough for the journal

*Written 2026-11-24T19:00:23+00:00*

Feedback (owner, 2026-11-24): readers judged the current results not good enough for JKSU-CIS. My own state agrees: the only method that beats tuned waiting on dev (lawm 0.755) is matched by an ODaSC-style baseline (0.760), the novelty score is 14/25, and the closest JKSU-CIS paper on the same data (MSTDP) is a full method paper with many baselines and figures. Next: (1) benchmark systematically against JKSU-CIS papers (structure, datasets, metrics incl. effort-aware ones, numbers); (2) develop stronger denoisers on dev, starting from the oracle headroom (decomp_L1_W30 0.785 vs best real 0.760 on dev).
