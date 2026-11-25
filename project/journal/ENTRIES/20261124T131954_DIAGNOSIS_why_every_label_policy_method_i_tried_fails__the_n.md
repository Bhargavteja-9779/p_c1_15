# DIAGNOSIS: Why every label-policy method I tried fails: the noisy examples are old, and age carries no information about them

*Written 2026-11-24T13:19:54+00:00*

Combining the decomposition with the LAW diagnosis: the harmful false-clean commits are mostly OLD (the age-based posterior gives truly buggy provisional negatives mean q 0.086, results/diag_law_neutron.json). Any rule that uses only commit age (wait, awt, LAW-base) can at best drop or down-weight young data; it cannot find the old dormant bugs. Finding them needs information about the commit itself (features / model), but using the current model's score creates a feedback loop (LAW-model). A method that could work must identify dormant bugs among OLD provisional negatives from features while being protected from self-confirmation. That is cycle-2 material.
