# HYPOTHESIS: H7/H8: spend a small inspection budget on the newest commits

*Written 2026-11-25T10:28:10+00:00*

If the newest labels carry the ranking cost (D1), then a small budget of developer inspections of new commits, revealing their true label at commit time, should help more than any re-weighting of provisional labels. Prior work (HumLa, Song & Minku FSE 2023) assumes developers inspect the commits flagged as most risky. Written before E9 (dev only: fabric, neutron, sentry; seeds 0-2; budgets 2% and 5%):
H7: at a 5% budget, inspecting the commits closest to the decision threshold ('unc') gives higher mean dev AUC than inspecting the top-risk commits ('top', HumLa-like) and than random inspection, for each of nowait, LAW and ODaSC.
H8: the AUC gain from a 5% budget (best policy vs no inspection) is larger than the AUC difference between the best and worst of the three label policies without inspection.
