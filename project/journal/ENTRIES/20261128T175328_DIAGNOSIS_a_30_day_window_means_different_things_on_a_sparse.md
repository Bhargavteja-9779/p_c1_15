# DIAGNOSIS: A 30-day window means different things on a sparse benchmark (post-hoc, exploratory)

*Written 2026-11-28T17:53:28+00:00*

Written after seeing E7, so this is exploratory, not confirmatory. Across the 18 projects, the share of the gap recovered by young-30 labels correlates with commit density (Spearman rho 0.69, p = 0.002) and with how fast defects are found (share found within 30 days: rho 0.70, p = 0.001; median delay: rho -0.62), but not with defect rate (rho -0.22, p = 0.38) (tables/E7_diag_benchmark_profile.csv). ApacheJIT is a curated sample: 24-169 commits per 30 days versus 72-248 in the Cabral projects, and only 10-33% of defects found within 30 days versus 18-57%. So the last 30 days contain few commits and few discoverable defects. My reading: what matters is not calendar age but how many informative labels a window holds. I cannot confirm this without fresh data; the claim in the paper must be the conditional one, with this as a stated conjecture.
