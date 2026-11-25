# HANDOFF — read this first
*Auto-generated 2026-11-25T21:47:57+00:00 by scripts/write_handoff.py*

## READ ALSO: USER_DIRECTIVES.md (owner standing orders)

## Where we are
- **Status:** RUNNING   **Cycle:** 3 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** cycle 3: E8 analysed (H6 fail, H3 replicated); plan_v8 dev round on dual denoiser
- **Last action:** E8 done and analysed; gates G5/G7 updated; journal RESULT
- **NEXT ACTION:** 1) Dev-only: diagnose dual on nova (results/diag_dev/dual_nova_seed0.txt), design plan_v8 (latency-corrected neighbour posterior r_S = rS/(1-r+rS); combination rule) BEFORE running; grid on Cabral dev only. 2) Find an untouched confirmation dataset (e.g. other JIT datasets with fix dates; ApacheJIT and Cabral test are USED). 3) Update novelty score + blind review. 4) E3 (144 skipped_budget) low priority.

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 1526, 'skipped_budget': 144, 'skipped_plan': 117}; running jobs: none
- Processes: `none`
- Heartbeat age: 718s

## Compute
- Cycle 3: 3.31 h / 15 h   Global: 29.50 h / 120 h (CPU-hours; machine has no GPU)

## Gate status (Section 7)
| Gate | Status | Evidence |
|---|---|---|
| G1 | pass (marginal; caveat stated) | journal_selection/selected_journal.md — median 71 d (12 m) / 74 d (24 m); 2025 quartile UNVERIFIED |
| G2 | fail (in progress) | state/novelty_ledger.json: 12 papers logged as opened (abstract or full text) + 13 JKSU papers in literature/journal_papers_matrix.csv; claim table present; need >=30 opened and full-text check of dormant-defects (TOSEM 2021) |
| G3 | fail | self-score 14/25 cycle 1 (state/novelty_ledger.json scores); no blind review yet |
| G4 | partial | wait/ORB reproduced under same protocol with equal tuning budget (tables/E0_dev_tuning.csv); ODaSC not reimplemented; published ORB numbers use a different learner (Hoeffding trees) -> not directly comparable |
| G5 | fail | results/statistics.json E8_planv7_H6_primary_vs_baselines (ApacheJIT, 9 fresh projects): primary odasc_W30_t0.8 vs wait_W90 +0.0012 (Holm p=0.60), vs orb_W90 +0.0114 (Holm p=0.60). Our candidates descriptive only: dual_W30_k50 +0.0186/+0.0288/+0.0175 vs wait_W90/orb_W90/odasc (8/9 wins vs orb and odasc, Holm p=0.16-0.20); lawm_soft_W30 +0.011/+0.022/+0.010 |
| G6 | fail | no surviving method to ablate |
| G7 | pass | H3 (denoising the wait set recovers most of the wait->oracle gap) holds on Cabral test (10/10) AND on fresh ApacheJIT (9/9 projects vs wait_W90, Holm p=0.0078; gap recovered 0.90 of means; per project 0.75-0.98): results/statistics.json E8_secondary_* |
| G8 | pass | tests/test_no_future.py (future discoveries do not change past predictions for nowait/wait/orb/law/awt); dev/test project split fixed before modelling; decomp is a diagnostic using true labels, never a competitor |
| G9 | unknown |  |
| G10 | unknown |  |
| G11 | unknown |  |

## Last 10 decisions
- 2026-11-25T13:34:47+00:00: Session magical-bardeen resumed 2026-11-25: adopted zen-cray-ajbt81 state (most advanced: cycle 2, plan_v6 E0e running, plan_v7 pre-registered) into branch claude/magical-bardeen-9yglkz via merge -s ours; zen-cray's heartbeat was 12 min stale (session presumed stopped)
- 2026-11-25T13:34:47+00:00: Added scripts/freeze_v6.py and enqueue E8 (plan_v7 ApacheJIT confirmation, exactly the plan_v7 method list); ApacheJIT downloaded and sha256-verified; smoke test on the first 1200 kafka commits checked only that every method runs (no metrics inspected)
- 2026-11-25T14:53:00+00:00: Owner asked to continue from the most recent branch: adopted claude/magical-bardeen-9yglkz (cycle 2, heartbeat 28 min stale → session presumed stopped) into claude/keen-edison-jo222n via merge -s ours (keen-edison history kept). Keen-edison's parallel cycle-1 dev selection (E0b/E0c calibration/fsc/fixed-rate grids, dev only, never run on test) is kept under archive/keen_edison_cycle1/ for reference; its compute is not counted in this lineage's budget.json. Runners + autocommit relaunched on keen-edison.
- 2026-11-25T20:19:39+00:00: Cycle 3 started (cycle-2 budget 15 h exhausted). Re-queued 3 E0e nova jobs (skipped_budget); E3 (144 jobs, Cabral test robustness, test set already declared 'used' by plan_v7) stays skipped_budget until E8 is done
- 2026-11-25T20:59:35+00:00: plan_v6 freeze: dual=dual_W30_k50 (0.6812); lawm=lawm_soft_W30 (0.7551), odasc=odasc_W30_t0.8 (0.7598); primary (best dev) = odasc_W30_t0.8; H5 on dev: False
- 2026-11-25T21:00:02+00:00: E8 enqueued exactly as pre-registered in plan_v7 (9 ApacheJIT projects x 5 confirm seeds x 9 methods = 405 jobs) despite H5 being false on dev
- 2026-11-25T21:04:27+00:00: final_report E8/H6: the primary candidate (best dev mean) is odasc_W30_t0.8 itself, so the pre-registered 'primary vs odasc' test is a degenerate self-comparison; dropped, Holm over the 2 waiting baselines. Our own methods (dual_W30_k50, lawm_soft_W30) vs wait_W90/orb_W90/odasc are reported descriptively as pre-registered
- 2026-11-25T21:37:55+00:00: Gates: G5 stays fail (H6 failed on fresh data); G7 -> pass (H3 replicated on ApacheJIT 9/9). ApacheJIT declared used for confirmation. Next round (plan_v8, dev only): fix dual's nova failure with a principled latency-corrected neighbour posterior, then find an untouched confirmation dataset
- 2026-11-25T21:47:57+00:00: Adopted keen-edison (cycle 3) into zealous-lamport; zealous cycle-1 lineage archived; dreamy-fermat (cycle 2 copy of zealous) left on its branch
- 2026-11-25T21:47:57+00:00: Wrote SUBMISSION_READINESS.md in answer to the owner's request for a final submission

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

## Untouched confirmation data (needed after ApacheJIT was used by E8, 2026-11-25)
- JIT-Defects4J (Ni et al., 2022; built on Herbold et al.'s LLTC4J): 21 Java projects, 2,332 buggy / 24,987 clean commits. Buggy commits come from manually labelled fix lines via git blame, so fix commits (and their dates) can in principle be recovered via git. NOT yet checked whether the released files contain the bug->fix link; that would need data engineering (clone repos for timestamps).
- ApacheJIT projects excluded by plan_v7 for size (<2000 commits: spark, zeppelin, mapreduce, zookeeper): untouched but small, weak.
- Defectors (Zenodo 10.5281/zenodo.7708984): file-level Python dataset, not commit-level JIT -> probably unsuitable (UNVERIFIED).

