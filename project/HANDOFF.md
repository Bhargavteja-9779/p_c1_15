# HANDOFF — read this first
*Auto-generated 2026-11-28T19:07:12+00:00 by scripts/write_handoff.py*

## Where we are
- **Status:** RUNNING   **Cycle:** 2 / 12   **Phase:** PHASE5_RUN   **Pivots:** 0 / 3
- **Step:** cycle 2 closing: E2/E3 finishing; honest exit decided (see decisions.md)
- **Last action:** E7/E8/E10 analysed; G9 fresh-clone 97/97; blind novelty 13/25 (self 12); manuscript draft paper/manuscript.md
- **NEXT ACTION:** Relaunch runner (bash scripts/launch_runner.sh 4) until E2/E3 done; python scripts/final_report.py && python scripts/paper_numbers.py; fill {{E2_TABLE}}/{{E3_TEXT}} in paper/manuscript.md; run 3-reviewer panel; scripts/audit_numbers.py; write FINAL_REPORT.md (honest exit); set status FINISHED

- **Selected journal:** JKSU-CIS (Springer Nature, ISSN 1319-1578, IF 6.4 2025; turnaround median 71–74 d, marginal)
- **Topic:** Verification-latency-aware online JIT-SDP: latency-aware weighting (LAW) of provisionally-clean commits
- **Hypothesis:** LAW beats the best tuned waiting-time baseline by >=0.02 G-mean on 10 held-out projects (Holm p<0.05)

## Running right now
- Queue (full): {'done': 2518, 'running': 4, 'pending': 40}; running jobs: ['E3_tomcat_wait_W90_ds2_s101', 'E3_tomcat_wait_W90_ds2_s102', 'E3_tomcat_wait_W90_ds2_s103', 'E3_tomcat_wait_W90_ds2_s104']
- Processes: `893 tmux new-session -d -s research_w0 python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
894 bash -c python3 run_all.py --mode full --resume --worker 0 >> logs/runner_w0.log 2>&1
896 python3 run_all.py --mode full --resume --worker 0
900 bash -c python3 run_all.py --mode full --resume --worker 1 >> logs/runner_w1.log 2>&1
903 python3 run_all.py --mode full --resume --worker 1
906 bash -c python3 run_all.py --mode full --resume --worker 2 >> logs/runner_w2.log 2>&1
908 python3 run_all.py --mode full --resume --worker 2
1021 bash -c python3 run_all.py --mode full --resume --worker 3 >> logs/runner_w3.log 2>&1
1023 python3 run_all.py --mode full --resume --worker 3`
- Heartbeat age: 0s

## Compute
- Cycle 2: 11.48 h / 15 h   Global: 26.51 h / 120 h (CPU-hours; machine has no GPU)

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
- 2026-11-25T10:19:45+00:00: Cycle 2 starts (cycle-1 budget of 15 CPU-h exhausted at 15.04 h). Finish frozen plan_v3 E2/E3 (332 skipped_budget jobs) first
- 2026-11-25T10:19:45+00:00: Consolidated on lineage claude/zealous-lamport-bjc4um (latest, 73 commits: E0 done, plan_v3 frozen, E1 done). Fast-forwarded working branch claude/dreamy-fermat-7983nm to it. Branches zen-cray (cycle-2 JKSU benchmark, owner directive), keen-edison and magical-bardeen were parallel forks from the same handoff and are NOT merged; useful items will be ported explicitly
- 2026-11-25T10:25:36+00:00: Prior art: Recalibration-vs-Retraining JIT-SDP study (Zenodo 24527309, 2026-11-25) logged as HIGH threat to an operating-point claim
- 2026-11-25T10:26:41+00:00: plan_v4: E7 latency-cost decomposition (H5) on 18 non-dev projects and E8 frozen replication (H6) on 8 fresh ApacheJIT projects
- 2026-11-25T10:28:10+00:00: E9 dev grid: inspection policies {rand, top, unc} x budgets {2%,5%} x base methods {nowait_gmax_lat, LAW, ODaSC_W30}; 162 dev runs; all counted as variants
- 2026-11-28T16:43:45+00:00: E9 analysed on dev: H7 and H8 refuted; no inspection variant is promoted to confirmation
- 2026-11-28T16:54:49+00:00: plan_v5: E7b completes H5 on all 5 confirmation seeds (336 jobs); E10/H9 tests threshold-vs-label-policy on ApacheJIT (200 jobs)
- 2026-11-28T17:53:28+00:00: H5 reported as heterogeneous (supported on Cabral-test, refuted on ApacheJIT); no post-hoc redefinition of the window is tested on these data as confirmation
- 2026-11-28T18:18:12+00:00: End of cycle 2: take the HONEST EXIT (Section 11.7) after finishing E2/E3, the manuscript, one review round, audit and reproducibility check, instead of starting cycle 3 / pivot 1
- 2026-11-28T18:18:17+00:00: Correction to the previous entry: compute used at that time was 23.35 CPU-h global (cycle 2: 8.32 h), not about 21

## Last failures (journal entries)
- journal/ENTRIES/20261125T101945_FAILURE_the_primary_hypothesis_fails_on_held_out_data__and.md
- journal/ENTRIES/20261128T165402_FAILURE_h6_fails__no_replication_of_the_e1_wins.md
- journal/ENTRIES/20261125T102820_DEAD END_a_feature_dependent_discovery_delay_model.md
- journal/ENTRIES/20261128T164345_DEAD END_choosing_which_commits_to_inspect.md

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

