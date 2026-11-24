# OBSERVATION: Someone already moved the threshold, but to a fixed target

*Written 2026-11-24T21:31:18+00:00*

The prior-art query 'waiting time verification latency just-in-time software defect prediction' surfaced Pessoa's 2021 UFPE MSc dissertation (literature/pdfs/Pessoa_MSc2021.pdf). Section 3.1.5 keeps the share of commits predicted defective at a fixed rate fr1 chosen by tuning, using a rate-driven threshold over a sliding window, and argues this should be a standard baseline for class-imbalance evolution. They mention that choosing a G-mean-optimal threshold at every time step is the alternative, but do not do it. This is the closest thing to my calibration. My difference: no tuned target rate, and the threshold is chosen against latency-corrected labels. If a tuned fixed rate does as well, my calibration claim is weak; so it goes in as a baseline (plan_v3, E0c) with a larger tuning grid (25 configs) than my method gets.
