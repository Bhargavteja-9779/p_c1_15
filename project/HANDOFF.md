# HANDOFF — read this first
*Auto-generated 2026-11-24T13:21:32+00:00 by scripts/write_handoff.py*

## Where we are
- **Status:** RUNNING   **Cycle:** 1 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** E1/E3b/E3/E2 on test projects running (frozen config, SEEDS_CONFIRM)
- **Last action:** E0b done: H2a refuted (denoising closes 95% of wait30->oracle gap on dev); awt dead end; config frozen; plan_v3 pre-registers H3; test runs launched
- **NEXT ACTION:** 1) If container restarted: pip install -r requirements.txt && python scripts/get_data.py && bash scripts/launch_runner.sh 3 && tmux new -d -s autocommit 'bash scripts/autocommit.sh'. 2) When E1/E3b finish: python scripts/final_report.py (update for E3b + H3), write RESULT entries, fill gates. 3) Cycle 2 (plan_v4): method that identifies dormant bugs among OLD provisional negatives from features without self-confirmation (e.g. scorer trained only on mature labels; co-teaching style), dev only first; add ODaSC baseline. 4) More prior-art for C3 (noise-dominance) incl. dormant-defects TOSEM 2021 full text.

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 294, 'pending': 941, 'running': 3}; running jobs: ['E1_brackets_law_lagakos_model_s101', 'E1_brackets_law_lagakos_model_s102', 'E1_brackets_law_lagakos_model_s103']
- Processes: `785 tmux new-session -d -s research_w0 python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
786 bash -c python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
788 python3 run_all.py --mode full --resume --worker 0
792 bash -c python3 run_all.py --mode full --resume --worker 1 >> logs/runner_w1.log 2>&1
794 python3 run_all.py --mode full --resume --worker 1
798 bash -c python3 run_all.py --mode full --resume --worker 2 >> logs/runner_w2.log 2>&1
800 python3 run_all.py --mode full --resume --worker 2`
- Heartbeat age: 3s

## Compute
- Cycle 1: 5.41 h / 15 h   Global: 5.41 h / 120 h (CPU-hours; machine has no GPU)

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
- 2026-11-24T03:22:41+00:00: Runner parallelised to 3 workers (cores-1); budget counts summed worker seconds (CPU-time-like)
- 2026-11-24T03:35:03+00:00: User allowed Frontiers journals; checked Frontiers in AI (median 78 d), Big Data (74 d), Computer Science (100 d)
- 2026-11-24T04:05:16+00:00: plan_v2: add E0b dev diagnostics (awt eps grid, decomposition with true labels); LAW kept as pre-specified but recorded as failing on dev
- 2026-11-24T04:05:16+00:00: Liu et al. 2024a ('PU learning for JIT-SDP', EMSE 29(5):98) marked UNVERIFIED
- 2026-11-24T04:05:16+00:00: ODaSC baseline reimplementation deferred
- 2026-11-24T04:06:17+00:00: Reset orphaned queue record E0_sentry_law_lagakos_base_s2 to pending
- 2026-11-24T12:46:15+00:00: Reset 96 E0b jobs to pending and relaunched workers
- 2026-11-24T13:19:54+00:00: plan_v2 rule outcome: no candidate (law_*, awt_*) beats best dev baseline -> E1 runs on test as pre-registered NEGATIVE-RESULT confirmation
- 2026-11-24T13:19:55+00:00: Frozen config: wait W*=90, orb W*=90, best dev baseline=orb_W90
- 2026-11-24T13:20:12+00:00: plan_v3 written and E1, E3b, E3, E2 enqueued on test projects (first test touch)

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

