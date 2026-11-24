# HANDOFF — read this first
*Auto-generated 2026-11-24T21:27:40+00:00 by scripts/write_handoff.py*

## Where we are
- **Status:** RUNNING   **Cycle:** 1 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** E0 (rest) + E0b dev grid running (plan_v2)
- **Last action:** plan_v2 written; thr_cal + fsc implemented, leakage test extended (passes); E0b enqueued (324 jobs); workers relaunched
- **NEXT ACTION:** 1) python scripts/status.py; if workers dead: bash scripts/launch_runner.sh 3. 2) While E0/E0b run: prior-art work for G2 (>=30 papers opened; claims now: threshold-calibration under verification latency, waiting-time-as-operating-point insight); log in state/novelty_ledger.json. 3) When E0+E0b done: update scripts/freeze_config.py for plan_v2 (wait/orb/fsc W*, wait+lat W*, fsc+lat W*), run it, extend scripts/enqueue.py E1/E2/E3 per plan_v2, enqueue and launch. 4) Then scripts/final_report.py, statistics, gates.

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 152, 'pending': 361, 'running': 3}; running jobs: ['E0_nova_law_naive_model_s0', 'E0_nova_law_naive_model_s1', 'E0_nova_law_naive_base_s2']
- Processes: `1033 tmux new-session -d -s research_w0 python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
1034 bash -c python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
1036 python3 run_all.py --mode full --resume --worker 0
1040 bash -c python3 run_all.py --mode full --resume --worker 1 >> logs/runner_w1.log 2>&1
1042 python3 run_all.py --mode full --resume --worker 1
1046 bash -c python3 run_all.py --mode full --resume --worker 2 >> logs/runner_w2.log 2>&1
1048 python3 run_all.py --mode full --resume --worker 2`
- Heartbeat age: 18s

## Compute
- Cycle 1: 1.92 h / 15 h   Global: 1.92 h / 120 h (CPU-hours; machine has no GPU)

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
- 2026-11-24T03:22:41+00:00: Topic: verification-latency-aware online JIT-SDP (latency-aware weighting, LAW)
- 2026-11-24T03:22:41+00:00: Dev/test split by project: dev={fabric,neutron,nova,sentry}, test=other 10 (rng seed 0 draw before modelling)
- 2026-11-24T03:22:41+00:00: Primary metric G-mean over the evaluation window (commits from #500 to last-365-days), against final labels
- 2026-11-24T03:22:41+00:00: Runner parallelised to 3 workers (cores-1); budget counts summed worker seconds (CPU-time-like)
- 2026-11-24T03:35:03+00:00: User allowed Frontiers journals; checked Frontiers in AI (median 78 d), Big Data (74 d), Computer Science (100 d)
- 2026-11-24T21:02:13+00:00: Work continues on branch claude/keen-edison-jo222n (this session's assigned branch; same history as claude/dreamy-fermat-7983nm at b18fc8e)
- 2026-11-24T21:02:13+00:00: Runner fix: on start a worker resets its OWN jobs left 'running' (worker id == self) to pending
- 2026-11-24T21:02:13+00:00: Liu et al. 2024a (PU learning for JIT-SDP) marked UNVERIFIED; generic PU framing of clean commits conceded as prior art; LAW claim narrowed to age/delay-distribution weighting in the online setting
- 2026-11-24T21:27:40+00:00: plan_v2 adopted: adds latency-corrected threshold calibration (thr_cal), ODaSC-inspired fsc baseline, E0b dev grid (324 runs); PROPOSED fixed in advance = law_lagakos_model + thr_cal_lat; plan_v1 E1-E3 dropped
- 2026-11-24T21:27:40+00:00: E0 jobs interrupted at 152/192 to load new code (3 running jobs reset and re-run, no results lost)

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
| Snapshot backup | `bash scripts/snapshot.sh` |

## Moving to a new account / machine
1. Everything lives in git on branch `claude/dreamy-fermat-7983nm` of `bhargavteja-9779/p_c1_15` (pushed after every step).
2. On the new machine: `git clone` that repo, `git checkout claude/dreamy-fermat-7983nm`, `pip install -r project/requirements.txt`.
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

