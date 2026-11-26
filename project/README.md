# Where does verification latency hurt online JIT defect prediction?

Code, data pointers, frozen plans and results for the manuscript in `paper/manuscript.md`. Tested with Python 3.13 on Linux (CPU only, 4 cores).

## Setup
```bash
pip install -r requirements.txt
```
Data: the Cabral et al. (ICSE 2019) artifact, Zenodo record 2591761 (`spdisc-icse19-V1.02.zip`). The data folder is git-ignored; fetch the 14 ARFF files with:
```bash
python scripts/get_data.py
```

## Reproduce
```bash
python tests/test_no_future.py                 # leakage + estimator tests
python run_all.py --mode quick                 # smoke test (<1 min)
python scripts/enqueue.py E0 && bash scripts/launch_runner.sh 3   # dev tuning (detached)
python scripts/freeze_config.py                # choose W* on dev projects only
python scripts/enqueue.py E1 && python scripts/enqueue.py E2 && python scripts/enqueue.py E3 && bash scripts/launch_runner.sh 3
python scripts/final_report.py                 # tables/, figures/, results/statistics.json, RESULTS_SUMMARY.md
python scripts/audit_numbers.py                # every number in paper/manuscript.md traced to a result file
```
Each job is one prequential simulation (`src/jit.py: simulate`); results are appended to `results/raw_results.jsonl`.

## Reproducing the paper

**Fast path (no simulation, ~1 min):** all simulation outputs are committed (`results/raw_results.jsonl`, `results/review1/raw.jsonl`, `archive/zealous_lamport_cycle1/results/raw_results.jsonl`). Regenerate every table, figure and number of the manuscript and check them:
```bash
python scripts/get_data.py            # Cabral (ARFF checksums asserted) + ApacheJIT (zip checksum asserted)
python scripts/review1_shapley.py     # 2x2 / Shapley decomposition (Table 3b)
python scripts/paper_numbers.py       # paper/tables/*.md, paper/figures/*.png, results/paper_numbers.json
python scripts/audit_paper_strict.py  # every number in the manuscript traced to a declared source (must print Unmatched: 0)
python tests/test_no_future.py && python tests/test_no_future_threshold_rules.py   # leakage tests
```

**Full re-simulation** (order matters: development runs, then freeze, then confirmation). CPU-hours are for 1 core.

| Manuscript item | Experiments | Commands | approx. CPU-h |
|---|---|---|---|
| Dev tuning (Sect. 4.3) | E0, E0b, E0c, E0d, E0e (dev projects) | `python scripts/enqueue.py E0` (same for E0b, E0c, E0d, E0e) `&& bash scripts/launch_runner.sh 3`, then `python scripts/freeze_config.py`, `python scripts/freeze_v5.py`, `python scripts/freeze_v6.py` | 12 |
| Table 4 (RQ3) | E1 (Cabral test) | `python scripts/enqueue.py E1 && bash scripts/launch_runner.sh 3` | 4 |
| Table 3, Cabral column (RQ2) | E3b (Cabral test) | `python scripts/enqueue.py E3b && bash scripts/launch_runner.sh 3` | 4 |
| Table 3, ApacheJIT column; Table 5 (RQ4) | E8 (ApacheJIT) | `python scripts/enqueue.py E8 && bash scripts/launch_runner.sh 3` | 3 |
| Tables 3b/8/9, A5 (review round 1) | A2-A5 (plan_v8) | `python scripts/review1_runs.py 3` | 8 |
| Table 6 (RQ5 diagnostic) | lineage 2, dev | `python archive/zealous_lamport_cycle1/scripts/diag_operating_point.py fabric,neutron` (run from `archive/zealous_lamport_cycle1/` with `data/` linked) | 0.2 |
| Table 7 (RQ5 confirmation, Cabral) | lineage 2, E1 | `python scripts/reproduce_table7.py` (compares with the archived values) | 3 |

Then run the fast path. `run_all.py --mode quick` is a smoke test of the queue infrastructure (a few minutes).
Plans that fixed each configuration before its confirmatory run: `experiments/plan_v1.yaml` … `plan_v8_review1.yaml` (main lineage) and `archive/zealous_lamport_cycle1/experiments/plan_v1-v3.yaml` (lineage 2). Every configuration evaluated is listed in `state/variants_tried.csv` and `archive/zealous_lamport_cycle1/state/variants_tried.csv`.
