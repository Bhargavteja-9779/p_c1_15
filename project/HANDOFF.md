# HANDOFF — read this first
*Auto-generated 2026-11-24T04:05:26+00:00 by scripts/write_handoff.py*

## Where we are
- **Status:** RUNNING   **Cycle:** 1 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** E0 + E0b (plan_v2 dev diagnostics) running; LAW failing on dev, diagnosed
- **Last action:** New account resumed; E0 relaunched; Liu 2024a UNVERIFIED; LAW dev failure diagnosed (feedback loop + uninformative age posterior); plan_v2 with awt + decomposition enqueued
- **NEXT ACTION:** 1) If container restarted: pip install -r requirements.txt && python scripts/get_data.py && bash scripts/launch_runner.sh 3. 2) Wait for E0 + E0b (dev only) to finish (python scripts/status.py). 3) Analyse E0b: decomposition (H2a) and awt vs best fixed W on dev; write RESULT journal entries. 4) Update scripts/freeze_config.py for plan_v2 rule (candidate chosen on dev among law_*/awt_*), freeze, enqueue E1 (+E3 diag) on test, launch. 5) Continue prior-art queries for C3/C4 (need >=8 phrasings each).

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 126, 'pending': 158, 'running': 4}; running jobs: ['E0_sentry_wait_W15_s0', 'E0_sentry_orb_W90_s1', 'E0_sentry_orb_W90_s2', 'E0_sentry_law_lagakos_base_s2']
- Processes: `509 tmux new-session -d -s research_w0 python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
510 bash -c python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
512 python3 run_all.py --mode full --resume --worker 0
516 bash -c python3 run_all.py --mode full --resume --worker 1 >> logs/runner_w1.log 2>&1
519 python3 run_all.py --mode full --resume --worker 1
522 bash -c python3 run_all.py --mode full --resume --worker 2 >> logs/runner_w2.log 2>&1
524 python3 run_all.py --mode full --resume --worker 2`
- Heartbeat age: 3s

## Compute
- Cycle 1: 1.06 h / 15 h   Global: 1.06 h / 120 h (CPU-hours; machine has no GPU)

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
- 2026-11-24T03:11:07+00:00: Selected journal: Journal of King Saud University – Computer and Information Sciences (Springer Nature, ISSN 1319-1578, IF 6.4 (2025))
- 2026-11-24T03:11:07+00:00: Interpretation: "submission→acceptance ≤ 72" evaluated as the MEDIAN (Accepted−Received) of a random sample
- 2026-11-24T03:22:41+00:00: Topic: verification-latency-aware online JIT-SDP (latency-aware weighting, LAW)
- 2026-11-24T03:22:41+00:00: Dev/test split by project: dev={fabric,neutron,nova,sentry}, test=other 10 (rng seed 0 draw before modelling)
- 2026-11-24T03:22:41+00:00: Primary metric G-mean over the evaluation window (commits from #500 to last-365-days), against final labels
- 2026-11-24T03:22:41+00:00: Runner parallelised to 3 workers (cores-1); budget counts summed worker seconds (CPU-time-like)
- 2026-11-24T03:35:03+00:00: User allowed Frontiers journals; checked Frontiers in AI (median 78 d), Big Data (74 d), Computer Science (100 d)
- 2026-11-24T04:05:16+00:00: plan_v2: add E0b dev diagnostics (awt eps grid, decomposition with true labels); LAW kept as pre-specified but recorded as failing on dev
- 2026-11-24T04:05:16+00:00: Liu et al. 2024a ('PU learning for JIT-SDP', EMSE 29(5):98) marked UNVERIFIED
- 2026-11-24T04:05:16+00:00: ODaSC baseline reimplementation deferred

## Last failures (journal entries)
- journal/ENTRIES/20261124T040516_FAILURE_the_pre_specified_law_method_loses_to_a_tuned_wait.md

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

