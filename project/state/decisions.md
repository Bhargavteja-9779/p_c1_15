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

- **2026-11-24T23:02:09+00:00** — Liu et al. 2024a (PU learning for JIT-SDP, EMSE 29(5):98) marked UNVERIFIED / not found
  - Reason: 8 searches in Crossref/OpenAlex incl. EMSE 2024 listing found no such paper; EMSE 29(4):98 is an unrelated paper. Not used as prior art or reference unless a resolvable DOI appears.

- **2026-11-24T23:02:09+00:00** — plan_v2: add ODaSC-style baseline (batch adaptation: kNN label confidence at labelling time, delta=0.9, k=50, pool=5000 recent labelled commits) tuned over W in {15,30,60,90,180} on dev = 5 configs, same budget as wait/orb
  - Reason: ODaSC is the closest prior work (same noise, same data); Rule 6 requires strongest baselines with equal tuning budget. Exact DenStream/Hoeffding OOB reimplementation is outside our shared-learner protocol; adaptation keeps its label-confidence rule on the shared LightGBM learner and is described as an adaptation.

- **2026-11-24T23:02:09+00:00** — plan_v2: LAW configuration for E1 chosen on dev from its 4 E0 variants (best mean dev G-mean), instead of the plan_v1 pre-specified lagakos+model
  - Reason: Equal treatment: baselines pick W from 5 configs on dev; plan_v1 tuning_budget already allowed <=5 configs per method. Decided before any test-project run; partial E0 shows lagakos+model unstable (std .095).

- **2026-11-24T23:02:09+00:00** — Runner fix: a restarted worker now resets its own stale 'running' jobs
  - Reason: After the account handoff, E0_sentry_law_lagakos_base_s2 stayed 'running' forever because worker 0 holds its own lock and looked alive.

- **2026-11-24T23:04:02+00:00** — Test projects are not touched until the selected LAW variant beats the best baseline (incl. ODaSC) on dev
  - Reason: Running E1 with a method already losing on dev would spend the held-out set; any later LAW revision would then be evaluated on test data already seen (Rule 5). Ladder 6.4 runs on dev first.
