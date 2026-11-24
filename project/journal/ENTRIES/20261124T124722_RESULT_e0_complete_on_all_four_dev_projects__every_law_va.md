# RESULT: E0 complete on all four dev projects: every LAW variant is below tuned waiting time

*Written 2026-11-24T12:47:22+00:00*

Mean dev G-mean over fabric/neutron/nova/sentry x seeds 0-2 (results/raw_results.jsonl, experiment E0): oracle 0.794; best baseline orb_W90 0.724; wait_W90 0.709; best LAW variant law_lagakos_base 0.664 (law_naive_base 0.664, pre-specified law_lagakos_model 0.613, law_naive_model 0.580); nowait 0.385. LAW wins only on sentry (0.683 vs orb_W90 0.637) and fabric (0.673 vs 0.653) but loses clearly on neutron and nova, the two projects with the longest discovery delays. The pre-registered LAW hypothesis H1 is not supported on dev.
