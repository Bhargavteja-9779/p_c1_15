# HYPOTHESIS: A threshold set from matured past predictions removes most of the W sensitivity

*Written 2026-11-24T21:13:42+00:00*

Written before testing. H2: if at each update the decision threshold is set to maximise G-mean on the method's OWN past prequential predictions, scored against labels as observed at T with undiscovered commits counted by their latency-corrected posterior (found=positive; not found: positive weight q=pS(a)/(1-p+pS(a)), p=base rate of mature commits), then (a) the G-mean spread across W shrinks to roughly the best-threshold spread (<=0.08 on neutron instead of 0.59), and (b) nowait + calibration and LAW + calibration come within 0.02 of the best tuned wait-W baseline on all 4 dev projects. What would prove me wrong: calibrated variants stay >0.03 below best wait-W on >=2 dev projects, or the calibration over-predicts on fabric like W180 does.
