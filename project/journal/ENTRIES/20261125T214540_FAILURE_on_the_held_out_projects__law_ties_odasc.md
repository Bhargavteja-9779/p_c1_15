# FAILURE: On the held-out projects, LAW ties ODaSC

*Written 2026-11-25T21:45:40+00:00*

E1 (10 test projects x 5 confirmation seeds, frozen plan_v3; results/statistics.json). Mean G-mean: oracle 0.715, LAW+threshold 0.696, ODaSC-W15+threshold 0.695, ODaSC-W30 0.695, wait-W30+threshold 0.676, ORB-W90 0.658, wait-W90 0.654, nowait 0.429. Against the primary comparator ODaSC-W30 the difference is +0.0009 (95% CI -0.0086 to 0.0114, Wilcoxon p=0.77, Holm p=1.0, 6 wins/4 losses). G5 fails. The dev margin (+0.013) was selection noise, as I expected when I froze.
What does hold, with Holm-corrected p=0.0195 and 9/10 project wins: LAW+threshold beats the waiting-time rule (+0.042 vs wait-W90) and ORB (+0.038), the methods from Cabral et al. 2019. Its dev AUC advantage did not replicate (test AUC 0.751 vs ODaSC 0.762). Best explanation: the age-based weight and the feature-neighbourhood confidence of ODaSC both recover most of what waiting loses (they close about 70% of the gap between wait-W90 and the oracle), and neither is better than the other on these data.
