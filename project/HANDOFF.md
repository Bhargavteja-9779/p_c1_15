# HANDOFF — read this first
*Auto-generated 2026-11-25T21:00:02+00:00 by scripts/write_handoff.py*

## READ ALSO: USER_DIRECTIVES.md (owner standing orders)

## Where we are
- **Status:** RUNNING   **Cycle:** 3 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** cycle 3: E8 (ApacheJIT fresh confirmation, 405 jobs) running
- **Last action:** freeze_v6 done (H5 false on dev; primary=odasc_W30_t0.8); journal RESULT; E8 enqueued and runners launched
- **NEXT ACTION:** 1) Keep runners alive (bash scripts/launch_runner.sh 3; it also restores data/). 2) When E8 is done: python scripts/final_report.py (plan_v7 H6: Holm over 3 Wilcoxon, 9 projects), update gates G5/G7, novelty, journal RESULT. 3) Dev-only method round (owner directive): diagnose dual collapse on nova (operating point / noisy-OR saturation) and threshold calibration (archive/keen_edison_cycle1 shows latency-corrected calibration brings all methods near best-threshold G-mean on dev). 4) E3 (144 skipped_budget) only if budget allows after E8.

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 1122, 'skipped_budget': 144, 'skipped_plan': 117, 'pending': 401, 'running': 3}; running jobs: ['E8_aj_activemq_decomp_L1_W30_s101', 'E8_aj_activemq_decomp_L1_W30_s102', 'E8_aj_activemq_decomp_L1_W30_s103']
- Processes: `1084 tmux new-session -d -s research_w0 python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
1085 bash -c python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
1087 python3 run_all.py --mode full --resume --worker 0
1091 bash -c python3 run_all.py --mode full --resume --worker 1 >> logs/runner_w1.log 2>&1
1093 python3 run_all.py --mode full --resume --worker 1
1097 bash -c python3 run_all.py --mode full --resume --worker 2 >> logs/runner_w2.log 2>&1
1099 python3 run_all.py --mode full --resume --worker 2`
- Heartbeat age: -0s

## Compute
- Cycle 3: 1.54 h / 15 h   Global: 27.74 h / 120 h (CPU-hours; machine has no GPU)

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
- 2026-11-24T19:11:12+00:00: plan_v5 freeze: lawm=lawm_soft_W30 (0.7551), odasc=odasc_W30_t0.8 (0.7598); lawm beats odasc on dev: False
- 2026-11-25T13:07:06+00:00: plan_v6: dual-evidence denoiser (noisy-OR of mature-scorer posterior and kNN label composition) on dev; MSTDP-protocol experiment E7 pre-registered
- 2026-11-25T13:07:06+00:00: GitHub push currently fails (403, authentication must be reconnected by owner); commits accumulate locally and autocommit retries
- 2026-11-25T13:15:25+00:00: Parallel branches found (dreamy-fermat cycle 2, zealous-lamport, keen-edison, magical-bardeen) forked from b18fc8e; continue on zen-cray (most recent, owner directives); Cabral test projects declared 'used'; fresh confirmation on ApacheJIT (plan_v7)
- 2026-11-25T13:34:47+00:00: Session magical-bardeen resumed 2026-11-25: adopted zen-cray-ajbt81 state (most advanced: cycle 2, plan_v6 E0e running, plan_v7 pre-registered) into branch claude/magical-bardeen-9yglkz via merge -s ours; zen-cray's heartbeat was 12 min stale (session presumed stopped)
- 2026-11-25T13:34:47+00:00: Added scripts/freeze_v6.py and enqueue E8 (plan_v7 ApacheJIT confirmation, exactly the plan_v7 method list); ApacheJIT downloaded and sha256-verified; smoke test on the first 1200 kafka commits checked only that every method runs (no metrics inspected)
- 2026-11-25T14:53:00+00:00: Owner asked to continue from the most recent branch: adopted claude/magical-bardeen-9yglkz (cycle 2, heartbeat 28 min stale → session presumed stopped) into claude/keen-edison-jo222n via merge -s ours (keen-edison history kept). Keen-edison's parallel cycle-1 dev selection (E0b/E0c calibration/fsc/fixed-rate grids, dev only, never run on test) is kept under archive/keen_edison_cycle1/ for reference; its compute is not counted in this lineage's budget.json. Runners + autocommit relaunched on keen-edison.
- 2026-11-25T20:19:39+00:00: Cycle 3 started (cycle-2 budget 15 h exhausted). Re-queued 3 E0e nova jobs (skipped_budget); E3 (144 jobs, Cabral test robustness, test set already declared 'used' by plan_v7) stays skipped_budget until E8 is done
- 2026-11-25T20:59:35+00:00: plan_v6 freeze: dual=dual_W30_k50 (0.6812); lawm=lawm_soft_W30 (0.7551), odasc=odasc_W30_t0.8 (0.7598); primary (best dev) = odasc_W30_t0.8; H5 on dev: False
- 2026-11-25T21:00:02+00:00: E8 enqueued exactly as pre-registered in plan_v7 (9 ApacheJIT projects x 5 confirm seeds x 9 methods = 405 jobs) despite H5 being false on dev

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
1. Everything lives in git on branch `claude/keen-edison-jo222n` (older copies: claude/magical-bardeen-9yglkz, claude/zen-cray-ajbt81) of `bhargavteja-9779/p_c1_15` (pushed after every step).
2. On the new machine: `git clone` that repo, `git checkout claude/keen-edison-jo222n`, `pip install -r project/requirements.txt`.
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

