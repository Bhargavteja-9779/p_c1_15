# Verification-latency-aware online JIT defect prediction

Research code for the study described in `topic/selected_topic.md` (state of the project: `HANDOFF.md`).

## Setup
```bash
pip install -r requirements.txt
```
Data: the Cabral et al. (ICSE 2019) artifact, Zenodo record 2591761 (`spdisc-icse19-V1.02.zip`). The data folder is git-ignored; fetch the 14 ARFF files with:
```bash
python scripts/get_data.py        # Cabral et al. (14 projects)
python scripts/get_apachejit.py   # ApacheJIT (Zenodo 5907847), sha256-checked
```

## Reproduce
```bash
python tests/test_no_future.py                 # leakage + estimator tests
python run_all.py --mode quick                 # smoke test (<1 min)
python scripts/enqueue.py E0 && bash scripts/launch_runner.sh 3   # dev tuning (detached)
python scripts/freeze_config.py                # choose W* on dev projects only
python scripts/enqueue.py E1 && python scripts/enqueue.py E2 && python scripts/enqueue.py E3 && bash scripts/launch_runner.sh 3
# Every job ever queued (E0-E10, D1) is exported per experiment to experiments/specs/<EXP>.json; e.g. the
# plan_v4/v5 ApacheJIT replication, latency-cost decomposition and threshold study:
python scripts/enqueue_list.py experiments/specs/E8.json 6 && python scripts/enqueue_list.py experiments/specs/E7.json 7 && python scripts/enqueue_list.py experiments/specs/E10.json 9
bash scripts/launch_runner.sh 3
python scripts/final_report.py                 # tables/, figures/, results/statistics.json, RESULTS_SUMMARY.md
python scripts/paper_numbers.py                # derived numbers quoted in the paper (results/paper_numbers.json)
python scripts/reproduce_check.py              # re-runs one stored job per experiment x variant and compares (G9)
python scripts/audit_numbers.py                # every number in paper/manuscript.md traced to a result file
```
Each job is one prequential simulation (`src/jit.py: simulate`); results are appended to `results/raw_results.jsonl`.
