# HANDOFF — read this first
*Auto-generated 2026-11-25T07:55:59+00:00 by scripts/write_handoff.py*

## Where we are
- **Status:** RUNNING   **Cycle:** 1 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** E1-E3 confirmation running on 10 held-out projects (frozen plan_v3)
- **Last action:** Dev tuning complete (528 runs, 44 variants); frozen plan_v3: LAW lagakos+model+gmax_lat vs 6 baselines; E1/E2/E3 enqueued
- **NEXT ACTION:** 1) Keep runners alive: bash scripts/watch_and_checkpoint.sh (relaunches workers, commits every 5 min). If cycle-1 budget (15 h) runs out, remaining jobs become skipped_budget: set cycle=2 in state/agent_state.json, reset skipped_budget->pending, relaunch. 2) When E1 is done: update scripts/final_report.py for plan_v3 (primary = law_lagakos_model_gmax_lat vs odasc_W30, Holm over 6 baselines, bootstrap CI, 0.02 margin) and run it. 3) Update gates G4-G8, novelty score, journal RESULT entry; then 6.4/Section 11 decision.

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 528, 'pending': 800}; running jobs: none
- Processes: `none`
- Heartbeat age: 17s

## Compute
- Cycle 1: 10.09 h / 15 h   Global: 10.09 h / 120 h (CPU-hours; machine has no GPU)

## Gate status (Section 7)
| Gate | Status | Evidence |
|---|---|---|
| G1 | pass (marginal; caveat stated) | journal_selection/selected_journal.md — median 71 d (12 m) / 74 d (24 m); 2025 quartile UNVERIFIED |
| G2 | unknown |  |
| G3 | unknown |  |
| G4 | unknown |  |
| G5 | unknown |  |
| G6 | unknown |  |
| G7 | unknown |  |
| G8 | unknown |  |
| G9 | unknown |  |
| G10 | unknown |  |
| G11 | unknown |  |

## Last 10 decisions
- 2026-11-24T03:35:03+00:00: User allowed Frontiers journals; checked Frontiers in AI (median 78 d), Big Data (74 d), Computer Science (100 d)
- 2026-11-24T23:02:09+00:00: Liu et al. 2024a (PU learning for JIT-SDP, EMSE 29(5):98) marked UNVERIFIED / not found
- 2026-11-24T23:02:09+00:00: plan_v2: add ODaSC-style baseline (batch adaptation: kNN label confidence at labelling time, delta=0.9, k=50, pool=5000 recent labelled commits) tuned over W in {15,30,60,90,180} on dev = 5 configs, same budget as wait/orb
- 2026-11-24T23:02:09+00:00: plan_v2: LAW configuration for E1 chosen on dev from its 4 E0 variants (best mean dev G-mean), instead of the plan_v1 pre-specified lagakos+model
- 2026-11-24T23:02:09+00:00: Runner fix: a restarted worker now resets its own stale 'running' jobs
- 2026-11-24T23:04:02+00:00: Test projects are not touched until the selected LAW variant beats the best baseline (incl. ODaSC) on dev
- 2026-11-24T23:13:20+00:00: 6.4 ladder rung 3-4: enqueue E0c (dev only, 252 runs): thr_policy in {ratematch (H3 as pre-written), gmax_lat (latency-corrected G-mean threshold)} for nowait and LAW-base; gmax_lat for all 15 wait/orb/odasc configs
- 2026-11-25T00:25:33+00:00: E0c extended with law_{lagakos,naive}_model_gmax_lat (24 runs, dev only)
- 2026-11-25T00:25:33+00:00: Runner: dead-worker resets refund the attempt; enqueue.py takes the queue lock
- 2026-11-25T07:54:45+00:00: FROZEN (plan_v3): proposed = LAW lagakos+model with latency-corrected G-mean threshold; comparators nowait, wait_W90, orb_W90, odasc_W30 (primary), wait_W30_gmax_lat, odasc_W15_gmax_lat

## Last failures (journal entries)
- none yet

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

