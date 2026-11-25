# HANDOFF — read this first
*Auto-generated 2026-11-25T13:15:31+00:00 by scripts/write_handoff.py*

## READ ALSO: USER_DIRECTIVES.md (owner standing orders)

## Where we are
- **Status:** RUNNING   **Cycle:** 2 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** cycle 2: owner directive -> benchmark vs JKSU-CIS + stronger methods on dev; E4 test held
- **Last action:** Cycle 1 closed: H1 negative on test, H3 confirmed (10/10); gates updated; novelty 14/25; plan_v4 lawm implemented + leakage test
- **NEXT ACTION:** 1) Finish E0d (3 nova jobs) then python scripts/freeze_v5.py (dev only). 2) Build literature/jksu_benchmark.md from literature/fulltext/*.html (structure, datasets, metrics, numbers). 3) New methods on dev (plan_v6): combine feature-based denoisers, add effort-aware metrics (Recall@20%Effort, Popt, IFA), stronger learners. 4) Only then one frozen test confirmation of the final candidates.

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 1082, 'pending': 180, 'skipped_plan': 117, 'running': 3}; running jobs: ['E0e_fabric_dual_W90_k50_s0', 'E0e_fabric_dual_W90_k50_s1', 'E0e_fabric_dual_W90_k50_s2']
- Processes: `233 tmux new-session -d -s research_w0 python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
234 bash -c python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
236 python3 run_all.py --mode full --resume --worker 0
240 bash -c python3 run_all.py --mode full --resume --worker 1 >> logs/runner_w1.log 2>&1
243 python3 run_all.py --mode full --resume --worker 1
246 bash -c python3 run_all.py --mode full --resume --worker 2 >> logs/runner_w2.log 2>&1
248 python3 run_all.py --mode full --resume --worker 2`
- Heartbeat age: 17s

## Compute
- Cycle 2: 9.60 h / 15 h   Global: 19.82 h / 120 h (CPU-hours; machine has no GPU)

## Gate status (Section 7)
| Gate | Status | Evidence |
|---|---|---|
| G1 | pass (marginal; caveat stated) | journal_selection/selected_journal.md — median 71 d (12 m) / 74 d (24 m); 2025 quartile UNVERIFIED |
| G2 | fail (in progress) | state/novelty_ledger.json: 12 papers logged as opened (abstract or full text) + 13 JKSU papers in literature/journal_papers_matrix.csv; claim table present; need >=30 opened and full-text check of dormant-defects (TOSEM 2021) |
| G3 | fail | self-score 14/25 cycle 1 (state/novelty_ledger.json scores); no blind review yet |
| G4 | partial | wait/ORB reproduced under same protocol with equal tuning budget (tables/E0_dev_tuning.csv); ODaSC not reimplemented; published ORB numbers use a different learner (Hoeffding trees) -> not directly comparable |
| G5 | fail | results/statistics.json E1_H1_family: LAW and awt below wait_W90/orb_W90 (Holm p>=0.15) |
| G6 | fail | no surviving method to ablate |
| G7 | partial | H3 holds on 10/10 held-out projects (one dataset family); second dataset not tested |
| G8 | pass | tests/test_no_future.py (future discoveries do not change past predictions for nowait/wait/orb/law/awt); dev/test project split fixed before modelling; decomp is a diagnostic using true labels, never a competitor |
| G9 | unknown |  |
| G10 | unknown |  |
| G11 | unknown |  |

## Last 10 decisions
- 2026-11-24T13:20:12+00:00: plan_v3 written and E1, E3b, E3, E2 enqueued on test projects (first test touch)
- 2026-11-24T15:00:34+00:00: Cycle 1 outcome: H1 (LAW) and candidate awt not supported on test; H3 supported. Gates G5/G6 fail for a method claim -> Section 6.4 ladder, cycle 2 targets a feature-based dormant-bug denoiser without self-confirmation (plan_v4, dev first)
- 2026-11-24T15:04:02+00:00: Cycle 2 started (plan_v4: lawm = mature cross-fitted dormant-bug posterior on the wait set); remaining cycle-1 E3/E2 jobs are charged to cycle 2 budget
- 2026-11-24T15:52:36+00:00: H4 holds on dev -> plan_v5: freeze lawm_soft_W30; add ODaSC-style baseline (equal 4-config dev budget), lawm ablations, robustness; skip remaining cycle-1 E2 (LAW ablation)
- 2026-11-24T19:00:23+00:00: Owner directive recorded in USER_DIRECTIVES.md, BOOTSTRAP_PROMPT.txt and MASTER_PROMPT addendum: iterate until top-notch, benchmark vs JKSU-CIS papers, no honest exit
- 2026-11-24T19:00:23+00:00: Hold the E4 test confirmation (lawm/odasc) until the next method-development round on dev is finished
- 2026-11-24T19:11:12+00:00: plan_v5 freeze: lawm=lawm_soft_W30 (0.7551), odasc=odasc_W30_t0.8 (0.7598); lawm beats odasc on dev: False
- 2026-11-25T13:07:06+00:00: plan_v6: dual-evidence denoiser (noisy-OR of mature-scorer posterior and kNN label composition) on dev; MSTDP-protocol experiment E7 pre-registered
- 2026-11-25T13:07:06+00:00: GitHub push currently fails (403, authentication must be reconnected by owner); commits accumulate locally and autocommit retries
- 2026-11-25T13:15:25+00:00: Parallel branches found (dreamy-fermat cycle 2, zealous-lamport, keen-edison, magical-bardeen) forked from b18fc8e; continue on zen-cray (most recent, owner directives); Cabral test projects declared 'used'; fresh confirmation on ApacheJIT (plan_v7)

## Last failures (journal entries)
- journal/ENTRIES/20261124T040516_FAILURE_the_pre_specified_law_method_loses_to_a_tuned_wait.md
- journal/ENTRIES/20261124T124615_FAILURE_infrastructure__new_experiment_ran_on_stale_code.md
- journal/ENTRIES/20261124T131954_DEAD END_adaptive_waiting_time__awt__gives_no_gain_on_dev.md

## Commands (run from `project/`)
| What | Command |
|---|---|
| Status | `python scripts/status.py` |
| Runner log | `tail -f logs/runner.log` |
| Supervisor log | `tail -f logs/supervisor.log` |
| Launch/resume compute (Layer A) | `bash scripts/launch_runner.sh` (idempotent; tmux session `research_runner`) |
| Smoke test | `python run_all.py --mode quick` |
| Start agent supervisor (Layer B) | `setsid nohup bash scripts/supervisor.sh >> logs/supervisor.log 2>&1 &` |
| Stop everything | `bash scripts/stop_all.sh` |
| Install autostart (cron @reboot + 5-min watchdog) | `bash scripts/install_autostart.sh` |
| Remove autostart (both layers) | `bash scripts/install_autostart.sh --remove` |
| Regenerate this file | `python scripts/write_handoff.py` |
| Snapshot backup | `bash scripts/snapshot.sh` |

## Moving to a new account / machine
1. Everything lives in git on branch `claude/zen-cray-ajbt81` (older copy: claude/dreamy-fermat-7983nm) of `bhargavteja-9779/p_c1_15` (pushed after every step).
2. On the new machine: `git clone` that repo, `git checkout claude/zen-cray-ajbt81`, `pip install -r project/requirements.txt`.
3. Paste the contents of `project/BOOTSTRAP_PROMPT.txt` into the new agent session.

## Known problems / environment facts
- **The original session ran in an ephemeral cloud container** (4 CPU cores, 15 GB RAM, **no GPU**, no `crontab`). Detached runs there die when the container is reclaimed; the git branch is the durable store. Background jobs are therefore kept short and results are committed as soon as they land.
- **Layer B (supervisor) was NOT started in the cloud container**: the agent was already running interactively there, and a second headless agent would edit the same files concurrently. `scripts/supervisor.sh` is provided and tested for syntax; it auto-detects the `claude` CLI and uses `claude -p ... --dangerously-skip-permissions`. Run it yourself on a persistent machine. Auto-restart is NOT active unless you start it.
- No autostart was installed in the cloud container (no crontab, no systemd user session). On a persistent Linux machine run `bash scripts/install_autostart.sh`.
- Compute budgets in Section 0 are interpreted as CPU-hours on this machine.

## Where things are
- State: `state/` (agent_state.json, queue.json, budget.json, decisions.md, variants_tried.csv, novelty_ledger.json, gates.json)
- Research diary: `journal/ENTRIES/` (append-only)
- Journal choice: `journal_selection/` ; literature: `literature/` ; topic: `topic/` ; plans: `experiments/plan_v*.yaml`
- Code: `src/` (runner, jobs, models), `scripts/` (status, report, audit, supervisor), `tests/`
- Results: `results/raw_results.jsonl` (canonical), `results/*.json`, `tables/`, `figures/`
- Paper: `paper/` ; reviews: `review/`

