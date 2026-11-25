# HANDOFF — read this first
*Auto-generated 2026-11-25T10:19:45+00:00 by scripts/write_handoff.py*

## Where we are
- **Status:** RUNNING   **Cycle:** 2 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** cycle 2: finishing frozen E2/E3; diagnosing latency cost (operating point vs ranking); searching fresh confirmation data
- **Last action:** E1 analysed (G5 fail vs ODaSC); 332 skipped jobs re-queued for cycle 2
- **NEXT ACTION:** Let E2/E3 finish (bash scripts/launch_runner.sh 3); find fresh projects with discovery times for a new untouched confirmation set; dev-only diagnostics of ranking headroom (delay depends on x?)

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 996, 'pending': 332}; running jobs: none
- Processes: `390 tmux new-session -d -s research_w0 python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
391 bash -c python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
393 python3 run_all.py --mode full --resume --worker 0
397 bash -c python3 run_all.py --mode full --resume --worker 1 >> logs/runner_w1.log 2>&1
400 python3 run_all.py --mode full --resume --worker 1
403 bash -c python3 run_all.py --mode full --resume --worker 2 >> logs/runner_w2.log 2>&1
405 python3 run_all.py --mode full --resume --worker 2`
- Heartbeat age: 1543s

## Compute
- Cycle 2: 0.00 h / 15 h   Global: 15.04 h / 120 h (CPU-hours; machine has no GPU)

## Gate status (Section 7)
| Gate | Status | Evidence |
|---|---|---|
| G1 | pass (marginal; caveat stated) | journal_selection/selected_journal.md — median 71 d (12 m) / 74 d (24 m); 2025 quartile UNVERIFIED |
| G2 | unknown |  |
| G3 | unknown |  |
| G4 | unknown |  |
| G5 | fail | results/statistics.json E1: LAW vs ODaSC-W30 +0.0009, CI [-0.0086,0.0114], Holm p=1.0 (wins vs waiting-time family pass) |
| G6 | fail (partial) | E2 partial: Lagakos vs naive +0.0001 (no effect); threshold +0.0687; model prior +0.016 |
| G7 | unknown |  |
| G8 | pass | tests/test_no_future.py (future discoveries do not change past predictions); dev/test split by project; features commit-time |
| G9 | unknown |  |
| G10 | unknown |  |
| G11 | unknown |  |

## Last 10 decisions
- 2026-11-24T23:02:09+00:00: plan_v2: add ODaSC-style baseline (batch adaptation: kNN label confidence at labelling time, delta=0.9, k=50, pool=5000 recent labelled commits) tuned over W in {15,30,60,90,180} on dev = 5 configs, same budget as wait/orb
- 2026-11-24T23:02:09+00:00: plan_v2: LAW configuration for E1 chosen on dev from its 4 E0 variants (best mean dev G-mean), instead of the plan_v1 pre-specified lagakos+model
- 2026-11-24T23:02:09+00:00: Runner fix: a restarted worker now resets its own stale 'running' jobs
- 2026-11-24T23:04:02+00:00: Test projects are not touched until the selected LAW variant beats the best baseline (incl. ODaSC) on dev
- 2026-11-24T23:13:20+00:00: 6.4 ladder rung 3-4: enqueue E0c (dev only, 252 runs): thr_policy in {ratematch (H3 as pre-written), gmax_lat (latency-corrected G-mean threshold)} for nowait and LAW-base; gmax_lat for all 15 wait/orb/odasc configs
- 2026-11-25T00:25:33+00:00: E0c extended with law_{lagakos,naive}_model_gmax_lat (24 runs, dev only)
- 2026-11-25T00:25:33+00:00: Runner: dead-worker resets refund the attempt; enqueue.py takes the queue lock
- 2026-11-25T07:54:45+00:00: FROZEN (plan_v3): proposed = LAW lagakos+model with latency-corrected G-mean threshold; comparators nowait, wait_W90, orb_W90, odasc_W30 (primary), wait_W30_gmax_lat, odasc_W15_gmax_lat
- 2026-11-25T10:19:45+00:00: Cycle 2 starts (cycle-1 budget of 15 CPU-h exhausted at 15.04 h). Finish frozen plan_v3 E2/E3 (332 skipped_budget jobs) first
- 2026-11-25T10:19:45+00:00: Consolidated on lineage claude/zealous-lamport-bjc4um (latest, 73 commits: E0 done, plan_v3 frozen, E1 done). Fast-forwarded working branch claude/dreamy-fermat-7983nm to it. Branches zen-cray (cycle-2 JKSU benchmark, owner directive), keen-edison and magical-bardeen were parallel forks from the same handoff and are NOT merged; useful items will be ported explicitly

## Last failures (journal entries)
- journal/ENTRIES/20261125T101945_FAILURE_the_primary_hypothesis_fails_on_held_out_data__and.md

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
| Keep runner alive + auto-commit (ephemeral container) | `bash scripts/watch_and_checkpoint.sh` |
| Snapshot backup | `bash scripts/snapshot.sh` |

## Moving to a new account / machine
1. Everything lives in git on branch `claude/zealous-lamport-bjc4um` of `bhargavteja-9779/p_c1_15` (pushed after every step; the earlier branch claude/dreamy-fermat-7983nm holds history up to the first handoff).
2. On the new machine: `git clone` that repo, `git checkout claude/zealous-lamport-bjc4um`, `pip install -r project/requirements.txt`.
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

