# PROBLEM: Provisionally clean commits in online JIT defect prediction

*Written 2026-11-24T03:22:41+00:00*

An online JIT-SDP model is retrained on past commits, but a commit's "clean" label is only provisional: the defect it introduced is discovered when a later fix points back at it. Reconstructing discovery times from the Cabral et al. artifact (src/data.py), I found that median commit→discovery delays per project range from 16 days (brackets) to 416 days (spring-integration), and 90th percentiles from 383 to 1964 days. The standard practice (Cabral et al. 2019) is to wait W days (90) before trusting a clean label. That either injects noise (defects found after W are trained as clean) or discards the newest data (everything younger than W lacks negatives). Teams using JIT-SDP for review triage get a model that is either stale or biased.
