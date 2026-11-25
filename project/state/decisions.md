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

- **2026-11-24T04:05:16+00:00** — plan_v2: add E0b dev diagnostics (awt eps grid, decomposition with true labels); LAW kept as pre-specified but recorded as failing on dev
  - Reason: Dev results + diagnosis (results/diag_law_neutron.json, results/diag_survival_dev.txt); no test project touched

- **2026-11-24T04:05:16+00:00** — Liu et al. 2024a ('PU learning for JIT-SDP', EMSE 29(5):98) marked UNVERIFIED
  - Reason: Cited only in MSTDP (JKSU-CIS 2026). Crossref and OpenAlex searches by title and venue/volume/issue return no such record; the paper cannot be opened. Not used as evidence either way

- **2026-11-24T04:05:16+00:00** — ODaSC baseline reimplementation deferred
  - Reason: Only needed if a method claim survives dev; ODaSC Table II is used now as literature evidence (opt≈estimated)

- **2026-11-24T04:06:17+00:00** — Reset orphaned queue record E0_sentry_law_lagakos_base_s2 to pending
  - Reason: Left 'running' by the reclaimed container; its worker id (0) is alive again in the new container so the automatic reset did not fire

- **2026-11-24T12:46:15+00:00** — Reset 96 E0b jobs to pending and relaunched workers
  - Reason: Workers had imported src/jit.py before awt/decomp were added (ValueError: awt). Infrastructure failure, not a method result; no compute spent

- **2026-11-24T13:19:54+00:00** — plan_v2 rule outcome: no candidate (law_*, awt_*) beats best dev baseline -> E1 runs on test as pre-registered NEGATIVE-RESULT confirmation
  - Reason: plan_v2.yaml proposed_method_rule

- **2026-11-24T13:19:55+00:00** — Frozen config: wait W*=90, orb W*=90, best dev baseline=orb_W90
  - Reason: Highest mean dev G-mean (E0, dev projects only); proposed method config pre-specified, not tuned

- **2026-11-24T13:20:12+00:00** — plan_v3 written and E1, E3b, E3, E2 enqueued on test projects (first test touch)
  - Reason: Config frozen on dev (state/frozen_config.json); decomposition pre-registered as H3 before test runs

- **2026-11-24T15:00:34+00:00** — Cycle 1 outcome: H1 (LAW) and candidate awt not supported on test; H3 supported. Gates G5/G6 fail for a method claim -> Section 6.4 ladder, cycle 2 targets a feature-based dormant-bug denoiser without self-confirmation (plan_v4, dev first)
  - Reason: results/statistics.json; journal RESULT entries

- **2026-11-24T15:04:02+00:00** — Cycle 2 started (plan_v4: lawm = mature cross-fitted dormant-bug posterior on the wait set); remaining cycle-1 E3/E2 jobs are charged to cycle 2 budget
  - Reason: Section 6.4 ladder rung 3; budget accounting kept simple and conservative

- **2026-11-24T15:52:36+00:00** — H4 holds on dev -> plan_v5: freeze lawm_soft_W30; add ODaSC-style baseline (equal 4-config dev budget), lawm ablations, robustness; skip remaining cycle-1 E2 (LAW ablation)
  - Reason: LAW failed on dev and test; ablating it supports no claim; saves ~2 CPU-h for the cycle-2 confirmation

- **2026-11-24T19:00:23+00:00** — Owner directive recorded in USER_DIRECTIVES.md, BOOTSTRAP_PROMPT.txt and MASTER_PROMPT addendum: iterate until top-notch, benchmark vs JKSU-CIS papers, no honest exit
  - Reason: Owner message 2026-11-24 (paper judged not good enough for the journal)

- **2026-11-24T19:00:23+00:00** — Hold the E4 test confirmation (lawm/odasc) until the next method-development round on dev is finished
  - Reason: Running test now and again after new methods would use the test projects twice; one frozen confirmation of the final candidate set keeps the test clean

- **2026-11-24T19:11:12+00:00** — plan_v5 freeze: lawm=lawm_soft_W30 (0.7551), odasc=odasc_W30_t0.8 (0.7598); lawm beats odasc on dev: False
  - Reason: best mean dev G-mean, dev projects only

- **2026-11-25T13:07:06+00:00** — plan_v6: dual-evidence denoiser (noisy-OR of mature-scorer posterior and kNN label composition) on dev; MSTDP-protocol experiment E7 pre-registered
  - Reason: Complementarity of lawm/odasc on dev; owner directive to compare with JKSU-CIS papers (MSTDP uses the same data)

- **2026-11-25T13:07:06+00:00** — GitHub push currently fails (403, authentication must be reconnected by owner); commits accumulate locally and autocommit retries
  - Reason: git push error 2026-11-25

- **2026-11-25T13:15:25+00:00** — Parallel branches found (dreamy-fermat cycle 2, zealous-lamport, keen-edison, magical-bardeen) forked from b18fc8e; continue on zen-cray (most recent, owner directives); Cabral test projects declared 'used'; fresh confirmation on ApacheJIT (plan_v7)
  - Reason: git branch -a 2026-11-25; dreamy-fermat RESULTS_SUMMARY shows the same test projects used with many variants

- **2026-11-25T13:34:47+00:00** — Session magical-bardeen resumed 2026-11-25: adopted zen-cray-ajbt81 state (most advanced: cycle 2, plan_v6 E0e running, plan_v7 pre-registered) into branch claude/magical-bardeen-9yglkz via merge -s ours; zen-cray's heartbeat was 12 min stale (session presumed stopped)
  - Reason: Owner asked to check the most recent branch and continue; development branch for this session is magical-bardeen. magical-bardeen's own cycle-1 work (plan_v2: LAT threshold policy, river-based ODaSC reimplementation) stays in git history (commit b90ea74); zen-cray found threshold effects small for denoisers (diag_threshold_dev.json), so LAT is not carried forward as a candidate.

- **2026-11-25T13:34:47+00:00** — Added scripts/freeze_v6.py and enqueue E8 (plan_v7 ApacheJIT confirmation, exactly the plan_v7 method list); ApacheJIT downloaded and sha256-verified; smoke test on the first 1200 kafka commits checked only that every method runs (no metrics inspected)
  - Reason: plan_v7 required these and they did not exist yet

- **2026-11-25T14:53:00+00:00** — Owner asked to continue from the most recent branch: adopted claude/magical-bardeen-9yglkz (cycle 2, heartbeat 28 min stale → session presumed stopped) into claude/keen-edison-jo222n via merge -s ours (keen-edison history kept). Keen-edison's parallel cycle-1 dev selection (E0b/E0c calibration/fsc/fixed-rate grids, dev only, never run on test) is kept under archive/keen_edison_cycle1/ for reference; its compute is not counted in this lineage's budget.json. Runners + autocommit relaunched on keen-edison.
  - Reason: owner instruction ("check recent branch and continue from there")

- **2026-11-25T20:19:39+00:00** — Cycle 3 started (cycle-2 budget 15 h exhausted). Re-queued 3 E0e nova jobs (skipped_budget); E3 (144 jobs, Cabral test robustness, test set already declared 'used' by plan_v7) stays skipped_budget until E8 is done
  - Reason: E0e completion is required by freeze_v6; E8 fresh confirmation has priority over E3

- **2026-11-25T20:59:35+00:00** — plan_v6 freeze: dual=dual_W30_k50 (0.6812); lawm=lawm_soft_W30 (0.7551), odasc=odasc_W30_t0.8 (0.7598); primary (best dev) = odasc_W30_t0.8; H5 on dev: False
  - Reason: best mean dev G-mean, dev projects only (plan_v6/plan_v7)

- **2026-11-25T21:00:02+00:00** — E8 enqueued exactly as pre-registered in plan_v7 (9 ApacheJIT projects x 5 confirm seeds x 9 methods = 405 jobs) despite H5 being false on dev
  - Reason: plan_v7 pre-registration; no changes after seeing dev results

- **2026-11-25T21:04:27+00:00** — final_report E8/H6: the primary candidate (best dev mean) is odasc_W30_t0.8 itself, so the pre-registered 'primary vs odasc' test is a degenerate self-comparison; dropped, Holm over the 2 waiting baselines. Our own methods (dual_W30_k50, lawm_soft_W30) vs wait_W90/orb_W90/odasc are reported descriptively as pre-registered
  - Reason: fixed before any E8 result was inspected; Wilcoxon on all-zero differences is undefined
