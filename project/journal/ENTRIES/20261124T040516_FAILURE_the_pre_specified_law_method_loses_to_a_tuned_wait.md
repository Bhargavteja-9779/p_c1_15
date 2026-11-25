# FAILURE: The pre-specified LAW method loses to a tuned waiting time on the dev projects

*Written 2026-11-24T04:05:16+00:00*

On the dev projects (seeds 0-2, E0 so far: fabric, neutron complete) the method I pre-specified in plan_v1, law_lagakos_model, reaches mean G-mean 0.668 (fabric) and 0.496 (neutron). The tuned baselines reach 0.683 (orb W=30, fabric) and 0.837/0.838 (orb/wait W=180, neutron). The neutron gap is 0.34 G-mean, not a small miss. The AUC is not the problem: law 0.888 vs wait W=180 0.897 on neutron (results/raw_results.jsonl, E0). The failure is in recall-1: 0.255 vs 0.976.
