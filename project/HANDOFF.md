# HANDOFF — read this first
*Auto-generated 2026-11-24T03:35:48+00:00 by scripts/write_handoff.py*

## Where we are
- **Status:** RUNNING   **Cycle:** 1 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** E0 dev tuning partially done; session handed off to a new account at user request
- **Last action:** Saved literature matrix (13 JKSU-CIS papers), Frontiers check (selection unchanged), novelty threats (ODaSC, Liu 2024a) logged; partial E0 results committed
- **NEXT ACTION:** 1) cd project && pip install -r requirements.txt && python scripts/get_data.py && python scripts/status.py. 2) Relaunch E0: bash scripts/launch_runner.sh 3 (jobs left "running" by the dead container are reset to pending automatically). 3) Meanwhile READ Liu et al. 2024a (Empir Softw Eng 29(5):98, PU learning for JIT-SDP) and the rest of ODaSC (Song_IJCNN2022.txt: results table, waiting time) and update state/novelty_ledger.json claims; if Liu 2024a pre-empts LAW, apply Section 6.4/6.5. 4) Write plan_v2 adding ODaSC (reimplementation) as a baseline with equal tuning budget, reason logged. 5) After E0 completes: python scripts/freeze_config.py, then enqueue E1-E3 (+ODaSC) and launch; then scripts/final_report.py.

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 93, 'running': 3, 'pending': 96}; running jobs: ['E0_neutron_wait_W90_s0', 'E0_neutron_wait_W90_s1', 'E0_neutron_wait_W90_s2']
- Processes: `1258 tmux new-session -d -s research_w0 python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
1259 bash -c python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
1261 python3 run_all.py --mode full --resume --worker 0
1265 bash -c python3 run_all.py --mode full --resume --worker 1 >> logs/runner_w1.log 2>&1
1268 python3 run_all.py --mode full --resume --worker 1
1271 bash -c python3 run_all.py --mode full --resume --worker 2 >> logs/runner_w2.log 2>&1
1273 python3 run_all.py --mode full --resume --worker 2`
- Heartbeat age: 4s

## Compute
- Cycle 1: 0.60 h / 15 h   Global: 0.60 h / 120 h (CPU-hours; machine has no GPU)

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
- 2026-11-24T03:04:37+00:00: Place project in repo subfolder project/ on branch claude/dreamy-fermat-7983nm
- 2026-11-24T03:04:37+00:00: Hardware: CPU-only (4 cores, 15 GB RAM, no CUDA/MPS). All compute budgets are counted as CPU-hours.
- 2026-11-24T03:11:07+00:00: Selected journal: Journal of King Saud University – Computer and Information Sciences (Springer Nature, ISSN 1319-1578, IF 6.4 (2025))
- 2026-11-24T03:11:07+00:00: Interpretation: "submission→acceptance ≤ 72" evaluated as the MEDIAN (Accepted−Received) of a random sample
- 2026-11-24T03:22:41+00:00: Topic: verification-latency-aware online JIT-SDP (latency-aware weighting, LAW)
- 2026-11-24T03:22:41+00:00: Dev/test split by project: dev={fabric,neutron,nova,sentry}, test=other 10 (rng seed 0 draw before modelling)
- 2026-11-24T03:22:41+00:00: Primary metric G-mean over the evaluation window (commits from #500 to last-365-days), against final labels
- 2026-11-24T03:22:41+00:00: Runner parallelised to 3 workers (cores-1); budget counts summed worker seconds (CPU-time-like)
- 2026-11-24T03:35:03+00:00: User allowed Frontiers journals; checked Frontiers in AI (median 78 d), Big Data (74 d), Computer Science (100 d)

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

