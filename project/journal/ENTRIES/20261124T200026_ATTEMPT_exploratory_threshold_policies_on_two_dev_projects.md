# ATTEMPT: Exploratory threshold policies on two dev projects (seed 0)

*Written 2026-11-24T20:00:26+00:00*

Config ids in results/exploratory/thr_dev.jsonl (10 runs, logged as exploratory variants). nowait with a latency-weighted threshold: neutron G-mean 0.793 (fixed-threshold nowait 0.245 in E0), fabric 0.706 (best fixed-W policy on fabric in E0: orb W=30, 0.683). Mature-label threshold: neutron 0.774, fabric 0.698. With wait W=90 underneath: latency 0.836 / 0.682, mature 0.821 / 0.642. The latency weighting beat the mature-label threshold in 4 of 4 pairs, but by small margins (0.008-0.040) on one seed, so this is a lead, not a result. I also reimplemented ODaSC (src/odasc.py); a first neutron run gives 0.824, close to the best fixed W (0.838), so it is a strong baseline. Next: plan_v2 with an equal 5-config budget for LAT, MAT, ODaSC and OOB on dev.
