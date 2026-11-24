# PROBLEM: LAW loses badly to a long waiting time on neutron (dev)

*Written 2026-11-24T21:02:13+00:00*

Partial E0 (dev projects, explore seeds; results/raw_results.jsonl): on neutron, wait W=180 reaches G-mean 0.838 and orb W=180 0.837, while LAW lagakos+base gets 0.683 and the pre-specified LAW lagakos+model only 0.496. On fabric LAW (0.673) is roughly level with the best baselines (orb W30 0.683). nowait collapses on neutron (0.245). So on neutron, the freshest data hurts and waiting a long time helps a lot; LAW behaves more like 'short wait'. The model-prior variant is worse than the base-rate prior on both projects. I do not yet know why; next I will diagnose on dev only (recall-1 vs recall-0, q values for true bugs vs cleans).
