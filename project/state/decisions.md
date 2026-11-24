# Decisions log

Every decision with reason and UTC timestamp. Append-only.

- **2026-11-24T03:04:37+00:00** — Place project in repo subfolder project/ on branch claude/dreamy-fermat-7983nm
  - Reason: Prompt specifies project/ layout; repo is the persistent store (container is ephemeral).

- **2026-11-24T03:04:37+00:00** — Hardware: CPU-only (4 cores, 15 GB RAM, no CUDA/MPS). All compute budgets are counted as CPU-hours.
  - Reason: nvidia-smi absent, torch.cuda.is_available()=False. This constrains topic choice to CPU-feasible experiments.

- **2026-11-24T03:11:07+00:00** — Selected journal: Journal of King Saud University – Computer and Information Sciences (Springer Nature, ISSN 1319-1578, IF 6.4 (2025))
  - Reason: Only verifiable reputable candidate with median Received→Accepted near 72 d (71 d last-12-month acceptances, 74 d 24-month window); 17 other verifiable candidates had medians 123–462 d; Elsevier fast journals could not be verified (no Crossref dates, ScienceDirect 403). G1 caveat: marginal on turnaround; 2025 JCR quartile UNVERIFIED (Q1 in 2024 JCR per KSU).

- **2026-11-24T03:11:07+00:00** — Interpretation: "submission→acceptance ≤ 72" evaluated as the MEDIAN (Accepted−Received) of a random sample
  - Reason: Section 4 asks to compute median and range; a per-paper guarantee is impossible.

- **2026-11-24T03:22:41+00:00** — Topic: verification-latency-aware online JIT-SDP (latency-aware weighting, LAW)
  - Reason: Public data with discovery times (Cabral et al. Zenodo 2591761), CPU-cheap, gap not found in 10-query prior-art search; see topic/selected_topic.md

- **2026-11-24T03:22:41+00:00** — Dev/test split by project: dev={fabric,neutron,nova,sentry}, test=other 10 (rng seed 0 draw before modelling)
  - Reason: Tuning only on dev projects; test projects touched only by frozen confirmation runs (Rule 5)

- **2026-11-24T03:22:41+00:00** — Primary metric G-mean over the evaluation window (commits from #500 to last-365-days), against final labels
  - Reason: Matches Cabral et al. 2019; last year excluded because final labels there are least complete

- **2026-11-24T03:22:41+00:00** — Runner parallelised to 3 workers (cores-1); budget counts summed worker seconds (CPU-time-like)
  - Reason: 4-core machine; budget remains conservative because seconds are summed across workers

- **2026-11-24T03:35:03+00:00** — User allowed Frontiers journals; checked Frontiers in AI (median 78 d), Big Data (74 d), Computer Science (100 d)
  - Reason: None faster than JKSU-CIS (71–74 d) and quartiles UNVERIFIED -> keep JKSU-CIS (journal_selection/journal_comparison.md addendum)

- **2026-11-24T21:02:13+00:00** — Work continues on branch claude/keen-edison-jo222n (this session's assigned branch; same history as claude/dreamy-fermat-7983nm at b18fc8e)
  - Reason: New account/session is restricted to pushing that branch

- **2026-11-24T21:02:13+00:00** — Runner fix: on start a worker resets its OWN jobs left 'running' (worker id == self) to pending
  - Reason: Bug found on resume: flock self-check made a worker's own orphaned jobs look alive; 2 jobs were stuck 'running' and were reset manually

- **2026-11-24T21:02:13+00:00** — Liu et al. 2024a (PU learning for JIT-SDP) marked UNVERIFIED; generic PU framing of clean commits conceded as prior art; LAW claim narrowed to age/delay-distribution weighting in the online setting
  - Reason: Primary source not found: Crossref scan of all 2024 EMSE works finds no such paper; EMSE 29(4):98 is a different article

- **2026-11-24T21:27:40+00:00** — plan_v2 adopted: adds latency-corrected threshold calibration (thr_cal), ODaSC-inspired fsc baseline, E0b dev grid (324 runs); PROPOSED fixed in advance = law_lagakos_model + thr_cal_lat; plan_v1 E1-E3 dropped
  - Reason: Dev diagnosis: G-mean gaps are mostly operating point; pre-specified LAW fails on neutron dev; closest prior work must be a baseline

- **2026-11-24T21:27:40+00:00** — E0 jobs interrupted at 152/192 to load new code (3 running jobs reset and re-run, no results lost)
  - Reason: Workers had the old module imported
