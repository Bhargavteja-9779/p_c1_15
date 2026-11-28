# RESULT: Fresh-clone reproducibility check passes

*Written 2026-11-28T18:58:03+00:00*

I cloned the pushed branch into an empty directory, downloaded both datasets from Zenodo with the README scripts (sha256 match), ran the tests (3 passed), the quick smoke test, and scripts/reproduce_check.py, which re-runs one stored job per experiment x variant (97 jobs across E0-E10 and D1). All 97 reproduce the stored G-mean, AUC and recalls exactly (results/reproduce_check_fresh_clone.json, logs/fresh_clone_test.log). E3 was not yet in the results at clone time.
